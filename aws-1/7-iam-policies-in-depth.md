# Tìm Hiểu Sâu Về IAM Policies (Chính Sách IAM)

## Tổng Quan

Trong bài giảng này, chúng ta sẽ khám phá chi tiết về IAM policies và hiểu cách chúng hoạt động với users, groups cũng như cấu trúc kế thừa của chúng.

## Cấu Trúc IAM Policy và Groups

### Gán Policy Dựa Trên Group

Hãy xem xét một ví dụ thực tế với một nhóm các developers:
- **Users**: Alice, Bob, và Charles
- Khi chúng ta gán một policy ở cấp độ group, nó sẽ áp dụng cho tất cả các thành viên
- Cả ba users (Alice, Bob, và Charles) đều sẽ kế thừa và có quyền truy cập thông qua policy này

### Ví Dụ Về Nhiều Groups

Nếu chúng ta có một nhóm thứ hai gọi là "Operations" với một policy khác:
- Users David và Edward sẽ có policy khác với nhóm developers
- Mỗi nhóm duy trì bộ quyền riêng biệt của mình

### Inline Policies

Đối với các users riêng lẻ như Fred:
- Users không nhất thiết phải thuộc về một group
- Chúng ta có thể tạo **inline policies** - các policies được gán trực tiếp cho một user cụ thể
- Inline policies có thể được áp dụng cho bất kỳ user nào, dù họ có thuộc group hay không

### Thành Viên Của Nhiều Groups

Users có thể thuộc nhiều groups cùng một lúc:
- Nếu Charles và David đều thuộc về "Audit Team" với policy riêng
- **Charles** kế thừa policies từ cả hai:
  - Policy của nhóm Developers
  - Policy của nhóm Audit team
- **David** kế thừa policies từ cả hai:
  - Policy của nhóm Operations team
  - Policy của nhóm Audit team

Mô hình kế thừa này sẽ trở nên rõ ràng hơn khi bạn thực hành trực tiếp.

## Cấu Trúc IAM Policy

### Định Dạng JSON Document

IAM policies được viết dưới dạng JSON documents. Hiểu cấu trúc này rất quan trọng vì bạn sẽ gặp nó thường xuyên trong AWS.

### Các Thành Phần Chính

Cấu trúc IAM policy bao gồm:

#### 1. Version (Phiên bản)
- Thường là `2012-10-17`
- Đại diện cho phiên bản ngôn ngữ policy

#### 2. ID (Tùy chọn)
- Định danh cho policy
- Không bắt buộc nhưng hữu ích cho việc tổ chức

#### 3. Statement(s) (Câu lệnh)
- Có thể là một hoặc nhiều statements
- Mỗi statement chứa nhiều phần quan trọng

### Các Thành Phần Của Statement

Mỗi statement bao gồm:

#### Sid (Statement ID)
- Định danh cho statement
- Trường tùy chọn
- Ví dụ: Có thể được đánh số như "1", "2", v.v.

#### Effect (Bắt buộc)
- Xác định statement **cho phép** hay **từ chối** quyền truy cập
- Chỉ có hai giá trị: `Allow` hoặc `Deny`

#### Principal (Bắt buộc)
- Chỉ định accounts, users, hoặc roles mà policy áp dụng
- Ví dụ: Có thể là root account của AWS account của bạn

#### Action (Bắt buộc)
- Danh sách các API calls sẽ được cho phép hoặc từ chối dựa trên Effect
- Định nghĩa những operations nào có thể được thực hiện

#### Resource (Bắt buộc)
- Danh sách các resources mà actions sẽ được áp dụng
- Ví dụ: Một S3 bucket hoặc các AWS resources khác

#### Condition (Tùy chọn)
- Chỉ định khi nào statement nên được áp dụng
- Không phải lúc nào cũng có vì nó là tùy chọn

## Chuẩn Bị Cho Kỳ Thi

Đối với kỳ thi AWS, hãy đảm bảo bạn hiểu các thành phần chính sau:
- **Effect**: Allow hoặc Deny
- **Principal**: Policy áp dụng cho ai
- **Action**: Những API calls nào bị ảnh hưởng
- **Resource**: Những resources nào được nhắm đến

Đừng lo lắng nếu điều này có vẻ phức tạp bây giờ - bạn sẽ gặp những khái niệm này xuyên suốt khóa học và sẽ tự tin hơn với chúng vào cuối khóa.

## Tóm Tắt

- IAM policies kiểm soát quyền truy cập vào các AWS resources
- Policies có thể được gán cho groups, users, hoặc roles
- Users kế thừa policies từ tất cả các groups họ thuộc về
- Inline policies cung cấp quyền cụ thể cho từng user
- Cấu trúc policy tuân theo định dạng JSON chuẩn
- Hiểu về Effect, Principal, Action, và Resource là cần thiết

Đó là tất cả cho bài giảng này! Hẹn gặp bạn ở bài tiếp theo.