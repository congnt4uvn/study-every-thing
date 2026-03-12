# AWS CloudFront Signed URLs - Quản Lý Khóa

## Tổng Quan

Hướng dẫn này giải thích cách tạo và quản lý khóa để ký URL với Amazon CloudFront. Signed URLs cung cấp quyền truy cập an toàn, có giới hạn thời gian vào nội dung CloudFront của bạn.

## Các Loại Signers

CloudFront hỗ trợ hai loại signers để tạo signed URLs:

### 1. Trusted Key Groups (Phương Pháp Được Khuyến Nghị)

**Trusted key group** là phương pháp mới và được khuyến nghị để quản lý signed URLs trên CloudFront.

**Ưu điểm:**
- Tận dụng APIs để tự động tạo và xoay vòng khóa
- Sử dụng IAM cho bảo mật API trong việc quản lý key group
- Có thể được quản lý bởi bất kỳ IAM user nào có đủ quyền (không chỉ root account)
- Khả năng bảo mật và tự động hóa tốt hơn

### 2. CloudFront Key Pairs (Phương Pháp Cũ)

Phương pháp ban đầu sử dụng AWS account với CloudFront key pairs.

**Nhược điểm:**
- Yêu cầu thông tin đăng nhập root account
- Chỉ có thể quản lý qua AWS console
- Không hỗ trợ API để tự động hóa
- Cách tiếp cận kém an toàn hơn
- **Không được khuyến nghị cho các triển khai mới**

## Cách Thức Hoạt Động Của Trusted Key Groups

### Cấu Trúc Khóa

Bạn có thể tạo một hoặc nhiều trusted key groups trong CloudFront distribution của mình. Mỗi triển khai yêu cầu:

1. **Private Key (Khóa Riêng)** - Được sử dụng bởi ứng dụng của bạn (ví dụ: EC2 instances) để ký URLs
2. **Public Key (Khóa Công Khai)** - Được tải lên CloudFront để xác minh chữ ký URL

### Luồng Hoạt Động Của Khóa

```
Private Key → EC2 Instances → Ký URLs
Public Key → CloudFront → Xác Minh Chữ Ký
```

Private key được sử dụng bởi ứng dụng của bạn để tạo signed URLs, trong khi CloudFront sử dụng public key để xác minh tính hợp lệ của các chữ ký.

## Hướng Dẫn Thực Hành: Thiết Lập Trusted Key Groups

### Bước 1: Tạo Cặp Khóa RSA

1. Tạo cặp khóa RSA 2,048-bit sử dụng trình tạo trực tuyến hoặc OpenSSL
2. **Quan trọng:** Kích thước khóa phải chính xác là 2,048 bits
3. Đợi quá trình tạo khóa hoàn tất (khoảng 3 giây)
4. Lưu cả hai khóa:
   - **Private Key**: Giữ an toàn và bí mật - sử dụng bởi ứng dụng của bạn
   - **Public Key**: Sẽ được tải lên CloudFront

> **Lưu Ý Bảo Mật:** Private key nên được lưu trữ an toàn. Public key có thể được tạo lại từ private key nếu cần.

### Bước 2: Tạo Public Key Trong CloudFront

1. Điều hướng đến CloudFront trong AWS Console
2. Vào phần **Key Management**
3. Chọn **Public Keys** từ thanh bên trái
4. Nhấp **Create Public Key**
5. Cung cấp tên (ví dụ: "demo key")
6. Dán public key đã tạo của bạn
7. Nhấp **Create**

**Xử Lý Sự Cố:** Nếu gặp lỗi, hãy xác minh rằng bạn đang sử dụng khóa 2,048-bit. Nếu vấn đề vẫn tiếp diễn, hãy tạo lại cặp khóa 2,048-bit mới.

### Bước 3: Tạo Key Group

1. Trong CloudFront Key Management, chọn **Key Groups**
2. Nhấp **Create Key Group**
3. Cung cấp tên (ví dụ: "demo key group")
4. Thêm tối đa 5 public keys vào nhóm
5. Chọn public key vừa tạo của bạn
6. Nhấp **Create**

### Bước 4: Tham Chiếu Key Group Trong CloudFront Distribution

Key group sẽ được CloudFront tham chiếu để xác thực các signed URLs được tạo bởi ứng dụng của bạn (ví dụ: EC2 instances).

## Phương Pháp Cũ: CloudFront Key Pairs (Không Khuyến Nghị)

### Truy Cập CloudFront Key Pairs

1. Đăng nhập bằng **root account** (bắt buộc)
2. Nhấp vào tên tài khoản của bạn
3. Chọn **My Security Credentials**
4. Tìm phần **CloudFront Key Pair**

### Tạo Key Pair (Phương Pháp Cũ)

1. Chọn tạo key pair mới hoặc tải lên key pair của riêng bạn
2. Nếu tạo mới:
   - Nhấp **Create New Key Pair**
   - Tải xuống file private key
   - Tải xuống file public key
   - Nhấp **Close**

### Quản Lý Key Pairs

- Khóa có thể được đặt thành: Active, Inactive, hoặc Deleted
- Key pairs áp dụng cho tất cả CloudFront distributions
- Private keys phải được phân phối thủ công đến EC2 instances

### Tại Sao Phương Pháp Này Không Được Khuyến Nghị

- **Yêu cầu root account**: Chỉ root account mới có thể quản lý các khóa này
- **Không hỗ trợ API**: Không thể tự động hóa
- **Kém an toàn hơn**: Rủi ro bảo mật cao hơn so với trusted key groups
- **Không tích hợp IAM**: Không thể tận dụng quyền IAM

## Thực Hành Tốt Nhất

1. ✅ **Sử Dụng Trusted Key Groups** - Luôn ưu tiên phương pháp này hơn legacy key pairs
2. ✅ **IAM Users** - Cho phép IAM users với quyền phù hợp quản lý khóa
3. ✅ **Xoay Vòng Khóa** - Sử dụng APIs để tự động hóa việc xoay vòng khóa
4. ✅ **Lưu Trữ An Toàn** - Lưu trữ private keys an toàn (ví dụ: AWS Secrets Manager)
5. ✅ **Khóa 2,048-bit** - Luôn sử dụng khóa RSA 2,048-bit
6. ❌ **Tránh Root Account** - Không sử dụng root account để quản lý khóa

## Lời Khuyên Cho Kỳ Thi

Đối với các kỳ thi chứng chỉ AWS, hãy nhớ:
- **Trusted Key Groups** là phương pháp được khuyến nghị
- Bất kỳ IAM user nào có đủ quyền đều có thể quản lý key groups
- Phương pháp CloudFront Key Pair cũ yêu cầu quyền truy cập root account
- Trusted key groups hỗ trợ tự động hóa dựa trên API
- Private keys ký URLs; public keys xác minh chữ ký

## Tóm Tắt

CloudFront signed URLs cung cấp quyền truy cập an toàn, có kiểm soát vào nội dung của bạn. Phương pháp hiện đại sử dụng trusted key groups mang lại bảo mật, tự động hóa và tích hợp IAM tốt hơn so với phương pháp CloudFront key pair cũ. Luôn ưu tiên trusted key groups cho các triển khai mới.

---

**Điểm Chính Cần Nhớ:**
- Tạo cặp khóa RSA 2,048-bit
- Tải public keys lên CloudFront
- Tạo key groups để tổ chức public keys
- Giữ private keys an toàn trên các máy chủ ứng dụng của bạn
- Sử dụng IAM users thay vì root account để quản lý khóa