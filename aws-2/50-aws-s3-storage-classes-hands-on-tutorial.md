# AWS S3 Storage Classes - Hướng Dẫn Thực Hành

## Tổng Quan
Hướng dẫn này trình bày cách làm việc với các lớp lưu trữ (storage classes) khác nhau của Amazon S3, bao gồm cách thiết lập storage class khi tải lên đối tượng, thay đổi storage class thủ công và tự động hóa chuyển đổi bằng lifecycle rules.

## Tạo S3 Bucket

Đầu tiên, hãy tạo một S3 bucket mới để thực hành:

1. Tạo bucket mới với tên `s3-storage-classes-demos-2022`
2. Chọn bất kỳ region nào bạn muốn
3. Nhấp **Create Bucket**

## Tìm Hiểu Về S3 Storage Classes

Khi tải lên một đối tượng lên S3, bạn có thể chọn từ nhiều storage classes khác nhau. Hãy cùng tìm hiểu từng tùy chọn:

### Các Storage Classes Khả Dụng

#### 1. **S3 Standard**
- Lớp lưu trữ mặc định
- Được thiết kế cho dữ liệu truy cập thường xuyên
- Được lưu trữ trên nhiều Availability Zones (AZs)
- Cung cấp độ trễ thấp và thông lượng cao

#### 2. **S3 Intelligent-Tiering**
- Lý tưởng khi bạn không biết mẫu truy cập dữ liệu của mình
- AWS tự động di chuyển các đối tượng giữa các tiers dựa trên mẫu truy cập
- Bao gồm phí giám sát và tự động phân tiers
- Tối ưu hóa chi phí tự động

#### 3. **S3 Standard-IA (Infrequent Access)**
- Dành cho dữ liệu được truy cập ít thường xuyên
- Vẫn cung cấp độ trễ thấp khi được truy cập
- Chi phí lưu trữ thấp hơn Standard
- Áp dụng thời gian lưu trữ tối thiểu
- Kích thước đối tượng tính phí tối thiểu

#### 4. **S3 One Zone-IA**
- Lưu trữ dữ liệu chỉ trong một Availability Zone duy nhất
- Chi phí thấp hơn Standard-IA
- Phù hợp cho dữ liệu có thể tái tạo nếu bị mất
- **Rủi ro**: Dữ liệu có thể bị mất nếu AZ bị hỏng

#### 5. **S3 Glacier Storage Classes**

**Glacier Instant Retrieval**
- Dành cho dữ liệu lưu trữ cần truy cập ngay lập tức
- Chi phí thấp hơn Standard-IA
- Thời gian truy xuất tính bằng mili giây

**Glacier Flexible Retrieval**
- Dành cho dữ liệu lưu trữ với thời gian truy xuất linh hoạt
- Tùy chọn truy xuất: vài phút đến vài giờ
- Chi phí lưu trữ rất thấp

**Glacier Deep Archive**
- Lớp lưu trữ có chi phí thấp nhất
- Dành cho lưu trữ dài hạn và bảo quản kỹ thuật số
- Thời gian truy xuất: 12-48 giờ

#### 6. **Reduced Redundancy (Đã Ngừng Sử Dụng)**
- Lớp lưu trữ này đã bị ngừng sử dụng
- Không còn được khuyến nghị sử dụng

## Thực Hành: Tải Lên Đối Tượng Với Storage Classes

### Bước 1: Tải Lên Đối Tượng

1. Điều hướng đến bucket của bạn
2. Nhấp **Upload**
3. Nhấp **Add Files** và chọn một tệp (ví dụ: `coffee.JPEG`)
4. Trước khi tải lên, vào **Properties**
5. Trong **Storage Class**, chọn lớp bạn muốn (ví dụ: **Standard-IA**)
6. Nhấp **Upload**

### Bước 2: Xác Minh Storage Class

Sau khi tải lên, bạn có thể xác minh storage class:
- Chọn đối tượng trong bucket của bạn
- Storage class sẽ được hiển thị (ví dụ: `Standard-IA`)

## Thay Đổi Storage Classes Thủ Công

