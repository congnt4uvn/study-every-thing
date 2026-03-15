# AWS DynamoDB Accelerator (DAX)

## Overview
DAX (DynamoDB Accelerator) is a fully managed, highly available caching service built for Amazon DynamoDB. It provides microsecond latency for cached data.

## Creating a DAX Cluster

### Step 1: Access DAX Console
- Navigate to DynamoDB console
- Find DAX on the left-hand side menu
- **Note**: DAX is **not part of the free tier** - creating a DAX cluster will incur costs

### Step 2: Cluster Configuration

#### Cluster Name
- Example: `DemoDAX`

#### Node Family Selection
You can choose between two main node types:

**T-types (Burstable Performance)**
- Recommended for lower throughput use cases
- Cost-effective for development and testing
- Example: `t2.small`

**R-types (Memory Optimized)**
- Designed for always-ready capacity
- Better for production workloads with consistent high throughput
- Example: `r5.large`, `r5.4xlarge`

### Step 3: Cluster Size
- **Range**: 1 to 11 nodes
- **1 node**: Good for single AZ or development environments
  - ⚠️ May experience reduced availability
- **2 nodes**: Still may experience reduced availability
- **3 nodes**: Provides multi-AZ setup for high availability

### Step 4: Network Configuration

#### Subnet Group
- Select or create a subnet group for your DAX cluster
- Example: `demosubnetgroup`
- Must live within a specific VPC
- Choose subnets based on availability requirements:
  - 3 subnets = support for highly available 3-node setup

#### Access Control
- Configure security group to control access to DAX cluster
- **Required Port**: 
  - Port **8111** (standard connection)
  - Port **9111** (if using in-transit encryption)
- Can create a security group from EC2 console
- Default security group can be used for demonstration

### Step 5: Availability Zone Allocation
- Choose between:
  - **Automatic**: AWS automatically distributes nodes across AZs
  - **Manual**: Specify AZ placement for each node

## Best Practices
✅ Use 3 or more nodes for production environments
✅ Enable encryption in transit for sensitive data
✅ Place nodes across multiple AZs for high availability
✅ Configure appropriate security groups to restrict access
⚠️ Remember DAX is not free tier eligible - monitor costs

## Key Takeaways
- DAX significantly reduces read latency for DynamoDB
- Proper cluster sizing impacts both availability and cost
- Multi-AZ deployment requires appropriate subnet configuration
- Security groups must allow traffic on DAX-specific ports
