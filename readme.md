### Kafka Topics


kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.cast.add --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.events.other --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic farcaster.events.dlq --partitions 1 --replication-factor 1


### Consume Events Sample

Run the below command in the container.


kafka-console-consumer  --bootstrap-server localhost:9092 --topic farcaster.events.add --from-beginning --property print.key=true --property print.value=true




### Local Installation

1. Activate your python environment install the necessary dependencies: pip install -r requirement.txt
2. Spin up a Kafka instance locally but running: docker-compose up -d
3. Run python3 -m producers.pollers to run poller locally
4. Run python3 -m consumers.consumers

