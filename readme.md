### Kafka Topics


kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.cast.add --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.events.other --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.events.dlq --partitions 1 --replication-factor 1


### Consume Events Sample


kafka-console-consumer  --bootstrap-server localhost:9092 --topic farcaster.events.add --from-beginning --property print.key=true --property print.value=true