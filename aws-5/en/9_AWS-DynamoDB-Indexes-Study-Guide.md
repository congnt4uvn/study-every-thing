# AWS DynamoDB Indexes - Study Guide

## Overview
This guide covers how to create and use indexes in Amazon DynamoDB, including Local Secondary Indexes (LSI) and Global Secondary Indexes (GSI).

## Table Structure Basics

### Primary Keys
- **Partition Key**: The main attribute used to distribute data (e.g., `user_id`)
- **Sort Key**: Optional attribute that allows sorting and range queries (e.g., `game_timestamp`)

## Types of Indexes

### 1. Local Secondary Index (LSI)
- **Creation Time**: Can ONLY be created at table creation time
- **Partition Key**: Must use the SAME partition key as the base table
- **Sort Key**: Must specify a DIFFERENT sort key from the base table
- **Use Case**: Query the same partition key with different sort key

**Example:**
- Base Table: Partition Key = `user_id`, Sort Key = `game_timestamp`
- LSI: Partition Key = `user_id`, Sort Key = `game_id`

### 2. Global Secondary Index (GSI)
- **Creation Time**: Can be created at table creation OR afterwards
- **Partition Key**: Can specify a DIFFERENT partition key
- **Sort Key**: Can optionally specify a DIFFERENT sort key
- **Use Case**: Query data using different access patterns

## Attribute Projection

When creating an index, you must choose which attributes to project:

1. **All**: Projects all attributes from the base table
2. **Keys Only**: Projects only the key attributes
3. **Include**: Projects specific attributes you specify

## Provisioned Capacity

Indexes can have their own provisioned capacity settings:
- **RCU** (Read Capacity Units)
- **WCU** (Write Capacity Units)

## Creating a Table with Indexes

### Step-by-Step Process:
1. Navigate to DynamoDB Tables
2. Create new table (e.g., `demo_indexes`)
3. Choose Partition key (`user_id`)
4. Choose Sort key (`game_timestamp`)
5. Customize settings for Provisioned capacity
6. Define secondary indexes:
   - Add Local Secondary Index with different sort key
   - (Optional) Add Global Secondary Index with different partition/sort keys
7. Select attribute projection strategy
8. Create table

## Querying with Indexes

When querying, you can choose:
- **Query the table**: Use the table's primary keys
- **Query an index**: Use the index's keys for different access patterns

## Key Differences Summary

| Feature | Local Secondary Index | Global Secondary Index |
|---------|----------------------|------------------------|
| Creation Time | Table creation only | Anytime |
| Partition Key | Same as table | Can be different |
| Sort Key | Must be different | Can be different |
| Capacity | Shares with table | Separate capacity |

## Best Practices

1. Plan your indexes carefully during table design
2. Use LSI when you need alternative sort orders for the same partition key
3. Use GSI when you need to query using completely different attributes
4. Choose projection carefully to balance storage costs and query performance
5. Monitor index capacity separately from table capacity

## Common Use Cases

- **User Activity Tracking**: Query by user_id and sort by different timestamps or IDs
- **Game Leaderboards**: Query by game_id instead of user_id
- **Multi-tenant Applications**: Query by tenant_id with various sort patterns

---

*Study Tip: Practice creating tables with both types of indexes in the AWS Console to understand the differences hands-on.*
