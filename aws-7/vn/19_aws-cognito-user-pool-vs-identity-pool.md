# Ghi Chu Hoc AWS: Cognito User Pools va Identity Pools

## 1. Tong quan
Amazon Cognito co 2 thanh phan khac nhau, giai quyet 2 bai toan khac nhau:

- **Cognito User Pools** -> Xac thuc (Authentication): Ban la ai?
- **Cognito Identity Pools** -> Phan quyen truy cap AWS (Authorization): Ban duoc lam gi trong AWS?

Nham lan pho bien la dung User Pool cho bai toan phan quyen AWS, hoac nguoc lai.

## 2. Cognito User Pools (Xac thuc)
Dung User Pools khi can **quan ly nguoi dung ung dung** web/mobile.

### Tinh nang chinh
- Co so du lieu nguoi dung duoc quan ly boi Cognito
- Luong dang ky / dang nhap
- Ho tro dang nhap lien ket (federation):
  - Social login (Google, Facebook, Amazon)
  - OIDC
  - SAML (dang nhap doanh nghiep)
- Hosted UI co the tuy chinh giao dien/logo
- Tich hop Lambda trigger trong auth flow (pre-auth, post-auth,...)
- Ho tro adaptive authentication va MFA

### Y chinh
User Pools xac minh danh tinh va tra ve token nguoi dung.

## 3. Cognito Identity Pools (Phan quyen)
Dung Identity Pools khi nguoi dung can **temporary AWS credentials** de truy cap tai nguyen AWS.

### Tinh nang chinh
- Doi token/danh tinh hop le lay temporary credentials (qua STS)
- Anh xa nguoi dung vao IAM roles va policies
- Kiem soat truy cap chi tiet vao tai nguyen AWS
- Ho tro nguoi dung chua xac thuc (guest/unauthenticated)

### Y chinh
Identity Pools quyet dinh nguoi dung duoc truy cap tai nguyen AWS nao.

## 4. Khi nao dung cai nao?

### Truong hop A
Chi can dang nhap va quan ly tai khoan nguoi dung.

- Dung **Cognito User Pools**

### Truong hop B
Nguoi dung can truy cap truc tiep den AWS (vi du S3, DynamoDB).

- Dung **Cognito Identity Pools**
- Thuong ket hop voi User Pools

## 5. Luong ket hop tot nhat
1. Nguoi dung dang nhap qua **Cognito User Pool** (hoac IdP lien ket).
2. Ung dung nhan token sau khi danh tinh duoc xac minh.
3. Ung dung doi token voi **Cognito Identity Pool**.
4. Identity Pool dung STS cap temporary AWS credentials.
5. Ung dung goi API AWS (S3/DynamoDB) bang credentials tam thoi.
6. IAM role/policy dinh nghia dung quyen can thiet.

## 6. Bang so sanh nhanh
| Chu de | User Pools | Identity Pools |
|---|---|---|
| Muc dich chinh | Xac thuc | Phan quyen truy cap AWS |
| Dau ra | User identity tokens | Temporary AWS credentials |
| Nen tang quyen | CSDL nguoi dung Cognito | IAM roles + STS |
| Ho tro guest | Khong phai use case chinh | Co |
| Truy cap truc tiep S3/DynamoDB | Khong tu than | Co (qua IAM policy) |

## 7. Meo ghi nho
- **User Pool = "Dang nhap"**
- **Identity Pool = "Truy cap AWS"**

Hoac:
- Xac minh danh tinh truoc (authn)
- Cap quyen sau (authz)

## 8. Câu hoi tu kiem tra
1. Thanh phan nao cua Cognito luu nguoi dung ung dung?
2. Thanh phan nao cap temporary AWS credentials?
3. Identity Pools co the dung doc lap khong?
4. Tai sao mobile app truy cap S3/DynamoDB nen ket hop ca hai?

## 9. Tom tat 1 cau
Dung **User Pools** de xac thuc nguoi dung, va dung **Identity Pools** de cap quyen truy cap AWS bang temporary credentials dua tren IAM.
