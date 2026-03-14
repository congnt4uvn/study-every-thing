# Tài Liệu Học Tập AWS Lambda Concurrency

## Tổng Quan
Tài liệu này bao gồm các thiết lập và cấu hình concurrency (đồng thời) của AWS Lambda, bao gồm reserved concurrency và provisioned concurrency.

## Kiến Thức Cơ Bản Về Lambda Concurrency

### Unreserved Account Concurrency (Concurrency Chưa Dành Riêng)
- Thiết lập concurrency mặc định cho các hàm Lambda
- Mặc định: **1000 lần thực thi đồng thời** trên mỗi tài khoản
- Được chia sẻ giữa tất cả các hàm Lambda trong tài khoản
- Có thể được sử dụng bởi bất kỳ hàm nào không có reserved concurrency

### Reserved Concurrency (Concurrency Dành Riêng)
Reserved concurrency phân bổ một số lượng cụ thể các lần thực thi đồng thời cho một hàm Lambda.

#### Cách Hoạt Động
- Bạn có thể đặt giới hạn concurrency cụ thể cho một hàm
- Ví dụ: Đặt reserved concurrency là **20** cho một hàm
  - Hàm này nhận được 20 lần thực thi đồng thời được đảm bảo
  - Unreserved account concurrency trở thành: 1000 - 20 = **980**
  - Các hàm khác chia sẻ 980 lần thực thi đồng thời còn lại

#### Kiểm Tra Throttling (Giới Hạn Tốc Độ)
- Đặt reserved concurrency thành **0** để kiểm tra hành vi throttling
- Hàm sẽ luôn bị throttled (bị giới hạn)
- Hữu ích cho việc kiểm tra xử lý lỗi trong ứng dụng
- Lỗi trả về: "Exceeded rate" từ invoke API action

#### Các Bước Cấu Hình
1. Điều hướng đến cấu hình hàm Lambda
2. Chọn tab **Concurrency** ở bên trái
3. Nhấp **Edit** (Chỉnh sửa)
4. Chọn giữa:
   - Sử dụng unreserved account concurrency
   - Dành riêng concurrency (chỉ định số lượng)
5. Lưu các thay đổi

## Provisioned Concurrency (Concurrency Được Cấp Phát Trước)

### Mục Đích
- Loại bỏ **cold starts** trong các hàm Lambda
- Cold starts xảy ra khi ứng dụng khởi tạo lần đầu
- Mất thời gian để khởi động môi trường thực thi

### Cách Hoạt Động
- Giữ một pool các instance hàm đã được khởi tạo sẵn (warm)
- Giảm độ trễ cho các lần gọi hàm
- Các instance được khởi tạo trước và sẵn sàng phản hồi ngay lập tức

### Cấu Hình
- Thêm cấu hình provisioned concurrency
- Có thể được đặt cho:
  - **Alias** - con trỏ có tên đến một phiên bản hàm
  - **Version** - bản snapshot bất biến của mã và cấu hình hàm
- Chỉ định số lượng lần thực thi đồng thời được cấp phát trước cần thiết

## Các Thực Hành Tốt Nhất

1. **Giám Sát Việc Sử Dụng Concurrency**
   - Theo dõi số lần thực thi đồng thời mà các hàm của bạn cần
   - Điều chỉnh reserved concurrency dựa trên các mẫu sử dụng thực tế

2. **Kiểm Tra Các Tình Huống Throttling**
   - Đặt concurrency thành 0 để kiểm tra hành vi ứng dụng khi bị throttling
   - Triển khai xử lý lỗi phù hợp cho các lỗi vượt quá tốc độ

3. **Sử Dụng Provisioned Concurrency Cho Các Ứng Dụng Nhạy Cảm Về Độ Trễ**
   - Được khuyến nghị cho các ứng dụng yêu cầu độ trễ thấp nhất quán
   - Đánh đổi: Chi phí cao hơn cho các instance luôn sẵn sàng

4. **Cân Bằng Giữa Các Hàm**
   - Nhớ rằng: Reserved concurrency làm giảm concurrency khả dụng cho các hàm khác
   - Lên kế hoạch phân bổ concurrency trên tất cả các hàm trong tài khoản của bạn

## Những Điểm Chính Cần Nhớ

- **Unreserved Concurrency**: Pool chia sẻ mặc định (1000 trên mỗi tài khoản)
- **Reserved Concurrency**: Phân bổ chuyên dụng cho các hàm cụ thể
- **Provisioned Concurrency**: Các instance được làm nóng trước để loại bỏ cold starts
- **Kiểm Tra**: Đặt concurrency thành 0 để kiểm tra hành vi throttling
- **Cấu Hình**: Có thể truy cập trong Lambda console dưới tab Concurrency

## Các Thông Báo Lỗi Thường Gặp

**"Calling the invoke API action failed because we have exceeded the rate"**
- Xảy ra khi hàm vượt quá giới hạn reserved concurrency của nó
- Hoặc khi tài khoản đạt đến giới hạn unreserved concurrency
- Giải pháp: Tăng reserved concurrency hoặc sử dụng unreserved account concurrency
