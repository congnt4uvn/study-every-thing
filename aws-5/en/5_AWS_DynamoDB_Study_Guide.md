# AWS DynamoDB Study Guide

## Overview
This guide covers the essential DynamoDB API calls that you need to know for the exam.

## Writing Data to DynamoDB

### 1. PutItem
- **Purpose**: Creates or fully replaces an item
- **Key Points**:
  - Creates a new item with the specified Primary Key
  - If an item with the same Primary Key exists, it completely replaces it
  - Consumes Write Capacity Units (WCU)
  - Use when you want to do a full replace or write a new item

### 2. UpdateItem
- **Purpose**: Edits existing item attributes or adds a new item
- **Key Points**:
  - Different from PutItem - only edits specific attributes, not all attributes
  - Adds a new item if it doesn't exist
  - More efficient when you only need to modify a few attributes
  - Can be used with Atomic Counters

### 3. Conditional Writes
- **Purpose**: Accept write/update/delete only if conditions are met
- **Key Points**:
  - Helps with concurrent access to items
  - Ensures data integrity in multi-user scenarios

## Reading Data from DynamoDB

### 1. GetItem
- **Purpose**: Read data based on Primary Key
- **Key Points**:
  - Reads based on Primary Key (HASH or HASH+Range)
  - **Read Modes**:
    - **Eventually Consistent Read** (default): May not reflect most recent write
    - **Strongly Consistent Read**: Always returns most up-to-date data (requires more RCU and may have higher latency)
  - **Projection Expression**: Specify to receive only certain attributes from DynamoDB

### 2. Query
- **Purpose**: Return items based on key conditions
- **Key Points**:
  - **Key Condition Expression**:
    - Partition Key: Must use equal operator (e.g., "John123")
    - Sort Key (optional): Can use equal, less than, greater than, begins_with, between, etc.
  - **FilterExpression**: Additional filtering applied after the query operation
  - More efficient than Scan when you know the Partition Key

## Key Concepts Summary

| Operation | Use Case | Primary Key Required |
|-----------|----------|---------------------|
| PutItem | Full item write/replace | Yes |
| UpdateItem | Partial attribute update | Yes |
| GetItem | Single item retrieval | Yes |
| Query | Multiple items with same Partition Key | Yes (Partition Key) |

## Exam Tips
- Know the difference between PutItem (full replace) vs UpdateItem (partial update)
- Understand Eventually Consistent vs Strongly Consistent reads
- Remember that Query requires a Partition Key condition
- FilterExpression is applied AFTER the query operation
