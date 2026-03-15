# AWS DynamoDB - PartiQL Study Guide

## Overview

PartiQL is a SQL-compatible query language that allows you to interact with DynamoDB tables using familiar SQL-like syntax. This makes DynamoDB more accessible to developers who are already comfortable with SQL.

## Key Concepts

### What is PartiQL?

- **SQL-like syntax** for DynamoDB operations
- Designed for developers familiar with SQL
- Supports standard CRUD operations
- Compatible with DynamoDB's NoSQL structure

### Supported Operations

PartiQL supports the following operations on DynamoDB tables:

1. **INSERT** - Add new items to a table
2. **UPDATE** - Modify existing items
3. **SELECT** - Query and retrieve items
4. **DELETE** - Remove items from a table

### Batch Operations

PartiQL also supports batch operations, allowing you to perform multiple operations efficiently in a single request.

## Using PartiQL in AWS Console

### Accessing PartiQL Editor

1. Navigate to DynamoDB in AWS Console
2. Select your table from the left-hand side
3. Open the **PartiQL editor**

### Example Operations

#### Creating Sample Data

**Users Table:**
```json
{
  "user_id": "123",
  "name": "Stephan"
}
```

**Users Post Table:**
```json
{
  "user_id": "123",
  "post_id": "456"
}
```

**Demo Indexes Table:**
```json
{
  "user_id": "123",
  "game_timestamp": "2022",
  "game_id": "456"
}
```

#### SELECT Operations

**Scan entire table:**
```sql
SELECT * FROM users
```

**Query with conditions:**
```sql
SELECT * FROM demo_indexes 
WHERE user_id = '123' 
AND game_timestamp = 'Sort key value'
```

Note: The sort key condition is optional in queries.

### Working with Results

- View results in **JSON format** for code integration
- **Download results** as CSV for data analysis
- Item results are displayed with their attributes

## Best Practices

1. **Use Query over Scan** when possible for better performance
2. **Specify conditions** to limit the data returned
3. **Validate SQL statements** before execution
4. **Use batch operations** for multiple items to improve efficiency
5. **Understand partition keys and sort keys** for effective querying

## Common Use Cases

- Data migration from SQL databases
- Quick data exploration and debugging
- Ad-hoc queries for analytics
- Development and testing

## Important Notes

- PartiQL statements must be well-formed (proper syntax)
- Remember that DynamoDB is still NoSQL underneath
- Partition keys are required for Query operations
- Sort keys are optional but improve query specificity

## Additional Resources

- AWS DynamoDB Documentation
- PartiQL Language Specification
- DynamoDB Best Practices Guide
