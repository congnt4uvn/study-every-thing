# AWS DynamoDB Operations Study Guide

## Table Cleanup Operations

When you need to clean up a DynamoDB table, you have two main approaches:

### Option 1: Scan and Delete
- **Process**: Scan all items in the table and delete them one by one
- **Disadvantages**:
  - Very slow process
  - High cost - consumes significant RCU (Read Capacity Units) for scanning
  - High cost - consumes significant WCU (Write Capacity Units) for deleting
  - Not recommended for production use

### Option 2: Drop and Recreate (Recommended)
- **Process**: Drop (delete) the entire table and recreate it
- **Advantages**:
  - Fast execution
  - Efficient operation
  - Cost-effective
- **Important**: Make sure to recreate the table with the correct settings matching the original configuration

## Copying a DynamoDB Table

There are three main methods to copy a DynamoDB table:

### 1. AWS Backup Service
- Create a backup of the source table
- Restore the backup to create a new table
- Can restore within the same account or to a different account
- Managed service approach

### 2. AWS Glue (ETL Service)
- AWS Glue creates an automated script
- The script reads from the source table
- Can write the data to any destination you specify
- Good for data transformation and migration tasks

### 3. Custom Code Solution
- Write your own application code
- Use DynamoDB API calls:
  - `Scan` - to read items from source table
  - `PutItem` - to write individual items
  - `BatchWriteItem` - to write multiple items efficiently
- More complex than using AWS managed services
- Provides maximum flexibility and control

## Key Takeaways

- For table cleanup, always prefer **Drop and Recreate** over scan and delete
- For copying tables, use **AWS Backup** for simplicity or **AWS Glue** for transformation needs
- Custom code solutions are more complex but offer the most control
- Consider RCU/WCU consumption when choosing your approach
