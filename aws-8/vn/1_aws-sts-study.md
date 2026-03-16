# Ghi Chu On Tap AWS STS

## AWS STS La Gi?
AWS Security Token Service (STS) cung cap thong tin xac thuc tam thoi de truy cap tai nguyen AWS.

- Thoi gian hieu luc: thuong tu 15 phut den 1 gio
- Truong hop dung pho bien: assume role, federated access, API bat buoc MFA, truy cap cross-account

## Cac API STS Quan Trong

### 1. AssumeRole
Dung de assume IAM role:
- Trong cung account
- Giua cac account khac nhau (cross-account)

Vi sao quan trong:
- Nen tang cho mo hinh least privilege
- Noi dung trong tam cho ky thi AWS

### 2. AssumeRoleWithSAML
Dung khi nguoi dung dang nhap thong qua nha cung cap danh tinh SAML.

### 3. AssumeRoleWithWebIdentity
Dung cho nguoi dung dang nhap bang nha cung cap danh tinh web (vi du Google, Facebook, OIDC).

Luu y:
- Kien truc hien dai thuong uu tien Cognito Identity Pools thay vi goi truc tiep `AssumeRoleWithWebIdentity`.

### 4. GetSessionToken
Dung de lay credential tam thoi cho IAM user (hoac root user), dac biet khi bat MFA.

Gia tri tra ve:
- Access key ID
- Secret access key
- Session token
- Thoi diem het han

### 5. GetFederationToken
Dung de lay credential tam thoi cho federated user.

### 6. GetCallerIdentity
Tra ve thong tin danh tinh dang goi API:
- Account ID
- ARN
- Thong tin principal

Huu ich khi:
- Ban khong chac profile/credential nao dang duoc su dung.

### 7. DecodeAuthorizationMessage
Giai ma thong diep loi phan quyen duoc ma hoa trong phan hoi AWS API.

Huu ich de:
- Phan tich loi kieu `AccessDenied`.

## API Can Uu Tien On Thi
Tap trung manh vao:
- `AssumeRole`
- `GetSessionToken`
- `GetCallerIdentity`
- `DecodeAuthorizationMessage`

## Cac Buoc Hoat Dong Cua AssumeRole
1. Tao hoac xac dinh IAM role dich.
2. Cau hinh trust policy (ai duoc phep assume role).
3. Gan permission policies (role duoc lam gi).
4. Goi STS `AssumeRole`.
5. Dung credential tam thoi tra ve de goi AWS services voi quyen cua role do.

## Luong Truy Cap Cross-Account
1. Tao role trong target account.
2. Cau hinh trust relationship cho phep principal tu source account.
3. Dam bao quyen IAM dung o ca hai ben.
4. Goi `AssumeRole` tu source account.
5. Dung credential tam thoi de truy cap tai nguyen target account (vi du S3).

## STS Ket Hop MFA (Noi Dung Trong Tam)
Dung `GetSessionToken` sau khi xac thuc MFA, sau do ep buoc MFA trong IAM condition.

Vi du IAM condition:
- `"aws:MultiFactorAuthPresent": true`

Tac dung thuc te:
- Hanh dong nhay cam (vi du stop/terminate EC2) chi duoc phep khi co MFA.

## Checklist On Nhanh
- Phan biet khi nao dung `AssumeRole` va `GetSessionToken`.
- Hieu ro trust policy + permission policy khi assume role.
- Nho credential tam thoi luon co han su dung.
- Dung `GetCallerIdentity` de xac nhan danh tinh hien tai.
- Dung `DecodeAuthorizationMessage` de debug loi bi tu choi API.
