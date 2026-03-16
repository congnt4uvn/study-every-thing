# Huong Dan Hoc AWS CDK Xu Ly Hinh Anh

## Tong Quan

Tai lieu nay duoc xay dung tu mot bai huong dan su dung AWS CDK de trien khai mot he thong xu ly hinh anh tren AWS. Giai phap tao ra:

- Mot bucket Amazon S3 de luu hinh anh duoc tai len
- Mot ham AWS Lambda de xu ly hinh anh
- Amazon Rekognition de nhan dien nhan trong hinh anh
- Mot bang Amazon DynamoDB de luu ket qua nhan dien

Muc tieu chinh la hieu cach Infrastructure as Code hoat dong voi AWS CDK va cach cac dich vu AWS lien ket voi nhau trong mot quy trinh huong su kien.

## Kien Truc

Luong xu ly cua ung dung nhu sau:

1. Nguoi dung tai mot hinh anh len bucket S3.
2. S3 kich hoat mot ham Lambda.
3. Ham Lambda gui hinh anh den Amazon Rekognition.
4. Rekognition tra ve cac nhan da phat hien.
5. Ham Lambda luu ten hinh va danh sach nhan vao DynamoDB.

## Tai Sao Nen Dung AWS CDK

AWS CDK cho phep ban dinh nghia ha tang bang ngon ngu lap trinh nhu JavaScript hoac Python thay vi viet truc tiep CloudFormation.

Loi ich duoc nhac den trong bai hoc:

- Phat trien nhanh hon voi ngon ngu quen thuoc
- Co the tai su dung cac construct va abstraction
- De lien ket giua cac tai nguyen ha tang
- CDK tu dong sinh ra mau CloudFormation

## Cac Dich Vu AWS Duoc Su Dung

### Amazon S3

- Luu tep hinh anh duoc tai len
- Gui su kien khi co object moi duoc tao

### AWS Lambda

- Chay ma serverless khi duoc S3 kich hoat
- Goi Rekognition va ghi ket qua vao DynamoDB

### Amazon Rekognition

- Nhan dien cac nhan trong hinh anh
- Vi du nhan co the la `penguin`, `bird`, `person`, `shoe`

### Amazon DynamoDB

- Luu ket qua da xu ly
- Moi item chua ten tep va cac nhan duoc phat hien

### AWS IAM

- Cap quyen de Lambda truy cap cac dich vu AWS khac
- Cac policy co the duoc gan ngay trong ma CDK

### AWS CloudFormation

- CDK bien ha tang thanh mau CloudFormation
- CloudFormation thuc hien viec trien khai thuc te

## Cac Buoc Thiet Lap Trong Bai Hoc

### 1. Cai dat thu vien CDK

Bai hoc cai dat phu thuoc CDK bang `npm`.

Vi du:

```bash
sudo npm install aws-cdk-lib
```

Sau khi cai dat, lenh `cdk` se san sang de su dung.

### 2. Tao du an CDK

Tao thu muc du an va khoi tao CDK app.

Vi du:

```bash
mkdir cdk-app
cd cdk-app
cdk init app --language javascript
```

Kiem tra viec khoi tao:

```bash
cdk ls
```

Ket qua mong doi: mot stack, vi du `CdkAppStack`.

### 3. Thay the tep stack mac dinh

Tep duoc tao san trong thu muc `lib` se duoc thay bang ma CDK tu dinh nghia:

- S3 bucket
- IAM role va quyen truy cap
- Bang DynamoDB
- Ham Lambda
- Su kien S3 kich hoat Lambda
- Cac output nhu ten bucket

## Cac Khai Niem CDK Quan Trong

### Removal Policy

Tai nguyen co the duoc cau hinh voi removal policy nhu `DESTROY`, nghia la se bi xoa khi stack bi xoa.

### Outputs

CDK co the tao CloudFormation outputs, vi du:

- Ten bucket
- Ten bang

Nhung output nay rat huu ich sau khi trien khai.

### Rut Gon Quyen Truy Cap

