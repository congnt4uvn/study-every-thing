# AWS Exam Study Guide

## Core Mindset
- Practice makes perfect.
- Do not rush the exam if you are not confident.
- Real hands-on work matters more than memorization.
- If needed, review the course again over weeks, not days.

## Recommended Hands-On Practice
1. Deploy an existing app manually on EC2.
2. Deploy the same app on Elastic Beanstalk with Auto Scaling.
3. Build a CI/CD pipeline (CodeCommit, CodeBuild, CodeDeploy, CodePipeline).
4. Break an app into components and decouple with SQS and SNS.
5. Try a serverless version with Lambda + API Gateway + DynamoDB.

## Practical Mini Projects
- Create a script (CLI/SDK) to stop EC2 at night and start in the morning.
- Automate daily EBS snapshots.
- Report underutilized EC2 instances (for example CPU < 10%).

## Exam Question Strategy
- Start by eliminating clearly wrong answers.
- Most questions are scenario-based.
- Avoid overthinking: there are very few trick questions.
- Prefer solutions that are simpler and operationally reasonable.
- If two answers look correct, choose the one with lower complexity and effort.
- Watch for keywords (for example "serverless" often suggests Lambda, API Gateway, DynamoDB).

## Important Reading and Review
### Whitepapers (skim at minimum)
- Security Best Practices
- Well-Architected Framework
- Architecting for the Cloud
- CI/CD on AWS
- Microservices on AWS
- Serverless Architectures with AWS Lambda
- Optimizing Enterprise Economics with Serverless
- Containerized Microservices on AWS
- Blue/Green Deployments on AWS

### Service FAQs
- Read FAQs for key services (especially weak areas).
- FAQs often clarify exam-style edge cases.

## Community and Learning Loop
- Join AWS community discussions and forums.
- Review Q&A from other learners.
- Learn by teaching: answer questions when possible.
- Use practice tests to identify weak domains.
- Watch selected AWS re:Invent talks for deeper understanding.

## 4-Week Study Plan (Example)
### Week 1
- IAM, EC2, EBS, VPC basics.
- Deploy one app to EC2 manually.

### Week 2
- Elastic Beanstalk, Auto Scaling, ELB.
- Build one CI/CD pipeline.

### Week 3
- SQS, SNS, Lambda, API Gateway, DynamoDB.
- Refactor one flow to serverless.

### Week 4
- Review weak topics, FAQs, and whitepapers.
- Take practice tests and analyze mistakes.

## Final Advice
- Build confidence through real implementation.
- Focus on practical architecture decisions.
- Keep a steady pace and avoid rushing exam day.
