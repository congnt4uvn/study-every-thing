# AWS DynamoDB Indexes Study Guide

## Overview
Amazon DynamoDB provides two types of indexes to optimize query performance: Local Secondary Indexes (LSI) and Global Secondary Indexes (GSI).

## Local Secondary Index (LSI)

### Definition
A Local Secondary Index provides an alternative sort key for your table while maintaining the same partition key from the base table.

### Key Characteristics
- **Same partition key** as the base table
- **Alternative sort key** for different query patterns
- Sort key consists of one scalar attribute (string, number, or binary)
- Maximum of **5 LSIs per table**

### Important Constraints
- **Must be defined at table creation time**
- Cannot be added after table creation
- Requires careful table design planning upfront

### Attribute Projection
- Can include some or all attributes from the main table
- Choose specific attributes based on query requirements
- Optimize for query performance and storage costs

### Example Use Case

**Base Table Structure:**
- Partition Key: `user_id`
- Sort Key: `game_id`
- Attributes: `game_timestamp`, `score`, `result`

**Query Limitations Without LSI:**
- Can query by `user_id` and `game_id`
- Cannot efficiently query by `user_id` and `game_timestamp`
- Would require a scan operation with client-side filtering

**Solution with LSI:**
- Create LSI on `game_timestamp` attribute
- Enables efficient queries like: "Get all games played by this user between 2020 and 2021"
- Same partition key (`user_id`), different sort key (`game_timestamp`)

## Global Secondary Index (GSI)

### Definition
A Global Secondary Index provides an alternative primary key, allowing completely different partition and sort keys from the base table.

### Key Characteristics
- **Different partition key** (hash key) from base table
- Optional **different sort key** as well
- Speeds up queries on non-key attributes
- Can use scalar attributes (string, number, binary)

### Flexibility
- Can be created at any time (not just at table creation)
- Allows querying on attributes that aren't part of the primary key
- More flexible than LSI but with different performance characteristics

### Attribute Projection
- Choose which attributes to include in the index
- Balance between query performance and storage costs

## Comparison: LSI vs GSI

| Feature | LSI | GSI |
|---------|-----|-----|
| Partition Key | Same as base table | Can be different |
| Sort Key | Different from base table | Can be different |
| Creation Time | Must be at table creation | Can be added anytime |
| Limit per Table | 5 | 20 (default) |
| Use Case | Alternative sorting on same partition | Querying different access patterns |

## Best Practices

1. **Plan LSIs carefully** - They cannot be modified after table creation
2. **Use GSIs for flexibility** - When you need to query on non-key attributes
3. **Project only needed attributes** - Minimize storage costs
4. **Consider query patterns** - Design indexes based on actual access patterns
5. **Monitor performance** - Track index usage and adjust as needed

## Summary

DynamoDB indexes are essential tools for optimizing query performance:
- **LSI**: Alternative sort key with the same partition key, must be defined at creation
- **GSI**: Alternative primary key, can be added anytime, enables flexible query patterns

Choose the appropriate index type based on your data access patterns and query requirements.
