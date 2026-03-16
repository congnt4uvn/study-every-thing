# Ghi Chu On Tap AWS KMS

## 1. AWS KMS la gi?
- AWS KMS (Key Management Service) la dich vu tao va quan ly khoa ma hoa.
- KMS duoc tich hop sau rong voi nhieu dich vu AWS.
- Rat nhieu tinh nang ma hoa trong AWS thuc te su dung KMS o phia sau.

## 2. Tai sao nen dung KMS?
- AWS quan ly ha tang khoa, giam cong van hanh.
- Tich hop IAM de kiem soat truy cap.
- Moi API call su dung khoa co the audit bang CloudTrail.
- De dang bat ma hoa du lieu at rest cho EBS, S3, RDS, SSM, va nhieu dich vu khac.

## 3. Su dung KMS cho secrets
- Khong luu secret dang plain text, dac biet trong source code.
- Dung KMS API (CLI hoac SDK) de ma hoa du lieu nhay cam.
- Chi luu du lieu da ma hoa (vi du trong code hoac bien moi truong).

## 4. Cac loai khoa KMS

### Khoa doi xung (symmetric)
- Mot khoa dung cho ca ma hoa va giai ma.
- Pho bien trong tich hop giua AWS services va KMS.
- Ban khong truy cap truc tiep key material, chi goi API KMS de su dung.

### Khoa bat doi xung (asymmetric)
- Public key dung de ma hoa (hoac verify), private key dung de giai ma (hoac sign).
- Co the tai public key ve.
- Private key luon nam trong KMS, chi duoc dung qua API.
- Phu hop khi nguoi dung ben ngoai AWS can ma hoa du lieu bang public key.

## 5. Mo hinh so huu va quan ly khoa

### AWS owned keys
- Mien phi.
- Do AWS service quan ly hoan toan.
- Thuong khong thay truc tiep trong tai khoan cua ban.

### AWS managed keys
- Mien phi.
- Co dang ten `aws/<service>` (vi du `aws/rds`, `aws/ebs`, `aws/dynamodb`).
- Chi dung voi dich vu gan voi key do.

### Customer managed keys (CMK)
- Ban tu tao, tu quan ly.
- Chi phi: khoang $1/thang moi key (chua tinh API requests).
- Co the import key material (van tinh phi tuong tu).
- Huu ich khi can quyen chi tiet, audit chat, hoac cross-account.

## 6. Tong quan chi phi
- Phi key: khoang $1/thang cho moi customer managed key.
- Phi API: khoang $0.03 cho 10,000 requests.

## 7. Xoay vong khoa (rotation)
- AWS managed keys: tu dong xoay 1 nam/lan.
- Customer managed keys: bat duoc auto rotation theo chu ky va co ho tro on-demand rotation.
- Imported keys: chi xoay thu cong (thuong ket hop alias de doi khoa).

## 8. Pham vi theo region
- KMS key la tai nguyen theo tung region.
- Mot key khong the dung chung truc tiep giua nhieu region.
- Luong chuyen EBS ma hoa sang region khac:
  1. Tao snapshot tu volume da ma hoa.
  2. Copy snapshot sang region dich.
  3. Ma hoa lai bang KMS key o region dich.
  4. Restore volume tu snapshot da copy.

## 9. KMS key policy
- Key policy quyet dinh ai duoc dung/admin KMS key.
- Neu policy khong cho phep, truy cap se that bai.

### Default key policy
- Thuong cho phep su dung trong account (ket hop IAM permissions).

### Custom key policy
- Chi dinh cu the user/role duoc phep su dung va quan tri key.
- Can thiet cho yeu cau quyen chi tiet va cross-account.

## 10. Quy trinh cross-account voi encrypted snapshot
1. Tao snapshot ma hoa bang customer managed key o source account.
2. Them key policy cho phep target account.
3. Share encrypted snapshot sang target account.
4. O target account, copy snapshot va ma hoa lai bang CMK cua target.
5. Tao EBS volume tu snapshot da copy.

## 11. Meo hoc va on thi
- Ghi nho bo 4: KMS + IAM + Key Policy + CloudTrail.
- Phan biet ro AWS owned, AWS managed, customer managed keys.
- Biet khi nao can asymmetric keys.
- Nho gioi han theo region va hanh vi re-encrypt khi copy.
- Luyen tap luong cross-account cho du lieu ma hoa.
