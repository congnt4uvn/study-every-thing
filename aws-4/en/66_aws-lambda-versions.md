# AWS Lambda Versions - Study Guide

## Overview
AWS Lambda versions allow you to fix a specific amount of code, resources, and settings at a point in time. This enables you to author and manage different versions of your Lambda function as it evolves.

## Key Concepts

### What are Lambda Versions?
- Versions are snapshots of your Lambda function code and configuration
- Each version is immutable (cannot be changed once published)
- Allows functions to evolve over time while maintaining stable references to previous versions

### Version Identification
- **$LATEST**: The unpublished, editable version of your function
- **Numbered versions**: Published versions (1, 2, 3, etc.)

## Step-by-Step Tutorial: Creating Lambda Versions

### Step 1: Create a Lambda Function
1. Create a new function named: `lambda-version-demo`
2. Runtime: Python 3.8
3. Create the function

### Step 2: Write Version 1 Code
```python
def lambda_handler(event, context):
    return "this is version one."
```

### Step 3: Deploy and Test
1. Deploy your changes
2. Create a sample test event
3. Test the function
4. Verify output: "this is version one."

### Step 4: Publish Version 1
1. Click **Action** → **Publish new version**
2. Add a description (optional)
3. Click **Publish**
4. Version 1 is now created and immutable

### Step 5: Understanding Version Behavior
- When viewing a published version (e.g., Version 1):
  - The designer/code editor is read-only
  - You cannot modify the code
  - You can still test the function
  - The version number appears in the function overview

### Step 6: Continue Development
1. Return to the main function ($LATEST)
2. Edit the code for the next version:
```python
def lambda_handler(event, context):
    return "this is version two."
```
3. Deploy and test the changes
4. The function now shows: "this is version two."

## Important Notes

- ✅ Published versions are immutable
- ✅ Only $LATEST version can be edited
- ✅ Each published version maintains its own code snapshot
- ✅ You can test any version at any time
- ✅ Versions enable safe deployment and rollback strategies

## Use Cases

1. **Safe Deployments**: Test new code without affecting production
2. **Rollback Capability**: Quick revert to previous stable versions
3. **A/B Testing**: Run different versions simultaneously
4. **Gradual Updates**: Use aliases to shift traffic between versions

## Best Practices

- Always test thoroughly before publishing a version
- Add meaningful descriptions when publishing versions
- Use aliases to manage version routing in production
- Keep track of which versions are in use
- Clean up unused old versions periodically

---

**Practice Exercise**: Create your own Lambda function, publish multiple versions, and test switching between them to understand the immutability and versioning workflow.
