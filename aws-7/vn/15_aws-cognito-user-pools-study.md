# Ghi Chu Hoc AWS Cognito User Pools

## 1. Lambda Trigger trong User Pools
Cognito User Pools co the goi ham AWS Lambda dong bo trong cac su kien xac thuc.

### Trigger quan trong cho dang nhap
- Pre authentication: kiem tra va co the chap nhan/tu choi yeu cau dang nhap truoc khi xac thuc xong.
- Post authentication: ghi log dang nhap thanh cong de phan tich hoac kiem toan.
- Pre token generation: them, xoa, hoac chinh sua claim trong token.

### Trigger lien quan den dang ky
- Pre sign-up: kiem tra du lieu nguoi dung hoac ap dung logic dang ky tuy chinh.
- Post confirmation: xu ly sau khi nguoi dung xac nhan tai khoan (vi du gui quy trinh chao mung).
- Migrate user: di chuyen nguoi dung tu he thong cu sang Cognito trong luc dang nhap.

### Trigger tuy chinh noi dung tin nhan
- Tuy chinh noi dung email/SMS gui cho nguoi dung.

## 2. Hosted Authentication UI
Cognito cung cap man hinh dang nhap san, giup ung dung khong can tu xay giao dien dang ky/dang nhap tu dau.

### Loi ich
- Trien khai nhanh quy trinh xac thuc.
- Tich hop san social login, OIDC va SAML.
- Co the tuy chinh logo va CSS de dong bo voi thuong hieu ung dung.

## 3. Yeu cau Custom Domain
Khi dung custom domain cho hosted UI cua Cognito:
- Phai dung chung chi HTTPS trong AWS Certificate Manager (ACM).
- Chung chi bat buoc tao o region us-east-1.
- Quy tac nay van dung ngay ca khi User Pool nam o region khac (vi du eu-west-1).
- Cau hinh custom domain nam trong phan App integration cua User Pools.

## 4. Adaptive Authentication
Adaptive authentication bao ve dang nhap dua tren muc do rui ro.

### Cach hoat dong
- Moi lan dang nhap duoc Cognito danh gia va gan muc rui ro (low, medium, high).
- Dua vao muc rui ro, Cognito co the:
  - Cho phep dang nhap binh thuong.
  - Yeu cau MFA.
  - Chan lan dang nhap dang nghi.

### Yeu to danh gia rui ro
- Thiet bi co quen thuoc hay khong.
- Vi tri dang nhap.
- Mau dia chi IP.
- Cac tin hieu hanh vi/ngu canh khac.

### Ho tro bao mat
- Bao ve truong hop tai khoan bi chiem doat (account takeover protection).
- Xac minh bo sung qua phone/email khi can.
- Toan bo su kien co the xem trong CloudWatch logs (lan thu dang nhap, risk score, ket qua challenge).

## 5. JWT Token tu Cognito
Sau khi dang nhap thanh cong, Cognito cap JWT (JSON Web Token).

### Cau truc JWT
- Header.
- Payload.
- Signature.

### Nguyen tac quan trong
Luon xac minh signature truoc khi tin du lieu trong payload.

### Cac claim pho bien trong payload
- sub: dinh danh duy nhat cua nguoi dung trong Cognito User Pool.
- username.
- cognito groups (neu co).
- exp (thoi gian het han token).

Co the dung sub de truy van them thuoc tinh nguoi dung trong Cognito (email, given name, phone, custom attributes).

## 6. Ghi nho cho hoc tap va on thi
- Nam ro trigger Lambda tuong ung tung giai doan xac thuc.
- Nho quy tac region chung chi custom domain: us-east-1.
- Hieu khi nao adaptive authentication bat buoc MFA.
- Giai thich duoc vi sao phai verify signature truoc khi dung payload JWT.
- Dung claim sub lam dinh danh on dinh khi tich hop he thong phia sau.
