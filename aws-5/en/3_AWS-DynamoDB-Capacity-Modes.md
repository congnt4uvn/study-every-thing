# AWS DynamoDB - Read and Write Capacity Modes

## Overview

DynamoDB capacity modes control how your table handles throughput. You can choose between two capacity modes:

1. **Provisioned Mode** - Specify read and write throughput in advance
2. **On-Demand Mode** - Automatically scales based on workload

> **Note:** You can switch between modes once every 24 hours.

---

## Provisioned Mode

### Key Concepts

- **RCU (Read Capacity Units)** - Throughput for reads
- **WCU (Write Capacity Units)** - Throughput for writes
- You pay for what you provision, regardless of actual usage
- Auto-scaling available to meet demand
- **Burst Capacity** - Temporary capacity available if you exceed provisioned limits

### When Capacity is Exceeded

If you exhaust burst capacity, you get:
- **`ProvisionedThroughputExceededException`**
- Solution: Use **exponential backoff retry strategy**

---

## Write Capacity Units (WCU)

### Formula

**1 WCU = 1 write per second for an item up to 1 KB**

- Items larger than 1 KB consume more WCUs
- **Always round up to the nearest KB**

### Examples

**Example 1:**
- Write 10 items/second
- Item size: 2 KB
- Calculation: `10 × (2 KB / 1 KB) = 20 WCUs`

**Example 2:**
- Write 6 items/second
- Item size: 4.5 KB → rounds to 5 KB
- Calculation: `6 × (5 KB / 1 KB) = 30 WCUs`

**Example 3:**
- Write 120 items/minute
- Item size: 2 KB
- Calculation: `(120 / 60) × (2 KB / 1 KB) = 2 × 2 = 4 WCUs`

---

## Read Capacity Units (RCU)

### Read Consistency Types

#### Eventually Consistent Read (Default)
- May return stale data if read immediately after write
- Data typically consistent within ~100 milliseconds
- **More cost-effective**

#### Strongly Consistent Read
- Always returns the most recent data
- Set `ConsistentRead` parameter to `True` in API calls
- Available for: GetItem, BatchGetItem, Query, Scan
- **Consumes 2x the RCU**
- May have slightly higher latency

### Formula

**1 RCU = One of the following:**
- 1 strongly consistent read/second for items up to 4 KB
- 2 eventually consistent reads/second for items up to 4 KB

- Items larger than 4 KB consume more RCUs
- **Always round up to the nearest 4 KB**

### Examples

**Example 1: Strongly Consistent Reads**
- 10 strongly consistent reads/second
- Item size: 4 KB
- Calculation: `10 × (4 KB / 4 KB) = 10 RCUs`

**Example 2: Eventually Consistent Reads**
- 16 eventually consistent reads/second
- Item size: 12 KB
- Calculation: `(16 / 2) × (12 KB / 4 KB) = 8 × 3 = 24 RCUs`

**Example 3: Strongly Consistent with Rounding**
- 10 strongly consistent reads/second
- Item size: 6 KB → rounds to 8 KB
- Calculation: `10 × (8 KB / 4 KB) = 10 × 2 = 20 RCUs`

---

## DynamoDB Partitions

### How Partitions Work

- Tables are divided into partitions (distributed across servers)
- **Partition key** goes through a hash function to determine partition placement
- Data is replicated across multiple servers

### Partition Distribution Formula (for reference)

- Number of partitions by capacity: `(RCU / 3000) + (WCU / 1000)`
- Number of partitions by size: `Total size / 10 GB`
- Final partitions = `max(capacity-based, size-based)`

> **Important:** RCUs and WCUs are **spread evenly** across partitions

### Example
- 10 partitions with 10 WCUs and 10 RCUs provisioned
- Each partition gets: 1 WCU and 1 RCU

---

## Throttling

### Causes of `ProvisionedThroughputExceededException`

1. **Hot Key** - One partition key read/written too frequently
2. **Hot Partition** - One partition receiving too much traffic
3. **Very Large Items** - Large items consume more RCU/WCU

### Solutions

1. **Exponential Backoff** - Retry with increasing delays (included in SDK)
2. **Better Partition Key Design** - Distribute data more evenly
3. **DynamoDB Accelerator (DAX)** - Caching solution for read-heavy workloads

---

## On-Demand Mode

### Key Features

- **No capacity planning required**
- Automatically scales up/down with workload
- No throttling (unlimited capacity)
- Pay per request:
  - **RRU (Read Request Units)**
  - **WRU (Write Request Units)**

### Pricing

- Approximately **2.5x more expensive** than provisioned mode

### Best Use Cases

- Unknown workloads
- Unpredictable application traffic
- New applications without traffic history
- Spiky or intermittent workloads

---

## Summary

| Feature | Provisioned Mode | On-Demand Mode |
|---------|------------------|----------------|
| **Capacity Planning** | Required (RCU/WCU) | Not required |
| **Scaling** | Auto-scaling available | Automatic |
| **Throttling** | Yes (if exceeded) | No |
| **Pricing** | Pay for provisioned capacity | Pay per request (~2.5x more) |
| **Best For** | Predictable workloads | Unpredictable/spiky workloads |

---

## Quick Reference

### WCU Calculation
```
WCU = (items per second) × (item size in KB rounded up / 1 KB)
```

### RCU Calculation
```
Strongly Consistent:
RCU = (items per second) × (item size in KB rounded up to 4 KB / 4 KB)

Eventually Consistent:
RCU = (items per second / 2) × (item size in KB rounded up to 4 KB / 4 KB)
```
