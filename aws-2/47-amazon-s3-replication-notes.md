# Amazon S3 Replication - Những Lưu Ý Quan Trọng

## Tổng Quan

Tài liệu này trình bày những lưu ý quan trọng về tính năng Amazon S3 Replication và các hành vi chính của nó.

## Các Điểm Chính

### 1. Chỉ Sao Chép Các Đối Tượng Mới

Sau khi bạn kích hoạt Replication, **chỉ các đối tượng mới sẽ được sao chép**. Các đối tượng đã tồn tại trước khi kích hoạt replication sẽ không được tự động sao chép.

### 2. Sao Chép Các Đối Tượng Đã Tồn Tại

Nếu bạn muốn sao chép các đối tượng đã tồn tại, bạn cần sử dụng tính năng **S3 Batch Replication**. Tính năng này cho phép bạn:
- Sao chép các đối tượng đã tồn tại
- Sao chép các đối tượng đã thất bại trong quá trình replication

### 3. Các Thao Tác Xóa

Đối với các thao tác xóa:
- Bạn **có thể** sao chép các delete markers từ bucket nguồn sang bucket đích (đây là cài đặt tùy chọn)
- Nếu bạn có thao tác xóa với version ID, **chúng sẽ không được sao chép**
- Các thao tác xóa vĩnh viễn không được sao chép để tránh các thao tác xóa độc hại xảy ra từ bucket này sang bucket khác

### 4. Không Có Chuỗi Replication

**Không có chuỗi replication** (no chaining of replications).

**Ví dụ:**
- Nếu bucket một có replication sang bucket hai
- Và bucket hai có replication sang bucket ba
- Thì các đối tượng từ bucket một **không** được sao chép vào bucket ba

Mỗi mối quan hệ replication là độc lập và không lan truyền theo chuỗi.

## Tóm Tắt

S3 Replication là một tính năng mạnh mẽ, nhưng điều quan trọng là phải hiểu những hạn chế và hành vi này để cấu hình chiến lược replication của bạn một cách phù hợp và tránh các kết quả không mong muốn.