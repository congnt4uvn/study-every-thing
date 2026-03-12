# Chiến lược và Ràng buộc Đặt Task trong ECS

## Tổng quan

Khi tạo một ECS task loại EC2, ECS phải xác định nơi đặt task dựa trên bộ nhớ, CPU và cổng có sẵn trên các EC2 instance mục tiêu của bạn.

**Lưu ý quan trọng:** Chiến lược và ràng buộc đặt task chỉ áp dụng cho **ECS trên EC2 instances**, không áp dụng cho Fargate. Với Fargate, AWS tự động xác định nơi khởi động container và bạn không quản lý các backend instance.

## Quy trình Đặt Task

ECS sử dụng phương pháp best-effort (cố gắng tối đa) khi đặt task. Quy trình đặt task tuân theo các bước sau:

1. **Xác định các instance phù hợp** - Tìm các instance đáp ứng yêu cầu về CPU, bộ nhớ và cổng được định nghĩa trong task definition
2. **Áp dụng ràng buộc đặt task** - Lọc các instance dựa trên các ràng buộc đã định nghĩa
3. **Áp dụng chiến lược đặt task** - Chọn instance đáp ứng tốt nhất chiến lược đặt task
4. **Đặt task** - Triển khai task trên instance đã chọn

## Chiến lược Đặt Task

Chiến lược đặt task hướng dẫn nơi các container mới sẽ được thêm vào hoặc container nào sẽ bị xóa khi mở rộng quy mô.

### 1. Binpack

**Mục đích:** Giảm thiểu số lượng instance đang sử dụng để tiết kiệm chi phí.

**Cách hoạt động:** Đặt các task dựa trên lượng CPU hoặc bộ nhớ khả dụng ít nhất, lấp đầy một instance trước khi chuyển sang instance tiếp theo.

**Cấu hình JSON:**
```json
{
  "type": "binpack",
  "field": "memory"
}
```

**Lợi ích:**
- Tối đa hóa việc sử dụng từng EC2 instance
- Giảm thiểu tổng số instance cần thiết
- Mang lại tiết kiệm chi phí cao nhất

**Ví dụ:** Nếu bạn có nhiều EC2 instance, binpack sẽ lấp đầy instance đầu tiên hoàn toàn với các container trước khi đặt bất kỳ container nào trên instance thứ hai.

### 2. Random

**Mục đích:** Phân phối ngẫu nhiên đơn giản các task.

**Cách hoạt động:** Đặt các task ngẫu nhiên trên các instance có sẵn mà không có logic cụ thể.

**Cấu hình JSON:**
```json
{
  "type": "random"
}
```

**Đặc điểm:**
- Triển khai rất đơn giản
- Không có tối ưu hóa
- Hoạt động tốt cho các kịch bản cơ bản

### 3. Spread

**Mục đích:** Tối đa hóa tính khả dụng cao bằng cách phân phối task đều.

**Cách hoạt động:** Phân tán các task dựa trên một giá trị được chỉ định như instance ID hoặc availability zone.

**Cấu hình JSON:**
```json
{
  "type": "spread",
  "field": "attribute:ecs.availability-zone"
}
```

**Lợi ích:**
- Tối đa hóa tính khả dụng cao
- Phân phối task đều trên các availability zone hoặc instance
- Giảm thiểu tác động của lỗi instance hoặc AZ

**Ví dụ:** Với ba availability zone (AZ-A, AZ-B, AZ-C), các task được phân phối đều:
- Task đầu tiên → AZ-A
- Task thứ hai → AZ-B
- Task thứ ba → AZ-C
- Task thứ tư → AZ-A (chu kỳ lặp lại)

### Kết hợp Chiến lược

Bạn có thể kết hợp nhiều chiến lược đặt task:
- Spread theo availability zone + Spread theo instance ID
- Spread theo availability zone + Binpack theo bộ nhớ

## Ràng buộc Đặt Task

Các ràng buộc thêm quy tắc để kiểm soát nơi có thể đặt task.

### 1. distinctInstance

**Mục đích:** Đảm bảo mỗi task chạy trên một container instance khác nhau.

**Cấu hình JSON:**
```json
{
  "type": "distinctInstance"
}
```

**Kết quả:** Bạn sẽ không bao giờ có hai task trên cùng một instance.

### 2. memberOf

**Mục đích:** Đặt task trên các instance đáp ứng một biểu thức cụ thể sử dụng Cluster Query Language.

**Ví dụ Cấu hình JSON:**
```json
{
  "type": "memberOf",
  "expression": "attribute:ecs.instance-type =~ t2.*"
}
```

**Kết quả:** Ví dụ này đảm bảo tất cả các task chỉ được đặt trên các loại instance t2.

**Đặc điểm:**
- Sử dụng Cluster Query Language nâng cao
- Cung cấp lọc linh hoạt dựa trên thuộc tính instance
- Phức tạp hơn distinctInstance

## Điểm chính cần nhớ

1. **Chỉ dành cho ECS trên EC2** - Chiến lược và ràng buộc đặt task không áp dụng cho Fargate
2. **Best effort** - Chiến lược đặt task là best-effort, không được đảm bảo
3. **Ba chiến lược chính** - Binpack (tối ưu chi phí), Random (đơn giản), Spread (khả dụng cao)
4. **Hai loại ràng buộc** - distinctInstance (đơn giản) và memberOf (nâng cao)
5. **Kết hợp linh hoạt** - Các chiến lược có thể được kết hợp cho logic đặt task phức tạp hơn
6. **Trọng tâm kỳ thi** - Hiểu sự khác biệt cơ bản giữa các chiến lược binpack, spread và random

## Các trường hợp sử dụng

- **Binpack** - Sử dụng khi tối ưu hóa chi phí là ưu tiên
- **Random** - Sử dụng cho các workload đơn giản, không quan trọng
- **Spread** - Sử dụng khi tính khả dụng cao là quan trọng
- **distinctInstance** - Sử dụng khi các task phải được cô lập trên các instance riêng biệt
- **memberOf** - Sử dụng khi các task có yêu cầu instance cụ thể (loại, AMI, v.v.)