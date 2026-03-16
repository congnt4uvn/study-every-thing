# Bao Mat AWS CodeBuild - Tai Lieu Hoc

## 1. CodeBuild va VPC
- Mac dinh, AWS CodeBuild chay ben ngoai VPC cua ban.
- Ban co the cau hinh CodeBuild chay ben trong VPC de truy cap tai nguyen private.
- Vi du pho bien: truy cap RDS private, ElastiCache, hoac internal service.

## 2. Quan Ly Secret Trong CodeBuild
Khong luu thong tin nhay cam duoi dang plaintext trong environment variables cua CodeBuild.

### Cach lam khong an toan
- `DB_PASSWORD = supersecret` (plaintext)
- Rui ro: secret co the bi lo trong logs, trang cau hinh, hoac qua thao tac nham.

### Cach khuyen nghi
Su dung environment variables tham chieu den:
- AWS Systems Manager Parameter Store
- AWS Secrets Manager

Khi build runtime, CodeBuild se lay gia tri secret that va inject vao container.

## 3. Su Dung SSM Parameter Store (Vi Du)
Quy trinh:
1. Tao parameter trong Parameter Store.
2. Vi du ten: `/CodeBuild/DBPassword`
3. Kieu parameter: `SecureString`
4. Ma hoa bang KMS key (CMK).
5. Luu gia tri (vi du: `SuperSecret`).
6. Trong environment variables cua CodeBuild:
   - Name: `DB_PASSWORD`
   - Type: `Parameter Store`
   - Value: `/CodeBuild/DBPassword`

Ket qua: CodeBuild resolve `/CodeBuild/DBPassword` o runtime va inject gia tri da giai ma.

## 4. Su Dung AWS Secrets Manager (Lua Chon Khac)
- Ban co the lam tuong tu voi Secrets Manager.
- Trong env vars cua CodeBuild, chon loai tham chieu secret va nhap ten secret.

## 5. Quyen IAM Can Thiet
IAM role gan voi CodeBuild project can co quyen truy cap:
- SSM Parameter Store (vi du: `ssm:GetParameters`)
- Secrets Manager (vi du: `secretsmanager:GetSecretValue`)
- Quyen KMS decrypt neu dung customer-managed key

Neu thieu quyen, build se loi khi lay secret.

## 6. Meo On Thi
- Nho rang: plaintext env vars khong an toan cho secrets.
- Uu tien tham chieu qua Parameter Store hoac Secrets Manager.
- Neu can truy cap tai nguyen private, cau hinh CodeBuild trong VPC (subnet + security group).
- Luon kiem tra IAM permissions de lay secret.

## Checklist Nhanh
- CodeBuild dang chay dung network chua (default hay VPC)?
- Secrets da duoc dua ra ngoai plaintext env vars chua?
- Tham chieu secret da cau hinh dung chua?
- IAM role cua CodeBuild da co quyen SSM/Secrets Manager/KMS chua?
