# Phương Pháp Luận 15-Factor: Nguyên Tắc Sáu Đến Mười

## Tổng Quan

Tài liệu này bao gồm các nguyên tắc từ 6 đến 10 của phương pháp luận 15-factor để xây dựng microservices cloud-native với Spring Boot. Những hướng dẫn này tập trung vào các khía cạnh vận hành bao gồm logging, disposability, backing services, environment parity và administrative processes.

---

## 6. Logs (Nhật Ký)

### Thách Thức
Trong các ứng dụng monolithic truyền thống, logs được ghi vào các file tại các vị trí cụ thể trên server. Khi có vấn đề xảy ra, developers phải truy cập thủ công vào các file log này để điều tra. Tuy nhiên, cách tiếp cận này không hiệu quả với kiến trúc microservices khi bạn có thể có hàng trăm services chạy trên nhiều servers.

### Nguyên Tắc
Việc định tuyến và lưu trữ log **không phải** là mối quan tâm của ứng dụng. Ứng dụng không nên ghi logs vào các thư mục hoặc vị trí cụ thể.

### Cách Hoạt Động
1. **Standard Output**: Ứng dụng chỉ đơn giản chuyển hướng logs ra standard output (stdout)
2. **Sequential Events**: Logs được xử lý như các sự kiện tuần tự theo thời gian
3. **External Tool**: Một công cụ log aggregator xử lý việc lưu trữ và rotation logs
4. **Centralized Access**: Log aggregator thu thập, tập hợp và cung cấp quyền truy cập vào tất cả logs để debugging

### Kiến Trúc
```
Accounts Microservice  ──┐
                         ├──> Standard Output ──> Log Aggregator Tool
Loans Microservice     ──┤                         (Lưu Trữ Tập Trung)
                         │                                  │
Cards Microservice     ──┘                                  ↓
                                                    UI Đơn Để Tìm Kiếm
```

### Lợi Ích
- ✅ Quản lý log tập trung cho tất cả microservices
- ✅ Dễ dàng tìm kiếm và debug từ một giao diện duy nhất
- ✅ Không cần truy cập từng server riêng lẻ
- ✅ Đơn giản hóa log rotation và retention policies
- ✅ Tương quan sự kiện tốt hơn giữa các services

### Triển Khai
- Ứng dụng sử dụng các logging framework chuẩn
- Logs được in ra standard output
- Các công cụ log aggregator bên ngoài (ví dụ: ELK Stack, Splunk, CloudWatch) thu thập và index logs
- Operations và development teams truy cập logs thông qua dashboard thống nhất

### Nội Dung Khóa Học
Khóa học này bao gồm một phần riêng biệt trình bày cách triển khai log aggregation, đưa logs từ tất cả microservices vào một công cụ tập trung với UI duy nhất để tìm kiếm và phân tích.

---

## 7. Disposability (Khả Năng Hủy Bỏ)

### Cách Tiếp Cận Truyền Thống vs. Cloud-Native

**Ứng Dụng Monolithic Truyền Thống:**
- Ưu tiên hàng đầu: Giữ ứng dụng luôn chạy
- Không có chỗ cho việc terminate hoặc stop
- Yêu cầu giám sát thủ công

**Ứng Dụng Cloud-Native:**
- Ứng dụng được coi là **ephemeral** (tạm thời)
- Nhiều instances chạy trên các môi trường
- Thay thế và scaling tự động

### Nguyên Tắc
Ứng dụng nên được thiết kế cho **disposability** - chúng có thể được start hoặc stop khi cần thiết mà không gây ra vấn đề.

### Khả Năng Chính

#### 1. Phục Hồi Tự Động
- Các instances không phản hồi có thể bị terminate và thay thế tự động
- Các nền tảng như Kubernetes xử lý điều này mà không cần can thiệp thủ công

#### 2. Auto-Scaling
- Trong thời gian tải cao, các instances bổ sung được spin up tự động
- Khi tải giảm, các instances được shutdown để tiết kiệm tài nguyên

