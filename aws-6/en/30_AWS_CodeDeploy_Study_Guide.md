# AWS CodeDeploy Study Guide

## Overview
AWS CodeDeploy is a deployment service that automates application deployments to various compute services like Amazon EC2, AWS Lambda, and on-premises servers.

## Key Concepts

### 1. EC2 Instance Deployments

#### AppSpec.yml File
- Located at the root of your code
- Defines deployment actions and lifecycle event hooks
- Essential for deployment configuration

#### Deployment Strategy
- **In-Place Updates**: Updates existing EC2 instances in your fleet
- Example: Half-at-a-time deployment
  - First half taken down and upgraded to version 2
  - Second half taken down and upgraded to version 2
  - No new instances created

### 2. Auto Scaling Group (ASG) Deployments

CodeDeploy offers two deployment types for ASG:

#### A. In-Place Deployment
- Updates existing EC2 instances within the ASG
- New EC2 instances created by ASG automatically receive deployments
- No creation of new ASG

#### B. Blue/Green Deployment
- Creates a new Auto Scaling Group
- Settings copied from original ASG
- Process:
  1. ELB directs traffic to original instances (Blue - V1)
  2. New ASG created with updated launch template (Green - V2)
  3. CodeDeploy deploys application to new instances
  4. ELB receives traffic from both V1 and V2 instances
  5. After health checks pass, V1 instances terminated
  6. Traffic fully redirected to V2 instances

**Key Advantage**: You can choose how long to keep the old ASG before termination

### 3. Deployment Hooks
- Set in the appspec.yml file
- Used to verify deployments after each deployment phase
- Allows for validation and testing during deployment lifecycle

### 4. Redeploys and Rollbacks

#### What is a Rollback?
- Redeploying a previously successful application revision
- "Going back in time" to a known good state

#### Rollback Trigger Methods

**Automatic Rollback:**
- Deployment failure detected
- CloudWatch Alarm triggered indicating deployment issues

**Manual Rollback:**
- Initiated by operator/administrator
- Can be disabled if needed

#### Important: How Rollbacks Work
⚠️ **Exam Tip**: CodeDeploy does NOT restore the previous version. Instead:
- It redeploys the last known good revision as a **NEW deployment**
- Creates a new deployment version (doesn't revert)
- Uses the last successful deployment's code

### 5. Elastic Load Balancer (ELB) Integration
- Routes traffic between old and new versions during blue/green deployments
- Enables zero-downtime deployments
- Gradually shifts traffic from old to new target groups

## Study Tips
- Understand the difference between in-place and blue/green deployments
- Remember that rollbacks create NEW deployments, not restore operations
- Know the role of appspec.yml in the deployment process
- Be familiar with automatic vs manual rollback triggers

## Exam Focus Areas
✓ Rollback mechanism (new deployment vs restore)
✓ Blue/green vs in-place deployment differences
✓ ASG deployment capabilities
✓ AppSpec.yml file location and purpose
✓ Deployment hooks and validation
