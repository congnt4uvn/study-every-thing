# Ghi Chu Hoc AWS Secrets Manager

## Tong Quan

AWS Secrets Manager la dich vu duoc quan ly boi AWS de luu tru, truy xuat, xoay vong va quan ly cac thong tin bi mat mot cach an toan. Dich vu nay thuong duoc dung cho thong tin dang nhap co so du lieu, API key va cac cau hinh nhay cam ma ung dung can tai thoi diem chay.

## Muc Dich Chinh

- Luu tru secret an toan thay vi hardcode trong ung dung.
- Truy xuat secret thong qua API khi ung dung can dung.
- Quan ly vong doi cua secret tu luc tao den luc xoa.
- Tu dong xoay vong credentials de tang bao mat.

## Khac Gi So Voi Parameter Store

So voi Systems Manager Parameter Store dung `SecureString`, Secrets Manager tap trung nhieu hon vao viec quan ly toan bo vong doi cua secret.

Khac biet quan trong:

- Secrets Manager ho tro tu dong rotation.
- Rotation co the ket noi voi AWS Lambda.
- Dich vu tich hop tot voi cac he co so du lieu nhu Amazon RDS, PostgreSQL, Redshift va DocumentDB.

Tom lai, ca hai dich vu deu co the luu gia tri da ma hoa, nhung Secrets Manager duoc thiet ke de viec rotation de dang va an toan hon.

## Co The Luu Tru Gi

Secrets Manager ho tro nhieu loai secret, bao gom:

- Thong tin dang nhap co so du lieu
- API key
- Secret tuy chinh theo cap key-value
- Secret dang JSON plaintext

Voi database secret, ban thuong luu:

- Username
- Password

Voi custom secret, ban co the luu mot hoac nhieu cap key-value, vi du:

```json
{
  "apiKey": "gia-tri-bi-mat",
  "secretKey": "gia-tri-bi-mat-thu-hai"
}
```

Day la diem khac biet thuc te so voi cach luu tham so don gian, vi mot secret co the chua nhieu gia tri lien quan.

## Ma Hoa

Khi tao secret, ban chon khoa ma hoa:

- Dung khoa mac dinh do AWS quan ly
- Dung khoa KMS do khach hang tu quan ly

Lua chon nay quyet dinh cach secret duoc ma hoa khi luu tru.

## Cach Tao Secret

Quy trinh thong thuong:

1. Chon loai secret.
2. Nhap gia tri thu cong hoac dan JSON.
3. Chon khoa ma hoa.
4. Dat ten cho secret.
5. Co the them mo ta va tags.
6. Cau hinh rotation neu can.

Vi du ten secret:

- `prod/my-secret-api`

## Tu Dong Rotation

Mot trong nhung tinh nang quan trong nhat cua Secrets Manager la tu dong rotation.

Cach hoat dong:

- Ban dinh nghia chu ky rotation, vi du moi 60 ngay.
- Secrets Manager se kich hoat mot ham Lambda.
- Ham Lambda do se thuc hien logic rotation.
- Ham nay phai co quyen IAM phu hop.

Ham Lambda co the:

- Tao password moi
- Cap nhat credentials tren dich vu ben thu ba
- Lam moi hoac thay API key

Theo noi dung trong file nguon, chu ky toi da co the dat:

- Toi da 1 nam

## Tich Hop Voi Co So Du Lieu

Secrets Manager co the tich hop truc tiep voi cac co so du lieu duoc ho tro.

Khi dung tich hop nay:

- Secret luu username va password.
- Secrets Manager co the dong thoi cap nhat thong tin dang nhap tren database da lien ket.
- Rotation co the duoc bat de secret va credentials tren database luon dong bo.

Dieu nay manh hon viec chi luu secret don thuan.

## Kiem Soat Truy Cap

Quyen truy cap secret duoc quan ly boi IAM.

Dieu do co nghia la ban co the quy dinh:

- Nguoi dung nao duoc doc secret
- Role nao duoc phep rotation
- Ung dung nao duoc phep truy xuat secret

## Gia Duoc De Cap Trong Noi Dung Nguon

Ban ghi am nhac den:

- `$0.40` cho moi secret moi thang
- `$0.05` cho moi 10,000 API calls
- Mien phi 30 ngay cho secret storage

Gia co the thay doi, vi vay nen kiem tra lai tren trang pricing chinh thuc cua AWS.

## Truy Xuat Secret Bang Code

Noi dung file goc giai thich rang viec lay secret kha don gian thong qua AWS SDK:

- Tao Secrets Manager client
- Goi `GetSecretValue`
- Truyen ten secret hoac secret identifier
- Doc gia tri secret string tra ve

Trong Python, cach dung thuong la:

- Tao client
- Goi `get_secret_value`
- Doc truong `SecretString`
- Parse JSON neu can

## Hanh Vi Khi Xoa Secret

Khi xoa secret, ban co the cau hinh thoi gian cho truoc khi xoa vinh vien. Dieu nay giup tranh xoa nham.

## Y Chinh Can Nho

- Secrets Manager duoc dung cho cac gia tri nhay cam nhu credentials va API keys.
- Loi the lon nhat la tu dong rotation.
- Rotation thuong duoc thuc hien bang Lambda.
- Dich vu tich hop tot voi database tren AWS.
- IAM kiem soat truy cap.
- KMS xu ly ma hoa.

## Cau Hoi On Tap Nhanh

1. Loi the chinh cua Secrets Manager so voi Parameter Store la gi?
2. Vi sao Lambda quan trong trong rotation?
3. Mot secret co the luu nhung loai gia tri nao?
4. IAM giup bao ve Secrets Manager nhu the nao?
5. Tai sao tich hop voi database lai huu ich?

## Tom Tat Ngan

AWS Secrets Manager la dich vu an toan de luu tru va quan ly secret. Tinh nang noi bat nhat la tu dong rotation, thuong ket hop voi Lambda, va dich vu nay tich hop manh voi cac database tren AWS. Day la lua chon phu hop khi ung dung can credentials duoc quan ly tap trung, bao mat va xoay vong dinh ky.