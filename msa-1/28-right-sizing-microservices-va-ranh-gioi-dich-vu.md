# Right-Sizing Microservices và Ranh Giới Dịch Vụ

## Giới Thiệu

Trong bài học này, chúng ta sẽ khám phá cách định kích thước phù hợp cho microservices và xác định ranh giới dịch vụ thích hợp thông qua ví dụ thực tế về ứng dụng ngân hàng. Chúng ta sẽ phân tích ba phương pháp khác nhau được đề xuất bởi các nhóm khác nhau và xác định chiến lược sizing nào hiệu quả nhất.

## Tình Huống

Một ứng dụng ngân hàng cần di chuyển hoặc được xây dựng dựa trên kiến trúc microservices. CEO/CTO thành lập ba nhóm khác nhau để phân tích và đề xuất chiến lược sizing microservices của riêng họ.

Các nhóm đã sử dụng các phương pháp như:
- Domain-Driven Sizing (Định kích thước theo miền nghiệp vụ)
- Event-Driven Sizing (Định kích thước theo sự kiện)

## Các Đề Xuất Của Các Nhóm

### Phương Án Nhóm 1: 2 Microservices

**Cấu trúc:**
1. **Accounts Microservice** - Kết hợp:
   - Chức năng Tài khoản Tiết kiệm
   - Chức năng Tài khoản Giao dịch

2. **Cards & Loans Microservice** - Kết hợp:
   - Quản lý Thẻ
   - Quản lý Khoản vay

**Phân tích:**
- ❌ **Không được khuyến nghị** - Tạo ra sự liên kết chặt chẽ
- Thẻ và Khoản vay được gộp chung
- Tài khoản Tiết kiệm và Tài khoản Giao dịch được gộp chung
- Các cải tiến trong tương lai của một nhóm (ví dụ: Thẻ) sẽ ảnh hưởng đến nhóm khác (ví dụ: Khoản vay)
- Thiếu tính linh hoạt cho sự phát triển độc lập

### Phương Án Nhóm 2: 4 Microservices ✅

**Cấu trúc:**
1. **Saving Account Microservice** (Microservice Tài khoản Tiết kiệm)
2. **Trading Account Microservice** (Microservice Tài khoản Giao dịch)
3. **Cards Microservice** (Microservice Thẻ)
4. **Loans Microservice** (Microservice Khoản vay)

**Phân tích:**
- ✅ **Hợp lý nhất và được Khuyến nghị**
- Mỗi miền nghiệp vụ là một microservice độc lập
- Cung cấp sự liên kết lỏng lẻo giữa các dịch vụ
- Mang lại tính linh hoạt cho các nhóm khác nhau có chu trình cải tiến riêng
- Các nhóm có thể chọn ngôn ngữ lập trình và cơ sở dữ liệu riêng
- Lựa chọn an toàn hơn cho yêu cầu hiện tại

### Phương Án Nhóm 3: 7+ Microservices

**Cấu trúc:**
1. **Saving Account Microservice** (Microservice Tài khoản Tiết kiệm)
2. **Trading Account Microservice** (Microservice Tài khoản Giao dịch)
3. **Debit Card Microservice** (Microservice Thẻ Ghi nợ)
4. **Credit Card Microservice** (Microservice Thẻ Tín dụng)
5. **Home Loan Microservice** (Microservice Vay mua Nhà)
6. **Vehicle Loan Microservice** (Microservice Vay mua Xe)
7. **Personal Loan Microservice** (Microservice Vay Cá nhân)

**Phân tích:**
- ⚠️ **Quá Chi tiết** - Chỉ hợp lý khi có sự khác biệt về chức năng đáng kể
- Chỉ có ý nghĩa nếu có sự khác biệt chức năng lớn giữa:
  - Thẻ ghi nợ vs. Thẻ tín dụng
  - Vay mua nhà vs. Vay mua xe vs. Vay cá nhân
- Nếu chức năng tương tự, điều này tạo ra:
  - Quá nhiều microservices
  - Chi phí vận hành cao
  - Độ phức tạp không cần thiết

## Tiêu Chí Quyết Định

Khi chọn kích thước microservices, hãy xem xét:

1. **Phân tách Miền Nghiệp vụ**: Mỗi microservice nên đại diện cho một miền nghiệp vụ riêng biệt
2. **Liên kết Lỏng lẻo**: Các dịch vụ nên độc lập và liên kết lỏng lẻo
3. **Tính Tự chủ của Nhóm**: Các nhóm khác nhau nên có khả năng cải tiến dịch vụ của họ một cách độc lập
4. **Chi phí Vận hành**: Tránh tạo quá nhiều dịch vụ làm tăng độ phức tạp quản lý
5. **Sự Khác biệt về Chức năng**: Chỉ tách dịch vụ khi có sự khác biệt đáng kể về logic nghiệp vụ

## Phương Án Chiến Thắng

**Phương án của Nhóm 2 được lựa chọn** vì:

- Hiện tại không có logic nghiệp vụ riêng biệt để phân biệt giữa:
  - Thẻ ghi nợ vs. Thẻ tín dụng
  - Vay mua nhà vs. Vay mua xe vs. Vay cá nhân
- Những khác biệt nhỏ có thể được xử lý thông qua:
  - Các cột trong cơ sở dữ liệu
  - Cấu hình
  - Các phương pháp khác cho những khác biệt logic nghiệp vụ nhỏ
- Cung cấp sự cân bằng tốt giữa tách biệt các mối quan tâm và sự đơn giản trong vận hành

## Những Điểm Chính Cần Nhớ

1. **Không có Sizing Hoàn hảo ngay từ Ngày Đầu**: Không có kích thước "đúng" phổ quát cho microservices ban đầu
2. **Phát triển Liên tục**: Các tổ chức nên liên tục đánh giá và định kích thước lại microservices của họ
3. **Quá trình Học hỏi**: Các công ty học hỏi từ việc triển khai microservices và điều chỉnh ranh giới cho phù hợp
4. **Linh hoạt cho Tương lai**: Nếu có vấn đề phát sinh (ví dụ: Cards microservice trở nên quá phức tạp), bạn có thể tách nó sau thành Debit Card và Credit Card microservices
5. **Sự Tham gia của Các Bên liên quan**: Các thay đổi sizing lớn nên được thảo luận với tất cả các bên liên quan
6. **Tránh Over-Engineering**: Đừng tạo microservices riêng biệt cho những khác biệt logic nghiệp vụ nhỏ

## Thực Hành Tốt Nhất

- Bắt đầu với phương pháp sizing an toàn, vừa phải
- Giám sát độ phức tạp của dịch vụ và tính tự chủ của nhóm
- Sẵn sàng tách hoặc hợp nhất các dịch vụ dựa trên kinh nghiệm thực tế
- Cân bằng giữa quá ít (liên kết chặt chẽ) và quá nhiều (chi phí vận hành) microservices
- Xem xét khả năng tách biệt cơ sở dữ liệu
- Đánh giá yêu cầu về chu trình cải tiến của nhóm

## Kết Luận

Right-sizing microservices là một quá trình lặp đi lặp lại. Bắt đầu với một phương pháp hợp lý cung cấp sự liên kết lỏng lẻo và tính tự chủ của nhóm, sau đó điều chỉnh dựa trên kinh nghiệm và yêu cầu thực tế. Mục tiêu không phải là đạt được sizing hoàn hảo ngay từ ngày đầu tiên, mà là tạo ra một kiến trúc linh hoạt có thể phát triển cùng với nhu cầu của tổ chức bạn.