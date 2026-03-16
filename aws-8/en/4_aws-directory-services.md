# AWS Directory Services Study Guide

## 1. What is Microsoft Active Directory (AD)?

Microsoft Active Directory is software found on **Windows Server** with **AD Domain Services**. It is essentially a **database of objects**, which can include:

- User accounts
- Computers
- Printers
- File shares
- Security groups

### Key Concepts

| Term | Description |
|------|-------------|
| **Domain Controller** | The central server that manages all AD objects |
| **Tree** | A hierarchical structure of objects in AD |
| **Forest** | A group of trees |

### How It Works (Simple Example)

1. A domain controller is set up.
2. An account is created (e.g., username: `John`, password: `password`).
3. All Windows machines in the network connect to the domain controller.
4. When a user logs in on any machine, the machine checks with the domain controller to verify credentials.
5. Users can access any machine in the network using a single account.

---

## 2. AWS Directory Services

AWS Directory Services provides a way to **create and use Active Directory on AWS**. There are **three main flavors**:

---

### 2.1 AWS Managed Microsoft AD

- Creates your **own Active Directory in AWS**.
- Manage users **locally** within AWS.
- Supports **Multi-Factor Authentication (MFA)**.
- Can establish a **trust connection** with your **on-premise AD**.
  - AWS AD trusts on-premise AD (and vice versa).
  - Users can authenticate against either directory.
  - Users are **shared** between AWS AD and on-premise AD.

**Editions:**
| Edition | Max Objects |
|---------|-------------|
| Standard | Up to 30,000 objects |
| Enterprise | Up to 500,000 objects |

> **Use case:** You want to manage users **both in AWS and on-premises**, with MFA support.

---

### 2.2 AD Connector

- Acts as a **direct gateway/proxy** to redirect authentication requests to your **on-premise AD**.
- Supports **MFA**.
- Users are **solely managed in the on-premise AD**.
- The AD Connector does **not** store any user data itself — it only proxies requests.

**Sizes:**
| Connector | Max Users |
|-----------|-----------|
| Small | Up to 500 users |
| Large | Up to 5,000 users |

> **Use case:** You want to **proxy users to on-premise AD** without storing anything in AWS.

---

### 2.3 Simple AD

- A **standalone, managed, AD-compatible directory** on AWS.
- Does **NOT** use Microsoft Active Directory technology.
- **Cannot** be joined with or connected to an on-premise Active Directory.

> **Use case:** You **don't have on-premise AD** and just need a simple standalone directory for your AWS cloud resources.

---

## 3. Comparison Table

| Feature | AWS Managed Microsoft AD | AD Connector | Simple AD |
|---------|--------------------------|--------------|-----------|
| Users managed in AWS | Yes | No | Yes |
| Users managed on-premise | Yes (via trust) | Yes (only here) | No |
| MFA support | Yes | Yes | No |
| Trust with on-premise AD | Yes | N/A (proxy) | No |
| Microsoft AD technology | Yes | Proxy only | No |
| Standalone | Yes | No | Yes |

---

## 4. Why Use AWS Directory Services with EC2?

- EC2 instances running **Windows** can join a domain controller.
- This allows Windows EC2 instances to **share logins and credentials**.
- Having a directory in AWS keeps it **closer to your EC2 instances**, reducing latency.

---

## 5. Exam Tips

- **AD Connector** → Proxy users to on-premise AD (no user management in AWS).
- **AWS Managed Microsoft AD** → Manage users in the cloud (AWS) with MFA + optional trust with on-premise.
- **Simple AD** → No on-premise AD exists; need a standalone directory in AWS only.

> **Note:** Amazon Cognito User Pool is sometimes listed alongside directory services in the console but is a **separate service** — it does NOT count as a directory service.
