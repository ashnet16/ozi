import duckdb
import logging
import json
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from consumers.base import Consumer
from consumers.config import ANALYTICS_TOPIC, BATCH_SIZE
from table_queries import create_casts_table, create_comments_table, create_reactions_table




logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class KafkaAnalyticsConsumer(Consumer):
    def __init__(self, topic_name=ANALYTICS_TOPIC, group_id="ozi-analytics-consumer-group"):
        super().__init__(
            end_point="kafka:29092", topic_name=topic_name, consumer_group=group_id
        )

        self.consumer = KafkaConsumer(
            topic_name,
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
        print('Ashley')
        print(msg)
        try:
            event_type = msg.get("message_subtype")
            print(event_type)
            if event_type == "CAST_ADD":
                self.cast_buffer.append(self.prepare_cast_record(msg))
            elif event_type == "COMMENT_ADD":
                self.comment_buffer.append(self.prepare_comment_record(msg))
            elif event_type == "REACTION_ADD":
                self.reaction_buffer.append(self.prepare_reaction_record(msg))
            else:
                logger.warning(f"Unknown event_type: {event_type}")
        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")

    def prepare_cast_record(self, msg):
        return (
            int(msg["id"]),
            msg.get("msg_type", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg["msg_timestamp"]),
            msg.get("network", ""),
            None,
            None,
            msg.get("text", ""),
            msg.get("lang", ""),
            json.dumps(msg.get("embeds", [])),
            msg.get("hash", ""),
            msg.get("signature", ""),
            msg.get("signer", ""),
        )

    def prepare_comment_record(self, msg):
        return (
            int(msg["id"]),
            msg.get("msg_type", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg["msg_timestamp"]),
            msg.get("network", ""),
            int(msg.get("parent_fid", 0)),
            msg.get("parent_hash", ""),
            msg.get("text", ""),
            msg.get("lang", ""),
            json.dumps(msg.get("embeds", [])),
            msg.get("hash", ""),
            msg.get("signature", ""),
            msg.get("signer", ""),
        )

    def prepare_reaction_record(self, msg):
        return (
            int(msg["id"]),
            msg.get("msg_type", ""),
            int(msg["fid"]),
            datetime.utcfromtimestamp(msg["msg_timestamp"]),
            msg.get("network", ""),
            msg.get("reaction_type", ""),
            int(msg.get("target_fid", 0)),
            msg.get("target_hash", ""),
            msg.get("hash", ""),
            msg.get("signature", ""),
            msg.get("signer", ""),
        )

    def bulk_insert_casts(self):
        try:
            self.conn.executemany("""
                INSERT INTO casts (id, msg_type, fid, msg_timestamp, network, parent_fid, parent_hash, text, lang, embeds, hash, signature, signer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                INSERT INTO casts (id, msg_type, fid, msg_timestamp, network, parent_fid, parent_hash, text, lang, embeds, hash, signature, signer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                INSERT INTO reactions (id, msg_type, fid, msg_timestamp, network, reaction_type, target_fid, target_hash, hash, signature, signer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        logger.info("Starting Kafka analytics consumer for topic: %s", self.topic_name)

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
    consumer = KafkaAnalyticsConsumer(topic_name=ANALYTICS_TOPIC)
    consumer.consume()
