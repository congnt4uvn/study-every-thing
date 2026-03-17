# AWS Study Notes: ACM + Elastic Beanstalk + HTTPS

## Lesson Goal
Deploy a web app with HTTPS by:
- Requesting an SSL/TLS certificate in AWS Certificate Manager (ACM)
- Validating domain ownership with Route 53 (DNS validation)
- Attaching the certificate to an Application Load Balancer in Elastic Beanstalk
- Accessing the app securely through a custom domain

## Architecture Used
- **ACM**: Issues and manages the public certificate
- **Route 53**: Hosts DNS zone and validation/CNAME records
- **Elastic Beanstalk**: Deploys app environment
- **Application Load Balancer (ALB)**: Terminates HTTPS on port 443
- **EC2 + Auto Scaling Group**: Created by Beanstalk environment

## Step-by-Step Process

### 1. Request a public certificate in ACM
1. Open **AWS Certificate Manager**.
2. Choose **Request a public certificate**.
3. Enter domain name (example: `acmdemo.example.com`).
4. Select **DNS validation**.
5. Keep default key algorithm and submit request.

### 2. Validate domain ownership in Route 53
1. In ACM, find pending validation record.
2. Click **Create records in Route 53**.
3. Wait until certificate status changes to **Issued**.

## 3. Create Elastic Beanstalk environment with HTTPS listener
1. Create a new **Web server environment**.
2. Use a managed platform (example from lesson: Node.js sample app).
3. Select **Application Load Balancer**.
4. Add listener:
   - Port: **443**
   - Protocol: **HTTPS**
5. Select the ACM certificate you just issued.
6. Choose a TLS security policy.
7. Launch environment.

## 4. Point custom domain to Beanstalk URL
1. In Route 53 hosted zone, create a DNS record:
   - Name: `acmdemo`
   - Type: **CNAME**
   - Value: Beanstalk environment domain (without protocol)
2. Wait for DNS propagation.

## 5. Verify HTTPS is working
- Open `https://acmdemo.example.com`.
- Confirm browser lock icon and valid certificate details.
- In **EC2 > Load Balancers > Listeners**, verify HTTPS 443 listener and attached ACM certificate.

## Key Concepts to Remember
- DNS validation is fast and simple when ACM and Route 53 are in the same AWS account.
- TLS is terminated at the ALB, not on EC2 instances.
- You can manage default or additional certificates on the ALB listeners.
- DNS propagation delay can temporarily cause access issues.

## Common Issues
- Certificate stuck in **Pending validation**: DNS validation record missing or incorrect.
- Domain not resolving: CNAME not created correctly or propagation not complete.
- HTTPS not active: Listener 443 missing or wrong certificate selected.

## Cleanup (Important for Cost)
After testing:
1. Delete Elastic Beanstalk environment/application.
2. Remove Route 53 test records (optional but recommended).
3. Delete unused ACM certificates if no longer needed.

## Quick Review Questions
1. Why is DNS validation commonly preferred with Route 53?
2. Where is HTTPS terminated in this setup?
3. Which DNS record maps your custom subdomain to the Beanstalk URL?
4. What should you delete to avoid ongoing charges?
