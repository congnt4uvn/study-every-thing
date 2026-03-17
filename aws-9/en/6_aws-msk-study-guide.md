# AWS Study Guide: Amazon MSK (Managed Streaming for Apache Kafka)

## 1. What is Amazon MSK?
Amazon MSK is a fully managed Apache Kafka service on AWS.

With Amazon MSK, you can:
- Create, update, and delete Kafka clusters.
- Deploy clusters inside your VPC.
- Run across multiple Availability Zones (up to 3 AZs) for high availability.
- Get automatic recovery from common Kafka failures.
- Store data on EBS volumes for as long as needed (you pay for storage).

## 2. MSK Serverless
MSK Serverless lets you run Apache Kafka without managing servers or capacity.

AWS handles:
- Infrastructure provisioning
- Automatic compute scaling
- Automatic storage scaling

Use this option when you want Kafka with minimal operational overhead.

## 3. Apache Kafka Basics
A Kafka system includes:
- **Brokers**: Kafka servers in the cluster.
- **Producers**: Applications that send data to Kafka topics.
- **Topics**: Streams of records (can be partitioned and replicated).
- **Consumers**: Applications that read and process topic data.

Typical producer sources mentioned:
- Kinesis
- IoT
- RDS

Typical consumer destinations mentioned:
- EMR
- S3
- SageMaker
- Kinesis
- RDS

## 4. MSK vs Kinesis Data Streams (Exam-Oriented)

### Similar idea
Both services support real-time data streaming.

### Key differences
- **Message size**:
  - Kinesis Data Streams: 1 MB limit per message.
  - MSK (Kafka): Default around 1 MB, configurable to larger values (example: 10 MB).

- **Scaling unit**:
  - Kinesis: Shards.
  - MSK: Topics with partitions.

- **Scale operations**:
  - Kinesis: Scale out/in via shard split/merge.
  - MSK: You can add partitions, but cannot remove partitions.

- **In-flight encryption**:
  - Kinesis: In-flight encryption supported.
  - MSK: Plaintext or TLS in-flight encryption.

- **At-rest encryption**:
  - Both support data encryption at rest.

- **Data retention**:
  - Kinesis has configured retention windows.
  - MSK can retain data for very long periods (even beyond 1 year) as long as EBS storage is paid.

## 5. How to Consume Data from MSK
Common options:
- Kinesis Data Analytics for Apache Flink
- AWS Glue streaming ETL jobs (Spark Streaming)
- AWS Lambda as an event source consumer
- Custom Kafka consumer on EC2, ECS, or EKS

## 6. Quick Exam Notes
- Amazon MSK = managed Kafka cluster on AWS.
- MSK Serverless = no server/capacity management.
- Multi-AZ deployment improves availability.
- MSK scaling focuses on adding partitions.
- Long-term retention in MSK depends on EBS storage cost.
