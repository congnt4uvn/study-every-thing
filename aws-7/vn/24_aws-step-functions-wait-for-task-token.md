# Ghi chu hoc AWS: Step Functions Wait for Task Token

## Tong quan
`waitForTaskToken` la mot integration pattern trong Step Functions, duoc dung khi workflow can tam dung de cho callback tu he thong ben ngoai truoc khi tiep tuc.

Ban nen dung pattern nay khi quy trinh phu thuoc vao:
- Dich vu AWS khac
- Phe duyet thu cong (human approval)
- He thong ben thu ba
- He thong legacy nam ngoai Step Functions

## Co che hoat dong
Trong mot Task state, them `.waitForTaskToken` vao truong `Resource`.

Vi du y tuong:
- `sqs:sendMessage.waitForTaskToken`

Khi dung pattern nay, workflow se tam dung cho den khi nhan callback voi dung token qua mot trong hai API:
- `SendTaskSuccess`
- `SendTaskFailure`

## Luong xu ly thuong gap
1. Step Functions bat dau execution.
2. Mot task (vi du kiem tra han muc tin dung) can xu ly ben ngoai.
3. Step Functions gui message den SQS, kem theo:
- Du lieu nghiep vu (input payload)
- Task token
4. Worker ben ngoai doc SQS (Lambda, ECS, EC2, hoac server ben thu ba).
5. Worker xu ly message.
6. Worker goi callback API ve Step Functions bang dung token da nhan:
- Thanh cong: `SendTaskSuccess` + output
- That bai: `SendTaskFailure`
7. Step Functions kiem tra token hop le va tiep tuc workflow.

## Loi ich cua pattern
- Tach biet orchestration voi he thong xu ly ben ngoai
- Ho tro tac vu bat dong bo va chay lau
- Phu hop quy trinh co con nguoi phe duyet
- Tich hop de dang voi he thong non-AWS va legacy

## Diem can nho
- Luon truyen task token cho he thong xu ly ben ngoai.
- Callback phai dung chinh xac token da nhan.
- Neu khong co callback, execution se bi tam dung (hoac timeout neu co cau hinh).
- Can co xu ly loi ro rang cho nhanh `SendTaskFailure`.

## Cau hoi on tap nhanh
1. Tai sao dung `waitForTaskToken` thay vi Task thong thuong?
2. Hai callback API nao co the ket thuc task dang tam dung?
3. Message gui ra ngoai can co du lieu bat buoc nao?
4. Dieu gi xay ra neu he thong ben ngoai khong callback?
