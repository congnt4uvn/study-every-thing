# Tổng Quan về Mã Hóa Object trong Amazon S3

## Giới Thiệu

Mã hóa object trong Amazon S3 cung cấp nhiều phương thức để bảo mật dữ liệu của bạn khi lưu trữ và truyền tải. Hiểu rõ các tùy chọn mã hóa này là rất quan trọng để triển khai các biện pháp bảo mật phù hợp cho S3 buckets của bạn.

## Các Phương Thức Mã Hóa

Bạn có thể mã hóa các object trong S3 buckets bằng một trong bốn phương thức sau:

### 1. Mã Hóa Phía Server (SSE - Server-Side Encryption)

Mã hóa phía server có nhiều loại:

#### SSE-S3 (Mã Hóa Phía Server với Khóa do Amazon S3 Quản Lý)

**Tổng Quan:**
- Mã hóa sử dụng các khóa được xử lý, quản lý và sở hữu bởi AWS
- Bạn không bao giờ có quyền truy cập vào các khóa này
- Object được mã hóa phía server bởi AWS
- Sử dụng thuật toán mã hóa AES-256
- **Được bật mặc định** cho các bucket và object mới

**Cách Hoạt Động:**
1. Người dùng tải lên file với header đúng: `"x-amz-server-side-encryption": "AES256"`
2. Amazon S3 nhận object
3. S3 ghép nối object với khóa thuộc sở hữu của S3
4. Quá trình mã hóa được thực hiện bằng cách kết hợp khóa và object
5. Object đã mã hóa được lưu trữ trong S3 bucket

**Header Bắt Buộc:**
```
x-amz-server-side-encryption: AES256
```

#### SSE-KMS (Mã Hóa Phía Server với Khóa KMS)

**Tổng Quan:**
- Sử dụng AWS Key Management Service (KMS) để quản lý khóa mã hóa
- Cung cấp quyền kiểm soát khóa mã hóa cho người dùng
- Khóa có thể được tạo và quản lý trong KMS
- Việc sử dụng khóa được kiểm toán bằng AWS CloudTrail

**Ưu Điểm:**
- Người dùng có quyền kiểm soát khóa mã hóa
- Khả năng tạo các khóa tùy chỉnh trong KMS
- Theo dõi việc sử dụng khóa thông qua CloudTrail

**Cách Hoạt Động:**
1. Người dùng tải lên object với header KMS, chỉ định khóa KMS cần sử dụng
2. Object xuất hiện trong Amazon S3
3. Khóa KMS được chỉ định từ AWS KMS được sử dụng để mã hóa
4. Object và khóa được kết hợp để tạo file đã mã hóa
5. File đã mã hóa được lưu trữ trong S3 bucket

**Header Bắt Buộc:**
```
x-amz-server-side-encryption: aws:kms
```

**Yêu Cầu Truy Cập:**
Để đọc file được mã hóa bằng SSE-KMS, bạn cần:
- Quyền truy cập vào chính S3 object
- Quyền truy cập vào khóa KMS cơ bản được sử dụng để mã hóa

**Hạn Chế:**
- Các API của KMS (GenerateDataKey cho mã hóa, Decrypt cho giải mã) được tính vào hạn ngạch KMS
- Giới hạn lượt gọi API: 5.000 đến 30.000 yêu cầu mỗi giây (tùy theo vùng)
- Hạn ngạch có thể được tăng thông qua Service Quotas Console
- S3 bucket có lưu lượng cao với mã hóa KMS có thể gặp phải giới hạn throttling

#### SSE-C (Mã Hóa Phía Server với Khóa do Khách Hàng Cung Cấp)

**Tổng Quan:**
- Khóa được quản lý bên ngoài AWS
- Vẫn là mã hóa phía server (khóa được gửi đến AWS)
- Amazon S3 không bao giờ lưu trữ khóa mã hóa
- Khóa bị loại bỏ sau khi sử dụng

