# AWS VPC và Subnets - Giới Thiệu

## Tổng Quan

Hướng dẫn này cung cấp phần giới thiệu về Amazon Virtual Private Cloud (VPC) và subnets, những khái niệm mạng cơ bản trong AWS.

## VPC là gì?

**VPC (Virtual Private Cloud)** là một mạng riêng trong AWS cloud cho phép bạn triển khai các tài nguyên của mình. Đặc điểm chính:

- VPC là **tài nguyên cấp vùng (regional resource)**
- Mỗi vùng AWS có thể có các VPC khác nhau
- VPC là cấu trúc logic chứa hạ tầng mạng của bạn

## Hiểu Về Subnets

**Subnets** cho phép bạn phân vùng mạng bên trong VPC:

- Subnets được định nghĩa ở **cấp độ availability zone (AZ)**
- Bạn có thể có nhiều subnets trong một VPC
- Có hai loại subnets chính:

### Public Subnets (Mạng Con Công Khai)

- Có thể truy cập từ internet
- Có thể truy cập World Wide Web
- Có thể được truy cập từ World Wide Web
- Thường chứa các tài nguyên cần truy cập internet (ví dụ: web servers)

### Private Subnets (Mạng Con Riêng Tư)

- Không thể truy cập từ internet
- Cung cấp bảo mật và quyền riêng tư cao hơn
- Lý tưởng cho các tài nguyên backend như cơ sở dữ liệu
- Các tài nguyên vẫn có thể truy cập internet thông qua NAT gateways

## Route Tables (Bảng Định Tuyến)

**Route tables** định nghĩa cách lưu lượng mạng di chuyển giữa các subnets:

- Kiểm soát quyền truy cập internet và giữa các subnets
- Xác định điều gì làm cho một subnet công khai hay riêng tư
- Mỗi subnet được liên kết với một route table

## Kiến Trúc VPC

Một kiến trúc VPC điển hình bao gồm:

- **CIDR Range**: Một tập hợp các dải IP được phép trong VPC của bạn
- **Nhiều Availability Zones**: Để đảm bảo tính sẵn sàng cao
- **Public và Private Subnets**: Trong mỗi AZ
- **EC2 Instances**: Được triển khai trong các subnets phù hợp

### Ví Dụ Kiến Trúc

```
Vùng (Region)
└── VPC (với CIDR range)
    ├── Availability Zone 1
    │   ├── Public Subnet
    │   └── Private Subnet
    └── Availability Zone 2
        ├── Public Subnet
        └── Private Subnet
```

## Default VPC (VPC Mặc Định)

Khi bạn bắt đầu sử dụng AWS:

- AWS tạo một **default VPC** trong mỗi vùng
- Chỉ chứa các public subnets
- Một public subnet cho mỗi availability zone
- Sẵn sàng sử dụng ngay lập tức

## Internet Gateways (Cổng Internet)

**Internet Gateway (IGW)** cho phép các instances trong VPC kết nối với internet:

- Nằm trong VPC của bạn
- Public subnets có tuyến đường trực tiếp đến internet gateway
- Định tuyến này làm cho subnet trở thành "công khai"
- Cho phép giao tiếp hai chiều với internet

## NAT Gateways và NAT Instances

**NAT (Network Address Translation)** gateways cho phép các instances trong private subnet truy cập internet trong khi vẫn giữ tính riêng tư:

### NAT Gateway vs NAT Instance

| Tính Năng | NAT Gateway | NAT Instance |
|-----------|-------------|--------------|
| Quản lý | Được AWS quản lý | Tự quản lý |
| Cung cấp | Tự động | Thủ công |
| Mở rộng | Tự động | Thủ công |

### Cách NAT Hoạt Động

1. NAT gateway/instance được triển khai trong **public subnet**
2. Private subnet tạo tuyến đường đến NAT gateway/instance
3. NAT gateway định tuyến đến internet gateway
4. Private instances có thể truy cập internet mà không bị truy cập trực tiếp từ internet

### Luồng Kiến Trúc

```
Private Subnet → NAT Gateway (trong Public Subnet) → Internet Gateway → Internet
```

## Các Trường Hợp Sử Dụng

- **Public Subnets**: Web servers, application load balancers, bastion hosts
- **Private Subnets**: Cơ sở dữ liệu, application servers, Lambda functions
- **NAT Gateways**: Cho phép cập nhật phần mềm cho các private instances

## Những Điểm Chính Cần Nhớ

- VPCs cung cấp môi trường mạng cô lập trong AWS
- Subnets phân vùng VPC của bạn ở cấp độ AZ
- Public subnets có tuyến đường trực tiếp đến internet gateway
- Private subnets sử dụng NAT cho truy cập internet đi ra
- Route tables kiểm soát tất cả luồng lưu lượng mạng
- Hạ tầng này là nền tảng cho các triển khai AWS an toàn

## Các Bước Tiếp Theo

Tiếp tục tìm hiểu về các khái niệm VPC bổ sung bao gồm:
- Security Groups (Nhóm Bảo Mật)
- Network ACLs (Danh Sách Kiểm Soát Truy Cập Mạng)
- VPC Peering (Kết Nối VPC)
- VPN Connections (Kết Nối VPN)
- Direct Connect (Kết Nối Trực Tiếp)

---

*Lưu ý: Đây là phần tổng quan ở mức độ cao. Các hướng dẫn thực hành chi tiết hơn sẽ được đề cập trong các bài giảng tiếp theo.*