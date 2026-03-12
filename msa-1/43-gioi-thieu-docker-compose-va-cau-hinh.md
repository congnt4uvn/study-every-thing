# Giới Thiệu Docker Compose và Cấu Hình

## Tổng Quan
Trong bài học này, chúng ta sẽ khám phá Docker Compose, một công cụ mạnh mẽ giải quyết thách thức quản lý nhiều microservices. Chúng ta sẽ học cách định nghĩa và cấu hình tất cả microservices trong một file YAML duy nhất và khởi động chúng chỉ bằng một lệnh.

## Vấn Đề: Quản Lý Nhiều Microservices

### Thách Thức Hiện Tại

Với ba microservices của chúng ta (Accounts, Loans và Cards), chúng ta đối mặt với nhiều vấn đề:

- **Tạo Container Thủ Công:** Phải chạy lệnh `docker run` riêng biệt cho mỗi microservice
- **Nhiều Instances:** Khởi động nhiều instances yêu cầu chạy lệnh nhiều lần
- **Tốn Thời Gian:** Quản lý 100 microservices sẽ yêu cầu 100 lệnh riêng biệt
- **Dễ Sai Sót:** Thực thi thủ công tăng khả năng mắc lỗi
- **Không Mở Rộng Được:** Cách tiếp cận này không khả thi cho môi trường production

### Ví Dụ Cách Tiếp Cận Thủ Công

```bash
docker run -p 8080:8080 eazybytes/accounts:S4
docker run -p 8090:8090 eazybytes/loans:S4
docker run -p 9000:9000 eazybytes/cards:S4
```

## Giải Pháp: Docker Compose

### Docker Compose Là Gì?

**Docker Compose** là công cụ để định nghĩa và chạy ứng dụng Docker đa container. Với Compose, bạn có thể:

- ✅ Sử dụng file YAML để cấu hình tất cả các services của ứng dụng
- ✅ Tạo và khởi động tất cả services chỉ bằng một lệnh
- ✅ Quản lý services trên các môi trường khác nhau (production, staging, development, testing)
- ✅ Làm việc liền mạch với CI/CD pipelines

### Lợi Ích Chính

1. **Khởi động, dừng và rebuild services** dễ dàng
2. **Xem trạng thái của các services đang chạy** ở một nơi
3. **Stream log output** từ tất cả services
4. **Chạy các lệnh một lần** trên các services
5. **Đơn giản hóa việc điều phối microservices**

## Cài Đặt Docker Compose

### Xác Minh

Docker Compose được cài đặt tự động với Docker Desktop. Xác minh cài đặt:

```bash
docker compose version
```

**Ví Dụ Output:**
```
Docker Compose version v2.x.x
```

### Cài Đặt Thủ Công

