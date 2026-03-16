# AWS AppSync Study Notes

## Learning Goal
Build a simple GraphQL API using AWS AppSync, connect it to DynamoDB, test mutations/queries, review settings, and clean up resources.

## What Is AppSync?
AWS AppSync is a managed service to build GraphQL APIs.
- It can connect to data sources like DynamoDB.
- It helps web and mobile clients use one API layer.
- It supports real-time and multiple authorization modes.

## Hands-On Flow

### 1. Create the API
1. Open AWS AppSync.
2. Choose **GraphQL APIs** (not Merged API for this basic lab).
3. Choose **Design from scratch**.
4. API name: **My AppSync API**.

### 2. Define a Model Backed by DynamoDB
1. Create a type backed by DynamoDB.
2. Model name: **Student**.
3. Add fields:
   - `id`: `ID!` (required)
   - `name`: `String!` (required)
   - `age`: `Int` (optional)
   - `certified`: `Boolean` (optional)

### 3. Configure the DynamoDB Table
- Table name: **StudentTable**
- Primary key: `id`
- Sort key: none

Create the API.

## Result After Creation
AppSync automatically generates:
- GraphQL schema
- Data source mapping to DynamoDB
- Standard operations (queries/mutations)

You can verify in DynamoDB that `StudentTable` was created.

## Testing in AppSync Queries

### Query before inserting data
Run `listStudents` first: result is empty.

### Insert records with mutation
Use `createStudent` with sample inputs:
- Student 1: Mike, age 25, certified true
- Student 2: Alice, age 30, certified true

### Query again
Run `listStudents` and confirm both students are returned.

### Verify in DynamoDB
Check table items in `StudentTable`; records should match query output.

## Key AppSync Settings to Know

### Caching options
- Full request caching
- Per-resolver caching
- No caching

### API information
- GraphQL endpoint
- API ID
- Real-time endpoint

### Authorization modes
- API Key (used in this lab)
- IAM
- OpenID Connect
- AWS Lambda authorizer
- Amazon Cognito User Pool

AppSync also supports multiple authorization providers at the same time.

### Monitoring
Track request count, errors, and related metrics.

### Custom domain
You can map the API to your own domain.

## Why This Matters
This setup gives you a GraphQL API on top of DynamoDB quickly.
- Useful for web clients (JavaScript).
- Useful for mobile clients (Android/iOS).
- One API style for multiple frontend platforms.

## Cleanup Steps
After practice, delete resources to avoid cost:
1. Delete AppSync API (`My AppSync API`).
2. Delete DynamoDB table (`StudentTable`).

## Quick Review Questions
1. Why choose GraphQL API instead of Merged API in a beginner lab?
2. Which field is the DynamoDB partition key in this exercise?
3. What mutation is used to add students?
4. What query is used to fetch all students?
5. Name two authorization methods supported by AppSync.

## 5-Minute Exam Memory
- AppSync provides managed GraphQL APIs.
- AppSync can use DynamoDB as a backend data source.
- Schema + operations can be auto-generated from model setup.
- Common operations: `createStudent`, `listStudents`.
- Always clean up AppSync APIs and DynamoDB tables after labs.