**Yêu Cầu:**
- **Phải sử dụng HTTPS** để truyền tải
- Khóa phải được truyền như một phần của HTTP headers cho mọi yêu cầu

**Cách Hoạt Động:**
1. Người dùng tải lên file cùng với khóa mã hóa (được quản lý bên ngoài AWS)
2. Amazon S3 sử dụng khóa do client cung cấp và object để thực hiện mã hóa
3. File đã mã hóa được lưu trữ trong S3 bucket
4. Để đọc file, người dùng phải cung cấp cùng khóa đã được sử dụng để mã hóa

### 2. Mã Hóa Phía Client (Client-Side Encryption)

**Tổng Quan:**
- Mã hóa được thực hiện hoàn toàn ở phía client
- Dữ liệu được mã hóa trước khi gửi đến Amazon S3
- Dữ liệu lấy từ S3 phải được giải mã bởi client
- Client hoàn toàn quản lý khóa và chu trình mã hóa

**Triển Khai:**
- Dễ dàng triển khai hơn khi sử dụng các thư viện client như AWS Client-Side Encryption Library

**Cách Hoạt Động:**
1. Client có một file và một khóa mã hóa (bên ngoài AWS)
2. Client thực hiện mã hóa cục bộ
3. File đã mã hóa được tải lên Amazon S3
4. File vẫn được mã hóa trong S3
5. Client lấy và giải mã file khi cần thiết

## Mã Hóa Trong Quá Trình Truyền Tải (Encryption in Transit)

**Tổng Quan:**
Mã hóa trong quá trình truyền tải, còn được gọi là mã hóa SSL/TLS, bảo vệ dữ liệu trong khi nó được truyền giữa client của bạn và Amazon S3.

**Các Endpoint của S3:**
- **HTTP endpoint** - Không được mã hóa
- **HTTPS endpoint** - Mã hóa trong quá trình truyền tải (được khuyến nghị)

**Thực Hành Tốt Nhất:**
- Luôn sử dụng HTTPS để truyền dữ liệu an toàn
- SSE-C **yêu cầu** giao thức HTTPS
- Hầu hết các client sử dụng HTTPS endpoint theo mặc định

### Bắt Buộc Mã Hóa Trong Quá Trình Truyền Tải

Bạn có thể ép buộc chỉ truy cập qua HTTPS bằng cách sử dụng bucket policy:

**Ví Dụ Bucket Policy:**
```json
{
  "Effect": "Deny",
  "Action": "s3:GetObject",
  "Condition": {
    "aws:SecureTransport": "false"
  }
}
```

**Cách Hoạt Động:**
- `aws:SecureTransport` là `true` khi sử dụng HTTPS
- `aws:SecureTransport` là `false` khi sử dụng HTTP
- Policy từ chối bất kỳ thao tác GetObject nào khi SecureTransport là false
- Người dùng cố gắng sử dụng HTTP sẽ bị chặn
- Người dùng sử dụng HTTPS sẽ được phép truy cập

## Tóm Tắt

Amazon S3 cung cấp các tùy chọn mã hóa toàn diện:

- **SSE-S3**: Mã hóa mặc định với khóa do AWS quản lý (tùy chọn đơn giản nhất)
- **SSE-KMS**: Mã hóa với khóa KMS do khách hàng kiểm soát (kiểm toán và kiểm soát)
- **SSE-C**: Mã hóa với khóa do khách hàng cung cấp (kiểm soát khóa hoàn toàn, khóa không được AWS lưu trữ)
- **Mã Hóa Phía Client**: Kiểm soát hoàn toàn mã hóa và khóa ở phía client
- **Mã Hóa Trong Quá Trình Truyền Tải**: Sử dụng HTTPS để bảo vệ dữ liệu trong quá trình truyền

Chọn phương thức mã hóa phù hợp nhất với yêu cầu bảo mật và tuân thủ của bạn.