CDK cung cap cac ham ho tro de cap quyen doc ghi cho Lambda ma khong can tu viet day du IAM policy.

### Tham Chieu Giua Cac Dich Vu

Tai nguyen co the tham chieu den nhau trong ma. Vi du:

- Lambda nhan environment variable dua tren bang DynamoDB
- Lambda duoc gan vao su kien cua S3

Day la loi the lon cua viec dung ngon ngu lap trinh de mo ta ha tang.

## Muc Dich Cua Ham Lambda

Ham Lambda thuc hien cac buoc sau:

1. Nhan su kien tu S3 khi mot hinh anh duoc tai len.
2. Doc thong tin cua hinh anh.
3. Goi Amazon Rekognition de nhan dien nhan.
4. Ghi ket qua vao DynamoDB.

Bai hoc cho biet ma nguon Lambda duoc viet bang Python trong tep `index.py`.

## Bootstrap, Synthesize, Deploy

### CDK Bootstrap

Truoc khi trien khai CDK app trong mot account va region, ban can chay bootstrap mot lan.

```bash
cdk bootstrap
```

Lenh nay tao cac tai nguyen ho tro nhu:

- S3 bucket
- IAM roles
- ECR repository
- SSM parameters

Thong thuong chung nam trong stack CloudFormation co ten `CDKToolkit`.

### CDK Synthesize

Sinh ra mau CloudFormation tren may cuc bo:

```bash
cdk synth
```

Lenh nay giup ban xem truoc nhung tai nguyen se duoc tao.

### CDK Deploy

Trien khai stack len AWS:

```bash
cdk deploy
```

Lenh nay tao cac tai nguyen thuc te trong tai khoan AWS cua ban.

## Kiem Thu Toan Bo Quy Trinh

Sau khi trien khai:

1. Mo bucket S3 da tao.
2. Tai len mot vai hinh anh mau.
3. Cho Lambda chay.
4. Kiem tra bang DynamoDB.

Ket qua mong doi:

- Moi hinh anh tao ra mot item moi trong DynamoDB.
- Item chua ten tep va cac nhan da duoc phat hien.

Vi du trong bai hoc co cac hinh:

- `penguins.jpeg`
- `kid_and_pigeons`
- `swans`

## Don Dep Tai Nguyen

De xoa toan bo he thong:

1. Lam rong bucket S3 truoc.
2. Xoa stack CDK.

```bash
cdk destroy
```

Dieu nay giup tranh loi khi xoa stack, vi bucket S3 thuong phai rong truoc khi bi xoa.

## Cac Y Quan Trong De On Tap

- AWS CDK la cong cu Infrastructure as Code sinh ra CloudFormation.
- S3 co the kich hoat Lambda thong qua su kien tao object.
- Lambda co the goi Amazon Rekognition de phan tich hinh anh.
- DynamoDB phu hop de luu ket qua dang key-value nhanh.
- IAM permission la bat buoc de cac dich vu truy cap nhau.
- `cdk bootstrap`, `cdk synth`, `cdk deploy`, `cdk destroy` la cac lenh cot loi.
- CDK giup lien ket nhieu dich vu de hon so voi viet template thu cong.

## Cau Hoi On Tap Goi Y

1. Tai sao nen dung AWS CDK thay vi viet CloudFormation truc tiep?
2. Su kien nao lam cho ham Lambda duoc kich hoat trong kien truc nay?
3. Rekognition tra ve loai du lieu nao trong vi du nay?
4. Tai sao DynamoDB phu hop de luu ket qua nhan dien?
5. Tai sao can lam rong bucket S3 truoc khi chay `cdk destroy`?

## Tom Tat Ngan

Vi du nay minh hoa mot ung dung AWS huong su kien duoc xay bang CDK. Hinh anh duoc tai len S3, xu ly boi Lambda va Rekognition, sau do ket qua duoc luu vao DynamoDB. Bai hoc nhan manh cach CDK don gian hoa viec tao ha tang, cap quyen, trien khai va don dep tai nguyen.