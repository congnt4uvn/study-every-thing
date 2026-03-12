# Giới thiệu về Amazon S3

## Tổng quan

Chào mừng bạn đến với phần học về Amazon S3. Phần này rất quan trọng vì Amazon S3 là một trong những khối xây dựng chính của AWS và được quảng cáo là dịch vụ lưu trữ có khả năng mở rộng vô hạn.

Trên thực tế, rất nhiều trang web phụ thuộc vào Amazon S3. Ví dụ, nhiều website sử dụng Amazon S3 làm nền tảng và nhiều dịch vụ AWS cũng sử dụng Amazon S3 để tích hợp.

Trong phần này, chúng ta sẽ có cách tiếp cận từng bước với Amazon S3 để tìm hiểu các tính năng chính.

## Các trường hợp sử dụng

Có rất nhiều trường hợp sử dụng cho Amazon S3 vì về cốt lõi nó là dịch vụ lưu trữ. S3 được sử dụng cho:

- **Sao lưu và Lưu trữ** - Cho các tệp tin, đĩa của bạn, v.v.
- **Khôi phục thảm họa** - Di chuyển dữ liệu của bạn sang một region khác. Trong trường hợp một region gặp sự cố, dữ liệu của bạn được sao lưu ở nơi khác
- **Lưu trữ** - Lưu trữ các tệp tin trong Amazon S3 và truy xuất nó vào giai đoạn sau với chi phí rẻ hơn nhiều
- **Lưu trữ đám mây kết hợp** - Trong trường hợp bạn có lưu trữ tại chỗ nhưng muốn mở rộng nó lên đám mây
- **Lưu trữ ứng dụng** - Lưu trữ các ứng dụng và phương tiện như tệp video, hình ảnh, v.v.
- **Data Lake** - Lưu trữ nhiều dữ liệu và thực hiện phân tích dữ liệu lớn
- **Cập nhật phần mềm** - Cung cấp các bản cập nhật phần mềm
- **Website tĩnh** - Lưu trữ các website tĩnh

### Ví dụ thực tế

- **Nasdaq** lưu trữ bảy năm dữ liệu vào dịch vụ S3 Glacier, đây là dịch vụ lưu trữ của Amazon S3
- **Sysco** chạy phân tích trên dữ liệu của mình và thu được thông tin chi tiết về kinh doanh từ Amazon S3

## S3 Buckets

Amazon S3 lưu trữ các tệp tin vào **buckets**. Buckets có thể được xem như các thư mục cấp cao nhất.

### Đặc điểm chính

- Các tệp tin trong S3 buckets được gọi là **objects** (đối tượng)
- Buckets được tạo trong tài khoản của bạn và phải có **tên duy nhất toàn cầu**
- Tên phải là duy nhất trên tất cả các region, tất cả các tài khoản tồn tại trên AWS
- Buckets được định nghĩa ở **cấp độ region**
- S3 trông giống như một dịch vụ toàn cầu, nhưng buckets thực sự được tạo trong một AWS region cụ thể

### Quy ước đặt tên

Tên bucket phải tuân theo các quy tắc sau:

- Không có chữ hoa
- Không có dấu gạch dưới
- Phải dài từ 3 đến 63 ký tự
- Không được là địa chỉ IP
- Phải bắt đầu bằng chữ thường hoặc số thường
- Sử dụng chữ cái, số và dấu gạch ngang

## S3 Objects

Objects là các tệp tin có cái gọi là **key** (khóa).

### Object Keys

Khóa đối tượng Amazon S3 là **đường dẫn đầy đủ** của tệp tin của bạn.

**Ví dụ:**

- Tệp đơn giản: `my_file.txt`
- Tệp lồng nhau: `my_folder_1/another_folder/my_file.txt`

Key được tạo thành từ:
- **Prefix** (tiền tố): `my_folder_1/another_folder`
- **Object name** (tên đối tượng): `my_file.txt`

### Khái niệm quan trọng

Amazon S3 không có khái niệm thư mục như vậy, mặc dù khi bạn nhìn vào console, giao diện người dùng sẽ khiến bạn nghĩ ngược lại và bạn thực sự sẽ tạo các thư mục. Nhưng bất cứ thứ gì trong Amazon S3 thực sự đều là một **key**. Keys chỉ là những tên rất dài chứa dấu gạch chéo và được tạo thành từ prefix và object name.

### Thuộc tính của Object

**Giá trị Object:**
- Nội dung của phần thân
- Bạn có thể tải lên bất kỳ tệp nào vào Amazon S3
- Kích thước đối tượng tối đa: **5 terabytes** (5.000 gigabytes)
- Nếu tải lên tệp lớn hơn 5 gigabytes, bạn phải sử dụng **multi-part upload** (tải lên nhiều phần)

**Thuộc tính bổ sung:**

- **Metadata** - Danh sách các cặp key-value có thể được đặt bởi hệ thống hoặc người dùng để chỉ ra một số yếu tố về tệp tin
- **Tags** (thẻ) - Các cặp key-value Unicode (tối đa 10), hữu ích cho bảo mật và quản lý vòng đời
- **Version ID** - Nếu bạn đã bật tính năng versioning (phiên bản)

## Các bước tiếp theo

Bây giờ bạn đã có phần giới thiệu về Amazon S3, hãy cùng vào console để bắt đầu thực hành.