# Ghi chu hoc AWS: Xu ly loi trong Step Functions

## Muc tieu
Hieu cach AWS Step Functions xu ly loi tu AWS Lambda bang `Retry` va `Catch`.

## Tinh huong trong bai hoc
- Tao mot ham Lambda tu blueprint loi cua Step Functions.
- Ham duoc thiet ke de chu dong nem loi.
- State machine goi ham Lambda nay.
- Luong xu ly se di theo nhanh khac nhau tuy loai loi.

## Hanh vi cua Lambda
Ban dau, Lambda nem loi tuy chinh ten `CustomError`.

Y tuong code:
```js
throw new Error("This is a custom error!")
```

Sau do, Lambda duoc sua de nem mot loai loi khac (`NotCustomError`) de kiem tra nhanh xu ly khac.

## Thiet ke state machine
Luong chinh:
1. Goi task Lambda.
2. Neu thanh cong, ket thuc workflow.
3. Neu that bai, ap dung chinh sach retry.
4. Neu retry het lan, dinh tuyen bang catch.

Cac fallback state trong bai:
- `CustomErrorFallback`
- `ReservedTypeFallback`
- `CatchAllFallback`

## Khai niem quan trong
### 1) Retry
`Retry` cho phep thu lai tu dong truoc khi state that bai hoan toan.

Cac truong thuong gap:
- `ErrorEquals`: loai loi ap dung retry
- `IntervalSeconds`: thoi gian cho truoc lan retry dau
- `MaxAttempts`: tong so lan thu
- `BackoffRate`: he so nhan de tang thoi gian cho cho lan sau

Quan sat trong demo:
- `CustomError` duoc retry nhanh.
- Loi khac duoc retry cham hon (vi du 30 giay, sau do 60 giay).

### 2) Catch
`Catch` xu ly loi sau khi da het so lan retry.

Dinh tuyen trong demo:
- `CustomError` -> `CustomErrorFallback`
- Loi loai reserved/test -> `ReservedTypeFallback`
- Moi loi con lai (`States.ALL`) -> `CatchAllFallback`

## Dieu gi da xay ra khi chay
### Truong hop A: `CustomError`
- Lambda that bai.
- Step Functions retry nhanh.
- Khi het retry, execution chuyen sang `CustomErrorFallback`.
- Workflow van hoan tat thanh cong.

### Truong hop B: loi khac (`NotCustomError`)
- Lambda that bai voi loai loi khac.
- Thoi gian retry theo chinh sach khac (cho lau hon).
- Sau retry, execution chuyen sang `ReservedTypeFallback`.
- Workflow van hoan tat thanh cong.

## Vi sao phan nay quan trong
- Ban co the tao workflow ben vung ma khong can tu viet vong lap retry.
- Moi loai loi co the co chien luoc phuc hoi rieng.
- Event history cua Step Functions giup debug tung lan retry va tung transition.

## Don dep tai nguyen
Neu khong dung nua, ban co the xoa state machine va Lambda da tao.

## Cau hoi on tap nhanh
1. Khac nhau giua `Retry` va `Catch` trong Step Functions la gi?
2. `States.ALL` dung de lam gi?
3. `BackoffRate` anh huong the nao den thoi gian retry?
4. Vi sao can dinh tuyen tung loai loi vao cac fallback khac nhau?
