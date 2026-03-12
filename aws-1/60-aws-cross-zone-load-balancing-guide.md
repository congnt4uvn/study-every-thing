# Hướng Dẫn Cross-Zone Load Balancing trên AWS

## Tổng Quan

Cross-zone load balancing là một tính năng quan trọng trong AWS Elastic Load Balancing, quyết định cách thức phân phối traffic đến các EC2 instances trên nhiều Availability Zones (AZs).

## Cross-Zone Load Balancing là gì?

Cross-zone load balancing cho phép mỗi load balancer instance phân phối traffic đều đặn đến tất cả các instances đã đăng ký trong tất cả các availability zones, bất kể load balancer node nằm ở AZ nào.

### Ví Dụ Minh Họa

Xét một thiết lập với hai availability zones:
- **AZ1**: Load balancer với 2 EC2 instances
- **AZ2**: Load balancer với 8 EC2 instances
- Tổng cộng: 10 EC2 instances

## Khi Bật Cross-Zone Load Balancing

Khi cross-zone load balancing được kích hoạt:

1. Client gửi 50% traffic đến ALB instance thứ nhất và 50% đến ALB instance thứ hai
2. **Mỗi ALB phân phối traffic đến TẤT CẢ 10 EC2 instances** (bất kể AZ nào)
3. Mỗi EC2 instance nhận được 10% tổng traffic
4. Traffic được phân phối đồng đều trên tất cả các instances

### Lợi Ích
- Phân phối traffic đồng đều trên tất cả instances
- Không có instance nào bị quá tải do mất cân bằng AZ
- Tận dụng tài nguyên tốt hơn

## Khi Tắt Cross-Zone Load Balancing

Khi cross-zone load balancing bị vô hiệu hóa:

1. Client gửi 50% traffic đến AZ1 và 50% đến AZ2
2. **Mỗi ALB chỉ phân phối traffic đến các EC2 instances trong cùng AZ của nó**
3. Ở AZ1: Mỗi instance trong số 2 instances nhận 25% tổng traffic (50% ÷ 2)
4. Ở AZ2: Mỗi instance trong số 8 instances nhận 6.25% tổng traffic (50% ÷ 8)
5. Traffic được giữ trong phạm vi mỗi AZ

### Hệ Quả
- Phân phối traffic có thể không đồng đều nếu các AZ có số lượng instances khác nhau
- Một số instances có thể nhận nhiều traffic hơn các instances khác
- Traffic ở lại trong cùng AZ (không có data transfer giữa các AZ)

## Các Loại Load Balancer và Cài Đặt Mặc Định

### Application Load Balancer (ALB)
- **Mặc định**: Cross-zone load balancing **ĐƯỢC BẬT**
- Có thể tắt ở cấp độ target group
- **Chi phí**: Không tính phí cho data transfer giữa các AZ
- Cross-zone load balancing luôn bật mặc định cho ALB
- Có thể ghi đè cài đặt ở cấp độ target group với ba tùy chọn:
  - Kế thừa từ thuộc tính load balancer (bật mặc định)
  - Bắt buộc bật
  - Bắt buộc tắt

### Network Load Balancer (NLB)
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật trong phần attributes settings
- **Chi phí**: Áp dụng phí data transfer khu vực khi được bật

### Gateway Load Balancer (GWLB)
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật trong phần attributes settings
- **Chi phí**: Áp dụng phí data transfer khu vực khi được bật

### Classic Load Balancer (CLB) - Phiên Bản Cũ
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật
- **Chi phí**: Không tính phí cho data transfer giữa các AZ khi được bật
- **Lưu ý**: Classic Load Balancer là thế hệ cũ và sẽ sớm bị ngừng hỗ trợ

## Cân Nhắc Chi Phí

### Lưu Ý Quan Trọng Về Phí Data Transfer

