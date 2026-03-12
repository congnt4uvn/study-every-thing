# Thách Thức Giao Tiếp Nội Bộ Giữa Các Microservices

## Giới Thiệu

Trong phần này, chúng ta sẽ khám phá các thách thức phát sinh khi xây dựng ứng dụng microservices, đặc biệt tập trung vào các mô hình giao tiếp nội bộ giữa các dịch vụ. Trước khi đi sâu vào các thách thức, điều quan trọng là phải hiểu các khái niệm và thuật ngữ chính trong kiến trúc microservices.

## Kiến Trúc Mạng Microservices

### Thiết Lập Microservices Hiện Tại

Mạng microservices của chúng ta hiện bao gồm ba microservices xử lý logic nghiệp vụ:

1. **Accounts Microservice** - Xử lý các thao tác liên quan đến tài khoản
2. **Loans Microservice** - Quản lý các thao tác về khoản vay
3. **Cards Microservice** - Xử lý các giao dịch liên quan đến thẻ

Các microservices này chịu trách nhiệm:
- Lưu trữ dữ liệu
- Truy xuất dữ liệu
- Xử lý các yêu cầu và thực thi logic nghiệp vụ
- Gửi các phản hồi phù hợp

## Mô Hình Giao Tiếp Bên Ngoài

### Mô Hình API Gateway

Trong các ứng dụng microservices triển khai thực tế, các dịch vụ không được phép truy cập trực tiếp từ các client bên ngoài. Thay vào đó, chúng ta tuân theo mô hình giao tiếp an toàn:

- Tất cả microservices được triển khai trong một **mạng microservices** (microservice network)
- Một **tường lửa** (firewall) bao quanh mạng microservices
- Các client bên ngoài (C1, C2, C3, v.v.) phải vào qua một **điểm vào duy nhất**
- Điểm vào này được gọi là **API Gateway** (hoặc Gateway)

### Lợi Ích Của API Gateway

API Gateway đóng vai trò là điểm vào duy nhất cho lưu lượng bên ngoài và cung cấp:

- **Kiểm tra bảo mật** - Xác thực và phân quyền
- **Kiểm toán** - Theo dõi và giám sát yêu cầu
- **Ghi log** - Ghi log tập trung cho tất cả các yêu cầu bên ngoài
- **Các yêu cầu phi chức năng** - Xử lý các vấn đề xuyên suốt

### Luồng Lưu Lượng Bên Ngoài

```
Client Bên Ngoài (C1, C2, C3)
        ↓
   API Gateway
        ↓
Mạng Microservices
    (Accounts, Loans, Cards)
```

Tất cả các yêu cầu từ client bên ngoài đều đi qua API Gateway trước khi đến bất kỳ microservice nào. Lưu lượng này được gọi là **lưu lượng bên ngoài** (external traffic) hoặc **giao tiếp bên ngoài** (external communication).

## Mô Hình Giao Tiếp Nội Bộ

### Giao Tiếp Giữa Các Dịch Vụ

Trong mạng microservices, các dịch vụ thường cần giao tiếp với nhau. Ví dụ:

**Kịch bản**: Một yêu cầu từ bên ngoài đến Accounts microservice thông qua API Gateway. Để hoàn thành phản hồi, Accounts microservice có thể cần:

1. Kết nối với **Loans microservice** để lấy thông tin khoản vay
2. Kết nối với **Cards microservice** để truy xuất chi tiết thẻ

Loại giao tiếp giữa các dịch vụ trong mạng microservices này được gọi là **giao tiếp nội bộ** (internal communication) hoặc **lưu lượng nội bộ** (internal traffic).

### Các Loại Giao Tiếp

| Loại Giao Tiếp | Mô Tả | Phạm Vi |
|----------------|-------|---------|
| **Giao Tiếp Bên Ngoài** | Lưu lượng từ client bên ngoài qua API Gateway | Bên ngoài → Bên trong mạng |
| **Giao Tiếp Nội Bộ** | Giao tiếp giữa các dịch vụ trong mạng | Chỉ bên trong mạng |

## Trọng Tâm Của Phần Này

Phần này đề cập cụ thể đến:

- **Trọng tâm chính**: Các thách thức giao tiếp nội bộ giữa các microservices
- **Nội dung**: Các thách thức phát sinh khi microservices giao tiếp với nhau
- **Giải pháp**: Cách khắc phục các thách thức giao tiếp nội bộ

**Lưu ý**: API Gateway và các mô hình lưu lượng bên ngoài sẽ được đề cập trong các phần tiếp theo.

## Điểm Chính Cần Nhớ

1. Microservices không bao giờ nên được truy cập trực tiếp từ các client bên ngoài
2. API Gateway cung cấp một điểm vào duy nhất, an toàn cho tất cả lưu lượng bên ngoài
3. Giao tiếp nội bộ giữa các microservices cần được xem xét cẩn thận
4. Hiểu sự khác biệt giữa lưu lượng bên ngoài và nội bộ là rất quan trọng
5. Cả hai mô hình giao tiếp đều có những thách thức riêng cần được giải quyết

## Nội Dung Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Các thách thức cụ thể trong giao tiếp nội bộ microservices
- Các giải pháp và best practices cho giao tiếp giữa các dịch vụ
- Chiến lược triển khai sử dụng Spring Boot và Java
- Các mô hình API Gateway (sẽ được đề cập trong các phần sau)

---

*Tài liệu này là một phần của khóa học toàn diện về kiến trúc microservices tập trung vào triển khai với Java Spring Boot.*