#### 3. Fast Startup (Khởi Động Nhanh)
- Khởi động nhanh cho phép hệ thống linh hoạt
- Đảm bảo tính vững chắc và khả năng phục hồi
- Quan trọng để xử lý workloads động

#### 4. Graceful Shutdown (Tắt Máy Nhẹ Nhàng)
Khi shutdown, ứng dụng phải:
- ✅ Ngừng chấp nhận requests mới
- ✅ Xử lý thành công tất cả requests đang thực hiện
- ✅ Hoàn thành các operations đang chờ
- ✅ Trả jobs về worker queues (đối với worker processes)
- ✅ Thoát sạch sẽ

### Công Nghệ Hỗ Trợ

**Spring Boot + Docker:**
- Tạo và hủy microservices trong vòng **vài giây**

**Virtual Machines Truyền Thống:**
- Mất 10-15 phút để start/stop
- Không phù hợp cho dynamic scaling

### Tích Hợp Kubernetes
Khi sử dụng Docker containers với Kubernetes orchestrator:
- Tự động đáp ứng yêu cầu disposability
- Health checks và restart policies tự động
- Scaling và load balancing liền mạch
- Rolling updates không downtime

### Thực Hành Tốt Nhất
- Thiết kế cho stateless operations khi có thể
- Sử dụng external storage cho state (databases, caches)
- Implement health check endpoints
- Xử lý SIGTERM signals cho graceful shutdown
- Giữ startup time tối thiểu

### Nội Dung Khóa Học
Khóa học này sử dụng Docker ngay từ đầu và giới thiệu Kubernetes vào cuối khóa, chạy tất cả microservices trong Kubernetes cluster để đạt được true disposability.

---

## 8. Backing Services (Dịch Vụ Hỗ Trợ)

### Định Nghĩa
Backing services là các tài nguyên bên ngoài mà microservices của bạn phụ thuộc vào:
- Databases (MySQL, PostgreSQL, MongoDB)
- SMTP servers
- FTP servers
- Caching systems (Redis, Memcached)
- Message brokers (RabbitMQ, Kafka)
- Third-party APIs

### Nguyên Tắc
Xử lý backing services như **attached resources** có thể được sửa đổi hoặc thay thế mà không cần thay đổi code ứng dụng.

### Resource Binding
Kết nối với backing services được thực hiện thông qua **resource binding**, cung cấp:
- URL/endpoint
- Username
- Password
- Các tham số kết nối khác

Những thông tin này nên được cung cấp thông qua **externalized configurations**, không hardcode trong ứng dụng.

### Ví Dụ: Chuyển Đổi Database

Trong suốt vòng đời phát triển phần mềm, các databases khác nhau thường được sử dụng:
- **Development**: Local database hoặc H2
- **Testing**: QA database
- **Production**: Production database

Bằng cách xử lý databases như attached resources, bạn có thể chuyển đổi giữa chúng chỉ bằng cách thay đổi cấu hình:

```
Cùng Docker Image + Cấu Hình Khác Nhau:
├── Development  → Local Database (chỉ đổi config)
├── Testing      → QA Database (chỉ đổi config)
└── Production   → Production Database (chỉ đổi config)
```

### Không Cần Rebuild
- ❌ **Không Nên**: Rebuild Docker image cho mỗi môi trường
- ✅ **Nên**: Sử dụng cùng Docker image với các cấu hình bên ngoài khác nhau

### Chuyển Đổi Backing Services
```
Application
    ├── Local Database (development)
    ├── AWS RDS (testing)
    └── Azure SQL (production)
    
Chỉ thay đổi cấu hình - không thay đổi code!
```

### Lợi Ích
- ✅ Linh hoạt môi trường
- ✅ Dễ dàng thay thế dịch vụ
- ✅ Đơn giản hóa disaster recovery
- ✅ Độc lập với vendor
- ✅ Testing với các providers khác nhau

### Triển Khai
- Sử dụng Spring profiles cho các cấu hình theo môi trường
- Externalize tất cả connection details
- Sử dụng environment variables hoặc configuration servers
- Không bao giờ hardcode credentials hoặc URLs

---

## 9. Environment Parity (Sự Tương Đồng Môi Trường)

