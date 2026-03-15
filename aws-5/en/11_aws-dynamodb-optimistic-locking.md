# AWS DynamoDB - Optimistic Locking

## Overview

DynamoDB has a feature called **Optimistic Locking** that allows you to perform Conditional Writes. This feature ensures that an item has not changed before you update or delete it.

## What is Optimistic Locking?

Optimistic Locking is a mechanism that lets you write to DynamoDB only if certain conditions are met. You're essentially saying: "I want to write this only if this condition is met."

## How It Works

The implementation uses a version number attribute on items:
- An attribute acts as a version number
- An equality condition is checked on this version number before writes
- This prevents concurrent update conflicts

## Example Scenario

### Initial State
```
DynamoDB Table Item:
- User ID: [some_id]
- First Name: [some_name]
- Version: 1
```

### Concurrent Update Attempt

Two clients simultaneously try to update the same item:

**Client 1:** 
- Update: `name = John`
- Condition: `only if version = 1`

**Client 2:**
- Update: `name = Lisa`
- Condition: `only if version = 1`

### What Happens

1. One request reaches DynamoDB first (let's say Client 2)
2. DynamoDB updates:
   - First Name → `Lisa`
   - Version → `2`
3. Client 1's update fails because:
   - Client 1 specified condition: `version = 1`
   - Current version is now: `2`
4. Client 1 receives an error message indicating the data has changed
5. Client 1 must perform a GET operation to retrieve the latest data before retrying the update

## Key Takeaways

- **Conditional Writes** prevent overwriting changes made by other clients
- The **version number** acts as a concurrency control mechanism
- Failed updates require fetching the latest data before retrying
- This is an important exam topic for AWS certifications

## Use Cases

- Preventing race conditions in concurrent environments
- Ensuring data consistency without locks
- Managing updates to shared resources

---

*Note: This feature is commonly tested in AWS certification exams.*
