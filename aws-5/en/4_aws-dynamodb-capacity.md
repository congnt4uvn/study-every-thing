# AWS DynamoDB - Capacity Modes

## Overview
This document covers DynamoDB capacity modes, RCU (Read Capacity Units), and WCU (Write Capacity Units) configuration.

## Capacity Mode Configuration

### Accessing Capacity Settings
1. Select your DynamoDB table (e.g., User's table)
2. Navigate to the right-hand side
3. Click on **Additional settings**
4. Access **Read/Write capacity**
5. Click **Edit**

### Key Features
- Settings defined at table creation time can be modified
- You can **switch between capacity modes** at any time
- Capacity can be adjusted over time based on your needs

## Capacity Modes

### 1. On-Demand Mode

**Characteristics:**
- Simplified billing - pay only for actual reads and writes
- **Cost:** 2-3x more expensive than provisioned mode
- No capacity planning required

**Best Use Cases:**
- Unpredictable workload patterns
- Development environments
- Sporadic usage (e.g., unused for 24 hours, then heavily used for 1 hour)
- Applications with highly variable traffic

**Advantage:** Charges based on actual usage - excellent for intermittent workloads

### 2. Provisioned Capacity Mode

**Characteristics:**
- Requires planning and calculating RCU and WCU
- More cost-effective than on-demand
- Predictable pricing

**Configuration Parameters:**

#### Using the Capacity Calculator:
1. **Average item size:** e.g., 6 kilobytes
2. **Reads per second:** e.g., 3 reads/second
3. **Writes per second:** e.g., 2 writes/second
4. **Read consistency type:**
   - Eventually consistent
   - Strongly consistent
   - Transactional (advanced topic)
5. **Write consistency type:**
   - Standard
   - Transactional (advanced topic)

**Calculator Output:**
- Required RCU (Read Capacity Units)
- Required WCU (Write Capacity Units)
- Estimated monthly cost

## Key Concepts

### RCU (Read Capacity Units)
Units that represent the read throughput capacity for your table.

### WCU (Write Capacity Units)
Units that represent the write throughput capacity for your table.

### Read Consistency Types:
- **Eventually Consistent:** Default option, lower RCU consumption
- **Strongly Consistent:** Guaranteed latest data, higher RCU consumption
- **Transactional:** For ACID transactions (covered in advanced topics)

### Write Consistency Types:
- **Standard:** Default write mode
- **Transactional:** For ACID transactions (covered in advanced topics)

## Best Practices

1. **Use the Capacity Calculator** to estimate your needs
2. **Practice with different scenarios** to understand capacity planning
3. **Start with on-demand** for development/testing
4. **Switch to provisioned** for production with predictable workloads
5. **Monitor your usage** and adjust capacity as needed

## Cost Optimization

- **On-demand:** Best for unpredictable or sporadic workloads
- **Provisioned:** Best for steady, predictable traffic patterns
- Consider using provisioned mode with auto-scaling for variable but predictable workloads

---

*Note: This is a foundational guide. Advanced topics like transactional operations will be covered separately.*
