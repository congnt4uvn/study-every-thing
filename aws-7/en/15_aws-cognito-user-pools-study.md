# AWS Cognito User Pools - Study Notes

## 1. Lambda Triggers in User Pools
Cognito User Pools can invoke AWS Lambda functions synchronously during auth lifecycle events.

### Important authentication triggers
- Pre authentication: validate or block sign-in requests before authentication completes.
- Post authentication: log successful logins for analytics or auditing.
- Pre token generation: add, remove, or modify claims in tokens.

### Sign-up related triggers
- Pre sign-up: validate user attributes or apply custom sign-up logic.
- Post confirmation: run actions after user confirms registration (for example, send welcome workflows).
- Migrate user: move users from an old identity store into Cognito during sign-in.

### Message customization trigger
- Customize messages sent to users (email/SMS style and content).

## 2. Hosted Authentication UI
Cognito provides a built-in hosted login UI so applications do not need to build sign-up/sign-in screens from scratch.

### Benefits
- Faster implementation of authentication flows.
- Built-in integrations for social login providers, OIDC, and SAML.
- Can be branded with custom logo and CSS to match your app.

## 3. Custom Domain Requirement
When using a custom domain for Cognito hosted UI:
- You must use an HTTPS certificate from AWS Certificate Manager (ACM).
- The certificate must be created in region us-east-1.
- This rule applies even if your User Pool is in another region (for example, eu-west-1).
- Custom domain setup is configured in the App integration section of User Pools.

## 4. Adaptive Authentication
Adaptive authentication applies risk-based sign-in protection.

### How it works
- Cognito evaluates each sign-in attempt and assigns a risk level (low, medium, high).
- Based on risk, Cognito can:
  - Allow normal login.
  - Require MFA challenge.
  - Block suspicious sign-in attempts.

### Risk factors
- Device familiarity.
- Sign-in location.
- IP address patterns.
- Other behavioral/contextual signals.

### Security support
- Account takeover protection for compromised credentials.
- Extra verification such as phone/email checks when needed.
- Events are visible in CloudWatch logs (attempts, risk scores, challenge outcomes).

## 5. JWT Tokens from Cognito
After successful authentication, Cognito issues JWTs (JSON Web Tokens).

### JWT structure
- Header.
- Payload.
- Signature.

### Key validation rule
Always verify token signature before trusting payload data.

### Common payload claims
- sub: unique user ID in Cognito User Pool.
- username.
- cognito groups (if assigned).
- exp (token expiration).

Use sub to look up full user profile attributes in Cognito (email, given name, phone, custom attributes).

## 6. Exam and Practical Reminders
- Know which Lambda trigger is used for each lifecycle event.
- Remember the custom-domain certificate region requirement: us-east-1.
- Understand when adaptive authentication enforces MFA.
- Be able to explain why signature verification is mandatory for JWT trust.
- Use sub claim as the stable user identifier when integrating with downstream systems.
