# Ghi Chu Hoc AWS: Cognito Identity Pool

## Tong Quan
Cognito Identity Pool cho phep nguoi dung nhan temporary AWS credentials. Cac credentials nay duoc gan vao IAM roles va permissions.

Tai lieu nay duoc tong hop tu quy trinh thuc hanh voi:
- Authenticated access
- Guest (unauthenticated) access
- Gan IAM role cho tung loai truy cap

## Cau Hinh Ban Dau
Khi tao Identity Pool, ban chon cac loai truy cap:
- Authenticated access
- Guest access (tuy chon)

Voi authenticated access, can chon identity provider (IdP), vi du:
- Amazon Cognito User Pool
- Facebook
- Google
- Apple
- Amazon
- Twitter
- OIDC
- SAML
- Custom developer provider

Trong bai thuc hanh nay, IdP duoc chon la Amazon Cognito User Pool.

## IAM Roles Trong Identity Pool
Ban can cau hinh 2 IAM roles:
- Authenticated role: duoc signed-in users su dung
- Unauthenticated role: duoc guest users su dung

Moi role nen chi co dung quyen can thiet (least privilege).

Vi du ten role trong huong dan:
- Cognito Identity Pool Authenticated Role Demo
- Unauthenticated Role Demo

## Lien Ket User Pool Va Identity Pool
Vi da chon Cognito User Pool lam nguon dang nhap, ban phai cung cap:
- User Pool ID
- App Client ID

## Lua Chon Mapping Role
Voi authenticated users, co 2 cach mapping role:
- Dung default authenticated role
- Dung rules dua tren token claims

Nang cao:
- Co the dung token attributes (vi du username, client) trong IAM policy conditions de kiem soat truy cap chi tiet hon.

## Buoc Tao Pool Cuoi Cung
- Dat ten Identity Pool (vi du: Demo Identity Pool)
- Giu mac dinh authentication mode neu chua chac chan
- Tao Identity Pool

Sau khi tao xong, he thong co ca authenticated va guest access.

## Sau Khi Tao Identity Pool
Quy trinh tich hop ung dung thuong la:
1. Cau hinh AWS SDK trong ung dung.
2. Xac thuc nguoi dung qua IdP da chon.
3. Doi identity de lay temporary AWS credentials.
4. Dung credentials do de goi AWS services.

## Noi Quan Ly Permissions
Vao IAM Roles va tim cac role duoc tao cho Identity Pool (thuong co chu "Cognito").

Sau do:
- Gan managed policies, hoac
- Tao inline policies

Vi du cau hinh quyen:
- Service: Amazon S3
- Permission: read/get access

## Diem Quan Trong Cho Hoc Tap / Phong Van
- Identity Pool cap AWS credentials, khong phai giao dien dang nhap.
- User Pool xu ly sign-up/sign-in; Identity Pool xu ly cap quyen truy cap AWS.
- Tach role cho authenticated va guest users la thiet ke bao mat quan trong.
- Mapping role theo claims giup phan quyen chi tiet.

## Best Practices
- Bat dau voi quyen toi thieu.
- Tach ro kha nang guest va authenticated.
- Kiem tra IAM policy conditions khi dung token attributes.
- Thu nghiem credentials va duong truy cap trong code thuc te.

## Tom Tat Nhanh
Cognito Identity Pool la cau noi giua user identity va truy cap tai nguyen AWS. Ban quyet dinh ai duoc truy cap (auth hay guest), ho se assume role nao, va duoc phep thuc hien hanh dong gi tren AWS thong qua IAM policies.
