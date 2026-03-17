# AWS AppConfig Study Notes

## 1. What is AWS AppConfig?
AWS AppConfig helps you manage application configuration outside your application code.

With AppConfig, you can:
- Configure dynamic settings
- Validate configurations before rollout
- Deploy configuration changes safely
- Roll back automatically when issues are detected

This lets your app behavior change without redeploying code or restarting services.

## 2. Why use AppConfig?
In many apps, configuration is bundled with code or environment variables. That works, but it is less flexible.

AppConfig provides:
- Faster and safer config changes
- Independent config lifecycle from application deployment
- Better control over gradual rollouts
- Runtime updates for modern cloud workloads

## 3. Feature Flags Example
A common use case is feature flags.

Example flow:
1. Deploy new code with a feature flag set to `false`
2. Verify system stability
3. Switch flag to `true` in AppConfig
4. Application picks up the new value and enables the feature

No code redeploy is required.

## 4. Other Dynamic Configuration Use Cases
AppConfig can manage many runtime settings, for example:
- Performance tuning parameters
- IP allow lists / block lists
- Operational thresholds
- Business rules toggles

## 5. Where does configuration come from?
Based on the source material, AppConfig can use sources such as:
- AWS Systems Manager Parameter Store
- AWS Systems Manager Documents
- Amazon S3
- Other supported locations

Applications (running on EC2, Lambda, ECS, EKS, etc.) retrieve updates regularly.

## 6. Safe Deployment and Rollback
AppConfig supports gradual configuration deployment.

Why gradual rollout matters:
- Reduces blast radius
- Helps detect issues early
- Allows automatic rollback if health signals degrade

Monitoring can be integrated with Amazon CloudWatch alarms.
If alarms trigger, AppConfig can roll back to a previous known-good configuration.

## 7. Configuration Validation Options
Before deployment, AppConfig can validate config using:
- JSON Schema: structural/type validation
- AWS Lambda validator: custom logic for complex checks

This helps prevent invalid configs from reaching production.

## 8. Services Mentioned in Context
The transcript highlights that AppConfig is useful for applications running on:
- Amazon EC2
- AWS Lambda
- Amazon ECS
- Amazon EKS

## 9. Quick Exam-Style Summary
- AppConfig separates configuration from code deployment.
- It enables runtime config changes.
- It supports feature flags and dynamic operational controls.
- It provides validation, staged rollout, CloudWatch monitoring, and rollback.

## 10. Self-Check Questions
1. Why is externalized configuration useful compared to hardcoded config?
2. How does AppConfig improve feature flag operations?
3. What is the difference between JSON Schema and Lambda validation?
4. Why is gradual rollout safer than immediate full rollout?
5. How do CloudWatch alarms support AppConfig safety?