Bạn có thể thay đổi storage class của một đối tượng bất kỳ lúc nào:

1. Chọn đối tượng trong bucket của bạn
2. Vào **Properties**
3. Cuộn xuống **Storage Class**
4. Nhấp **Edit**
5. Chọn storage class mới (ví dụ: **One Zone-IA**)
6. Nhấp **Save Changes**

Đối tượng bây giờ sẽ được lưu trữ trong storage class mới. Bạn có thể lặp lại quy trình này để di chuyển giữa bất kỳ storage classes nào, chẳng hạn như:
- Di chuyển đến **Glacier Instant Retrieval** để lưu trữ
- Di chuyển đến **Intelligent-Tiering** để tối ưu hóa tự động

## Tự Động Hóa Chuyển Đổi Storage Class Với Lifecycle Rules

Thay vì thay đổi storage classes thủ công, bạn có thể tự động hóa quy trình bằng cách sử dụng S3 Lifecycle Rules.

### Tạo Lifecycle Rule

1. Điều hướng đến bucket của bạn
2. Vào tab **Management**
3. Nhấp **Create Lifecycle Rule**

### Cấu Hình Rule

1. **Rule Name**: Nhập tên (ví dụ: `DemoRule`)
2. **Rule Scope**: Chọn áp dụng cho tất cả các đối tượng trong bucket (hoặc chỉ định prefix/tag)
3. Nhấp **Acknowledge** khi được nhắc

### Thiết Lập Transitions

Cấu hình transitions cho phiên bản hiện tại của các đối tượng:

**Ví Dụ Lịch Trình Chuyển Đổi:**
- Sau **30 ngày**: Di chuyển đến **Standard-IA**
- Sau **60 ngày**: Di chuyển đến **Intelligent-Tiering**
- Sau **180 ngày**: Di chuyển đến **Glacier Flexible Retrieval**

Bạn có thể thêm nhiều transitions tùy theo yêu cầu vòng đời dữ liệu của mình.

### Xem Xét và Tạo

1. Xem xét tất cả các transitions đã cấu hình
2. Xác minh timeline chuyển đổi
3. Nhấp **Create Rule**

## Những Điểm Chính Cần Nhớ

- **Nhiều Storage Classes**: S3 cung cấp nhiều storage classes được tối ưu hóa cho các mẫu truy cập và yêu cầu chi phí khác nhau
- **Linh Hoạt**: Bạn có thể thay đổi storage classes thủ công bất kỳ lúc nào
- **Tự Động Hóa**: Lifecycle rules cho phép chuyển đổi tự động dựa trên tuổi của đối tượng
- **Tối Ưu Chi Phí**: Chọn storage class phù hợp có thể giảm đáng kể chi phí lưu trữ
- **Độ Bền Dữ Liệu**: Hầu hết các storage classes (trừ One Zone-IA) lưu trữ dữ liệu trên nhiều AZs để có độ bền cao

## Thực Hành Tốt Nhất

1. **Sử dụng Standard** cho dữ liệu được truy cập thường xuyên
2. **Sử dụng Intelligent-Tiering** khi mẫu truy cập không xác định hoặc thay đổi
3. **Sử dụng Standard-IA hoặc One Zone-IA** cho dữ liệu truy cập không thường xuyên
4. **Sử dụng Glacier classes** cho lưu trữ dài hạn
5. **Triển khai Lifecycle Rules** để tự động tối ưu hóa chi phí
6. **Xem xét thời gian lưu trữ tối thiểu** khi lập kế hoạch chuyển đổi

## Kết Luận

AWS S3 Storage Classes cung cấp các tùy chọn mạnh mẽ để tối ưu hóa chi phí lưu trữ trong khi duy trì mức độ truy cập và độ bền phù hợp cho dữ liệu của bạn. Bằng cách hiểu từng storage class và triển khai lifecycle rules, bạn có thể đảm bảo dữ liệu của mình được lưu trữ một cách hiệu quả về chi phí trong suốt vòng đời của nó.

---

*Hướng dẫn này là một phần của khóa học AWS Storage Services.*