| Loại Load Balancer | Cài Đặt Mặc Định | Phí Cross-AZ Khi Bật |
|-------------------|-----------------|----------------------|
| Application (ALB) | Bật | **Không tính phí** |
| Network (NLB) | Tắt | **Có tính phí** |
| Gateway (GWLB) | Tắt | **Có tính phí** |
| Classic (CLB) | Tắt | **Không tính phí** |

Trong AWS, data transfer giữa các Availability Zones thường phát sinh chi phí. Tuy nhiên:
- **ALB**: Không tính phí cho cross-zone data transfer (mặc dù được bật mặc định)
- **NLB và GWLB**: Phải trả phí khu vực nếu cross-zone được bật
- **CLB**: Không tính phí cho cross-zone data transfer khi được bật

## Hướng Dẫn Thực Hành

### Cấu Hình Network Load Balancer

1. Điều hướng đến NLB của bạn trong AWS Console
2. Kéo xuống và nhấp vào **Attributes**
3. Cross-zone load balancing sẽ hiển thị là **OFF** mặc định
4. Nhấp **Edit**
5. Bật cross-zone load balancing
6. Lưu ý: Điều này có thể bao gồm phí khu vực cho NLB của bạn

### Cấu Hình Gateway Load Balancer

1. Điều hướng đến GWLB của bạn trong AWS Console
2. Vào **Attributes**
3. Cross-zone load balancing sẽ hiển thị là **OFF** mặc định
4. Nhấp **Edit**
5. Bật cross-zone load balancing
6. Lưu ý: Điều này sẽ phát sinh phí data transfer

### Cấu Hình Application Load Balancer

1. Điều hướng đến ALB của bạn trong AWS Console
2. Vào **Attributes**
3. Cross-zone load balancing **BẬT** mặc định
4. Để điều khiển chi tiết hơn, điều hướng đến **Target Group** của bạn
5. Vào phần **Attributes** của target group
6. Nhấp **Edit**
7. Cấu hình cross-zone load balancing với các tùy chọn:
   - Kế thừa cài đặt từ thuộc tính load balancer (bật mặc định)
   - Bắt buộc bật
   - Bắt buộc tắt cho target group cụ thể

## Các Trường Hợp Sử Dụng

### Khi Nào Nên Bật Cross-Zone Load Balancing
- Bạn có số lượng instances không đồng đều giữa các AZ
- Bạn muốn phân phối traffic đều bất kể AZ nào
- Bạn ưu tiên cân bằng tải hơn chi phí data transfer (cho NLB/GWLB)

### Khi Nào Nên Tắt Cross-Zone Load Balancing
- Bạn muốn giảm thiểu chi phí data transfer giữa các AZ
- Bạn có instances phân phối đều trên các AZ
- Kiến trúc của bạn yêu cầu traffic ở lại trong cùng AZ
- Bạn muốn kiểm tra tính độc lập của AZ

## Những Điểm Chính

1. **Cross-zone load balancing phân phối traffic đến tất cả instances trong tất cả các AZ**
2. **Không có nó, traffic chỉ đi đến instances trong cùng AZ với load balancer node**
3. **Các loại load balancer khác nhau có cài đặt mặc định và chi phí khác nhau**
4. **ALB có tính năng này bật mặc định và không tính phí thêm**
5. **NLB và GWLB có nó tắt mặc định và tính phí data transfer khi bật**
6. **Không có câu trả lời đúng hay sai - tùy thuộc vào trường hợp sử dụng của bạn**

## Dọn Dẹp

Sau khi hoàn thành thực hành, nhớ xóa các load balancers để tránh phí không cần thiết.

## Kết Luận

Cross-zone load balancing là một tính năng linh hoạt cho phép bạn kiểm soát cách traffic được phân phối trên cơ sở hạ tầng của bạn. Hiểu rõ hành vi, chi phí và các tùy chọn cấu hình cho từng loại load balancer sẽ giúp bạn đưa ra lựa chọn đúng đắn cho trường hợp sử dụng cụ thể của mình.