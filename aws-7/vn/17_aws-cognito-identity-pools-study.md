# Ghi Chu Hoc AWS: Cognito Identity Pools (Federated Identities)

## 1. Identity Pool La Gi

Amazon Cognito Identity Pools (con goi la Federated Identities) cho phep nguoi dung ben ngoai AWS nhan thong tin dang nhap AWS tam thoi.

Doi tuong thuong gap:
- Nguoi dung ung dung web
- Nguoi dung ung dung mobile

Sau do ho co the goi truc tiep den cac dich vu AWS nhu:
- Amazon S3
- Amazon DynamoDB

## 2. Vi Sao Can Identity Pools

Khong nen tao IAM User thong thuong cho tung end user vi:
- So luong nguoi dung rat lon
- Khong scale tot
- Muc do tin cay cua end user khong cao

Thay vao do, Identity Pools cap temporary credentials thong qua AWS STS.

## 3. Cac Nha Cung Cap Danh Tinh Ho Tro

Identity Pools co the tin cay token dang nhap tu:
- Amazon Cognito User Pools
- Nha cung cap cong khai (Amazon, Google, Facebook, Apple)
- OpenID Connect (OIDC)
- SAML
- Developer authenticated identities (he thong dang nhap tu xay)

Ngoai ra, Identity Pools ho tro ca nguoi dung khong xac thuc (guest).

## 4. Luong Xac Thuc Tong Quan

1. Nguoi dung dang nhap qua mot identity provider da cau hinh.
2. Nguoi dung nhan token.
3. Ung dung gui token den Cognito Identity Pool.
4. Identity Pool xac minh token voi provider.
5. Identity Pool goi AWS STS (`AssumeRoleForWebIdentity`).
6. STS tra ve temporary AWS credentials.
7. Ung dung dung credentials de goi truc tiep cac AWS service.

## 5. Ket Hop Identity Pools Va User Pools

Kien truc pho bien:
- User Pools xu ly dang nhap va quan ly user directory.
- User Pools cap JWT token.
- Identity Pools doi JWT token thanh temporary AWS credentials.

Loi ich:
- Tap trung quan ly user trong User Pools
- Kiem soat quyen truy cap AWS chi tiet thong qua IAM role/policy

## 6. Gan Role Va Kiem Soat Truy Cap

Identity Pools quyet dinh quyen truy cap dua tren IAM roles va IAM policies.

Co the cau hinh:
- Role mac dinh cho authenticated users
- Role mac dinh cho unauthenticated (guest) users
- Rule map user vao role (dua tren user ID/thuoc tinh)

Yeu cau quan trong:
- IAM role phai co trust policy cho phep Cognito Identity Pools assume role.

## 7. Vi Du Fine-Grained Access Control

### Vi Du A: Guest Chi Duoc Doc 1 Object S3

Policy cho guest co the chi cho phep:
- `s3:GetObject` tren 1 object cu the (vi du `my_picture.jpg`)

=> Quyen guest bi gioi han rat chat.

### Vi Du B: User Da Dang Nhap Chi Duoc Truy Cap Prefix Cua Minh Tren S3

Dung policy variable (identity ID) de moi user chi truy cap duoc du lieu trong prefix cua chinh ho.

Ket qua:
- User A khong doc duoc du lieu cua User B.

### Vi Du C: Bao Mat Theo Tung Dong Du Lieu Tren DynamoDB

Dung IAM condition key (vi du `dynamodb:LeadingKeys`) gan voi user identity.

Ket qua:
- Moi user chi truy cap duoc cac row thuoc ve key cua minh.

## 8. API Va Luu Y Bao Mat

Identity Pools lay credentials tu STS bang API:
- `AssumeRoleForWebIdentity`

Mo hinh bao mat:
- Credentials la tam thoi
- Pham vi truy cap phu thuoc role policy
- Nen ap dung least privilege

## 9. Diem Can Nho Cho Thi Va Phong Van

Phan biet ro:
- User Pool = xac thuc + luu tru thong tin nguoi dung
- Identity Pool = cap quyen truy cap AWS resource bang temporary credentials

Tom tat nhanh:
- Dang nhap -> token -> Identity Pool -> STS credentials -> truy cap truc tiep AWS

## 10. Checklist Luyen Tap

- Tao Identity Pool
- Them it nhat 1 identity provider
- Cau hinh role cho auth user va guest
- Gan IAM policy theo least privilege
- Test truy cap S3 voi guest va authenticated user
- Test fine-grained access tren DynamoDB
