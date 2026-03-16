# AWS Parameter Store Study Notes

## 1) What is Parameter Store?
AWS Systems Manager Parameter Store is a service for storing configuration values and secrets.

You can store:
- Plain configuration values (for example, database URL)
- Sensitive values (for example, passwords) encrypted with AWS KMS

## 2) How to open it in AWS Console
1. Search for Parameter Store in the AWS Console search bar.
2. Open it under Systems Manager > Application Tools > Parameter Store.

## 3) Naming and hierarchy
A recommended naming pattern from the lesson:
- `/my-app/dev/db-url`
- `/my-app/dev/db-password`
- `/my-app/prod/db-url`
- `/my-app/prod/db-password`

This path structure helps organize parameters by:
- Application (`my-app`)
- Environment (`dev`, `prod`)
- Setting name (`db-url`, `db-password`)

## 4) Tiers
### Standard
- Up to 10,000 parameters
- Max value size: 4 KB
- No parameter sharing with other accounts

### Advanced
- Up to 100,000 parameters
- Max value size: 8 KB
- Can share parameters with other accounts

## 5) Parameter types
- `String`: plain text value
- `StringList`: list of string values
- `SecureString`: encrypted value using KMS

## 6) SecureString and KMS
For sensitive values (like passwords), use `SecureString`.
You can encrypt using:
- AWS managed key: `alias/aws/ssm`
- Your customer-managed KMS key (for example, `Tutorial`)

To view decrypted values, user permissions must allow KMS decrypt operations.

## 7) CLI commands from the lesson

### Get specific parameters
```bash
aws ssm get-parameters \
  --names "/my-app/dev/db-url" "/my-app/dev/db-password"
```

### Decrypt SecureString values
```bash
aws ssm get-parameters \
  --names "/my-app/dev/db-url" "/my-app/dev/db-password" \
  --with-decryption
```

### Get parameters by path
```bash
aws ssm get-parameters-by-path --path "/my-app/dev"
```

### Get all parameters recursively under a namespace
```bash
aws ssm get-parameters-by-path \
  --path "/my-app" \
  --recursive
```

### Recursive + decryption
```bash
aws ssm get-parameters-by-path \
  --path "/my-app" \
  --recursive \
  --with-decryption
```

## 8) Key takeaways
- Use hierarchy paths to keep parameters organized.
- Use `SecureString` for secrets.
- Use KMS keys and IAM permissions for secure access.
- CLI commands make Parameter Store easy to automate in scripts.

## 9) Quick practice checklist
- Create 4 parameters (`dev` + `prod`, URL + password).
- Make password parameters `SecureString`.
- Retrieve values using `get-parameters`.
- Try `--with-decryption`.
- Try `get-parameters-by-path --recursive`.
