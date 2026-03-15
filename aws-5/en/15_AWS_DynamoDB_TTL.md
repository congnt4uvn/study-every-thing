# AWS DynamoDB - Time To Live (TTL)

## Overview
Time To Live (TTL) is a feature that allows you to automatically delete items after an expired timestamp in DynamoDB tables.

## How It Works

### Basic Concept
- Define a specific column that contains the expiration timestamp
- When the current time exceeds the value in this column, DynamoDB automatically removes the item
- **No Write Capacity Units (WCU) consumed** - deletion is free of charge

### Timestamp Format
- Must be a **number** representing the **Unix Epoch timestamp** value
- Example: 1710518400 (represents March 15, 2025 00:00:00 UTC)

## TTL Process Flow

### Example: Session Data Table
| User ID | Session ID | Expired Time (TTL) |
|---------|------------|-------------------|
| user123 | sess456    | 1710518400        |

### Deletion Process
1. **Expiration Marking**: DynamoDB periodically scans the table
   - Compares current time with TTL column values
   - Marks items where TTL < current time

2. **Item Deletion**: A second process scans and deletes marked items
   - Deletion occurs automatically
   - Items also removed from indexes (LSI and GSI)

## Important Considerations

### Timing
- Expired items are deleted **within a few days** of expiration (not immediate)
- Can take **up to 48 hours** to see items fully deleted

### Reading Expired Items
- ⚠️ **Expired items that haven't been deleted yet will still appear** in:
  - Read operations
  - Query operations
  - Scan operations
- **Solution**: Implement client-side filtering to exclude expired items

### DynamoDB Streams Integration
- Each TTL deletion generates a delete operation entry in DynamoDB Streams
- Enables recovery or tracking of deleted items if needed

### Index Behavior
- Expired items are automatically removed from:
  - Local Secondary Indexes (LSI)
  - Global Secondary Indexes (GSI)

## Use Cases

1. **Data Retention Management**
   - Keep only current, relevant items
   - Automatically purge old data

2. **Regulatory Compliance**
   - Adhere to data retention policies
   - Automatically comply with GDPR, HIPAA requirements

3. **Session Management**
   - Auto-expire user sessions after inactivity
   - Clean up temporary session data

4. **Cost Optimization**
   - Reduce storage costs by removing obsolete data
   - No additional cost for deletions

## Best Practices

- ✅ Set appropriate TTL values based on use case
- ✅ Implement client-side filtering for reads if immediate consistency is needed
- ✅ Use DynamoDB Streams to archive or backup deleted items
- ✅ Monitor TTL deletions through CloudWatch metrics
- ✅ Test TTL behavior in development before production deployment

## Key Takeaways

- **Free deletions** - no WCU consumed
- **Eventual deletion** - not immediate (up to 48 hours)
- **Stream integration** - deleted items appear in DynamoDB Streams
- **Client-side filtering recommended** - for queries involving TTL items
