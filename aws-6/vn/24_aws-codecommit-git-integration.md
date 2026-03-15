# AWS CodeCommit - Hướng Dẫn Tích Hợp Git

## Tổng Quan
AWS CodeCommit là dịch vụ kiểm soát mã nguồn được quản lý hoàn toàn, lưu trữ các kho lưu trữ Git an toàn. Hướng dẫn này bao gồm cách tích hợp Git với AWS CodeCommit.

## Yêu Cầu Trước
- Tài khoản AWS với IAM user
- Đã cài đặt Git trên máy tính
- Hiểu biết cơ bản về kiểm soát phiên bản

## Phương Thức Xác Thực

### 1. SSH Keys (Khóa SSH)
- **Trường hợp sử dụng**: Dành cho các chuyên gia Git đã quen với SSH
- **Vị trí thiết lập**: IAM → Users → Security Credentials → SSH keys for AWS CodeCommit
- **Các bước**:
  1. Tải lên SSH public key của bạn lên AWS IAM
  2. Điều hướng đến kho CodeCommit của bạn
  3. Chọn "Clone URL" → "Clone SSH"
  4. Sử dụng SSH URL với lệnh git clone

### 2. HTTPS Git Credentials (Khuyến Nghị cho Người Mới)
- **Trường hợp sử dụng**: Thiết lập dễ dàng hơn cho người mới dùng Git
- **Vị trí thiết lập**: IAM → Users → Security Credentials → HTTPS Git credentials for AWS CodeCommit
- **Các bước**:
  1. Click "Generate" để tạo credentials
  2. Tải xuống và lưu credentials (username và password)
  3. Lưu ý: Bạn có thể tạo tối đa 2 bộ credentials cho mỗi user

## Nhân Bản Kho Lưu Trữ (Clone Repository)

### Sử dụng HTTPS
```bash
# 1. Lấy HTTPS clone URL từ CodeCommit
# 2. Clone repository
git clone <HTTPS_URL>

# 3. Nhập Git credentials khi được yêu cầu
Username: <your-git-username>
Password: <your-git-password>
```

### Kiểm Tra Cài Đặt Git
```bash
# Kiểm tra xem Git đã được cài đặt chưa
git --version

# Kết quả trả về: git version 2.9.2 hoặc cao hơn
```

## Cài Đặt Git
- **Windows**: Tải từ [git-scm.com](https://git-scm.com)
- **Mac**: Sử dụng Homebrew hoặc tải trình cài đặt
- **Ubuntu/Linux**: `sudo apt-get install git`

## Làm Việc với Repository Đã Clone

Sau khi clone, bạn sẽ có bản sao local của repository:
```bash
# Di chuyển vào repository
cd <repository-name>

# Kiểm tra branch hiện tại
git branch

# Liệt kê các files
ls
```

## Quản Lý Git Credentials trong IAM

Trong phần Security Credentials, bạn có thể:
- Tạo credentials mới
- Xem trạng thái credentials đang hoạt động
- Đặt lại mật khẩu
- Đặt credentials sang chế độ không hoạt động
- Xóa credentials

## Điểm Quan Trọng Cần Nhớ

1. **Hai Tùy Chọn Xác Thực**: SSH keys hoặc HTTPS credentials
2. **Giới Hạn Credentials**: Tối đa 2 HTTPS Git credentials cho mỗi IAM user
3. **Bảo Mật**: Credentials được thiết kế riêng cho CodeCommit
4. **UI vs Command Line**: Command line thực tế hơn cho quy trình phát triển thường xuyên
5. **Yêu Cầu Git**: Phải cài đặt Git locally để làm việc với CodeCommit

## Thực Hành Tốt Nhất

- Giữ Git credentials của bạn an toàn và không bao giờ chia sẻ
- Sử dụng SSH keys nếu bạn thành thạo với SSH
- Sử dụng HTTPS credentials cho thiết lập đơn giản hơn
- Thường xuyên xoay vòng credentials của bạn để bảo mật
- Tải xuống và lưu credentials ngay sau khi tạo

## Mẹo Cho Kỳ Thi

- Nhớ rằng CodeCommit hỗ trợ cả xác thực SSH và HTTPS
- Biết vị trí để tạo Git credentials (IAM → Security Credentials)
- Hiểu sự khác biệt giữa Access Keys (cho AWS CLI/SDK) và Git credentials (cho CodeCommit)
- Bạn không cần phải là chuyên gia Git cho kỳ thi, nhưng hiểu các khái niệm tích hợp cơ bản

## Các Bước Tiếp Theo

Sau khi thiết lập kết nối Git:
1. Thêm files mới vào repository
2. Commit thay đổi locally
3. Push thay đổi lên CodeCommit
4. Cộng tác với các thành viên trong nhóm

---

*Ngày Học: 15 tháng 3, 2026*
