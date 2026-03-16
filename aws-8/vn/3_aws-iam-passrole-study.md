# Ghi Chu Hoc AWS: IAM PassRole va Trust Relationship

## Muc tieu hoc
Hieu cach `iam:PassRole` va trust policy phoi hop voi nhau khi dich vu AWS (EC2, Lambda, CodePipeline, ECS task, ...) can assume IAM role.

## Y tuong cot loi
Khi ban gan IAM role cho mot dich vu AWS, thuc chat la ban dang **pass** role do cho dich vu.

De viec nay an toan, AWS yeu cau du 2 dieu kien:

1. Nguoi goi phai co quyen pass role (`iam:PassRole`).
2. Trust policy cua role phai cho phep dich vu dich assume role do.

Can du ca hai dieu kien.

## Vi du thuc te pho bien
- EC2 instance profile role duoc pass cho EC2 instance.
- Lambda execution role duoc pass cho Lambda function.
- CodePipeline service role duoc pass cho CodePipeline.
- ECS task role duoc pass cho ECS task.

## Quyen IAM can co
Thong thuong user hoac automation principal can:
- `iam:PassRole` de pass mot role cu the.
- `iam:GetRole` (thuong di kem) de xem thong tin role.

## Vi du policy (Ai duoc pass role nao)
Vi du duoi day cho phep principal dung EC2 action va chi pass dung 1 role ten `S3Access`.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole",
        "iam:GetRole"
      ],
      "Resource": "arn:aws:iam::123456789012:role/S3Access"
    }
  ]
}
```

## Trust Policy (Dich vu nao duoc assume role)
Ngay ca khi ai do pass duoc role, role chi co the duoc assume boi cac dich vu nam trong trust policy cua role.

Vi du: chi trust EC2 service.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Neu la Lambda thi service principal se la `lambda.amazonaws.com`.

## Luu y bao mat quan trong
- Gioi han `iam:PassRole` theo role ARN cu the, khong de `*`.
- Tach role theo tung workload (EC2 role, Lambda role, pipeline role).
- Ap dung least privilege cho ca permission policy va trust policy.
- Kiem tra va audit ai co quyen pass role co dac quyen cao.

## Mo hinh ghi nho nhanh
Hay xem viec dung role nhu he thong 2 khoa:
- Khoa 1: "Nguoi goi co pass duoc role nay khong?" -> `iam:PassRole`
- Khoa 2: "Dich vu nay co duoc assume role nay khong?" -> trust policy

Mot trong 2 khoa that bai thi thao tac role se that bai.

## Checklist nhanh
Truoc khi gan role cho dich vu, hay kiem tra:
- Nguoi goi co `iam:PassRole` tren dung role do.
- Trust policy cua role co dung service principal can thiet.
- Permission policy cua role chi cap quyen can thiet.

## Cau hoi tu kiem tra
1. Tai sao chi co `iam:PassRole` la chua du?
2. Neu trust policy chi cho EC2 ma ban pass role cho Lambda thi sao?
3. Vi sao wildcard `iam:PassRole` nguy hiem?
4. Policy nao quyet dinh dich vu nao duoc assume role: permission policy hay trust policy?

## Tra loi ngan
1. Vi trust policy cung phai cho phep dich vu dich assume role.
2. Lambda khong assume duoc, thao tac se loi.
3. Co the cho phep gan role manh qua rong, dan den privilege escalation.
4. Trust policy.
