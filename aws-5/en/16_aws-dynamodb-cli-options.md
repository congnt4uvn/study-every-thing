# AWS DynamoDB CLI Options

## Overview
This document covers important CLI options for DynamoDB that may appear in AWS exams.

## Key CLI Options

### 1. projection-expression
- **Purpose**: Specify one or more attributes to retrieve
- **Use Case**: When you don't want to retrieve all columns/attributes
- **Benefit**: Retrieve only a subset of data to reduce data transfer and get only what you need

### 2. filter-expression
- **Purpose**: Filter items returned from the query
- **Use Case**: Apply conditions to filter the results
- **Benefit**: Get only the items that meet specific criteria

## Pagination Options

### page-size
- **Purpose**: Control the size of each sub-API call to AWS
- **How it works**: 
  - Still retrieves the entire dataset
  - Each API call to AWS is smaller
  - Prevents API timeouts
- **Example**:
  - Table with 10,000 items
  - Without page-size: 1 API call retrieving all 10,000 items (may timeout)
  - With page-size=100: 100 API calls of 100 items each (avoids timeout)
- **Benefit**: Optimization to avoid timeouts while still getting all data

### max-items
- **Purpose**: Limit the number of items returned in a single CLI result
- **How it works**: Works in combination with NextToken/starting-token
- **Use Case**: Pagination through results
- **Example**:
  - Set max-items=25 to receive 25 items
  - Use NextToken to retrieve the next 25 items
  - Continue pagination as needed

### NextToken / starting-token
- **Purpose**: Retrieve the next set of paginated results
- **How it works**: Used after receiving results with max-items
- **Use Case**: Get subsequent pages of data

## Practice Environment
- Access UserPosts table to view items
- Use AWS CLI (configured terminal) or AWS CloudShell for hands-on practice

## Key Takeaways
- **projection-expression**: Select specific attributes
- **filter-expression**: Filter results with conditions
- **page-size**: Optimize API calls to avoid timeouts (retrieves all data)
- **max-items + NextToken**: Limit results and paginate through them
