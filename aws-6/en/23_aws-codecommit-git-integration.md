# AWS CodeCommit - Git Integration Study Guide

## Overview
AWS CodeCommit is a fully managed source control service that hosts secure Git-based repositories. This guide covers how to integrate Git with AWS CodeCommit.

## Prerequisites
- AWS Account with IAM user
- Git installed on your machine
- Basic understanding of version control

## Authentication Methods

### 1. SSH Keys
- **Use case**: For Git experts familiar with SSH
- **Setup location**: IAM → Users → Security Credentials → SSH keys for AWS CodeCommit
- **Steps**:
  1. Upload your SSH public key to AWS IAM
  2. Navigate to your CodeCommit repository
  3. Select "Clone URL" → "Clone SSH"
  4. Use the SSH URL with git clone command

### 2. HTTPS Git Credentials (Recommended for Beginners)
- **Use case**: Easier setup for users new to Git
- **Setup location**: IAM → Users → Security Credentials → HTTPS Git credentials for AWS CodeCommit
- **Steps**:
  1. Click "Generate" to create credentials
  2. Download and save the credentials (username and password)
  3. Note: You can generate up to 2 sets of credentials per user

## Cloning a Repository

### Using HTTPS
```bash
# 1. Get the HTTPS clone URL from CodeCommit
# 2. Clone the repository
git clone <HTTPS_URL>

# 3. Enter your Git credentials when prompted
Username: <your-git-username>
Password: <your-git-password>
```

### Verify Git Installation
```bash
# Check if Git is installed
git --version

# Should return something like: git version 2.9.2 or higher
```

## Installing Git
- **Windows**: Download from [git-scm.com](https://git-scm.com)
- **Mac**: Use Homebrew or download installer
- **Ubuntu/Linux**: `sudo apt-get install git`

## Working with Cloned Repository

After cloning, you'll have a local copy of your repository:
```bash
# Navigate into the repository
cd <repository-name>

# Check current branch
git branch

# List files
ls
```

## Managing Git Credentials in IAM

In the Security Credentials section, you can:
- Generate new credentials
- View active credential status
- Reset passwords
- Make credentials inactive
- Delete credentials

## Key Points to Remember

1. **Two Authentication Options**: SSH keys or HTTPS credentials
2. **Credential Limit**: Up to 2 HTTPS Git credentials per IAM user
3. **Security**: Credentials are specific to CodeCommit
4. **UI vs Command Line**: Command line is more practical for regular development workflow
5. **Git Required**: Must have Git installed locally to work with CodeCommit

## Best Practices

- Keep your Git credentials secure and never share them
- Use SSH keys if you're comfortable with SSH
- Use HTTPS credentials for simpler setup
- Regularly rotate your credentials for security
- Download and save credentials immediately after generation

## Exam Tips

- Remember that CodeCommit supports both SSH and HTTPS authentication
- Know the location to generate Git credentials (IAM → Security Credentials)
- Understand the difference between Access Keys (for AWS CLI/SDK) and Git credentials (for CodeCommit)
- You don't need to be a Git expert for the exam, but understand the basic integration concepts

## Next Steps

Once you have Git connectivity established:
1. Add new files to your repository
2. Commit changes locally
3. Push changes to CodeCommit
4. Collaborate with team members

---

*Study Date: March 15, 2026*
