# AWS DynamoDB Write Sharding

## Overview
DynamoDB Write Sharding is a strategy to prevent hot partition issues by distributing data more evenly across partitions.

## Problem: Hot Partitions

### Use Case Example
Consider a voting application with two candidates:
- Candidate A
- Candidate B

### Issue
If we use **Candidate ID** as the partition key:
- All votes go to only **2 partitions** (one per candidate)
- Creates **hot partition issues** for both writes and reads
- Poor performance due to uneven distribution

## Solution: Add Suffix or Prefix to Partition Key

### Strategy
Distribute the candidate ID better across partitions by adding a suffix or prefix to the partition key value.

### Example Implementation
Instead of:
- `candidate_A`
- `candidate_B`

Use:
- `candidate_A_11`
- `candidate_A_20`
- `candidate_B_17`
- `candidate_B_18`

### Result
- Partition key takes **more unique values**
- Data is **fully distributed** across DynamoDB table
- Better **write and read performance**

## Methods for Creating Suffix/Prefix

### 1. Random Suffix
- Generate random numbers to append
- Simple implementation
- Ensures distribution

### 2. Calculated Suffix (Hashing Algorithm)
- Use a hashing algorithm to compute the suffix
- Deterministic approach
- Consistent distribution

## Key Takeaway
The goal is to create a **highly distributed partition key** to avoid hot partitions and ensure optimal performance in DynamoDB.

---

**Topic**: AWS DynamoDB
**Concept**: Write Sharding Strategy
**Level**: Intermediate
