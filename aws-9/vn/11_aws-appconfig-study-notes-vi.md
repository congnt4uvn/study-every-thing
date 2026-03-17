# Ghi Chu Hoc AWS AppConfig

## 1. AWS AppConfig la gi?
AWS AppConfig giup quan ly cau hinh ung dung tach roi khoi ma nguon.

Voi AppConfig, ban co the:
- Cau hinh thong so dong (dynamic)
- Kiem tra tinh hop le truoc khi trien khai
- Trien khai thay doi cau hinh an toan
- Tu dong rollback khi phat hien su co

Dieu nay cho phep ung dung thay doi hanh vi ma khong can deploy lai code hoac restart dich vu.

## 2. Tai sao nen dung AppConfig?
Nhieu ung dung de cau hinh trong code hoac bien moi truong. Cach nay don gian nhung kem linh hoat.

AppConfig mang lai:
- Thay doi cau hinh nhanh va an toan hon
- Vong doi cau hinh doc lap voi vong deploy ung dung
- Kiem soat rollout theo tung buoc
- Cap nhat runtime phu hop he thong cloud hien dai

## 3. Vi du ve Feature Flag
Use case pho bien nhat la feature flag.

Quy trinh vi du:
1. Deploy code moi voi flag = `false`
2. Kiem tra he thong van on dinh
3. Chuyen flag sang `true` trong AppConfig
4. Ung dung doc gia tri moi va bat tinh nang

Khong can deploy lai code.

## 4. Cac truong hop cau hinh dong khac
AppConfig co the quan ly:
- Tham so toi uu hieu nang
- Danh sach IP cho phep / chan
- Nguong van hanh (threshold)
- Bat/tat quy tac nghiep vu

## 5. Nguon cau hinh den tu dau?
Theo noi dung tai lieu, AppConfig co the lay cau hinh tu:
- AWS Systems Manager Parameter Store
- AWS Systems Manager Documents
- Amazon S3
- Cac nguon duoc ho tro khac

Ung dung chay tren EC2, Lambda, ECS, EKS... se dinh ky lay cap nhat cau hinh.

## 6. Trien khai an toan va Rollback
AppConfig ho tro rollout cau hinh theo tung giai doan.

Loi ich rollout dan dan:
- Giam pham vi anh huong khi co loi
- Phat hien su co som
- Co the rollback tu dong neu chi so he thong xau di

Co the ket hop Amazon CloudWatch alarm.
Neu alarm kich hoat, AppConfig co the quay lai cau hinh on dinh truoc do.

## 7. Cac cach validate cau hinh
Truoc khi trien khai, AppConfig co the validate bang:
- JSON Schema: kiem tra cau truc/kieu du lieu
- AWS Lambda validator: kiem tra logic phuc tap tuy chinh

Muc tieu la ngan cau hinh sai vao production.

## 8. Cac dich vu duoc nhac den
Tai lieu nhac rang AppConfig huu ich cho ung dung chay tren:
- Amazon EC2
- AWS Lambda
- Amazon ECS
- Amazon EKS

## 9. Tom tat kieu on thi
- AppConfig tach cau hinh khoi qua trinh deploy code.
- Ho tro thay doi cau hinh ngay luc runtime.
- Ho tro feature flag va cac cai dat van hanh dong.
- Co validate, rollout theo dot, giam sat CloudWatch va rollback.

## 10. Cau hoi tu kiem tra
1. Vi sao nen tach cau hinh ra khoi code?
2. AppConfig cai thien viec van hanh feature flag nhu the nao?
3. Khac nhau giua JSON Schema va Lambda validation?
4. Vi sao rollout dan dan an toan hon rollout toan bo?
5. CloudWatch alarm dong vai tro gi trong co che bao ve?
