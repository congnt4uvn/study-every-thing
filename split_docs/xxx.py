
import os
import sys
from pathlib import Path

parent_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'chat_AI'))

from chat_AI.run_chat_request import chat

text = """
Kafka Architecture: Components: broker, topic, partition
Kafka Architecture: Components: replica, ISR, controller
Kafka Architecture: Components: Zookeeper vs KRaft (new metadata quorum)
Kafka Architecture: Cluster metadata: how metadata is stored, propagated, cached on clients
Kafka Architecture: Broker responsibilities: request handling, log management, replication, quotas
Kafka Architecture: Network model: TCP, binary protocol, request/response, batching
Data flow: Producer → broker → consumer; how messages are appended to logs
Data flow: Message format: key, value, headers, timestamp, offset
Data flow: Append-only log: segment files, index files, page cache usage
Data flow: Fetching: how consumers read from offsets, zero-copy transfer (sendfile)
Retention & compaction: Time-based and size-based retention
Retention & compaction: Log compaction: use cases (CDC, latest state), how it works, tombstones
Retention & compaction: Segment rolling, deletion, compaction vs deletion policies
Retention & compaction: Impact on storage, performance, and consumer behavior
Topics, Partitions, Ordering: Topic vs partition vs replica
Topics, Partitions, Ordering: Ordering guarantees (ordering only within a partition)
Topics, Partitions, Ordering: Rebalancing partitions across brokers
Topics, Partitions, Ordering: Impact of partition count on throughput, latency, and consumer scaling
How partitioning affects: Parallelism and throughput
How partitioning affects: Ordering guarantees and key affinity
How partitioning affects: Hot partitions, skew, and mitigation strategies
Partitioning strategies: Default partitioner, custom partitioner
Partitioning strategies: Key-based partitioning and its impact on data locality and hot partitions
Partitioning strategies: Sticky partitioner (Kafka 2.4+), batching benefits
Partitioning strategies: Idempotent producer and partitioning implications
Producer basics: Asynchronous send, callbacks, futures
Producer basics: Batching, compression, linger.ms, batch.size
Producer configs: `acks` (0, 1, all) and durability trade-offs
Producer configs: `retries`, `delivery.timeout.ms`, `max.in.flight.requests.per.connection`
Producer configs: `enable.idempotence` and exactly-once semantics (EOS) basics
Producer configs: `compression.type` (gzip, snappy, lz4, zstd) and performance trade-offs
Producer configs: `buffer.memory`, `max.block.ms`, backpressure behavior
Producer reliability: Idempotent producer: how it works (PID, sequence numbers)
Producer reliability: Transactional producer: transactions, fencing, EOS with Kafka Streams / consumers
Producer reliability: Handling `TimeoutException`, `RecordTooLargeException`, `NotEnoughReplicas`
Producer performance: Tuning batch size, linger, compression
Producer performance: Impact of partitions on producer throughput
Producer performance: Monitoring producer metrics (record-send-rate, retries, errors)
Consumer group model: Consumer groups, group.id, group coordinator
Consumer group model: Rebalancing, partition assignment strategies (range, round-robin, sticky)
Consumer group model: Static membership, cooperative rebalancing
Consumer configs: `auto.offset.reset` (earliest, latest, none)
Consumer configs: `enable.auto.commit` vs manual commit
Consumer configs: `max.poll.records`, `max.poll.interval.ms`, `session.timeout.ms`, `heartbeat.interval.ms`
Consumer configs: `fetch.min.bytes`, `fetch.max.wait.ms`, `max.partition.fetch.bytes`
Offset management: Committing offsets to Kafka (`__consumer_offsets`)
Offset management: At-least-once vs at-most-once vs effectively-once patterns
Offset management: Manual commit (sync vs async), commit per record vs per batch
Offset management: Handling reprocessing, replay, and backfills
Consumer reliability: Handling poison messages (DLQ patterns, retries)
Consumer reliability: Idempotent consumers (deduplication, transactional reads)
Consumer reliability: Dealing with slow consumers, backpressure, and lag
Consumer performance: Tuning fetch sizes, concurrency, and partition assignment
Consumer performance: Monitoring consumer lag (consumer-lag metrics, tools)
Consumer performance: Scaling consumers horizontally vs increasing partitions
Replication: Leader/follower model, ISR, min.insync.replicas
Replication: Unclean leader election, data loss scenarios
Replication: Rack awareness, cross-AZ replication patterns
Durability & consistency: `acks=all` + `min.insync.replicas`
Durability & consistency: Trade-offs between latency and durability
Durability & consistency: Exactly-once semantics end-to-end (producer + broker + consumer)
Failure scenarios: Broker failure, controller failure, network partitions
Failure scenarios: What happens during leader election and rebalancing
Failure scenarios: Impact on producers and consumers (errors, retries, timeouts)
Monitoring & observability: Key broker metrics (under-replicated partitions, offline partitions)
Monitoring & observability: Producer/consumer metrics, lag monitoring
Monitoring & observability: Using Prometheus, Grafana, Kafka Manager, Confluent Control Center
Security: Authentication (SASL/PLAIN, SASL/SCRAM, Kerberos, OAuth)
Security: Authorization (ACLs, resource patterns)
Security: Encryption in transit (SSL) and at rest (disk-level, cloud-level)
Spring Kafka basics: `spring-kafka` vs raw Kafka client
Spring Kafka basics: Auto-configuration in Spring Boot (`KafkaAutoConfiguration`)
Spring Kafka basics: `KafkaTemplate` for producing messages
Spring Kafka producer: Configuring `ProducerFactory` and `KafkaTemplate`
Spring Kafka producer: Serializers (String, JSON, Avro, custom)
Spring Kafka producer: Async send with callbacks, error handling, retries
Spring Kafka consumer: `@KafkaListener` annotation basics
Spring Kafka consumer: Concurrency (`concurrency` attribute) and partition assignment
Spring Kafka consumer: Container types (`ConcurrentMessageListenerContainer`, `KafkaMessageListenerContainer`)
Spring Kafka consumer configs: `AckMode` (BATCH, RECORD, MANUAL, MANUAL_IMMEDIATE)
Spring Kafka consumer configs: Manual ack vs auto ack, offset commit strategies
Spring Kafka consumer configs: Error handling (`ErrorHandler`, `SeekToCurrentErrorHandler`, `DeadLetterPublishingRecoverer`)
Spring Kafka error handling: Retries with `RetryTemplate` / `RecoveringBatchErrorHandler`
Spring Kafka error handling: DLQ pattern with `DeadLetterPublishingRecoverer`
Spring Kafka error handling: Handling deserialization errors (`ErrorHandlingDeserializer`)
Spring Kafka transactions: Configuring transactional producer (`transactionIdPrefix`)
Spring Kafka transactions: `@Transactional` with Kafka, exactly-once processing patterns
Spring Kafka transactions: Consuming, processing, and producing in a single transaction
Spring Kafka advanced: Message headers, correlation IDs, tracing (Sleuth, OpenTelemetry)
Spring Kafka advanced: Batch listeners (`@KafkaListener` with `List<ConsumerRecord>`)
Spring Kafka advanced: Seeking, pausing/resuming consumption programmatically
Serialization formats: String, JSON, Avro, Protobuf, Thrift
Serialization formats: Trade-offs: schema evolution, size, performance
Schema Registry: Purpose and benefits (compatibility, evolution)
Schema Registry: Avro/Protobuf with Confluent Schema Registry
Schema Registry: Compatibility modes (BACKWARD, FORWARD, FULL, NONE)
Spring + Schema Registry: Using `KafkaAvroSerializer` / `KafkaAvroDeserializer`
Spring + Schema Registry: Configuring schema registry URL, subject naming strategies
Spring + Schema Registry: Handling schema evolution in Spring services
Data contracts: Versioning topics vs versioning schemas
Data contracts: Backward/forward compatibility strategies
Data contracts: Handling breaking changes and deprecation
Messaging patterns: Event-driven architecture vs request/response
Messaging patterns: Event sourcing, CQRS with Kafka
Messaging patterns: CDC (Change Data Capture) with Debezium + Kafka
Design patterns: Topic design (by entity, by use case, by bounded context)
Design patterns: Single writer principle per key (for ordering)
Design patterns: Multi-tenant topics vs per-tenant topics
Processing patterns: Stream processing vs simple consumers
Processing patterns: Using Kafka Streams vs Spring Kafka vs Flink
Processing patterns: Aggregations, joins, windowing (Kafka Streams concepts)
Reliability patterns: Outbox pattern (DB → Kafka)
Reliability patterns: Idempotent consumers, deduplication store
Reliability patterns: DLQ, retry topics, exponential backoff
Multi-environment patterns: Dev/stage/prod topic naming and isolation
Multi-environment patterns: Schema evolution across environments
Multi-environment patterns: Backward-compatible deployments and rolling upgrades
Kafka Streams basics: KStream, KTable, GlobalKTable
Kafka Streams basics: Topology, DSL vs Processor API
Kafka Streams state: State stores, changelog topics, fault tolerance
Kafka Streams state: Exactly-once processing, EOS v2
Kafka Streams operations: Map, filter, groupByKey, aggregate, join, windowed operations
Kafka Streams operations: Repartitioning topics, impact on performance
Spring integration: Using Kafka Streams with Spring Boot
Spring integration: Managing Kafka Streams lifecycle in Spring
Spring integration: Monitoring Kafka Streams apps (thread states, lag, store sizes)
Capacity planning: Estimating partitions, throughput, retention storage
Capacity planning: Impact of message size, compression, and retention on hardware
Tuning: Broker configs (`num.network.threads`, `num.io.threads`, `log.segment.bytes`, `log.retention.hours`)
Tuning: Producer/consumer tuning for low latency vs high throughput
Tuning: GC considerations, JVM tuning for brokers and clients
Upgrades & compatibility: Kafka client vs broker version compatibility
Upgrades & compatibility: Rolling upgrades, protocol versions, feature flags (KIP-based)
Cloud & managed Kafka: Differences with Confluent Cloud, MSK, Aiven, etc.
Cloud & managed Kafka: Networking, security, and IAM integration
Cloud & managed Kafka: Observability and limits in managed offerings
"""

