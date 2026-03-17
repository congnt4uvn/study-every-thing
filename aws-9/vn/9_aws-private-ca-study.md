# Ghi Chu Hoc AWS: Chung Chi Rieng Tu ACM va AWS Private CA

## 1. Y Tuong Chinh
AWS Certificate Manager (ACM) co the cap:
- Chung chi cong khai (public certificates)
- Chung chi rieng tu (private certificates)

De cap chung chi rieng tu, ban phai dung **AWS Private Certificate Authority (AWS Private CA)**.

## 2. AWS Private CA La Gi?
AWS Private CA la dich vu duoc quan ly boi AWS, giup ban xay dung PKI (Public Key Infrastructure) rieng ben trong to chuc.

Ban co the tao:
- Root CA
- Subordinate CA (CA cap duoi, phu thuoc vao root CA)

## 3. Chung Chi X.509 End-Entity
Tu private CA, ban co the cap chung chi X.509 cho ung dung, nguoi dung va thiet bi.

Luu y quan trong:
- Chung chi end-entity dung cho ma hoa va xac thuc danh tinh.
- Chung chi nay **khong** duoc dung de tao/cap chung chi moi.

## 4. Mo Hinh Tin Cay
Chung chi rieng tu chi duoc tin cay boi cac he thong tin cay private CA cua ban.

Thuong la:
- Ung dung noi bo
- Nguoi dung/thiet bi/dich vu noi bo trong to chuc

Cac chung chi nay **khong** phu hop de su dung nhu chung chi tin cay tren internet cong cong.

## 5. Tich Hop Voi Dich Vu AWS
Neu mot dich vu AWS tich hop voi ACM, ban co the gan chung chi rieng tu vao dich vu do.

Vi du da duoc de cap:
- CloudFront
- API Gateway
- Load Balancer
- Cac dich vu lien quan Kubernetes

## 6. Doi Tuong Duoc Cap Chung Chi
Co the cap chung chi private cho:
- Nguoi dung
- May tinh
- API / HTTP endpoints
- Thiet bi IoT

## 7. Tinh Huong Su Dung Chinh
- Ma hoa TLS cho giao tiep noi bo
- Ky ma (code signing) va xac thuc
- Xac thuc nguoi dung, may tinh, API, thiet bi IoT
- Xay dung ha tang PKI rieng cho doanh nghiep

## 8. On Tap Nhanh (Thi/Phong Van)
- ACM ho tro ca chung chi public va private.
- Muon cap private cert phai dung AWS Private CA.
- Root CA co the ky cho subordinate CA.
- End-entity cert khong ky duoc cert khac.
- Private cert chu yeu dung cho tin cay noi bo.

## 9. Meo Ghi Nho
- "Public cert = tin cay internet"
- "Private cert = tin cay trong to chuc"
- "Private CA = nha may cap chung chi noi bo"