### Nguyên Tắc
Giảm thiểu sự khác biệt giữa các môi trường khác nhau và tránh các shortcuts tốn kém. Làm cho tất cả môi trường (development, testing, production) giống nhau nhất có thể.

### Tại Sao Quan Trọng
Khi môi trường trông giống nhau:
- ✅ Ứng dụng hoạt động nhất quán
- ✅ Ít bugs theo môi trường hơn
- ✅ Dễ debugging và troubleshooting hơn
- ✅ Giảm vấn đề "works on my machine"

### Ba Khoảng Cách Cần Giải Quyết

#### 1. Time Gap (Khoảng Cách Thời Gian)
**Vấn Đề**: Thời gian dài giữa code development và production deployment

**Giải Pháp**:
- Áp dụng CI/CD pipelines
- Implement continuous deployment
- Tự động hóa toàn bộ quy trình deployment
- Giảm thời gian từ development đến production

**Lợi Ích**:
- Feedback loops nhanh hơn
- Môi trường được đồng bộ hóa
- Debugging dễ dàng hơn

#### 2. People Gap (Khoảng Cách Con Người)
**Vấn Đề**: Developers xây dựng ứng dụng, nhưng operations teams deploy riêng biệt

**Giải Pháp**:
- Áp dụng **văn hóa DevOps**
- Thúc đẩy sự hợp tác giữa developers và operators
- Tuân theo triết lý: **"You build it, you run it"**

**Lợi Ích**:
- Phối hợp tốt hơn
- Trách nhiệm được chia sẻ
- Ít vấn đề handoff hơn
- Giải quyết vấn đề nhanh hơn

#### 3. Tools Gap (Khoảng Cách Công Cụ)
**Vấn Đề**: Các công cụ và backing services khác nhau giữa các môi trường

**Ví Dụ Thực Hành Xấu**:
```
❌ Development:  H2 Database
❌ Production:   PostgreSQL
```

**Tại Sao Thất Bại**:
- Code được tối ưu hóa cho H2 có thể không hoạt động với PostgreSQL
- Các SQL dialects khác nhau gây ra vấn đề
- Đặc điểm hiệu suất khác nhau
- Bugs chỉ xuất hiện ở production

**Giải Pháp**:
```
✅ Development:  PostgreSQL 14.5
✅ Testing:      PostgreSQL 14.5
✅ Production:   PostgreSQL 14.5
```

### Thực Hành Tốt Nhất
- Sử dụng cùng backing services trên tất cả môi trường
- Duy trì cùng phiên bản của tools và services
- Sử dụng containers để đảm bảo tính nhất quán
- Tự động hóa provisioning môi trường
- Document cấu hình môi trường
- Đồng bộ môi trường thường xuyên

### Lợi Ích
- ✅ Hành vi nhất quán giữa các môi trường
- ✅ Ít bất ngờ ở production hơn
- ✅ Debugging dễ dàng hơn
- ✅ Giảm bugs liên quan đến môi trường
- ✅ Chu kỳ deployment nhanh hơn

---

## 10. Administrative Processes (Quy Trình Quản Trị)

### Định Nghĩa
Administrative processes là các tác vụ quản lý cần thiết để hỗ trợ ứng dụng:
- Database migrations
- Batch jobs để dọn dẹp dữ liệu
- Cập nhật và chuyển đổi dữ liệu
- One-time scripts
- Maintenance tasks

### Nguyên Tắc
Administrative và management tasks nên được xử lý như **isolated processes**, tách biệt với application processes.

### Yêu Cầu Chính

#### 1. Version Control
- Code cho administrative tasks phải được version controlled
- Theo dõi thay đổi giống như application code
- Duy trì lịch sử của migrations và scripts

#### 2. Packaging
- Đóng gói administrative tasks cùng với ứng dụng
- Deploy chúng vào cùng môi trường
- Đảm bảo chúng có sẵn khi cần

#### 3. Execution Environment
- Chạy trong cùng môi trường với ứng dụng
- Sử dụng cùng runtime và dependencies
- Truy cập cùng backing services

