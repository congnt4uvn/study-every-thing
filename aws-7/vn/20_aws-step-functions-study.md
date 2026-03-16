# AWS Step Functions - Ghi Chu Hoc Tap

## 1. AWS Step Functions la gi?
AWS Step Functions la dich vu dung de **dieu phoi quy trinh** theo mo hinh **state machine**.

- Moi workflow tuong ung mot state machine
- Workflow duoc dinh nghia bang JSON (Amazon States Language)
- Co giao dien truc quan va lich su thuc thi

Cac tinh huong su dung pho bien:
- Xu ly don hang
- Pipeline xu ly du lieu
- Workflow backend cho ung dung web
- Bat ky quy trinh nhieu buoc co nhanh re nhanh

## 2. Y tuong cot loi
Step Functions cho phep ban dinh nghia:
- Buoc dau tien la gi
- Buoc tiep theo la gi
- Dieu kien de di theo nhanh nao
- Cho bao lau giua cac buoc
- Ket thuc thanh cong hay that bai

No chu yeu dieu phoi cac dich vu khac, khong phai thay the logic xu ly chi tiet.

## 3. Cach khoi dong workflow
Co the khoi dong Step Functions bang:
- AWS SDK / API call
- API Gateway
- CloudWatch Events / Amazon EventBridge
- Chay thu cong tren AWS Console

## 4. Task state (quan trong nhat)
**Task** state dung de thuc hien cong viec thong qua tich hop voi dich vu AWS.

Cac tich hop pho bien:
- Goi AWS Lambda
- Gui job AWS Batch
- Chay Amazon ECS task va doi hoan tat
- Ghi du lieu vao Amazon DynamoDB
- Gui message len Amazon SNS hoac Amazon SQS
- Goi mot workflow Step Functions khac

Ngoai ra co **Activities**:
- Worker ben ngoai (EC2, ECS, hoac server on-prem) se polling de lay viec
- Worker xu ly va tra ket qua ve Step Functions

## 5. Vi du Task goi Lambda
Mot Task thuong co:
- `Type: Task`
- `Resource`: ARN tich hop goi Lambda
- `Parameters`: ten ham va payload
- `Next`: state tiep theo
- `TimeoutSeconds`: gioi han thoi gian

## 6. Cac loai state quan trong
- **Task**: thuc hien cong viec
- **Choice**: re nhanh theo dieu kien
- **Wait**: cho theo thoi gian hoac moc thoi gian
- **Pass**: truyen input sang output hoac chen du lieu co dinh
- **Parallel**: chay nhieu nhanh song song
- **Map**: lap dong tren danh sach du lieu
- **Succeed**: ket thuc thanh cong
- **Fail**: ket thuc that bai

Goc nhin on thi:
- Thuong gap nhat la Task va Parallel

## 7. Mau luong thuc thi truc quan
Mau quy trinh trong noi dung nguon:
1. Submit job
2. Wait X giay
3. Lay job status
4. Neu chua xong -> quay lai Wait (vong lap)
5. Neu xong -> lay final status
6. End

Diem manh cua Step Functions la nhin duoc luong chay va lich su tung buoc.

## 8. Tai sao khong gop het vao mot Lambda lon?
- De doc, de bao tri voi workflow phuc tap
- Co san nhanh, cho, retry, va duong xu ly loi
- Co lich su thuc thi va giao dien theo doi
- Toi uu cho dieu phoi nhieu dich vu

## 9. Cau hoi tu on
1. Task state co vai tro gi?
2. Khi nao dung Choice va khi nao dung Parallel?
3. Workflow co the duoc trigger bang nhung cach nao?
4. Lich su thuc thi giup gi trong moi truong production?
5. Khac nhau giua service integration truc tiep va Activities?
