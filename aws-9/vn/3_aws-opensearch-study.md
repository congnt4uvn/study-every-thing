# Ghi Chu Hoc AWS: Amazon OpenSearch Service

## 1) Amazon OpenSearch Service La Gi?
Amazon OpenSearch Service la dich vu tim kiem va phan tich du lieu do AWS quan ly.
Day la dich vu ke nhiem cua Amazon Elasticsearch Service.

## 2) Tai Sao Dung OpenSearch?
OpenSearch phu hop khi ban can:
- Tim kiem full-text tren nhieu truong du lieu
- Tim kiem khop mot phan (vi du: mot phan ten san pham)
- Chay truy van phan tich nhanh tren du lieu da index

So voi DynamoDB:
- DynamoDB thuong truy van theo primary key hoac index
- OpenSearch cho phep tim kiem linh hoat tren nhieu field cua document

## 3) Cac Cach Trien Khai
Co 2 mo hinh chinh:
- Managed cluster: ban chon va van hanh cac instance duoc provision
- Serverless: AWS tu dong scale va van hanh

## 4) Ngon Ngu Truy Van Va SQL
- OpenSearch co query language rieng
- SQL khong duoc ho tro native mac dinh
- Co the bat SQL compatibility bang plugin

## 5) Nguon Nap Du Lieu Pho Bien
Du lieu co the vao OpenSearch tu:
- Amazon Kinesis Data Firehose
- AWS IoT
- Amazon CloudWatch Logs
- Ung dung tu xay dung

## 6) Bao Mat
OpenSearch tich hop voi:
- Amazon Cognito
- AWS IAM

Ho tro ma hoa:
- Ma hoa du lieu luu tru (at rest)
- Ma hoa khi truyen (in transit)

## 7) Phan Tich Va Truc Quan Hoa
Dung OpenSearch Dashboards de:
- Tao dashboard va bieu do
- Phan tich du lieu da index

## 8) Kien Truc Thuong Gap

### Mo Hinh A: DynamoDB + OpenSearch cho Search
1. Ung dung ghi du lieu vao DynamoDB
2. DynamoDB Streams ghi nhan thay doi
3. AWS Lambda doc stream event
4. Lambda index du lieu vao OpenSearch gan nhu real time
5. Ung dung tim trong OpenSearch de lay item ID
6. Ung dung dung item ID de lay full record tu DynamoDB

Ly do mo hinh nay pho bien:
- DynamoDB van la source of truth
- OpenSearch dam nhan tim kiem nang cao

### Mo Hinh B: CloudWatch Logs vao OpenSearch
Lua chon 1 (real time):
- CloudWatch Logs Subscription Filter -> AWS managed Lambda -> OpenSearch

Lua chon 2 (near real time):
- CloudWatch Logs Subscription Filter -> Kinesis Data Firehose -> OpenSearch

### Mo Hinh C: Kinesis vao OpenSearch
Lua chon 1 (near real time):
- Kinesis Data Streams -> Kinesis Data Firehose -> (co the Lambda transform) -> OpenSearch

Lua chon 2 (real time, custom code):
- Kinesis Data Streams -> Lambda tu viet consumer -> OpenSearch

## 9) Real Time Va Near Real Time
- Lambda xu ly stream thuong la real time
- Firehose thuong la near real time vi co co che buffer

## 10) Y Chinh De On Tap
- OpenSearch dung cho ca tim kiem va phan tich
- Thuong di cung DynamoDB, khong nhat thiet thay the hoan toan
- DynamoDB luu du lieu goc, OpenSearch luu du lieu phuc vu search
- Firehose de trien khai, nhung near real time
- Lambda linh hoat hon, co the real time
- OpenSearch Dashboards de truc quan hoa

## 11) Cau Hoi Tu Kiem Tra
1. Vi sao nen giu DynamoDB lam source of truth?
2. Khac nhau giua Firehose ingestion va Lambda ingestion?
3. Tim kiem mot phan chuoi nen dung dich vu nao?
4. Khi nao nen chon OpenSearch Serverless?

## 12) Tom Tat 1 Cau
Dung Amazon OpenSearch Service khi ung dung can tim kiem manh va phan tich du lieu nhanh, trong khi van giu du lieu chinh o he thong nhu DynamoDB.