### Anti-Pattern Phổ Biến
❌ **Không Bỏ Qua Ở Môi Trường Thấp Hơn**

Developers đôi khi bỏ qua việc chạy administrative tasks ở dev/QA để tiết kiệm thời gian:
- Bỏ qua database migrations
- Không chạy batch jobs
- Bỏ qua maintenance tasks
- Deploy trực tiếp vào production

**Kết Quả**: Thất bại bất ngờ ở production!

### Thực Hành Tốt Nhất

#### Tùy Chọn 1: Independent Microservices (Được Khuyến Nghị)
```
Business Logic Microservice  ──> Chạy liên tục
                                 Phục vụ clients

Administrative Microservice  ──> Chạy một lần
                                 Hủy bỏ khi xong
```

**Lợi Ích**:
- ✅ Tách biệt concerns rõ ràng
- ✅ Có thể hủy bỏ sau khi thực thi
- ✅ Không làm phình to ứng dụng chính
- ✅ Scaling và monitoring độc lập

**Tại Sao Hiệu Quả**:
- Tránh mang logic administrative không cần thiết trong microservice
- Main service chạy liên tục không bị overhead
- Administrative tasks thực thi khi cần và terminate

#### Tùy Chọn 2: Designated Endpoints
Administrative tasks có thể được tích hợp trực tiếp vào ứng dụng:
- Kích hoạt bằng cách gọi các endpoints cụ thể
- Vẫn được tách biệt logic
- Có thể disable ở production

**Lưu Ý**: Mặc dù khả thi, deploy như independent microservices được ưu tiên hơn.

### Ví Dụ

**Database Migration**:
```
Migration Service:
  1. Chạy schema updates
  2. Migrate data
  3. Validate migration
  4. Exit/terminate
```

**Data Cleanup Batch Job**:
```
Cleanup Service:
  1. Xác định records cũ
  2. Archive/delete data
  3. Log results
  4. Exit/terminate
```

### Lợi Ích
- ✅ Kiến trúc sạch
- ✅ Hiệu quả tài nguyên
- ✅ Testing tốt hơn
- ✅ Hành vi nhất quán trên các môi trường
- ✅ Version control đúng đắn
- ✅ Rollback dễ dàng hơn

---

## Tóm Tắt

Các nguyên tắc 6-10 của phương pháp luận 15-factor tập trung vào sự xuất sắc trong vận hành:

### 6. Logs
- Định tuyến logs ra standard output
- Sử dụng external log aggregators
- Tìm kiếm và debug tập trung

### 7. Disposability
- Thiết kế cho fast startup và graceful shutdown
- Cho phép automatic scaling
- Sử dụng Docker + Kubernetes cho ephemeral instances

### 8. Backing Services
- Xử lý external dependencies như attached resources
- Chuyển đổi services qua cấu hình
- Không cần thay đổi code

### 9. Environment Parity
- Giảm thiểu sự khác biệt giữa các môi trường
- Giải quyết time, people và tools gaps
- Sử dụng cùng backing services ở mọi nơi

### 10. Administrative Processes
- Xử lý như isolated, independent processes
- Version control và package với ứng dụng
- Deploy như separate microservices khi có thể

---

## Implementation Stack

Các nguyên tắc này được triển khai trong suốt khóa học bằng cách sử dụng:
- **Spring Boot**: Fast startup và framework support
- **Docker**: Container-based deployment
- **Kubernetes**: Orchestration và auto-scaling
- **Log Aggregators**: Centralized logging solutions
- **Spring Cloud Config**: Externalized configuration
- **CI/CD Pipelines**: Automated deployment

---

## Bước Tiếp Theo

Chúng ta đã đề cập đến 10 trong số 15 nguyên tắc. Trong bài giảng tiếp theo, chúng ta sẽ thảo luận về năm hướng dẫn cuối cùng để hoàn thiện hiểu biết của chúng ta về phương pháp luận 15-factor cho cloud-native microservices.

---

**Key Takeaway**: Những nguyên tắc vận hành này đảm bảo microservices của bạn sẵn sàng cho production, có khả năng mở rộng và dễ bảo trì trong môi trường cloud.