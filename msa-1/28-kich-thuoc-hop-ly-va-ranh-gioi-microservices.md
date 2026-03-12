# Kích Thước Hợp Lý và Ranh Giới Microservices

## Giới Thiệu

Sau khi xây dựng ba microservices khác nhau (Accounts, Loans và Cards) với REST APIs, chúng ta đối mặt với một thách thức quan trọng khác trong kiến trúc microservices: **Thách thức 2 - Làm thế nào để xác định kích thước hợp lý và ranh giới dịch vụ của Microservices**.

## Phép So Sánh với Kích Cỡ Áo

### Hiểu về Tầm Quan Trọng của Kích Thước

Giống như việc chọn kích cỡ áo phù hợp là rất quan trọng để thoải mái và đẹp mắt, việc xác định kích thước hợp lý cho microservices cũng cần thiết cho một kiến trúc thành công:

- **Small (S)** → Quá nhỏ đối với một số người
- **Medium (M)** → Vừa vặn tiêu chuẩn
- **Large (L)** → Thoải mái cho người có vóc dáng lớn hơn
- **Extra Large (XL)** → Phù hợp với kích cỡ lớn hơn
- **Double Extra Large (XXL)** → Kích cỡ tối đa

### Vấn Đề với Kích Thước Không Phù Hợp

**Mặc Sai Kích Cỡ:**
- Người mặc M nhưng mặc XXL: xấu hổ, rộng thùng thình, không thoải mái
- Người mặc XL nhưng mặc S: chật, hạn chế, không thể di chuyển đúng cách

**Tương tự, trong Agile/Scrum:**
- User stories được định kích thước bằng cách sử dụng kích cỡ áo dựa trên độ phức tạp
- Nguyên tắc tương tự áp dụng cho microservices

## Thách Thức 2: Xác Định Kích Thước Hợp Lý cho Microservices

### Kích Thước Hợp Lý là Gì?

Kích thước hợp lý là khía cạnh thách thức nhất khi xây dựng một hệ thống microservice thành công. Nó bao gồm:

1. **Không Quá Lớn**: Microservices không nên quá lớn đến mức bạn mất đi các lợi ích của kiến trúc microservices
2. **Không Quá Nhỏ**: Microservices không nên quá nhỏ đến mức thiếu logic nghiệp vụ đầy đủ
3. **Cân Bằng**: Tìm điểm tối ưu giảm thiểu chi phí vận hành trong khi tối đa hóa lợi ích

### Tại Sao Kích Thước Hợp Lý Quan Trọng?

**Vấn Đề với Kích Thước Không Hợp Lý:**

**Quá Nhiều Microservices Nhỏ:**
- Tăng chi phí vận hành
- Kết nối phức tạp
- Quản lý giao tiếp khó khăn
- Nhiều hạ tầng cần bảo trì hơn

**Quá Ít Microservices Lớn:**
- Mất lợi ích của microservices
- Giảm tính linh hoạt
- Khó scale độc lập
- Triển khai phức tạp hơn

### Các Bên Liên Quan Chịu Trách Nhiệm

- Kiến trúc sư (Architects)
- Lập trình viên (Developers)
- Trưởng nhóm kỹ thuật (Technical Leads)
- Quản lý (Managers)

## Hai Phương Pháp Phổ Biến để Xác Định Kích Thước Hợp Lý

### 1. Định Kích Thước Theo Lĩnh Vực (Domain-Driven Sizing - DDS)

#### Tổng Quan

Xác định kích thước và ranh giới cho microservices phù hợp chặt chẽ với các lĩnh vực nghiệp vụ và khả năng kinh doanh.

#### Ví Dụ: Ứng Dụng EasyBank

**Các Lĩnh Vực (Phòng ban/Mảng kinh doanh):**
- Tài khoản (Accounts)
- Thẻ (Cards)
- Vay (Loans)
- (Các lĩnh vực khác...)

**Cách Hoạt Động:**

Xây dựng microservices dựa trên các lĩnh vực nghiệp vụ này. Ví dụ:
- Accounts Microservice
- Cards Microservice
- Loans Microservice

#### Khi Nào Không Nên Sử Dụng Nghiêm Ngặt

**Tránh định kích thước nghiêm ngặt theo lĩnh vực khi:**
- Một lĩnh vực rất lớn
- Một lĩnh vực duy nhất xử lý nhiều sản phẩm
- Hàng trăm lập trình viên làm việc trên một lĩnh vực
- Các hoạt động kinh doanh phức tạp trong một lĩnh vực

