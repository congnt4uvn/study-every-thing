# Ghi Chu Hoc AWS: Amazon Cognito

## Amazon Cognito la gi?
Amazon Cognito cap danh tinh cho nguoi dung de ho co the tuong tac voi ung dung web va mobile.

- Cac nguoi dung nay thuong nam ngoai tai khoan AWS cua ban.
- Cognito giup xac thuc va quan ly nhom nguoi dung ben ngoai nay.

## Cac thanh phan chinh
Amazon Cognito co 2 dich vu con chinh:

### 1. Cognito User Pool
Muc dich: Dang nhap va xac thuc nguoi dung cho ung dung.

Y chinh:
- Cung cap chuc nang dang ky/dang nhap.
- Tich hop tot voi API Gateway.
- Tich hop tot voi Application Load Balancer (ALB).

### 2. Cognito Identity Pool (Federated Identities)
Muc dich: Cap temporary AWS credentials cho nguoi dung da xac thuc.

Y chinh:
- Truoc day duoc goi la Federated Identity.
- Cho phep nguoi dung ung dung truy cap truc tiep mot so tai nguyen AWS (voi quyen duoc kiem soat).
- Co kha nang tich hop voi Cognito User Pools.

## Khac nhau giua Cognito va IAM Users
- IAM users thuong dung cho nguoi/tainguyen ben trong tai khoan AWS.
- Cognito users thuong la nguoi dung web/mobile nam ngoai tai khoan AWS.

## Tu khoa de nho khi hoc/lam bai
Hay chu y cac dau hieu:
- So luong nguoi dung lon (hang tram tro len)
- Nguoi dung ung dung mobile hoac web
- Bai toan xac thuc/federation (vi du: SAML)
- Can cap temporary AWS credentials cho end users

## Tom tat nhanh
- Dung User Pools cho authentication (nguoi dung la ai).
- Dung Identity Pools cho authorization vao tai nguyen AWS (nguoi dung duoc lam gi).
