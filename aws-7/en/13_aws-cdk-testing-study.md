# AWS CDK Testing - Study Notes

## 1. Why testing matters in CDK
When you use AWS CDK, your infrastructure is written as code.
That means you can test it like normal application code (Python, JavaScript, etc.).

CDK provides assertion modules that work with common test frameworks such as:
- Jest (JavaScript/TypeScript)
- Pytest (Python)

You can verify resources, rules, conditions, and parameters before deployment.

## 2. Main idea of CDK testing
In CDK tests, you usually check the synthesized CloudFormation template.
Goal: make sure the generated template contains exactly what you expect.

## 3. Two test types

### A) Fine-grained assertions (most common)
Test specific resources and properties.

Examples:
- A Lambda function has the correct handler.
- A Lambda function uses runtime `nodejs14.x`.
- An SNS topic has exactly one subscription.

Use this when you want precise checks for important properties.

### B) Snapshot tests
Compare the current synthesized template against a previously saved baseline template (snapshot).

Use this when you want to detect any unexpected infrastructure change.

## 4. Building the template under test
There are two important methods:

### `Template.fromStack(...)`
Use when the stack is defined in CDK code.

### `Template.fromString(...)`
Use when the CloudFormation template is external (not defined in CDK code).

These two methods are important to remember for exam and real-world usage.

## 5. Quick exam checklist
- Know the difference between fine-grained and snapshot tests.
- Know when to use `fromStack` vs `fromString`.
- Be able to assert key properties for Lambda, SNS, DynamoDB, and other resources.

## 6. Practical takeaway
Testing CDK helps you catch infrastructure mistakes early, improves confidence in deployments, and keeps changes controlled over time.
