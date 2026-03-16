# Ghi Chu Hoc AWS: Xac Thuc Nguoi Dung voi Application Load Balancer (ALB)

## 1) Y Tuong Chinh
Application Load Balancer (ALB) co the xac thuc nguoi dung **truoc khi** request vao ung dung.
Cach nay giup dua phan xac thuc ra khoi app, de app tap trung vao business logic.

## 2) Hai Cach Xac Thuc Tren ALB
ALB ho tro 2 tuy chon chinh:

1. **`authenticate-cognito`**
- Dung Amazon Cognito User Pools.
- Phu hop cho dang nhap mang xa hoi (Amazon, Google, Facebook) va federation doanh nghiep (SAML/LDAP/Microsoft AD thong qua Cognito).

2. **`authenticate-oidc`**
- Ket noi truc tiep voi nha cung cap dinh danh tuan theo OpenID Connect (OIDC).
- Linh hoat hon, nhung thuong can cau hinh thu cong nhieu hon.

## 3) Cau Hinh Listener Bat Buoc
De dung xac thuc tren ALB, can:
- Listener **HTTPS** (bat buoc bao mat)
- Rule action:
  - `authenticate-cognito`, hoac
  - `authenticate-oidc`
- Sau do forward request den backend/target group.

Thu tu thuong gap trong listener rule:
1. Xac thuc nguoi dung
2. Forward request den backend

## 4) Xu Ly Nguoi Dung Chua Xac Thuc
ALB co 3 cach xu ly:

1. **Authenticate** (mac dinh): chuyen huong nguoi dung den trang dang nhap
2. **Deny**: tu choi request
3. **Allow**: cho phep request di qua ma khong can xac thuc

`Allow` huu ich cho endpoint cong khai, vi du trang dang nhap.

## 5) Vi Du: ALB + Amazon ECS + Cognito
Luong xu ly tong quat:
1. Nguoi dung goi API (vi du: `GET /api/data`)
2. ALB ap dung `authenticate-cognito`
3. Cognito xac thuc nguoi dung
4. ALB forward request den ECS kem thong tin/claims cua nguoi dung
5. Ung dung co the tra ve response tuy theo nguoi dung

## 6) Cac Buoc Cai Dat (Cognito)
1. Tao Cognito User Pool
2. Tao App Client
3. Tao/cau hinh Cognito Domain
4. Dam bao ID token (JWT) duoc tra ve (mac dinh)
5. Neu can, ket noi voi social/corporate IdP
6. Cau hinh callback URL va redirect URL
7. Gan cau hinh Cognito vao ALB listener rule

## 7) Luong Tich Hop OIDC Truc Tiep
Voi `authenticate-oidc`, ALB lam viec truc tiep voi IdP:

1. ALB chuyen huong nguoi dung den authorization endpoint cua IdP
2. Nguoi dung dang nhap, IdP tra authorization code
3. ALB doi code tai token endpoint de lay ID/access token
4. ALB goi user info endpoint bang access token de lay user claims
5. ALB forward request goc + claims den backend

## 8) Thong So Cau Hinh OIDC
Thuong can khai bao:
- Authorization endpoint
- Token endpoint
- User info endpoint
- Client ID
- Client secret
- Redirect/callback URL dung

## 9) So Sanh Nhanh Cognito va OIDC
- **Cognito**: tich hop AWS-native de hon, setup nhanh hon trong nhieu truong hop
- **OIDC truc tiep**: linh hoat hon ve nha cung cap, nhung cau hinh thu cong nhieu hon

## 10) Diem Trong Tam De On Thi/Phong Van
- Xac thuc ALB bat buoc listener **HTTPS**.
- Rule action la `authenticate-cognito` va `authenticate-oidc`.
- ALB co the offload xac thuc khoi code ung dung.
- Nguoi dung chua dang nhap co the xu ly theo 3 che do: authenticate/deny/allow.
- Backend nhan duoc thong tin nguoi dung sau khi xac thuc thanh cong.

## 11) Cau Hoi Tu On Nhanh
1. Vi sao xac thuc tai ALB co loi cho kien truc ung dung?
2. Khac nhau chinh giua `authenticate-cognito` va `authenticate-oidc` la gi?
3. Vi sao xac thuc ALB bat buoc HTTPS?
4. Khi nao nen chon `allow` cho request chua xac thuc?
5. Khi dung OIDC thi can cau hinh cac endpoint nao?
