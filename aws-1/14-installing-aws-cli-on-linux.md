# Cài Đặt AWS CLI Trên Linux

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quá trình cài đặt AWS CLI Version 2 trên hệ thống Linux bằng phương pháp cài đặt chính thức.

## Yêu Cầu Trước Khi Cài Đặt

- Hệ thống Linux có quyền truy cập terminal
- Quyền `sudo` để thực hiện cài đặt
- Kết nối Internet để tải xuống bộ cài đặt

## Các Bước Cài Đặt

### Bước 1: Tải Xuống Bộ Cài Đặt AWS CLI

Đầu tiên, tải xuống gói cài đặt AWS CLI:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

Lệnh này sẽ tải xuống bộ cài đặt AWS CLI Version 2 mới nhất dưới dạng file ZIP.

### Bước 2: Giải Nén Bộ Cài Đặt

Sau khi quá trình tải xuống hoàn tất, giải nén nội dung của file ZIP:

```bash
unzip awscliv2.zip
```

Lệnh này sẽ giải nén gói cài đặt và chuẩn bị cho quá trình cài đặt.

### Bước 3: Chạy Bộ Cài Đặt

Cài đặt AWS CLI bằng cách chạy bộ cài đặt với quyền root:

```bash
sudo ./aws/install
```

Bạn sẽ được yêu cầu nhập mật khẩu. Sau khi nhập mật khẩu, quá trình cài đặt sẽ tự động tiến hành.

## Kiểm Tra Cài Đặt

Sau khi quá trình cài đặt hoàn tất, hãy kiểm tra xem AWS CLI đã được cài đặt chính xác bằng cách kiểm tra phiên bản:

```bash
aws --version
```

Bạn sẽ thấy kết quả tương tự như:

```
AWS CLI/2.x.x Python/3.x.x Linux/x.x.x botocore/x.x.x
```

Các số phiên bản cụ thể sẽ khác nhau tùy thuộc vào thời điểm bạn thực hiện cài đặt.

## Bước Tiếp Theo

Sau khi AWS CLI đã được cài đặt thành công và lệnh kiểm tra phiên bản hoạt động, bạn có thể tiếp tục với việc cấu hình và sử dụng các lệnh AWS CLI.

## Xử Lý Sự Cố

Nếu bạn gặp bất kỳ vấn đề nào trong quá trình cài đặt, vui lòng tham khảo tài liệu chính thức của AWS CLI để biết các bước xử lý sự cố chi tiết và giải pháp.

---

*Lưu ý: Đảm bảo rằng `/usr/local/bin` nằm trong PATH của bạn để có thể chạy lệnh `aws` từ bất kỳ đâu trong terminal.*