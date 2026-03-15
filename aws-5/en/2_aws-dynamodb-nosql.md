# AWS DynamoDB - NoSQL Database Study Guide

## Overview
DynamoDB is a **NoSQL serverless database** provided by AWS.

## Traditional Architecture vs NoSQL

### Traditional RDBMS Architecture
```
Clients → ELB → EC2 Instances (Auto Scaling Group) → RDS Database
```

**Components:**
- **Elastic Load Balancer (ELB)**: Distributes traffic
- **EC2 Instances**: Application layer with Auto Scaling Group
- **Amazon RDS**: Relational database (MySQL, PostgreSQL, etc.)

### Traditional RDBMS Features
✅ **Advantages:**
- SQL query language support
- Strong data modeling requirements
- Defined tables and schemas
- Supports joins, aggregations, and complex computations

⚠️ **Scaling Limitations:**
- **Vertical Scaling**: Requires upgrading to more powerful hardware (CPU, RAM, better I/O)
- **Horizontal Scaling**: Limited to read operations only
  - Add EC2 instances at application layer
  - Add RDS Read Replicas (limited by maximum replica count)
- **No horizontal write scaling** with RDS

## NoSQL Databases

### Definition
- **NoSQL** = "Not Only SQL" or "Non SQL"
- Non-relational databases
- Distributed architecture
- Provides horizontal scalability

### Popular NoSQL Technologies
- **MongoDB**
- **AWS DynamoDB** ⭐

### Key Benefits
- ✅ Horizontal scalability
- ✅ Distributed architecture
- ✅ Better suited for high-scale applications
- ✅ Serverless option (DynamoDB)

## Study Notes
- DynamoDB is AWS's managed NoSQL database service
- Overcomes traditional RDS horizontal scaling limitations
- Ideal for applications requiring high read/write throughput
- Serverless means no infrastructure management required
