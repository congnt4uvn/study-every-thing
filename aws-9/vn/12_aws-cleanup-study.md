# Tai lieu hoc AWS: Checklist don dep sau khi thuc hanh

## Vi sao can don dep tai nguyen
Sau khi hoan thanh cac bai lab AWS, ban nen xoa tai nguyen khong con dung de:
- Tranh phat sinh chi phi bat ngo.
- Giu tai khoan gon gang, de quan ly.
- Hinh thanh thoi quen van hanh cloud tot.

Hay kiem tra tat ca region ban da su dung trong qua trinh hoc (vi du: Paris `eu-west-3`, N. Virginia `us-east-1`).

## Thu tu don dep de nghi
1. Xac dinh cac region da su dung.
2. Xoa nhom dich vu tinh toan va du lieu ton chi phi cao truoc.
3. Xoa tai nguyen mang va tich hop.
4. Xoa phan giam sat va CI/CD con sot.
5. Xoa IAM cuoi cung (vi nhieu dich vu phu thuoc IAM role/policy).

## Checklist theo tung dich vu

### 1. EC2 va dich vu lien quan
- Terminate EC2 instances.
- Xoa Auto Scaling groups.
- Xoa Load Balancers va target groups.
- Xoa EBS volumes/snapshots khong dung (neu co).

### 2. Lambda
- Xoa Lambda functions khong can thiet.
- (Lambda co the khong ton nhieu tien khi khong chay, nhung van nen don dep.)

### 3. Elastic Beanstalk
- Xoa environments.
- Xoa applications.

### 4. S3
- Kiem tra tat ca buckets.
- Xoa file lon hoac khong can thiet.
- Xoa buckets trong khong con su dung.

### 5. Co so du lieu
- RDS: xoa DB instances/snapshots khong can.
- DynamoDB: xoa tables/indexes khong dung.
- Luu y free tier DynamoDB: tranh vuot gioi han capacity (theo ngu canh tai lieu nay, 10 RCU / 10 WCU).

### 6. API va tich hop
- API Gateway: xoa API/stage khong dung.
- SNS: xoa topic/subscription dung de test.
- SQS: xoa queue test.
- Step Functions / SWF: xoa workflow/state machine test.

### 7. Developer Tools
- Don dep CodeCommit repositories.
- Xoa CodeBuild projects.
- Xoa CodeDeploy applications/deployment groups.
- Xoa CodePipeline pipelines.

### 8. Giam sat va ha tang bang code
- CloudWatch: xoa alarms, dashboards, events/rules.
- CloudFormation: xoa stacks (cach nhanh de xoa nhom tai nguyen).
- Systems Manager Parameter Store: xoa parameters da tao khi lab.

### 9. Streaming / Analytics
- Kinesis: xoa streams da tao de test.
- Quan trong: Kinesis co the ton chi phi cao va thuong khong nam trong free tier.

### 10. Bao mat va danh tinh
- Cognito: xoa user pools/identity pools test.
- IAM: xoa user/role/policy dung cho lab sau khi da xoa cac tai nguyen phu thuoc.

## Kiem tra nhanh lan cuoi
- Chuyen tung region de xac nhan khong con tai nguyen tinh phi.
- Kiem tra Billing Dashboard va Cost Explorer de phat hien chi phi moi.
- Giup ban tiet kiem tien: dung lai checklist nay sau moi lan hoc/lab.

## Bai hoc chinh
Muc tieu khong chi la hoc thi, ma con la ren luyen cach van hanh AWS an toan, toi uu chi phi. Don dep tai nguyen la mot phan cua thuc hanh chuyen nghiep.
