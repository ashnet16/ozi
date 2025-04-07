from abc import ABC, abstractmethod
import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import aiohttp
import asyncio
from datetime import datetime
from consumers.base import Consumer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class KafkaEmbedConsumer(Consumer):
    def __init__(self, embedder_hosts, topic_name="farcaster.events.other", group_id="ozi-embed-consumer-group"):
        super().__init__(end_point=embedder_hosts[0], topic_name=topic_name, consumer_group=group_id)
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=["localhost:29092"],
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            enable_auto_commit=True,
            auto_offset_reset="earliest"
        )
        self.embedder_hosts = embedder_hosts
        self.embedder_index = 0

    async def send_to_embedder(self, batch, retries=3):
        for attempt in range(retries):
            host = self.embedder_hosts[self.embedder_index]
            self.embedder_index = (self.embedder_index + 1) % len(self.embedder_hosts)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"http://{host}/embed", json=batch) as resp:
                        if resp.status == 200:
                            logger.info("Successfully sent batch to embedder: %s", host)
                            return
                        else:
                            logger.warning("Attempt %d failed to send to embedder %s: %s", attempt + 1, host, await resp.text())
            except Exception as e:
                logger.warning("Attempt %d exception while sending to embedder %s: %s", attempt + 1, host, str(e))
        logger.error("All retry attempts to embedder failed.")

    def process(self, messages):
        cast_adds = []
        comments = []
        timestamp = datetime.utcnow().isoformat()
        for msg in messages:
            print(msg)
            
            if msg.get("message_type") == "CAST_ADD":
                cast = msg.get("cast", {})
                text = cast.get("text")
                fid = msg.get("fid")
                parent = cast.get("parent_url") or cast.get("parent_hash")

                if text and fid:
                    record = {
                        "fid": fid,
                        "text": text,
                        "consumer_ts": timestamp
                    }

                    if parent:
                        comments.append(record)
                    else:
                        cast_adds.append(record)

        if cast_adds:
            logger.info("Top-level casts:")
            for cast in cast_adds:
                print(json.dumps(cast, indent=2))

        if comments:
            logger.info("Comments/replies:")
            for comment in comments:
                print(json.dumps(comment, indent=2))


    def consume(self):
        logger.info("Starting Kafka consumer for topic: %s", self.topic_name)
        buffer = []

        for message in self.consumer:
            try:
                buffer.append(message.value)
                if len(buffer) >= 10:
                    self.process(buffer)
                    buffer = []
            except KafkaError as e:
                logger.error("Kafka error while consuming message: %s", str(e))
            except Exception as e:
                logger.error("Unexpected error while consuming message: %s", str(e))


if __name__ == "__main__":
    embedder_hosts = ["localhost:8000"]
    consumer = KafkaEmbedConsumer(embedder_hosts)
    consumer.consume()