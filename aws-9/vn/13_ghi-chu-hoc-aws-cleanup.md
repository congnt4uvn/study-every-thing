# Ghi Chu Hoc AWS Ve Cleanup

## Muc tieu
Tai lieu nay giup ban on tap cac dich vu AWS va thuc hanh cleanup an toan sau moi bai lab hoac du an.

## Cach hoc
1. Hieu vai tro cua tung dich vu.
2. Xac dinh cac tai nguyen thuong duoc tao trong bai lab.
3. Luyen tim tai nguyen bang AWS Console va AWS CLI.
4. Kiem tra phu thuoc truoc khi xoa.
5. Xac minh chi phi va giam sat sau cleanup.

## Checklist Cleanup Theo Dich Vu

### Compute va Scaling
- EC2 Instances: Dung hoac terminate instance khong dung; kiem tra EBS va security group dinh kem.
- Elastic Load Balancer: Xoa ALB/NLB/CLB va target group khong con su dung.
- Launch Configurations: Xoa launch configuration cu khong con dung boi Auto Scaling.
- Auto Scaling Groups: Giam scale ve 0 va xoa group khong can thiet.
- Elastic IPs: Release Elastic IP khong gan voi tai nguyen nao.
- Security Groups: Xoa security group khong dung sau khi chac chan khong co network interface su dung.
- EBS Volumes: Xoa volume khong attach va snapshot cu neu khong can.
- Key Pairs: Xoa key pair khong su dung tren AWS va may local.
- ECS (Cluster, Service, Task Definition, ECR): Xoa service, dua task ve 0, xoa task definition va image ECR khong can.
- Elastic Beanstalk Applications va Environments: Terminate environment va xoa app version cu.
- AWS Lambda Functions: Xoa function cu va cac version khong can.

### Storage va Database
- S3 Files va Buckets: Lam rong bucket truoc, sau do xoa bucket khong con dung.
- RDS Database: Tao snapshot neu can, roi xoa database test va read replica.
- DynamoDB Tables va Indexes: Xoa table va GSI/LSI duoc tao de test.
- ElastiCache Cluster: Xoa cluster Redis/Memcached khong hoat dong.

### Networking va Integration
- Route 53: Xoa hosted zone va record khong su dung.
- API Gateway: Xoa API, stage va custom domain mapping da cu.
- Kinesis Streams: Xoa stream khong con producer/consumer.
- SNS Topics: Xoa topic test va subscription khong dung.
- SQS Queues: Xoa queue va dead-letter queue khong can.

### DevOps va Monitoring
- CodeCommit: Luu tru hoac xoa repository khong con dung.
- CodeBuild: Xoa project build cu va artifact khong can.
- CodePipeline: Xoa pipeline khong hoat dong va tai nguyen lien quan.
- CloudWatch Logs: Dat retention va xoa log group khong can.
- CloudWatch Metrics: Ra soat custom metric co the phat sinh chi phi.
- CloudWatch Dashboards: Xoa dashboard da cu.
- CloudWatch Alerts: Xoa alarm khong con gia tri hoac cap nhat nguong.
- CloudWatch Rules (EventBridge Rules): Tat/xoa rule schedule hoac event khong dung.
- CloudFormation Stacks: Xoa stack loi/cu va kiem tra retained resources.
- SSM Parameter Store: Xoa parameter cu va bao mat parameter nhay cam.

### Identity va Access
- IAM Users, Groups, Roles, Policies: Xoa identity khong dung va policy cap quyen qua rong.

## Quy trinh Cleanup An Toan
1. Gan tag truoc khi lam lab (vi du: Project=Lab, Owner=YourName, ExpireDate=YYYY-MM-DD).
2. Dung Resource Groups hoac AWS Config de tim tai nguyen theo tag.
3. Xoa theo thu tu phu thuoc:
   - Tang ung dung (API, service)
   - Tang compute (EC2, ASG, Lambda, ECS)
   - Tang du lieu (RDS, DynamoDB, S3 backup)
   - Networking va IAM
4. Xac minh:
   - Billing giam dan.
   - Khong co CloudWatch alarm bat thuong.
   - Khong xoa nham tai nguyen production.

## Bai tap thuc hanh
- Tao mot mo hinh nho (EC2 + ALB + RDS + S3), sau do cleanup toan bo.
- Viet script checklist CLI de liet ke tai nguyen theo tag.
- So sanh chi phi hang thang truoc va sau cleanup.

## Cau hoi on tap nhanh
- Tai nguyen AWS nao thuong phat sinh chi phi du khong su dung?
- Tai sao can snapshot RDS truoc khi xoa?
- Can kiem tra phu thuoc gi truoc khi xoa security group?
- Tai sao tagging quan trong voi tu dong hoa cleanup?

Chuc mung ban, day la mot ky nang quan trong de lam AWS hieu qua va tiet kiem chi phi.
