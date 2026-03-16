# Ghi Chu Hoc AWS: KMS Key Policies

## 1) KMS Key Policy la gi?
KMS key policy la resource policy gan truc tiep vao KMS key. Policy nay dinh nghia ai duoc phep quan ly va su dung key.

## 2) Hanh vi mac dinh cua key policy
Khi tao key bang AWS Console, default key policy thuong cho phep cac principal trong cung AWS account su dung key **neu** ho cung co IAM permission phu hop.

Diem quan trong:
- Trong mo hinh nay, ca key policy va IAM permission deu quan trong.

## 3) Cap quyen truc tiep trong key policy
Ban co the cho phep truc tiep mot principal cu the trong key policy, vi du:
- IAM user
- IAM role
- Federated user/session
- AWS service principal

Ban co the gioi han action duoc phep, vi du:
- `kms:Encrypt`
- `kms:Decrypt`
- va cac KMS action khac

Neu principal da duoc allow truc tiep trong key policy, principal do co the su dung key theo statement da cap (theo tinh huong mo ta trong noi dung goc).

## 4) Cac loai principal thuong gap
Cac mau principal pho bien (cho KMS va IAM noi chung):

1. Account root principal
- Dinh dang vi du: `arn:aws:iam::<account-id>:root`
- Y nghia: cho phep uy quyen cho principal trong account do, sau do IAM policy se ap dung.

2. IAM role cu the
- Dat role ARN vao `Principal`.

3. IAM role session / assumed role
- Session identity tao tu `AssumeRole`.
- Thuong gap trong cac luong federation.

4. IAM user
- Dat user ARN vao `Principal`.

5. Federated user/session
- Nguon vi du: Cognito Identity, SAML federation, v.v.

6. AWS service principal
- Vi du: cho phep mot AWS service su dung KMS key khi can.

7. Wildcard principal
- `"*"` (hoac cac mau rong)
- Rat rui ro; tranh dung neu khong that su can thiet, va phai rang buoc bang condition chat che.

## 5) Best practices bao mat
- Ap dung least privilege: chi cap dung action can thiet.
- Uu tien principal cu the, han che wildcard.
- Them condition khi co the (context, source account, encryption context, v.v.).
- Theo doi CloudTrail de audit KMS usage.
- Dinh ky ra soat key policy de tranh cap quyen qua rong.

## 6) Cau hoi tu kiem tra
1. Vai tro cua key policy va IAM policy trong KMS authorization khac nhau nhu the nao?
2. Khi nao nen cap quyen truc tiep trong key policy?
3. Vi sao `"*"` trong `Principal` nguy hiem?
4. Neu truy cap qua SAML, nen dung principal type nao?
5. Workload chi can ma hoa thi can action nao?

## 7) Tom tat 1 dong
KMS key policy xac dinh **ai** duoc su dung key; IAM thuong xac dinh **identity nao trong account** duoc phep theo identity policy, va thiet ke an toan can quyen toi thieu, ro rang, de kiem toan.