#### Quy Trình

**Bước 1: Thu Thập Kiến Thức Lĩnh Vực**
- Trò chuyện với các chuyên gia lĩnh vực
- Tham vấn các lãnh đạo kinh doanh
- Liên quan các chuyên gia kỹ thuật
- Gặp gỡ khách hàng, phân tích viên kinh doanh và chủ sản phẩm
- Phỏng vấn nhân viên có kinh nghiệm (những người làm việc hàng thập kỷ)

**Bước 2: Thu Thập Thông Tin (3-6 tháng)**
- Các hoạt động được xử lý bởi mỗi lĩnh vực
- Quy mô nhóm
- Các ứng dụng hiện có
- Quy trình kinh doanh
- Hoạt động hàng ngày

**Bước 3: Các Phiên Brainstorming**
- Liên quan tất cả các bên liên quan:
  - Người kinh doanh
  - Người kỹ thuật
  - Khách hàng
  - Chủ sản phẩm
  - Chuyên gia lĩnh vực

**Bước 4: Xác Định Kích Thước Hợp Lý**
- Dựa trên thông tin đã thu thập
- Sự đồng thuận giữa các bên liên quan
- Phương pháp lặp lại

#### Tinh Chỉnh Liên Tục

Các tổ chức thường:
1. Bắt đầu với các giả định và kích thước ban đầu
2. Bắt đầu phát triển và triển khai
3. Theo dõi chi phí vận hành
4. Xem xét lại và tinh chỉnh kích thước khi cần
5. Hoặc **tách** các microservices lớn hoặc **gộp** các microservices nhỏ lại với nhau

#### Ưu Điểm
- Hiểu biết sâu về lĩnh vực
- Quyết định có thông tin đầy đủ
- Phù hợp với khả năng kinh doanh

#### Nhược Điểm
- **Tốn thời gian** (tối thiểu 3-6 tháng)
- Yêu cầu chuyên gia có kiến thức sâu về kinh doanh và lĩnh vực
- Cần phối hợp nhiều bên liên quan

---

### 2. Định Kích Thước Theo Event-Storming (Event-Storming Sizing - ESS)

#### Tổng Quan

Một người điều phối tiến hành các phiên tương tác với các bên liên quan sử dụng giấy note dính để xác định các sự kiện, lệnh và phản ứng.

#### Người Tham Gia

- Chủ sản phẩm (Product owners)
- Lập trình viên (Developers)
- Kiểm thử viên (Testers)
- Khách hàng (Clients)
- Chủ doanh nghiệp (Business owners)
- Lãnh đạo kinh doanh (Business leaders)

#### Quy Trình

**Bước 1: Xác Định Sự Kiện**

Mỗi người tham gia sử dụng giấy note dính để viết các sự kiện có thể xảy ra trong kinh doanh.

**Ví Dụ Sự Kiện trong Ngân Hàng:**
- Khách hàng hoàn tất thanh toán
- Khách hàng tìm kiếm sản phẩm
- Tài khoản được tạo
- Đơn xin vay được gửi

**Bước 2: Xác Định Lệnh (Commands)**

Lệnh là các quy trình khởi tạo sự kiện.

**Ví Dụ:**
- **Sự kiện**: Thanh toán hoàn tất
- **Lệnh**: Khách hàng nhấp nút "Thanh toán"

**Bước 3: Xác Định Phản Ứng (Reactions)**

Phản ứng là kết quả của các sự kiện.

**Ví Dụ:**
- **Sự kiện**: Thanh toán hoàn tất
- **Phản ứng**: Số tiền được khấu trừ từ tài khoản

**Lưu ý**: Một phản ứng đôi khi có thể đóng vai trò là lệnh cho sự kiện tiếp theo.

**Bước 4: Phân Loại Theo Lĩnh Vực**

Nhóm các sự kiện, lệnh và phản ứng theo lĩnh vực:
- **Lĩnh vực Cards**: Tất cả sự kiện, lệnh, phản ứng liên quan đến thẻ
- **Lĩnh vực Loans**: Tất cả sự kiện, lệnh, phản ứng liên quan đến vay
- **Lĩnh vực Accounts**: Tất cả sự kiện, lệnh, phản ứng liên quan đến tài khoản

#### Ưu Điểm

