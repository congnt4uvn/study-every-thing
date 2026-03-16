# Ghi Chu Hoc AWS: Dynamic References Trong CloudFormation

## Tong Quan
Dynamic references cho phep AWS CloudFormation lay gia tri ben ngoai trong qua trinh tao, cap nhat hoac xoa stack.

Nhung gia tri nay thuong den tu:
- AWS Systems Manager Parameter Store
- AWS Secrets Manager

Cach nay rat huu ich khi ban khong muon hardcode mat khau, ten dang nhap hoac gia tri cau hinh truc tiep trong template CloudFormation.

## Cac Loai Dynamic Reference Duoc Ho Tro
CloudFormation ho tro 3 loai dynamic reference chinh:

1. `ssm`
   - Dung cho gia tri van ban thuong duoc luu trong Systems Manager Parameter Store.
2. `ssm-secure`
   - Dung cho gia tri Secure String da duoc ma hoa trong Systems Manager Parameter Store.
3. `secretsmanager`
   - Dung cho secret duoc luu trong AWS Secrets Manager.

## Cu Phap Tong Quat
Dinh dang chung la:

```text
{{resolve:service-name:reference-key}}
```

Vi du:

```text
{{resolve:ssm:parameter-name:version}}
{{resolve:ssm-secure:parameter-name:version}}
{{resolve:secretsmanager:secret-id:SecretString:json-key}}
```

## Vi Du 1: Su Dung Gia Tri Plain Text Tu Parameter Store
Vi du nay resolve mot tham so SSM va dung no trong thuoc tinh cua S3 bucket.

```yaml
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      AccessControl: '{{resolve:ssm:my-s3-access-control:1}}'
```

Dung cach nay khi gia tri khong nhay cam.

## Vi Du 2: Su Dung Secure String Tu Parameter Store
Vi du nay lay mot gia tri da ma hoa tu Parameter Store.

```yaml
Resources:
  MyUser:
    Type: AWS::IAM::User
    Properties:
      LoginProfile:
        Password: '{{resolve:ssm-secure:iam-user-password:1}}'
```

Hay dung `ssm-secure` khi tham so duoc luu duoi dang secure string.

## Vi Du 3: Su Dung Secrets Manager Cho Thong Tin Dang Nhap RDS
Vi du nay cho thay RDS database co the doc thong tin dang nhap tu Secrets Manager.

```yaml
Resources:
  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: mysql
      MasterUsername: '{{resolve:secretsmanager:my-db-secret:SecretString:username}}'
      MasterUserPassword: '{{resolve:secretsmanager:my-db-secret:SecretString:password}}'
```

Day la cach lam pho bien cho thong tin dang nhap database.

## Cac Mo Hinh CloudFormation + RDS + Secrets Manager
Co 2 mo hinh quan trong can nho.

### Mo Hinh 1: RDS Tu Dong Tao Secret
Neu ban cau hinh RDS cluster voi:

```yaml
ManageMasterUserPassword: true
```

RDS se tu dong tao va quan ly master user secret trong Secrets Manager.

De output ARN cua secret, dung `GetAtt`:

```yaml
Outputs:
  MasterUserSecretArn:
    Value: !GetAtt MyDBCluster.MasterUserSecret.SecretArn
```

Trong mo hinh nay:
- CloudFormation tao tai nguyen RDS.
- RDS tao va quan ly secret.
- Secrets Manager luu mat khau va co the xoay vong secret.

### Mo Hinh 2: CloudFormation Tao Secret
Trong mo hinh nay, CloudFormation tao secret truoc, thuong kem mat khau duoc sinh tu dong, sau do database dung dynamic reference de doc no.

Luong xu ly thuong la:
- Tao secret trong Secrets Manager.
- Tu dong sinh mat khau.
- Tham chieu secret trong tai nguyen RDS.
- Gan secret vao RDS database de ho tro rotation.

Vi du cau truc:

```yaml
Resources:
  MySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      GenerateSecretString:
        SecretStringTemplate: '{"username":"admin"}'
        GenerateStringKey: password

  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: mysql
      MasterUsername: '{{resolve:secretsmanager:MySecret:SecretString:username}}'
      MasterUserPassword: '{{resolve:secretsmanager:MySecret:SecretString:password}}'

  SecretAttachment:
    Type: AWS::SecretsManager::SecretTargetAttachment
    Properties:
      SecretId: !Ref MySecret
      TargetId: !Ref MyDatabase
      TargetType: AWS::RDS::DBInstance
```

Trong mo hinh nay:
- CloudFormation tao secret.
- Database doc thong tin dang nhap thong qua dynamic references.
- Secret co the duoc gan de ho tro rotation.

## Tai Sao Dynamic References Quan Trong
Dynamic references quan trong vi chung:
- Tranh hardcode gia tri nhay cam trong template.
- Cai thien bao mat va kha nang bao tri.
- Ho tro quy trinh xoay vong secret.
- Giup template CloudFormation gon gang va an toan hon.

## On Tap Nhanh
Hay nho cac diem sau:
- `ssm` dung cho parameter plain text.
- `ssm-secure` dung cho parameter da ma hoa trong Parameter Store.
- `secretsmanager` dung cho secret luu trong Secrets Manager.
- Dynamic references duoc resolve trong luc stack operation dien ra.
- RDS co the tu tao secret hoac dung secret do CloudFormation tao.

## Cau Hoi Tu Luyen
1. Khi nao nen dung `ssm` thay vi `ssm-secure`?
2. Vi sao Secrets Manager phu hop hon cho mat khau database?
3. `ManageMasterUserPassword: true` trong RDS co y nghia gi?
4. Tai sao can dung `SecretTargetAttachment`?
5. CloudFormation resolve dynamic references vao thoi diem nao?
