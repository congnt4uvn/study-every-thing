# AWS DynamoDB - Conditional Writes

## Overview
Conditional writes in DynamoDB allow you to specify conditions that determine which items should be modified during write operations. This ensures data integrity and prevents unwanted modifications.

## Write Operations Supporting Conditions
- **PutItem** - Insert or replace an item
- **UpdateItem** - Modify an existing item
- **DeleteItem** - Remove an item
- **BatchWriteItem** - Perform multiple write operations

## Condition Expression Functions

### Existence Checks
- `attribute_exists` - Check if an attribute exists
- `attribute_not_exists` - Check if an attribute does not exist
- `attribute_type` - Verify the data type of an attribute

### String Operations
- `contains` - Check if a string contains a substring
- `begins_with` - Check if a string starts with a specific prefix

### Value Comparisons
- `IN` - Check if a value is in a list of values
  - Example: Check if product category is in multiple categories
- `BETWEEN` - Check if a value is within a range
  - Example: `Price BETWEEN :low AND :high`
- Comparison operators: `>`, `<`, `>=`, `<=`, `=`

### Other Functions
- `size` - Get the length/size of an attribute (useful for strings, lists, etc.)

## Filter Expressions vs Condition Expressions

| Aspect | Filter Expressions | Condition Expressions |
|--------|-------------------|----------------------|
| **Purpose** | Filter results of read queries | Control which write operations succeed |
| **Operations** | Query, Scan | PutItem, UpdateItem, DeleteItem, BatchWriteItem |
| **When Applied** | After reading data | Before writing data |
| **Effect** | Reduces returned results | Prevents writes if condition fails |

## Example: UpdateItem with Condition Expression

### Command
```bash
aws dynamodb update-item \
  --table-name product_catalog \
  --key '{"id": {"N": "456"}}' \
  --update-expression "SET price = price - :discount" \
  --condition-expression "price > :limit" \
  --expression-attribute-values file://values.json
```

### Values File (values.json)
```json
{
  ":discount": {"N": "150"},
  ":limit": {"N": "500"}
}
```

### Behavior
1. **Initial State**: Item with ID 456 has price = 650
2. **First Update**: 
   - Condition: 650 > 500 ✓ (passes)
   - New price: 650 - 150 = 500
   - **Result**: Success, price updated to 500

3. **Second Update** (same command):
   - Condition: 500 > 500 ✗ (fails)
   - **Result**: Update rejected, price remains 500

## Key Takeaways
- Condition expressions prevent writes when conditions are not met
- They are evaluated **before** the write operation occurs
- Failed conditions throw a `ConditionalCheckFailedException`
- Use condition expressions to implement optimistic locking and business rules
- Always test your condition expressions to ensure they behave as expected

## Best Practices
1. Use `attribute_not_exists` for preventing overwrites during PutItem
2. Combine multiple conditions using `AND`, `OR`, `NOT` operators
3. Use expression attribute names for reserved keywords
4. Test conditions thoroughly before deploying to production
5. Handle `ConditionalCheckFailedException` appropriately in your application code
