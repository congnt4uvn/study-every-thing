# Ghi Chu Hoc AWS Parameter Store

## 1) Parameter Store la gi?
AWS Systems Manager Parameter Store la dich vu luu tru gia tri cau hinh va thong tin nhay cam.

Ban co the luu:
- Gia tri cau hinh thong thuong (vi du: URL database)
- Gia tri nhay cam (vi du: mat khau) duoc ma hoa bang AWS KMS

## 2) Mo trong AWS Console
1. Tim Parameter Store trong thanh tim kiem cua AWS Console.
2. Mo theo duong dan Systems Manager > Application Tools > Parameter Store.

## 3) Dat ten va cau truc hierarchy
Mau dat ten trong bai hoc:
- `/my-app/dev/db-url`
- `/my-app/dev/db-password`
- `/my-app/prod/db-url`
- `/my-app/prod/db-password`

Cau truc path giup to chuc tham so theo:
- Ung dung (`my-app`)
- Moi truong (`dev`, `prod`)
- Ten cau hinh (`db-url`, `db-password`)

## 4) Cac tier
### Standard
- Toi da 10,000 tham so
- Kich thuoc gia tri toi da: 4 KB
- Khong chia se tham so voi tai khoan khac

### Advanced
- Toi da 100,000 tham so
- Kich thuoc gia tri toi da: 8 KB
- Co the chia se tham so voi tai khoan khac

## 5) Kieu tham so
- `String`: chuoi van ban thuong
- `StringList`: danh sach chuoi
- `SecureString`: chuoi duoc ma hoa bang KMS

## 6) SecureString va KMS
Voi du lieu nhay cam (nhu mat khau), nen dung `SecureString`.
Ban co the ma hoa bang:
- KMS key do AWS quan ly: `alias/aws/ssm`
- KMS key do ban tu tao (vi du: `Tutorial`)

De xem gia tri da giai ma, nguoi dung phai co quyen KMS decrypt.

## 7) Lenh CLI trong bai hoc

### Lay mot so tham so cu the
```bash
aws ssm get-parameters \
  --names "/my-app/dev/db-url" "/my-app/dev/db-password"
```

### Giai ma SecureString
```bash
aws ssm get-parameters \
  --names "/my-app/dev/db-url" "/my-app/dev/db-password" \
  --with-decryption
```

### Lay tham so theo path
```bash
aws ssm get-parameters-by-path --path "/my-app/dev"
```

### Lay tat ca tham so de quy trong namespace
```bash
aws ssm get-parameters-by-path \
  --path "/my-app" \
  --recursive
```

### De quy + giai ma
```bash
aws ssm get-parameters-by-path \
  --path "/my-app" \
  --recursive \
  --with-decryption
```

## 8) Tong ket quan trong
- Dung hierarchy path de to chuc tham so ro rang.
- Dung `SecureString` cho secrets.
- Ket hop KMS key va IAM permission de bao mat.
- CLI rat huu ich de tu dong hoa script.

## 9) Checklist tu luyen
- Tao 4 tham so (`dev` + `prod`, URL + password).
- Dat tham so mat khau thanh `SecureString`.
- Thu `get-parameters`.
- Thu them `--with-decryption`.
- Thu `get-parameters-by-path --recursive`.
