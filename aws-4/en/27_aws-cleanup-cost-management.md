# AWS Cleanup and Cost Management

## Overview
This guide covers how to delete AWS resources to manage and control your costs effectively after completing a course or project.

## Resources to Clean Up

### 1. Elastic Beanstalk (Most Expensive)
Elastic Beanstalk is typically the most expensive resource to run, so it's critical to delete it when no longer needed.

**Steps to delete:**
1. Go to the Elastic Beanstalk console
2. Navigate to your environments
3. Click on the application you want to delete
4. Select "Delete" to remove the application
5. This will automatically delete all associated environments

**Important:** Make sure to delete Elastic Beanstalk first as it's the most costly resource.

### 2. CodePipeline
CodePipeline can be deleted to reduce costs when you're not actively deploying.

**Steps to delete:**
1. Go to the CodePipeline console
2. Click on your pipeline
3. Select "Edit" if needed
4. Click "Delete" to remove the pipeline

### 3. CodeDeploy
Similar to CodePipeline, CodeDeploy can be removed when not in use.

**Steps to delete:**
1. Navigate to the CodeDeploy console
2. Select the deployment configuration or application
3. Delete the resources as needed

## Cost Control Best Practices

- **Priority cleanup:** Always delete Elastic Beanstalk first due to its high cost
- **Regular reviews:** Periodically check for unused resources
- **Complete cleanup:** Delete all resources created during learning or testing
- **Monitor billing:** Keep an eye on your AWS billing dashboard

## Key Takeaways

✅ Elastic Beanstalk is the most expensive resource - delete it first  
✅ CodePipeline and CodeDeploy can be safely deleted when not in use  
✅ Deleting the application in Elastic Beanstalk removes all environments  
✅ Regular cleanup helps maintain cost control
