# Ghi Chu Hoc AWS Macie

## AWS Macie la gi?
AWS Macie la dich vu bao mat va quyen rieng tu du lieu duoc quan ly hoan toan.
Dich vu nay su dung machine learning va pattern matching de phat hien va bao ve du lieu nhay cam trong AWS.

## Muc dich chinh
Macie giup nhan dien du lieu nhay cam, dac biet la:
- PII (Thong tin dinh danh ca nhan)

## Cach hoat dong (luong co ban)
1. Du lieu cua ban duoc luu trong cac bucket Amazon S3.
2. AWS Macie quet va phan loai du lieu.
3. Macie phat hien noi dung nhay cam nhu PII.
4. Ket qua phat hien duoc gui qua Amazon EventBridge.
5. Ban co the tich hop hanh dong voi cac dich vu nhu:
- Amazon SNS
- AWS Lambda

## Diem hoc/thi quan trong
- Macie tap trung vao phat hien du lieu nhay cam trong S3.
- Day la dich vu managed (khong can quan ly ha tang).
- Ho tro phat hien tu dong bang ML va pattern matching.
- EventBridge co the dinh tuyen ket qua de canh bao va tu dong hoa.

## Tom tat nhanh
Dung AWS Macie khi ban muon phat hien va giam sat du lieu nhay cam (nhu PII) trong Amazon S3, dong thoi kich hoat canh bao hoac tu dong hoa dua tren ket qua phat hien.