✅ **Nhanh**: Hoàn thành trong 5-6 cuộc họp trong một tháng
✅ **Không cần chuyên gia**: Bất kỳ ai sử dụng hoặc kiểm thử sản phẩm đều có thể tham gia
✅ **Tương tác và hấp dẫn**: Các phiên vui vẻ với nhiều bên liên quan
✅ **Toàn diện**: Thu thập nhiều thông tin nhanh chóng
✅ **Hiệu quả**: Hiệu quả hơn so với Định kích thước theo Lĩnh vực
✅ **Đơn giản**: Quy trình và kết quả rõ ràng

#### Các Bước Triển Khai (từ Blog Lucidchart)

**Bước 1**: Mời đúng người
- Khách hàng
- Lập trình viên
- Kiểm thử viên
- Quản lý
- Kiến trúc sư
- Lãnh đạo kinh doanh

**Bước 2**: Cung cấp không gian mô hình hóa không giới hạn
- Sử dụng giấy note dính hoặc công cụ số (ví dụ: Lucidchart)
- Cho các bên liên quan tự do đề cập đến bất kỳ số lượng sự kiện nào
- Cho phép trùng lặp (người điều phối sẽ loại bỏ chúng sau)

**Bước 3**: Xác định lệnh cho mỗi sự kiện lĩnh vực

**Bước 4**: Xác định phản ứng
- Xem xét phản ứng dây chuyền
- Phản ứng có thể kích hoạt sự kiện mới

**Bước 5**: Phân loại theo lĩnh vực
- Lĩnh vực kinh doanh
- Tạo sản phẩm
- Bán hàng
- Kiểm thử
- Các lĩnh vực tổ chức khác

**Bước 6**: Sử dụng các sự kiện đã phân loại làm đầu vào cho việc định kích thước microservice

#### Tài Nguyên

**Blog Lucidchart**: Chứa hướng dẫn chi tiết về việc điều phối các phiên event-storming
- Hữu ích cho lập trình viên để hiểu quy trình
- Hữu ích cho chuẩn bị phỏng vấn
- Tài liệu tham khảo cho triển khai thực tế
- Mất khoảng 10 phút để đọc

## So Sánh: Định Kích Thước Theo Lĩnh Vực vs Event-Storming

| Khía Cạnh | Định Kích Thước Theo Lĩnh Vực | Định Kích Thước Event-Storming |
|-----------|-------------------------------|-------------------------------|
| **Thời Gian Yêu Cầu** | 3-6 tháng | 1 tháng (5-6 cuộc họp) |
| **Chuyên Môn Cần Thiết** | Cao (cần chuyên gia lĩnh vực) | Thấp (ai cũng có thể tham gia) |
| **Tốc Độ** | Chậm | Nhanh |
| **Sự Tham Gia** | Hạn chế bên liên quan | Tất cả bên liên quan |
| **Hiệu Quả** | Phụ thuộc vào chuyên gia | Rất hiệu quả |
| **Quy Trình** | Tuần tự, chính thức | Tương tác, vui vẻ |
| **Tính Linh Hoạt** | Ít linh hoạt hơn | Linh hoạt hơn |

## Những Điểm Chính Cần Nhớ

1. **Kích thước hợp lý là quan trọng**: Đây là nền tảng của kiến trúc microservices thành công
2. **Cân bằng là chìa khóa**: Tránh các cực đoan (quá lớn hoặc quá nhỏ)
3. **Quy trình liên tục**: Kích thước nên được xem xét lại và tinh chỉnh theo thời gian
4. **Sự tham gia của các bên liên quan**: Bao gồm các quan điểm đa dạng cho quyết định tốt hơn
5. **Chọn phương pháp phù hợp**: Chọn Định kích thước theo Lĩnh vực hoặc Event-Storming dựa trên nhu cầu tổ chức của bạn
6. **Chi phí vận hành quan trọng**: Xem xét chi phí bảo trì và giao tiếp

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ áp dụng các nguyên tắc kích thước hợp lý này vào ví dụ EasyBank để thấy triển khai thực tế và làm rõ hơn các khái niệm.

## Tài Liệu Tham Khảo

- Blog Lucidchart về Event Storming
- Tài liệu GitHub README (sẽ được cập nhật với các liên kết)
- Ví dụ ứng dụng EasyBank

---

*Tài liệu này là một phần của khóa học Microservices với Spring Boot.*