# Ghi Chu Hoc AWS Amplify

## 1. Bai Hoc Nay Noi Ve Gi
Bai hoc nay huong dan cach trien khai nhanh mot ung dung React bang AWS Amplify, ket noi voi GitHub, va hieu Amplify da tao gi trong tai khoan AWS.

## 2. Quy Trinh Tong The
1. Mo AWS Amplify va chon **Create new app**.
2. Su dung starter template tu tai lieu huong dan.
3. Clone repository mau vao tai khoan GitHub cua ban.
4. Trong Amplify, chon **GitHub** lam source provider.
5. Cap quyen de Amplify truy cap repository.
6. Chon repository va branch vua clone.
7. Giu nguyen build settings mac dinh.
8. De Amplify tu dong tao va dung service role moi.
9. Bam **Save and deploy**.

## 3. Dieu Gi Xay Ra Khi Deploy
- Amplify bootstrap cac tai nguyen can thiet trong tai khoan AWS.
- Cac stack AWS CDK/CloudFormation duoc tao hoac cap nhat.
- Ung dung duoc build va deploy tu dong thong qua CI/CD.
- He thong tao domain URL de truy cap app.

## 4. Cac Dich Vu Ban Se Lam Viec Cung
- **AWS Amplify Console**: Noi quan ly build/deploy va cai dat ung dung.
- **CloudFormation**: Theo doi stack chinh va nested stacks.
- **Data Manager (Amplify)**: Xem/sua du lieu cua ung dung.
- **DynamoDB**: Bang du lieu nen luu cac to-do items.
- **User Management (tich hop Cognito)**: Quan ly nguoi dung xac thuc.
- **Storage (vi du backend S3)**: Cau hinh luu tru file/object.
- **Functions (nen Lambda)**: Them serverless functions cho backend.
- **UI Library**: Su dung UI components va Figma-to-React.

## 5. Y Chinh Can Nho
- Amplify cung cap quy trinh all-in-one de host full-stack app tren AWS.
- Ha tang duoc truu tuong hoa, nhung van xem duoc trong CloudFormation.
- Du lieu tao trong app xuat hien ca o Amplify Data Manager va DynamoDB.
- Co the mo rong voi authentication, storage, va serverless functions.
- CI/CD duoc tich hop san khi ket noi GitHub.

## 6. Cac Khu Vuc Nen Kham Pha Trong Console
- Deployments
- Data
- User management
- Storage
- Functions
- UI library
- Custom domains
- Build notifications
- Build settings
- Environment variables

## 7. Cac Buoc Don Dep Tai Nguyen (Quan Trong)
1. Vao app settings cua Amplify, mo **General settings**.
2. Xoa app (xac nhan bang cach nhap `delete`).
3. Neu khong dung nua, xoa repository tren GitHub.

## 8. Cau Hoi Tu Kiem Tra Nhanh
1. Vi sao can ket noi Amplify voi GitHub?
2. Dich vu nao luu cac to-do items?
3. Xem ha tang do Amplify tao o dau?
4. Trong bai nay dung lua chon service role nao?
5. Tinh nang nao dung de bo sung authentication?

## 9. Bai Tap Thuc Hanh Nho
- Deploy starter app.
- Them it nhat 2 to-do items.
- Kiem tra records trong Amplify Data Manager.
- Kiem tra records trong DynamoDB.
- Xoa tat ca tai nguyen sau khi thuc hanh.
