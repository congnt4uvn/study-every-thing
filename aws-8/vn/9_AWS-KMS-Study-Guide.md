# AWS KMS (Key Management Service) - Hướng Dẫn Học Tập

## Tổng Quan
AWS Key Management Service (KMS) được sử dụng để mã hóa và giải mã dữ liệu. Nó cung cấp hai phương pháp chính:
1. Mã hóa/Giải mã trực tiếp (cho dữ liệu dưới 4KB)
2. Mã hóa bao (Envelope Encryption) (cho dữ liệu trên 4KB)

## 1. KMS Encrypt và Decrypt APIs

### Quá Trình Mã Hóa
- **Đầu vào**: Bí mật/dữ liệu dưới 4 kilobyte
- **Bước 1**: Sử dụng API Encrypt thông qua SDK hoặc CLI
- **Bước 2**: Chỉ định Customer Master Key (CMK) để sử dụng trong KMS
- **Bước 3**: KMS kiểm tra với IAM xem có đủ quyền không
- **Đầu ra**: Dữ liệu được mã hóa

### Quá Trình Giải Mã
- **Bước 1**: Sử dụng API Decrypt thông qua SDK hoặc CLI
- **Bước 2**: KMS tự động xác định CMK nào được sử dụng để mã hóa
- **Bước 3**: KMS kiểm tra với IAM xem có quyền giải mã không
- **Đầu ra**: Bí mật được giải mã ở dạng plain-text

### Hạn Chế Chính
- **Giới Hạn Kích Thước**: Tối đa 4 kilobyte cho mỗi lần mã hóa

---

## 2. Mã Hóa Bao (Envelope Encryption) (Cho Dữ Liệu > 4KB)

### Mã Hóa Bao Là Gì?
Mã hóa bao là một kỹ thuật mã hóa dữ liệu lớn (trên 4KB, lên tới hàng megabyte hoặc hơn) bằng cách bao quanh nó với một khóa mã hóa dữ liệu được mã hóa.

### API Chính: GenerateDataKey
**Khái Niệm Quan Trọng**: Bất kỳ dữ liệu nào trên 4 kilobyte PHẢI được mã hóa bằng mã hóa bao với API `GenerateDataKey`.

### Quá Trình Mã Hóa Bao

#### Các Bước Mã Hóa:
1. **Gọi API GenerateDataKey**
   - Chỉ định CMK để sử dụng
   - KMS kiểm tra quyền IAM
   - KMS tạo khóa mã hóa dữ liệu (DEK)

2. **Nhận Hai Khóa từ KMS**
   - Phiên bản plain-text của DEK (để sử dụng phía client)
   - Phiên bản được mã hóa của DEK (để lưu trữ)

3. **Mã Hóa Phía Client**
   - Sử dụng DEK plain-text để mã hóa file lớn phía client
   - Điều này sử dụng CPU của client cho công việc mã hóa thực tế

4. **Xây Dựng Bao**
   - Kết hợp file được mã hóa với DEK được mã hóa
   - Lưu trữ cả hai trong một file envelope duy nhất
   - Điều này tạo ra gói được mã hóa cuối cùng

#### Các Bước Giải Mã:
1. **Trích Xuất từ Bao**
   - Lấy DEK được mã hóa từ file envelope
   - Lấy file được mã hóa từ file envelope

2. **Gọi API Decrypt**
   - Chuyển DEK được mã hóa (tối đa 4KB) tới API KMS Decrypt
   - KMS kiểm tra quyền IAM
   - KMS trả về DEK ở dạng plain-text

3. **Giải Mã Phía Client**
   - Sử dụng DEK plain-text để giải mã file lớn phía client

### Tóm Tắt Kiến Trúc
```
MÃ HÓA:
File Lớn + GenerateDataKey API → DEK plain-text (phía client)
                              → DEK được mã hóa (từ KMS) + File được mã hóa → BAO

GIẢI MÃ:
BAO → Trích DEK được mã hóa → API Decrypt → DEK plain-text
   → Giải mã File Lớn (phía client) → File Gốc
```

---

## 3. Điểm Thi Quan Trọng

✓ **API Encrypt/Decrypt**: Cho dữ liệu ≤ 4KB  
✓ **API GenerateDataKey**: Cho dữ liệu > 4KB (Envelope Encryption)  
✓ **Luôn Kiểm Tra IAM**: KMS luôn xác minh quyền IAM trước khi mã hóa/giải mã  
✓ **Xử Lý Phía Client**: Hầu hết công việc mã hóa cho file lớn diễn ra phía client  
✓ **Bao Chứa**: Cả DEK được mã hóa và file được mã hóa cùng nhau  

---

## 4. Lợi Ích của Mã Hóa Bao

- ✓ Hỗ trợ mã hóa dữ liệu lớn hơn 4KB
- ✓ Giảm tải cho dịch vụ KMS (mã hóa/giải mã phía client)
- ✓ Duy trì bảo mật thông qua envelope được mã hóa
- ✓ Có thể mở rộng cho file lớn (hàng megabyte hoặc hơn)
