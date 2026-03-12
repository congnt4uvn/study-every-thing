# Strangler Fig Pattern cho việc Migration Microservices

## Tổng quan

Khi migration một ứng dụng legacy hoặc monolithic sang kiến trúc microservices hiện đại, **Strangler Fig Pattern** là một design pattern đã được chứng minh mà các tổ chức có thể tuân theo. Pattern này cho phép tiếp cận migration dần dần với rủi ro thấp.

## Strangler Fig Pattern là gì?

Strangler Fig Pattern là một software migration pattern được sử dụng để dần dần thay thế hoặc tái cấu trúc một legacy system bằng một system mới. Đặc điểm chính là legacy application được thay thế bằng cách tiếp cận hiện đại **từng phần một**, mà không làm gián đoạn chức năng hiện có.

### Nguồn gốc của tên gọi

Pattern này lấy tên từ cách thức cây sung dây (strangler fig plant) phát triển quanh một cây hiện có, từ từ thay thế nó cho đến khi cây gốc không còn cần thiết nữa. Cây sung dây:
1. Bắt đầu như một cây nhỏ mọc bên cạnh cây gốc
2. Dần dần phát triển quanh cây chính
3. Cuối cùng thay thế hoàn toàn cây gốc

Cùng một chiến lược này được áp dụng khi các tổ chức migrate các legacy application của họ sang microservices.

## Khi nào sử dụng Pattern này

Strangler Fig Pattern được khuyến nghị mạnh mẽ trong các trường hợp sau:

1. **Hệ thống Legacy lớn hoặc phức tạp**: Khi hiện đại hóa một legacy system lớn hoặc phức tạp (không khuyến nghị cho các hệ thống nhỏ)
2. **Tránh rủi ro Big Bang Migration**: Khi bạn muốn tránh các rủi ro liên quan đến việc viết lại hệ thống hoàn toàn hoặc "Big Bang" migration (đột ngột migrate mọi thứ trong một ngày)
3. **Tính liên tục hoạt động**: Khi legacy system cần duy trì hoạt động trong quá trình chuyển đổi sang hệ thống mới

## Ví dụ Migration: Ứng dụng Ngân hàng

Hãy xem xét một ví dụ thực tế về migration ứng dụng ngân hàng:

### Trạng thái ban đầu
- **Ứng dụng Monolithic** chứa toàn bộ chức năng:
  - Cards (Thẻ)
  - Accounts (Tài khoản)
  - Loans (Khoản vay)

### Các giai đoạn Migration

#### Giai đoạn 1: Accounts Microservice
- Development team tạo **Accounts microservice**
- Chức năng còn lại (Cards và Loans) vẫn ở trong monolithic app
- Team xác thực rằng Accounts microservice hoạt động đúng trong production

#### Giai đoạn 2: Cards Microservice
- Sau khi hài lòng với việc triển khai Accounts microservice
- Team migrate chức năng **Cards** sang microservice
- Monolithic app bây giờ chỉ chứa chức năng Loans

#### Giai đoạn 3: Loans Microservice
- Sau khi Cards migration thành công
- Team migrate chức năng **Loans**
- Monolithic app được thay thế hoàn toàn

#### Trạng thái cuối cùng
- Không còn monolithic app
- Tất cả chức năng tồn tại như các microservices độc lập

## Lợi ích chính

### 1. Rủi ro tối thiểu
- Migrate chỉ một component tại một thời điểm giảm rủi ro
- Các vấn đề dễ dàng được xử lý khi chúng xảy ra
- Bài học từ lần migration đầu tiên giúp ích cho các lần migration tiếp theo

### 2. Migration từng bước
- Tránh các thách thức của Big Bang migration
- Khả năng rollback dễ dàng
- Xử lý tốt hơn các bất ngờ và vấn đề
- Development team có cơ hội học hỏi từ sai lầm

### 3. Testing và Validation hiệu quả
- Cả monolithic và microservices cùng tồn tại trong quá trình migration
- Traffic có thể được route giữa legacy và hệ thống mới
- Kết quả có thể được so sánh giữa hai component
- Phân phối traffic linh hoạt (ví dụ: chia 50-50%)
- 100% traffic có thể được chuyển hướng về monolithic nếu có vấn đề
- Legacy code vẫn ở trạng thái "chết" nhưng sẵn có nếu cần

## Bốn giai đoạn của Migration

### 1. Identification (Xác định)
- Xác định cần bao nhiêu microservices
- Thực hiện right-sizing của microservices sử dụng phương pháp Domain-Driven Design (DDD)
- Chia nhỏ monolithic application thành các domain riêng biệt

### 2. Transformation (Chuyển đổi)
- Chuyển đổi các component từ legacy sang microservices
- Viết lại các service sử dụng công nghệ mới hơn
- Phát triển và test các microservices riêng lẻ

### 3. Coexistence (Cùng tồn tại)
- Cả monolithic và microservices tồn tại đồng thời
- Giới thiệu **Strangler Facade** để xử lý routing traffic
- Thường được triển khai bằng cách sử dụng **API Gateway**
- Dần dần chuyển traffic từ legacy sang microservices

### 4. Elimination (Loại bỏ)
- Loại bỏ hoàn toàn legacy application
- Tất cả traffic chảy đến microservices/ứng dụng hiện đại
- Legacy system được thay thế hoàn toàn

## Chuẩn bị phỏng vấn

Pattern này thường được hỏi trong các cuộc phỏng vấn. Khi được hỏi: **"Bạn đang migrate legacy của mình sang ứng dụng dựa trên microservice như thế nào?"**

**Trả lời**: Giải thích Strangler Fig Pattern, bao gồm:
- Phương pháp migration dần dần, từng phần một
- Bốn giai đoạn: Identification, Transformation, Coexistence, và Elimination
- Lợi ích của rủi ro tối thiểu và migration từng bước
- Sử dụng API Gateway để routing traffic trong giai đoạn coexistence
- Ví dụ về việc migrate các component từng cái một

## Tóm tắt

Strangler Fig Pattern là phương pháp được khuyến nghị để migrate các legacy system phức tạp sang kiến trúc microservices. Nó cung cấp một con đường an toàn, từng bước cho phép các tổ chức:
- Giảm thiểu rủi ro migration
- Duy trì tính liên tục hoạt động
- Học hỏi và thích ứng trong quá trình
- Test kỹ lưỡng trước khi cam kết hoàn toàn
- Rollback nếu cần thiết

Bằng cách tuân theo pattern này, các development team có thể hiện đại hóa thành công ứng dụng của họ trong khi tránh được các cạm bẫy của Big Bang migrations.