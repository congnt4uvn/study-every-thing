# Hướng Dẫn Khắc Phục Sự Cố SSH

Hướng dẫn này bao gồm các vấn đề kết nối SSH phổ biến khi kết nối đến AWS EC2 instances và cách giải quyết.

## 1) Lỗi Connection Timeout (Hết Thời Gian Kết Nối)

**Vấn đề:** Bị lỗi timeout khi cố gắng kết nối qua SSH.

**Giải pháp:** Đây là vấn đề về security group. Bất kỳ lỗi timeout nào (không chỉ SSH) đều liên quan đến security groups hoặc firewall. Đảm bảo security group của bạn được cấu hình đúng và được gán chính xác cho EC2 instance.

**Các điểm chính:**
- Kiểm tra cấu hình security group của EC2
- Xác minh inbound rules cho phép SSH (cổng 22) từ địa chỉ IP của bạn
- Đảm bảo security group được gắn vào EC2 instance của bạn

## 2) Lỗi Connection Timeout Vẫn Tiếp Diễn

**Vấn đề:** Lỗi timeout vẫn tiếp tục mặc dù đã cấu hình security groups đúng.

**Giải pháp:** Nếu security group đã được cấu hình đúng và vẫn còn vấn đề timeout, có thể firewall của công ty hoặc firewall cá nhân đang chặn kết nối.

**Khuyến nghị:** Sử dụng EC2 Instance Connect như một phương pháp thay thế để truy cập instance.

## 3) Lệnh SSH Không Hoạt Động Trên Windows

**Vấn đề:** Thông báo lỗi "ssh command not found" xuất hiện trên Windows.

**Giải pháp:** Điều này có nghĩa là bạn cần sử dụng PuTTY thay vì lệnh SSH gốc.

**Các bước:**
- Tải xuống và cài đặt PuTTY
- Làm theo hướng dẫn cấu hình PuTTY
- Nếu vấn đề vẫn tiếp diễn, hãy sử dụng EC2 Instance Connect như được mô tả trong bài giảng tiếp theo

## 4) Lỗi Connection Refused (Kết Nối Bị Từ Chối)

**Vấn đề:** Xuất hiện lỗi "Connection refused".

**Giải pháp:** Điều này có nghĩa là instance có thể truy cập được, nhưng không có dịch vụ SSH nào đang chạy trên instance.

**Các bước giải quyết:**
1. Thử khởi động lại instance
2. Nếu khởi động lại không hiệu quả, hãy terminate instance và tạo instance mới
3. Đảm bảo bạn đang sử dụng Amazon Linux 2

## 5) Lỗi Permission Denied (Quyền Truy Cập Bị Từ Chối)

**Vấn đề:** Thông báo lỗi "Permission denied (publickey,gssapi-keyex,gssapi-with-mic)"

**Các nguyên nhân có thể:**

### Security Key Sai
- Bạn đang sử dụng security key sai hoặc không sử dụng security key
- Kiểm tra cấu hình EC2 instance để đảm bảo bạn đã gán đúng key pair

### Tên Người Dùng Sai
- Bạn đang sử dụng tên người dùng sai
- Đảm bảo bạn đã khởi động Amazon Linux 2 EC2 instance
- Sử dụng đúng user: `ec2-user`
- Định dạng: `ec2-user@<public-ip>` (ví dụ: `ec2-user@35.180.242.162`)
- Áp dụng cho cả lệnh SSH và cấu hình PuTTY

## 6) Không Có Gì Hoạt Động

**Vấn đề:** Tất cả các bước khắc phục sự cố đều thất bại.

**Giải pháp:** Đừng hoảng sợ! Sử dụng EC2 Instance Connect như một giải pháp thay thế.

**Yêu cầu:**
- Đảm bảo bạn đã khởi động Amazon Linux 2 instance
- Truy cập thông qua EC2 Instance Connect từ AWS Console
- Bạn sẽ có thể làm theo hướng dẫn

## 7) Kết Nối Hoạt Động Hôm Qua Nhưng Hôm Nay Không

**Vấn đề:** Kết nối SSH hoạt động trước đó nhưng thất bại sau khi dừng và khởi động lại instance.

**Nguyên nhân gốc:** Khi bạn dừng và khởi động lại EC2 instance, địa chỉ public IP sẽ thay đổi.

**Giải pháp:**
- Lấy địa chỉ public IP mới từ EC2 console
- Cập nhật lệnh SSH hoặc cấu hình PuTTY với public IP mới
- Lưu cấu hình đã cập nhật

**Ví dụ:**
- Cũ: `ec2-user@35.180.242.162`
- Mới: `ec2-user@<new-public-ip>`

---

## Bảng Tham Khảo Nhanh

| Loại Lỗi | Nguyên Nhân Chính | Cách Khắc Phục Nhanh |
|-----------|-------------------|----------------------|
| Connection Timeout | Security Group / Firewall | Kiểm tra quy tắc security group |
| SSH Not Found (Windows) | Thiếu SSH client | Sử dụng PuTTY |
| Connection Refused | Dịch vụ SSH không chạy | Khởi động lại instance |
| Permission Denied | Key hoặc username sai | Xác minh key pair và dùng `ec2-user` |
| IP Thay Đổi | Instance bị dừng/khởi động | Cập nhật public IP trong cấu hình |

## Các Phương Pháp Hay Nhất

1. **Luôn sử dụng Amazon Linux 2** để đảm bảo tính nhất quán
2. **Giữ security groups được cấu hình đúng** với quyền truy cập tối thiểu cần thiết
3. **Sử dụng EC2 Instance Connect** như phương pháp dự phòng
4. **Lưu ý public IP thay đổi** khi dừng/khởi động instances
5. **Giữ private key an toàn** và ở đúng vị trí
6. **Sử dụng đúng username** (`ec2-user` cho Amazon Linux 2)