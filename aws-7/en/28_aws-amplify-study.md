# AWS Amplify Study Notes

## 1. What This Lesson Covers
This lesson shows how to quickly deploy a React app with AWS Amplify, connect it to GitHub, and understand what Amplify creates in your AWS account.

## 2. End-to-End Workflow
1. Open AWS Amplify and choose **Create new app**.
2. Use the starter template from the docs.
3. Clone the template repository into your own GitHub account.
4. In Amplify, choose **GitHub** as the source provider.
5. Authorize Amplify to access your repository.
6. Select the cloned repository and branch.
7. Keep default build settings.
8. Let Amplify create and use a new service role automatically.
9. Click **Save and deploy**.

## 3. What Happens During Deployment
- Amplify bootstraps required resources in your AWS account.
- AWS CDK/CloudFormation stacks are created or updated.
- The app is built and deployed automatically through CI/CD.
- A hosted domain URL is generated for your app.

## 4. Services You Interact With
- **AWS Amplify Console**: Main place to manage build/deploy and app settings.
- **CloudFormation**: Shows stack creation and nested stacks.
- **Data Manager (Amplify)**: View/edit app data records.
- **DynamoDB**: Underlying database table for to-do items.
- **User Management (Cognito integration)**: Manage authentication users.
- **Storage (for example S3-backed)**: Configure backend file/object storage.
- **Functions (Lambda-backed)**: Add backend serverless functions.
- **UI Library**: Use UI components and Figma-to-React features.

## 5. Key Learning Points
- Amplify gives an all-in-one workflow for full-stack app hosting on AWS.
- Much of the infrastructure is abstracted, but still visible in CloudFormation.
- Data created in the app appears in both Amplify Data Manager and DynamoDB.
- You can extend the app with authentication, storage, and serverless functions.
- CI/CD deployment is built in when connected to GitHub.

## 6. Common Console Areas to Explore
- Deployments
- Data
- User management
- Storage
- Functions
- UI library
- Custom domains
- Build notifications
- Build settings
- Environment variables

## 7. Cleanup Steps (Important)
1. In Amplify app settings, open **General settings**.
2. Delete the app (confirm by typing `delete`).
3. In GitHub, delete the repository if no longer needed.

## 8. Quick Self-Check Questions
1. Why do we connect Amplify to GitHub?
2. Which AWS service stores the to-do items?
3. Where can you inspect the infrastructure Amplify creates?
4. What service role choice is used in this walkthrough?
5. Which feature can be used to add authentication?

## 9. Mini Practice Task
- Deploy the starter app.
- Add at least 2 to-do items.
- Verify records in Amplify Data Manager.
- Verify records in DynamoDB.
- Delete all created resources after practice.