data = text.strip().splitlines()

def extract_response_text(response):
    if isinstance(response, dict):
        # Check for raw_response first (parse error case)
        if 'raw_response' in response:
            return response['raw_response']
        # Check for OpenAI-style response
        if 'choices' in response and response['choices']:
            return response['choices'][0].get('message', {}).get('content', '')
        # Check for direct content
        if 'content' in response:
            return response['content']
        # Check for text field
        if 'text' in response:
            return response['text']
    return str(response) if response else "No response"


def main():
    output_folder = Path(__file__).parent
    
    print(f"Processing {len(data)} items...\n")
    
    for idx, content in enumerate(data, 1):
        if not content.strip():
            continue
            
        print(f"[{idx}/{len(data)}] Processing item {idx}")
        try:
            response = chat(
                " I'm going to give you a piece of content about "
                + "kafka, spring boot. "  ########################################################
                + " Please summarize it in a concise way, "
                + " focusing on the key points and main ideas. " 
                + " give me code examples if possible, include inputs/outputs if possible."
                + " Make version English" ########################################################
                + "Here is the content:\n\n" 
                + content
                )

            java_folder = output_folder / "spring boot - kafka - en" ########################################################
            java_folder.mkdir(exist_ok=True)
            output_file = java_folder / f"doc_{idx:03d}.md"
            
            # Extract response text and add link to next doc
            content_text = extract_response_text(response)
            
            # Add link to next document if not the last item
            if idx < len(data):
                next_doc = f"doc_{(idx+1):03d}.md"
                content_text += f"\n\n---\n\n[Next: {next_doc}]({next_doc})\n"
            
            output_file.write_text(content_text, encoding='utf-8')
            print(f"✓ Saved: {output_file.name}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\nDone! Processed {len(data)} items.")


if __name__ == "__main__":
    main()