Nếu Docker Compose chưa được cài đặt, truy cập [trang cài đặt Docker Compose chính thức](https://docs.docker.com/compose/install/) và làm theo hướng dẫn cho hệ điều hành của bạn.

## Tạo Cấu Hình Docker Compose

### Bước 1: Tạo File docker-compose.yml

Tạo file có tên `docker-compose.yml` trong thư mục dự án của bạn (ví dụ: trong project accounts microservice):

```yaml
# Vị trí file: /accounts/docker-compose.yml
```

**Lưu Ý:** Extension `.yml` là bắt buộc vì cấu hình ở định dạng YAML.

### Bước 2: Định Nghĩa Services

#### Cấu Trúc Cơ Bản

```yaml
services:
  accounts:
    image: "eazybytes/accounts:S4"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank
```

### Cấu Hình docker-compose.yml Đầy Đủ

```yaml
services:
  accounts:
    image: "eazybytes/accounts:S4"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

  loans:
    image: "eazybytes/loans:S4"
    container_name: loans-ms
    ports:
      - "8090:8090"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

  cards:
    image: "eazybytes/cards:S4"
    container_name: cards-ms
    ports:
      - "9000:9000"
    deploy:
      resources:
        limits:
          memory: 700m
    networks:
      - eazybank

networks:
  eazybank:
    driver: bridge
```

## Phân Tích Cấu Hình

### 1. Phần Services

Phần tử gốc chứa tất cả các định nghĩa service:

```yaml
services:
  # Tất cả microservices được định nghĩa ở đây
```

### 2. Các Phần Tử Cấu Hình Service

#### Image
Chỉ định Docker image sử dụng:
```yaml
image: "eazybytes/accounts:S4"
```

#### Container Name
Gán tên có ý nghĩa cho container:
```yaml
container_name: accounts-ms
```

**Tại Sao Quan Trọng?**
- Không có điều này, Docker gán tên ngẫu nhiên (ví dụ: "angry_cannon")
- Giúp nhận diện container dễ dàng hơn
- Cải thiện quản lý và debug

#### Port Mapping
Ánh xạ cổng container sang cổng host:
```yaml
ports:
  - "8080:8080"  # host:container
```

**Định Dạng:** `"<cổng-host>:<cổng-container>"`

Nhiều ánh xạ cổng (nếu cần):
```yaml
ports:
  - "8080:8080"
  - "8081:8081"
```

#### Giới Hạn Memory
Hạn chế phân bổ memory tối đa:
```yaml
deploy:
  resources:
    limits:
      memory: 700m
```

**Lợi Ích:**
- Ngăn một service tiêu thụ toàn bộ memory hệ thống
- Đảm bảo phân phối tài nguyên công bằng
- Quan trọng cho hệ thống có RAM hạn chế (ví dụ: 16GB)

#### Networks
Gắn thẻ services vào một mạng chung:
```yaml
networks:
  - eazybank
```

**Mục Đích:**
- Cho phép giao tiếp giữa các services
- Không có điều này, services chạy trong mạng cô lập
- Bắt buộc cho microservices cần giao tiếp với nhau

### 3. Phần Networks

Định nghĩa mạng tùy chỉnh ở cấp độ gốc:

```yaml
networks:
  eazybank:
    driver: bridge
```

**Cấu Hình Mạng:**
- **Tên:** `eazybank` (có thể là bất kỳ tên nào)
- **Driver:** `bridge` - tạo mạng bridge cho giao tiếp service

## Quy Tắc Cú Pháp YAML

### Thụt Lề
YAML dựa vào thụt lề chính xác (sử dụng khoảng trắng, không phải tab):

```yaml
services:           # Cấp độ gốc (không thụt lề)
  accounts:         # 2 khoảng trắng
    image: "..."    # 4 khoảng trắng
    ports:          # 4 khoảng trắng
      - "8080:8080" # 6 khoảng trắng (mục danh sách với dấu gạch ngang)
```

### Danh Sách
Sử dụng dấu gạch ngang (-) cho các mục danh sách:

```yaml
ports:
  - "8080:8080"
  - "8081:8081"

networks:
  - eazybank
```

### Cặp Key-Value
Sử dụng dấu hai chấm (:) theo sau bởi khoảng trắng:

```yaml
image: "eazybytes/accounts:S4"
container_name: accounts-ms
```

## Cấu Trúc Phân Cấp Cấu Hình

```
services (gốc)
├── accounts (tên service)
│   ├── image
│   ├── container_name
│   ├── ports
│   ├── deploy
│   │   └── resources
│   │       └── limits
│   │           └── memory
│   └── networks
├── loans (tên service)
│   └── ... (cùng cấu trúc)
└── cards (tên service)
    └── ... (cùng cấu trúc)

networks (gốc)
└── eazybank
    └── driver
```

## Tại Sao Cấu Hình Mạng Quan Trọng

### Không Có Cấu Hình Mạng
- Mỗi service chạy trong mạng cô lập riêng
- Không thể giao tiếp giữa các services
- Services không thể khám phá lẫn nhau

### Có Cấu Hình Mạng
- Tất cả services chia sẻ cùng mạng (`eazybank`)
- Bridge driver cho phép giao tiếp
- Services có thể giao tiếp sử dụng tên container làm hostname
- Hỗ trợ các phụ thuộc service trong tương lai

## Thực Hành Tốt Nhất

### 1. Vị Trí File
- Đặt `docker-compose.yml` ở vị trí trung tâm
- Check vào version control (GitHub)
- Giữ cùng với các microservices liên quan

### 2. Đặt Tên Container
- Sử dụng tên mô tả với hậu tố: `-ms` (microservice)
- Ví dụ: `accounts-ms`, `loans-ms`, `cards-ms`
- Tránh tên ngẫu nhiên do Docker tạo

### 3. Giới Hạn Tài Nguyên
- Luôn đặt giới hạn memory trong production
- Ngăn cạn kiệt tài nguyên
- Điều chỉnh dựa trên yêu cầu service

### 4. Chiến Lược Mạng
- Sử dụng mạng tùy chỉnh cho các services liên quan
- Sử dụng bridge driver cho cấu hình đơn giản
- Lập kế hoạch cho nhu cầu giao tiếp service trong tương lai

### 5. Image Tags
- Sử dụng tags cụ thể (ví dụ: `S4`) thay vì `latest`
- Đảm bảo tính nhất quán phiên bản
- Tạo điều kiện cho rollbacks

## Hỗ Trợ IDE

### IntelliJ IDEA
- Plugin YAML cung cấp syntax highlighting
- Hỗ trợ tự động thụt lề
- Xác thực cấu trúc YAML

### VS Code
- Extension Docker cung cấp IntelliJ
- Extension YAML cho hỗ trợ cú pháp
- Hỗ trợ ngôn ngữ Docker Compose

## Chuẩn Bị Cho Triển Khai

### Trạng Thái Hiện Tại
✅ File Docker Compose đã tạo  
✅ Ba microservices đã được cấu hình  
✅ Thiết lập mạng hoàn tất  
✅ Giới hạn memory đã định nghĩa  
✅ Ánh xạ cổng đã thiết lập  

### Các Bước Tiếp Theo
Trong bài học tiếp theo, chúng ta sẽ học cách:
- Khởi động tất cả microservices với một lệnh duy nhất
- Xác minh trạng thái service
- Quản lý các container đang chạy
- Xem logs từ tất cả services

## Tóm Tắt

Trong bài học này, chúng ta đã đề cập:
- ✅ Thách thức quản lý nhiều microservices thủ công
- ✅ Giới thiệu Docker Compose và lợi ích của nó
- ✅ Cài đặt và xác minh Docker Compose
- ✅ Tạo file cấu hình `docker-compose.yml`
- ✅ Cấu hình services (image, ports, memory, networks)
- ✅ Thiết lập mạng tùy chỉnh cho giao tiếp giữa các services
- ✅ Cú pháp YAML và quy tắc thụt lề
- ✅ Thực hành tốt nhất cho cấu hình Docker Compose

Docker Compose đơn giản hóa quản lý microservices bằng cách thay thế nhiều lệnh thủ công bằng một file cấu hình khai báo duy nhất.

---

**Bài Học Tiếp Theo:** Khởi động tất cả microservices với một lệnh Docker Compose duy nhất.