# Ghi Chu Hoc AWS IAM Nang Cao

## 1) Mo Hinh Uy Quyen IAM (Ban Rut Gon)

Thu tu danh gia policy:
1. Bat dau voi **Deny** (mac dinh).
2. Kiem tra **explicit Deny**.
3. Neu khong co explicit deny, kiem tra **Allow**.
4. Neu khong co allow, ket qua cuoi cung la **Deny**.

Quy tac quan trong:
- **Explicit Deny luon uu tien hon Allow**.

### Vi du luong xu ly (Create DynamoDB table)
- User gui yeu cau: `dynamodb:CreateTable`
- IAM danh gia tat ca policy ap dung.
- Neu co bat ky statement explicit deny hanh dong nay -> **Denied**.
- Neu khong deny va co it nhat mot allow -> **Allowed**.
- Nguoc lai -> **Denied**.

## 2) Tuong Tac IAM Policy va S3 Bucket Policy

Voi quyen truy cap S3, AWS danh gia **hop (union)** cua:
- Identity-based policy (IAM user/role/group)
- Resource-based policy (S3 bucket policy)

Sau do ap dung quy tac danh gia thong thuong (explicit deny thang).

### 4 tinh huong can nho

1. IAM cho read/write, bucket policy khong deny
- Ket qua: **Allowed**

2. IAM cho read/write, bucket policy co explicit deny
- Ket qua: **Denied** (explicit deny thang)

3. IAM khong khai bao quyen S3, bucket policy explicit allow role
- Ket qua: **Allowed** (resource policy co the cap quyen)

4. IAM explicit deny, bucket policy allow
- Ket qua: **Denied** (explicit deny thang)

## 3) Dynamic IAM Policies

Muc tieu: tranh tao moi user mot policy rieng cho home folder.

### Cach khong mo rong duoc
- `Georges` -> allow `/home/georges`
- `Sarah` -> allow `/home/sarah`
- `Matt` -> allow `/home/matt`

### Cach mo rong tot
Su dung policy variable:
- `${aws:username}`

Vi du resource pattern:
- `/home/${aws:username}`

Luc runtime, AWS tu dong thay `${aws:username}` bang ten IAM user hien tai.

Loi ich:
- Mot policy dung lai cho tat ca user.
- Van dam bao moi user chi vao dung thu muc cua minh.

## 4) Cac Loai Policy Trong AWS IAM

### AWS Managed Policies
- Do AWS tao va bao tri.
- Hop voi cac vai tro pho bien (admin, power user, job function).
- Tu dong cap nhat khi AWS them service/API moi.
- It linh hoat hon ve muc do chi tiet.

### Customer Managed Policies
- Do to chuc cua ban tao va quan ly.
- Tai su dung cho nhieu principal.
- Ho tro versioning va rollback.
- Tot hon cho kiem soat chi tiet va audit.
- Thuong duoc xem la best practice trong moi truong production.

### Inline Policies
- Gan truc tiep vao mot IAM principal (1-1).
- Khong tai su dung.
- Yeu hon ve version control so voi managed policy.
- Xoa principal thi inline policy cung bi xoa.
- Co gioi han ve kich thuoc va kho bao tri.

## 5) Ghi Chu Thuc Te Tren Console

- Trong IAM > Policies:
  - Co the loc AWS managed va customer managed.
  - Customer managed hien version va usage, de audit hon.
- Inline policy duoc tao trong trang user/role/group cu the, khong trung tam hoa nhu managed policy.

## 6) Trong Tam Cho Thi Va Van Hanh

Can thuoc long cac diem sau:
- Mac dinh la **Deny**.
- **Explicit Deny > Allow** trong moi truong hop.
- Voi S3, phai danh gia IAM + bucket policy **cung nhau**.
- Dynamic variable nhu `${aws:username}` giup mo rong tot.
- Uu tien customer managed policy cho thiet ke quyen truy cap tai su dung, co kiem soat.

## 7) Tu Kiem Tra Nhanh

1. IAM allow, bucket policy explicit deny -> ket qua gi?
2. Bucket policy co the cap quyen neu IAM policy khong nhac S3 khong?
3. Vi sao `${aws:username}` huu ich cho phan quyen home folder?
4. Loai policy nao phu hop nhat cho mo hinh enterprise can tai su dung va versioning?

### Dap an
1. Denied.
2. Co, neu khong bi explicit deny chan lai.
3. Cho phep dung mot policy mau cho moi user duoc map dong theo ten dang nhap.
4. Customer managed policy.
