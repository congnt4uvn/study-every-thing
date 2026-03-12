# Tổng Quan Các Mẫu Thiết Kế API Gateway

## Giới Thiệu

Tài liệu này cung cấp cái nhìn tổng quan toàn diện về các mẫu thiết kế (design patterns) liên quan đến API Gateway trong kiến trúc microservices. Những mẫu thiết kế này rất quan trọng để xây dựng hệ thống microservice có khả năng mở rộng, dễ bảo trì và hiệu quả bằng Spring Cloud Gateway.

## 1. Mẫu API Gateway (API Gateway Pattern)

### Tổng Quan
Mẫu API Gateway đề cập đến một thành phần hoạt động như điểm vào duy nhất (single entry point) cho hệ sinh thái microservices của bạn.

### Trách Nhiệm Chính
- **Định tuyến (Routing)**: Điều hướng các yêu cầu từ client đến các microservices backend phù hợp
- **Bảo mật (Security)**: Xử lý xác thực và phân quyền
- **Giao tiếp (Communication)**: Đơn giản hóa giao tiếp giữa clients và services

### Kiến Trúc
```
Ứng Dụng Client (Web/Mobile) → API Gateway → Microservices
```

### Triển Khai
Chúng ta triển khai mẫu này bằng Spring Cloud Gateway, hoạt động như một edge server hoặc điểm vào thống nhất cho tất cả microservices.

### Lợi Ích
- Kiểm soát truy cập tập trung
- Đơn giản hóa giao tiếp từ phía client
- Điểm vào duy nhất cho tất cả các yêu cầu

---

## 2. Mẫu Định Tuyến Gateway (Gateway Routing Pattern)

### Tổng Quan
Mẫu này mô tả một edge server có khả năng định tuyến các yêu cầu từ client đến các microservices backend phù hợp dựa trên nhiều yếu tố khác nhau.

### Các Yếu Tố Định Tuyến
- Đường dẫn URL
- HTTP headers
- Tham số yêu cầu (request parameters)
- Query strings

### Triển Khai với Spring Cloud Gateway
Triển khai của chúng ta định tuyến các yêu cầu dựa trên giá trị URL, đáp ứng yêu cầu của mẫu này.

### Ví Dụ
```
/accounts/** → Microservice Tài Khoản
/loans/** → Microservice Cho Vay
/cards/** → Microservice Thẻ
```

---

## 3. Mẫu Giảm Tải Gateway (Gateway Offloading Pattern)

### Tổng Quan
Mẫu Gateway Offloading liên quan đến việc ủy thác các mối quan tâm xuyên suốt (cross-cutting concerns) từ các microservices riêng lẻ sang API Gateway.

### Các Mối Quan Tâm Xuyên Suốt Cần Giảm Tải
- **Bảo mật (Security)**: Xác thực và phân quyền
- **Bộ nhớ đệm (Caching)**: Lưu cache phản hồi
- **Giới hạn tốc độ (Rate Limiting)**: Kiểm soát lưu lượng yêu cầu
- **Giám sát (Monitoring)**: Ghi log và metrics
- **Kết thúc SSL (SSL Termination)**: Xử lý HTTPS
- **Cân bằng tải (Load Balancing)**: Phân phối yêu cầu

### Những Gì KHÔNG NÊN Giảm Tải
❌ Logic nghiệp vụ (ví dụ: logic quản lý tài khoản)
❌ Xử lý đặc thù domain
❌ Xác thực dữ liệu đặc thù cho quy tắc nghiệp vụ

### Lợi Ích
- Giảm trùng lặp mã nguồn
- Quản lý tập trung các mối quan tâm chung
- Đơn giản hóa việc phát triển microservice

---

## 4. Mẫu Backend For Frontend (BFF)

### Tổng Quan
Mẫu BFF liên quan đến việc tạo nhiều API Gateway, mỗi gateway được tùy chỉnh cho một loại ứng dụng client cụ thể.

### Kiến Trúc
```
Web Client → Web API Gateway → Microservices
Mobile Client → Mobile API Gateway → Microservices
Tablet Client → Tablet API Gateway → Microservices
```

### Các Trường Hợp Sử Dụng

#### Tối Ưu Hóa Phản Hồi
- **Mobile/Tablet**: Phản hồi được nén cho các client nhẹ
- **Web**: Phản hồi đầy đủ chi tiết với hình ảnh và dữ liệu mở rộng

#### Tùy Chỉnh Nội Dung
- **Web**: Thông tin đầy đủ bao gồm hình ảnh, giao dịch chi tiết
- **Mobile**: Thông tin hạn chế, chỉ có tóm tắt, không có hình ảnh
- **Tablet**: Tối ưu cho màn hình kích thước trung bình

