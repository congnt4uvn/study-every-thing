# Hướng Dẫn Quy Tắc Lifecycle AWS S3

## Giới Thiệu

Hướng dẫn này trình bày cách tạo và cấu hình các quy tắc lifecycle cho AWS S3 buckets để tự động quản lý việc chuyển đổi đối tượng giữa các lớp lưu trữ và xử lý hết hạn đối tượng.

## Tạo Quy Tắc Lifecycle

Hãy bắt đầu và tạo một quy tắc lifecycle cho buckets của chúng ta.

1. Điều hướng đến tab **Management** trong S3 bucket của bạn
2. Nhấp **Create a lifecycle rule**
3. Đặt tên cho quy tắc (ví dụ: "demo rule")
4. Áp dụng nó cho tất cả các đối tượng trong bucket và xác nhận

## Năm Hành Động Quy Tắc

Chúng ta có thể thấy có năm hành động quy tắc khác nhau:

1. **Di chuyển các phiên bản hiện tại của đối tượng giữa các lớp lưu trữ**
2. **Di chuyển các phiên bản không hiện tại của đối tượng giữa các lớp**
3. **Hết hạn các phiên bản hiện tại của đối tượng**
4. **Xóa vĩnh viễn các phiên bản không hiện tại của đối tượng**
5. **Xóa các đối tượng đã hết hạn, delete markers, hoặc incomplete multi-part upload**

Hãy xem xét từng cái một.

## Di Chuyển Các Đối Tượng Phiên Bản Hiện Tại Giữa Các Lớp Lưu Trữ

Di chuyển các đối tượng phiên bản hiện tại giữa các lớp lưu trữ có nghĩa là bạn có một bucket có phiên bản, và phiên bản hiện tại là phiên bản mới nhất - phiên bản được hiển thị cho người dùng.

### Ví Dụ Timeline Chuyển Đổi

Bạn có thể cấu hình các chuyển đổi như sau:

- **Sau 30 ngày** → Chuyển sang Standard-IA
- **Sau 60 ngày** → Chuyển sang Intelligent-Tiering
- **Sau 90 ngày** → Chuyển sang Glacier Instant Retrieval
- **Sau 180 ngày** → Chuyển sang Glacier Flexible Retrieval
- **Sau 365 ngày** → Chuyển sang Glacier Deep Archive

Bạn có thể có bao nhiêu chuyển đổi tùy thích.

## Di Chuyển Các Phiên Bản Không Hiện Tại

Chúng ta cũng có thể di chuyển các phiên bản không hiện tại nhanh hơn. Điều này áp dụng cho các đối tượng không phải là hiện tại - các đối tượng đã bị ghi đè bởi một phiên bản mới hơn.

Ví dụ, chúng ta có thể di chuyển các phiên bản không hiện tại vào Glacier Flexible Retrieval sau 90 ngày vì chúng ta biết rằng sau 90 ngày chúng ta sẽ không cần nó để truy xuất. Điều này hoàn hảo và chúng ta có thể tiếp tục, nhưng chúng ta có thể thêm nhiều chuyển đổi hơn.

## Hết Hạn và Xóa Đối Tượng

### Phiên Bản Hiện Tại
Chúng ta muốn cho hết hạn các phiên bản hiện tại của đối tượng sau một khoảng thời gian xác định. Bạn có thể thiết lập nó sau 700 ngày ở phía dưới.

### Phiên Bản Không Hiện Tại
Tương tự đối với các phiên bản không hiện tại - chúng ta muốn xóa vĩnh viễn chúng sau 700 ngày.

## Xem Xét Các Chuyển Đổi

Điều này rất hay vì nó cho bạn thấy một timeline về những gì sẽ xảy ra với phiên bản hiện tại và các phiên bản không hiện tại của đối tượng của bạn.

Nếu chúng ta hài lòng với tất cả những điều này, chúng ta chỉ cần tiếp tục và tạo quy tắc này, và quy tắc này sẽ hoạt động trong nền để thực hiện những gì nó phải làm.

## Kết Luận

Vậy là xong! Bây giờ bạn đã biết cách tự động di chuyển các đối tượng trong AWS giữa các lớp lưu trữ khác nhau.

Tôi hy vọng bạn thích nó và tôi sẽ gặp bạn trong bài giảng tiếp theo.