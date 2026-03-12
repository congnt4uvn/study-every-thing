# Lesson 06 — Schema & serialization: JSON vs Avro/Protobuf, compatibility

## Goals
- Understand why schemas matter for long-lived event streams
- Compare JSON vs Avro vs Protobuf at a high level
- Learn schema evolution rules and compatibility thinking

## Why schemas matter
Kafka topics often live for years and are consumed by multiple teams.

Without schema discipline, you get:
- Breaking changes that crash consumers
- “Mystery fields” and inconsistent payloads
- Slow, risky refactors

A good schema strategy provides:
- Backward/forward compatibility rules
- Validation at the edges
- Clear ownership and versioning

## Serialization options (practical overview)
### JSON
Pros:
- Human-readable
- Easy to debug

Cons:
- No strict schema by default
- Larger payloads
- Type ambiguity (numbers, dates)

### Avro
Pros:
- Compact binary
- Strong schema evolution patterns
- Good ecosystem with Schema Registry

Cons:
- Needs schema tooling
- Harder to debug without tooling

### Protobuf
Pros:
- Compact binary
- Strong typing and code generation

Cons:
- Evolution rules exist but differ from Avro
- Still needs registry/governance in multi-team environments

## Compatibility (core idea)
When producers and consumers deploy independently, you want to change schemas safely.

Common compatibility modes (conceptually):
- **Backward compatible**: new consumer can read old messages
- **Forward compatible**: old consumer can read new messages
- **Full**: both directions

Practical tips:
- Add fields as optional with defaults
- Avoid changing field meaning
- Avoid reusing field names for different meaning

## Hands-on lab (process, not vendor-specific)
1. Take your `demo.orders` payload and write down a schema contract:
   - Required fields
   - Optional fields
   - Allowed enum values

2. Propose two changes:
   - Safe: add optional field `source`
   - Risky: rename `orderId` to `id`

3. Decide compatibility policy and what you’d do to keep consumers working.

## Checklist
- I can explain why schemas prevent breaking changes
- I can compare JSON vs Avro vs Protobuf in tradeoffs
- I can identify safe vs unsafe schema changes

## Common pitfalls
- Treating schema evolution like “just change the JSON”
- Breaking consumers by renaming/removing required fields