### Khi Nào Sử Dụng BFF
- Ứng dụng doanh nghiệp phức tạp
- Các yêu cầu khác nhau từ client
- Cần tối ưu hóa theo từng loại client
- Định dạng dữ liệu thay đổi theo loại client

### Lợi Ích
- Trải nghiệm được tối ưu cho từng loại client
- Hiệu suất tốt hơn cho các thiết bị có tài nguyên hạn chế
- Linh hoạt trong định dạng phản hồi

---

## 5. Mẫu Tổng Hợp Gateway / Mẫu Kết Hợp Gateway (Gateway Aggregation / Gateway Composition Pattern)

### Tổng Quan
Mẫu này liên quan đến việc tổng hợp dữ liệu từ nhiều microservices thành một phản hồi duy nhất tại tầng API Gateway.

### Phát Biểu Vấn Đề
Khi client cần dữ liệu từ nhiều microservices (ví dụ: tóm tắt tài khoản, cho vay và thẻ), có một số cách tiếp cận:

#### ❌ Cách 1: Nhiều Lời Gọi Riêng Lẻ (Không Khuyến Nghị)
```
Client → Microservice Tài Khoản
Client → Microservice Cho Vay
Client → Microservice Thẻ
```
**Vấn đề**: Quá nhiều lưu lượng mạng, tăng độ trễ

#### ✅ Cách 2: Tổng Hợp Giữa Các Service
```
Client → Accounts → [Loans, Cards] → Phản Hồi Kết Hợp
```
**Triển khai**: Một microservice gọi các service khác và kết hợp dữ liệu

#### ✅ Cách 3: Tổng Hợp Gateway (Khuyến Nghị)
```
Client → API Gateway → [Accounts, Loans, Cards] → Phản Hồi Kết Hợp
```

### Ví Dụ Triển Khai
```
GET /api/summary
↓
API Gateway gọi:
  - GET /accounts/summary
  - GET /loans/summary
  - GET /cards/summary
↓
Kết hợp tất cả phản hồi
↓
Trả về phản hồi tổng hợp duy nhất
```

### Lợi Ích
- Yêu cầu đơn từ góc độ client
- Giảm chi phí mạng
- Logic tổng hợp dữ liệu tập trung
- Hiệu suất tốt hơn

---

## Tóm Tắt

### Bảng Tham Chiếu Nhanh Các Mẫu

| Mẫu | Mục Đích | Đặc Điểm Chính |
|---------|---------|-------------|
| **API Gateway** | Điểm vào duy nhất | Truy cập tập trung vào microservices |
| **Gateway Routing** | Định tuyến thông minh | Định tuyến dựa trên URL, headers, parameters |
| **Gateway Offloading** | Tập trung các mối quan tâm | Xử lý bảo mật, caching, monitoring |
| **Backend For Frontend** | Gateway riêng cho từng client | Tối ưu cho từng loại client |
| **Gateway Aggregation** | Kết hợp dữ liệu | Kết hợp dữ liệu từ nhiều services |

### Những Điểm Chính Cần Nhớ

1. **Mẫu API Gateway**: Nền tảng cho tất cả các mẫu khác - cung cấp điểm vào thống nhất
2. **Mẫu Gateway Routing**: Cần thiết để điều hướng lưu lượng đến đúng microservices
3. **Mẫu Gateway Offloading**: Giảm độ phức tạp của microservice bằng cách tập trung các mối quan tâm xuyên suốt
4. **Mẫu BFF**: Giải quyết các yêu cầu đặc thù của client trong ứng dụng phức tạp
5. **Mẫu Gateway Aggregation**: Tối ưu giao tiếp client-server bằng cách giảm số lượt đi về

### Thực Hành Tốt Nhất

- ✅ Triển khai API Gateway làm điểm vào của bạn
- ✅ Sử dụng định tuyến dựa trên các mẫu URL rõ ràng
- ✅ Giảm tải các mối quan tâm xuyên suốt sang gateway
- ✅ Cân nhắc BFF cho các yêu cầu client đa dạng
- ✅ Sử dụng aggregation để giảm độ phức tạp phía client
- ❌ Không giảm tải logic nghiệp vụ sang gateway
- ❌ Không tạo độ phức tạp không cần thiết với nhiều gateway trừ khi thực sự cần

---

## Kết Luận

Hiểu các mẫu thiết kế API Gateway này rất quan trọng cho:
- Phỏng vấn kiến trúc microservice
- Thiết kế hệ thống có khả năng mở rộng
- Đưa ra quyết định kiến trúc sáng suốt
- Triển khai các mẫu giao tiếp hiệu quả

Những mẫu này hoạt động cùng nhau để tạo ra một kiến trúc microservices mạnh mẽ, có khả năng mở rộng và dễ bảo trì bằng Spring Cloud Gateway.

---

*Tài liệu này dựa trên các nguyên tắc kiến trúc microservices và triển khai Spring Cloud Gateway.*