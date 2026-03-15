# AWS DynamoDB Study Guide

## Overview
This guide covers essential DynamoDB data API operations and best practices for interacting with DynamoDB tables.

## Table of Contents
1. [Scan Operation](#scan-operation)
2. [Put Item](#put-item)
3. [Update Item](#update-item)
4. [Get Item](#get-item)
5. [Batch Operations](#batch-operations)
6. [Query vs Scan](#query-vs-scan)

---

## Scan Operation

### Description
The **Scan** operation reads every item in a table and returns all data attributes by default.

### How to Use
1. Select your table
2. Choose 'Scan' option
3. Click 'Run'

### Key Points
- Scans the **entire table**
- Returns many items
- Can be inefficient for large tables
- Filters are applied **client-side** (in your web browser)

### Use Cases
- Small tables
- When you need all data
- Administrative tasks

---

## Put Item

### Description
The **PutItem** operation creates a new item or replaces an existing item with a new item.

### Example
```
User ID: Alice456
Timestamp: T050600
Content: Alice blog
```

### Key Points
- Sends a new item into DynamoDB
- Requires primary key attributes (user_id, post_timestamp)
- If item exists, it will be replaced
- Creates new item if it doesn't exist

### When to Use
- Creating new records
- Completely replacing existing items

---

## Update Item

### Description
The **UpdateItem** operation modifies existing attributes of an item or adds new attributes.

### How to Perform
1. Select the item
2. Choose 'Actions' → 'Edit'
3. Modify specific attributes
4. Click 'Save changes'

### Example
```
Original: Alice blog
Updated: Alice blog edited
```

### Key Points
- Only updates specified attributes
- More efficient than PutItem for partial updates
- Preserves other attributes
- Can add new attributes to existing items

---

## Get Item

### Description
The **GetItem** operation returns a single item from a table by accessing its primary key.

### How It Works
- Click on a specific row in the table
- The 'Item editor' displays the content
- Behind the scenes, a get_item API call is executed

### Key Points
- Retrieves content of a specific item
- Fast and efficient
- Requires knowing the primary key
- Returns all attributes of the item

### Performance
- Most efficient way to retrieve a single item
- Direct key lookup
- Consistent read or eventually consistent read options

---

## Batch Operations

### Batch Write
- Perform multiple PutItem or DeleteItem operations in a single request
- More efficient than individual operations

### Batch Delete
1. Select items for deletion
2. Choose 'Actions' → 'Delete Items'
3. Executes batch write with delete requests

### Key Points
- Can process up to 25 items per request
- Reduces number of API calls
- More cost-effective

---

## Deleting All Data

### Option 1: Scan and Batch Delete
- Scan the entire table
- Use batch delete on results
- **Not very efficient** for large tables

### Option 2: Drop the Table (Recommended)
- Simply delete and recreate the table
- Much faster for clearing all data
- Best for complete table reset

---

## Query vs Scan

### Scan
- **Reads entire table**
- Returns all items
- Filters applied client-side
- Less efficient for large tables
- Higher cost

### Query
- **More efficient** operation
- Uses partition key (and optional sort key)
- Filters applied server-side
- Lower cost
- Faster performance

### Best Practice
- Use **Query** when you know the partition key
- Use **Scan** only when necessary (small tables or need all data)

---

## Summary

| Operation | Use Case | Efficiency |
|-----------|----------|------------|
| Scan | Get all items | Low |
| Query | Get items by key | High |
| GetItem | Get single item | Very High |
| PutItem | Create/Replace item | High |
| UpdateItem | Modify attributes | High |
| Batch Operations | Multiple operations | High |

---

## Best Practices

1. **Prefer Query over Scan** whenever possible
2. **Use batch operations** for multiple items
3. **Update Item** instead of Put Item for partial updates
4. **Drop table** instead of scanning and deleting all items
5. **Design partition keys** to enable efficient queries
6. Consider **read/write capacity** when performing operations

---

## Study Tips

- Practice each operation in the AWS Console
- Understand the difference between Query and Scan
- Know when to use batch operations
- Remember that filters in Scan are client-side
- Understand primary key requirements for each operation
