# Ghi chu hoc AWS CDK Testing

## 1. Vi sao can test trong CDK
Khi dung AWS CDK, ban viet ha tang bang code.
Vi vay, ban co the test no giong nhu test code Python, JavaScript, va cac ngon ngu khac.

CDK co module assertion, thuong di kem framework test pho bien nhu:
- Jest (JavaScript/TypeScript)
- Pytest (Python)

Ban co the kiem tra resource, rule, condition, parameter truoc khi deploy.

## 2. Y tuong chinh cua CDK testing
Trong CDK test, ban thuong kiem tra CloudFormation template sau khi synthesize.
Muc tieu: dam bao template sinh ra dung voi ky vong.

## 3. Hai loai test

### A) Fine-grained assertions (pho bien nhat)
Kiem tra tung resource va thuoc tinh cu the.

Vi du:
- Lambda function co dung handler.
- Lambda function dung runtime `nodejs14.x`.
- SNS topic chi co 1 subscription.

Loai nay phu hop khi can kiem tra chinh xac cac thuoc tinh quan trong.

### B) Snapshot tests
So sanh template hien tai voi template moc da luu truoc do (snapshot).

Loai nay giup phat hien thay doi ha tang ngoai y muon.

## 4. Cach tao template de test
Co 2 method quan trong:

### `Template.fromStack(...)`
Dung khi stack duoc dinh nghia bang CDK code.

### `Template.fromString(...)`
Dung khi CloudFormation template nam ngoai CDK (template ben ngoai).

Hai method nay rat quan trong cho thi cu va lam viec thuc te.

## 5. Checklist on tap nhanh
- Nho su khac nhau giua fine-grained test va snapshot test.
- Nho khi nao dung `fromStack` va `fromString`.
- Co the assert cac thuoc tinh quan trong cua Lambda, SNS, DynamoDB, va resource khac.

## 6. Ket luan thuc hanh
Test CDK giup phat hien loi ha tang som, tang do tin cay khi deploy, va kiem soat thay doi tot hon theo thoi gian.
