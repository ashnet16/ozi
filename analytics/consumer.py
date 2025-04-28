import duckdb
import logging
import json
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from consumers.base import Consumer
from consumers.config import ANALYTICS_TOPIC, BATCH_SIZE, EMBEDDER_TOPIC
from table_queries import create_casts_table, create_comments_table, create_reactions_table

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class KafkaAnalyticsConsumer(Consumer):
    def __init__(self, topics=[ANALYTICS_TOPIC], group_id="ozi-analytics-consumer-group"):
        super().__init__(
            end_point="kafka:29092", topic_name=topics, consumer_group=group_id
        )
        self.topics = topics

        self.consumer = KafkaConsumer(
            *self.topics,
            bootstrap_servers=[self.end_point],
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )

        self.conn = duckdb.connect("duckdb_data/ozi.duckdb")
        self.ensure_tables_exist()
        self.cast_buffer = []
        self.comment_buffer = []
        self.reaction_buffer = []

    def ensure_tables_exist(self):
        logger.info("Ensuring DuckDB tables exist...")
        self.conn.execute(create_casts_table())
        self.conn.execute(create_comments_table())
        self.conn.execute(create_reactions_table())
        logger.info("DuckDB tables ready!")

    def process(self, msg):
        try:
            event_type = msg.get("message_subtype")
            if event_type == "CAST_ADD":
                parent_cast = (
                    msg.get("raw", {})
                    .get("merge_message_body", {})
                    .get("message", {})
                    .get("data", {})
                    .get("cast_add_body", {})
                    .get("parent_cast_id")
                )

                if parent_cast:
                    self.comment_buffer.append(self.prepare_comment_record(msg))
                else:
                    self.cast_buffer.append(self.prepare_cast_record(msg))

            elif event_type == "REACTION_ADD":
                self.reaction_buffer.append(self.prepare_reaction_record(msg))
            else:
                logger.warning(f"Unknown event_type: {event_type}")

        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")

    def prepare_cast_record(self, msg):
        msg_raw = msg["raw"]
        msg_body = msg_raw["merge_message_body"]["message"]["data"]
        cast_info = msg.get("cast", {})

        return (
            int(msg_raw["id"]),
            msg.get("message_subtype", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg_body["timestamp"]),
            cast_info.get("text", ""),
            cast_info.get("language", ""),
            json.dumps(cast_info.get("embeds", [])),
            json.dumps(cast_info.get("mentions", [])),
            msg.get("message_hash", "")
        )

    def prepare_comment_record(self, msg):
        msg_raw = msg["raw"]
        msg_body = msg_raw["merge_message_body"]["message"]["data"]
        cast_add_body = msg_body.get("cast_add_body", {})

        return (
            int(msg_raw["id"]),
            msg.get("message_subtype", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg["timestamp"]),
            int(cast_add_body.get("parent_cast_id", {}).get("fid", 0)),
            cast_add_body.get("parent_cast_id", {}).get("hash", ""),
            cast_add_body.get("text", ""),
            msg.get("cast", {}).get("language", ""),
            json.dumps(msg.get("cast", {}).get("embeds", [])),
            msg.get("message_hash", "")
        )

    def prepare_reaction_record(self, msg):
        msg_raw = msg["raw"]
        return (
            int(msg_raw["id"]),
            msg.get("message_subtype", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg["timestamp"]),
            msg["reaction"].get("type", ""),
            int(msg["reaction"].get("target_fid", 0)),
            msg["reaction"].get("target_hash", ""),
            msg.get("message_hash", "")
        )

    def bulk_insert_casts(self):
        try:
            self.conn.executemany("""
                INSERT INTO casts (id, msg_type, fid, msg_timestamp, text, lang, embeds, mentions, msg_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO NOTHING;
            """, self.cast_buffer)
            logger.info(f"Bulk inserted {len(self.cast_buffer)} casts.")
            self.cast_buffer = []
        except Exception as e:
            logger.error(f"Failed bulk insert casts: {str(e)}")
            self.cast_buffer = []

    def bulk_insert_comments(self):
        try:
            self.conn.executemany("""
                INSERT INTO comments (id, msg_type, fid, msg_timestamp, parent_fid, parent_hash, text, lang, embeds, msg_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO NOTHING;
            """, self.comment_buffer)
            logger.info(f"Bulk inserted {len(self.comment_buffer)} comments.")
            self.comment_buffer = []
        except Exception as e:
            logger.error(f"Failed bulk insert comments: {str(e)}")
            self.comment_buffer = []

    def bulk_insert_reactions(self):
        try:
            self.conn.executemany("""
                INSERT INTO reactions (id, msg_type, fid, msg_timestamp, reaction_type, target_fid, target_hash, msg_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO NOTHING;
            """, self.reaction_buffer)
            logger.info(f"Bulk inserted {len(self.reaction_buffer)} reactions.")
            self.reaction_buffer = []
        except Exception as e:
            logger.error(f"Failed bulk insert reactions: {str(e)}")
            self.reaction_buffer = []

    def flush_buffers(self):
        if self.cast_buffer:
            self.bulk_insert_casts()
        if self.comment_buffer:
            self.bulk_insert_comments()
        if self.reaction_buffer:
            self.bulk_insert_reactions()

    def consume(self):
        logger.info("Starting Kafka analytics consumer for topics: %s", self.topics)

        for message in self.consumer:
            try:
                self.process(message.value)
                if (
                    len(self.cast_buffer) >= BATCH_SIZE
                    or len(self.comment_buffer) >= BATCH_SIZE
                    or len(self.reaction_buffer) >= BATCH_SIZE
                ):
                    self.flush_buffers()

            except KafkaError as e:
                logger.error("Kafka error while consuming message: %s", str(e))
            except Exception as e:
                logger.error("Unexpected error while consuming message: %s", str(e))

        self.flush_buffers()

if __name__ == "__main__":
    consumer = KafkaAnalyticsConsumer(topics=[ANALYTICS_TOPIC, EMBEDDER_TOPIC])
    consumer.consume()
