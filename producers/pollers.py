import grpc
import logging
from ozi.producers.base import Poller, EventTransformer, KafkaTopic
from ozi.proto import rpc_pb2_grpc, request_response_pb2, hub_event_pb2, message_pb2
from google.protobuf.json_format import MessageToDict
from kafka import KafkaProducer
import json

MSG_TYPE_PREFIX = 'MESSAGE_TYPE'


FARCASTER_SUBSCRIBE_ENDPOINT = "ec2-13-58-183-70.us-east-2.compute.amazonaws.com:2283"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class KafkaJSONTopic(KafkaTopic):
    def __init__(self, topic_name, bootstrap_servers="localhost:29092", topic_type=None):
        super().__init__(topic_name, topic_type)
        self.producer = KafkaProducer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=100,
            batch_size=16384
        )

    def produce(self, event, topic_name=None):
        target_topic = topic_name or self.topic_name
        try:
            self.producer.send(target_topic, value=event)
            self.producer.flush()
            logger.info("Sent event to Kafka topic: %s", target_topic)
        except Exception as e:
            logger.error("Failed to send to Kafka: %s", e)


class FarcasterGRPCPoller(Poller):
    def __init__(self, end_point=FARCASTER_SUBSCRIBE_ENDPOINT):
        super().__init__(end_point, 'farcaster_grpc')
        self.channel = grpc.insecure_channel(end_point)
        self.stub = rpc_pb2_grpc.HubServiceStub(self.channel)
        self.topic_main = KafkaJSONTopic("farcaster.events.add")
        self.topic_other = KafkaJSONTopic("farcaster.events.other")
        self.topic_dlq = KafkaJSONTopic("farcaster.events.dlq")

    def poll(self):
        request = request_response_pb2.SubscribeRequest(event_types=[1, 2, 3])
        for event in self.stub.Subscribe(request):
            yield event

    def publish(self, event):
        topic = self._select_topic(event)
        topic.produce(event)

    def _select_topic(self, event):
        if event.get("dlq_reason"):
            return self.topic_dlq
        msg_type = event.get("message_type", "") 
        if msg_type == f'{MSG_TYPE_PREFIX}_CAST_ADD':
            return self.topic_main
        else:
            return self.topic_other

    def run(self):
        logger.info("Starting Farcaster gRPC Poller...")
        for event in self.poll():
            transformed_event = FarcasterMessageTransformer(event).transform()
            self.publish(transformed_event)


class FarcasterMessageTransformer(EventTransformer):
    def transform(self):
        event_type = hub_event_pb2.HubEventType.Name(self.event.type)
        output = {"event_type": event_type}
        logger.debug("Transforming event: %s", event_type)

        try:
            if (
                self.event.type == hub_event_pb2.HUB_EVENT_TYPE_MERGE_MESSAGE and
                self.event.HasField("merge_message_body")
            ):
                msg = self.event.merge_message_body.message
                data = msg.data
                msg_type = message_pb2.MessageType.Name(data.type)
          
                output.update({
                    "message_type": msg_type,
                    "fid": data.fid,
                    "timestamp": data.timestamp,
                })

                if msg_type == f'{MSG_TYPE_PREFIX}_CAST_ADD':
                    output["cast"] = {
                        "text": data.cast_add_body.text,
                        "mentions": list(data.cast_add_body.mentions),
                        "embeds": [e.url for e in data.cast_add_body.embeds if e.HasField("url")],
                    }

                elif msg_type == f'{MSG_TYPE_PREFIX}_REACTION_ADD':
                    body = data.reaction_body
                    output["reaction"] = {
                        "type": message_pb2.ReactionType.Name(body.type),
                        "target_fid": body.target_cast_id.fid,
                        "target_hash": body.target_cast_id.hash.hex(),
                    }

                elif msg_type == f'{MSG_TYPE_PREFIX}_LINK_ADD':
                    body = data.link_body
                    output["link"] = {
                        "type": body.type,
                        "target_fid": body.target_fid,
                    }

                elif msg_type == f'{MSG_TYPE_PREFIX}_USER_DATA_ADD':
                    body = data.user_data_body
                    output["user_data"] = {
                        "type": hub_event_pb2.UserDataType.Name(body.type),
                        "value": body.value,
                    }

                else:
                    output["data"] = MessageToDict(data, preserving_proto_field_name=True)
                    output["dlq_reason"] = f"Unhandled MESSAGE_TYPE: {msg_type}"
            else:
                output["raw"] = MessageToDict(self.event, preserving_proto_field_name=True)
                output["dlq_reason"] = f"Unhandled HubEventType or missing field: {event_type}"

        except Exception as e:
            output["error"] = f"Transformation failed: {str(e)}"
            output["raw"] = str(self.event)
            output["dlq_reason"] = f"Transformation error: {str(e)}"
        return output


if __name__ == "__main__":
    FarcasterGRPCPoller().run()
