# Ghi Chu Hoc AWS AppSync

## Muc tieu hoc tap
Xay dung mot GraphQL API don gian bang AWS AppSync, ket noi voi DynamoDB, thu mutation/query, xem cac cai dat quan trong va don dep tai nguyen sau khi hoc.

## AppSync la gi?
AWS AppSync la dich vu managed de tao GraphQL API.
- Co the ket noi den nguon du lieu nhu DynamoDB.
- Giup client web va mobile dung chung mot lop API.
- Ho tro real-time va nhieu kieu xac thuc.

## Quy trinh thuc hanh

### 1. Tao API
1. Mo AWS AppSync.
2. Chon **GraphQL APIs** (khong chon Merged API cho bai co ban).
3. Chon **Design from scratch**.
4. Dat ten API: **My AppSync API**.

### 2. Dinh nghia model backed boi DynamoDB
1. Tao type backed boi DynamoDB.
2. Ten model: **Student**.
3. Them cac field:
   - `id`: `ID!` (bat buoc)
   - `name`: `String!` (bat buoc)
   - `age`: `Int` (khong bat buoc)
   - `certified`: `Boolean` (khong bat buoc)

### 3. Cau hinh bang DynamoDB
- Ten bang: **StudentTable**
- Primary key: `id`
- Khong dung sort key

Sau do tao API.

## Ket qua sau khi tao
AppSync tu dong tao:
- GraphQL schema
- Data source lien ket toi DynamoDB
- Cac thao tac query/mutation co ban

Co the vao DynamoDB de kiem tra bang `StudentTable` da duoc tao.

## Thu nghiem trong phan Queries cua AppSync

### Query truoc khi co du lieu
Chay `listStudents` truoc: ket qua rong.

### Them du lieu bang mutation
Dung `createStudent` voi du lieu mau:
- Hoc vien 1: Mike, 25 tuoi, certified true
- Hoc vien 2: Alice, 30 tuoi, certified true

### Query lai
Chay `listStudents` va xac nhan da tra ve ca 2 hoc vien.

### Kiem tra trong DynamoDB
Vao table items cua `StudentTable` de doi chieu du lieu.

## Cac cai dat AppSync can nho

### Caching
- Full request caching
- Per-resolver caching
- Khong caching

### Thong tin API
- GraphQL endpoint
- API ID
- Real-time endpoint

### Authorization modes
- API Key (su dung trong bai nay)
- IAM
- OpenID Connect
- AWS Lambda authorizer
- Amazon Cognito User Pool

AppSync cho phep dung nhieu co che authorization cung luc.

### Monitoring
Theo doi so request, so loi va cac metric lien quan.

### Custom domain
Co the map API vao domain rieng.

## Y nghia thuc te
Ban co the tao nhanh mot GraphQL API tren DynamoDB.
- Dung cho web (JavaScript).
- Dung cho mobile (Android/iOS).
- Mot kieu API cho nhieu nen tang frontend.

## Don dep tai nguyen
Sau khi hoc xong de tranh ton chi phi:
1. Xoa AppSync API (`My AppSync API`).
2. Xoa DynamoDB table (`StudentTable`).

## Cau hoi tu on
1. Vi sao bai co ban nen chon GraphQL API thay vi Merged API?
2. Field nao dong vai tro partition key trong bai nay?
3. Mutation nao dung de them hoc vien?
4. Query nao dung de lay danh sach hoc vien?
5. Ke ten 2 phuong thuc authorization ma AppSync ho tro.

## Nho nhanh 5 phut
- AppSync cung cap GraphQL API duoc quan ly san.
- AppSync co the dung DynamoDB lam data source.
- Schema va thao tac co the duoc tao tu dong tu model.
- Thao tac quen thuoc: `createStudent`, `listStudents`.
- Luon xoa AppSync API va DynamoDB table sau khi lab.
