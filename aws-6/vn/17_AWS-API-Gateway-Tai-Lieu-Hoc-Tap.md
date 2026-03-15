# AWS API Gateway - Tài Liệu Học Tập

## Tổng Quan
Tài liệu này bao gồm các loại API khác nhau có sẵn trong AWS API Gateway và sự khác biệt chính giữa chúng.

## Các Loại API trong API Gateway

### 1. REST API
REST API là tùy chọn có nhiều tính năng nhất trong API Gateway với khả năng toàn diện:

**Tính Năng Chính:**
- Khả năng ánh xạ dữ liệu đầy đủ
- Hỗ trợ resource policies (chính sách tài nguyên)
- Usage plans (kế hoạch sử dụng) và API keys
- Nhiều phương thức ủy quyền
- Biến giai đoạn (stage variables)
- Chuyển đổi request/response
- Hỗ trợ caching
- Giám sát và ghi log toàn diện

**Các Tùy Chọn Ủy Quyền:**
- IAM roles và policies
- Amazon Cognito User Pools
- Lambda Authorizers (Custom Authorizers)
- Resource policies

**Các Trường Hợp Sử Dụng:**
- Ứng dụng doanh nghiệp yêu cầu tính năng nâng cao
- Ứng dụng cần kiểm soát truy cập chi tiết
- Hệ thống yêu cầu usage plans và API quotas

### 2. HTTP API
HTTP API là giải pháp thay thế mới hơn, đơn giản hơn và tiết kiệm chi phí hơn so với REST API:

**Tính Năng Chính:**
- Độ trễ thấp
- Tiết kiệm chi phí (rẻ hơn nhiều so với REST API)
- AWS Lambda proxy
- HTTP proxy API
- Tích hợp riêng tư (private integration)
- Hỗ trợ CORS tích hợp sẵn
- Chỉ proxy (không có ánh xạ dữ liệu)

**Các Tùy Chọn Ủy Quyền:**
- OIDC (OpenID Connect)
- OAuth 2.0

**Hạn Chế:**
- Không có usage plans hoặc API keys
- Không có resource policies
- Khả năng chuyển đổi dữ liệu hạn chế

**Các Trường Hợp Sử Dụng:**
- API proxy đơn giản
- Ứng dụng nhạy cảm về chi phí
- Yêu cầu xác thực hiện đại (OAuth 2.0, OIDC)

### 3. WebSocket API
WebSocket API cho phép giao tiếp hai chiều giữa clients và servers:

**Tính Năng Chính:**
- Giao tiếp hai chiều theo thời gian thực
- Kết nối liên tục
- Kiến trúc hướng sự kiện

**Các Trường Hợp Sử Dụng:**
- Ứng dụng chat
- Bảng điều khiển theo thời gian thực
- Thông báo trực tiếp
- Ứng dụng game

## Sự Khác Biệt Chính: HTTP API vs REST API

| Tính Năng | HTTP API | REST API |
|-----------|----------|----------|
| **Chi Phí** | Rẻ hơn nhiều | Đắt hơn |
| **Ánh Xạ Dữ Liệu** | Không hỗ trợ (chỉ proxy) | Hỗ trợ đầy đủ |
| **Ủy Quyền** | OIDC, OAuth 2.0 | IAM, Cognito, Lambda Auth, Resource Policies |
| **Usage Plans/API Keys** | Không hỗ trợ | Được hỗ trợ |
| **CORS** | Hỗ trợ tích hợp sẵn | Cấu hình thủ công |
| **Resource Policies** | Không hỗ trợ | Được hỗ trợ |
| **Độ Trễ** | Thấp hơn | Tiêu chuẩn |

## Mẹo Ôn Thi

1. **HTTP API rẻ hơn** REST API - hãy nhớ sự khác biệt chính này
2. **REST API hỗ trợ resource policies**, HTTP API thì không
3. HTTP API tốt nhất cho **các trường hợp sử dụng proxy đơn giản** với xác thực hiện đại
4. REST API tốt nhất cho **các kịch bản doanh nghiệp phức tạp** yêu cầu tính năng nâng cao
5. WebSocket API dành cho **giao tiếp hai chiều theo thời gian thực**

## Khi Nào Chọn API Nào?

### Chọn REST API khi bạn cần:
- Resource policies
- Usage plans và API keys
- Chuyển đổi dữ liệu nâng cao
- Xác thực request/response
- Caching
- Tích hợp IAM đầy đủ

### Chọn HTTP API khi bạn cần:
- Giải pháp chi phí thấp hơn
- Chức năng proxy đơn giản
- Xác thực OAuth 2.0 hoặc OIDC
- CORS tích hợp sẵn
- Yêu cầu độ trễ thấp

### Chọn WebSocket API khi bạn cần:
- Giao tiếp hai chiều theo thời gian thực
- Kết nối liên tục
- Tương tác hướng sự kiện

---

**Lưu Ý:** Tài liệu học tập này dựa trên các tính năng của AWS API Gateway. Luôn tham khảo tài liệu AWS mới nhất để có thông tin cập nhật nhất.
