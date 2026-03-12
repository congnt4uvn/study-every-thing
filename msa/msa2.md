
================================================================================
FILE: 1-mysql-database-integration.md
================================================================================

# Tích Hợp Cơ Sở Dữ Liệu MySQL cho Microservices

## Tổng Quan

Phần này tập trung vào việc di chuyển các microservices từ cơ sở dữ liệu H2 in-memory sang cơ sở dữ liệu MySQL để sẵn sàng cho môi trường production. Cơ sở dữ liệu H2 không được khuyến nghị cho các dự án thực tế hoặc ứng dụng production, do đó việc di chuyển này rất quan trọng cho các triển khai doanh nghiệp.

## Yêu Cầu Tiên Quyết

- Docker Desktop đã được cài đặt và đang chạy
- Ba microservices: accounts (tài khoản), loans (khoản vay), và cards (thẻ)
- Kiến thức về Spring Boot application
- Hiểu biết cơ bản về lệnh Docker

## Thiết Lập Dự Án

### 1. Cấu Trúc Thư Mục Dự Án

Tạo một thư mục section mới (Section 7) và sao chép codebase hiện có:

```
Section 7/
├── accounts/
├── loans/
├── cards/
├── configserver/
└── docker-compose/
```

Sao chép code từ `v2-spring-cloud-config` vào thư mục Section 7 mới.

### 2. Xóa Dependencies Spring Cloud Bus

Trước khi tích hợp MySQL, hãy xóa các dependencies Spring Cloud Bus và Config Monitor để giảm tải hệ thống và đơn giản hóa kiến trúc.

#### Thay Đổi Config Server

**pom.xml** - Xóa các dependencies:
- `spring-cloud-starter-bus-amqp`
- `spring-cloud-config-monitor`

**application.yml** - Xóa:
- Các thuộc tính kết nối RabbitMQ
- Giữ lại các thuộc tính actuator management để refresh thủ công
- Giữ lại cấu hình readiness và liveness probe

#### Thay Đổi Microservices (accounts, loans, cards)

Cho mỗi microservice:

**pom.xml** - Xóa:
- `spring-cloud-starter-bus-amqp`

**application.yml** - Xóa:
- Các thuộc tính kết nối RabbitMQ

## Thiết Lập Cơ Sở Dữ Liệu MySQL với Docker

### Tại Sao Dùng Docker cho MySQL?

- **Không cần cài đặt thủ công** - Tránh tiêu tốn dung lượng đĩa
- **Thiết lập nhanh** - Cơ sở dữ liệu sẵn sàng trong dưới 10 giây
- **Dễ dàng dọn dẹp** - Chỉ cần dừng/xóa containers khi hoàn tất
- **Môi trường cô lập** - Mỗi container chạy trong hệ sinh thái riêng

### Tạo MySQL Containers

#### 1. Cơ Sở Dữ Liệu Accounts

```bash
docker run -p 3306:3306 --name accountsdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=accountsdb -d mysql
```

**Giải thích các tham số:**
- `-p 3306:3306` - Ánh xạ cổng (host:container)
- `--name accountsdb` - Tên container
- `-e MYSQL_ROOT_PASSWORD=root` - Mật khẩu user root
- `-e MYSQL_DATABASE=accountsdb` - Tạo database khi khởi động
- `-d` - Chế độ detached (chạy nền)
- `mysql` - Tên Docker image

#### 2. Cơ Sở Dữ Liệu Loans

```bash
docker run -p 3307:3306 --name loansdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=loansdb -d mysql
```

**Lưu ý:** Cổng 3307 được sử dụng trên host vì 3306 đã bị accountsdb chiếm dụng.

#### 3. Cơ Sở Dữ Liệu Cards

```bash
docker run -p 3308:3306 --name cardsdb -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsdb -d mysql
```

### Khái Niệm Quan Trọng về Ánh Xạ Cổng

- **Cổng nội bộ container** (3306): Giống nhau cho tất cả containers do mạng bị cô lập
- **Cổng ngoại vi host** (3306, 3307, 3308): Phải là duy nhất trên hệ thống local
- Mỗi container có hệ sinh thái mạng cô lập riêng
- Ánh xạ cổng bên ngoài cho phép các microservices local kết nối

## Xác Minh Kết Nối Cơ Sở Dữ Liệu

### Sử Dụng SQLElectron Client

SQLElectron là một SQL client nhẹ, đa nền tảng hỗ trợ nhiều loại cơ sở dữ liệu.

**Tải về:** [https://sqlectron.github.io/](https://sqlectron.github.io/)

### Cấu Hình Kết Nối

#### Cơ Sở Dữ Liệu Accounts
- **Địa chỉ Server:** localhost
- **Cổng:** 3306
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** accountsdb

#### Cơ Sở Dữ Liệu Loans
- **Địa chỉ Server:** localhost
- **Cổng:** 3307
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** loansdb

#### Cơ Sở Dữ Liệu Cards
- **Địa chỉ Server:** localhost
- **Cổng:** 3308
- **Tên người dùng:** root
- **Mật khẩu:** root
- **Database:** cardsdb

## Thực Hành Tốt Nhất

### Mẫu Database cho Mỗi Microservice

Mỗi microservice nên có cơ sở dữ liệu riêng để đảm bảo:
- **Cô lập dữ liệu** - Không có phụ thuộc dữ liệu giữa các services
- **Mở rộng độc lập** - Mở rộng databases dựa trên nhu cầu của từng service
- **Cô lập lỗi** - Vấn đề trong một database không ảnh hưởng đến các database khác
- **Linh hoạt công nghệ** - Các microservices khác nhau có thể sử dụng công nghệ database khác nhau

### Development vs Production

- **Development:** Sử dụng Docker containers cho MySQL databases local
- **Production:** Sử dụng các dịch vụ database được quản lý bởi đội ngũ infrastructure
- **QA/Dev Servers:** Kết nối đến các database servers dùng chung do đội ngũ infrastructure cung cấp

## Khắc Phục Sự Cố

### Lỗi Cổng Đã Được Sử Dụng

**Vấn đề:** `failed to start because port 3306 is already being used`

**Giải pháp:** Sử dụng cổng host khác (ví dụ: 3307, 3308) trong khi giữ cổng container là 3306

### Tên Container Đã Tồn Tại

**Vấn đề:** `container name already exists`

**Giải pháp:** Xóa container hiện có và thử lại
```bash
docker rm <tên-container>
```

## Cân Nhắc về Yêu Cầu Hệ Thống

- **Hệ thống 8GB RAM:** Cần lưu ý khi chạy nhiều containers
- **Hệ thống 16GB+ RAM:** Hiệu suất tốt hơn với nhiều containers
- Xóa các dependencies không cần thiết (như RabbitMQ) giúp giảm tải hệ thống

## Các Bước Tiếp Theo

Giai đoạn tiếp theo bao gồm:
1. Sửa đổi code microservice để kết nối với MySQL databases
2. Cấu hình các thuộc tính Spring Boot cho MySQL
3. Thiết lập JPA/Hibernate cho MySQL
4. Tạo database schemas và tables
5. Kiểm thử microservices với MySQL backend

## Tóm Tắt

- Di chuyển từ H2 sang MySQL để sẵn sàng cho production
- Sử dụng Docker để thiết lập và quản lý MySQL dễ dàng
- Tạo ba databases riêng biệt cho ba microservices
- Xóa các dependencies Spring Cloud Bus để tối ưu hóa việc sử dụng tài nguyên
- Xác minh kết nối database bằng SQLElectron client
- Sẵn sàng tích hợp MySQL với code microservices

---

**Thời lượng:** Thiết lập nhanh (dưới 10 giây mỗi database)  
**Độ khó:** Cơ bản đến Trung cấp  
**Công nghệ:** Docker, MySQL, Spring Boot, Microservices



================================================================================
FILE: 10-client-side-service-discovery-pattern.md
================================================================================

# Mô Hình Service Discovery Phía Client Trong Microservices

## Tổng Quan

Trong kiến trúc microservices, service discovery (khám phá dịch vụ) cùng với service registration (đăng ký dịch vụ) giải quyết các vấn đề khi thiết lập giao tiếp nội bộ giữa các dịch vụ. Có hai cách tiếp cận khác nhau để triển khai service discovery:

1. **Client-Side Service Discovery** (Khám phá dịch vụ phía client)
2. **Server-Side Service Discovery** (Khám phá dịch vụ phía server)

Tài liệu này tập trung vào mô hình client-side service discovery và cách nó hoạt động trong microservices Spring Boot.

## Client-Side Service Discovery Là Gì?

Trong cách tiếp cận client-side service discovery, các ứng dụng chịu trách nhiệm:
- Tự đăng ký với service registry khi khởi động
- Hủy đăng ký khi tắt
- Truy vấn service registry để khám phá các dịch vụ khác
- Triển khai logic cân bằng tải để chọn instance dịch vụ

### Đặc Điểm Chính

Trách nhiệm chọn instance nào của dịch vụ backend để giao tiếp nằm ở **microservice client**. Đó là lý do được gọi là khám phá dịch vụ "phía client".

## Cách Hoạt Động

### Bước 1: Thiết Lập Service Registry

Trước khi khởi động microservices, service registry phải chạy như một server riêng biệt trong mạng microservice của bạn.

### Bước 2: Đăng Ký Dịch Vụ

Khi các instance microservice khởi động (ví dụ: hai instance của loans microservice):
- Mỗi instance kết nối với service registry
- Chúng đăng ký thông tin chi tiết: địa chỉ IP, hostname và số cổng
- Chúng gửi các **tín hiệu heartbeat** đều đặn để xác nhận tình trạng sức khỏe

### Bước 3: Khám Phá Dịch Vụ

Khi một client microservice (ví dụ: accounts microservice) muốn giao tiếp với dịch vụ khác (ví dụ: loans microservice):
1. Accounts microservice truy vấn service registry để lấy thông tin loans microservice
2. Service registry xác thực yêu cầu
3. Registry trả về danh sách tất cả địa chỉ IP khả dụng của loans microservice

### Bước 4: Cân Bằng Tải

Client microservice nhận được nhiều địa chỉ IP và:
- Áp dụng chiến lược cân bằng tải (round-robin, weighted round-robin, least connections, hoặc tùy chỉnh)
- Chuyển tiếp yêu cầu đến một instance được chọn
- Tự xử lý logic cân bằng tải

## Ưu Điểm

### 1. Chiến Lược Cân Bằng Tải Linh Hoạt

Bạn có thể chọn từ nhiều thuật toán:
- **Round Robin**: Phân phối yêu cầu đều trên các instance
- **Weighted Round Robin**: Gán trọng số cho các instance khác nhau
- **Least Connections**: Định tuyến đến instance có ít kết nối hoạt động nhất
- **Custom Algorithms**: Triển khai logic của riêng bạn

### 2. Kiểm Soát Phía Client

Client có toàn quyền kiểm soát việc chọn dịch vụ và quyết định định tuyến.

## Nhược Điểm

### 1. Tăng Trách Nhiệm Cho Developer

Developers phải:
- Thay đổi code trong từng microservice
- Triển khai giao tiếp với service registration
- Xử lý logic cân bằng tải

### 2. Yêu Cầu Hạ Tầng

Bạn cần duy trì một server tập trung cho:
- Đăng ký dịch vụ
- Hỗ trợ khám phá dịch vụ

## So Sánh Client-Side vs Server-Side Discovery

### Server-Side Discovery

- Sử dụng khi triển khai microservices trong môi trường **Kubernetes**
- Yêu cầu đội operations và platform chuyên dụng
- Chi phí hạ tầng cao hơn
- Tốt hơn cho các dự án có ngân sách và nguồn lực

### Client-Side Discovery

- Phù hợp cho các dự án không thể chi trả cho việc bảo trì Kubernetes cluster
- Phát triển server tập trung riêng cho service registration
- Developer tham gia nhiều hơn nhưng chi phí hạ tầng thấp hơn

## Kiến Trúc Service Discovery Layer

### Các Thành Phần

Service discovery layer bao gồm:
- Nhiều service discovery nodes (có thể triển khai bao nhiêu tùy theo tải)
- Không cần bảo trì địa chỉ IP thủ công
- Đồng bộ tự động giữa các nodes

### Giao Thức Gossip

Khi một microservice đăng ký với một service discovery node:
- Thông tin chi tiết được chia sẻ ngay lập tức với các nodes khác thông qua **giao thức gossip**
- Tất cả nodes duy trì thông tin đồng bộ và cập nhật
- Đảm bảo tính nhất quán trên toàn service discovery layer

### Luồng Giao Tiếp

1. Microservices đăng ký khi khởi động với IP, hostname và cổng
2. Tín hiệu heartbeat đều đặn duy trì trạng thái sức khỏe
3. Client microservices truy vấn bằng tên dịch vụ logic (ví dụ: "accounts", "loans")
4. Service discovery layer trả về danh sách địa chỉ IP
5. Client thực hiện cân bằng tải và gọi dịch vụ đích

## Client-Side Caching

### Chiến Lược Cache

Để giảm gánh nặng cho service discovery layer:
1. Client microservices cache địa chỉ IP sau lần truy vấn đầu tiên
2. Các yêu cầu tiếp theo sử dụng địa chỉ IP đã cache
3. Cache tự động làm mới mỗi 10-20 giây
4. Cache invalidation xảy ra ngay lập tức khi có exception

### Lợi Ích

- Giảm tải cho service discovery layer
- Thời gian phản hồi nhanh hơn cho các yêu cầu tiếp theo
- Quản lý cache tự động ở hậu trường

### Cache Invalidation

Khi giao tiếp thất bại:
- Cache phía client bị vô hiệu hóa ngay lập tức
- Thông tin địa chỉ IP mới được lấy từ service discovery layer
- Đảm bảo kết nối với các instance dịch vụ khỏe mạnh

## Triển Khai Với Spring Cloud

Spring Cloud cung cấp các công cụ đơn giản và mạnh mẽ để triển khai client-side service discovery trong microservices Spring Boot. Framework tự động xử lý hầu hết độ phức tạp:

- Không cần code thủ công logic đăng ký dịch vụ
- Cơ chế caching tích hợp sẵn
- Tự động làm mới và vô hiệu hóa cache
- Tích hợp với các giải pháp service discovery phổ biến

### Yêu Cầu Cho Developer

Developers chỉ cần:
- Biết các dự án Spring Cloud nào cần sử dụng
- Cấu hình chúng đúng cách trong microservices
- Hiểu mô hình và kiến trúc tổng thể

## Ví Dụ Thực Tế

### Kịch Bản

- **Accounts microservice** cần giao tiếp với **Loans** và **Cards** microservices
- Nhiều instances của mỗi dịch vụ đang chạy

### Luồng Hoạt Động

1. Tất cả microservices đăng ký với service discovery layer khi khởi động
2. Accounts microservice kiểm tra cache cục bộ cho thông tin loans microservice
3. Nếu cache miss, truy vấn service discovery layer
4. Nhận danh sách địa chỉ IP và cache chúng
5. Áp dụng chiến lược cân bằng tải
6. Chuyển tiếp yêu cầu đến instance được chọn
7. Sử dụng địa chỉ đã cache cho các yêu cầu tương lai

### Khả Năng Mở Rộng

Trong production với 100+ microservices:
- Mỗi dịch vụ có thể có 10+ instances
- Client-side caching ngăn không làm quá tải service discovery layer
- Tự động làm mới cache đảm bảo thông tin cập nhật
- Xử lý exception kích hoạt cache invalidation ngay lập tức

## Kết Luận

Client-side service discovery cung cấp một mô hình linh hoạt và mạnh mẽ cho giao tiếp microservices. Mặc dù yêu cầu developer tham gia nhiều hơn so với server-side discovery, nó mang lại:

- Chi phí hạ tầng thấp hơn
- Kiểm soát tốt hơn về cân bằng tải
- Hiệu suất xuất sắc với client-side caching
- Triển khai đơn giản với Spring Cloud

Mô hình hoạt động trơn tru ở hậu trường khi được cấu hình đúng cách, cho phép developers tập trung vào logic nghiệp vụ thay vì lo lắng về hạ tầng.

---

**Bước Tiếp Theo**: Chi tiết triển khai với các dự án Spring Cloud và ví dụ cấu hình sẽ được đề cập trong các bài giảng tiếp theo.



================================================================================
FILE: 11-implementing-client-side-service-discovery-with-spring-cloud.md
================================================================================

# Triển Khai Client-Side Service Discovery với Spring Cloud

## Tổng Quan

Tài liệu này trình bày cách triển khai thực tế client-side service discovery trong kiến trúc microservices sử dụng các thành phần Spring Cloud. Chúng ta sẽ khám phá các công nghệ và thư viện chính cần thiết để triển khai service discovery và registration.

## Các Thành Phần Chính

### 1. Spring Cloud Netflix Eureka

**Eureka** đóng vai trò như một service discovery agent trung tâm, chịu trách nhiệm:
- Đăng ký dịch vụ (Service registration)
- Khám phá dịch vụ (Service discovery)
- Hoạt động như máy chủ trung tâm để quản lý các instance microservice

### 2. Spring Cloud Load Balancer

Thư viện này cung cấp khả năng **cân bằng tải phía client**, thay thế thư viện Netflix Ribbon cũ. Nó cho phép:
- Phân phối tải động giữa các service instance
- Định tuyến thông minh dựa trên sức khỏe của service
- Tích hợp liền mạch với hệ sinh thái Spring Cloud

### 3. Netflix Feign Client (Spring Cloud OpenFeign)

Feign client được sử dụng cho **giao tiếp giữa các service**, tương tự như REST Template và WebClient trong Spring Framework cốt lõi. Nó cung cấp:
- Giao diện REST client khai báo (declarative)
- Đơn giản hóa việc sử dụng HTTP client
- Tích hợp dễ dàng với service discovery

## Các Giải Pháp Thay Thế

Mặc dù chúng ta sử dụng các thành phần Spring Cloud, nhưng có các lựa chọn thay thế trong ngành:

**Thay Thế Service Discovery:**
- Etcd
- Consul
- Apache Zookeeper

**Thay Thế Load Balancing:**
- Netflix Ribbon (hiện đang ở chế độ bảo trì)

> **Lưu ý:** Chúng ta chọn các thành phần Spring Cloud vì chúng tích hợp liền mạch trong hệ sinh thái Spring, giúp việc phát triển dễ dàng hơn khi sử dụng Spring Boot.

## Tại Sao Lại Có Tên Netflix?

Tên "Netflix" trong Spring Cloud Netflix có một câu chuyện thú vị:

### Câu Chuyện

1. **2007:** Netflix bắt đầu xây dựng các dịch vụ cloud-native và phát triển các thư viện nội bộ:
   - **Ribbon** - cho cân bằng tải
   - **Eureka** - cho service discovery
   - **Hystrix** - cho fault tolerance
   - **Governator** - để điều phối tất cả các thành phần

2. **2012:** Netflix mã nguồn mở các thư viện này, đóng góp cho cộng đồng Spring

3. **2015:** Nhóm Spring tạo ra dự án **Spring Cloud Netflix**, ghi nhận đóng góp của Netflix bằng cách đưa tên họ vào

4. **2018:** Chính Netflix bắt đầu sử dụng Spring Boot làm framework Java cốt lõi, tận dụng Spring Cloud Netflix một cách rộng rãi

### Stack Hiện Tại Của Netflix

Netflix đã phát triển stack của họ từ thiết lập ban đầu sang:
- **Spring Boot** làm framework cốt lõi
- **Spring Cloud Load Balancer** (thay thế Ribbon)
- **Spring Cloud Eureka** cho service discovery
- **Resilience4j** (thay thế Hystrix) cho fault tolerance

## Lợi Ích Của Client-Side Service Discovery

Triển khai client-side service discovery mang lại nhiều ưu điểm:

1. **Không Có Giới Hạn Về Tính Khả Dụng**
   - Có thể triển khai nhiều service discovery node
   - Giao tiếp ngang hàng (peer-to-peer) giữa các service

2. **Cấu Hình Động**
   - Địa chỉ IP và cấu hình load balancer có thể thay đổi động
   - Cấu hình tự động cập nhật ở hậu trường
   - Không cần can thiệp thủ công

3. **Khả Năng Chịu Lỗi và Phục Hồi**
   - Giao tiếp vẫn mạnh mẽ ngay cả khi service bị lỗi
   - Các pattern retry tự động và circuit breaker
   - Suy giảm dịch vụ một cách duyên dáng (graceful degradation)

## Tóm Tắt Technology Stack

Cho việc triển khai microservices của chúng ta, chúng ta sẽ sử dụng:

- ✅ **Spring Cloud Load Balancer** - cho client-side load balancing
- ✅ **Spring Cloud Netflix Eureka** - cho service discovery
- ✅ **Spring Cloud OpenFeign** - cho giao tiếp giữa các service
- ✅ **Resilience4j** - cho fault tolerance (sẽ đề cập trong các bài giảng sau)

## Tại Sao Stack Này?

Các thành phần này:
- **Đã được chứng minh trong ngành:** Được Netflix sử dụng để xử lý lượng traffic khổng lồ
- **Được bảo trì tích cực:** Cập nhật và cải tiến thường xuyên
- **Hiện đại:** Phiên bản mới nhất với các best practices hiện tại
- **Tích hợp tốt:** Tích hợp liền mạch trong hệ sinh thái Spring

## Kết Luận

Triển khai client-side service discovery với các thành phần Spring Cloud cung cấp một giải pháp mạnh mẽ, có khả năng mở rộng và dễ bảo trì cho kiến trúc microservices. Sự kết hợp của Eureka, Spring Cloud Load Balancer và OpenFeign tạo ra một nền tảng mạnh mẽ để xây dựng các hệ thống phân tán có khả năng phục hồi.

Trong các bài giảng tiếp theo, chúng ta sẽ triển khai các thành phần này từng bước một và thấy việc thiết lập service discovery trong mạng microservices Spring Boot dễ dàng như thế nào.

## Tài Liệu Tham Khảo

- [Spring Cloud Project](https://spring.io/projects/spring-cloud)
- [Spring Cloud Netflix](https://spring.io/projects/spring-cloud-netflix)
- [Spring Cloud OpenFeign](https://spring.io/projects/spring-cloud-openfeign)
- [Netflix Tech Blog - Spring Boot](https://netflixtechblog.com/)



================================================================================
FILE: 12-building-eureka-service-discovery-server.md
================================================================================

# Xây Dựng Eureka Service Discovery Server với Spring Cloud

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập một service discovery agent (tác nhân khám phá dịch vụ) sử dụng Eureka từ dự án Spring Cloud Netflix. Đây là một phần trong việc xây dựng kiến trúc microservices cho ứng dụng Eazy Bank.

## Yêu Cầu Trước

- Java 17
- Maven
- Spring Boot (phiên bản ổn định mới nhất)
- Các microservices đã có (accounts, loans, cards)
- Config Server đã được thiết lập

## Thiết Lập Ban Đầu

### 1. Tạo Cấu Trúc Dự Án

Tạo một thư mục mới `section 8` trong workspace của bạn và sao chép code từ `section 6 v2` (sử dụng H2 database thay vì MySQL).

### 2. Dọn Dẹp Dependencies

Xóa các dependencies không cần thiết như Spring Cloud Bus và RabbitMQ khỏi tất cả microservices:

**Từ `pom.xml`:**
- Xóa dependency `spring-cloud-bus`
- Xóa dependency `spring-cloud-config-monitor`

**Từ `application.yml`:**
- Xóa tất cả các properties liên quan đến RabbitMQ

> **Lưu ý:** Thực hiện việc dọn dẹp này cho Config Server, Accounts, Cards và Loans microservices để tránh các container không cần thiết có thể làm chậm hệ thống local của bạn.

## Tạo Eureka Server Project

### 1. Tạo Project Từ Spring Initializr

Truy cập [start.spring.io](https://start.spring.io) và cấu hình:

- **Project:** Maven
- **Language:** Java
- **Spring Boot:** Phiên bản ổn định mới nhất
- **Group:** com.eazybytes
- **Artifact:** eurekaserver
- **Name:** eurekaserver
- **Description:** Service discovery agent for Eazy Bank microservices
- **Package name:** Tự động điền dựa trên group và artifact
- **Packaging:** JAR
- **Java:** 17

### 2. Thêm Dependencies

Chọn các dependencies sau:

1. **Eureka Server** (KHÔNG phải Eureka Discovery Client)
2. **Config Client** - Để kết nối với Config Server
3. **Spring Boot Actuator** - Cho health checks

### 3. Import Vào Workspace

1. Generate và download project
2. Giải nén file zip vào thư mục `section 8`
3. Trong IntelliJ IDEA, vào tab Maven → Add Maven Projects → Chọn thư mục eurekaserver

## Cấu Hình Eureka Server

### 1. Bật Annotation Eureka Server

Trong class main application, thêm annotation `@EnableEurekaServer`:

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaserverApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaserverApplication.class, args);
    }
}
```

Annotation này chuyển đổi một Spring Boot project thông thường thành service discovery agent sử dụng thư viện Eureka.

### 2. Cấu Hình application.yml

Đổi tên `application.properties` thành `application.yml` và thêm cấu hình sau:

```yaml
spring:
  application:
    name: eurekaserver
  config:
    import: optional:configserver:http://localhost:8071

management:
  endpoints:
    web:
      exposure:
        include: "*"
  health:
    readinessstate:
      enabled: true
    livenessstate:
      enabled: true
  endpoint:
    health:
      probes:
        enabled: true
```

**Các Điểm Cấu Hình Quan Trọng:**

- **spring.application.name:** Phải khớp với tên file config trong Config Server
- **spring.config.import:** URL của Config Server để lấy properties
- **management.endpoints:** Expose tất cả actuator endpoints
- **health probes:** Bật readiness và liveness cho Docker health checks

### 3. Cấu Hình Properties Trong Config Server

Tạo file `eurekaserver.yml` trong GitHub config repository với nội dung sau:

```yaml
server:
  port: 8070

eureka:
  instance:
    hostname: localhost
  client:
    fetchRegistry: false
    registerWithEureka: false
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```

**Giải Thích Các Properties:**

- **server.port:** Eureka Server sẽ chạy trên port 8070
- **eureka.instance.hostname:** Hostname cho Eureka instance (localhost cho môi trường phát triển local)
- **eureka.client.fetchRegistry:** Đặt `false` vì Eureka Server không cần fetch registry details (nó là người duy trì chúng)
- **eureka.client.registerWithEureka:** Đặt `false` để ngăn Eureka Server tự đăng ký với chính nó
- **eureka.client.serviceUrl.defaultZone:** URL nơi Eureka Server expose chức năng của nó cho các microservices khác

> **Tại sao chỉ có một file config?** Không giống như các microservices khác, Eureka Server hoạt động giống nhau trên tất cả môi trường (dev, qa, prod) vì nó không phụ thuộc vào database credentials hay business logic phụ thuộc môi trường.

## Kiểm Tra Thiết Lập

### 1. Khởi Động Config Server

Khởi động Config Server trước vì Eureka Server phụ thuộc vào nó:

```bash
# Khởi động Config Server trên port 8071
```

### 2. Xác Minh Properties Từ Config Server

Truy cập Config Server để xác minh properties của Eureka đã được load:

```
http://localhost:8071/eurekaserver/default
```

Bạn sẽ thấy tất cả các Eureka-related properties mà bạn đã định nghĩa.

### 3. Khởi Động Eureka Server

Chạy main application class ở chế độ debug. Kiểm tra logs để xác nhận:
- Kết nối tới Config Server tại port 8071
- Load các default properties
- Server đã khởi động trên port 8070

### 4. Truy Cập Eureka Dashboard

Điều hướng tới:

```
http://localhost:8070
```

Bạn sẽ thấy Eureka Dashboard. Đây là UI được tích hợp sẵn do Spring Eureka Server cung cấp, hiển thị:
- System Status
- General Info
- Instance Info
- Registered Instances (hiện tại đang trống cho đến khi các microservices đăng ký)

## Tóm Tắt

Bạn đã thiết lập thành công một Eureka Service Discovery Server có các đặc điểm:
- ✅ Chạy trên port 8070
- ✅ Kết nối với Config Server để quản lý cấu hình tập trung
- ✅ Expose health check endpoints cho Docker orchestration
- ✅ Cung cấp dashboard để giám sát các services đã đăng ký

## Các Bước Tiếp Theo

Bước tiếp theo là thiết lập kết nối giữa các microservices riêng lẻ (accounts, loans, cards) và Eureka Service Discovery Server bằng cách:
1. Thêm Eureka Discovery Client dependency vào mỗi microservice
2. Cấu hình mỗi microservice để đăng ký với Eureka Server
3. Bật service-to-service communication thông qua service discovery

---

**Luồng Kiến Trúc:**
```
Microservices (accounts, loans, cards)
    ↓ (đăng ký với)
Eureka Server (port 8070)
    ↓ (lấy config từ)
Config Server (port 8071)
```



================================================================================
FILE: 13-implementing-eureka-client-in-accounts-microservice.md
================================================================================

# Triển Khai Eureka Client trong Accounts Microservice

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cấu hình accounts microservice để đăng ký với Eureka server nhằm thực hiện service discovery. Microservice sẽ tự động đăng ký trong quá trình khởi động và gửi heartbeat mỗi 30 giây để duy trì đăng ký.

## Yêu Cầu Tiên Quyết

Trước khi khởi động accounts microservice, hãy đảm bảo các dịch vụ sau đang chạy:
- Config Server
- Eureka Server (chạy trên cổng 8070)

## Bước 1: Thêm Dependency Eureka Client

Thêm dependency Eureka Discovery Client vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

**Quan trọng:** Chọn **Eureka Discovery Client**, không phải Eureka Server.

## Bước 2: Cấu Hình Application Properties

Thêm các cấu hình sau vào file `application.yml`:

### Cấu Hình Eureka Client

```yaml
eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/
```

**Chi Tiết Cấu Hình Quan Trọng:**

- **`preferIpAddress: true`**: Đăng ký microservice sử dụng địa chỉ IP thay vì hostname. Điều này rất quan trọng cho môi trường phát triển local không có DNS mapping.
- **`fetchRegistry: true`**: Cho phép microservice lấy thông tin registry khi giao tiếp với các microservice khác.
- **`registerWithEureka: true`**: Đảm bảo microservice đăng ký với Eureka server.
- **`serviceUrl.defaultZone`**: Chỉ định URL của Eureka server.

### Cấu Hình Thông Tin Ứng Dụng

Thêm metadata sẽ được hiển thị trong Eureka dashboard:

```yaml
info:
  app:
    name: accounts
    description: Eazy Bank Accounts Application
    version: 1.0.0
```

### Kích Hoạt Info Endpoint

Kích hoạt actuator info endpoint để expose metadata của ứng dụng:

```yaml
management:
  info:
    env:
      enabled: true
```

### Kích Hoạt Graceful Shutdown

Cấu hình shutdown endpoint để hủy đăng ký một cách graceful:

```yaml
management:
  endpoint:
    shutdown:
      enabled: true

endpoints:
  shutdown:
    enabled: true
```

**Lưu ý:** Cấu hình `endpoints` phải ở cấp root của file YAML, không nằm dưới `management`.

## Bước 3: Khởi Động Accounts Microservice

1. Build project
2. Khởi động ứng dụng ở chế độ debug
3. Microservice sẽ tự động:
   - Đăng ký với Eureka server (HTTP response 204 cho biết đăng ký thành công)
   - Bắt đầu gửi heartbeat mỗi 30 giây

## Bước 4: Xác Minh Đăng Ký

Truy cập Eureka dashboard tại `http://localhost:8070` để xác minh đăng ký.

### Những Gì Cần Kiểm Tra:

- **Tên Ứng Dụng**: Được liệt kê trong "Instances currently registered with Eureka" (khớp với thuộc tính `spring.application.name`)
- **Trạng Thái**: Nên hiển thị là "UP"
- **Chi Tiết Instance**: Click vào link instance để xem:
  - Tên ứng dụng
  - Mô tả
  - Phiên bản
  
URL của info endpoint sẽ có định dạng: `http://<địa-chỉ-ip>:8080/actuator/info`

## Hiểu Về Địa Chỉ IP vs Hostname

Khi bạn click vào instance trong Eureka dashboard, bạn có thể thấy một hostname khác thay vì "localhost". Đây là hành vi bình thường do Docker hoặc phần mềm khác tạo host entries cho địa chỉ IP localhost. Service discovery vẫn sẽ hoạt động chính xác với địa chỉ IP.

## Cảnh Báo Thường Gặp

Bạn có thể thấy thông báo cảnh báo: "Emergency! Eureka may be incorrectly claiming instances." Đây là cảnh báo phổ biến của Eureka dashboard và có thể bỏ qua trong quá trình phát triển. Khái niệm này sẽ được giải thích chi tiết trong các bài giảng tiếp theo.

## Cách Service Discovery Hoạt Động

1. **Khởi động**: Accounts microservice đăng ký với Eureka server
2. **Heartbeats**: Gửi tín hiệu heartbeat mỗi 30 giây để duy trì đăng ký
3. **Giao Tiếp Service**: Các microservice khác có thể khám phá accounts microservice thông qua Eureka server bằng địa chỉ IP
4. **Shutdown**: Trong quá trình graceful shutdown, microservice tự động hủy đăng ký khỏi Eureka

## Bài Tập

Áp dụng các thay đổi cấu hình tương tự cho **loans** và **cards** microservices để kích hoạt service discovery cho toàn bộ hệ sinh thái microservices.

## Điểm Chính Cần Nhớ

- Cấu hình Eureka client cho phép tự động đăng ký và khám phá service
- Sử dụng địa chỉ IP (thay vì hostname) là cần thiết cho môi trường phát triển local
- Metadata ứng dụng cải thiện khả năng hiển thị trong Eureka dashboard
- Cơ chế heartbeat đảm bảo theo dõi tính khả dụng của service
- Graceful shutdown đảm bảo hủy đăng ký sạch sẽ khỏi service registry

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ đề cập đến:
- Cấu hình loans và cards microservices
- Hiểu về thông báo cảnh báo emergency của Eureka
- Các pattern service discovery nâng cao



================================================================================
FILE: 14-registering-microservices-with-eureka-server.md
================================================================================

# Đăng Ký Microservices với Eureka Server

## Tổng Quan

Hướng dẫn này trình bày quy trình đăng ký các microservices Cards và Loans với Eureka Service Discovery server, hoàn thiện việc thiết lập đăng ký dịch vụ cho tất cả các microservices trong hệ thống.

## Yêu Cầu Tiên Quyết

- Eureka Server đang chạy trên cổng 8070
- Config Server đang chạy
- Microservice Accounts đã được đăng ký với Eureka
- Các microservices Cards và Loans sẵn sàng để cấu hình

## Các Bước Cấu Hình

### 1. Thêm Maven Dependencies

Thêm dependency Netflix Eureka Client vào cả hai microservices Cards và Loans:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

### 2. Cấu Hình application.yml cho Cards Microservice

Cập nhật file `application.yml` trong microservice Cards:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    shutdown:
      enabled: true
  info:
    env:
      enabled: true

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/

info:
  app:
    name: "cards"
    description: "Eazy Bank Cards Application"
```

### 3. Cấu Hình application.yml cho Loans Microservice

Tương tự, cập nhật file `application.yml` trong microservice Loans:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    shutdown:
      enabled: true
  info:
    env:
      enabled: true

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/

info:
  app:
    name: "loans"
    description: "Eazy Bank Loans Application"
```

## Khởi Động Microservices

1. Build cả hai microservices Cards và Loans
2. Đảm bảo Config Server và Eureka Server đang chạy
3. Khởi động microservice Cards (chạy trên cổng 9000)
4. Khởi động microservice Loans (chạy trên cổng 8090)

## Xác Thực

### Eureka Dashboard

Truy cập Eureka dashboard tại `http://localhost:8070` để xác minh tất cả microservices đã được đăng ký:

- Microservice Accounts
- Microservice Cards (cổng 9000)
- Microservice Loans (cổng 8090)

Mỗi microservice sẽ hiển thị thông tin chi tiết khi được nhấp vào.

### Eureka REST API

#### Lấy Tất Cả Ứng Dụng Đã Đăng Ký (Định Dạng XML)

```
GET http://localhost:8070/eureka/apps
```

Trả về tất cả các ứng dụng đã đăng ký và các instances của chúng ở định dạng XML theo mặc định.

#### Lấy Tất Cả Ứng Dụng Đã Đăng Ký (Định Dạng JSON)

Sử dụng Postman hoặc bất kỳ HTTP client nào:

```
GET http://localhost:8070/eureka/apps
Headers:
  Accept: application/json
```

**Response bao gồm:**
- Instance ID
- Hostname
- Tên ứng dụng
- Địa chỉ IP
- Trạng thái
- Số cổng
- Khoảng thời gian renewal
- Thời gian đăng ký
- Timestamp renewal cuối cùng
- Timestamp service khởi động
- Home page URL
- Status page URL
- Health check URL

#### Lấy Thông Tin Microservice Cụ Thể

Để lấy thông tin cho một microservice cụ thể:

```
GET http://localhost:8070/eureka/apps/accounts
GET http://localhost:8070/eureka/apps/cards
GET http://localhost:8070/eureka/apps/loans
```

Thêm header `Accept: application/json` để nhận response dạng JSON.

## Khái Niệm Chính

### Mô Hình Service Discovery và Registration

Việc triển khai tuân theo cách tiếp cận từng bước:

1. **Centralized Service Registry**: Eureka Server hoạt động như một server tập trung lưu trữ tất cả chi tiết service registry và hoạt động như một service discovery agent.

2. **Automatic Registration**: Tất cả microservices (Accounts, Cards, Loans) tự động đăng ký thông tin của chúng trong quá trình khởi động bằng cách bao gồm Eureka Client dependency và cấu hình phù hợp.

3. **Dynamic Service Discovery**: Các microservices có thể khám phá lẫn nhau mà không cần cấu hình địa chỉ IP thủ công, giúp giao tiếp nội bộ trở nên liền mạch.

4. **Hỗ Trợ Load Balancing**: Nhiều instances của cùng một microservice có thể được đăng ký, cho phép khả năng cân bằng tải.

## Lợi Ích Của Eureka Server

- **Tự Động Đăng Ký Service**: Không cần can thiệp thủ công để cập nhật địa chỉ IP trong registry
- **Khả Năng Mở Rộng**: Dễ dàng xử lý hàng trăm microservices
- **Cập Nhật Động**: Thông tin service được cập nhật tự động
- **Giám Sát Sức Khỏe Service**: Theo dõi trạng thái và tính khả dụng của service
- **Hỗ Trợ Nhiều Instance**: Quản lý nhiều instances cho mỗi microservice để đảm bảo tính sẵn sàng cao

## Thông Tin Instance Có Sẵn

Đối với mỗi instance đã đăng ký, Eureka cung cấp:
- Instance ID và hostname
- Tên ứng dụng và địa chỉ IP
- Trạng thái hiện tại và số cổng
- Khoảng thời gian renewal mặc định tính bằng giây
- Timestamp đăng ký
- Timestamp renewal cuối cùng
- Timestamp service khởi động
- URLs cho home page, status page và health check

## Các Bước Tiếp Theo

Với tất cả microservices đã được đăng ký thành công với Eureka Server, bây giờ bạn có thể triển khai:
- Client-side load balancing
- Giao tiếp giữa các microservices sử dụng tên service
- Các mô hình resilience với circuit breakers
- Tích hợp API Gateway

## Tóm Tắt

Hướng dẫn này đã trình bày cách đăng ký các microservices Cards và Loans với Eureka Server, hoàn thành việc thiết lập service discovery. Tất cả microservices giờ đây tự động đăng ký trong quá trình khởi động, cho phép khám phá service động và tạo điều kiện thuận lợi cho giao tiếp liền mạch giữa các microservices trong hệ thống phân tán.



================================================================================
FILE: 15-microservice-graceful-shutdown-and-deregistration.md
================================================================================

# Tắt Microservice Một Cách Linh Hoạt và Hủy Đăng Ký Khỏi Eureka Server

## Tổng Quan

Hướng dẫn này trình bày cách các microservice tự động hủy đăng ký khỏi Eureka Server trong quá trình tắt máy một cách linh hoạt, đảm bảo quản lý service registry đúng cách trong kiến trúc microservices Spring Boot.

## Yêu Cầu Trước

- Eureka Server đang chạy và được cấu hình
- Các microservice (Accounts, Loans, Cards) đã đăng ký với Eureka Server
- Spring Boot Actuator được cấu hình với shutdown endpoint
- Postman hoặc công cụ kiểm thử API tương tự

## Graceful Shutdown vs Forced Shutdown

### Forced Shutdown (Không Được Khuyến Nghị)
- Sử dụng nút stop của IDE (ví dụ: IntelliJ IDEA)
- Tắt ứng dụng ngay lập tức
- Không có quá trình hủy đăng ký
- **KHÔNG nên sử dụng trong các môi trường cao hơn (dev, qa, prod)**

### Graceful Shutdown (Được Khuyến Nghị)
- Sử dụng các script shutdown
- Sử dụng shutdown endpoint của Actuator
- Cho phép dọn dẹp và hủy đăng ký đúng cách
- **Thực hành chuẩn cho môi trường production**

## Cấu Hình

### Thiết Lập Actuator Shutdown Endpoint

Thêm các thuộc tính sau vào cấu hình microservices của bạn:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: shutdown
  endpoint:
    shutdown:
      enabled: true
```

Các thuộc tính này kích hoạt shutdown endpoint trong Spring Boot Actuator cho mỗi microservice (Accounts, Loans, Cards).

## Chi Tiết Shutdown Endpoint

### Thông Tin Endpoint
- **URL Pattern**: `http://localhost:{port}/actuator/shutdown`
- **HTTP Method**: POST (không cho phép phương thức GET)
- **Response**: Thông báo JSON xác nhận bắt đầu shutdown

### Các URL Ví Dụ
- Accounts Service: `http://localhost:8080/actuator/shutdown`
- Cards Service: `http://localhost:9000/actuator/shutdown`
- Loans Service: `http://localhost:8090/actuator/shutdown` (điều chỉnh port theo cấu hình)

## Quy Trình Hủy Đăng Ký

### Các Bước Shutdown Chi Tiết

1. **Khởi Động Shutdown**: Gửi POST request tới `/actuator/shutdown`
2. **Grace Period**: Ứng dụng dành thời gian để thực hiện các tác vụ dọn dẹp
3. **Hủy Đăng Ký**: Microservice tự hủy đăng ký khỏi Eureka Server
4. **Xác Nhận**: Eureka Server trả về HTTP status 200
5. **Hoàn Thành Shutdown**: Ứng dụng dừng một cách linh hoạt

### Response Mong Đợi
```json
{
  "message": "Shutting down, bye..."
}
```

## Demo: Tắt Các Microservice

### Tắt Accounts Microservice

1. Mở Postman
2. Điều hướng đến folder Accounts microservice
3. Chọn request "Shutdown"
4. Xác minh URL: `http://localhost:8080/actuator/shutdown`
5. Click nút "Send"
6. Quan sát response: "Shutting down, Bye bye"

### Các Bước Xác Minh

1. **Kiểm Tra Eureka Dashboard**
   - Refresh trang Eureka Server dashboard
   - Xác minh rằng AccountsApplication không còn trong danh sách
   - Xác nhận hủy đăng ký thành công

2. **Kiểm Tra Application Logs**
   ```
   Stopping service...
   Unregistering...
   Account deregistered from Eureka Server
   Status: 200 (Success)
   ```

### Tắt Cards Microservice

1. Trong Postman, điều hướng đến folder Cards
2. Chọn request "Shutdown"
3. Đảm bảo URL sử dụng port 9000: `http://localhost:9000/actuator/shutdown`
4. Click nút "Send"
5. Xác minh đã nhận được response

### Tắt Loans Microservice

1. Trong Postman, điều hướng đến folder Loans
2. Chọn request "Shutdown"
3. Click nút "Send"
4. Xác minh đã nhận được response

## Xác Thực và Kiểm Chứng

### Xác Minh Trên Eureka Dashboard
Sau khi tắt tất cả các microservice:
- Refresh Eureka Server dashboard
- **Không nên có instance nào khả dụng**
- Xác nhận tất cả microservices đã hủy đăng ký thành công

### Xác Minh Console Log

**Logs của Cards Microservice:**
```
Unregistering...
Status: 200 from Eureka Server
```

**Logs của Loans Microservice:**
```
Unregistering...
Status: 200 from Eureka Server
```

## Những Điểm Chính Cần Ghi Nhớ

### Đăng Ký và Hủy Đăng Ký Tự Động
- **Khởi động**: Microservices tự động đăng ký với Eureka Server
- **Tắt máy**: Microservices tự động hủy đăng ký trong quá trình graceful shutdown

### Ý Nghĩa Đối Với Service Discovery
- Không có entry trong service registry = Không thể service discovery
- Hủy đăng ký đúng cách ngăn chặn các entry service cũ
- Đảm bảo thông tin tình trạng service chính xác

### Best Practices (Thực Hành Tốt Nhất)
1. Luôn sử dụng graceful shutdown trong môi trường production
2. Không bao giờ force-kill microservices bằng nút stop của IDE trong các môi trường cao hơn
3. Theo dõi logs hủy đăng ký để đảm bảo hoàn thành thành công (HTTP status 200)
4. Triển khai các shutdown script phù hợp cho automated deployments

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

**Vấn đề**: Shutdown endpoint trả về 405 Method Not Allowed
- **Nguyên nhân**: Sử dụng GET thay vì POST
- **Giải pháp**: Sử dụng phương thức POST cho shutdown endpoint

**Vấn đề**: Không tìm thấy endpoint (404)
- **Nguyên nhân**: Actuator shutdown chưa được kích hoạt
- **Giải pháp**: Xác minh các thuộc tính cấu hình được thiết lập đúng

**Vấn đề**: Service vẫn xuất hiện trong Eureka Dashboard
- **Nguyên nhân**: Forced shutdown không có hủy đăng ký
- **Giải pháp**: Đợi lease expiration của Eureka hoặc restart Eureka Server

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- **Cơ Chế Heartbeat**: Cách các microservice gửi heartbeat tới Eureka Server
- **Giám Sát Sức Khỏe**: Cơ chế health check của Eureka Server
- **Lease Renewal**: Hiểu về quá trình lease expiration và renewal

## Kết Luận

Graceful shutdown và hủy đăng ký đúng cách là rất quan trọng để duy trì một hệ sinh thái microservices khỏe mạnh. Bằng cách sử dụng Actuator shutdown endpoint, các microservice có thể tự loại bỏ khỏi service registry một cách sạch sẽ, đảm bảo rằng các ứng dụng client không cố gắng định tuyến request đến các service không khả dụng.

---

**Các Chủ Đề Liên Quan:**
- Đăng Ký Service
- Cấu Hình Eureka Server
- Spring Boot Actuator
- Giám Sát Sức Khỏe Microservices



================================================================================
FILE: 16-microservice-heartbeat-and-eureka-server-communication.md
================================================================================

# Giao Tiếp Heartbeat và Eureka Server trong Microservice

## Tổng Quan

Tài liệu này trình bày cách các microservice gửi tín hiệu heartbeat đến Eureka Server và cách thức hoạt động tự động của quá trình đăng ký, cơ chế heartbeat, và hủy đăng ký trong kiến trúc microservices Spring Boot.

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá demo về các tín hiệu heartbeat được gửi bởi các microservice đến Eureka Server. Đây là một thành phần quan trọng của service discovery và giám sát sức khỏe trong hệ sinh thái microservices.

## Khởi Động Các Microservice

Để bắt đầu với demonstration này, chúng ta cần đảm bảo tất cả các microservice được khởi động theo thứ tự sau:

1. **Microservice Loans (Khoản vay)**
2. **Microservice Cards (Thẻ)**
3. **Microservice Accounts (Tài khoản)**

Khi các microservice này khởi động thành công, chúng sẽ tự động đăng ký thông tin instance của mình với Eureka Server ở chế độ nền.

## Xác Thực Đăng Ký

Bạn có thể xác thực việc đăng ký bằng cách truy cập dashboard Eureka:

1. Điều hướng đến dashboard Eureka
2. Làm mới trang
3. Xác minh rằng tất cả các instance hiện đang được đăng ký với Eureka

## Hiểu Về Cơ Chế Heartbeat

### Chu Kỳ Heartbeat Mặc Định

Các microservice cố gắng gửi tín hiệu heartbeat mỗi **30 giây** (chu kỳ mặc định) đến Eureka Server. Điều này đảm bảo Eureka Server chỉ duy trì thông tin của các instance khỏe mạnh.

### Demonstration Hành Vi Heartbeat

Để demonstration cơ chế heartbeat:

1. **Làm sạch console** của tất cả các microservice (accounts, loans, và cards)
2. **Dừng Eureka Server**
3. **Chờ 30 giây**
4. **Quan sát các exception** trong console của các microservice

## Hành Vi Mong Đợi Khi Eureka Server Bị Dừng

Khi Eureka Server bị dừng, bạn sẽ thấy các exception trong console của các microservice cho biết chúng đang cố gắng gửi heartbeat nhưng Eureka Server không phản hồi.

### Ví Dụ Về Log Messages

Trong console **AccountsApplication**, bạn sẽ tìm thấy:

- Các exception mới liên quan đến lỗi heartbeat
- Thông báo như: "was unable to send Heartbeat to Eureka Server"
- Các request PUT cố gắng cập nhật thông tin heartbeat tại URL của Eureka Server
- Lỗi do Eureka Server bị dừng

Hành vi tương tự có thể được quan sát thấy trong:
- Console **LoansApplication**
- Console **CardsApplication**

## Quản Lý Vòng Đời Service Tự Động

Tích hợp Eureka cung cấp quản lý tự động vòng đời của service:

### 1. Đăng Ký (Khởi Động)
- Trong quá trình khởi động, các microservice tự động đăng ký với Eureka Server
- Không cần can thiệp thủ công

### 2. Heartbeat (Thời Gian Chạy)
- Khi các service đã khởi động, heartbeat được gửi mỗi 30 giây
- Đảm bảo Eureka Server chỉ duy trì thông tin của các instance khỏe mạnh
- Giám sát sức khỏe tự động

### 3. Hủy Đăng Ký (Tắt)
- Trong quá trình shutdown, các microservice tự động hủy đăng ký
- Loại bỏ sạch sẽ khỏi service registry

## Điểm Chính Cần Nhớ

- **Giao Tiếp Tự Động**: Giao tiếp giữa các microservice và Eureka Server diễn ra tự động mà không cần can thiệp thủ công
- **Agent Service Discovery**: Eureka Server hoạt động như một agent service discovery
- **Service Registry**: Các microservice truyền thông tin instance của chúng đến Eureka Service Registry
- **Giám Sát Sức Khỏe**: Cơ chế heartbeat đảm bảo chỉ các service khỏe mạnh được duy trì trong registry

## Các Bước Tiếp Theo

Bây giờ chúng ta đã có:
- Eureka Server hoạt động như một agent service discovery
- Các microservice truyền thông tin instance của chúng đến Eureka Service Registry

Bước tiếp theo là hiểu:
- Cách một microservice có thể dựa vào Eureka Server để khám phá thông tin của các service khác
- Cách load balancing được thực hiện trong quá trình này

Các chủ đề này sẽ được đề cập trong bài giảng tiếp theo.

## Kết Luận

Tích hợp Eureka Server trong microservices Spring Boot cung cấp một cơ chế tự động mạnh mẽ cho việc đăng ký service, giám sát sức khỏe thông qua heartbeat, và hủy đăng ký. Nền tảng này là thiết yếu để xây dựng các kiến trúc microservices có khả năng mở rộng và linh hoạt.



================================================================================
FILE: 17-implementing-openfeign-client-for-microservice-communication.md
================================================================================

# Triển Khai OpenFeign Client Để Giao Tiếp Giữa Các Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai OpenFeign client trong kiến trúc microservices sử dụng Spring Boot để cho phép giao tiếp nội bộ giữa các microservice thông qua Eureka Server để khám phá dịch vụ.

## Kịch Bản

Chúng ta sẽ xây dựng một REST API mới trong **microservice accounts** với các chức năng:
- Thu thập thông tin liên quan đến tài khoản
- Lấy thông tin khoản vay từ microservice loans
- Lấy thông tin thẻ từ microservice cards
- Tổng hợp tất cả các phản hồi dựa trên số điện thoại di động
- Trả về dữ liệu khách hàng đầy đủ cho client

Microservice accounts cần giao tiếp nội bộ với các microservice cards và loans để lấy dữ liệu mà nó không có.

## Yêu Cầu Trước

- Eureka Server đang chạy
- Các microservice Accounts, Loans và Cards đã đăng ký với Eureka
- Cấu trúc dự án Maven

## Các Bước Triển Khai

### 1. Thêm Dependency OpenFeign

Truy cập [start.spring.io](https://start.spring.io) và thực hiện:
1. Chọn Maven làm công cụ build
2. Nhấp vào "Add dependency"
3. Tìm kiếm "OpenFeign"
4. Chọn dự án starter OpenFeign
5. Nhấp "Explore" và sao chép chi tiết dependency

Thêm dependency vào file `pom.xml` của microservice accounts (sau dependency Netflix Eureka Client):

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

Nhấp "Load Maven changes" để tải xuống các thư viện OpenFeign.

### 2. Kích Hoạt Feign Clients

Mở class Spring Boot chính (`AccountsApplication`) và thêm annotation `@EnableFeignClients`:

```java
@EnableFeignClients
@SpringBootApplication
public class AccountsApplication {
    // code hiện có
}
```

Annotation này kích hoạt chức năng Feign client, cho phép microservice accounts kết nối với các microservice khác.

### 3. So Sánh OpenFeign Với Cách Tiếp Cận Truyền Thống

**Cách Tiếp Cận Truyền Thống (REST Template/Web Client):**
- Yêu cầu viết code triển khai
- Xử lý thủ công URL, số cổng, dữ liệu request
- Logic xử lý exception tùy chỉnh

**Cách Tiếp Cận OpenFeign:**
- Chỉ cần code khai báo (tương tự Spring Data JPA)
- Không cần code triển khai
- Chỉ định nghĩa interface với các phương thức trừu tượng
- Framework tự động tạo implementation khi chạy

### 4. Tạo Các DTO

Sao chép các DTO cần thiết từ các microservice cards và loans:

**Từ Microservice Cards:**
- Sao chép class `CardsDto` vào package `com.eazybytes.accounts.dto`

**Từ Microservice Loans:**
- Sao chép class `LoansDto` vào package `com.eazybytes.accounts.dto`

### 5. Tạo Interface CardsFeignClient

Tạo package mới: `com.eazybytes.accounts.service.client`

Tạo interface `CardsFeignClient`:

```java
package com.eazybytes.accounts.service.client;

import com.eazybytes.accounts.dto.CardsDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(value = "cards")
public interface CardsFeignClient {
    
    @GetMapping(value = "/api/fetch", consumes = "application/json")
    CardsDto fetchCardDetails(@RequestParam String mobileNumber);
}
```

**Các Điểm Quan Trọng:**
- `@FeignClient(value = "cards")` - Sử dụng tên logic mà microservice cards đăng ký với Eureka Server
- Signature của phương thức phải khớp với REST API thực tế trong CardsController
- Không cần code triển khai - chỉ khai báo phương thức trừu tượng
- Bao gồm đường dẫn REST API đầy đủ (ví dụ: `/api/fetch`)

### 6. Tạo Interface LoansFeignClient

Tạo interface `LoansFeignClient` trong cùng package:

```java
package com.eazybytes.accounts.service.client;

import com.eazybytes.accounts.dto.LoansDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(value = "loans")
public interface LoansFeignClient {
    
    @GetMapping(value = "/api/fetch", consumes = "application/json")
    LoansDto fetchLoanDetails(@RequestParam String mobileNumber);
}
```

**Các Điểm Quan Trọng:**
- `@FeignClient(value = "loans")` - Sử dụng tên logic cho microservice loans
- Signature của phương thức khớp với fetch API trong LoansController
- Kiểu trả về là `LoansDto`
- Tham số request là `mobileNumber`

## Cách Hoạt Động

### Quy Trình Khám Phá Dịch Vụ

1. **Đăng Ký**: Các microservice cards và loans đăng ký với Eureka Server sử dụng tên logic ("cards" và "loans")

2. **Khám Phá**: Khi chạy, Feign client kết nối với Eureka Server và lấy chi tiết instance cho tên logic được chỉ định

3. **Lưu Cache**: Chi tiết instance được lưu cache trong 30 giây (thời gian mặc định)

4. **Cân Bằng Tải**: Trong khoảng thời gian cache 30 giây, Feign client sử dụng chi tiết IP đã lưu mà không kết nối lại với Eureka Server

5. **Gọi API**: Feign client gọi API đích với các tham số request được chỉ định

### Bên Trong Hoạt Động

OpenFeign tự động xử lý:
- Tạo code triển khai khi chạy
- Kết nối với Eureka Server để khám phá dịch vụ
- Phân giải địa chỉ IP của instance
- Serialization request/response
- Xử lý lỗi

## Yêu Cầu Cho Interface Feign Client

Khi tạo các interface Feign client, đảm bảo:

1. **Khớp Signature Phương Thức**: Tham số đầu vào, kiểu trả về và phương thức HTTP phải khớp với REST API thực tế
2. **Tên Logic**: Sử dụng cùng tên mà microservice đích dùng để đăng ký với Eureka
3. **Đường Dẫn Đầy Đủ**: Bao gồm toàn bộ đường dẫn REST API (cấp controller + cấp phương thức)
4. **Annotations**: Đánh dấu đúng với `@FeignClient`, `@GetMapping`/`@PostMapping`, v.v.
5. **Không Có Implementation**: Chỉ code khai báo - không có logic nghiệp vụ

## Lợi Ích Của OpenFeign

- **Phong Cách Khai Báo**: Tương tự Spring Data JPA - định nghĩa interface, không phải implementation
- **Giao Tiếp Đơn Giản**: Không cần quản lý REST template hoặc web client
- **Cân Bằng Tải Tích Hợp**: Cân bằng tải phía client thông qua tích hợp Eureka
- **Khám Phá Dịch Vụ Tự Động**: Tích hợp liền mạch với Eureka Server
- **Ít Code Boilerplate**: Code tối thiểu so với cách tiếp cận truyền thống

## Các Bước Tiếp Theo

Trong giai đoạn tiếp theo, bạn sẽ:
- Triển khai REST API mới trong microservice accounts
- Sử dụng Feign client để lấy dữ liệu từ các microservice cards và loans
- Tổng hợp các phản hồi và trả về thông tin khách hàng đầy đủ

## Tóm Tắt

OpenFeign cung cấp cách tiếp cận khai báo cho giao tiếp microservice, loại bỏ nhu cầu triển khai REST client thủ công. Bằng cách định nghĩa các interface với annotation và signature phương thức phù hợp, framework tự động tạo tất cả code triển khai cần thiết khi chạy, tích hợp liền mạch với Eureka Server để khám phá dịch vụ và cân bằng tải phía client.



================================================================================
FILE: 18-consolidated-customer-api-with-feign-client.md
================================================================================

# Xây Dựng API Tổng Hợp Thông Tin Khách Hàng Với Feign Client và Eureka

## Tổng Quan

Hướng dẫn toàn diện này trình bày cách xây dựng một API tổng hợp thông tin chi tiết khách hàng, tập hợp dữ liệu từ nhiều microservice sử dụng OpenFeign client và Eureka service discovery. Triển khai này thể hiện các pattern giao tiếp giữa các microservice trong kiến trúc Spring Boot microservices.

## Yêu Cầu Nghiệp Vụ

Tạo một endpoint API duy nhất trả về thông tin đầy đủ của khách hàng bao gồm:
- Thông tin cá nhân (tên, email, số điện thoại)
- Thông tin tài khoản
- Chi tiết khoản vay
- Thông tin thẻ

Dữ liệu được phân tán trên ba microservice:
- **Accounts Microservice**: Lưu trữ dữ liệu khách hàng và tài khoản
- **Loans Microservice**: Quản lý thông tin khoản vay
- **Cards Microservice**: Xử lý chi tiết thẻ

## Yêu Cầu Tiên Quyết

- Spring Cloud OpenFeign
- Spring Cloud Netflix Eureka Client
- Spring Boot Web
- Lombok
- H2 Database (cho môi trường phát triển)
- Config Server đang chạy
- Eureka Server đang chạy

## Triển Khai Từng Bước

### Bước 1: Tạo CustomerDetailsDto

Tạo một DTO toàn diện để lưu trữ dữ liệu tổng hợp từ cả ba microservice.

**File**: `src/main/java/com/easybank/accounts/dto/CustomerDetailsDto.java`

```java
package com.easybank.accounts.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(
    name = "CustomerDetails",
    description = "Schema để lưu thông tin khách hàng, tài khoản, thẻ và khoản vay"
)
public class CustomerDetailsDto {
    
    @Schema(description = "Tên của khách hàng", example = "Nguyễn Văn A")
    private String name;
    
    @Schema(description = "Địa chỉ email của khách hàng", example = "nguyenvana@example.com")
    private String email;
    
    @Schema(description = "Số điện thoại của khách hàng", example = "0123456789")
    private String mobileNumber;
    
    @Schema(description = "Thông tin tài khoản của khách hàng")
    private AccountsDto accountsDto;
    
    @Schema(description = "Thông tin khoản vay của khách hàng")
    private LoansDto loansDto;
    
    @Schema(description = "Thông tin thẻ của khách hàng")
    private CardsDto cardsDto;
}
```

**Điểm Chính**:
- Sử dụng annotation `@Data` của Lombok cho getter/setter
- Bao gồm annotation OpenAPI schema cho tài liệu API
- Kết hợp DTO từ cả ba microservice

### Bước 2: Tạo CustomerController

Xây dựng một REST controller mới dành riêng cho các thao tác khách hàng.

**File**: `src/main/java/com/easybank/accounts/controller/CustomerController.java`

```java
package com.easybank.accounts.controller;

import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.service.ICustomerService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@Tag(
    name = "REST API cho Khách hàng trong EasyBank",
    description = "REST APIs trong EasyBank để lấy thông tin chi tiết khách hàng"
)
@RestController
@RequestMapping(path = "/api", produces = {MediaType.APPLICATION_JSON_VALUE})
@Validated
public class CustomerController {
    
    private final ICustomerService iCustomerService;
    
    public CustomerController(ICustomerService iCustomerService) {
        this.iCustomerService = iCustomerService;
    }
    
    @Operation(
        summary = "API REST Lấy Thông Tin Chi Tiết Khách Hàng",
        description = "REST API để lấy thông tin chi tiết khách hàng dựa trên số điện thoại"
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "HTTP Status OK"
        ),
        @ApiResponse(
            responseCode = "500",
            description = "HTTP Status Internal Server Error"
        )
    })
    @GetMapping("/fetchCustomerDetails")
    public ResponseEntity<CustomerDetailsDto> fetchCustomerDetails(
            @RequestParam
            @Pattern(regexp = "(^$|[0-9]{10})", message = "Số điện thoại phải có 10 chữ số")
            String mobileNumber) {
        
        CustomerDetailsDto customerDetailsDto = 
            iCustomerService.fetchCustomerDetails(mobileNumber);
        return ResponseEntity
                .status(HttpStatus.OK)
                .body(customerDetailsDto);
    }
}
```

**Tính Năng Chính**:
- Constructor injection đơn (không cần `@Autowired`)
- Validation sử dụng `@Pattern` cho định dạng số điện thoại
- Annotation OpenAPI cho tài liệu Swagger
- RESTful endpoint tại `/api/fetchCustomerDetails`

### Bước 3: Định Nghĩa Interface ICustomerService

Tạo interface cho tầng service.

**File**: `src/main/java/com/easybank/accounts/service/ICustomerService.java`

```java
package com.easybank.accounts.service;

import com.easybank.accounts.dto.CustomerDetailsDto;

public interface ICustomerService {
    
    /**
     * Lấy thông tin chi tiết khách hàng bao gồm tài khoản, khoản vay và thẻ
     * @param mobileNumber - Số điện thoại đầu vào
     * @return CustomerDetailsDto - Thông tin khách hàng tổng hợp
     */
    CustomerDetailsDto fetchCustomerDetails(String mobileNumber);
}
```

### Bước 4: Triển Khai CustomerServiceImpl

Đây là nơi diễn ra điều kỳ diệu - điều phối các cuộc gọi đến nhiều microservice.

**File**: `src/main/java/com/easybank/accounts/service/impl/CustomerServiceImpl.java`

```java
package com.easybank.accounts.service.impl;

import com.easybank.accounts.dto.AccountsDto;
import com.easybank.accounts.dto.CardsDto;
import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.dto.LoansDto;
import com.easybank.accounts.entity.Accounts;
import com.easybank.accounts.entity.Customer;
import com.easybank.accounts.exception.ResourceNotFoundException;
import com.easybank.accounts.mapper.AccountsMapper;
import com.easybank.accounts.mapper.CustomerMapper;
import com.easybank.accounts.repository.AccountsRepository;
import com.easybank.accounts.repository.CustomerRepository;
import com.easybank.accounts.service.ICustomerService;
import com.easybank.accounts.service.client.CardsFeignClient;
import com.easybank.accounts.service.client.LoansFeignClient;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class CustomerServiceImpl implements ICustomerService {
    
    private AccountsRepository accountsRepository;
    private CustomerRepository customerRepository;
    private CardsFeignClient cardsFeignClient;
    private LoansFeignClient loansFeignClient;
    
    @Override
    public CustomerDetailsDto fetchCustomerDetails(String mobileNumber) {
        // Bước 1: Lấy khách hàng từ database local
        Customer customer = customerRepository.findByMobileNumber(mobileNumber)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Customer", "mobileNumber", mobileNumber));
        
        // Bước 2: Lấy tài khoản từ database local
        Accounts accounts = accountsRepository.findByCustomerId(customer.getCustomerId())
            .orElseThrow(() -> new ResourceNotFoundException(
                "Account", "customerId", customer.getCustomerId().toString()));
        
        // Bước 3: Ánh xạ customer và accounts sang DTO
        CustomerDetailsDto customerDetailsDto = CustomerMapper.mapToCustomerDetailsDto(
            customer, new CustomerDetailsDto());
        customerDetailsDto.setAccountsDto(
            AccountsMapper.mapToAccountsDto(accounts, new AccountsDto()));
        
        // Bước 4: Lấy khoản vay từ Loans microservice qua Feign Client
        ResponseEntity<LoansDto> loansDtoResponseEntity = 
            loansFeignClient.fetchLoanDetails(mobileNumber);
        customerDetailsDto.setLoansDto(loansDtoResponseEntity.getBody());
        
        // Bước 5: Lấy thẻ từ Cards microservice qua Feign Client
        ResponseEntity<CardsDto> cardsDtoResponseEntity = 
            cardsFeignClient.fetchCardDetails(mobileNumber);
        customerDetailsDto.setCardsDto(cardsDtoResponseEntity.getBody());
        
        return customerDetailsDto;
    }
}
```

**Điểm Nổi Bật Của Triển Khai**:
1. **Truy Cập Database Local**: Lấy dữ liệu khách hàng và tài khoản từ repository local
2. **Gọi Service Từ Xa**: Sử dụng Feign client để gọi Loans và Cards microservice
3. **Ánh Xạ Dữ Liệu**: Chuyển đổi entity sang DTO sử dụng các class mapper
4. **Xử Lý Exception**: Ném `ResourceNotFoundException` cho dữ liệu bị thiếu
5. **Dependency Injection**: Tất cả dependency được inject qua constructor

### Bước 5: Cập Nhật CustomerMapper

Thêm một phương thức mapper mới để hỗ trợ CustomerDetailsDto.

**File**: `src/main/java/com/easybank/accounts/mapper/CustomerMapper.java`

```java
package com.easybank.accounts.mapper;

import com.easybank.accounts.dto.CustomerDetailsDto;
import com.easybank.accounts.dto.CustomerDto;
import com.easybank.accounts.entity.Customer;

public class CustomerMapper {
    
    public static CustomerDto mapToCustomerDto(Customer customer, CustomerDto customerDto) {
        customerDto.setName(customer.getName());
        customerDto.setEmail(customer.getEmail());
        customerDto.setMobileNumber(customer.getMobileNumber());
        return customerDto;
    }
    
    public static Customer mapToCustomer(CustomerDto customerDto, Customer customer) {
        customer.setName(customerDto.getName());
        customer.setEmail(customerDto.getEmail());
        customer.setMobileNumber(customerDto.getMobileNumber());
        return customer;
    }
    
    // Phương thức mapper mới cho CustomerDetailsDto
    public static CustomerDetailsDto mapToCustomerDetailsDto(
            Customer customer, CustomerDetailsDto customerDetailsDto) {
        customerDetailsDto.setName(customer.getName());
        customerDetailsDto.setEmail(customer.getEmail());
        customerDetailsDto.setMobileNumber(customer.getMobileNumber());
        return customerDetailsDto;
    }
}
```

## Cách Hoạt Động Của Luồng Giao Tiếp

### Bên Trong Hệ Thống

Khi client gọi `GET /api/fetchCustomerDetails?mobileNumber=0123456789`:

1. **Yêu Cầu Đến** Accounts microservice `CustomerController`
2. **Controller** ủy quyền cho `CustomerServiceImpl`
3. **Tầng Service** thực thi:
   - Truy vấn database local cho dữ liệu customer
   - Truy vấn database local cho dữ liệu account
   - **Feign Client cho Loans**:
     - Liên hệ Eureka Server
     - Eureka trả về các instance Loans service khả dụng
     - Spring Cloud LoadBalancer chọn một instance
     - HTTP request được gửi đến Loans instance đã chọn
     - Response nhận được và parse thành `LoansDto`
   - **Feign Client cho Cards**:
     - Quy trình tương tự như Loans
     - Response nhận được và parse thành `CardsDto`
4. **Tổng Hợp Dữ Liệu**: Tất cả dữ liệu được merge vào `CustomerDetailsDto`
5. **Response Được Gửi** về cho client

### Quy Trình Khám Phá Dịch Vụ

```
Accounts Service
    ↓ (cần dữ liệu loans)
    → Feign Client
        ↓ (truy vấn)
        → Eureka Server
            ↓ (trả về)
            → Danh sách Loans service instance
        ↓ (chọn)
        → Spring Cloud LoadBalancer
            ↓ (instance được chọn)
            → Loans Service Instance #2
                ↓ (HTTP request)
                → Loans REST API
                    ↓ (response)
                    ← Dữ Liệu Loans
```

## Lợi Thế Chính

### 1. Không Hard-Code URL
```java
// ❌ Cách tiếp cận không tốt (hard-coded)
String url = "http://localhost:9090/api/fetch?mobileNumber=" + mobileNumber;

// ✅ Cách tiếp cận tốt (service discovery)
loansFeignClient.fetchLoanDetails(mobileNumber);
```

### 2. Cân Bằng Tải Tự Động
- Nhiều instance tự động được khám phá
- Cân bằng tải phía client với Spring Cloud LoadBalancer
- Không cần load balancer bên ngoài

### 3. REST Client Khai Báo
```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    @GetMapping("/api/fetch")
    ResponseEntity<LoansDto> fetchLoanDetails(@RequestParam String mobileNumber);
}
```

### 4. Phân Tách Trách Nhiệm
- Controller xử lý các vấn đề HTTP
- Service chứa logic nghiệp vụ
- Feign client trừu tượng hóa giao tiếp từ xa
- Mapper xử lý chuyển đổi dữ liệu

## Build và Chạy

### 1. Khởi Động Các Dịch Vụ Hạ Tầng

```bash
# Khởi động Config Server (port 8071)
cd configserver
mvn spring-boot:run

# Khởi động Eureka Server (port 8761)
cd eurekaserver
mvn spring-boot:run
```

### 2. Khởi Động Các Microservice

```bash
# Khởi động Accounts Microservice (port 8080)
cd accounts
mvn clean install
mvn spring-boot:run

# Khởi động Cards Microservice (port 9000)
cd cards
mvn spring-boot:run

# Khởi động Loans Microservice (port 8090)
cd loans
mvn spring-boot:run
```

### 3. Xác Minh Đăng Ký

Mở trình duyệt: `http://localhost:8761`

Bạn sẽ thấy cả ba microservice đã đăng ký:
- ACCOUNTS
- CARDS
- LOANS

## Kiểm Thử API

### Bước 1: Tạo Dữ Liệu Test

Vì chúng ta đang sử dụng H2 in-memory database, hãy tạo dữ liệu trong tất cả các microservice với cùng số điện thoại.

**Tạo Tài Khoản**:
```bash
POST http://localhost:8080/api/create
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789"
}
```

**Tạo Thẻ**:
```bash
POST http://localhost:9000/api/create
Content-Type: application/json

{
  "mobileNumber": "0123456789"
}
```

**Tạo Khoản Vay**:
```bash
POST http://localhost:8090/api/create
Content-Type: application/json

{
  "mobileNumber": "0123456789"
}
```

### Bước 2: Lấy Dữ Liệu Tổng Hợp

```bash
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber=0123456789
```

### Response Mong Đợi

```json
{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789",
  "accountsDto": {
    "accountNumber": 1234567890,
    "accountType": "Savings",
    "branchAddress": "123 Đường Chính, Hà Nội"
  },
  "loansDto": {
    "mobileNumber": "0123456789",
    "loanNumber": "LN123456789",
    "loanType": "Home Loan",
    "totalLoan": 500000000,
    "amountPaid": 50000000,
    "outstandingAmount": 450000000
  },
  "cardsDto": {
    "mobileNumber": "0123456789",
    "cardNumber": "1234567890123456",
    "cardType": "Credit Card",
    "totalLimit": 100000000,
    "amountUsed": 25000000,
    "availableAmount": 75000000
  }
}
```

## Cấu Hình

### application.yml (Accounts Microservice)

```yaml
spring:
  application:
    name: accounts
  cloud:
    openfeign:
      client:
        config:
          default:
            connectTimeout: 5000
            readTimeout: 5000

eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
  instance:
    preferIpAddress: true
```

### Kích Hoạt Feign Client

**Main Application Class**:
```java
@SpringBootApplication
@EnableFeignClients
@EnableEurekaClient
public class AccountsApplication {
    public static void main(String[] args) {
        SpringApplication.run(AccountsApplication.class, args);
    }
}
```

## Best Practices (Phương Pháp Tốt Nhất)

### 1. Xử Lý Lỗi

Triển khai xử lý exception phù hợp cho các lỗi Feign client:

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(FeignException.class)
    public ResponseEntity<ErrorResponse> handleFeignException(FeignException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.SERVICE_UNAVAILABLE.value(),
            "Dịch vụ tạm thời không khả dụng"
        );
        return new ResponseEntity<>(error, HttpStatus.SERVICE_UNAVAILABLE);
    }
}
```

### 2. Cấu Hình Timeout

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          loans:
            connectTimeout: 5000
            readTimeout: 5000
          cards:
            connectTimeout: 5000
            readTimeout: 5000
```

### 3. Circuit Breaker Pattern

Thêm Resilience4j để chịu lỗi:

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot2</artifactId>
</dependency>
```

```java
@CircuitBreaker(name = "loansService", fallbackMethod = "getDefaultLoans")
public LoansDto getLoansData(String mobileNumber) {
    return loansFeignClient.fetchLoanDetails(mobileNumber).getBody();
}

public LoansDto getDefaultLoans(String mobileNumber, Exception ex) {
    return new LoansDto(); // Trả về dữ liệu mặc định hoặc cached
}
```

### 4. Logging

Bật logging Feign client:

```yaml
logging:
  level:
    com.easybank.accounts.service.client: DEBUG
```

```java
@Configuration
public class FeignConfig {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
}
```

## Xử Lý Sự Cố

### Vấn Đề: Service Không Tìm Thấy

**Triệu chứng**: `FeignException: Service 'LOANS' not found`

**Giải pháp**:
1. Kiểm tra xem Loans microservice có đang chạy không
2. Xác minh Eureka dashboard hiển thị service
3. Kiểm tra `spring.application.name` khớp với tên Feign client
4. Đợi 30 giây để service đăng ký

### Vấn Đề: Connection Timeout

**Triệu chứng**: `SocketTimeoutException: Read timed out`

**Giải pháp**:
1. Tăng giá trị timeout trong cấu hình
2. Kiểm tra kết nối mạng
3. Xác minh service đích đang phản hồi
4. Kiểm tra các truy vấn database chậm

### Vấn Đề: Lỗi Load Balancer

**Triệu chứng**: `No instances available for LOANS`

**Giải pháp**:
1. Đảm bảo service được đăng ký với Eureka
2. Kiểm tra health endpoint của service
3. Xác minh `eureka.instance.preferIpAddress` được set đúng
4. Khởi động lại microservice

## Cân Nhắc Về Hiệu Suất

### 1. Gọi Song Song

Để hiệu suất tốt hơn, cân nhắc thực hiện các cuộc gọi Feign song song:

```java
CompletableFuture<LoansDto> loansFuture = 
    CompletableFuture.supplyAsync(() -> 
        loansFeignClient.fetchLoanDetails(mobileNumber).getBody());

CompletableFuture<CardsDto> cardsFuture = 
    CompletableFuture.supplyAsync(() -> 
        cardsFeignClient.fetchCardDetails(mobileNumber).getBody());

CompletableFuture.allOf(loansFuture, cardsFuture).join();

customerDetailsDto.setLoansDto(loansFuture.get());
customerDetailsDto.setCardsDto(cardsFuture.get());
```

### 2. Caching

Triển khai caching cho dữ liệu được truy cập thường xuyên:

```java
@Cacheable(value = "customerDetails", key = "#mobileNumber")
public CustomerDetailsDto fetchCustomerDetails(String mobileNumber) {
    // Triển khai
}
```

### 3. Connection Pooling

Cấu hình HTTP connection pool cho Feign:

```yaml
spring:
  cloud:
    openfeign:
      httpclient:
        enabled: true
        max-connections: 200
        max-connections-per-route: 50
```

## Giám Sát và Quan Sát

### 1. Distributed Tracing

Thêm Spring Cloud Sleuth và Zipkin:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-sleuth-zipkin</artifactId>
</dependency>
```

### 2. Metrics

Bật actuator endpoint:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

### 3. Health Check

Triển khai health indicator:

```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // Kiểm tra tình trạng của downstream service
        return Health.up().build();
    }
}
```

## Kết Luận

Triển khai này minh họa một cách tiếp cận sẵn sàng cho production để xây dựng API tổng hợp trong kiến trúc microservices. Những điểm chính:

✅ **Service Discovery**: Định vị service động qua Eureka  
✅ **Declarative Client**: Định nghĩa interface Feign đơn giản  
✅ **Load Balancing**: Cân bằng tải phía client tự động  
✅ **Phân Tách Trách Nhiệm**: Kiến trúc sạch với controller, service và client  
✅ **Xử Lý Lỗi**: Quản lý exception mạnh mẽ  
✅ **Khả Năng Mở Rộng**: Có thể xử lý nhiều instance service  

Pattern được trình bày ở đây tạo nền tảng để xây dựng microservice có khả năng phục hồi, có thể mở rộng và giao tiếp hiệu quả mà không bị ràng buộc chặt chẽ. Khi hệ thống của bạn phát triển, bạn có thể thêm circuit breaker, caching và các pattern khác để tăng cường độ tin cậy và hiệu suất.

## Các Bước Tiếp Theo

1. Triển khai circuit breaker pattern với Resilience4j
2. Thêm API Gateway cho điểm entry thống nhất
3. Triển khai distributed tracing
4. Thêm xử lý lỗi toàn diện
5. Triển khai chiến lược caching
6. Thêm bảo mật với OAuth2/JWT
7. Containerize với Docker
8. Deploy lên Kubernetes

Chúc bạn code vui vẻ! 🚀



================================================================================
FILE: 19-eureka-self-preservation-mode.md
================================================================================

# Chế Độ Tự Bảo Vệ Của Eureka (Self-Preservation Mode)

## Tổng Quan

Tài liệu này giải thích về chế độ tự bảo vệ trong Eureka Server, tại sao nó tồn tại, và cách nó hoạt động để duy trì tính ổn định trong mạng lưới microservice.

## Hiểu Thông Báo Cảnh Báo

Khi bạn thấy thông báo cảnh báo trên bảng điều khiển Eureka, điều này thường do một khái niệm gọi là **chế độ tự bảo vệ**. Cảnh báo này xuất hiện khi Eureka Server kích hoạt cơ chế bảo vệ này.

## Chế Độ Tự Bảo Vệ Là Gì?

Chế độ tự bảo vệ là một tính năng an toàn trong Eureka Server giúp ngăn chặn việc loại bỏ sớm các instance dịch vụ khỏi registry trong trường hợp có vấn đề về mạng hoặc lỗi tạm thời.

### Hoạt Động Bình Thường

Trong một mạng lưới microservice hoạt động bình thường:
- Eureka Server mong đợi nhận heartbeat từ các instance microservice đã đăng ký
- Nếu không nhận được heartbeat trong một khoảng thời gian nhất định, Eureka cho rằng instance đó không phản hồi, bị crash hoặc không khỏe mạnh
- Hành vi mặc định là xóa instance không phản hồi khỏi service registry
- Điều này giúp duy trì cái nhìn cập nhật về tất cả các instance dịch vụ khỏe mạnh đã đăng ký

### Vấn Đề: Lỗi Mạng

Các vấn đề về mạng có thể xảy ra trong thực tế - các website có thể tạm thời không khả dụng trong vài giây hoặc vài phút trước khi có thể truy cập trở lại. Các lỗi mạng tương tự có thể xảy ra trong mạng lưới microservice:

- Độ trễ hệ thống tạm thời hoặc lỗi mạng có thể khiến Eureka Server bỏ lỡ các heartbeat
- Điều này dẫn đến việc hết hạn sai hoặc loại bỏ nhầm các instance dịch vụ khỏe mạnh
- Việc loại bỏ không cần thiết gây ra sự không ổn định và gián đoạn trong mạng lưới microservice

**Ví Dụ Kịch Bản:**
- Lỗi mạng xảy ra trong 5 phút
- Eureka Server không nhận được bất kỳ heartbeat nào trong thời gian này
- Nếu Eureka loại bỏ tất cả các instance, registry sẽ trở nên trống rỗng
- Các dịch vụ client cố gắng khám phá microservice sẽ gặp ngoại lệ
- Service discovery và client-side load balancing thất bại

## Cách Chế Độ Tự Bảo Vệ Hoạt Động

### Kích Hoạt

Eureka Server chuyển sang chế độ tự bảo vệ khi nhận ra rằng phần lớn các instance microservice không gửi heartbeat. Thay vì ngay lập tức loại bỏ tất cả các instance dịch vụ:

1. Eureka chuyển sang chế độ tự bảo vệ
2. Ngay cả khi không nhận được tín hiệu heartbeat, nó không loại bỏ chi tiết dịch vụ khỏi registry
3. Điều này ngăn chặn việc loại bỏ tất cả các instance do độ trễ mạng tạm thời hoặc lỗi

### Trong Chế Độ Tự Bảo Vệ

- Eureka Server tiếp tục cung cấp các instance đã đăng ký cho các ứng dụng client
- Nó duy trì chế độ này ngay cả khi nghi ngờ một số instance không còn khả dụng
- Giả định rằng lỗi mạng có thể chỉ tồn tại giữa Eureka Server và các instance
- Điều này duy trì tính ổn định và khả dụng của service registry
- Client vẫn có thể khám phá và tương tác với các instance khả dụng

### Hủy Kích Hoạt

Chế độ tự bảo vệ tiếp tục cho đến khi:
- Đạt được ngưỡng cụ thể của các instance khỏe mạnh, HOẶC
- Các dịch vụ down được đưa trở lại online, HOẶC
- Lỗi mạng được giải quyết

## Ví Dụ Trực Quan

### Trạng Thái Ban Đầu (Trước Khi Có Vấn Đề Mạng)
- 5 instance của loans microservice được đăng ký
- Tất cả các instance gửi heartbeat mỗi 30 giây
- Eureka hiển thị tất cả 5 instance đều UP

### Vấn Đề Mạng Xảy Ra
- Vấn đề mạng giữa Eureka và các instance microservice
- Instance 4 và Instance 5 ngừng gửi heartbeat
- Eureka không loại bỏ chúng ngay lập tức
- Eureka cho 3 cơ hội (chờ tổng cộng 90 giây)
- Nếu không nhận được heartbeat sau 90 giây, Instance 4 và 5 bị loại bỏ
- Registry bây giờ chỉ hiển thị instance 1, 2, và 3

### Chế Độ Tự Bảo Vệ Được Kích Hoạt
- Eureka nhận ra 15% tổng số instance đã hết hạn (ngưỡng mặc định là 85%)
- Chuyển sang chế độ tự bảo vệ
- Bây giờ nếu Instance 3 cũng ngừng gửi heartbeat, nó sẽ không bị loại bỏ
- Instance 3 vẫn còn trong registry mặc dù thiếu heartbeat

## Các Thuộc Tính Cấu Hình

### 1. Khoảng Thời Gian Gia Hạn Lease
```yaml
eureka.instance.lease-renewal-interval-in-seconds: 30
```
- Mặc định: 30 giây
- Xác định tần suất Eureka Server mong đợi nhận tín hiệu heartbeat từ các client microservice

### 2. Thời Lượng Hết Hạn Lease
```yaml
eureka.instance.lease-expiration-duration-in-seconds: 90
```
- Mặc định: 90 giây
- Thời gian tối đa Eureka chờ để nhận một heartbeat
- Nếu không có heartbeat trong vòng 90 giây, instance có thể bị loại bỏ

### 3. Bộ Đếm Thời Gian Khoảng Loại Bỏ
```yaml
eureka.server.eviction-interval-timer-in-ms: 60000
```
- Mặc định: 60,000 mili giây (60 giây)
- Tần suất chạy của bộ lập lịch loại bỏ
- Bộ lập lịch kiểm tra xem chế độ tự bảo vệ có được kích hoạt không
- Nếu không kích hoạt: thực hiện quá trình loại bỏ
- Nếu kích hoạt: bỏ qua loại bỏ

### 4. Ngưỡng Phần Trăm Gia Hạn
```yaml
eureka.server.renewal-percent-threshold: 0.85
```
- Mặc định: 0.85 (85%)
- Được sử dụng để tính toán phần trăm mong đợi của heartbeat mỗi phút
- Nếu Eureka nhận được ít hơn 85% heartbeat mong đợi, nó chuyển sang chế độ tự bảo vệ

### 5. Khoảng Cập Nhật Ngưỡng Gia Hạn
```yaml
eureka.server.renewal-threshold-update-interval-ms: 900000
```
- Mặc định: 900,000 mili giây (15 phút)
- Bộ lập lịch chạy mỗi 15 phút để tính toán tổng số heartbeat mong đợi
- Giúp Eureka thích ứng với thay đổi về số lượng instance đã đăng ký
- Dựa trên tổng số heartbeat, tính toán giá trị ngưỡng để kích hoạt chế độ tự bảo vệ

### 6. Bật Tự Bảo Vệ
```yaml
eureka.server.enable-self-preservation: true
```
- Mặc định: true
- Đặt thành false để vô hiệu hóa vĩnh viễn chế độ tự bảo vệ
- **Cảnh báo:** Vô hiệu hóa tính năng này có thể dẫn đến vấn đề ổn định trong lỗi mạng

## Hiểu Cảnh Báo Trên Dashboard

Khi chế độ tự bảo vệ hoạt động, bạn sẽ thấy cảnh báo này:

> **KHẨN CẤP! EUREKA CÓ THỂ ĐANG SAI KHI TUYÊN BỐ CÁC INSTANCE ĐANG HOẠT ĐỘNG KHI CHÚNG KHÔNG. GIA HẠN ÍT HƠN NGƯỠNG VÀ DO ĐÓ CÁC INSTANCE KHÔNG BỊ HẾT HẠN CHỈ ĐỂ AN TOÀN.**

**Dịch nghĩa:**
- Chi tiết instance được hiển thị có thể không chính xác
- Heartbeat (gia hạn) ít hơn ngưỡng mong đợi
- Các instance không bị hết hạn như một biện pháp an toàn
- Đây là cơ chế bảo vệ, không phải lỗi

## Thực Hành Tốt Nhất

### Đừng Hoảng Sợ
Khi bạn thấy cảnh báo tự bảo vệ:
- Đây là cơ chế bảo vệ bình thường
- Khi vấn đề mạng được giải quyết, cảnh báo sẽ tự động biến mất
- Các instance microservice sẽ tiếp tục gửi tín hiệu heartbeat
- Eureka sẽ thoát khỏi chế độ tự bảo vệ

### Khi Nào Nên Vô Hiệu Hóa Tự Bảo Vệ
Cân nhắc vô hiệu hóa chế độ tự bảo vệ chỉ khi:
- Mạng của bạn cực kỳ ổn định
- Bạn có cơ chế thay thế để xử lý lỗi mạng
- Bạn hiểu rủi ro của việc có một service registry trống

**Rủi Ro Khi Vô Hiệu Hóa:**
- Tất cả chi tiết dịch vụ có thể bị xóa trong lỗi mạng
- Service registry trở nên trống rỗng
- Dẫn đến vấn đề ổn định trong mạng lưới microservice
- Không ai có thể cứu mạng lưới microservice của bạn khỏi các lỗi dây chuyền

## Tóm Tắt

- **Mục đích:** Eureka Server không hoảng sợ khi không nhận được heartbeat từ phần lớn các instance
- **Hành vi:** Giữ bình tĩnh và chuyển sang chế độ tự bảo vệ (như thiền định)
- **Trong Chế Độ:** Không loại bỏ các instance khỏi service registry
- **Trường Hợp Sử Dụng:** Tính năng cứu cánh khi lỗi mạng phổ biến
- **Kết Quả:** Giúp xử lý các cảnh báo dương tính giả và duy trì tính khả dụng của dịch vụ

## Kết Luận

Chế độ tự bảo vệ là một tính năng quan trọng để duy trì tính ổn định của microservice. Nó ngăn chặn các lỗi thảm khốc do vấn đề mạng tạm thời bằng cách giữ nguyên service registry. Hiểu được cơ chế này giúp các nhà phát triển và vận hành đưa ra quyết định có cơ sở về kiến trúc microservice của họ và tránh hoảng sợ không cần thiết khi thấy thông báo cảnh báo.



================================================================================
FILE: 2-connecting-microservices-to-mysql-database.md
================================================================================

# Kết Nối Spring Boot Microservices với MySQL Database Cục Bộ

## Tổng Quan

Hướng dẫn này trình bày cách kết nối các Spring Boot microservices (accounts, cards và loans) với cơ sở dữ liệu MySQL chạy cục bộ trong các Docker containers. Chúng ta sẽ thay thế cơ sở dữ liệu H2 in-memory bằng MySQL để có môi trường phát triển và kiểm thử thực tế hơn.

## Yêu Cầu Tiên Quyết

- Docker Desktop đã được cài đặt và đang chạy
- Spring Boot microservices (accounts, cards, loans)
- Config Server (cho cấu hình tập trung)
- Maven để quản lý dependencies
- Các MySQL Docker containers đang chạy cục bộ
- Postman hoặc công cụ kiểm thử API tương tự

## Bước 1: Cập Nhật Maven Dependencies

### Xóa H2 Database Dependency

Bước đầu tiên là xóa H2 database dependency khỏi `pom.xml` trong tất cả các microservices. Khi Spring Boot phát hiện H2 trong classpath, nó sẽ tự động cấu hình và khởi tạo H2, điều này chúng ta muốn tránh khi sử dụng MySQL.

**Trong pom.xml, xóa:**
```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
</dependency>
```

### Thêm MySQL Connector Dependency

Thay thế H2 dependency bằng MySQL connector:

```xml
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>
```

**Áp dụng thay đổi này cho cả ba microservices:**
1. Accounts microservice
2. Cards microservice
3. Loans microservice

Sau khi thực hiện các thay đổi này, tải lại Maven dependencies để tải xuống MySQL connector.

> **Lưu ý:** Config Server không sử dụng bất kỳ database nào, do đó không cần thay đổi gì ở đây.

## Bước 2: Cấu Hình Kết Nối Database trong application.yml

### Cấu Hình Accounts Microservice

Mở file `application.yml` trong accounts microservice và thay thế cấu hình datasource H2 bằng MySQL:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/accountsDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Chi Tiết Cấu Hình:**

- **Định Dạng URL**: `jdbc:mysql://<hostname>:<port>/<tên-database>`
- **Hostname**: `localhost` (vì MySQL đang chạy cục bộ)
- **Port**: `3306` (port của accounts database)
- **Tên Database**: `accountsDB`
- **Username/Password**: `root/root` (chỉ dùng cho phát triển cục bộ)
- **sql.init.mode**: `always` - yêu cầu Spring Boot thực thi `schema.sql` mỗi khi khởi động
- **show-sql**: `true` - hiển thị các câu lệnh SQL được thực thi trong console

### Cấu Hình Cards Microservice

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3308/cardsDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Điểm Khác Biệt:**
- **Port**: `3308` (port của cards database)
- **Tên Database**: `cardsDB`

### Cấu Hình Loans Microservice

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3307/loansDB
    username: root
    password: root
    sql:
      init:
        mode: always
  jpa:
    show-sql: true
```

**Điểm Khác Biệt:**
- **Port**: `3307` (port của loans database)
- **Tên Database**: `loansDB`

### Xóa Các Properties Không Cần Thiết Dành Cho H2

Xóa các properties sau đây khỏi tất cả microservices:
- `spring.datasource.driver-class-name`
- `spring.h2.console.enabled`
- `spring.h2.console.path`
- `spring.jpa.database-platform`
- `spring.jpa.hibernate.ddl-auto: update`

Giữ lại `spring.jpa.show-sql: true` để xem các câu lệnh SQL trong console logs.

## Bước 3: Cấu Hình Khởi Tạo Schema Tự Động

### Hiểu Về Hành Vi Khởi Tạo Schema

**H2 Database:**
- Tự động tìm và thực thi `schema.sql` trong quá trình khởi động Spring Boot
- Không cần cấu hình bổ sung

**MySQL Database:**
- KHÔNG tự động thực thi `schema.sql`
- Mong đợi developers đã tạo sẵn database schemas
- Yêu cầu cấu hình rõ ràng để thực thi schema scripts

### Kích Hoạt Thực Thi Schema Script

Thêm property sau để kích hoạt thực thi schema tự động:

```yaml
spring:
  datasource:
    sql:
      init:
        mode: always
```

**Quan trọng:** Property này phải nằm dưới `spring.datasource`, KHÔNG phải dưới `spring.jpa`.

**Vị trí sai:**
```yaml
spring:
  jpa:
    sql:
      init:
        mode: always  # ❌ Sai - không hoạt động ở đây
```

**Vị trí đúng:**
```yaml
spring:
  datasource:
    sql:
      init:
        mode: always  # ✅ Đúng
```

### Sử Dụng IF NOT EXISTS trong SQL Scripts

Đảm bảo các file `schema.sql` của bạn sử dụng `IF NOT EXISTS` để tránh lỗi khi khởi động lại:

```sql
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_number BIGINT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(100) NOT NULL,
    branch_address VARCHAR(200) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
```

**Không có `IF NOT EXISTS`:** Ứng dụng sẽ báo lỗi khi khởi động lại vì các bảng đã tồn tại.

## Bước 4: Thông Tin Đăng Nhập Database - Vấn Đề Bảo Mật

### Môi Trường Development

Đối với phát triển và kiểm thử cục bộ, việc hardcode credentials trong `application.yml` là chấp nhận được:

```yaml
spring:
  datasource:
    username: root
    password: root
```

### Môi Trường Production

**Không bao giờ hardcode credentials của production database** trong các file cấu hình ứng dụng. Thay vào đó, sử dụng các phương pháp cấu hình externalized:

1. **Biến Môi Trường (Environment Variables)**
   ```yaml
   spring:
     datasource:
       username: ${DB_USERNAME}
       password: ${DB_PASSWORD}
   ```

2. **Tham Số Dòng Lệnh (Command-Line Arguments)**
   ```bash
   java -jar app.jar --spring.datasource.username=user --spring.datasource.password=pass
   ```

3. **Biến Hệ Thống JVM (JVM System Variables)**
   ```bash
   java -Dspring.datasource.username=user -Dspring.datasource.password=pass -jar app.jar
   ```

4. **Docker Compose Environment Variables**
   ```yaml
   services:
     accounts:
       environment:
         - SPRING_DATASOURCE_USERNAME=user
         - SPRING_DATASOURCE_PASSWORD=pass
   ```

5. **Kubernetes ConfigMaps và Secrets**
   - Sử dụng ConfigMaps cho cấu hình không nhạy cảm
   - Sử dụng Secrets cho credentials nhạy cảm
   - Mount chúng dưới dạng biến môi trường hoặc volume files

## Bước 5: Khởi Động Docker MySQL Containers

Đảm bảo tất cả MySQL Docker containers đang chạy trước khi khởi động các microservices.

**Accounts Database Container:**
```bash
docker run -d -p 3306:3306 --name accountsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=accountsDB mysql:latest
```

**Cards Database Container:**
```bash
docker run -d -p 3308:3306 --name cardsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsDB mysql:latest
```

**Loans Database Container:**
```bash
docker run -d -p 3307:3306 --name loansDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=loansDB mysql:latest
```

## Bước 6: Khởi Động Các Microservices

### Trình Tự Khởi Động

Khởi động các microservices theo thứ tự sau:

1. **Config Server Trước**
   - Các microservices khác phụ thuộc vào Config Server
   - Đợi cho đến khi nó khởi động thành công

2. **Accounts Application**
   - Khởi động ở chế độ debug để dễ khắc phục sự cố

3. **Cards Application**
   - Khởi động ở chế độ debug

4. **Loans Application**
   - Khởi động ở chế độ debug

### Xác Minh Khởi Động Thành Công

Kiểm tra console logs của mỗi microservice để đảm bảo:
- Không có lỗi kết nối
- Schema scripts được thực thi thành công
- Các bảng được tạo trong database

## Bước 7: Xác Minh Tạo Bảng Database

Sử dụng MySQL client (như MySQL Workbench, DBeaver, hoặc SQL Electron) để xác minh việc tạo bảng.

### Accounts Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3306
- Database: accountsDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `customer`
- Bảng `accounts`

### Cards Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3308
- Database: cardsDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `cards`

### Loans Database

**Chi Tiết Kết Nối:**
- Host: localhost
- Port: 3307
- Database: loansDB
- Username: root
- Password: root

**Các Bảng Mong Đợi:**
- Bảng `loans`

## Bước 8: Kiểm Thử API Endpoints

Sử dụng Postman để kiểm thử các thao tác CRUD và xác minh tính bền vững của dữ liệu.

### Tạo Account

**Request:**
- Method: POST
- URL: `http://localhost:8080/api/create`
- Body:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong accounts database

### Tạo Card

**Request:**
- Method: POST
- URL: `http://localhost:9000/api/create`
- Body:
  ```json
  {
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong cards database

### Tạo Loan

**Request:**
- Method: POST
- URL: `http://localhost:8090/api/create`
- Body:
  ```json
  {
    "mobileNumber": "1234567890"
  }
  ```

**Response:**
- Status: 201 Created
- Xác minh dữ liệu được lưu trong loans database

### Lấy Dữ Liệu (Fetch Data)

Kiểm thử các GET endpoints để truy xuất dữ liệu:

**Fetch Account:**
- Method: GET
- URL: `http://localhost:8080/api/fetch?mobileNumber=1234567890`

**Fetch Card:**
- Method: GET
- URL: `http://localhost:9000/api/fetch?mobileNumber=1234567890`

**Fetch Loan:**
- Method: GET
- URL: `http://localhost:8090/api/fetch?mobileNumber=1234567890`

Tất cả các request nên trả về dữ liệu đã tạo trước đó.

## Tính Bền Vững Dữ Liệu Docker Container

### Cảnh Báo Quan Trọng: Mất Dữ Liệu Khi Xóa Container

Docker containers lưu trữ dữ liệu nội bộ trong hệ thống file của chúng. **Khi bạn xóa một container, tất cả dữ liệu được lưu bên trong sẽ bị mất vĩnh viễn.**

### Các Thao Tác Vòng Đời Container

**Dừng Container:**
```bash
docker stop accountsDB
```
- Container ngừng chạy
- **Dữ liệu được bảo toàn**
- Có thể khởi động lại sau với `docker start accountsDB`

**Xóa Container:**
```bash
docker rm accountsDB
```
- Container bị xóa vĩnh viễn
- **Tất cả dữ liệu bị mất mãi mãi**
- Phải tạo container mới từ đầu

### Minh Họa: Kịch Bản Mất Dữ Liệu

Hãy minh họa điều gì xảy ra khi bạn xóa một container:

1. **Trạng Thái Ban Đầu:**
   - Cả ba database containers đang chạy
   - Dữ liệu được lưu trong tất cả databases
   - Tất cả microservices đang chạy và được kết nối

2. **Dừng Tất Cả Microservices:**
   - Dừng accounts application
   - Dừng cards application
   - Dừng loans application

3. **Dừng Tất Cả Database Containers:**
   - Dừng accounts database container
   - Dừng loans database container
   - Dừng cards database container

4. **Xóa Cards Database Container:**
   ```bash
   docker rm cardsDB
   ```
   - Cards database và tất cả dữ liệu của nó đã biến mất

5. **Khởi Động Lại Accounts và Loans Containers:**
   ```bash
   docker start accountsDB
   docker start loansDB
   ```
   - Các containers này vẫn còn dữ liệu của chúng

6. **Tạo Lại Cards Database Container:**
   ```bash
   docker run -d -p 3308:3306 --name cardsDB -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=cardsDB mysql:latest
   ```
   - Container mới được tạo
   - Database trống không có bảng hoặc dữ liệu

7. **Khởi Động Lại Tất Cả Microservices:**
   - Khởi động config server
   - Khởi động accounts application (sẽ tạo bảng qua schema.sql)
   - Khởi động cards application (sẽ tạo bảng qua schema.sql - trống rỗng)
   - Khởi động loans application (sẽ tạo bảng qua schema.sql)

8. **Kiểm Thử API Endpoints:**
   - **Fetch Account:** ✅ Hoạt động - trả về dữ liệu đã lưu
   - **Fetch Card:** ❌ Không trả về dữ liệu - database đã bị xóa
   - **Fetch Loan:** ✅ Hoạt động - trả về dữ liệu đã lưu

### Best Practices cho Quản Lý Container

**NÊN:**
- ✅ Sử dụng `docker stop` để dừng containers khi không sử dụng
- ✅ Sử dụng `docker start` để khởi động lại containers đã dừng
- ✅ Triển khai backup database thường xuyên
- ✅ Sử dụng Docker volumes để lưu trữ dữ liệu bền vững
- ✅ Ghi chép các containers nào chứa dữ liệu quan trọng

**KHÔNG NÊN:**
- ❌ Xóa containers có dữ liệu quan trọng
- ❌ Sử dụng `docker rm` mà không backup dữ liệu trước
- ❌ Chỉ dựa vào lưu trữ container cho dữ liệu quan trọng
- ❌ Quên containers nào đang dừng so với đã xóa

### Sử Dụng Docker Volumes để Bền Vững

Để ngăn chặn mất dữ liệu, sử dụng Docker volumes:

```bash
docker run -d -p 3306:3306 \
  --name accountsDB \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=accountsDB \
  -v accounts-data:/var/lib/mysql \
  mysql:latest
```

**Lợi Ích:**
- Dữ liệu được lưu trong named volume `accounts-data`
- Tồn tại sau khi xóa container
- Có thể tái sử dụng với containers mới
- Có thể backup riêng biệt

## Xử Lý Sự Cố

### Vấn Đề: Không Tạo Được Bảng

**Triệu Chứng:**
- Ứng dụng khởi động thành công
- Không có lỗi trong logs
- Database tồn tại nhưng không có bảng

**Nguyên Nhân:**
Property `spring.datasource.sql.init.mode: always` được đặt sai vị trí

**Giải Pháp:**
Xác minh property nằm dưới `spring.datasource`:

```yaml
spring:
  datasource:
    sql:
      init:
        mode: always  # Phải ở đây
```

### Vấn Đề: Connection Refused

**Triệu Chứng:**
- Ứng dụng không khởi động được
- Lỗi: "Connection refused" hoặc "Unable to connect to database"

**Nguyên Nhân và Giải Pháp Có Thể:**

1. **Docker container không chạy**
   - Kiểm tra: `docker ps`
   - Giải pháp: Khởi động container với `docker start <tên-container>`

2. **Số port sai**
   - Kiểm tra application.yml khớp với port mapping của container
   - Accounts: 3306, Cards: 3308, Loans: 3307

3. **Tên database sai**
   - Kiểm tra tên database trong application.yml khớp với database của container
   - Nên là: accountsDB, cardsDB, loansDB

4. **Credentials sai**
   - Kiểm tra username và password khớp với cấu hình container
   - Mặc định: root/root

### Vấn Đề: Lỗi Table Already Exists

**Triệu Chứng:**
- Lỗi khi khởi động: "Table 'accounts' already exists"

**Nguyên Nhân:**
Thiếu `IF NOT EXISTS` trong SQL scripts

**Giải Pháp:**
Cập nhật `schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS accounts (
    -- định nghĩa các cột
);
```

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

✅ Thay thế H2 in-memory database bằng MySQL  
✅ Cấu hình ba microservices kết nối với các MySQL databases riêng biệt  
✅ Kích hoạt thực thi schema tự động khi khởi động  
✅ Kiểm thử tính bền vững dữ liệu trên tất cả microservices  
✅ Hiểu vòng đời dữ liệu container và rủi ro  

### Điểm Chính Cần Nhớ

1. **Quản Lý Dependency**: Thay H2 bằng MySQL connector trong pom.xml
2. **Cấu Hình**: Đặt đúng database URL, port và credentials trong application.yml
3. **Khởi Tạo Schema**: Sử dụng `spring.datasource.sql.init.mode: always` cho MySQL
4. **SQL Scripts**: Luôn sử dụng `IF NOT EXISTS` để tránh lỗi
5. **Bảo Mật**: Không bao giờ hardcode credentials production
6. **Tính Bền Vững Dữ Liệu**: Docker containers mất dữ liệu khi bị xóa
7. **Quản Lý Container**: Dừng containers, đừng xóa chúng
8. **Best Practice**: Sử dụng Docker volumes cho dữ liệu quan trọng

### Ưu Điểm của Cấu Hình Này

✅ **Thiết Lập Nhanh**: Tạo databases nhanh chóng với Docker  
✅ **Môi Trường Cô Lập**: Mỗi microservice có database riêng  
✅ **Dễ Kiểm Thử**: Có thể tạo lại toàn bộ môi trường nhanh chóng  
✅ **Không Cần Cài Đặt**: Không cần cài MySQL trên máy host  
✅ **Di Động**: Cùng một cấu hình hoạt động trên các máy phát triển khác nhau  

### Nhược Điểm và Hạn Chế

❌ **Rủi Ro Mất Dữ Liệu**: Xóa containers làm mất tất cả dữ liệu vĩnh viễn  
❌ **Không Bền Vững Volume**: Lưu trữ container là tạm thời theo mặc định  
❌ **Quản Lý Thủ Công**: Cần nhớ dừng, không xóa containers  
❌ **Chưa Sẵn Sàng Production**: Yêu cầu cấu hình volume phù hợp cho production  
❌ **Phức Tạp Backup**: Cần các chiến lược bổ sung cho backup dữ liệu  

## Bước Tiếp Theo

1. **Triển Khai Docker Volumes**: Cấu hình lưu trữ bền vững cho databases
2. **Docker Compose**: Quản lý tất cả containers với một file compose duy nhất
3. **Biến Môi Trường**: Externalize tất cả cấu hình
4. **Di Chuyển Kubernetes**: Học container orchestration cho production
5. **Giám Sát**: Thêm giám sát database và health checks
6. **Chiến Lược Backup**: Triển khai backup database tự động

---

**Chúc Mừng!** Bạn đã tích hợp thành công các Spring Boot microservices của mình với MySQL databases cục bộ chạy trong Docker containers. Cấu hình này cung cấp môi trường phát triển thực tế hơn so với H2 in-memory databases.



================================================================================
FILE: 20-generating-docker-images-for-microservices.md
================================================================================

# Tạo Docker Images cho Microservices với Google Jib

## Tổng Quan

Hướng dẫn này trình bày quy trình tạo Docker images cho các microservices Spring Boot sử dụng Google Jib Maven plugin, bao gồm Config Server và Eureka Server, và đẩy chúng lên Docker Hub.

## Yêu Cầu Trước Khi Bắt Đầu

- Docker server đang chạy trên hệ thống local
- Đã cài đặt Maven
- Các dự án microservices (Config Server, Eureka Server, Accounts, Loans, Cards)
- Tài khoản Docker Hub để đẩy images

## Các Bước Thực Hiện

### 1. Thêm Jib Plugin vào Eureka Server

Dự án Eureka Server cần cấu hình Google Jib plugin trong file `pom.xml`.

**Các bước:**
1. Mở file `pom.xml` của bất kỳ microservice nào (ví dụ: Config Server)
2. Sao chép cấu hình Google Jib plugin
3. Thêm vào file `pom.xml` của Eureka Server
4. Cập nhật tag name từ `S6` sang `S8` (Section 8)

> **Lưu ý:** Mặc định, dự án Eureka Server chỉ có cấu hình Spring Boot Maven plugin.

### 2. Cập Nhật Thông Tin Tag Cho Tất Cả Microservices

Cập nhật Docker image tag từ `S6` sang `S8` trong tất cả microservices:

- **Config Server** - Cập nhật tag sang S8
- **Accounts Microservice** - Cập nhật tag từ S6 sang S8
- **Cards Microservice** - Cập nhật tag sang S8
- **Loans Microservice** - Cập nhật tag sang S8

> **Tại sao là S6 chứ không phải S7?** Code được sao chép từ Section 6, không phải Section 7, nên tag ban đầu là S6.

### 3. Build Tất Cả Microservices

1. Thực hiện clean build hoàn toàn cho tất cả microservices
2. Dừng tất cả các instances đang chạy trong IntelliJ IDEA
3. Load tất cả các thay đổi Maven trước khi tiếp tục

### 4. Tạo Docker Images Sử Dụng Jib

Di chuyển đến thư mục của từng microservice trong terminal và thực thi lệnh Maven sau:

```bash
mvn compile jib:dockerBuild
```

#### Thứ Tự Build (Section 8):

1. **Config Server**
   ```bash
   cd config-server
   mvn compile jib:dockerBuild
   ```
   - Lưu ý: Về mặt kỹ thuật không bắt buộc vì không có thay đổi, nhưng vẫn tạo để đồng nhất

2. **Eureka Server**
   ```bash
   cd eureka-server
   mvn compile jib:dockerBuild
   ```

3. **Accounts Microservice**
   ```bash
   cd accounts
   mvn compile jib:dockerBuild
   ```

4. **Loans Microservice**
   ```bash
   cd loans
   mvn compile jib:dockerBuild
   ```

5. **Cards Microservice**
   ```bash
   cd cards
   mvn compile jib:dockerBuild
   ```

> **Lưu ý:** Thứ tự tạo Docker images không quan trọng. Bạn có thể tạo theo bất kỳ trình tự nào.

### 5. Quản Lý Docker Images

#### Dọn Dẹp Images Cũ

1. Mở Docker Dashboard
2. Tìm kiếm các images có tag `S7`
3. Xóa các images không sử dụng để tiết kiệm dung lượng đĩa local
4. Click "Delete Forever" để xóa vĩnh viễn

#### Kiểm Tra Images Mới

Tìm kiếm `S8` trong Docker Dashboard để xem tất cả năm Docker images mới được tạo:
- Config Server (S8)
- Eureka Server (S8)
- Accounts (S8)
- Loans (S8)
- Cards (S8)

### 6. Đẩy Images Lên Docker Hub

Sử dụng cấu trúc lệnh sau để đẩy images lên Docker Hub:

```bash
docker image push docker.io/<docker-username-của-bạn>/<tên-image>:<tag>
```

**Ví dụ:**
```bash
docker image push docker.io/easybytes/configserver:S8
```

Lặp lại quy trình này cho tất cả năm Docker images:
- configserver:S8
- eurekaserver:S8
- accounts:S8
- loans:S8
- cards:S8

### 7. Xác Minh Docker Hub Repository

Sau khi đẩy lên, xác minh trong Docker Hub rằng:
1. Tất cả images đã được upload thành công
2. Mỗi repository chứa nhiều phiên bản (S4, S6, S7, S8, v.v.)
3. Image `eurekaserver` mới đã có mặt

## Tóm Tắt

Bạn đã hoàn thành thành công:
- ✅ Cấu hình Google Jib plugin cho tất cả microservices
- ✅ Cập nhật Docker image tags sang S8
- ✅ Tạo Docker images cho tất cả năm services
- ✅ Dọn dẹp các images S7 cũ
- ✅ Đẩy tất cả images lên Docker Hub

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
- Cập nhật file Docker Compose
- Khởi động tất cả services với một lệnh Docker Compose duy nhất
- Xác thực service discovery và registration trong môi trường Docker

## Tham Khảo Các Lệnh Chính

| Nhiệm Vụ | Lệnh |
|----------|------|
| Tạo Docker Image | `mvn compile jib:dockerBuild` |
| Đẩy lên Docker Hub | `docker image push docker.io/<username>/<image>:<tag>` |
| Liệt kê Docker Images | `docker images` |

---

**Chủ Đề Liên Quan:**
- Google Jib Maven Plugin
- Spring Boot Microservices
- Quản Lý Docker Image
- Service Discovery với Eureka
- Docker Hub Registry



================================================================================
FILE: 21-updating-docker-compose-for-eureka-integration.md
================================================================================

# Cập Nhật Docker Compose Để Tích Hợp Eureka

## Tổng Quan

Hướng dẫn này sẽ hướng dẫn bạn quy trình cập nhật các tệp cấu hình Docker Compose để tích hợp Eureka Service Discovery vào môi trường microservices. Chúng ta sẽ cấu hình Eureka Server và cập nhật tất cả các microservices để đăng ký với nó.

## Yêu Cầu Trước

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices hiện có với Config Server
- Hiểu biết cơ bản về Spring Boot và Eureka

## Bước 1: Xóa RabbitMQ Service

Đầu tiên, mở tệp Docker Compose trong thư mục profile mặc định và xóa RabbitMQ service vì nó không còn cần thiết nữa.

1. Xóa định nghĩa RabbitMQ service
2. Xóa cấu hình `depends_on` cho RabbitMQ dưới Config Server
3. Cập nhật phiên bản image từ S6 lên S8

## Bước 2: Thêm Eureka Server Service

Tạo một định nghĩa service mới cho Eureka Server:

```yaml
eurekaserver:
  image: eazybytes/eurekaserver:s8
  container_name: eurekaserver-ms
  ports:
    - "8070:8070"
  healthcheck:
    test: "curl --fail --silent localhost:8070/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-configserver-config
  depends_on:
    configserver:
      condition: service_healthy
  environment:
    SPRING_APPLICATION_NAME: "eurekaserver"
```

### Chi Tiết Cấu Hình Chính

- **Ánh Xạ Cổng**: Eureka Server chạy trên cổng 8070
- **Kiểm Tra Sức Khỏe**: Sử dụng actuator health endpoint để kiểm tra readiness
- **Phụ Thuộc**: Phụ thuộc vào Config Server phải healthy
- **Tên Ứng Dụng**: Đặt là "eurekaserver" để tải cấu hình từ Config Server

## Bước 3: Cập Nhật Cấu Hình Chung

Trong tệp `common-config.yml`, thêm các cấu hình liên quan đến Eureka sẽ được chia sẻ giữa tất cả các microservices:

### Thêm Phụ Thuộc Eureka Server

```yaml
microservice-configserver-config:
  depends_on:
    configserver:
      condition: service_healthy
    eurekaserver:
      condition: service_healthy
```

### Thêm Biến Môi Trường Eureka Client

```yaml
environment:
  EUREKA_CLIENT_SERVICEURL_DEFAULTZONE: http://eurekaserver:8070/eureka/
```

**Quan Trọng**: Sử dụng tên service (`eurekaserver`) thay vì `localhost` cho Docker networking.

### Xóa Cấu Hình RabbitMQ

Xóa bất kỳ biến môi trường nào liên quan đến RabbitMQ khỏi cấu hình chung.

## Bước 4: Cập Nhật Images Của Microservices

Cập nhật phiên bản Docker image cho tất cả các microservices:

- **Accounts Microservice**: Cập nhật từ S6 lên S8
- **Loans Microservice**: Cập nhật từ S6 lên S8
- **Cards Microservice**: Cập nhật từ S6 lên S8

## Bước 5: Sao Chép Cấu Hình Qua Các Môi Trường

Sao chép các tệp `docker-compose.yml` và `common-config.yml` đã cập nhật sang các profile môi trường khác:

### Cho Profile Production

1. Sao chép cả hai tệp vào thư mục `prod`
2. Cập nhật `SPRING_PROFILES_ACTIVE` từ `default` sang `prod` trong `common-config.yml`

### Cho Profile QA

1. Sao chép cả hai tệp vào thư mục `qa`
2. Cập nhật `SPRING_PROFILES_ACTIVE` từ `default` sang `qa` trong `common-config.yml`

## Lợi Ích Của Cấu Hình Dựa Trên Profile

Duy trì các tệp Docker Compose riêng biệt cho các môi trường khác nhau mang lại:

- **Linh Hoạt**: Dễ dàng tùy chỉnh cấu hình cho từng môi trường
- **Cách Ly**: Các thay đổi cụ thể cho môi trường không ảnh hưởng đến môi trường khác
- **Khả Năng Bảo Trì**: Tách biệt rõ ràng các mối quan tâm

## Luồng Phụ Thuộc Service

```
Accounts/Loans/Cards Microservices
         ↓
    Eureka Server
         ↓
    Config Server
```

Tất cả các microservices phụ thuộc vào cả Config Server và Eureka Server phải healthy trước khi khởi động.

## Cấu Hình Kiểm Tra Sức Khỏe

Cấu hình kiểm tra sức khỏe của Eureka Server đảm bảo:

- Các services chờ Eureka hoạt động hoàn toàn
- Health readiness endpoint được giám sát
- Tự động thử lại với khoảng thời gian có thể cấu hình
- Trình tự khởi động đúng của tất cả các services

## Các Bước Tiếp Theo

Sau khi cập nhật cấu hình Docker Compose:

1. Khởi động tất cả containers bằng Docker Compose
2. Xác minh Eureka Server dashboard tại `http://localhost:8070`
3. Xác nhận tất cả microservices đã đăng ký với Eureka
4. Kiểm tra service discovery và giao tiếp giữa các microservices

## Tóm Tắt

Bản cập nhật cấu hình này:

- ✅ Xóa RabbitMQ service đã lỗi thời
- ✅ Thêm Eureka Server với các kiểm tra sức khỏe phù hợp
- ✅ Cấu hình tất cả microservices làm Eureka clients
- ✅ Đảm bảo trình tự khởi động service đúng đắn
- ✅ Duy trì cấu hình cụ thể cho từng môi trường

Môi trường Docker hiện đã sẵn sàng để kiểm tra các pattern service discovery và registration dựa trên Eureka.



================================================================================
FILE: 22-deploying-microservices-with-docker-compose-and-eureka.md
================================================================================

# Triển khai Microservices với Docker Compose và Eureka Server

## Tổng quan

Hướng dẫn này trình bày cách triển khai và cấu hình microservices với Eureka Server sử dụng Docker Compose, bao gồm xử lý các vấn đề cấu hình thường gặp và xác thực toàn bộ thiết lập.

## Yêu cầu

- Docker và Docker Compose đã được cài đặt
- Các microservices đã được build và container hóa
- Config Server đã được cấu hình
- Eureka Server đã được thiết lập

## Thiết lập ban đầu

### 1. Di chuyển đến thư mục Docker Compose

Di chuyển đến thư mục Docker Compose trong Section8:

```bash
cd Section8/docker-compose/default
```

### 2. Đảm bảo môi trường Docker sạch

Trước khi chạy Docker Compose, đảm bảo không có container nào đang chạy hoặc dừng để cung cấp đủ bộ nhớ:

```bash
docker ps -a
```

Nếu có containers tồn tại, hãy dọn dẹp chúng trước khi tiếp tục.

### 3. Khởi động các dịch vụ với Docker Compose

Thực thi lệnh Docker Compose:

```bash
docker compose up -d
```

## Trình tự khởi động dịch vụ

Các dịch vụ tuân theo thứ tự khởi động cụ thể:

1. **Config Server** khởi động trước
2. **Eureka Server** khởi động sau khi Config Server hoạt động tốt
3. **Microservices** (Accounts, Loans, Cards) khởi động sau khi Eureka Server đã sẵn sàng

## Xử lý sự cố kết nối

### Vấn đề 1: Eureka Server không kết nối được với Config Server

**Vấn đề**: Eureka Server không thể kết nối với Config Server.

**Nguyên nhân**: Service `microservice-base-config` chỉ cung cấp cấu hình mạng và triển khai, thiếu các thuộc tính kết nối Config Server cần thiết.

**Giải pháp**: Tạo một service cấu hình riêng cho Eureka.

### Tạo cấu hình riêng cho Eureka

Thêm service configuration mới trong `docker-compose.yml`:

```yaml
microservice-eureka-config:
  extends: microservice-configserver-config
  depends_on:
    eureka-server:
      condition: service_started
```

### Cập nhật cấu hình Eureka Server

Sửa đổi service Eureka Server để extend cấu hình mới:

```yaml
eureka-server:
  extends: microservice-configserver-config
  environment:
    SPRING_APPLICATION_NAME: "eurekaserver"
    # Các biến môi trường bổ sung
```

**Quan trọng**: Xóa dependency Config Server khỏi service Eureka Server vì nó đã có trong cấu hình chung.

### Cập nhật cấu hình Microservices

Cập nhật từng microservice (Accounts, Loans, Cards) để sử dụng cấu hình Eureka:

```yaml
accounts:
  extends: microservice-eureka-config
  # Cấu hình riêng của service

loans:
  extends: microservice-eureka-config
  # Cấu hình riêng của service

cards:
  extends: microservice-eureka-config
  # Cấu hình riêng của service
```

## Các lỗi cấu hình thường gặp

### Vấn đề 2: Lỗi thụt lề biến môi trường

**Vấn đề**: Eureka Server vẫn không kết nối được với Config Server.

**Nguyên nhân**: Các biến môi trường không được thụt lề đúng cách như các phần tử con dưới thuộc tính `environment`.

**Định dạng sai**:
```yaml
environment:
SPRING_PROFILES_ACTIVE: "default"
SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
```

**Định dạng đúng**:
```yaml
environment:
  SPRING_PROFILES_ACTIVE: "default"
  SPRING_CONFIG_IMPORT: "configserver:http://configserver:8071/"
```

**Giải pháp**: Đảm bảo tất cả các biến môi trường được thụt lề đúng cách như các phần tử con dưới thuộc tính `environment`.

## Các bước xác thực

### 1. Kiểm tra khởi động Container

Kiểm tra Docker Dashboard hoặc chạy:

```bash
docker ps
```

Xác minh rằng tất cả các containers đang chạy thành công:
- Config Server
- Eureka Server
- Accounts Microservice
- Loans Microservice
- Cards Microservice

### 2. Truy cập Eureka Dashboard

Mở trình duyệt và truy cập:

```
http://localhost:8070
```

Xác minh rằng tất cả các microservices đã đăng ký với Eureka Server.

### 3. Kiểm tra API Microservice

Sử dụng Postman hoặc bất kỳ API client nào để kiểm tra theo trình tự sau:

#### Tạo tài khoản
```http
POST http://localhost:8080/api/create
```

#### Tạo thẻ
```http
POST http://localhost:8080/api/cards/create
```
Sử dụng cùng số điện thoại với tài khoản.

#### Tạo khoản vay
```http
POST http://localhost:8080/api/loans/create
```
Sử dụng cùng số điện thoại với tài khoản.

#### Lấy thông tin chi tiết khách hàng
```http
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber={mobileNumber}
```

API này minh họa Feign Client tận dụng Eureka Server để gọi các microservices khác (Loans và Cards).

**Kết quả mong đợi**: Phản hồi thành công chứa:
- Thông tin chi tiết khách hàng
- Thông tin chi tiết tài khoản
- Thông tin chi tiết khoản vay
- Thông tin chi tiết thẻ

## Cấu hình đa môi trường

### Áp dụng thay đổi cho các Profile khác

Sau khi xác thực cấu hình trong profile default, sao chép các thay đổi sang các môi trường khác:

#### Môi trường QA

1. Sao chép `docker-compose.yml` vào `qa/docker-compose.yml`
2. Sao chép `common-config.yml` vào profile QA
3. Cập nhật tên profile từ "default" thành "qa"

#### Môi trường Production

1. Sao chép `docker-compose.yml` vào `prod/docker-compose.yml`
2. Sao chép `common-config.yml` vào profile Production
3. Cập nhật tên profile từ "default" thành "prod"

## Dọn dẹp

Để dừng và xóa tất cả containers:

```bash
docker compose down
```

Lệnh này xóa tất cả các containers đang chạy và đã dừng được tạo bởi Docker Compose.

## Thực hành tốt nhất

1. **Môi trường sạch**: Luôn đảm bảo không có containers xung đột đang chạy trước khi khởi động Docker Compose
2. **Thứ tự khởi động**: Tuân thủ các phụ thuộc dịch vụ - Config Server → Eureka Server → Microservices
3. **Tái sử dụng cấu hình**: Sử dụng service extension để tránh trùng lặp cấu hình
4. **Định dạng YAML**: Chú ý cẩn thận đến việc thụt lề trong các file YAML
5. **Health Checks**: Triển khai các health check dependencies phù hợp giữa các dịch vụ
6. **Kiểm tra**: Kiểm tra toàn bộ luồng sau khi triển khai để đảm bảo tất cả các tích hợp hoạt động

## Tóm tắt

Hướng dẫn này đã đề cập:
- Triển khai microservices với Docker Compose
- Cấu hình tích hợp Eureka Server
- Xử lý các vấn đề cấu hình thường gặp
- Xác thực đăng ký dịch vụ và giao tiếp
- Thiết lập cấu hình đa môi trường

Với cấu hình phù hợp, tất cả các microservices đăng ký thành công với Eureka Server và giao tiếp liền mạch thông qua service discovery và tích hợp Feign Client.



================================================================================
FILE: 23-client-side-load-balancing-with-multiple-instances.md
================================================================================

# Cân Bằng Tải Phía Client với Nhiều Instance Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra cân bằng tải phía client bằng cách chạy nhiều instance của một microservice với Spring Boot, Eureka Service Discovery và Docker Compose.

## Yêu Cầu Trước

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices Spring Boot với Eureka Server
- Hiểu biết cơ bản về service discovery và cân bằng tải

## Tạo Nhiều Instance với Docker Compose

### Bước 1: Nhân Bản Cấu Hình Service

Để tạo nhiều instance của loans microservice, bạn cần nhân bản cấu hình service trong file `docker-compose.yml`.

**Các điểm quan trọng:**
- Tên service phải là duy nhất (ví dụ: `loans`, `loans1`)
- Tên container phải là duy nhất (ví dụ: `loans-ms`, `loans-ms1`)
- Các port mapping phải khác nhau để tránh xung đột

### Bước 2: Cập Nhật Cấu Hình Docker Compose

```yaml
services:
  loans:
    container_name: loans-ms
    ports:
      - "8090:8090"
    # ... các cấu hình khác

  loans1:
    container_name: loans-ms1
    ports:
      - "8091:8090"  # Port host khác
    # ... các cấu hình khác
```

### Bước 3: Khởi Động Các Services

Chạy lệnh sau để khởi động tất cả services:

```bash
docker-compose up -d
```

**Hành vi mong đợi:**
- Thời gian khởi động: 3-4 phút cho nhiều containers
- Sử dụng CPU cao là bình thường (có thể đạt 200-500% với nhiều cores)
- Tất cả instances sẽ đăng ký với Eureka Server độc lập

## Xác Minh Đăng Ký Service

### Kiểm Tra Eureka Dashboard

Truy cập Eureka dashboard để xác minh nhiều instances đã được đăng ký:

- URL: `http://localhost:8070/eureka/apps`
- Tìm số lượng instance trong dấu ngoặc (ví dụ: LOANS (2))
- Mỗi instance sẽ có thông tin đăng ký riêng biệt

### Kết Quả Đăng Ký Mong Đợi

- **Accounts Microservice:** 1 instance
- **Cards Microservice:** 1 instance
- **Loans Microservice:** 2 instances

## Kiểm Tra Cân Bằng Tải Phía Client

### Hiểu Kịch Bản Kiểm Tra

Vì mỗi instance microservice sử dụng database H2 riêng trong demo này:
- Dữ liệu tạo trên một instance sẽ không có sẵn trên instance khác
- Điều này mô phỏng hành vi cân bằng tải
- Trong production, tất cả instances sẽ chia sẻ cùng database (MySQL, PostgreSQL, v.v.)

### Các Bước Kiểm Tra

1. **Tạo dữ liệu test trên một instance:**
   - Tạo thông tin tài khoản
   - Tạo thông tin thẻ
   - Tạo thông tin khoản vay chỉ sử dụng port 8090

2. **Kiểm tra API Fetch Customer Details:**
   ```
   GET /api/fetchCustomerDetails?mobileNumber={number}
   ```

3. **Quan sát kết quả:**
   - Một số request sẽ thành công (được route đến instance có dữ liệu)
   - Một số request sẽ thất bại với lỗi "Loan not found" (được route đến instance không có dữ liệu)
   - Hành vi luân phiên này chứng minh cân bằng tải đang hoạt động

## Cách Hoạt Động của Cân Bằng Tải Phía Client

### Các Thành Phần Chính

1. **Eureka Server:** Duy trì service registry
2. **Eureka Client:** Mỗi instance microservice tự đăng ký
3. **OpenFeign Client:** Xử lý cân bằng tải ở cấp độ client
4. **Service Discovery:** Tự động phát hiện các instances có sẵn

### Luồng Cân Bằng Tải

1. Account service truy vấn Eureka để lấy các instances Loans service khả dụng
2. OpenFeign Client nhận danh sách tất cả instances đã đăng ký
3. Các requests được phân phối qua các instances sử dụng thuật toán cân bằng tải
4. Mỗi request có thể được route đến một instance khác nhau

## Các Cân Nhắc về Hiệu Suất

### Môi Trường Development Cục Bộ

- **Sử Dụng CPU:** Có thể đạt 200-500% với nhiều containers
- **Tài Nguyên Docker:** Phân bổ ít nhất 5 cores cho hiệu suất tối ưu
- **Thời Gian Khởi Động:** 3-4 phút để khởi tạo hoàn toàn
- **Memory:** Giám sát phân bổ memory của Docker

### Môi Trường Production

- Tất cả instances nên kết nối đến database được chia sẻ (MySQL, PostgreSQL)
- Cân nhắc sử dụng Kubernetes cho orchestration tốt hơn
- Cân bằng tải phía server có thể được triển khai cùng với phía client

## Những Điểm Chính Cần Nhớ

1. **Nhiều Instances:** Dễ dàng tạo bằng cách nhân bản cấu hình Docker Compose
2. **Tự Động Phát Hiện:** Eureka tự động theo dõi tất cả instances
3. **Cân Bằng Tải Phía Client:** OpenFeign xử lý phân phối một cách trong suốt
4. **Không Cần Load Balancer Bên Ngoài:** Cân bằng tải xảy ra ở cấp độ ứng dụng
5. **Khả Năng Mở Rộng:** Thêm hoặc xóa instances mà không cần thay đổi code

## Các Bước Tiếp Theo

- Khám phá service discovery phía server với Kubernetes
- Triển khai health checks và graceful shutdown
- Cấu hình các thuật toán cân bằng tải tùy chỉnh
- Thiết lập databases cấp production cho shared state

## Kết Luận

Cân bằng tải phía client với Spring Cloud và Eureka cung cấp một cách tiếp cận phi tập trung mạnh mẽ để phân phối requests qua nhiều instances của service. Thư viện OpenFeign Client tích hợp liền mạch với Eureka Service Discovery để cho phép cân bằng tải tự động mà không cần load balancers bên ngoài.

---

**Các Chủ Đề Liên Quan:**
- Service Discovery và Registration
- Cấu Hình Eureka Server
- Triển Khai OpenFeign Client
- Docker Compose cho Microservices
- Các Mẫu Khả Năng Mở Rộng Microservice



================================================================================
FILE: 24-exploring-graalvm-cho-nha-phat-trien-microservice.md
================================================================================

# Khám Phá GraalVM: Kiến Thức Cần Thiết Cho Các Nhà Phát Triển Microservice

## Tổng Quan

GraalVM đã xuất hiện như một yếu tố thay đổi cuộc chơi trong hệ sinh thái Java, mang đến nhiều lợi thế cho các nhà phát triển microservice. Việc hiểu rõ khả năng của nó không chỉ là có lợi mà gần như là điều cần thiết trong bối cảnh năng động ngày nay.

## GraalVM Là Gì?

GraalVM là một runtime hiệu suất cao cung cấp các cải tiến đáng kể về hiệu suất và hiệu quả ứng dụng. Nó cung cấp khả năng đa ngôn ngữ (polyglot), cho phép bạn chạy nhiều ngôn ngữ lập trình trên một VM duy nhất.

## Lợi Ích Chính Cho Phát Triển Microservice

### 1. **Thời Gian Khởi Động Nhanh Hơn**
Biên dịch native image của GraalVM cho phép microservices khởi động nhanh hơn đáng kể so với các ứng dụng dựa trên JVM truyền thống. Điều này rất quan trọng cho các microservices cần mở rộng quy mô nhanh chóng trong môi trường cloud.

### 2. **Giảm Dung Lượng Bộ Nhớ**
Native images được biên dịch với GraalVM tiêu thụ ít bộ nhớ hơn, khiến chúng trở nên lý tưởng cho các microservices được đóng gói trong container, nơi hiệu quả tài nguyên là tối quan trọng.

### 3. **Cải Thiện Hiệu Suất**
Các tối ưu hóa tiên tiến của GraalVM mang lại hiệu suất runtime tốt hơn, dẫn đến thời gian phản hồi nhanh hơn cho microservices của bạn.

### 4. **Tương Thích Cloud-Native Tốt Hơn**
Với các container images nhỏ hơn và thời gian khởi động nhanh hơn, các microservices dựa trên GraalVM hoàn toàn phù hợp với Kubernetes và các nền tảng cloud-native khác.

## Tại Sao Nó Cần Thiết Cho Các Nhà Phát Triển Hiện Đại

Trong kiến trúc microservices ngày nay, nơi mà:
- **Khả năng mở rộng (Scalability)** là quan trọng
- **Hiệu quả tài nguyên** ảnh hưởng trực tiếp đến chi phí
- **Triển khai nhanh** là lợi thế cạnh tranh

GraalVM cung cấp các công cụ cần thiết để xây dựng các microservices hiệu quả hơn, hiệu suất cao hơn và tiết kiệm chi phí hơn.

## Bắt Đầu

Để tìm hiểu sâu hơn về GraalVM và ý nghĩa của nó đối với phát triển microservice, hãy cân nhắc khám phá:

- Tài liệu chính thức của GraalVM
- Tích hợp Spring Native cho các ứng dụng Spring Boot
- Framework Quarkus để tối ưu hóa microservices với GraalVM
- Kỹ thuật đánh giá hiệu suất và tối ưu hóa

## Kết Luận

Khi hệ sinh thái Java tiếp tục phát triển, GraalVM đại diện cho một bước tiến quan trọng đối với các nhà phát triển microservice. Lợi ích của nó về thời gian khởi động, sử dụng bộ nhớ và hiệu suất tổng thể khiến nó trở thành một công cụ vô giá để xây dựng các ứng dụng cloud-native hiện đại.

---

*Ghi chú: Tài liệu này là một phần của loạt bài về phát triển microservices với Java và Spring Boot.*



================================================================================
FILE: 25-exploring-graalvm-for-microservice-developers.md
================================================================================

# Khám Phá GraalVM cho Nhà Phát Triển Microservice

## Lưu Ý Quan Trọng về GraalVM

👉 **Khám Phá GraalVM: Kiến Thức Bắt Buộc cho Nhà Phát Triển Microservice**

GraalVM đã nổi lên như một yếu tố thay đổi cuộc chơi trong hệ sinh thái Java, mang đến nhiều lợi ích cho các nhà phát triển microservice. Việc hiểu được khả năng của nó không chỉ có lợi mà gần như là thiết yếu trong bối cảnh năng động ngày nay.

Để tìm hiểu sâu hơn về GraalVM và những tác động của nó đối với phát triển microservice, tôi đặc biệt khuyến nghị xem video tại liên kết sau:

**Video YouTube:** [Khám Phá GraalVM cho Nhà Phát Triển Microservice](https://www.youtube.com/watch?v=example)

## Giới Thiệu về GraalVM

GraalVM tăng tốc hiệu suất ứng dụng trong khi tiêu thụ ít tài nguyên hơn—cải thiện hiệu quả ứng dụng và giảm chi phí IT. Nó đạt được điều này bằng cách biên dịch ứng dụng Java của bạn trước thời gian (ahead of time) thành một tệp nhị phân native. Tệp nhị phân này nhỏ hơn, khởi động nhanh hơn tới 100 lần, cung cấp hiệu suất đỉnh cao mà không cần warmup, và sử dụng ít bộ nhớ và CPU hơn so với một ứng dụng chạy trên Java Virtual Machine (JVM).

Với tối ưu hóa hướng dẫn bởi profile và bộ thu gom rác G1 (Garbage-First), bạn có thể đạt được độ trễ thấp hơn và hiệu suất đỉnh cao ngang bằng hoặc tốt hơn, cũng như thông lượng so với một ứng dụng chạy trên JVM.

## Lợi Ích Chính

Các lợi ích chính của GraalVM bao gồm:

### Sử Dụng Tài Nguyên Thấp
Một ứng dụng Java được biên dịch ahead-of-time bởi GraalVM yêu cầu ít bộ nhớ và CPU hơn để chạy. Không có bộ nhớ và chu kỳ CPU nào được sử dụng cho biên dịch just-in-time. Kết quả là, ứng dụng của bạn cần ít tài nguyên hơn để chạy và rẻ hơn để vận hành ở quy mô lớn.

### Khởi Động Nhanh
Với GraalVM, bạn có thể khởi động ứng dụng Java nhanh hơn bằng cách khởi tạo các phần của nó tại thời điểm build thay vì runtime, và ngay lập tức đạt được hiệu suất đỉnh cao có thể dự đoán mà không cần warmup.

### Đóng Gói Nhỏ Gọn
Một ứng dụng Java được biên dịch ahead-of-time bởi GraalVM có kích thước nhỏ và có thể dễ dàng được đóng gói vào một container image nhẹ để triển khai nhanh chóng và hiệu quả.

### Bảo Mật Được Cải Thiện
GraalVM giảm bề mặt tấn công của ứng dụng Java bằng cách loại trừ những điều sau:
- Code không thể truy cập được (các class, method và field không sử dụng)
- Cơ sở hạ tầng biên dịch just-in-time
- Code được khởi tạo tại build-time

Giả định thế giới đóng (closed world assumption) của GraalVM ngăn ứng dụng của bạn load code không xác định bằng cách vô hiệu hóa các tính năng động như reflection, serialization, v.v. tại runtime, và yêu cầu một danh sách bao gồm rõ ràng các class, method và field như vậy tại build time. GraalVM có thể nhúng software bill of materials (SBOM) vào tệp nhị phân của bạn, giúp bạn dễ dàng sử dụng các công cụ quét bảo mật phổ biến để kiểm tra ứng dụng Java của bạn về các Common Vulnerabilities and Exposures (CVEs) đã được công bố.

### Dễ Dàng Xây Dựng Microservices Cloud Native
Các framework microservices phổ biến như **Micronaut**, **Spring Boot**, **Helidon**, và **Quarkus**, cũng như các nền tảng cloud như:
- Oracle Cloud Infrastructure (OCI)
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- Microsoft Azure

Tất cả đều hỗ trợ GraalVM. Điều này giúp bạn dễ dàng xây dựng các microservices Java cloud native, được biên dịch thành tệp nhị phân, đóng gói trong các container nhỏ, và chạy trên các nền tảng cloud phổ biến nhất.

### Mở Rộng Ứng Dụng Java với Python và Các Ngôn Ngữ Khác
Với GraalVM, bạn có thể nhúng các ngôn ngữ như Python, JavaScript và các ngôn ngữ khác để mở rộng ứng dụng Java của bạn.

### Sử Dụng Các Công Cụ Phát Triển và Giám Sát Hiện Có
Các công cụ phát triển và giám sát ứng dụng Java hiện có của bạn hoạt động với các tệp nhị phân ứng dụng GraalVM. GraalVM cung cấp:
- Build plugins cho Maven và Gradle
- GitHub Actions cho CI/CD
- Hỗ trợ Java Flight Recorder (JFR)
- Java Management Extensions (JMX)
- Heap dumps, VisualVM và các công cụ giám sát khác
- Tích hợp với các editor/IDE Java hiện có
- Các framework unit test như JUnit

## Cấp Phép và Hỗ Trợ

**Oracle GraalVM** được cấp phép theo GraalVM Free Terms and Conditions (GFTC) bao gồm License for Early Adopter Versions. Tuân theo các điều kiện trong giấy phép, bao gồm License for Early Adopter Versions, GFTC được thiết kế để cho phép sử dụng bởi bất kỳ người dùng nào bao gồm sử dụng thương mại và sản xuất. Phân phối lại được cho phép miễn là không tính phí.

**GraalVM Community Edition** là dự án mã nguồn mở được xây dựng từ các nguồn có sẵn trên GitHub và được phân phối theo phiên bản 2 của GNU General Public License với "Classpath" Exception, là các điều khoản tương tự như đối với Java. Kiểm tra giấy phép của các thành phần GraalVM riêng lẻ thường là dẫn xuất của giấy phép của một ngôn ngữ cụ thể và có thể khác nhau.

## Bắt Đầu với Oracle GraalVM

Tại đây bạn có thể tìm thấy thông tin về cách cài đặt Oracle GraalVM và chạy các ứng dụng cơ bản với nó.

Nếu bạn mới làm quen với Oracle GraalVM, chúng tôi khuyên bạn nên bắt đầu với GraalVM Overview, nơi bạn sẽ tìm thấy thông tin về lợi ích, phân phối, nền tảng được chứng nhận, các tính năng có sẵn và cấp phép của GraalVM.

Nếu bạn đã cài đặt Oracle GraalVM và có kinh nghiệm sử dụng nó, bạn có thể bỏ qua trang này và chuyển đến các hướng dẫn tham khảo chuyên sâu.

### Cài Đặt

Các bước cài đặt cho nền tảng cụ thể của bạn:
- Oracle Linux
- Linux
- macOS
- Windows

### Chạy Ứng Dụng

Oracle GraalVM bao gồm Java Development Kit (JDK), trình biên dịch just-in-time (Graal compiler), Native Image, và các công cụ Java quen thuộc khác. Bạn có thể sử dụng GraalVM JDK giống như bất kỳ JDK nào khác trong IDE của bạn, vì vậy sau khi cài đặt Oracle GraalVM, bạn có thể chạy bất kỳ ứng dụng Java nào mà không cần sửa đổi.

Trình khởi chạy `java` chạy JVM với Graal như trình biên dịch tầng cuối. Kiểm tra phiên bản Java đã cài đặt:

```bash
java -version
```

Sử dụng GraalVM Native Image, bạn có thể biên dịch bytecode Java thành một tệp thực thi native độc lập, dành riêng cho nền tảng để đạt được khởi động nhanh hơn và dung lượng nhỏ hơn cho ứng dụng của bạn.

Biên dịch ứng dụng `HelloWorld.java` này thành bytecode và sau đó xây dựng một tệp thực thi native:

```java
public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("Hello, World!");
  }
}
```

```bash
javac HelloWorld.java
```

```bash
native-image HelloWorld
```

Lệnh cuối cùng tạo ra một tệp thực thi có tên `helloworld` trong thư mục làm việc hiện tại. Gọi nó sẽ chạy code đã được biên dịch native của class HelloWorld như sau:

```bash
./helloworld
Hello, World!
```

> **Lưu ý:** Để biên dịch, `native-image` phụ thuộc vào toolchain cục bộ. Đảm bảo hệ thống của bạn đáp ứng các điều kiện tiên quyết.

## Điều Gì Nên Đọc Tiếp Theo

### Người Dùng Mới
Tiếp tục với Native Image basics để tự học về công nghệ này. Đối với người dùng đã quen thuộc với GraalVM Native Image nhưng có thể có ít kinh nghiệm sử dụng nó, hãy chuyển đến User Guides.

Để biết thêm thông tin về trình biên dịch, hãy xem Graal Compiler. Các ví dụ Java lớn hơn có thể được tìm thấy trong kho lưu trữ GraalVM Demos trên GitHub.

### Người Dùng Nâng Cao
Các nhà phát triển có kinh nghiệm hơn với GraalVM hoặc muốn làm nhiều hơn với GraalVM có thể chuyển trực tiếp đến Reference Manuals để có tài liệu chuyên sâu.

Bạn có thể tìm thấy thông tin về mô hình bảo mật của GraalVM trong Security Guide, và tài liệu API phong phú trong Oracle GraalVM Java API Reference.

### Người Dùng Oracle Cloud Infrastructure
Người dùng Oracle Cloud Infrastructure đang cân nhắc Oracle GraalVM cho khối lượng công việc cloud của họ được mời đọc Oracle GraalVM on OCI. Trang này tập trung vào việc sử dụng Oracle GraalVM với một Oracle Cloud Infrastructure Compute instance.

Chúng tôi cũng khuyến nghị kiểm tra [GraalVM Team Blog](https://graalvm.org/blog).

---

*Tài liệu này cung cấp tổng quan toàn diện về GraalVM cho các nhà phát triển microservice làm việc với ứng dụng Java và Spring Boot.*



================================================================================
FILE: 26-graalvm-native-image-guide.md
================================================================================

# GraalVM Native Image: Hướng Dẫn Đầy Đủ

## Giới Thiệu

Native Image là công nghệ biên dịch mã Java ahead-of-time thành tệp nhị phân—một file thực thi native. File thực thi native chỉ bao gồm mã cần thiết tại thời điểm chạy, cụ thể là các lớp ứng dụng, các lớp thư viện chuẩn, runtime của ngôn ngữ, và mã native được liên kết tĩnh từ JDK.

## Lợi Thế Chính

File thực thi được tạo ra bởi Native Image có nhiều lợi thế quan trọng:

- **Hiệu Quả Tài Nguyên**: Sử dụng một phần nhỏ tài nguyên so với Java Virtual Machine, do đó rẻ hơn khi chạy
- **Khởi Động Nhanh**: Khởi động trong vài mili giây
- **Hiệu Suất Đỉnh Ngay Lập Tức**: Đạt hiệu suất đỉnh ngay lập tức, không cần thời gian khởi động
- **Triển Khai Nhẹ**: Có thể đóng gói thành container image nhẹ để triển khai nhanh chóng và hiệu quả
- **Bảo Mật Tăng Cường**: Giảm thiểu bề mặt tấn công

## Cách Hoạt Động của Native Image

File thực thi native được tạo ra bởi Native Image builder hoặc công cụ `native-image`, công cụ này xử lý các lớp ứng dụng và metadata khác để tạo ra file nhị phân cho hệ điều hành và kiến trúc cụ thể.

Quá trình bao gồm hai bước chính:

1. **Phân Tích Tĩnh**: Công cụ `native-image` thực hiện phân tích tĩnh mã của bạn để xác định các lớp và phương thức có thể truy cập khi ứng dụng chạy
2. **Biên Dịch**: Nó biên dịch các lớp, phương thức và tài nguyên thành file nhị phân

Toàn bộ quá trình này được gọi là **build time** để phân biệt rõ ràng với việc biên dịch mã nguồn Java thành bytecode.

## Mục Lục

- Xây Dựng Native Executable Sử Dụng Maven hoặc Gradle
- Xây Dựng Native Executable Sử Dụng Công Cụ native-image
- Cấu Hình Build
- Cấu Hình Native Image với Thư Viện Bên Thứ Ba
- Đọc Thêm

## Yêu Cầu Tiên Quyết

Công cụ `native-image`, có sẵn trong thư mục bin của bản cài đặt GraalVM, phụ thuộc vào toolchain cục bộ (header files cho thư viện C, glibc-devel, zlib, gcc, và/hoặc libstdc++-static).

### Linux

Trên **Oracle Linux** sử dụng trình quản lý gói yum:
```bash
sudo yum install gcc glibc-devel zlib-devel
```

Một số bản phân phối Linux có thể yêu cầu thêm `libstdc++-static`. Bạn có thể cài đặt nó nếu các repository tùy chọn được kích hoạt (ol7_optional_latest trên Oracle Linux 7, ol8_codeready_builder trên Oracle Linux 8, và ol9_codeready_builder trên Oracle Linux 9).

Trên **Ubuntu Linux** sử dụng trình quản lý gói apt-get:
```bash
sudo apt-get install build-essential zlib1g-dev
```

Trên **các bản phân phối Linux khác** sử dụng trình quản lý gói dnf:
```bash
sudo dnf install gcc glibc-devel zlib-devel libstdc++-static
```

### MacOS

Trên macOS sử dụng xcode:
```bash
xcode-select --install
```

### Windows

Để sử dụng Native Image trên Windows, bạn cần Microsoft Visual C++ (MSVC) compiler phiên bản 14.x hoặc mới hơn. Cách dễ nhất để cài đặt là sử dụng Windows Package Manager (winget):

```powershell
winget install --id Microsoft.VisualStudio.2022.BuildTools --source winget
```

Bạn cũng có thể:
- Cài đặt Visual Studio 2022 phiên bản 17.13.2 hoặc bất kỳ phiên bản tương thích mới hơn
- Cài đặt Visual Studio Build Tools với Windows 11 SDK (hoặc phiên bản mới hơn)
- Cài đặt Visual Studio với Windows 11 SDK (hoặc phiên bản mới hơn)

Tất cả các phương pháp cài đặt đều phải bao gồm Windows SDK. Native Image chạy trên cả PowerShell và Command Prompt và sẽ tự động phát hiện cài đặt Visual Studio của bạn.

## Xây Dựng Native Executable Sử Dụng Maven

### Thiết Lập Dự Án Maven

Plugin Maven cho Native Image thêm hỗ trợ biên dịch ứng dụng Java thành file thực thi native sử dụng Apache Maven.

Tạo dự án Maven Java mới có tên "helloworld" với cấu trúc sau:

```
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── App.java
```

Bạn có thể chạy lệnh này để tạo dự án Maven mới:

```bash
mvn archetype:generate -DgroupId=com.example -DartifactId=helloworld -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

### Cấu Hình pom.xml

Thêm các plugin Maven thông thường để biên dịch và đóng gói dự án:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.12.1</version>
            <configuration>
                <fork>true</fork>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.3.0</version>
            <configuration>
                <archive>
                    <manifest>
                        <mainClass>com.example.App</mainClass>
                        <addClasspath>true</addClasspath>
                    </manifest>
                </archive>
            </configuration>
        </plugin>
    </plugins>
</build>
```

Kích hoạt plugin Maven cho Native Image bằng cách thêm profile sau:

```xml
<profiles>
  <profile>
    <id>native</id>
    <build>
      <plugins>
        <plugin>
          <groupId>org.graalvm.buildtools</groupId>
          <artifactId>native-maven-plugin</artifactId>
          <version>${native.maven.plugin.version}</version>
          <extensions>true</extensions>
          <executions>
            <execution>
            <id>build-native</id>
              <goals>
                <goal>compile-no-fork</goal>
              </goals>
              <phase>package</phase>
            </execution>
          </executions>
        </plugin>
      </plugins>
    </build>
  </profile>
</profiles>
```

### Build và Chạy

Biên dịch dự án và xây dựng file thực thi native:

```bash
mvn -Pnative package
```

File thực thi native có tên `helloworld` được tạo trong thư mục `target/`.

Chạy file thực thi:

```bash
./target/helloworld
```

## Xây Dựng Native Executable Sử Dụng Gradle

### Thiết Lập Dự Án Gradle

Tạo dự án Gradle Java mới có tên "helloworld" với cấu trúc sau:

```
├── app
│   ├── build.gradle
│   └── src
│       ├── main
│       │   ├── java
│       │   │   └── org
│       │   │       └── example
│       │   │           └── App.java
│       │   └── resources
```

Khởi tạo dự án Gradle mới:

```bash
mkdir helloworld && cd helloworld
gradle init --project-name helloworld --type java-application --test-framework junit-jupiter --dsl groovy
```

### Cấu Hình build.gradle

Kích hoạt plugin Gradle cho Native Image:

```groovy
plugins {
    // ...
    id 'org.graalvm.buildtools.native' version 'x.x.x'
}
```

### Build và Chạy

Xây dựng file thực thi native:

```bash
./gradlew nativeCompile
```

File thực thi native có tên `app` được tạo trong thư mục `app/build/native/nativeCompile/`.

Chạy file thực thi native:

```bash
./app/build/native/nativeCompile/app
```

## Xây Dựng Sử Dụng Công Cụ native-image

### Từ File Class

Tạo file Java đơn giản `HelloWorld.java`:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Native World!");
    }
}
```

Biên dịch và xây dựng file thực thi native:

```bash
javac HelloWorld.java
native-image HelloWorld
```

Chạy ứng dụng:

```bash
./helloworld
```

Đo hiệu suất:

```bash
time -f 'Elapsed Time: %e s Max RSS: %M KB' ./helloworld
# Kết quả:
# Hello, Native World!
# Elapsed Time: 0.00 s Max RSS: 7620 KB
```

### Từ File JAR

Xây dựng file thực thi native từ file JAR:

```bash
native-image [options] -jar jarfile [imagename]
```

Hành vi mặc định của `native-image` được căn chỉnh với lệnh `java`. Ví dụ:
- `java -jar App.jar someArgument` trở thành `native-image -jar App.jar` và `./App someArgument`

### Từ Module

Xây dựng file thực thi native từ Java module:

```bash
native-image [options] --module <module>[/<mainclass>] [options]
```

## Cấu Hình Build

Có nhiều tùy chọn bạn có thể truyền cho công cụ `native-image` để cấu hình quá trình build. Chạy `native-image --help` để xem danh sách đầy đủ. Các tùy chọn được truyền cho `native-image` được đánh giá từ trái sang phải.

## Làm Việc với Thư Viện Bên Thứ Ba

### Giả Định Thế Giới Đóng

Xây dựng file nhị phân độc lập với `native-image` diễn ra theo "giả định thế giới đóng" (closed world assumption). Công cụ `native-image` thực hiện phân tích để xem các lớp, phương thức và trường nào trong ứng dụng của bạn có thể truy cập và phải được bao gồm trong file thực thi native.

**Quan trọng**: Phân tích là tĩnh—nó không chạy ứng dụng của bạn. Điều này có nghĩa là tất cả bytecode trong ứng dụng của bạn có thể được gọi tại runtime phải được biết (quan sát và phân tích) tại thời điểm build.

### Yêu Cầu Metadata

Phân tích có thể xác định một số trường hợp dynamic class loading, nhưng không phải lúc nào cũng có thể dự đoán đầy đủ tất cả việc sử dụng:
- Java Native Interface (JNI)
- Java Reflection
- Dynamic Proxy objects
- Class path resources

### Cung Cấp Metadata

Để xử lý các tính năng động này, bạn cung cấp thông tin chi tiết về các lớp sử dụng Reflection, Proxy, v.v. cho phân tích. Bạn có thể:
- Cung cấp cho công cụ `native-image` các file cấu hình định dạng JSON
- Tính toán trước metadata trong mã

### Tài Nguyên Bổ Sung

Một số ứng dụng có thể cần cấu hình bổ sung để được biên dịch với Native Image. Native Image cũng có thể tương tác với các ngôn ngữ native thông qua API tùy chỉnh, cho phép bạn chỉ định các điểm vào native tùy chỉnh vào ứng dụng Java của bạn và xây dựng nó thành thư viện chia sẻ native.

## Đọc Thêm

- Kiểm tra trang **Basics of Native Image** để hiểu rõ hơn các khía cạnh chính
- Xem xét các hướng dẫn người dùng để biết ví dụ demo và các tình huống sử dụng
- Khám phá tài liệu **Native Image Build Overview** và **Build Configuration**
- Chạy các workshop tương tác tại Luna Labs (tìm kiếm "Native Image")
- Gửi vấn đề trong GitHub cho các lỗi tiềm ẩn
- Tuân theo quy trình đóng góp chuẩn để đóng góp cho Native Image

## Kết Luận

GraalVM Native Image cung cấp một cách mạnh mẽ để biên dịch ứng dụng Java thành file thực thi native với lợi ích đáng kể về thời gian khởi động, sử dụng bộ nhớ và hiệu quả triển khai. Cho dù bạn đang xây dựng microservices với Spring Boot hay ứng dụng Java độc lập, Native Image có thể giúp tối ưu hóa hiệu suất và tiêu thụ tài nguyên của ứng dụng của bạn.



================================================================================
FILE: 27-api-gateway-and-routing-challenges.md
================================================================================

# Thách Thức về API Gateway và Định Tuyến trong Microservices

## Tổng Quan

Tài liệu này thảo luận về các thách thức khi chấp nhận lưu lượng truy cập bên ngoài vào mạng lưới microservices và giới thiệu mô hình API Gateway như một giải pháp để quản lý giao tiếp bên ngoài, định tuyến và các mối quan tâm xuyên suốt.

## Thách Thức #6: Quản Lý Giao Tiếp Bên Ngoài

### Vấn Đề

Khi xây dựng kiến trúc microservices, chúng ta phải giải quyết cách xử lý lưu lượng truy cập bên ngoài đi vào mạng lưới microservice. Không giống như giao tiếp nội bộ giữa các dịch vụ, giao tiếp bên ngoài yêu cầu xem xét cẩn thận một số khía cạnh quan trọng:

1. **Quản Lý Điểm Vào Duy Nhất**
2. **Triển Khai Các Mối Quan Tâm Xuyên Suốt**
3. **Khả Năng Định Tuyến Động**

## Các Thách Thức Chính

### 1. Duy Trì Một Điểm Vào Duy Nhất

**Câu hỏi:** Làm thế nào để duy trì một điểm vào duy nhất vào mạng lưới microservice?

**Tại sao điều này quan trọng:**

- **Không có điểm vào duy nhất**, các client bên ngoài phải:
  - Theo dõi tất cả các dịch vụ khác nhau trong mạng lưới microservice
  - Duy trì kiến thức về URL endpoint cho từng dịch vụ
  - Theo dõi số port cho từng dịch vụ
  - Xử lý service discovery ở phía client

- **Có điểm vào duy nhất**, các client bên ngoài có thể:
  - Giao tiếp với một thành phần trong mạng lưới microservices
  - Đơn giản hóa code phía client
  - Giảm sự phụ thuộc giữa client và dịch vụ
  - Tập trung quản lý truy cập

### 2. Xử Lý Các Mối Quan Tâm Xuyên Suốt

**Câu hỏi:** Làm thế nào để xử lý các mối quan tâm xuyên suốt như logging, auditing, tracing và security?

**Các mối quan tâm chính cần giải quyết:**

- **Authentication và Authorization**: Đảm bảo các request bên ngoài được xác thực và ủy quyền đúng cách
- **Logging**: Ghi lại thông tin request/response để giám sát
- **Auditing**: Theo dõi ai truy cập cái gì và khi nào
- **Tracing**: Theo dõi request qua các ranh giới dịch vụ để debug

**Tại sao tập trung hóa quan trọng:**

- Triển khai các mối quan tâm này trong mỗi microservice dẫn đến:
  - Code trùng lặp trên hàng trăm microservices
  - Hành vi không nhất quán
  - Khó bảo trì
  - Tăng thời gian phát triển

- Cách tiếp cận tốt hơn: Triển khai các mối quan tâm xuyên suốt ở một nơi duy nhất

### 3. Định Tuyến Động Dựa Trên Yêu Cầu Tùy Chỉnh

**Câu hỏi:** Làm thế nào để thực hiện định tuyến động dựa trên yêu cầu tùy chỉnh?

**Các kịch bản định tuyến phổ biến:**

- **Định tuyến dựa trên path**: Chuyển hướng request đến microservices cụ thể dựa trên đường dẫn request
- **Định tuyến dựa trên header**: Định tuyến dựa trên giá trị HTTP header
  - Ví dụ: Header phiên bản (v1, v2) để định tuyến đến các phiên bản dịch vụ khác nhau
- **Định tuyến logic nghiệp vụ tùy chỉnh**: Áp dụng các quy tắc định tuyến cụ thể dựa trên thuộc tính request

## Giải Pháp: Edge Server / API Gateway

### Edge Server Là Gì?

**Edge Server** (còn được gọi là **API Gateway** hoặc **Gateway**) là một server có khả năng:

- Nằm ở rìa của mạng lưới microservice
- Giám sát tất cả các request đến và đi
- Hoạt động như điểm vào duy nhất cho các client bên ngoài
- Xử lý định tuyến, bảo mật và các mối quan tâm xuyên suốt

### Tại Sao Sử Dụng Edge Server?

Mô hình Edge Server giải quyết các thách thức sau:

1. **Điểm Vào Tập Trung**: Cung cấp một điểm liên lạc duy nhất cho tất cả các client bên ngoài
2. **Các Mối Quan Tâm Xuyên Suốt**: Triển khai logging, security, auditing và tracing ở một nơi
3. **Định Tuyến Động**: Cho phép định tuyến linh hoạt dựa trên paths, headers hoặc logic tùy chỉnh
4. **Trừu Tượng Hóa Dịch Vụ**: Ẩn cấu trúc microservice nội bộ khỏi các client bên ngoài
5. **Chuyển Đổi Protocol**: Có thể chuyển đổi giữa các protocol khác nhau (REST, gRPC, v.v.)
6. **Load Balancing**: Phân phối request qua các instance dịch vụ

### Thuật Ngữ

Các thuật ngữ sau được sử dụng thay thế cho nhau trong ngành:

- **Edge Server** - Được đặt tên vì nó nằm ở rìa của mạng lưới
- **API Gateway** - Nhấn mạnh vai trò của nó như một gateway cho các API request
- **Gateway** - Dạng rút gọn của API Gateway

## Triển Khai trong Spring Boot

Khi triển khai Edge Server trong kiến trúc microservices Spring Boot, bạn thường sử dụng:

- **Spring Cloud Gateway** - Gateway hiện đại, reactive được xây dựng trên Spring WebFlux
- **Netflix Zuul** - Tùy chọn cũ (ít được sử dụng hơn hiện nay)

## Best Practices (Thực Hành Tốt Nhất)

1. **Giữ Gateway Nhẹ**: Tránh đặt logic nghiệp vụ trong gateway
2. **Triển Khai Circuit Breakers**: Bảo vệ chống lại các lỗi lan truyền
3. **Sử Dụng Caching**: Cache response khi thích hợp để giảm tải backend
4. **Giám Sát Hiệu Suất Gateway**: Theo dõi độ trễ, tỷ lệ lỗi và throughput
5. **Bảo Mật Gateway**: Triển khai authentication và authorization đúng cách
6. **Phiên Bản Hóa API**: Hỗ trợ nhiều phiên bản API thông qua định tuyến

## Bước Tiếp Theo

Để triển khai đầy đủ mô hình API Gateway, bạn cần:

1. Chọn công nghệ gateway phù hợp (ví dụ: Spring Cloud Gateway)
2. Cấu hình các quy tắc định tuyến cho microservices của bạn
3. Triển khai các filter authentication và authorization
4. Thiết lập logging, auditing và tracing
5. Cấu hình load balancing và circuit breakers
6. Kiểm tra gateway với các mẫu lưu lượng khác nhau

## Tóm Tắt

Mô hình API Gateway là thiết yếu để quản lý giao tiếp bên ngoài trong kiến trúc microservices. Bằng cách cung cấp một điểm vào duy nhất, tập trung hóa các mối quan tâm xuyên suốt và cho phép định tuyến động, Edge Server đơn giản hóa tương tác của client và cải thiện khả năng bảo trì tổng thể của hệ sinh thái microservices.

Không có API Gateway phù hợp, bạn có nguy cơ tạo ra một hệ thống phức tạp, phụ thuộc chặt chẽ, nơi các client bên ngoài phải quản lý service discovery và các mối quan tâm xuyên suốt bị trùng lặp trên nhiều dịch vụ.

---

**Điểm Chính**: Luôn duy trì một điểm vào duy nhất vào mạng lưới microservice của bạn bằng cách sử dụng Edge Server/API Gateway để xử lý định tuyến, bảo mật và các mối quan tâm xuyên suốt một cách hiệu quả.



================================================================================
FILE: 28-tai-sao-can-edge-server-api-gateway.md
================================================================================

# Tại Sao Chúng Ta Cần Edge Server (API Gateway) Trong Kiến Trúc Microservices

## Giới Thiệu

Tài liệu này giải thích sự cần thiết của việc có một edge server (API Gateway) riêng biệt trong kiến trúc microservices và những thách thức khi không có nó.

## Thách Thức Khi Không Có Edge Server

### Giao Tiếp Trực Tiếp Từ Client Đến Microservice

Trong kiến trúc microservices không có edge server:
- Các microservices riêng lẻ (accounts, loans, cards) được triển khai trên các server/container riêng biệt
- Các client bên ngoài giao tiếp trực tiếp với từng microservice tương ứng
- Trong các dự án thực tế với hơn 100 microservices, điều này tạo ra nhiều thách thức nghiêm trọng

### Các Vấn Đề Chính

1. **Thiếu Tính Nhất Quán**: Việc triển khai các cross-cutting concerns (bảo mật, kiểm toán, logging, routing) đòi hỏi phải lặp lại logic trên tất cả các microservices
2. **Không Nhất Quán Giữa Các Developer**: Các developer khác nhau có thể tuân theo các tiêu chuẩn khác nhau khi triển khai cùng một concerns
3. **Không Có Kiểm Soát Tập Trung**: Khó khăn trong việc áp dụng các thực hành bảo mật, kiểm toán và logging thống nhất

### Tại Sao Thư Viện Chung Không Giải Quyết Được Vấn Đề

Mặc dù việc xây dựng các cross-cutting concerns vào một thư viện chung có vẻ hợp lý, nhưng nó có những nhược điểm:

- **Khớp Nối Chặt Chẽ**: Tạo ra sự phụ thuộc giữa thư viện chung và tất cả các microservices
- **Bảo Trì Khó Khăn**: Các thay đổi về bảo mật, kiểm toán hoặc logging đòi hỏi:
  - Kiểm thử hồi quy toàn diện
  - Phân tích tác động trên tất cả các microservices
  - Không khả thi với số lượng lớn microservices

## Giải Pháp Edge Server

### Tổng Quan Kiến Trúc

```
Ứng dụng Client → Edge Server/API Gateway → Microservices
                                             ├─ Accounts
                                             ├─ Loans
                                             └─ Cards
```

### Cách Hoạt Động

1. Edge server nằm giữa các ứng dụng client và microservices
2. Nhận tất cả các request từ bên ngoài
3. Thực thi logic của các cross-cutting concerns
4. Xác thực các request
5. Chỉ chuyển tiếp đến microservice thực tế sau khi xác thực

## Khả Năng Của API Gateway

### Các Chức Năng Cốt Lõi

1. **Cross-Cutting Concerns**
   - Bảo mật (xác thực & phân quyền)
   - Logging
   - Kiểm toán
   - Định tuyến

2. **Khả Năng Chịu Lỗi & Độ Bền**
   - Ngăn chặn lỗi lan truyền (cascading failures)
   - Làm cho các dịch vụ downstream có khả năng chịu lỗi
   - Triển khai circuit breaker
   - Xử lý ngoại lệ

3. **Quản Lý Lưu Lượng**
   - Retry và timeout cho các lệnh gọi dịch vụ nội bộ
   - Chính sách quota dựa trên gói đăng ký của client (standard, premium, advanced)
   - Giới hạn tốc độ (rate limiting)

### Quy Trình Xử Lý Request

API Gateway xử lý các request qua nhiều giai đoạn:

1. **Giai Đoạn Xác Thực**
   - Xác thực request
   - Blacklist/whitelist địa chỉ IP
   - Kiểm tra danh sách include/exclude

2. **Giai Đoạn Bảo Mật**
   - Xác thực (Authentication)
   - Phân quyền (Authorization)

3. **Kiểm Soát Lưu Lượng**
   - Giới hạn tốc độ (Rate limiting)
   - Áp dụng quota

4. **Định Tuyến & Chuyển Đổi**
   - Định tuyến động
   - Service discovery
   - Chỉnh sửa request/response
   - Chuyển đổi giao thức (ví dụ: HTTPS → HTTP)

5. **Giám Sát & Logging**
   - Tích hợp với công cụ giám sát (Grafana)
   - Logging tập trung
   - Theo dõi lỗi qua dashboard

6. **Caching** (Tùy chọn)
   - Tích hợp Redis cache
   - Logic nghiệp vụ dựa trên cache

## API Gateway vs Eureka Server

### Tại Sao Không Dùng Eureka Cho Mọi Thứ?

**Mục Đích Của Eureka Server**: Tập trung nghiêm ngặt vào service discovery và service registry

**Mục Đích Của API Gateway**: Xử lý các yêu cầu phi chức năng và cross-cutting concerns

### Lợi Ích Của Việc Tách Biệt

- **Linh Hoạt**: Tổ chức có thể chọn component nào để sử dụng
- **Tách Biệt Mối Quan Tâm**: Các component khác nhau xử lý các vấn đề khác nhau
- **Triển Khai Tùy Chọn**: Chức năng Gateway có thể được bỏ qua nếu không cần

## Triển Khai Với Spring Cloud

Việc xây dựng API Gateway có thể có vẻ phức tạp, nhưng các framework Spring Boot và Spring Cloud đơn giản hóa đáng kể việc triển khai.

### Điểm Chính

- Dễ dàng triển khai với Spring Cloud
- Các pattern và practices được tài liệu hóa tốt
- Giải pháp sẵn sàng cho doanh nghiệp
- Kiến trúc có khả năng mở rộng

## Tóm Tắt Ưu Điểm

✅ **Tính Nhất Quán**: Triển khai tập trung các cross-cutting concerns  
✅ **Khả Năng Bảo Trì**: Điểm duy nhất cho cập nhật và thay đổi  
✅ **Linh Hoạt**: Dễ dàng thay đổi chính sách mà không ảnh hưởng đến microservices  
✅ **Bảo Mật**: Xác thực và phân quyền tập trung  
✅ **Độ Bền**: Circuit breakers và khả năng chịu lỗi  
✅ **Giám Sát**: Logging và metrics thống nhất  
✅ **Kiểm Soát Lưu Lượng**: Quản lý rate limiting và quota  
✅ **Linh Hoạt Giao Thức**: Khả năng chuyển đổi giao thức  

## Kết Luận

Edge Server/API Gateway là thiết yếu cho:
- Quản lý giao tiếp bên ngoài trong microservices
- Triển khai các cross-cutting concerns một cách nhất quán
- Đảm bảo khả năng chịu lỗi và độ bền
- Cung cấp tính linh hoạt và khả năng bảo trì

Trong các phần tiếp theo, chúng ta sẽ khám phá cách Spring Cloud giúp triển khai các khả năng này trong kiến trúc microservices của chúng ta.

---

**Lưu ý**: Tất cả các chức năng có thể được kích hoạt hoặc vô hiệu hóa dựa trên yêu cầu nghiệp vụ. Các khả năng được đề cập là phổ biến nhưng không đầy đủ.



================================================================================
FILE: 29-spring-cloud-gateway-introduction.md
================================================================================

# Giới Thiệu Spring Cloud Gateway

## Tổng Quan

Spring Cloud Gateway là một dự án trong Spring Cloud cho phép các lập trình viên dễ dàng tạo ra các edge service đạt chuẩn production và sẵn sàng triển khai. Gateway này đóng vai trò là điểm tiếp nhận cho mọi giao tiếp bên ngoài trong mạng lưới microservices của bạn.

## Tính Năng Chính

### Xây Dựng Trên Spring Reactive Framework

Spring Cloud Gateway được xây dựng trên nền tảng Spring Reactive framework, cho phép:
- Xử lý mượt mà mọi khối lượng công việc
- Xử lý hiệu quả lượng traffic lớn
- Hoạt động với yêu cầu bộ nhớ và thread tối thiểu
- Cung cấp các thao tác reactive không chặn (non-blocking)

### Đóng Vai Trò Gatekeeper (Người Gác Cổng)

Gateway nằm giữa các ứng dụng client và microservices, cung cấp:
- **Điểm Vào Tập Trung**: Mọi traffic đến đều phải đi qua gateway
- **Bảo Mật**: Các ứng dụng client không thể tương tác trực tiếp với từng microservice riêng lẻ
- **Trong Suốt Vị Trí**: Client không cần biết địa chỉ vật lý của các instance microservice

## Dễ Dàng Phát Triển

Xây dựng gateway với Spring Cloud Gateway rất đơn giản:
- Tương tự như xây dựng bất kỳ ứng dụng Spring Boot nào khác
- Yêu cầu code tối thiểu
- Cấu hình đơn giản
- Ít dependency cần thêm vào

Nếu bạn đã là lập trình viên Spring Boot, bạn sẽ thấy rất dễ dàng khi làm việc với Spring Cloud Gateway.

## Khả Năng và Trường Hợp Sử Dụng

### Định Tuyến Động (Dynamic Routing)

Gateway có thể định tuyến động các request dựa trên nhiều ngữ cảnh khác nhau:
- **Định Tuyến Theo Phiên Bản API**: Định tuyến request đến các microservice backend có phiên bản phù hợp dựa trên giá trị trong request header
- **Định Tuyến Dựa Trên Ngữ Cảnh**: Định tuyến thông minh dựa trên các thuộc tính của request

### Sticky Sessions

Hỗ trợ duy trì phiên làm việc của người dùng:
- Đảm bảo request của một người dùng cụ thể luôn đến cùng một instance microservice
- Duy trì tính nhất quán của session giữa các request

### Cross-Cutting Concerns (Mối Quan Tâm Xuyên Suốt)

Spring Cloud Gateway xử lý nhiều yêu cầu phi chức năng:
- Bảo mật
- Logging
- Auditing
- Thu thập metrics
- Giám sát
- Khả năng phục hồi (Resiliency)

### Điểm Thực Thi Chính Sách Tập Trung

Là một vị trí tập trung, gateway có thể thực thi:
- Chính sách định tuyến tĩnh và động
- Chính sách bảo mật
- Giới hạn tốc độ request (Rate limiting)
- Viết lại đường dẫn (Path rewriting)

## Spring Cloud Gateway vs. Zuul

Mặc dù **Zuul** là một lựa chọn phổ biến khác để xây dựng API gateway trong Java, Spring Cloud Gateway được ưa chuộng hơn vì:

| Tính Năng | Spring Cloud Gateway | Zuul |
|-----------|---------------------|------|
| Framework | Spring Reactor (Reactive) | Blocking |
| Hiệu Suất | Tốt hơn | Tốt |
| Tích Hợp Circuit Breaker | ✓ | Hạn chế |
| Tích Hợp Service Discovery | ✓ | ✓ |
| Non-blocking | ✓ | ✗ |

## Các Thành Phần Chính

### Predicates (Vị Từ)
Predicates được sử dụng để khớp các route dựa trên bất kỳ thuộc tính request nào, cho phép quyết định định tuyến linh hoạt.

### Filters (Bộ Lọc)
Filters dành riêng cho các route và có thể sửa đổi request và response khi chúng đi qua gateway.

### Điểm Tích Hợp
- **Circuit Breaker**: Hỗ trợ circuit breaker tích hợp sẵn
- **Spring Cloud Discovery Client**: Tích hợp với service discovery (ví dụ: Eureka Server)
- **Rate Limiting**: Khả năng giới hạn tốc độ request
- **Path Rewriting**: Sửa đổi đường dẫn động

## Tài Nguyên Chính Thức

Để biết thêm thông tin, truy cập dự án Spring Cloud Gateway chính thức tại [spring.io](https://spring.io):
1. Điều hướng đến Projects
2. Chọn Spring Cloud
3. Chọn Spring Cloud Gateway

### Mục Tiêu Dự Án

Theo tài liệu chính thức, Spring Cloud Gateway hướng đến:
- Cung cấp cách đơn giản và hiệu quả để định tuyến đến APIs
- Cung cấp các cross-cutting concerns như bảo mật, giám sát và khả năng phục hồi
- Cho phép dễ dàng triển khai predicates và filters
- Hỗ trợ giới hạn tốc độ request và viết lại đường dẫn

## Tóm Tắt

Spring Cloud Gateway là một giải pháp mạnh mẽ, sẵn sàng production để triển khai edge servers trong kiến trúc microservices. Tính chất reactive, dễ sử dụng và bộ tính năng toàn diện của nó làm cho nó trở thành lựa chọn xuất sắc để xử lý các yêu cầu API gateway trong các ứng dụng cloud-native hiện đại.

## Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Kiến trúc nội bộ của Spring Cloud Gateway
- Cách predicates và filters hoạt động
- Các ví dụ triển khai thực tế
- Các tùy chọn cấu hình nâng cao

---

*Tài liệu này là một phần của khóa học microservices toàn diện sử dụng Spring Boot và Spring Cloud.*



================================================================================
FILE: 3-docker-compose-mysql-integration.md
================================================================================

# Tích Hợp Docker Compose với MySQL Databases cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình Docker Compose để chạy các Spring Boot microservices cùng với các MySQL database containers. Chúng ta sẽ học cách thiết lập kết nối giữa microservices và databases sử dụng environment variables và service dependencies, thay thế cấu hình localhost được hardcode.

## Tại Sao Dùng Docker Compose Thay Vì Localhost?

### Vấn Đề Với Localhost

Khi chạy microservices cục bộ, chúng ta có thể sử dụng `localhost` trong `application.yml`:

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/accountsDB
```

**Cách này hoạt động ở local nhưng thất bại trong môi trường containerized** vì:
- Mỗi container có network namespace riêng
- `localhost` bên trong container chỉ đề cập đến chính container đó
- Containers không thể kết nối với containers khác qua `localhost`

### Giải Pháp Docker Compose

Docker Compose tạo một shared network nơi:
- Containers giao tiếp sử dụng **service names** làm hostnames
- Database URLs sử dụng service names thay vì `localhost`
- Environment variables ghi đè các giá trị được hardcode
- Tất cả containers khởi động theo đúng thứ tự dependency

## Yêu Cầu Tiên Quyết

- Docker Desktop đã cài đặt và đang chạy
- Spring Boot microservices (accounts, cards, loans, config server)
- Maven để build projects
- Code microservices trước đó với MySQL dependencies

## Bước 1: Dọn Dẹp Tài Nguyên Hiện Có

Trước khi bắt đầu với Docker Compose, dọn dẹp các instances và containers đang chạy.

### Dừng Tất Cả Microservices Đang Chạy

Dừng tất cả Spring Boot applications đang chạy trong IDE của bạn:
1. Dừng Accounts microservice
2. Dừng Cards microservice
3. Dừng Loans microservice
4. Dừng Config Server (nếu đang chạy)

### Dừng và Xóa Tất Cả Docker Containers

Vì chúng ta sẽ tạo containers thông qua Docker Compose, hãy xóa các containers được tạo thủ công:

```bash
# Xem tất cả containers đang chạy
docker ps

# Dừng tất cả containers
docker stop accountsDB cardsDB loansDB

# Xóa tất cả containers
docker rm accountsDB cardsDB loansDB
```

**Tại sao xóa?** Docker Compose sẽ quản lý vòng đời container, nên không còn cần containers thủ công.

### Xóa Docker Images Cũ (Tùy Chọn)

Giải phóng dung lượng đĩa bằng cách xóa images không dùng:

```bash
# Liệt kê tất cả images
docker images

# Xóa images cụ thể (ví dụ: images Section 6)
docker rmi eazybytes/accounts:s6
docker rmi eazybytes/cards:s6
docker rmi eazybytes/loans:s6
docker rmi eazybytes/configserver:s6
```

**Best Practice:** Thường xuyên dọn dẹp Docker images và containers không sử dụng để giải phóng storage và memory.

## Bước 2: Tạo Lại Docker Images với Cấu Hình Mới

Vì chúng ta đã thực hiện thay đổi (xóa H2, thêm MySQL), cần rebuild Docker images.

### Cập Nhật Image Tags trong pom.xml

Thay đổi tag từ `s6` sang `s7` trong tất cả microservices để phản ánh section/version mới.

**Accounts Microservice - pom.xml:**
```xml
<configuration>
    <to>
        <image>eazybytes/accounts:s7</image>
    </to>
</configuration>
```

**Cards Microservice - pom.xml:**
```xml
<configuration>
    <to>
        <image>eazybytes/cards:s7</image>
    </to>
</configuration>
```

**Loans Microservice - pom.xml:**
```xml
<configuration>
    <to>
        <image>eazybytes/loans:s7</image>
    </to>
</configuration>
```

**Config Server - pom.xml:**
```xml
<configuration>
    <to>
        <image>eazybytes/configserver:s7</image>
    </to>
</configuration>
```

Sau khi cập nhật, tải lại Maven changes trong IDE của bạn.

### Build Docker Images Sử Dụng Jib

Điều hướng đến thư mục mỗi microservice và build Docker image.

**Accounts Microservice:**
```bash
cd accounts
mvn compile jib:dockerBuild
```

**Cards Microservice:**
```bash
cd cards
mvn compile jib:dockerBuild
```

**Loans Microservice:**
```bash
cd loans
mvn compile jib:dockerBuild
```

**Config Server:**
```bash
cd configserver
mvn compile jib:dockerBuild
```

### Xác Minh Images Đã Được Tạo

Kiểm tra Docker Desktop hoặc chạy:
```bash
docker images | grep s7
```

Bạn sẽ thấy:
- `eazybytes/accounts:s7`
- `eazybytes/cards:s7`
- `eazybytes/loans:s7`
- `eazybytes/configserver:s7`

### Push Images Lên Docker Hub (Tùy Chọn Nhưng Được Khuyến Nghị)

```bash
docker push eazybytes/accounts:s7
docker push eazybytes/cards:s7
docker push eazybytes/loans:s7
docker push eazybytes/configserver:s7
```

**Tại sao push?** Repository tập trung đảm bảo images có thể truy cập từ bất kỳ môi trường nào.

## Bước 3: Tạo MySQL Database Services trong Docker Compose

Mở file `docker-compose.yml` trong thư mục default.

### Xóa RabbitMQ Service

Vì chúng ta đã xóa Spring Cloud Bus dependencies, RabbitMQ không còn cần thiết:

```yaml
# Xóa toàn bộ service block này
rabbitmq:
  image: rabbitmq:3.13-management
  # ... toàn bộ cấu hình rabbitmq
```

### Thêm Accounts Database Service

Tạo MySQL database service đầu tiên cho accounts:

```yaml
services:
  accountsdb:
    container_name: accountsdb
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: accountsDB
    extends:
      file: common-config.yml
      service: network-deploy-service
```

**Chi Tiết Cấu Hình:**

- **Service Name**: `accountsdb` - được các containers khác sử dụng để kết nối
- **Container Name**: `accountsdb` - tên thân thiện cho container
- **Port Mapping**: `3306:3306` - map host port 3306 đến container port 3306
- **Environment Variables**:
  - `MYSQL_DATABASE: accountsDB` - tạo database khi khởi động
- **Extends**: Kế thừa cấu hình chung từ `common-config.yml`

### Thêm Loans Database Service

```yaml
  loansdb:
    container_name: loansdb
    ports:
      - "3307:3306"
    environment:
      MYSQL_DATABASE: loansDB
    extends:
      file: common-config.yml
      service: network-deploy-service
```

**Điểm Khác Biệt Chính:**
- **Port Mapping**: `3307:3306` - expose trên host port 3307 (để tránh xung đột)
- **Database Name**: `loansDB`

### Thêm Cards Database Service

```yaml
  cardsdb:
    container_name: cardsdb
    ports:
      - "3308:3306"
    environment:
      MYSQL_DATABASE: cardsDB
    extends:
      file: common-config.yml
      service: network-deploy-service
```

**Điểm Khác Biệt Chính:**
- **Port Mapping**: `3308:3306` - expose trên host port 3308
- **Database Name**: `cardsDB`

## Bước 4: Cấu Hình Database Health Checks

Health checks đảm bảo databases đã khởi động hoàn toàn trước khi microservices cố gắng kết nối.

### Tạo Common Database Configuration

Trong `common-config.yml`, tạo cấu hình database có thể tái sử dụng:

```yaml
services:
  microservice-db-config:
    extends:
      service: network-deploy-service
    image: mysql:latest
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 10s
      retries: 10
      interval: 10s
      start_period: 10s
    environment:
      MYSQL_ROOT_PASSWORD: root
```

**Cấu Hình Health Check:**

- **test**: Lệnh kiểm tra sức khỏe database - ping MySQL server
- **timeout**: Thời gian tối đa chờ phản hồi - 10 giây
- **retries**: Số lần thử lại - 10 lần
- **interval**: Thời gian giữa các health checks - 10 giây
- **start_period**: Khoảng thời gian ân hạn trước khi bắt đầu health checks - 10 giây

**Cách hoạt động:**
1. Docker chạy `mysqladmin ping -h localhost`
2. Nếu thành công, container được đánh dấu là "healthy"
3. Nếu thất bại sau 10 lần thử, container được đánh dấu là "unhealthy"

### Extend Database Configuration trong docker-compose.yml

Cập nhật database services để extend cấu hình chung:

```yaml
  accountsdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: accountsdb
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: accountsDB

  loansdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: loansdb
    ports:
      - "3307:3306"
    environment:
      MYSQL_DATABASE: loansDB

  cardsdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: cardsdb
    ports:
      - "3308:3306"
    environment:
      MYSQL_DATABASE: cardsDB
```

**Lợi Ích:**
- Loại bỏ cấu hình lặp lại
- Health checks nhất quán trên tất cả databases
- Dễ dàng cập nhật tất cả databases cùng lúc

## Bước 5: Cấu Hình Kết Nối Database cho Microservices

### Thêm Common Database Credentials

Trong `common-config.yml`, thêm database credentials áp dụng cho tất cả microservices:

```yaml
  microservice-configserver-config:
    extends:
      service: network-deploy-service
    environment:
      SPRING_APPLICATION_NAME: configserver
      SPRING_PROFILES_ACTIVE: default
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root
```

**Tại sao ở đây?** Cả ba microservices sử dụng cùng database credentials (`root/root`), nên chúng ta định nghĩa một lần.

### Cấu Hình Accounts Microservice Database URL

Trong `docker-compose.yml`, thêm datasource URL cho accounts:

```yaml
  accounts:
    image: "eazybytes/accounts:s7"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    environment:
      SPRING_APPLICATION_NAME: accounts
      SPRING_DATASOURCE_URL: jdbc:mysql://accountsdb:3306/accountsDB
    depends_on:
      accountsdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config
```

**Cấu Hình Chính:**

- **SPRING_DATASOURCE_URL**: `jdbc:mysql://accountsdb:3306/accountsDB`
  - Sử dụng **service name** `accountsdb` thay vì `localhost`
  - Port `3306` là internal container port
  - Database name `accountsDB`

- **depends_on**: Đảm bảo `accountsdb` healthy trước khi khởi động accounts service
  - **condition: service_healthy** - đợi health check pass

### Cấu Hình Loans Microservice Database URL

```yaml
  loans:
    image: "eazybytes/loans:s7"
    container_name: loans-ms
    ports:
      - "8090:8090"
    environment:
      SPRING_APPLICATION_NAME: loans
      SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3306/loansDB
    depends_on:
      loansdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config
```

**Quan trọng:** 
- Service name: `loansdb`
- Internal port: `3306` (không phải 3307 - đó là host port)
- Database: `loansDB`

### Cấu Hình Cards Microservice Database URL

```yaml
  cards:
    image: "eazybytes/cards:s7"
    container_name: cards-ms
    ports:
      - "9000:9000"
    environment:
      SPRING_APPLICATION_NAME: cards
      SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3306/cardsDB
    depends_on:
      cardsdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config
```

**Quan trọng:**
- Service name: `cardsdb`
- Internal port: `3306` (không phải 3308)
- Database: `cardsDB`

## Bước 6: Hiểu Về Environment Variable Override

### Cách Spring Boot Xử Lý Cấu Hình

Spring Boot sử dụng thứ tự ưu tiên này (cao nhất đến thấp nhất):

1. **Command-line arguments**
2. **Environment variables** ⭐ (Được Docker Compose sử dụng)
3. **application.yml / application.properties**
4. **Default values**

### Ví Dụ: Ghi Đè Datasource URL

**Trong application.yml:**
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/accountsDB
```

**Docker Compose environment variable:**
```yaml
environment:
  SPRING_DATASOURCE_URL: jdbc:mysql://accountsdb:3306/accountsDB
```

**Kết quả:** Docker Compose environment variable **ghi đè** giá trị `localhost`.

### Quy Ước Đặt Tên Environment Variable

Chuyển đổi property keys thành environment variables:

| application.yml | Environment Variable |
|----------------|---------------------|
| `spring.datasource.url` | `SPRING_DATASOURCE_URL` |
| `spring.datasource.username` | `SPRING_DATASOURCE_USERNAME` |
| `spring.datasource.password` | `SPRING_DATASOURCE_PASSWORD` |
| `spring.application.name` | `SPRING_APPLICATION_NAME` |

**Quy tắc:**
- Thay `.` (dấu chấm) bằng `_` (gạch dưới)
- Chuyển thành CHỮ HOA

## Bước 7: Áp Dụng Cấu Hình cho QA và Prod

Lặp lại các thay đổi tương tự trong:
- `docker-compose-qa.yml`
- `docker-compose-prod.yml`

**Điểm Khác Biệt cho QA/Prod:**
- Image tags khác nhau (nếu sử dụng tags specific cho môi trường)
- Database credentials khác nhau (sử dụng secrets trong production)
- Resource limits khác nhau
- Cấu hình scaling khác nhau

## Cấu Trúc Docker Compose File Hoàn Chỉnh

### docker-compose.yml (Default)

```yaml
services:
  # Database Services
  accountsdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: accountsdb
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: accountsDB

  loansdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: loansdb
    ports:
      - "3307:3306"
    environment:
      MYSQL_DATABASE: loansDB

  cardsdb:
    extends:
      file: common-config.yml
      service: microservice-db-config
    container_name: cardsdb
    ports:
      - "3308:3306"
    environment:
      MYSQL_DATABASE: cardsDB

  # Config Server
  configserver:
    image: "eazybytes/configserver:s7"
    container_name: configserver-ms
    ports:
      - "8071:8071"
    healthcheck:
      test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 10s
    extends:
      file: common-config.yml
      service: microservice-base-config

  # Microservices
  accounts:
    image: "eazybytes/accounts:s7"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    environment:
      SPRING_APPLICATION_NAME: accounts
      SPRING_DATASOURCE_URL: jdbc:mysql://accountsdb:3306/accountsDB
    depends_on:
      configserver:
        condition: service_healthy
      accountsdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config

  loans:
    image: "eazybytes/loans:s7"
    container_name: loans-ms
    ports:
      - "8090:8090"
    environment:
      SPRING_APPLICATION_NAME: loans
      SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3306/loansDB
    depends_on:
      configserver:
        condition: service_healthy
      loansdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config

  cards:
    image: "eazybytes/cards:s7"
    container_name: cards-ms
    ports:
      - "9000:9000"
    environment:
      SPRING_APPLICATION_NAME: cards
      SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3306/cardsDB
    depends_on:
      configserver:
        condition: service_healthy
      cardsdb:
        condition: service_healthy
    extends:
      file: common-config.yml
      service: microservice-configserver-config

networks:
  eazybank:
    driver: bridge
```

### common-config.yml

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank

  microservice-db-config:
    extends:
      service: network-deploy-service
    image: mysql:latest
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 10s
      retries: 10
      interval: 10s
      start_period: 10s
    environment:
      MYSQL_ROOT_PASSWORD: root

  microservice-base-config:
    extends:
      service: network-deploy-service
    deploy:
      resources:
        limits:
          memory: 700m

  microservice-configserver-config:
    extends:
      service: microservice-base-config
    environment:
      SPRING_PROFILES_ACTIVE: default
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root

networks:
  eazybank:
    driver: bridge
```

## Tóm Tắt Các Khái Niệm Chính

### Service Names làm Hostnames

Trong Docker Compose networks:
- Service name = hostname
- `accountsdb` service → có thể truy cập tại `accountsdb:3306`
- `loansdb` service → có thể truy cập tại `loansdb:3306`
- Không cần địa chỉ IP

### Port Mapping vs Internal Ports

**Port Mapping** (host:container):
- `3306:3306` - Accounts DB (có thể truy cập từ host tại localhost:3306)
- `3307:3306` - Loans DB (có thể truy cập từ host tại localhost:3307)
- `3308:3306` - Cards DB (có thể truy cập từ host tại localhost:3308)

**Giao Tiếp Nội Bộ Container:**
- Luôn sử dụng container port (3306)
- `jdbc:mysql://accountsdb:3306/accountsDB` ✅
- `jdbc:mysql://accountsdb:3307/accountsDB` ❌

### Health Check Dependencies

```yaml
depends_on:
  accountsdb:
    condition: service_healthy
```

**Đảm bảo:**
1. `accountsdb` khởi động trước
2. Health check pass
3. Sau đó `accounts` microservice khởi động

**Không có health checks:** Microservices có thể khởi động trước khi databases sẵn sàng, gây lỗi kết nối.

### Kế Thừa Cấu Hình với Extends

```yaml
extends:
  file: common-config.yml
  service: microservice-db-config
```

**Lợi ích:**
- DRY (Don't Repeat Yourself)
- Cấu hình nhất quán
- Single source of truth
- Bảo trì dễ dàng

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ:
1. Xác thực cấu hình Docker Compose
2. Khởi động tất cả services với `docker-compose up`
3. Kiểm tra giao tiếp giữa microservices và databases
4. Xác minh tính bền vững dữ liệu
5. Khắc phục sự cố nếu có

## Best Practices

✅ **Sử dụng service names cho giao tiếp container**  
✅ **Triển khai health checks cho tất cả services**  
✅ **Sử dụng environment variables cho cấu hình**  
✅ **Giữ cấu hình chung trong shared files**  
✅ **Tag images với số version**  
✅ **Dọn dẹp Docker resources không dùng thường xuyên**  
✅ **Push images lên Docker Hub để lưu trữ tập trung**  

❌ **Không sử dụng localhost trong containerized applications**  
❌ **Không hardcode cấu hình trong môi trường container**  
❌ **Không khởi động services mà không quản lý dependencies**  
❌ **Không duplicate cấu hình trên các files**  

---

**Tiếp Theo:** Chạy và xác thực toàn bộ Docker Compose setup với tất cả microservices và databases hoạt động cùng nhau.



================================================================================
FILE: 30-spring-cloud-gateway-internal-architecture.md
================================================================================

# Kiến Trúc Nội Bộ của Spring Cloud Gateway

## Tổng Quan

Tài liệu này giải thích kiến trúc nội bộ của Spring Cloud Gateway và cách nó xử lý các request trong môi trường microservices. Spring Cloud Gateway hoạt động như một edge server quản lý routing, filtering và bảo mật cho các ứng dụng microservice.

## Kiến Trúc Luồng Request

### 1. Điểm Nhận Request từ Client

Các client bên ngoài gửi request đến gateway server, bao gồm:
- Ứng dụng di động
- Ứng dụng web
- Các REST API khác

### 2. Gateway Handler Mapping

**Gateway Handler Mapping** là thành phần quan trọng đầu tiên:
- Xác định path được gọi bởi ứng dụng client
- Quyết định microservice nào sẽ nhận request
- Sử dụng cấu hình routing do developer định nghĩa (không dựa trên AI)

Developer phải cấu hình các quy tắc routing chỉ định:
- Mẫu đường dẫn request
- Đích đến là microservice nào

### 3. Predicates (Điều Kiện)

**Predicates** là các thành phần logic boolean thực thi trước khi chuyển tiếp request:
- Định nghĩa các điều kiện phải đáp ứng để chuyển tiếp request
- Trả về true hoặc false dựa trên đánh giá
- Từ chối các request không đáp ứng điều kiện đã định nghĩa
- Tương tự như functional interface predicate trong Java 8

Nếu predicates thất bại, gateway sẽ từ chối request với thông báo lỗi phù hợp.

### 4. Pre-Filters (Bộ Lọc Trước)

**Pre-Filters** thực thi logic nghiệp vụ trước khi chuyển tiếp request đến microservices:
- Xác thực request
- Auditing và logging
- Sửa đổi request
- Kiểm tra bảo mật
- Bất kỳ yêu cầu cross-cutting hoặc yêu cầu phi chức năng nào

Có thể cấu hình nhiều pre-filters dựa trên yêu cầu.

### 5. Xử Lý Microservice

Sau khi đánh giá predicate thành công và thực thi pre-filter:
- Request được chuyển tiếp đến microservice đích (loans, cards, accounts, v.v.)
- Microservice xử lý request
- Response được tạo ra

### 6. Post-Filters (Bộ Lọc Sau)

**Post-Filters** tác động lên response trước khi gửi cho client:
- Sửa đổi response
- Xác thực response
- Logging hoặc auditing bổ sung
- Thu thập số liệu hiệu suất

### 7. Gửi Response

Sau khi thực thi post-filter:
- Response quay về Gateway Handler Mapping
- Gateway Handler Mapping gửi response cho ứng dụng client

## Filters và Predicates Được Định Nghĩa Sẵn

Spring Cloud Gateway cung cấp nhiều filters và predicates tích hợp sẵn cho các tình huống phổ biến.

### Route Predicate Factories

Cấu hình routes dựa trên các tham số khác nhau:
- **Dựa trên Header**: Route dựa trên HTTP headers
- **Dựa trên Cookie**: Route dựa trên giá trị cookie
- **Dựa trên Host**: Route dựa trên mẫu host
- **Dựa trên Method**: Route dựa trên HTTP methods (GET, POST, v.v.)
- **Dựa trên Path**: Route dựa trên đường dẫn URL
- **Dựa trên Query**: Route dựa trên query parameters
- **Dựa trên Remote Address**: Route dựa trên địa chỉ IP client
- **Dựa trên Weight**: Phân phối traffic theo trọng số

### Gateway Filter Factories

Các filters được xây dựng sẵn cho các thao tác phổ biến:
- **AddRequestHeader**: Thêm headers vào requests
- **AddRequestParameter**: Thêm query parameters vào requests
- **AddResponseHeader**: Thêm headers vào responses
- **CircuitBreaker**: Triển khai mẫu circuit breaker
- **CacheRequestBody**: Cache request body để xử lý
- **FallbackHeaders**: Thêm fallback headers
- **JsonToGrpc**: Chuyển đổi JSON requests sang gRPC
- **ModifyRequestBody**: Sửa đổi nội dung request body
- **ModifyResponseBody**: Sửa đổi nội dung response body
- **Retry**: Triển khai logic retry
- **TokenRelay**: Chuyển tiếp security tokens

### Global Filters

Các filters bổ sung có sẵn toàn cục:
- **Gateway Metrics**: Thu thập metrics và dữ liệu monitoring
- **TLS/SSL Handlers**: Thực hiện các thao tác TLS handshake

## Cấu Hình và Triển Khai

Các bài giảng tiếp theo sẽ đề cập:
- Tạo gateway server với Spring Cloud Gateway
- Cấu hình quy tắc routing
- Định nghĩa predicates tùy chỉnh
- Tạo pre-filters và post-filters
- Sử dụng predefined filters hiệu quả

## Tài Nguyên Bổ Sung

Để biết thông tin chi tiết và các tình huống nâng cao, tham khảo [Tài Liệu Chính Thức Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway).

## Tóm Tắt

Spring Cloud Gateway cung cấp giải pháp toàn diện cho:
- Routing tập trung trong kiến trúc microservices
- Filtering request và response
- Xử lý request có điều kiện
- Bảo mật và các vấn đề cross-cutting
- Cấu hình dễ dàng với các thành phần định nghĩa sẵn

Kiến trúc đảm bảo tất cả các request đi qua một pipeline được kiểm soát, cho phép xử lý nhất quán các vấn đề chung trên tất cả các microservices.



================================================================================
FILE: 31-setting-up-spring-cloud-gateway-server.md
================================================================================

# Thiết Lập Spring Cloud Gateway Server

## Tổng Quan

Hướng dẫn này trình bày quy trình từng bước để tạo API Gateway (Edge Server) sử dụng Spring Cloud Gateway cho kiến trúc microservices. Gateway server đóng vai trò là điểm truy cập duy nhất cho tất cả các yêu cầu từ client và định tuyến chúng đến các microservices phù hợp.

## Yêu Cầu Tiên Quyết

- Java 17
- Spring Boot 3.1.2 (hoặc phiên bản ổn định mới nhất)
- Maven
- IntelliJ IDEA
- Các microservices đã có (accounts, loans, cards)
- Eureka Server (Service Discovery)
- Config Server

## Thiết Lập Dự Án

### 1. Tạo Spring Boot Project

Truy cập [start.spring.io](https://start.spring.io) và cấu hình dự án với các thiết lập sau:

- **Loại Dự Án**: Maven Project
- **Ngôn Ngữ**: Java
- **Phiên Bản Spring Boot**: 3.1.2 (hoặc phiên bản ổn định mới nhất)
- **Group**: com.easybytes
- **Artifact**: gateway-server
- **Name**: gateway-server
- **Description**: Easy Bank Gateway Server Application
- **Package Name**: com.easybytes.gateway
- **Packaging**: Jar
- **Phiên Bản Java**: 17

### 2. Thêm Các Dependencies Cần Thiết

Chọn các dependencies sau:

1. **Gateway** - Spring Cloud Gateway để xây dựng API gateway
2. **Eureka Discovery Client** - Để kết nối với Eureka server và lấy service registry
3. **Config Client** - Để tải cấu hình từ Config Server trong quá trình khởi động
4. **Actuator** - Để hiển thị các endpoints quản lý và giám sát
5. **DevTools** - Để phát triển nhanh hơn với khởi động lại tự động

### 3. Thiết Lập Cấu Trúc Dự Án

Sau khi tạo và tải xuống dự án:

1. Tạo thư mục `section9` trong workspace của bạn
2. Giải nén dự án gateway-server đã tải xuống vào thư mục `section9`
3. Xóa bất kỳ thư mục `.idea` nào từ các dự án đã sao chép
4. Mở thư mục `section9` trong IntelliJ IDEA

## Cấu Hình

### 1. Cập Nhật pom.xml

Thêm Google Jib plugin để tạo Docker image:

```xml
<plugin>
    <groupId>com.google.cloud.tools</groupId>
    <artifactId>jib-maven-plugin</artifactId>
    <configuration>
        <to>
            <image>easybytes/${project.artifactId}:s9</image>
        </to>
    </configuration>
</plugin>
```

**Lưu ý**: Cập nhật tên tag từ `s8` sang `s9` trong tất cả các microservices khác (accounts, cards, loans, config-server, eureka-server).

### 2. Cấu Hình application.yml

Đổi tên `application.properties` thành `application.yml` và thêm cấu hình sau:

```yaml
spring:
  application:
    name: gateway-server
  config:
    import: optional:configserver:http://localhost:8071
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true

management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    gateway:
      enabled: true
  info:
    env:
      enabled: true

info:
  app:
    name: gateway-server
    description: Easy Bank Gateway Server Application
```

### 3. Cấu Hình Properties Gateway Server trong Config Server

Tạo file `gateway-server.yml` trong GitHub configuration repository của bạn:

```yaml
server:
  port: 8072

eureka:
  instance:
    preferIpAddress: true
  client:
    fetchRegistry: true
    registerWithEureka: true
    serviceUrl:
      defaultZone: http://localhost:8070/eureka/
```

## Giải Thích Các Cấu Hình Chính

### Spring Cloud Gateway Discovery Locator

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
```

Cấu hình này yêu cầu gateway:
- Kết nối với Eureka discovery server
- Tự động tìm kiếm tất cả các microservices đã đăng ký
- Sử dụng thông tin này để định tuyến các yêu cầu đến các services phù hợp

### Actuator Gateway Endpoint

```yaml
management:
  endpoint:
    gateway:
      enabled: true
```

Kích hoạt các actuator endpoints cụ thể cho gateway để giám sát và quản lý.

### Cấu Hình Eureka Client

Gateway server tự đăng ký với Eureka và lấy service registry để biết các endpoints thực tế của tất cả microservices.

## Cách Hoạt Động

1. **Đăng Ký Service**: Tất cả microservices (accounts, loans, cards) đăng ký với Eureka Server
2. **Gateway Discovery**: Gateway Server kết nối với Eureka và lấy tất cả đăng ký services
3. **Định Tuyến Yêu Cầu**: Các client bên ngoài gửi yêu cầu đến Gateway Server
4. **Chuyển Tiếp Tự Động**: Gateway tự động định tuyến yêu cầu đến microservices phù hợp dựa trên tên service
5. **Cập Nhật Động**: Gateway luôn đồng bộ với Eureka về bất kỳ thay đổi nào trong các service instances

## Lợi Ích Của Dự Án

- **Điểm Truy Cập Duy Nhất**: Clients chỉ cần biết địa chỉ gateway
- **Tích Hợp Service Discovery**: Định tuyến tự động dựa trên Eureka service registry
- **Cấu Hình Tập Trung**: Tất cả cài đặt gateway được quản lý qua Config Server
- **Giám Sát**: Các actuator endpoints tích hợp sẵn cho health checks và metrics
- **Sẵn Sàng Docker**: Jib plugin được cấu hình để containerization dễ dàng

## Các Bước Tiếp Theo

1. Khởi động tất cả microservices (accounts, loans, cards)
2. Khởi động Config Server trên cổng 8071
3. Khởi động Eureka Server trên cổng 8070
4. Khởi động Gateway Server trên cổng 8072
5. Test microservices bằng cách gửi yêu cầu qua gateway thay vì trực tiếp đến microservices

## Tổng Kết Cấu Hình Cổng

- **Config Server**: 8071
- **Eureka Server**: 8070
- **Gateway Server**: 8072
- **Accounts Service**: (như đã cấu hình)
- **Loans Service**: (như đã cấu hình)
- **Cards Service**: (như đã cấu hình)

## Lưu Ý Quan Trọng

- Đảm bảo tất cả microservices được cấu hình để đăng ký với Eureka
- Cấu hình gateway server được duy trì trong Config Server để quản lý tập trung
- Gateway sử dụng service discovery để định tuyến yêu cầu động mà không cần URLs cố định
- Luôn cập nhật Docker image tags nhất quán trên tất cả services để quản lý phiên bản đúng cách

## Kiểm Thử

Sau khi gateway đang chạy, bạn có thể truy cập microservices thông qua:

```
http://localhost:8072/{service-name}/{endpoint}
```

Ví dụ:
- `http://localhost:8072/accounts/api/fetch`
- `http://localhost:8072/loans/api/fetch`
- `http://localhost:8072/cards/api/fetch`

Gateway sẽ tự động phát hiện và định tuyến đến các service instances phù hợp đã đăng ký trong Eureka.

## Kết Luận

Spring Cloud Gateway cung cấp một giải pháp mạnh mẽ và linh hoạt để xây dựng API Gateway cho kiến trúc microservices. Với sự tích hợp chặt chẽ với Eureka Service Discovery và Spring Cloud Config, nó cho phép định tuyến động, cấu hình tập trung và quản lý dễ dàng của tất cả các microservices trong hệ thống.



================================================================================
FILE: 32-testing-spring-cloud-gateway-server-in-action.md
================================================================================

# Kiểm Thử Spring Cloud Gateway Server Trong Thực Tế

## Tổng Quan
Hướng dẫn này trình bày cách kiểm thử và xác thực Spring Cloud Gateway Server trong kiến trúc microservices sử dụng Spring Boot, Eureka Service Discovery và Spring Cloud Gateway.

## Yêu Cầu Tiên Quyết

Trước khi khởi động Gateway Server, đảm bảo các dịch vụ sau đang chạy theo đúng thứ tự:

1. **Config Server** - Phải khởi động trước tiên
2. **Eureka Server** - Khởi động sau Config Server
3. **Microservices** (Accounts, Cards, Loans) - Khởi động theo thứ tự bất kỳ sau Eureka Server
4. **Gateway Server** - Phải khởi động cuối cùng (Cổng: 8072)

### Tại Sao Phải Khởi Động Gateway Server Cuối Cùng?

Gateway Server cần:
- Kết nối với Eureka Server
- Lấy thông tin chi tiết về tất cả microservices đã đăng ký
- Xử lý định tuyến traffic cho các microservices nội bộ

Nếu khởi động trước các microservices khác, Eureka Server sẽ không có thông tin về các microservices để chia sẻ với Gateway.

## Xác Minh Cài Đặt

### 1. Kiểm Tra Eureka Dashboard

Truy cập Eureka Dashboard để xác minh tất cả dịch vụ đã được đăng ký:
- Microservice Accounts
- Microservice Cards
- Microservice Loans
- Gateway Server

Nhấp vào bất kỳ liên kết dịch vụ nào để xem thông tin được cấu hình trong file `application.yml`.

### 2. Kiểm Tra Gateway Actuator Endpoints

Truy cập Gateway Server actuator tại:
```
http://localhost:8072/actuator
```

**Mẹo:** Cài đặt plugin Chrome "JSON View" để hiển thị JSON được định dạng tốt hơn.

#### Xem Gateway Routes

Truy cập endpoint routes:
```
http://localhost:8072/actuator/gateway/routes
```

Endpoint này hiển thị thông tin định tuyến cho từng microservice.

## Hiểu Cấu Hình Định Tuyến Gateway

### Cấu Trúc Route

Mỗi route microservice chứa:

1. **Predicate**: Khớp các request đến dựa trên đường dẫn
2. **URI**: Đích đến với tiền tố load balancer (`lb://`)
3. **Filters**: Quy tắc viết lại và chuyển đổi đường dẫn

### Ví Dụ: Route Microservice Loans

Khi một request được gửi đến Gateway Server với đường dẫn `/loans`:

- **Port**: Chuyển tiếp đến cổng 8090 (cổng của loans microservice)
- **Load Balancer**: Sử dụng định dạng `lb://LOANS`
  - `lb` = load balancer (cân bằng tải)
  - `LOANS` = tên ứng dụng trong Eureka Server
- **Service Discovery**: Tận dụng Eureka để tìm các instances
- **Load Balancing**: Sử dụng chiến lược Spring Cloud Load Balancer

### Path Rewriting Filter

Filter **RewritePath**:
- Loại bỏ tiền tố (ví dụ: `/loans`) khỏi đường dẫn đến
- Chỉ chuyển tiếp phần đường dẫn còn lại đến microservice đích
- Ví dụ: `/loans/api/create` trở thành `/api/create` khi được chuyển tiếp

Cấu hình này áp dụng tương tự cho microservices **Accounts** và **Cards**.

### Gateway Server Self-Routing

Gateway Server cũng có thể định tuyến request đến chính nó:
- Yêu cầu tiền tố đường dẫn `gatewayserver`
- Sử dụng cổng 8072
- Đăng ký trong Eureka với tên "Gateway Server"

## Kiểm Thử Với Postman

### Test 1: Tạo Tài Khoản Qua Gateway

**Cấu Hình Request:**
```
POST http://localhost:8072/ACCOUNTS/api/create
```

**Các Điểm Chính:**
- Cổng `8072`: Cổng của Gateway Server
- `ACCOUNTS`: Tên logic đăng ký trong Eureka (sử dụng CHỮ HOA)
- `/api/create`: Đường dẫn endpoint thực tế trong accounts microservice

**Request Body:**
```json
{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "mobileNumber": "0123456789"
}
```

**Luồng Xử Lý:**
1. Request được gửi đến Gateway Server
2. Gateway khớp cấu hình định tuyến cho đường dẫn `/ACCOUNTS`
3. Loại bỏ tiền tố `/ACCOUNTS`
4. Chuyển tiếp đường dẫn còn lại (`/api/create`) đến accounts microservice
5. Sử dụng Eureka cho service discovery với load balancer

**Kết Quả:** Phản hồi tạo tài khoản thành công

### Test 2: Lấy Thông Tin Tài Khoản

**Cấu Hình Request:**
```
GET http://localhost:8072/ACCOUNTS/api/fetch?mobileNumber=0123456789
```

**Các Điểm Chính:**
- Logic định tuyến giống như Test 1
- Tham số query được truyền qua accounts microservice
- Số điện thoại phải khớp với tài khoản đã đăng ký

**Kết Quả:** Chi tiết tài khoản được trả về thành công

### Test 3: Truy Cập Loans Microservice

**Cấu Hình Request:**
```
GET http://localhost:8072/LOANS/api/fetch?mobileNumber=0123456789
```

Các client bên ngoài gửi request với tiền tố đường dẫn `/loans` để truy cập loans microservice thông qua Gateway.

**Lưu Ý:** Nếu không tồn tại khoản vay nào cho số điện thoại, bạn sẽ nhận được lỗi "not found".

## Lợi Ích Của Việc Sử Dụng Gateway Server

### Mô Hình Edge Server

- Tất cả traffic bên ngoài đi qua Gateway Server
- Các microservices nội bộ không được expose trực tiếp cho client bên ngoài
- Gateway hoạt động như một điểm vào duy nhất (edge server)

### Các Cân Nhắc Về Bảo Mật

**Cài Đặt Hiện Tại:**
- Client vẫn có thể gọi trực tiếp microservices nếu biết URLs
- Truy cập trực tiếp về mặt kỹ thuật vẫn khả thi với cấu hình hiện tại

**Cải Tiến Tương Lai:**
- Các chính sách bảo mật sẽ được áp dụng trong các phần tiếp theo
- Client sẽ được yêu cầu chỉ truy cập microservices thông qua Gateway
- Việc gọi trực tiếp microservice sẽ bị chặn

## Tóm Tắt

Với cài đặt Spring Cloud Gateway Server này, bạn đã thành công:

✅ Cấu hình một edge server cho mạng microservices của bạn  
✅ Triển khai service discovery với Eureka  
✅ Thiết lập cân bằng tải tự động với Spring Cloud Load Balancer  
✅ Cấu hình các quy tắc viết lại đường dẫn và định tuyến  
✅ Tạo một điểm vào duy nhất cho các request từ client bên ngoài  

Gateway Server có thể được tối ưu hóa và bảo mật thêm trong các triển khai tiếp theo.

## Các Bước Tiếp Theo

- Triển khai bảo mật và xác thực
- Thêm rate limiting và circuit breakers
- Cấu hình custom filters cho logging và monitoring
- Tối ưu hóa hiệu suất Gateway Server

---

**Lưu Ý:** Đảm bảo tất cả tên dịch vụ trong Eureka đều ở dạng CHỮ HOA theo mặc định để cấu hình định tuyến hoạt động đúng.



================================================================================
FILE: 33-cau-hinh-spring-cloud-gateway-ten-dich-vu-chu-thuong.md
================================================================================

# Cấu Hình Spring Cloud Gateway Cho Tên Dịch Vụ Chữ Thường

## Tổng Quan

Theo mặc định, Spring Cloud Gateway yêu cầu tên các microservice phải được chỉ định bằng chữ in hoa khi định tuyến các yêu cầu. Tài liệu này giải thích cách cấu hình Gateway server để chấp nhận tên dịch vụ viết thường, giúp cung cấp cấu trúc API chuyên nghiệp và thân thiện với người dùng hơn.

## Thách Thức Với Hành Vi Mặc Định

Khi sử dụng Spring Cloud Gateway với service discovery, cấu hình mặc định yêu cầu tên dịch vụ phải viết hoàn toàn bằng chữ in hoa:

```
http://gateway-server/ACCOUNTS/api/...
http://gateway-server/LOANS/api/...
http://gateway-server/CARDS/api/...
```

Nếu bạn cố gắng sử dụng tên dịch vụ viết thường mà không có cấu hình phù hợp, Gateway server sẽ trả về lỗi **404 Not Found**:

```
http://gateway-server/accounts/api/...  ❌ Trả về lỗi 404
```

Hành vi này không lý tưởng vì:
- Sử dụng chữ in hoa hoàn toàn trong đường dẫn URL là không phổ biến
- Tạo trải nghiệm kém cho người tiêu dùng API
- Không tuân theo các thực hành tốt nhất của REST API

## Giải Pháp: Kích Hoạt Lowercase Service ID

Để cho phép tên dịch vụ viết thường trong định tuyến Gateway, thêm cấu hình sau vào file `application.yml` của Gateway server:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lowercase-service-id: true
```

### Giải Thích Cấu Hình

- **`spring.cloud.gateway.discovery.locator.enabled`**: Kích hoạt tự động tạo route dựa trên các dịch vụ đã đăng ký với discovery server
- **`spring.cloud.gateway.discovery.locator.lowercase-service-id`**: Cấu hình Gateway để chấp nhận tên dịch vụ ở định dạng chữ thường

## Các Bước Triển Khai

1. **Mở Cấu Hình Gateway Server**
   - Điều hướng đến dự án Spring Cloud Gateway của bạn trong IntelliJ IDEA
   - Mở file `application.yml`

2. **Thêm Thuộc Tính Cấu Hình**
   - Tìm section `spring.cloud.gateway.discovery.locator`
   - Thêm thuộc tính `lowercase-service-id: true` cùng cấp với `enabled`

3. **Build Lại Ứng Dụng**
   - Thực hiện clean build Gateway server
   - Đợi quá trình build hoàn tất thành công

4. **Khởi Động Lại Gateway Server**
   - Dừng instance Gateway server đang chạy
   - Khởi động Gateway server với cấu hình mới

## Kiểm Tra Cấu Hình

### Trước Khi Cấu Hình
```
GET http://gateway-server/ACCOUNTS/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/accounts/api/fetch?mobileNumber=1234567890
❌ Lỗi (404 Not Found)
```

### Sau Khi Cấu Hình
```
GET http://gateway-server/accounts/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/loans/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)

GET http://gateway-server/cards/api/fetch?mobileNumber=1234567890
✅ Thành công (200 OK)
```

## Lợi Ích

1. **Thiết Kế API Chuyên Nghiệp**: URL viết thường tuân theo tiêu chuẩn ngành và quy ước REST API
2. **Trải Nghiệm Lập Trình Viên Tốt Hơn**: Người tiêu dùng API không cần phải nhớ quy ước viết hoa
3. **Tính Nhất Quán**: Phù hợp với các mẫu URL phổ biến được sử dụng trong các ứng dụng web hiện đại
4. **Tính Linh Hoạt**: Hỗ trợ cả tên dịch vụ viết hoa và viết thường (mặc dù khuyến nghị viết thường)

## Thực Hành Tốt Nhất

- Luôn sử dụng tên dịch vụ viết thường trong môi trường production
- Tài liệu hóa các mẫu URL một cách rõ ràng cho người tiêu dùng API
- Kiểm tra cả các thao tác fetch và create/update sau khi triển khai thay đổi này
- Đảm bảo tất cả các ứng dụng client được cập nhật để sử dụng tên dịch vụ viết thường

## Kết Luận

Việc kích hoạt lowercase service ID trong Spring Cloud Gateway là một thay đổi cấu hình đơn giản nhưng cải thiện đáng kể khả năng sử dụng và tính chuyên nghiệp của kiến trúc microservices của bạn. Thay đổi cấu hình một dòng này đảm bảo các API endpoint của bạn tuân theo các thực hành tốt nhất của ngành và cung cấp trải nghiệm tốt hơn cho các developer sử dụng dịch vụ của bạn.



================================================================================
FILE: 34-configuring-custom-routing-with-spring-cloud-gateway.md
================================================================================

# Cấu Hình Routing Tùy Chỉnh với Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này giải thích cách cấu hình routing tùy chỉnh trong Spring Cloud Gateway để xử lý các yêu cầu định tuyến động vượt ra ngoài hành vi mặc định. Chúng ta sẽ triển khai mô hình routing chuyên nghiệp sử dụng tiền tố tổ chức cho các endpoint microservice.

## Hành Vi Routing Mặc Định

Theo mặc định, Spring Cloud Gateway tự động tạo các route dựa trên tên service đã đăng ký với Eureka Server. Gateway lấy thông tin routing từ Eureka và chuyển tiếp request đến các microservice.

**Mô hình routing mặc định:**
- `/accounts/**` → ACCOUNTS microservice
- `/loans/**` → LOANS microservice
- `/cards/**` → CARDS microservice

Điều này hoạt động tốt, nhưng có thể không phù hợp với tất cả các yêu cầu dự án.

## Yêu Cầu Routing Tùy Chỉnh

Để có cấu trúc API chuyên nghiệp hơn, chúng ta có thể triển khai routing tùy chỉnh với tiền tố tổ chức:

**Mô hình routing tùy chỉnh:**
- `/easybank/accounts/**` → ACCOUNTS microservice
- `/easybank/loans/**` → LOANS microservice
- `/easybank/cards/**` → CARDS microservice

Mô hình này cung cấp ngữ cảnh tốt hơn cho các ứng dụng client, làm rõ tổ chức và microservice nào mà họ đang tương tác.

## Các Bước Triển Khai

### 1. Tạo Bean RouteLocator

Điều hướng đến class chính trong Gateway server (`GatewayServerApplication.java`) và tạo một phương thức cấu hình:

```java
@Bean
public RouteLocator easybankRouteConfig(RouteLocatorBuilder routeLocatorBuilder) {
    return routeLocatorBuilder.routes()
        .route(p -> p
            .path("/easybank/accounts/**")
            .filters(f -> f.rewritePath(
                "/easybank/accounts/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://ACCOUNTS"))
        .route(p -> p
            .path("/easybank/loans/**")
            .filters(f -> f.rewritePath(
                "/easybank/loans/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://LOANS"))
        .route(p -> p
            .path("/easybank/cards/**")
            .filters(f -> f.rewritePath(
                "/easybank/cards/(?<segment>.*)", 
                "/${segment}"))
            .uri("lb://CARDS"))
        .build();
}
```

### 2. Hiểu Về Cấu Hình

**Các thành phần chính:**

- **`@Bean`**: Đăng ký RouteLocator như một Spring bean
- **`RouteLocatorBuilder`**: Builder để tạo các cấu hình route
- **`.routes()`**: Bắt đầu chuỗi định nghĩa route
- **`.route()`**: Định nghĩa cấu hình route riêng lẻ
- **`.path()`**: Chỉ định mẫu đường dẫn request đến
- **`.filters()`**: Áp dụng các filter để chuyển đổi request
- **`.rewritePath()`**: Viết lại đường dẫn trước khi chuyển tiếp đến microservice
- **`.uri()`**: Chỉ định URI microservice đích

**Viết lại đường dẫn:**
- Mẫu `/easybank/accounts/(?<segment>.*)` bắt mọi thứ sau `/easybank/accounts/` như một biến có tên `segment`
- Thay thế `/${segment}` chỉ chuyển tiếp đường dẫn đã bắt đến microservice
- Ví dụ: `/easybank/accounts/api/create` → `/api/create`

**Cân bằng tải:**
- `lb://ACCOUNTS` chỉ định routing có cân bằng tải
- Sử dụng Spring Cloud LoadBalancer cho cân bằng tải phía client
- Tên service phải khớp với tên ứng dụng đã đăng ký trong Eureka (phân biệt chữ hoa/thường)

### 3. Vô Hiệu Hóa Routing Mặc Định

Để tránh nhầm lẫn với nhiều cấu hình routing, vô hiệu hóa hành vi mặc định trong `application.yml`:

```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: false  # Thay đổi từ true
```

Điều này đảm bảo chỉ các route tùy chỉnh của bạn được kích hoạt.

### 4. Build và Kiểm Tra

1. Lưu các thay đổi
2. Build dự án với Maven
3. Kiểm tra bằng Postman hoặc bất kỳ REST client nào

**Ví dụ request:**
```
POST http://localhost:8072/easybank/accounts/api/create
```

**Xác minh các route:**
```
GET http://localhost:8072/actuator/gateway/routes
```

Bạn sẽ chỉ thấy các route tùy chỉnh với tiền tố `easybank`.

## Các Kịch Bản Kiểm Tra

### Kiểm Tra Tích Cực
- Endpoint: `POST /easybank/accounts/api/create`
- Kỳ vọng: Response thành công từ ACCOUNTS microservice
- Request được định tuyến đúng và đường dẫn được viết lại

### Kiểm Tra Tiêu Cực
- Endpoint: `POST /accounts/api/create` (không có tiền tố)
- Kỳ vọng: 404 Not Found
- Routing mặc định đã bị vô hiệu hóa, nên đường dẫn này không còn hoạt động

## Những Điểm Quan Trọng Cần Lưu Ý

### Phân Biệt Chữ Hoa/Thường Của Tên Service
Luôn sử dụng tên ứng dụng chính xác như đã đăng ký trong Eureka:
- ✅ `lb://ACCOUNTS` (nếu đăng ký là ACCOUNTS)
- ❌ `lb://accounts` (sẽ thất bại nếu không khớp chữ hoa/thường)

### Định Dạng URI
Đảm bảo định dạng URI đúng với hai dấu gạch chéo:
- ✅ `uri("lb://ACCOUNTS")`
- ❌ `uri("lb:ACCOUNTS")` (thiếu dấu gạch chéo)

## Cấu Hình Thay Thế: Dựa Trên YAML

Spring Cloud Gateway cũng hỗ trợ cấu hình routing dựa trên YAML:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: accounts-route
          uri: lb://ACCOUNTS
          predicates:
            - Path=/easybank/accounts/**
          filters:
            - RewritePath=/easybank/accounts/(?<segment>.*), /$\{segment}
```

## Khuyến Nghị: Cấu Hình Java vs YAML

**Nên dùng cấu hình dựa trên Java** cho:
- Logic routing phức tạp
- Nhiều filter
- Cấu hình động
- Hỗ trợ IDE tốt hơn và type safety

**Hạn chế của cấu hình YAML:**
- Kém linh hoạt cho các tình huống phức tạp
- Khả năng chuỗi filter hạn chế
- Khó bảo trì hơn cho cấu hình lớn

## Kết Luận

Routing tùy chỉnh với Spring Cloud Gateway cung cấp cấu trúc API chuyên nghiệp và có tổ chức. Bằng cách sử dụng cấu hình dựa trên Java với `RouteLocator`, bạn có được sự linh hoạt và kiểm soát tối đa đối với logic routing của mình trong khi duy trì code sạch và dễ bảo trì.

Mô hình sử dụng tiền tố tổ chức (`/easybank/`) theo sau là tên service tạo ra một hệ thống phân cấp rõ ràng giúp cải thiện khả năng phát hiện API và trải nghiệm của developer.



================================================================================
FILE: 35-adding-multiple-filters-spring-cloud-gateway.md
================================================================================

# Thêm Nhiều Filter trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình nhiều filter trong Spring Cloud Gateway, bao gồm các filter có sẵn và chuẩn bị cho việc triển khai filter tùy chỉnh.

## Cấu Hình Gateway Hiện Tại

Hiện tại, Gateway server có các cấu hình routing bao gồm:
- **Path Predicate**: Xác thực xem đường dẫn request có khớp với giá trị predicate không
- **Rewrite Path Filter**: Viết lại đường dẫn trước khi chuyển tiếp đến microservice thực tế
- **Request Forwarding**: Định tuyến request đến microservice đích

## Hiểu về Cấu Hình Spring Cloud Gateway

### Cách Tiếp Cận Tài Liệu

Khi làm việc với Spring Cloud Gateway hoặc bất kỳ framework nào, hãy làm theo các bước sau:

1. **Đọc Tài Liệu Chính Thức**: Tài liệu đầy đủ chứa tất cả các chi tiết cần thiết
2. **Xem Xét Ví Dụ**: Các ví dụ chính thức minh họa các mẫu triển khai đúng
3. **Điều Chỉnh Theo Yêu Cầu**: Sửa đổi ví dụ dựa trên nhu cầu kinh doanh

### Các Phương Pháp Cấu Hình

#### 1. Fluent Java Routes API (Được Khuyến Nghị)

Sử dụng cấu hình dựa trên Java với annotation `@Bean` trả về `RouteLocator`:
- Cung cấp tính linh hoạt tối đa
- Cho phép triển khai các yêu cầu phức tạp
- Cho phép định nghĩa route theo cách lập trình

#### 2. Cấu Hình YAML

Định nghĩa routes sử dụng application properties:
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: route-id
          uri: target-uri
          predicates:
            - Path=/path/**
```

**Khuyến Nghị**: Ưu tiên cấu hình kiểu Java để có tính linh hoạt tốt hơn và xử lý các yêu cầu phức tạp.

## Thêm Response Header Filter

### Mục Tiêu

Thêm filter để bao gồm các header tùy chỉnh trong response gửi đến ứng dụng client.

### Các Bước Triển Khai

#### 1. Tìm Tài Liệu Filter

Từ tài liệu chính thức:
- Điều hướng đến **Gateway Filter Factories**
- Tìm **AddResponseHeader GatewayFilter Factory**

#### 2. Thêm Filter vào Cấu Hình Java

```java
.filter(f -> f.addResponseHeader("X-Response-Time", LocalDateTime.now().toString()))
```

### Chi Tiết Filter

**Tên Header**: `X-Response-Time`

**Mục Đích**:
- Cung cấp timestamp của thời điểm tạo response
- Giúp client tính toán thời gian khứ hồi request-response
- Hữu ích cho việc giám sát hiệu suất

**Giá Trị**: Ngày và giờ hiện tại sử dụng `LocalDateTime.now().toString()`

### Áp Dụng cho Tất Cả Microservices

Thêm cùng cấu hình filter cho:
- Route của Accounts microservice
- Route của Loans microservice
- Route của Cards microservice

## Kiểm Tra Triển Khai

### Sử Dụng Postman

1. Gửi request đến Gateway server
2. Kiểm tra response headers
3. Xác minh header `X-Response-Time` có mặt
4. Quan sát giá trị ngày và giờ hiện tại

### Trước và Sau

**Trước**: Ba header mặc định trong response

**Sau**: Thêm header tùy chỉnh `X-Response-Time` với timestamp

## Các Gateway Filter Có Sẵn

Spring Cloud Gateway cung cấp nhiều filter có sẵn:

- **Request Filters**:
  - AddRequestHeader
  - AddRequestParameter
  - ModifyRequestBody
  - MapRequestHeader

- **Response Filters**:
  - AddResponseHeader
  - ModifyResponseBody
  - LocalResponseCache

- **Path Filters**:
  - RewritePath
  - PrefixPath
  - StripPrefix

- **Advanced Filters**:
  - CircuitBreaker
  - FallbackHeaders
  - JsonToGrpc
  - Redirect

## Thực Hành Tốt Nhất

1. **Tận Dụng Filter Có Sẵn**: Sử dụng các filter được định nghĩa sẵn để đáp ứng yêu cầu kinh doanh
2. **Xem Xét Tài Liệu**: Khám phá các filter có sẵn trong tài liệu chính thức
3. **Thêm Nhiều Filter**: Chuỗi các filter sử dụng method chaining trong cấu hình Java
4. **Giám Sát Hiệu Suất**: Sử dụng response headers để theo dõi và debug

## Khi Filter Có Sẵn Không Đủ

Nếu không có filter được định nghĩa sẵn nào phù hợp với logic kinh doanh của bạn:
- Định nghĩa filter tùy chỉnh
- Triển khai logic filter tùy chỉnh
- Đăng ký filter tùy chỉnh trong cấu hình Gateway

## Các Bước Tiếp Theo

Chủ đề tiếp theo bao gồm việc tạo và triển khai filter tùy chỉnh trong Spring Cloud Gateway khi các filter có sẵn không đáp ứng các yêu cầu kinh doanh cụ thể.

## Tóm Tắt

- Spring Cloud Gateway hỗ trợ nhiều filter cho mỗi route
- Sử dụng filter `addResponseHeader` để bao gồm header tùy chỉnh
- Chuỗi nhiều filter sử dụng fluent API
- Filter có sẵn bao phủ hầu hết các trường hợp sử dụng phổ biến
- Filter tùy chỉnh có sẵn cho logic kinh doanh cụ thể

---

**Chủ Đề Liên Quan**:
- Triển Khai Filter Tùy Chỉnh
- Gateway Filter Factories
- Cấu Hình Routing
- Giám Sát Hiệu Suất



================================================================================
FILE: 36-tao-custom-filters-spring-cloud-gateway.md
================================================================================

# Tạo Custom Filters trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách tạo các custom filter trong Spring Cloud Gateway để triển khai tính năng truy vết request sử dụng correlation ID xuyên suốt các microservices.

## Kịch Bản Nghiệp Vụ

Khi Gateway server nhận các request từ bên ngoài, chúng ta muốn:
1. Tạo một correlation ID duy nhất cho mỗi request
2. Truyền cùng một correlation ID đến tất cả các microservices phía sau (accounts, loans, cards, v.v.)
3. Thêm các câu lệnh logger trong microservices sử dụng correlation ID
4. Bao gồm correlation ID trong response header để client có thể khắc phục sự cố

Cách tiếp cận này cho phép các developer truy vết request qua nhiều microservices và nhanh chóng xác định vị trí xảy ra vấn đề.

## Các Bước Triển Khai

### 1. Tạo Package Filter

Tạo cấu trúc package mới:
```
com.eazybytes.gatewayserver.filters
```

### 2. Tạo Ba Class Filter

#### RequestTraceFilter
Chịu trách nhiệm tạo và thiết lập correlation ID khi một request mới đến Gateway server.

**Tính Năng Chính:**
- Sử dụng annotation `@Component` để đăng ký làm Spring bean
- Sử dụng `@Order(1)` để đảm bảo thứ tự ưu tiên thực thi
- Implement interface `GlobalFilter` để xử lý tất cả traffic đến
- Tạo correlation ID sử dụng `UUID.randomUUID()`
- Kiểm tra xem correlation ID đã tồn tại chưa (tránh ghi đè trong trường hợp redirect)

**Cấu Trúc Code:**
```java
@Component
@Order(1)
public class RequestTraceFilter implements GlobalFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        HttpHeaders requestHeaders = exchange.getRequest().getHeaders();
        
        if (isCorrelationIdPresent(requestHeaders)) {
            logger.debug("eazybank-correlation-id found in RequestTraceFilter");
        } else {
            String correlationId = generateCorrelationId();
            exchange = setCorrelationId(exchange, correlationId);
            logger.debug("eazybank-correlation-id generated in RequestTraceFilter");
        }
        
        return chain.filter(exchange);
    }
}
```

#### ResponseTraceFilter
Thêm correlation ID vào response headers trước khi gửi lại cho client.

**Tính Năng Chính:**
- Sử dụng annotation `@Configuration`
- Tạo bean `GlobalFilter` thông qua cấu hình method
- Hoạt động như một post-filter sử dụng method `.then()`
- Trích xuất correlation ID từ request headers
- Thêm correlation ID vào response headers

**Cấu Trúc Code:**
```java
@Configuration
public class ResponseTraceFilter {
    
    @Bean
    public GlobalFilter postGlobalFilter() {
        return (exchange, chain) -> {
            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                String correlationId = getCorrelationId(exchange.getRequest().getHeaders());
                exchange.getResponse().getHeaders().add(CORRELATION_ID, correlationId);
                logger.debug("Updated the correlation id to the outbound headers");
            }));
        };
    }
}
```

#### FilterUtility
Chứa các phương thức tiện ích chung được chia sẻ giữa request và response filters.

**Các Phương Thức:**
- `getCorrelationId()` - Lấy correlation ID từ request headers
- `setCorrelationId()` - Thiết lập correlation ID trong request headers
- `isCorrelationIdPresent()` - Kiểm tra xem correlation ID có tồn tại không

**Tên Header:**
```
eazybank-correlation-id
```

### 3. Hiểu Về Kiến Trúc Spring Cloud Gateway

**Lưu Ý Quan Trọng:**
- Spring Cloud Gateway được xây dựng trên **Spring Reactive** (không phải Servlet API truyền thống)
- Sử dụng `ServerWebExchange` thay vì HttpServletRequest/Response
- Sử dụng `Mono` và `Flux` cho lập trình reactive
  - `Mono<Void>` - Đại diện cho một response trống duy nhất
  - `Mono` - Đối tượng đơn
  - `Flux` - Tập hợp các đối tượng

### 4. Thực Thi Filter Chain

Các filter trong Gateway thực thi theo chuỗi:
1. Custom filters thực thi theo thứ tự (sử dụng annotation `@Order`)
2. Mỗi filter phải gọi `chain.filter(exchange)` để tiếp tục đến filter tiếp theo
3. Post-filters sử dụng method `.then()` để thực thi sau khi nhận được response

### 5. Kích Hoạt Debug Logging

Thêm cấu hình vào `application.yml`:

```yaml
logging:
  level:
    com.easybytes.gatewayserver: DEBUG
```

Cấu hình này kích hoạt tất cả các câu lệnh logger debug trong package gateway server.

## Các Bước Tiếp Theo

Sau khi triển khai Gateway filters, bạn cần:
1. Cập nhật các microservices riêng lẻ để chấp nhận correlation ID header
2. Đọc giá trị correlation ID trong microservices
3. Thêm các câu lệnh logger trong business logic sử dụng correlation ID

## Luồng Correlation ID

```
Request Bên Ngoài → Gateway Server (Tạo Correlation ID)
                        ↓
                Thêm vào Request Header
                        ↓
            Chuyển tiếp đến Microservice (Accounts)
                        ↓
        Chuyển tiếp đến Microservice (Loans/Cards)
                        ↓
                  Xử Lý Request
                        ↓
            Trả Response về Gateway
                        ↓
        Thêm Correlation ID vào Response Header
                        ↓
            Trả về Client Bên Ngoài
```

## Lợi Ích

1. **Truy Vết Request** - Theo dõi requests qua nhiều microservices
2. **Gỡ Lỗi** - Nhanh chóng xác định nơi xảy ra vấn đề sử dụng correlation ID
3. **Phân Tích Log** - Tìm kiếm logs xuyên suốt các services sử dụng một correlation ID duy nhất
4. **Hỗ Trợ Client** - Client có thể cung cấp correlation ID để khắc phục sự cố

## Điểm Chính Cần Nhớ

- Sử dụng `GlobalFilter` cho các filter áp dụng cho tất cả traffic
- Sử dụng `@Order` để kiểm soát thứ tự thực thi filter
- Spring Cloud Gateway sử dụng mô hình lập trình reactive
- Correlation IDs cho phép distributed tracing
- Cả request và response đều có thể mang correlation ID
- Ngăn chặn việc tạo correlation ID trùng lặp trong quá trình redirections



================================================================================
FILE: 37-trien-khai-correlation-id-trong-microservices.md
================================================================================

# Triển Khai Correlation ID trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai xử lý correlation ID trong các microservices riêng lẻ (Accounts, Loans, Cards) để nhận và xử lý correlation ID được gửi bởi Spring Cloud Gateway server.

## Luồng Kiến Trúc

```
Gateway Server (Port 8072)
    ↓ (chuyển tiếp correlation ID)
Accounts Microservice
    ↓ (chuyển tiếp correlation ID qua Feign)
Loans & Cards Microservices
```

## Triển Khai trong Accounts Microservice

### 1. Cập Nhật CustomerController

`CustomerController` chứa API `fetchCustomerDetails` giao tiếp với nhiều microservices.

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetchCustomerDetails")
public ResponseEntity<CustomerDetailsDto> fetchCustomerDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    // Business logic
}
```

### 2. Thêm Logger vào CustomerController

**Tạo Biến Logger:**

```java
public class CustomerController {
    
    private static final Logger logger = LoggerFactory.getLogger(CustomerController.class);
    
    // ... existing code ...
}
```

**Thêm Câu Lệnh Logger:**

```java
logger.debug("eazybank-correlation-id found: {}", correlationId);
```

### 3. Cập Nhật Service Layer

**Chỉnh Sửa Interface ICustomerService:**

```java
public interface ICustomerService {
    CustomerDetailsDto fetchCustomerDetails(String correlationId, String mobileNumber);
}
```

**Cập Nhật CustomerServiceImpl:**

```java
@Override
public CustomerDetailsDto fetchCustomerDetails(String correlationId, String mobileNumber) {
    // Truyền correlationId cho Feign clients
    LoansDto loansDto = loansFeignClient.fetchLoanDetails(correlationId, mobileNumber);
    CardsDto cardsDto = cardsFeignClient.fetchCardDetails(correlationId, mobileNumber);
    
    // ... existing code ...
}
```

### 4. Cập Nhật Feign Clients

**Interface LoansFeignClient:**

```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    
    @GetMapping("/api/fetch")
    public ResponseEntity<LoansDto> fetchLoanDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber);
}
```

**Interface CardsFeignClient:**

```java
@FeignClient(name = "cards")
public interface CardsFeignClient {
    
    @GetMapping("/api/fetch")
    public ResponseEntity<CardsDto> fetchCardDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber);
}
```

## Triển Khai trong Loans Microservice

### 1. Cập Nhật LoansController

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetch")
public ResponseEntity<LoansDto> fetchLoanDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    logger.debug("eazybank-correlation-id found: {}", correlationId);
    
    // ... existing code ...
}
```

### 2. Thêm Biến Logger

```java
public class LoansController {
    
    private static final Logger logger = LoggerFactory.getLogger(LoansController.class);
    
    // ... existing code ...
}
```

## Triển Khai trong Cards Microservice

### 1. Cập Nhật CardsController

**Thêm Tham Số Request Header:**

```java
@GetMapping("/fetch")
public ResponseEntity<CardsDto> fetchCardDetails(
    @RequestHeader("eazybank-correlation-id") String correlationId,
    @RequestParam String mobileNumber) {
    
    logger.debug("eazybank-correlation-id found: {}", correlationId);
    
    // ... existing code ...
}
```

### 2. Thêm Biến Logger

```java
public class CardsController {
    
    private static final Logger logger = LoggerFactory.getLogger(CardsController.class);
    
    // ... existing code ...
}
```

## Kích Hoạt Debug Logging

Thêm cấu hình sau vào `application.yml` cho mỗi microservice:

### Accounts Microservice

```yaml
logging:
  level:
    com.eazybytes.accounts: DEBUG
```

### Loans Microservice

```yaml
logging:
  level:
    com.eazybytes.loans: DEBUG
```

### Cards Microservice

```yaml
logging:
  level:
    com.eazybytes.cards: DEBUG
```

## Kiểm Thử Triển Khai

### 1. Khởi Động Lại Tất Cả Services

Khởi động lại các services theo thứ tự:
1. **Accounts Application**
2. **Loans Application**
3. **Cards Application**
4. Xác minh tất cả services đã đăng ký với **Eureka Server**
5. **Gateway Server Application**

### 2. Tạo Dữ Liệu Test

Vì sử dụng H2 database, tạo dữ liệu test trước thông qua Gateway Server (Port 8072):

**Tạo Account:**
```http
POST http://localhost:8072/eazybank/accounts/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Tạo Card:**
```http
POST http://localhost:8072/eazybank/cards/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

**Tạo Loan:**
```http
POST http://localhost:8072/eazybank/loans/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

### 3. Kiểm Tra Luồng Correlation ID

**Lấy Thông Tin Chi Tiết Customer:**
```http
GET http://localhost:8072/eazybank/accounts/api/fetchCustomerDetails?mobileNumber=1234567890
```

**Response Mong Đợi:**
- Status: 200 OK
- Body: Chứa chi tiết account, loan, và card
- **Headers: Chứa `eazybank-correlation-id`**

### 4. Xác Minh Logs

**Gateway Server Logs:**
```
eazybank-correlation-id generated in RequestTraceFilter: <UUID>
Updated the correlation id to the outbound headers
```

**Accounts Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

**Loans Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

**Cards Microservice Logs:**
```
eazybank-correlation-id found: <UUID>
```

## Các Tình Huống Sử Dụng Correlation ID

### Luồng Request Thành Công

1. Client gửi request đến Gateway Server
2. Gateway tạo correlation ID: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
3. Gateway chuyển tiếp đến Accounts với correlation ID trong header
4. Accounts ghi log: "correlation-id found: a1b2c3d4..."
5. Accounts chuyển tiếp đến Loans với cùng correlation ID
6. Loans ghi log: "correlation-id found: a1b2c3d4..."
7. Accounts chuyển tiếp đến Cards với cùng correlation ID
8. Cards ghi log: "correlation-id found: a1b2c3d4..."
9. Gateway trả về response với correlation ID trong header

### Gỡ Lỗi Request Thất Bại

**Tình Huống:** Client báo lỗi với correlation ID cụ thể

1. Tìm kiếm Gateway logs theo correlation ID → Request đã đến Gateway ✓
2. Tìm kiếm Accounts logs theo correlation ID → Request đã đến Accounts ✓
3. Tìm kiếm Loans logs theo correlation ID → Request KHÔNG tìm thấy ✗
4. **Kết Luận:** Vấn đề xảy ra trong giao tiếp Accounts → Loans

## Các Điểm Triển Khai Chính

### Sử Dụng @RequestHeader

```java
@RequestHeader("eazybank-correlation-id") String correlationId
```

- Trích xuất giá trị header từ HTTP request
- Tương tự `@RequestParam` nhưng dành cho headers
- Tự động ánh xạ giá trị header sang tham số method

### Truyền Headers qua Feign Client

```java
@FeignClient(name = "loans")
public interface LoansFeignClient {
    @GetMapping("/api/fetch")
    ResponseEntity<LoansDto> fetchLoanDetails(
        @RequestHeader("eazybank-correlation-id") String correlationId,
        @RequestParam String mobileNumber
    );
}
```

- Feign tự động thêm header vào request gửi đi
- Duy trì correlation ID qua các ranh giới microservice

### Thực Hành Tốt Với Logger

```java
private static final Logger logger = LoggerFactory.getLogger(ClassName.class);
```

- Sử dụng SLF4J Logger
- Đặt `static final` để tối ưu hiệu suất
- Sử dụng tên class đúng để nhận diện log

## Lợi Ích Của Triển Khai Này

1. **Truy Vết End-to-End** - Theo dõi requests qua tất cả microservices
2. **Gỡ Lỗi Dễ Dàng** - Nhanh chóng xác định nơi xảy ra lỗi
3. **Hỗ Trợ Client** - Clients có thể cung cấp correlation ID trong support tickets
4. **Tập Hợp Log** - Tìm kiếm tất cả logs sử dụng một correlation ID duy nhất
5. **Phân Tích Hiệu Suất** - Đo độ trễ qua các microservices

## Gateway Server như Edge Server

Gateway Server hoạt động như một **Edge Server** cung cấp:

- **Điểm Vào Duy Nhất** - Tất cả traffic bên ngoài đi qua port 8072
- **Cross-Cutting Concerns** - Logging, auditing, security
- **Request Routing** - Định tuyến đến microservices thích hợp
- **Custom Filters** - Tiền xử lý và hậu xử lý requests/responses
- **Security Layer** - Xác thực và phân quyền (được đề cập trong phần security)

## Tóm Tắt Các Bước Triển Khai

1. ✅ Tạo Gateway Server với Spring Cloud Gateway
2. ✅ Thêm dependencies vào project
3. ✅ Cấu hình properties trong `application.yml`
4. ✅ Cấu hình routing
5. ✅ Tạo custom filters cho correlation ID
6. ✅ Cập nhật microservices để chấp nhận correlation ID
7. ✅ Kích hoạt debug logging
8. ✅ Kiểm thử qua Gateway Server trên port 8072

## Chuẩn Bị Phỏng Vấn

Các khái niệm chính cần nhớ:
- **Edge Server Pattern** - Điểm vào duy nhất cho tất cả client requests
- **Correlation ID** - Mã định danh duy nhất để truy vết request
- **Spring Cloud Gateway** - Được xây dựng trên Spring Reactive (không phải Servlet API)
- **Custom Filters** - Triển khai cross-cutting concerns
- **Feign Client** - HTTP client khai báo cho giao tiếp giữa các services
- **Service Discovery** - Tất cả services đăng ký với Eureka

## Các Bước Tiếp Theo

Trong phần bảo mật microservices, Gateway Server sẽ được tận dụng để:
- Triển khai xác thực và phân quyền
- Đảm bảo chỉ người dùng được xác thực mới có thể truy cập microservices
- Tập trung hóa các vấn đề bảo mật tại edge

## Tài Nguyên

- Tham khảo slides để ôn tập nhanh các khái niệm
- Sử dụng trong chuẩn bị phỏng vấn
- Tham chiếu cho việc triển khai Gateway patterns trong dự án thực tế



================================================================================
FILE: 38-api-gateway-design-patterns-overview.md
================================================================================

# Tổng Quan Các Mẫu Thiết Kế API Gateway

## Giới Thiệu

Tài liệu này cung cấp cái nhìn tổng quan toàn diện về các mẫu thiết kế (design patterns) liên quan đến API Gateway trong kiến trúc microservices. Những mẫu thiết kế này rất quan trọng để xây dựng hệ thống microservice có khả năng mở rộng, dễ bảo trì và hiệu quả bằng Spring Cloud Gateway.

## 1. Mẫu API Gateway (API Gateway Pattern)

### Tổng Quan
Mẫu API Gateway đề cập đến một thành phần hoạt động như điểm vào duy nhất (single entry point) cho hệ sinh thái microservices của bạn.

### Trách Nhiệm Chính
- **Định tuyến (Routing)**: Điều hướng các yêu cầu từ client đến các microservices backend phù hợp
- **Bảo mật (Security)**: Xử lý xác thực và phân quyền
- **Giao tiếp (Communication)**: Đơn giản hóa giao tiếp giữa clients và services

### Kiến Trúc
```
Ứng Dụng Client (Web/Mobile) → API Gateway → Microservices
```

### Triển Khai
Chúng ta triển khai mẫu này bằng Spring Cloud Gateway, hoạt động như một edge server hoặc điểm vào thống nhất cho tất cả microservices.

### Lợi Ích
- Kiểm soát truy cập tập trung
- Đơn giản hóa giao tiếp từ phía client
- Điểm vào duy nhất cho tất cả các yêu cầu

---

## 2. Mẫu Định Tuyến Gateway (Gateway Routing Pattern)

### Tổng Quan
Mẫu này mô tả một edge server có khả năng định tuyến các yêu cầu từ client đến các microservices backend phù hợp dựa trên nhiều yếu tố khác nhau.

### Các Yếu Tố Định Tuyến
- Đường dẫn URL
- HTTP headers
- Tham số yêu cầu (request parameters)
- Query strings

### Triển Khai với Spring Cloud Gateway
Triển khai của chúng ta định tuyến các yêu cầu dựa trên giá trị URL, đáp ứng yêu cầu của mẫu này.

### Ví Dụ
```
/accounts/** → Microservice Tài Khoản
/loans/** → Microservice Cho Vay
/cards/** → Microservice Thẻ
```

---

## 3. Mẫu Giảm Tải Gateway (Gateway Offloading Pattern)

### Tổng Quan
Mẫu Gateway Offloading liên quan đến việc ủy thác các mối quan tâm xuyên suốt (cross-cutting concerns) từ các microservices riêng lẻ sang API Gateway.

### Các Mối Quan Tâm Xuyên Suốt Cần Giảm Tải
- **Bảo mật (Security)**: Xác thực và phân quyền
- **Bộ nhớ đệm (Caching)**: Lưu cache phản hồi
- **Giới hạn tốc độ (Rate Limiting)**: Kiểm soát lưu lượng yêu cầu
- **Giám sát (Monitoring)**: Ghi log và metrics
- **Kết thúc SSL (SSL Termination)**: Xử lý HTTPS
- **Cân bằng tải (Load Balancing)**: Phân phối yêu cầu

### Những Gì KHÔNG NÊN Giảm Tải
❌ Logic nghiệp vụ (ví dụ: logic quản lý tài khoản)
❌ Xử lý đặc thù domain
❌ Xác thực dữ liệu đặc thù cho quy tắc nghiệp vụ

### Lợi Ích
- Giảm trùng lặp mã nguồn
- Quản lý tập trung các mối quan tâm chung
- Đơn giản hóa việc phát triển microservice

---

## 4. Mẫu Backend For Frontend (BFF)

### Tổng Quan
Mẫu BFF liên quan đến việc tạo nhiều API Gateway, mỗi gateway được tùy chỉnh cho một loại ứng dụng client cụ thể.

### Kiến Trúc
```
Web Client → Web API Gateway → Microservices
Mobile Client → Mobile API Gateway → Microservices
Tablet Client → Tablet API Gateway → Microservices
```

### Các Trường Hợp Sử Dụng

#### Tối Ưu Hóa Phản Hồi
- **Mobile/Tablet**: Phản hồi được nén cho các client nhẹ
- **Web**: Phản hồi đầy đủ chi tiết với hình ảnh và dữ liệu mở rộng

#### Tùy Chỉnh Nội Dung
- **Web**: Thông tin đầy đủ bao gồm hình ảnh, giao dịch chi tiết
- **Mobile**: Thông tin hạn chế, chỉ có tóm tắt, không có hình ảnh
- **Tablet**: Tối ưu cho màn hình kích thước trung bình

### Khi Nào Sử Dụng BFF
- Ứng dụng doanh nghiệp phức tạp
- Các yêu cầu khác nhau từ client
- Cần tối ưu hóa theo từng loại client
- Định dạng dữ liệu thay đổi theo loại client

### Lợi Ích
- Trải nghiệm được tối ưu cho từng loại client
- Hiệu suất tốt hơn cho các thiết bị có tài nguyên hạn chế
- Linh hoạt trong định dạng phản hồi

---

## 5. Mẫu Tổng Hợp Gateway / Mẫu Kết Hợp Gateway (Gateway Aggregation / Gateway Composition Pattern)

### Tổng Quan
Mẫu này liên quan đến việc tổng hợp dữ liệu từ nhiều microservices thành một phản hồi duy nhất tại tầng API Gateway.

### Phát Biểu Vấn Đề
Khi client cần dữ liệu từ nhiều microservices (ví dụ: tóm tắt tài khoản, cho vay và thẻ), có một số cách tiếp cận:

#### ❌ Cách 1: Nhiều Lời Gọi Riêng Lẻ (Không Khuyến Nghị)
```
Client → Microservice Tài Khoản
Client → Microservice Cho Vay
Client → Microservice Thẻ
```
**Vấn đề**: Quá nhiều lưu lượng mạng, tăng độ trễ

#### ✅ Cách 2: Tổng Hợp Giữa Các Service
```
Client → Accounts → [Loans, Cards] → Phản Hồi Kết Hợp
```
**Triển khai**: Một microservice gọi các service khác và kết hợp dữ liệu

#### ✅ Cách 3: Tổng Hợp Gateway (Khuyến Nghị)
```
Client → API Gateway → [Accounts, Loans, Cards] → Phản Hồi Kết Hợp
```

### Ví Dụ Triển Khai
```
GET /api/summary
↓
API Gateway gọi:
  - GET /accounts/summary
  - GET /loans/summary
  - GET /cards/summary
↓
Kết hợp tất cả phản hồi
↓
Trả về phản hồi tổng hợp duy nhất
```

### Lợi Ích
- Yêu cầu đơn từ góc độ client
- Giảm chi phí mạng
- Logic tổng hợp dữ liệu tập trung
- Hiệu suất tốt hơn

---

## Tóm Tắt

### Bảng Tham Chiếu Nhanh Các Mẫu

| Mẫu | Mục Đích | Đặc Điểm Chính |
|---------|---------|-------------|
| **API Gateway** | Điểm vào duy nhất | Truy cập tập trung vào microservices |
| **Gateway Routing** | Định tuyến thông minh | Định tuyến dựa trên URL, headers, parameters |
| **Gateway Offloading** | Tập trung các mối quan tâm | Xử lý bảo mật, caching, monitoring |
| **Backend For Frontend** | Gateway riêng cho từng client | Tối ưu cho từng loại client |
| **Gateway Aggregation** | Kết hợp dữ liệu | Kết hợp dữ liệu từ nhiều services |

### Những Điểm Chính Cần Nhớ

1. **Mẫu API Gateway**: Nền tảng cho tất cả các mẫu khác - cung cấp điểm vào thống nhất
2. **Mẫu Gateway Routing**: Cần thiết để điều hướng lưu lượng đến đúng microservices
3. **Mẫu Gateway Offloading**: Giảm độ phức tạp của microservice bằng cách tập trung các mối quan tâm xuyên suốt
4. **Mẫu BFF**: Giải quyết các yêu cầu đặc thù của client trong ứng dụng phức tạp
5. **Mẫu Gateway Aggregation**: Tối ưu giao tiếp client-server bằng cách giảm số lượt đi về

### Thực Hành Tốt Nhất

- ✅ Triển khai API Gateway làm điểm vào của bạn
- ✅ Sử dụng định tuyến dựa trên các mẫu URL rõ ràng
- ✅ Giảm tải các mối quan tâm xuyên suốt sang gateway
- ✅ Cân nhắc BFF cho các yêu cầu client đa dạng
- ✅ Sử dụng aggregation để giảm độ phức tạp phía client
- ❌ Không giảm tải logic nghiệp vụ sang gateway
- ❌ Không tạo độ phức tạp không cần thiết với nhiều gateway trừ khi thực sự cần

---

## Kết Luận

Hiểu các mẫu thiết kế API Gateway này rất quan trọng cho:
- Phỏng vấn kiến trúc microservice
- Thiết kế hệ thống có khả năng mở rộng
- Đưa ra quyết định kiến trúc sáng suốt
- Triển khai các mẫu giao tiếp hiệu quả

Những mẫu này hoạt động cùng nhau để tạo ra một kiến trúc microservices mạnh mẽ, có khả năng mở rộng và dễ bảo trì bằng Spring Cloud Gateway.

---

*Tài liệu này dựa trên các nguyên tắc kiến trúc microservices và triển khai Spring Cloud Gateway.*



================================================================================
FILE: 39-generating-docker-images-gateway-and-health-probes.md
================================================================================

# Tạo Docker Images cho Gateway Server và Cấu hình Health Probes

## Tổng quan

Hướng dẫn này bao gồm quy trình xây dựng Docker images cho các microservices trong Phần 9, bao gồm cấu hình health probes cho Edge server (API Gateway) và tạo Docker images sử dụng Maven và Jib.

## Yêu cầu trước

- Các dự án microservices đã hoàn thành (accounts, loans, cards, config server, Eureka server, gateway server)
- Docker Desktop đã được cài đặt và đang chạy
- Maven đã được cài đặt
- Tài khoản Docker Hub (để push images)

## Bước 1: Kích hoạt Health Probes trong Microservices

Trước khi tạo Docker images, chúng ta cần kích hoạt các endpoints liên quan đến health (readiness và liveness probes) trong các microservices accounts, loans và cards. Điều này rất quan trọng để Docker Compose quản lý đúng các phụ thuộc của service.

### Tại sao cần Health Probes?

Gateway server chỉ nên khởi động sau khi các microservices accounts, cards và loans đã hoạt động tốt và khỏe mạnh. Health probes cho phép Docker Compose kiểm tra tình trạng health của service trước khi khởi động các services phụ thuộc.

### Các bước cấu hình

#### 1. Microservice Accounts

Trong file `application.yml`, thêm các thuộc tính sau:

**Dưới `management.endpoints`:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
    shutdown:
      enabled: true
    health:
      probes:
        enabled: true
```

**Thêm cấu hình health:**
```yaml
management:
  health:
    readinessstate:
      enabled: true
    livenessstate:
      enabled: true
```

#### 2. Microservice Cards

Áp dụng cùng cấu hình trong `cards/application.yml`:

- Thêm health probes enabled dưới `management.endpoints`
- Thêm cấu hình readiness và liveness state dưới `management.health`

#### 3. Microservice Loans

Áp dụng cùng cấu hình trong `loans/application.yml`:

- Thêm health probes enabled dưới `management.endpoints`
- Thêm cấu hình readiness và liveness state dưới `management.health`

## Bước 2: Chuẩn bị cho việc tạo Docker Image

### Kiểm tra cấu hình POM

Trước khi build Docker images, đảm bảo tất cả các microservices có tag đúng trong file `pom.xml`:

```xml
<image>
    <name>docker.io/yourusername/${project.artifactId}:s9</name>
</image>
```

Tag nên là `s9` để chỉ ra images của Phần 9.

### Làm sạch môi trường Docker

1. Mở Docker Desktop
2. Xóa bất kỳ images microservice hiện có nào
3. Đảm bảo không có containers liên quan đang chạy

## Bước 3: Build Docker Images với Maven và Jib

Điều hướng đến từng thư mục microservice và chạy lệnh Maven để build Docker images sử dụng Jib.

### Cú pháp lệnh

```bash
mvn compile jib:dockerBuild
```

**Lưu ý:** Chữ 'B' trong dockerBuild phải viết hoa.

### Trình tự Build

#### 1. Microservice Accounts

```bash
cd section9/accounts
mvn compile jib:dockerBuild
```

#### 2. Microservice Loans

```bash
cd ../loans
mvn compile jib:dockerBuild
```

#### 3. Microservice Cards

```bash
cd ../cards
mvn compile jib:dockerBuild
```

#### 4. Config Server

```bash
cd ../configserver
mvn compile jib:dockerBuild
```

#### 5. Eureka Server

```bash
cd ../eurekaserver
mvn compile jib:dockerBuild
```

#### 6. Gateway Server

```bash
cd ../gatewayserver
mvn compile jib:dockerBuild
```

### Ưu điểm của Jib

- **Build nhanh:** Jib tạo Docker images nhanh hơn nhiều so với Buildpacks
- **Không cần Docker daemon:** Có thể build mà không cần Docker đang chạy
- **Phân lớp hiệu quả:** Tối ưu hóa layer caching để rebuild nhanh hơn

Buildpacks thường mất ít nhất 1 phút mỗi image, trong khi Jib hoàn thành trong vài giây.

## Bước 4: Xác minh Docker Images

### Sử dụng Command Line

```bash
docker images
```

Tìm 6 images với tag `s9`:
1. accounts:s9
2. loans:s9
3. cards:s9
4. configserver:s9
5. eurekaserver:s9
6. gatewayserver:s9

### Sử dụng Docker Desktop

1. Mở Docker Desktop
2. Điều hướng đến phần Images
3. Tìm kiếm images với tag `s9`
4. Xác minh tất cả 6 images đều có mặt

## Bước 5: Push Images lên Docker Hub

Để chia sẻ images của bạn hoặc triển khai chúng đến các môi trường khác, push chúng lên Docker Hub.

### Cú pháp lệnh Push

```bash
docker image push docker.io/yourusername/imagename:s9
```

### Ví dụ: Push Microservice Accounts

```bash
docker image push docker.io/eazybytes/accounts:s9
```

### Push tất cả Images

Lặp lại lệnh cho từng microservice:

```bash
docker image push docker.io/yourusername/accounts:s9
docker image push docker.io/yourusername/loans:s9
docker image push docker.io/yourusername/cards:s9
docker image push docker.io/yourusername/configserver:s9
docker image push docker.io/yourusername/eurekaserver:s9
docker image push docker.io/yourusername/gatewayserver:s9
```

## Các bước tiếp theo

1. Cập nhật file Docker Compose để bao gồm cấu hình gateway server
2. Định nghĩa các phụ thuộc service sử dụng health checks
3. Kiểm tra toàn bộ mạng microservices với Docker containers
4. Xác minh routing và filtering của gateway server

## Best Practices (Thực hành tốt nhất)

- **Tạo Image thường xuyên:** Build Docker images tại các mốc quan trọng để dễ dàng kiểm tra
- **Quản lý Tag:** Sử dụng tags mô tả (như số phần) để kiểm soát phiên bản
- **GitHub Repository:** Lưu trữ các lệnh Maven trong repository của bạn
- **Môi trường sạch:** Xóa các images cũ trước khi build images mới để tránh xung đột

## Tóm tắt

Trong hướng dẫn này, chúng ta đã:
- Kích hoạt health probes trong các microservices accounts, loans và cards
- Cấu hình readiness và liveness endpoints để kiểm tra health của service
- Tạo Docker images cho tất cả 6 microservices sử dụng Maven và Jib
- Xác minh việc tạo image trong Docker Desktop
- Push images lên Docker Hub để phân phối

Các bước này chuẩn bị microservices của bạn cho việc triển khai container hóa và cho phép quản lý phụ thuộc đúng cách trong Docker Compose.



================================================================================
FILE: 4-validating-docker-compose-setup.md
================================================================================

# Xác Thực và Khắc Phục Sự Cố Docker Compose với MySQL Databases

## Tổng Quan

Hướng dẫn này hướng dẫn quy trình xác thực cấu hình Docker Compose, xác định và khắc phục các vấn đề thường gặp, và kiểm thử toàn bộ thiết lập microservices với MySQL databases. Chúng ta sẽ đề cập đến các khái niệm quan trọng về Docker networking và kỹ thuật khắc phục sự cố.

## Yêu Cầu Tiên Quyết

- Hoàn thành cấu hình Docker Compose từ phần trước
- Docker Desktop đã cài đặt và đang chạy
- Tất cả Docker images được build với tag `s7`
- Truy cập Terminal/Command prompt
- SQL client (SQL Electron hoặc tương tự) để xác minh database
- Postman để kiểm thử API

## Bước 1: Cập Nhật Docker Image Tags

Trước khi chạy Docker Compose, đảm bảo tất cả microservice images sử dụng tag đúng.

### Vấn Đề

Nếu bạn sử dụng image tags cũ (như `s6`), những images đó chứa cấu hình H2 database, không phải MySQL. Điều này sẽ gây lỗi kết nối.

### Giải Pháp

Mở `docker-compose.yml` và cập nhật tất cả image tags từ `s6` sang `s7`:

**Trước:**
```yaml
services:
  configserver:
    image: "eazybytes/configserver:s6"  # ❌ Tag cũ
  
  accounts:
    image: "eazybytes/accounts:s6"  # ❌ Tag cũ
  
  loans:
    image: "eazybytes/loans:s6"  # ❌ Tag cũ
  
  cards:
    image: "eazybytes/cards:s6"  # ❌ Tag cũ
```

**Sau:**
```yaml
services:
  configserver:
    image: "eazybytes/configserver:s7"  # ✅ Tag mới
  
  accounts:
    image: "eazybytes/accounts:s7"  # ✅ Tag mới
  
  loans:
    image: "eazybytes/loans:s7"  # ✅ Tag mới
  
  cards:
    image: "eazybytes/cards:s7"  # ✅ Tag mới
```

**Tại sao điều này quan trọng:** Images `s7` bao gồm MySQL dependencies và configurations, trong khi images `s6` có thiết lập H2 database.

## Bước 2: Xóa Dependencies Đã Lỗi Thời

### Xóa RabbitMQ Dependency khỏi Config Server

Vì chúng ta đã xóa Spring Cloud Bus, Config Server không còn phụ thuộc vào RabbitMQ.

**Tìm đoạn này trong docker-compose.yml:**
```yaml
configserver:
  image: "eazybytes/configserver:s7"
  depends_on:
    - rabbit  # ❌ Service này không còn tồn tại
```

**Sửa:**
```yaml
configserver:
  image: "eazybytes/configserver:s7"
  # Xóa depends_on hoàn toàn, hoặc xóa rabbit khỏi danh sách
```

**Lỗi bạn sẽ thấy nếu không sửa:**
```
Error: config server depends on undefined service: rabbit
```

## Bước 3: Lần Thử Docker Compose Đầu Tiên

Điều hướng đến thư mục Docker Compose và chạy lệnh.

### Điều Hướng Đến Thư Mục

```bash
cd docker-compose/default
```

### Chạy Docker Compose

```bash
docker-compose up
```

**Điều gì xảy ra:**
- Database containers khởi động trước
- Sau khi healthy, microservices bắt đầu khởi động
- Logs xuất hiện trong terminal (chưa dùng detached mode)

### Thứ Tự Khởi Động Mong Đợi

1. **Database containers** (accountsdb, loansdb, cardsdb)
2. **Config Server** (sau khi databases healthy)
3. **Microservices** (accounts, loans, cards - sau khi Config Server healthy)

## Bước 4: Xác Định Vấn Đề Cấu Hình Port

### Vấn Đề Bất Ngờ

Sau khi đợi containers khởi động, bạn sẽ nhận thấy:

✅ **Khởi động thành công:**
- accountsdb
- loansdb
- cardsdb
- configserver
- accounts microservice

❌ **Thất bại khi khởi động:**
- cards microservice
- loans microservice

### Xem Lỗi

**Trong Docker Desktop:**
1. Click vào container thất bại (cards hoặc loans)
2. Kiểm tra logs

**Thông báo lỗi:**
```
Unable to connect to database
Connection refused to loansdb:3307
Connection refused to cardsdb:3308
```

## Bước 5: Hiểu Về Docker Networking

### Nguyên Nhân Gốc Rễ

**Cấu hình của bạn:**
```yaml
loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3307/loansDB  # ❌ Port sai

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3308/cardsDB  # ❌ Port sai
```

### Tại Sao Điều Này Sai

**Khái niệm quan trọng:** Có sự khác biệt giữa **external ports** (host) và **internal ports** (container network).

**Cú pháp port mapping:** `HOST_PORT:CONTAINER_PORT`

```yaml
loansdb:
  ports:
    - "3307:3306"  # Host port 3307 → Container port 3306

cardsdb:
  ports:
    - "3308:3306"  # Host port 3308 → Container port 3306
```

### Giao Tiếp External vs Internal

**Giao Tiếp External** (từ máy host của bạn):
- Sử dụng: `localhost:3307` cho loansdb
- Sử dụng: `localhost:3308` cho cardsdb
- Ví dụ: SQL Electron kết nối từ máy tính của bạn

**Giao Tiếp Internal** (giữa các containers):
- Sử dụng: `loansdb:3306` (service name + internal port)
- Sử dụng: `cardsdb:3306` (service name + internal port)
- Ví dụ: Microservices kết nối đến databases

### Tại Sao Port Mapping Tồn Tại

**Câu hỏi:** Nếu containers giao tiếp trên port 3306, tại sao map sang 3307 và 3308?

**Trả lời:** Port mapping chỉ dành cho **truy cập external**:
- Cho phép SQL clients trên host kết nối
- Kích hoạt debugging và xác minh dữ liệu
- Ngăn xung đột port (không thể có ba services trên port 3306 trên host)

**Quan trọng:** Port mapping **không cần thiết** cho giao tiếp container-to-container. Nó hoàn toàn dành cho truy cập từ host.

## Bước 6: Sửa Cấu Hình Port

Cập nhật datasource URLs để sử dụng internal container ports.

### Cấu Hình Đúng

```yaml
accounts:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://accountsdb:3306/accountsDB  # ✅ Đúng

loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://loansdb:3306/loansDB  # ✅ Đã sửa

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://cardsdb:3306/cardsDB  # ✅ Đã sửa
```

**Điểm chính:** Tất cả kết nối database từ microservices sử dụng port **3306** (internal container port), không phải các external mapped ports.

## Bước 7: Khởi Động Lại Docker Compose

### Dừng Containers Đang Chạy

Nhấn `Ctrl+C` trong terminal nơi `docker-compose up` đang chạy.

**Điều này chỉ dừng containers, không xóa chúng.**

### Xóa Containers

```bash
docker-compose down
```

**Lệnh này:**
- Dừng tất cả containers
- Xóa tất cả containers
- Xóa network
- KHÔNG xóa volumes hoặc images

### Khởi Động với Detached Mode

```bash
docker-compose up -d
```

**Flag `-d`:**
- Chạy containers ở background (detached mode)
- Giải phóng terminal cho các lệnh khác
- Logs vẫn truy cập được qua `docker logs` hoặc Docker Desktop

## Bước 8: Cập Nhật Cấu Hình QA và Prod

Áp dụng các sửa chữa tương tự cho các môi trường khác.

### Copy Cấu Hình Default

**Cho Prod:**
1. Mở `docker-compose-prod.yml`
2. Copy tất cả nội dung từ `docker-compose.yml` (default)
3. Paste vào `docker-compose-prod.yml`

**Cho QA:**
1. Mở `docker-compose-qa.yml`
2. Copy tất cả nội dung từ `docker-compose.yml` (default)
3. Paste vào `docker-compose-qa.yml`

### Cập Nhật Common Config cho Prod

**Trong common-config.yml cho prod:**
```yaml
microservice-configserver-config:
  extends:
    service: microservice-base-config
  environment:
    SPRING_PROFILES_ACTIVE: prod  # ✅ Đổi thành prod
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_DATASOURCE_USERNAME: root
    SPRING_DATASOURCE_PASSWORD: root
```

### Cập Nhật Common Config cho QA

**Trong common-config.yml cho qa:**
```yaml
microservice-configserver-config:
  extends:
    service: microservice-base-config
  environment:
    SPRING_PROFILES_ACTIVE: qa  # ✅ Đổi thành qa
    SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
    SPRING_DATASOURCE_USERNAME: root
    SPRING_DATASOURCE_PASSWORD: root
```

## Bước 9: Xác Minh Khởi Động Thành Công

### Kiểm Tra Docker Desktop

Mở Docker Desktop và xác minh tất cả 7 containers đang chạy:

✅ **Database Containers:**
- accountsdb
- loansdb
- cardsdb

✅ **Application Containers:**
- configserver
- accounts
- loans
- cards

### Giám Sát Logs Khởi Động

Click vào từng microservice container để xem logs:

**Cho Cards microservice:**
```
Added connection to database
Created connection pool
Started CardsApplication in X seconds
```

**Cho Loans microservice:**
```
Added connection to database
Created connection pool
Started LoansApplication in X seconds
```

**Các thông báo log này xác nhận kết nối database thành công.**

## Bước 10: Kiểm Thử REST APIs với Postman

Xác minh tất cả microservices hoạt động đúng.

### Kiểm Thử Create Account

**Request:**
- Method: POST
- URL: `http://localhost:8080/api/create`
- Body:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Thông báo thành công

### Kiểm Thử Create Card

**Request:**
- Method: POST
- URL: `http://localhost:9000/api/create`
- Body:
```json
{
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Chi tiết card được trả về

### Kiểm Thử Create Loan

**Request:**
- Method: POST
- URL: `http://localhost:8090/api/create`
- Body:
```json
{
  "mobileNumber": "9876543210"
}
```

**Response Mong Đợi:**
- Status: 201 Created
- Chi tiết loan được trả về

**Kết quả:** Cả ba APIs nên trả về responses thành công.

## Bước 11: Xác Minh Tính Bền Vững Database

Sử dụng SQL Electron (hoặc bất kỳ MySQL client nào) để xác minh dữ liệu đã được lưu.

### Chi Tiết Kết Nối

**Accounts Database:**
- Host: localhost
- Port: 3306
- Database: accountsDB
- Username: root
- Password: root

**Loans Database:**
- Host: localhost
- Port: 3307 ⭐ (external port)
- Database: loansDB
- Username: root
- Password: root

**Cards Database:**
- Host: localhost
- Port: 3308 ⭐ (external port)
- Database: cardsDB
- Username: root
- Password: root

### Xác Minh Dữ Liệu

**Trong Accounts Database:**
1. Kết nối đến accountsdb
2. Kiểm tra bảng `accounts` - nên có dữ liệu account
3. Kiểm tra bảng `customer` - nên có dữ liệu customer

**Trong Loans Database:**
1. Kết nối đến loansdb
2. Kiểm tra bảng `loans` - nên có dữ liệu loan

**Trong Cards Database:**
1. Kết nối đến cardsdb
2. Kiểm tra bảng `cards` - nên có dữ liệu card

**Thành công:** Tất cả bảng chứa dữ liệu bạn đã tạo qua REST APIs.

## Bước 12: Kết Nối Với External Databases

### Kịch Bản: Sử Dụng Cloud hoặc Remote Databases

Nếu bạn không sử dụng local Docker database containers? Nếu bạn có:
- Development database trong cloud (AWS RDS, Azure SQL, v.v.)
- Shared development database server
- Managed database service

### Thay Đổi Đơn Giản

**Bạn không cần database containers trong docker-compose.yml.**

Xóa các services này:
```yaml
# Xóa hoàn toàn
accountsdb:
  # ... tất cả cấu hình database

loansdb:
  # ... tất cả cấu hình database

cardsdb:
  # ... tất cả cấu hình database
```

### Cập Nhật Datasource URLs

Trỏ trực tiếp đến external databases:

```yaml
accounts:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/accountsDB
    # Hoặc sử dụng public IP: jdbc:mysql://52.123.45.67:3306/accountsDB

loans:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/loansDB

cards:
  environment:
    SPRING_DATASOURCE_URL: jdbc:mysql://dev-db.example.com:3306/cardsDB
```

### Cập Nhật Credentials

Sử dụng credentials phù hợp cho external database:

```yaml
microservice-configserver-config:
  environment:
    SPRING_DATASOURCE_USERNAME: dev_user  # Không phải root
    SPRING_DATASOURCE_PASSWORD: secure_password
```

**Best Practice:** Sử dụng environment variables hoặc secrets cho production credentials:

```yaml
environment:
  SPRING_DATASOURCE_USERNAME: ${DB_USERNAME}
  SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD}
```

### Xóa Database Dependencies

Xóa `depends_on` cho databases:

```yaml
accounts:
  depends_on:
    configserver:
      condition: service_healthy
    # Xóa accountsdb dependency
```

**Tại sao:** External databases đã chạy rồi; không cần đợi chúng khởi động.

## Tóm Tắt Khái Niệm Docker Networking

### Container Networks

Khi sử dụng Docker Compose:
- Tất cả services trong cùng compose file chia sẻ một network
- Containers giao tiếp sử dụng **service names** làm hostnames
- Không cần biết địa chỉ IP

### Giải Thích Port Mapping

**Cú pháp:** `HOST_PORT:CONTAINER_PORT`

```yaml
ports:
  - "8080:8080"  # Host 8080 → Container 8080
  - "3307:3306"  # Host 3307 → Container 3306
```

**Hai góc nhìn:**

**Từ Host (máy tính của bạn):**
- Truy cập accounts microservice: `http://localhost:8080`
- Truy cập loans database: `localhost:3307`

**Từ Bên Trong Containers:**
- Truy cập accounts microservice: `http://accounts:8080`
- Truy cập loans database: `loansdb:3306`

### Khi Nào Port Mapping Cần Thiết

✅ **Cần port mapping:**
- Truy cập services từ máy host
- Sử dụng SQL clients từ máy tính của bạn
- Kiểm thử APIs từ Postman trên host
- Debugging từ IDE trên host

❌ **Không cần port mapping:**
- Giao tiếp container-to-container
- Microservice kết nối đến database
- Service discovery trong Docker network

**Ví dụ:** Nếu bạn chỉ cần microservices giao tiếp với databases (không truy cập external), bạn có thể bỏ qua port mapping hoàn toàn:

```yaml
loansdb:
  # Không cần phần ports cho truy cập chỉ internal
  image: mysql:latest
```

## Hướng Dẫn Khắc Phục Sự Cố

### Vấn Đề 1: Lỗi Undefined Service

**Lỗi:**
```
Error: configserver depends on undefined service: rabbit
```

**Nguyên nhân:** Tham chiếu đến service không tồn tại trong docker-compose.yml

**Giải pháp:** Xóa dependency hoặc thêm service còn thiếu

### Vấn Đề 2: Connection Refused

**Lỗi:**
```
Unable to connect to database
Connection refused to loansdb:3307
```

**Nguyên nhân:** Sử dụng external port thay vì internal container port

**Giải pháp:** Đổi datasource URL để sử dụng internal port (3306)

### Vấn Đề 3: Cấu Hình Database Sai

**Lỗi:**
```
Table doesn't exist
Schema not found
```

**Nguyên nhân:** Sử dụng Docker images cũ với cấu hình H2

**Giải pháp:** Rebuild images với tag đúng và MySQL dependencies

### Vấn Đề 4: Container Không Khởi Động

**Lỗi:**
```
Container exits immediately
Unhealthy status
```

**Nguyên nhân:** Nhiều khả năng
- Dependencies còn thiếu
- Lỗi cấu hình
- Health check thất bại

**Giải pháp:** 
- Kiểm tra logs: `docker logs <tên-container>`
- Xác minh cấu hình health check
- Đảm bảo dependencies healthy trước

### Vấn Đề 5: Không Thể Truy Cập Từ Host

**Lỗi:**
```
Cannot connect to localhost:3307 from SQL client
```

**Nguyên nhân:** Port mapping chưa được cấu hình

**Giải pháp:** Thêm port mapping trong docker-compose.yml

## Các Lệnh Docker Compose Hữu Ích

### Khởi Động Services

```bash
# Khởi động ở foreground (xem logs)
docker-compose up

# Khởi động ở background (detached)
docker-compose up -d

# Khởi động service cụ thể
docker-compose up -d accounts

# Rebuild và khởi động
docker-compose up --build
```

### Dừng Services

```bash
# Dừng containers (không xóa)
docker-compose stop

# Dừng và xóa containers, networks
docker-compose down

# Dừng và xóa containers, networks, volumes
docker-compose down -v

# Dừng service cụ thể
docker-compose stop accounts
```

### Xem Trạng Thái và Logs

```bash
# Liệt kê containers đang chạy
docker-compose ps

# Xem logs (tất cả services)
docker-compose logs

# Xem logs (service cụ thể)
docker-compose logs accounts

# Theo dõi logs real-time
docker-compose logs -f

# Xem 100 dòng cuối
docker-compose logs --tail=100
```

### Khởi Động Lại Services

```bash
# Khởi động lại tất cả services
docker-compose restart

# Khởi động lại service cụ thể
docker-compose restart accounts
```

### Thực Thi Lệnh Trong Containers

```bash
# Mở shell trong container
docker-compose exec accounts sh

# Chạy lệnh trong container
docker-compose exec accountsdb mysql -u root -p
```

## Best Practices

✅ **Luôn sử dụng detached mode trong production** (flag `-d`)  
✅ **Sử dụng internal ports đúng cho giao tiếp container**  
✅ **Giữ image tags cập nhật và nhất quán**  
✅ **Giám sát logs sau khởi động để xác minh kết nối**  
✅ **Sử dụng health checks cho tất cả services**  
✅ **Xóa dependencies lỗi thời**  
✅ **Kiểm thử APIs sau deployment**  
✅ **Xác minh tính bền vững database**  

❌ **Không sử dụng external ports cho giao tiếp container-to-container**  
❌ **Không để lại service dependencies lỗi thời**  
❌ **Không sử dụng image tags cũ với cấu hình sai**  
❌ **Không bỏ qua xác minh logs**  
❌ **Không hardcode production credentials**  

## Tóm Tắt

### Những Gì Chúng Ta Đã Hoàn Thành

✅ Cập nhật Docker image tags từ s6 sang s7  
✅ Xóa RabbitMQ dependencies lỗi thời  
✅ Xác định và sửa vấn đề cấu hình port  
✅ Hiểu các khái niệm Docker networking  
✅ Khởi động thành công tất cả 7 containers  
✅ Kiểm thử tất cả REST APIs  
✅ Xác minh tính bền vững database  
✅ Học về cấu hình external database  

### Điểm Chính Cần Nhớ

1. **Image Tags Quan Trọng:** Sử dụng tags đúng khớp với cấu hình của bạn
2. **Internal vs External Ports:** Containers dùng internal ports (3306), host dùng mapped ports (3307, 3308)
3. **Service Names:** Sử dụng service names cho giao tiếp container-to-container
4. **Health Checks:** Quan trọng cho thứ tự khởi động đúng
5. **Detached Mode:** Sử dụng `-d` cho thực thi background
6. **External Databases:** Có thể bỏ qua database containers khi sử dụng remote databases
7. **Troubleshooting:** Kiểm tra logs và hiểu thông báo lỗi

### Điểm Chính Docker Networking

- **Service Name = Hostname** trong Docker networks
- **Port Mapping** chỉ dành cho external access
- **Giao tiếp internal** luôn sử dụng container ports
- **Xung đột external port** được ngăn chặn bởi mappings khác nhau

## Bước Tiếp Theo

Bây giờ mọi thứ đã hoạt động:

1. **Khám phá Docker volumes** cho tính bền vững dữ liệu
2. **Triển khai secrets management** cho credentials
3. **Thêm monitoring và observability**
4. **Học Docker Compose scaling**
5. **Khám phá Kubernetes** cho production deployments
6. **Triển khai CI/CD pipelines**
7. **Thêm API Gateway** cho unified access point
8. **Triển khai service mesh** cho advanced networking

---

**Chúc Mừng!** Bạn đã xác thực và khắc phục sự cố thành công toàn bộ thiết lập Docker Compose với Spring Boot microservices và MySQL databases. Bây giờ bạn hiểu Docker networking và có thể tự tin deploy containerized microservices.



================================================================================
FILE: 40-deploying-gateway-server-with-docker-compose.md
================================================================================

# Triển khai Gateway Server với Docker Compose

## Tổng quan

Hướng dẫn này bao gồm quy trình triển khai Spring Cloud Gateway server cùng với các microservice (Accounts, Loans, Cards) sử dụng Docker Compose. Chúng ta sẽ cấu hình health check, các phụ thuộc dịch vụ và xác thực tính năng correlation ID trên tất cả microservice.

## Yêu cầu trước khi bắt đầu

- Docker images đã được push lên Docker Hub với tag `S9`
- Các microservice hiện có: Accounts, Loans, Cards
- Config Server và Eureka Server đã được cấu hình
- Docker và Docker Compose đã được cài đặt

## Docker Images

Tất cả Docker images cho Section 9 đã được push lên Docker Hub với tag `S9`:
- `gatewayserver:S9`
- `accounts:S9`
- `loans:S9`
- `cards:S9`
- `configserver:S9`
- `eurekaserver:S9`

## Cấu hình Docker Compose

### 1. Thêm Gateway Server Service

Di chuyển đến thư mục `docker-compose/default` và mở file `docker-compose.yaml`. Thêm cấu hình Gateway Server service:

```yaml
gatewayserver:
  image: gatewayserver:S9
  container_name: gatewayserver-ms
  ports:
    - "8072:8072"
  environment:
    - SPRING_APPLICATION_NAME=gatewayserver
  depends_on:
    accounts:
      condition: service_healthy
    loans:
      condition: service_healthy
    cards:
      condition: service_healthy
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

### 2. Cập nhật Image Tags

Thay thế tất cả tag `S8` bằng `S9` trong toàn bộ file Docker Compose:
- Tìm kiếm: `S8`
- Thay thế bằng: `S9`

### 3. Cấu hình Health Checks

Thêm cấu hình health check cho từng microservice để đảm bảo thứ tự khởi động đúng.

#### Accounts Microservice (Cổng 8080)

```yaml
accounts:
  image: accounts:S9
  container_name: accounts-ms
  ports:
    - "8080:8080"
  healthcheck:
    test: "curl --fail --silent localhost:8080/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

#### Loans Microservice (Cổng 8090)

```yaml
loans:
  image: loans:S9
  container_name: loans-ms
  ports:
    - "8090:8090"
  healthcheck:
    test: "curl --fail --silent localhost:8090/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

#### Cards Microservice (Cổng 9000)

```yaml
cards:
  image: cards:S9
  container_name: cards-ms
  ports:
    - "9000:9000"
  healthcheck:
    test: "curl --fail --silent localhost:9000/actuator/health/readiness | grep UP || exit 1"
    interval: 10s
    timeout: 5s
    retries: 10
    start_period: 10s
  extends:
    file: common-config.yml
    service: microservice-eureka-config
```

## Thứ tự khởi động dịch vụ

Cấu hình Docker Compose đảm bảo các dịch vụ khởi động theo thứ tự sau:

1. **Config Server** - Quản lý cấu hình tập trung
2. **Eureka Server** - Khám phá và đăng ký dịch vụ
3. **Microservices** - Accounts, Loans và Cards (song song)
4. **Gateway Server** - Chỉ khởi động sau khi tất cả microservice đều healthy

## Các bước triển khai

### 1. Di chuyển đến thư mục Docker Compose

```bash
cd docker-compose/default
```

### 2. Khởi động tất cả Containers

```bash
docker compose up -d
```

Lệnh này sẽ khởi động tất cả container ở chế độ detached. Quá trình khởi động mất khoảng 1-2 phút.

### 3. Theo dõi tiến trình khởi động

Bạn có thể theo dõi các container sử dụng Docker Desktop hoặc dòng lệnh:

```bash
docker compose ps
```

Tất cả container sẽ hiển thị trạng thái "running" khi đã khởi động hoàn toàn.

## Kiểm thử triển khai

### 1. Tạo dữ liệu test

Sử dụng Gateway Server để tạo dữ liệu trong từng microservice:

**Tạo tài khoản:**
```http
POST http://localhost:8072/accounts/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Tạo thẻ:**
```http
POST http://localhost:8072/cards/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

**Tạo khoản vay:**
```http
POST http://localhost:8072/loans/api/create
Content-Type: application/json

{
  "mobileNumber": "1234567890"
}
```

### 2. Lấy thông tin khách hàng

Kiểm tra API tổng hợp lấy dữ liệu từ tất cả microservice:

```http
GET http://localhost:8072/accounts/api/fetchCustomerDetails?mobileNumber=1234567890
```

**Kết quả mong đợi:**
- Thông tin tài khoản
- Thông tin khoản vay
- Thông tin thẻ
- Response header: `easybank-correlationid` với correlation ID duy nhất

## Xác thực Correlation ID

Tính năng correlation ID cho phép theo dõi request qua nhiều microservice.

### 1. Kiểm tra Response Headers

Sau khi thực hiện request, kiểm tra response headers để tìm:
```
easybank-correlationid: <unique-id>
```

### 2. Xác minh Logs trong từng Microservice

Copy correlation ID và tìm kiếm nó trong logs của từng container:

**Accounts Microservice:**
```bash
docker logs accounts-ms | grep <correlation-id>
```

**Loans Microservice:**
```bash
docker logs loans-ms | grep <correlation-id>
```

**Cards Microservice:**
```bash
docker logs cards-ms | grep <correlation-id>
```

Bạn sẽ tìm thấy các log entry với:
- `RequestTraceFilter` - Request đến
- `ResponseTraceFilter` - Response đi

## Dừng Containers

Để dừng tất cả container đang chạy:

```bash
docker compose down
```

## Triển khai đa môi trường

### Môi trường QA

Cập nhật `qa/docker-compose.yml` với cùng cấu hình và đảm bảo:
```yaml
environment:
  - SPRING_PROFILES_ACTIVE=qa
```

### Môi trường Production

Cập nhật `prod/docker-compose.yml` với cùng cấu hình và đảm bảo:
```yaml
environment:
  - SPRING_PROFILES_ACTIVE=prod
```

## Lợi ích của Gateway Server

1. **Điểm truy cập duy nhất** - Client bên ngoài chỉ cần biết một URL
2. **Logic Client đơn giản** - Không cần quản lý nhiều URL microservice
3. **Tập trung Cross-Cutting Concerns** - Authentication, logging, rate limiting
4. **Định tuyến Request** - Định tuyến động dựa trên patterns
5. **Load Balancing** - Client-side load balancing với Eureka integration

## Xử lý sự cố

### Gateway Server không khởi động

- Xác minh tất cả microservice phụ thuộc đều healthy
- Kiểm tra Eureka Server đang chạy và có thể truy cập
- Xem lại gateway server logs: `docker logs gatewayserver-ms`

### Health Check thất bại

- Đảm bảo actuator endpoints được kích hoạt
- Xác minh port mappings đúng
- Kiểm tra kết nối mạng giữa các container

### Correlation ID không có

- Xác minh custom filters được cấu hình trong Gateway Server
- Kiểm tra thứ tự filter trong cấu hình gateway
- Xem lại gateway server logs để kiểm tra việc thực thi filter

## Các bước tiếp theo

Trong các phần tiếp theo, chúng ta sẽ nâng cao Gateway Server với:
- **Bảo mật** - Authentication và authorization
- **Khả năng chịu lỗi** - Circuit breakers và retry mechanisms
- **Resilience** - Rate limiting và bulkhead patterns
- **Giám sát** - Distributed tracing và metrics

## Tóm tắt

Chúng ta đã thành công:
- ✅ Cấu hình Gateway Server trong Docker Compose
- ✅ Triển khai health checks cho tất cả microservice
- ✅ Thiết lập các phụ thuộc dịch vụ đúng cách
- ✅ Xác thực correlation ID tracking qua các microservice
- ✅ Tạo cấu hình đa môi trường (QA và Prod)

Gateway Server hiện đóng vai trò là điểm truy cập duy nhất cho tất cả client bên ngoài, đơn giản hóa kiến trúc microservice và cung cấp nền tảng để triển khai các pattern nâng cao.

## Tài nguyên

- Website chính thức: [eazybytes.com](https://eazybytes.com)
- Liên hệ: Có sẵn trên website chính thức
- LinkedIn: Link profile trên website chính thức

---

**Lưu ý:** Tài liệu này là một phần của khóa học microservices toàn diện. Để biết thêm các khóa học và cập nhật, hãy truy cập website chính thức.



================================================================================
FILE: 41-xay-dung-microservices-ben-vung-voi-resilience4j.md
================================================================================

# Xây Dựng Microservices Bền Vững với Resilience4j

## Giới Thiệu

Xây dựng microservices có khả năng phục hồi là một thách thức quan trọng trong các hệ thống phân tán hiện đại. Khả năng phục hồi (resiliency) có nghĩa là khả năng chịu đựng những thời điểm khó khăn và phục hồi trở lại - giống như nhân loại đã vượt qua những thách thức như Covid, các microservices của chúng ta cũng phải có khả năng chịu đựng các vấn đề về mạng, hiệu suất và các thách thức khác hàng ngày.

## Các Thách Thức Chính Trong Microservice Resiliency

### 1. Tránh Lỗi Lan Truyền (Cascading Failures)

**Vấn Đề:**
Trong một mạng lưới microservices, nhiều dịch vụ làm việc cùng nhau để xử lý yêu cầu từ client. Khi một dịch vụ bị lỗi hoặc phản hồi chậm, nó có thể tạo ra hiệu ứng domino trong toàn bộ chuỗi microservices.

**Ví Dụ Tình Huống:**
- Ứng dụng client gọi REST API trong microservice accounts
- Microservice accounts giao tiếp với các microservice loans và cards
- Nếu microservice loans hoặc cards bị lỗi hoặc phản hồi chậm, microservice accounts sẽ tiếp tục chờ đợi
- Việc chờ đợi này tiêu tốn threads và bộ nhớ trong các dịch vụ phụ thuộc (accounts, gateway server)
- Cuối cùng, toàn bộ chuỗi microservices có thể bị lỗi

**Thách Thức:**
Làm thế nào để đảm bảo rằng một microservice bị lỗi không làm sập toàn bộ mạng lưới microservices?

### 2. Xử Lý Lỗi Một Cách Linh Hoạt với Fallback

**Vấn Đề:**
Khi nhiều microservices cộng tác để phục vụ yêu cầu từ client, chúng ta cần một cơ chế để xử lý các lỗi một phần một cách linh hoạt.

**Ví Dụ Tình Huống:**
- Nếu microservice cards không hoạt động đúng cách
- Thay vì trả về exception cho client
- Chúng ta nên triển khai fallback để trả về ít nhất là thông tin accounts và loans

**Các Cơ Chế Fallback:**
- Trả về giá trị mặc định
- Trả về dữ liệu từ cache
- Gọi một dịch vụ thay thế
- Lấy dữ liệu từ database khác

**Mục Tiêu:**
Đảm bảo rằng lỗi của một microservice đơn lẻ không làm thất bại toàn bộ yêu cầu từ client.

### 3. Khả Năng Tự Phục Hồi (Self-Healing)

**Vấn Đề:**
Các dịch vụ có thể phản hồi chậm hoặc tạm thời bị lỗi do sự cố mạng, vấn đề hiệu suất hoặc sự cố tạm thời. Chúng ta cần các cơ chế để cho phép dịch vụ có thời gian phục hồi.

**Các Chiến Lược Tự Phục Hồi:**
- **Timeouts:** Giải phóng threads và bộ nhớ nhanh chóng thay vì chờ đợi vô thời hạn
- **Retries:** Thử lại yêu cầu nhiều lần (ví dụ: 3-4 lần) để cho phép phục hồi sau sự cố tạm thời
- **Thời Gian Phục Hồi:** Cho các dịch vụ bị lỗi thời gian để ổn định và trở lại hoạt động bình thường

## Giải Pháp: Resilience4j

### Bối Cảnh Lịch Sử

**Ngữ Cảnh Lịch Sử:**
- **Hystrix:** Trước đây, hệ sinh thái Java sử dụng thư viện Hystrix của Netflix để triển khai các pattern resiliency
- **Chế Độ Bảo Trì:** Hystrix vào chế độ bảo trì vào năm 2018 và không còn được phát triển tích cực
- **Resilience4j:** Xuất hiện như người kế nhiệm, nhanh chóng trở nên phổ biến

### Resilience4j Là Gì?

Resilience4j là một thư viện chịu lỗi nhẹ được thiết kế đặc biệt cho lập trình hàm (functional programming) (mặc dù nó cũng hoạt động với các chương trình không hàm). Nó cung cấp nhiều pattern để làm cho các ứng dụng và microservices có khả năng chịu lỗi và phục hồi.

### Các Pattern Resilience Cốt Lõi

Resilience4j cung cấp một số pattern chính:

1. **Circuit Breaker:** Ngăn chặn lỗi lan truyền bằng cách dừng các yêu cầu đến dịch vụ đang bị lỗi
2. **Fallback:** Cung cấp các phản hồi thay thế khi một dịch vụ bị lỗi
3. **Retry:** Tự động thử lại các yêu cầu bị lỗi
4. **Rate Limiter:** Kiểm soát tốc độ yêu cầu để ngăn quá tải
5. **Bulkhead:** Cô lập tài nguyên để ngăn một dịch vụ bị lỗi làm cạn kiệt tất cả tài nguyên
6. **Time Limiter:** Đặt timeout cho các hoạt động
7. **Cache:** Lưu cache các phản hồi để giảm tải

## Triển Khai Trong Spring Boot

### Hỗ Trợ Framework

Resilience4j hỗ trợ nhiều framework Java:
- **Spring Boot 2 và 3:** Tích hợp đầy đủ với các ứng dụng Spring Boot
- **Spring Reactor:** Hỗ trợ lập trình reactive
- **Spring Cloud:** Tích hợp cho microservices cloud-native
- **Micronaut:** Hỗ trợ framework Micronaut

### Bắt Đầu

Website chính thức của Resilience4j (https://resilience4j.readme.io) cung cấp:
- Tài liệu toàn diện cho từng pattern
- Hướng dẫn bắt đầu cho các framework khác nhau
- Spring Boot starter dependencies
- Các ví dụ cấu hình

## Best Practices

1. **Chọn Pattern Phù Hợp:** Lựa chọn các pattern resilience dựa trên yêu cầu kinh doanh cụ thể của bạn
2. **Kết Hợp Các Pattern:** Sử dụng nhiều pattern cùng nhau (ví dụ: circuit breaker + fallback + retry)
3. **Cấu Hình Phù Hợp:** Đặt timeout, số lần retry và ngưỡng dựa trên đặc điểm dịch vụ của bạn
4. **Giám Sát và Điều Chỉnh:** Liên tục giám sát các metrics resilience và điều chỉnh cấu hình khi cần thiết

## Kết Luận

Xây dựng microservices có khả năng phục hồi là điều cần thiết cho các ứng dụng sẵn sàng production. Resilience4j cung cấp một bộ công cụ toàn diện các pattern để xử lý lỗi một cách linh hoạt, ngăn chặn lỗi lan truyền và cho phép khả năng tự phục hồi. Bằng cách triển khai các pattern này, chúng ta có thể đảm bảo mạng lưới microservices của mình vẫn ổn định và đáng tin cậy ngay cả khi các dịch vụ riêng lẻ gặp thách thức.

## Các Bước Tiếp Theo

Trong phần này, chúng ta sẽ:
- Tìm hiểu sâu về từng pattern resilience
- Triển khai các ví dụ thực tế trong Spring Boot microservices
- Cấu hình và kiểm tra các cơ chế resilience
- Áp dụng các pattern này vào các tình huống thực tế

## Tài Nguyên

- **Website Chính Thức:** https://resilience4j.readme.io
- **Tài Liệu Core Modules:** Có sẵn trên website chính thức
- **Hướng Dẫn Tích Hợp Spring Boot:** Phần getting started trên website



================================================================================
FILE: 42-microservices-resiliency-and-circuit-breaker-pattern.md
================================================================================

# Khả Năng Phục Hồi của Microservices và Mô Hình Circuit Breaker

## Tổng Quan

Tài liệu này thảo luận về khả năng chịu lỗi và các mô hình phục hồi trong kiến trúc microservices, tập trung vào mô hình Circuit Breaker để xử lý các lỗi lan truyền.

## Giới Thiệu về Khả Năng Phục Hồi trong Microservices

Khả năng phục hồi là yếu tố quan trọng trong kiến trúc microservices để đảm bảo rằng sự cố của một dịch vụ không tạo ra hiệu ứng gợn sóng trên toàn bộ hệ thống. Hiểu về khả năng chịu lỗi giúp chúng ta xây dựng các microservices mạnh mẽ có thể xử lý các thách thức vận hành hàng ngày.

## Kịch Bản Điển Hình của Microservice

### Các Thành Phần Kiến Trúc

Trong một mạng lưới microservices điển hình, chúng ta có:

- **Edge Server / API Gateway**: Nhận lưu lượng truy cập từ bên ngoài từ các client
- **Accounts Microservice**: Xử lý thông tin tài khoản và khách hàng
- **Loans Microservice**: Quản lý thông tin khoản vay
- **Cards Microservice**: Xử lý dữ liệu liên quan đến thẻ

### Luồng API fetchCustomerDetails

Hệ thống cung cấp một REST API tại đường dẫn `fetchCustomerDetails` trong accounts microservice. Khi được gọi, API này trả về thông tin khách hàng đầy đủ bao gồm:

- Chi tiết khách hàng
- Thông tin tài khoản
- Chi tiết khoản vay
- Thông tin thẻ

#### Luồng Yêu Cầu

1. **Yêu Cầu từ Client**: Client bên ngoài gửi yêu cầu đến API Gateway
2. **Chuyển Tiếp từ Gateway**: Edge server chuyển tiếp yêu cầu đến accounts microservice
3. **Điều Phối Dịch Vụ**: Accounts microservice:
   - Có quyền truy cập trực tiếp vào dữ liệu tài khoản và khách hàng
   - Gọi loans microservice để lấy chi tiết khoản vay
   - Gọi cards microservice để lấy chi tiết thẻ
4. **Tổng Hợp Phản Hồi**: Accounts microservice tổng hợp tất cả các phản hồi
5. **Trả Về Phản Hồi**: Thông tin đầy đủ được gửi lại qua edge server đến client

## Vấn Đề: Lỗi Lan Truyền

### Mô Tả Kịch Bản

Xem xét tình huống một microservice trong luồng gặp sự cố:

- **Cards microservice** gặp vấn đề
- Có thể đang xử lý quá nhiều yêu cầu
- Phản hồi rất chậm hoặc không phản hồi

### Phân Tích Tác Động

#### Kịch Bản Bình Thường
- Thời gian phản hồi mong đợi: **< 1 giây**
- Luồng dữ liệu mượt mà qua tất cả các dịch vụ

#### Kịch Bản Có Vấn Đề
- Thời gian phản hồi của Cards microservice: **> 10 giây** hoặc không có phản hồi
- Một thread trong accounts microservice chờ đợi phản hồi từ cards
- Tài nguyên hệ thống (bộ nhớ, CPU) bị phân bổ và bị khóa

### Hiệu Ứng Gợn Sóng

Khi cards microservice có vấn đề về hiệu suất, nó gây ra lỗi lan truyền:

1. **Tác Động đến Accounts Microservice**
   - Một yêu cầu chờ đợi hơn 10 giây
   - Nhiều yêu cầu tích tụ, mỗi yêu cầu đều chờ đợi
   - Các thread và tài nguyên bị tiêu thụ
   - Hiệu suất tổng thể giảm sút

2. **Tác Động đến Edge Server**
   - Accounts microservice phản hồi chậm
   - Các thread của Edge server chờ lâu hơn
   - Tiêu thụ tài nguyên tăng lên
   - Sự suy giảm hiệu suất lan rộng

3. **Tác Động Toàn Hệ Thống**
   - Tất cả lưu lượng truy cập qua edge server bị ảnh hưởng
   - Không chỉ `fetchCustomerDetails`, mà cả các API khác
   - Một microservice bị lỗi ảnh hưởng đến toàn bộ mạng lưới

## Giải Pháp: Mô Hình Circuit Breaker

Để xử lý các tình huống này và ngăn chặn lỗi lan truyền, chúng ta có thể triển khai **mô hình Circuit Breaker** - một mô hình phục hồi quan trọng trong kiến trúc microservices.

### Lợi Ích Chính

- Ngăn chặn hiệu ứng gợn sóng trong toàn bộ mạng lưới microservice
- Bảo vệ tài nguyên khỏi bị cạn kiệt
- Duy trì sự ổn định của hệ thống trong khi có lỗi cục bộ
- Cho phép giảm cấp dịch vụ một cách uyển chuyển

### Cách Hoạt Động

Mô hình Circuit Breaker sẽ được đề cập chi tiết trong các bài giảng tiếp theo, tập trung vào:

- Các trạng thái của circuit breaker (Closed, Open, Half-Open)
- Cấu hình ngưỡng lỗi
- Cài đặt timeout
- Cơ chế dự phòng (fallback)
- Chiến lược phục hồi

## Kết Luận

Hiểu về khả năng chịu lỗi và triển khai các mô hình phục hồi như Circuit Breaker là điều cần thiết để xây dựng microservices mạnh mẽ. Một lỗi dịch vụ đơn lẻ không nên làm suy yếu toàn bộ hệ thống. Bằng cách triển khai các mô hình phục hồi phù hợp, chúng ta có thể:

- Cô lập lỗi
- Ngăn chặn cạn kiệt tài nguyên
- Duy trì tính khả dụng của hệ thống
- Cung cấp trải nghiệm người dùng tốt hơn

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:

- Triển khai chi tiết mô hình Circuit Breaker
- Cấu hình và các phương pháp hay nhất
- Tích hợp với Spring Boot và Resilience4j
- Giám sát và khả năng quan sát

---

*Tài liệu này là một phần của loạt bài toàn diện về kiến trúc microservices bao gồm service discovery, API gateways và các mô hình phục hồi.*



================================================================================
FILE: 43-circuit-breaker-pattern-introduction.md
================================================================================

# Mẫu Thiết Kế Circuit Breaker Trong Microservices

## Giới Thiệu

Mẫu thiết kế Circuit Breaker là một pattern quan trọng để xây dựng các microservices có khả năng phục hồi, giúp ngăn chặn các lỗi lan truyền (cascading failures) trong hệ thống phân tán. Pattern này được lấy cảm hứng từ cầu dao điện và cung cấp chức năng bảo vệ tương tự trong kiến trúc phần mềm.

## Hiểu Về Circuit Breaker Trong Hệ Thống Điện

Trước khi đi vào triển khai phần mềm, hãy tìm hiểu khái niệm từ hệ thống điện:

- **Mục đích**: Thiết bị an toàn được thiết kế để bảo vệ mạch điện khỏi dòng điện quá mức hoặc nguy cơ cháy nổ
- **Chức năng**: Tự động ngắt khi phát hiện lỗi như ch短 mạch hoặc quá tải
- **Bảo vệ**: Ngăn chặn hư hỏng cho các thiết bị điện bằng cách dừng dòng điện trong điều kiện nguy hiểm

### Ví Dụ Tình Huống

Khi cầu dao phát hiện chập mạch hoặc quá tải, nó tự động ngắt để bảo vệ các thiết bị (như bóng đèn) khỏi bị hư hỏng. Nếu không có bảo vệ này, dòng điện quá mức sẽ chạy qua và làm hỏng các thiết bị kết nối.

## Mẫu Circuit Breaker Trong Phát Triển Phần Mềm

### Vấn Đề

Trong môi trường phân tán, các lời gọi từ xa đến các dịch vụ và tài nguyên có thể thất bại do nhiều lý do:

- Lỗi tạm thời (transient faults)
- Kết nối mạng chậm
- Vấn đề timeout
- Tài nguyên bị quá tải
- Tình trạng không khả dụng tạm thời

**Quan trọng**: Hầu hết các lỗi này đều tạm thời và thường tự khắc phục sau một khoảng thời gian ngắn.

### Cách Hoạt Động Của Circuit Breaker Pattern

Circuit Breaker pattern giám sát tất cả các lời gọi từ xa đến một dịch vụ cụ thể và thực hiện các hành vi sau:

1. **Giám sát**: Theo dõi tất cả các lời gọi đến các dịch vụ downstream (ví dụ: Cards microservice)
2. **Phát hiện**: Xác định khi một dịch vụ:
   - Mất quá nhiều thời gian để phản hồi
   - Không phản hồi
   - Gặp vấn đề về mạng
3. **Mở Circuit**: Khi phần lớn các lời gọi thất bại, circuit breaker "mở" và:
   - Dừng tất cả các yêu cầu trong tương lai đến dịch vụ bị lỗi
   - Trả về phản hồi lỗi ngay lập tức cho client
   - Ngăn chặn việc chờ đợi và lỗi lan truyền
4. **Thất Bại Nhanh**: Các ứng dụng client (như Accounts microservice và Gateway server) nhận được phản hồi lỗi ngay lập tức thay vì chờ timeout

### Luồng Ví Dụ

```
Gateway Server → Accounts Microservice → Cards Microservice (đang lỗi)
```

Khi Cards microservice bị down hoặc chậm:
- Circuit breaker phát hiện các lỗi
- Mở circuit đến Cards microservice
- Trả về lỗi ngay lập tức cho Accounts microservice
- Ngăn chặn hiệu ứng gợn sóng trên Gateway và các dịch vụ khác
- Các API khác (ví dụ: Accounts + Loans) vẫn hoạt động bình thường

## Cơ Chế Phục Hồi

Circuit breaker không chặn traffic vĩnh viễn:

1. **Thời Gian Phục Hồi**: Cho dịch vụ bị lỗi thời gian để phục hồi (30-90 giây dựa trên cấu hình)
2. **Kiểm Tra Traffic Một Phần**: Định kỳ gửi các yêu cầu giới hạn để kiểm tra xem dịch vụ đã phục hồi chưa
3. **Đóng Circuit**: Nếu traffic một phần thành công, cho phép tất cả các yêu cầu đi qua
4. **Bảo Vệ Liên Tục**: Nếu traffic một phần thất bại, giữ circuit mở thêm thời gian phục hồi

## Các Lợi Ích Chính

### 1. Thất Bại Nhanh
- Yêu cầu thất bại ngay lập tức (trong vòng 1 giây) thay vì chờ timeout (10+ giây)
- Giảm tiêu thụ tài nguyên trên các dịch vụ phụ thuộc
- Cải thiện khả năng đáp ứng tổng thể của hệ thống

### 2. Suy Giảm Tinh Tế (Graceful Degradation)
- Cho phép các cơ chế fallback cho các yêu cầu thất bại
- Cung cấp phản hồi thay thế khi dịch vụ không khả dụng
- Duy trì chức năng một phần trong thời gian gián đoạn

### 3. Phục Hồi Liền Mạch
- Cho các dịch vụ bị lỗi thời gian để phục hồi mà không có traffic đến
- Cho phép các vấn đề tạm thời (vấn đề mạng) tự giải quyết một cách tự nhiên
- Tự động tiếp tục hoạt động bình thường khi dịch vụ phục hồi

## Tóm Tắt

Mẫu Circuit Breaker là thiết yếu để xây dựng kiến trúc microservices có khả năng phục hồi. Bằng cách giám sát các lời gọi dịch vụ, phát hiện lỗi và triển khai quản lý traffic thông minh, nó:

- Ngăn chặn lỗi lan truyền trong mạng lưới microservices
- Cho phép thất bại nhanh và suy giảm tinh tế
- Hỗ trợ phục hồi tự động các dịch vụ bị lỗi tạm thời
- Duy trì sự ổn định tổng thể của hệ thống trong thời gian gián đoạn một phần

Trong các phần tiếp theo, chúng ta sẽ khám phá các chi tiết triển khai thực tế và trình diễn circuit breaker pattern trong môi trường Spring Boot microservices.



================================================================================
FILE: 44-circuit-breaker-pattern-traffic-control.md
================================================================================

# Mô Hình Circuit Breaker: Kiểm Soát Lưu Lượng Truy Cập Trong Microservices

## Tổng Quan

Mô hình Circuit Breaker là một mô hình khả năng phục hồi quan trọng giúp kiểm soát luồng traffic đến các microservices đang gặp sự cố hoặc vấn đề về hiệu suất. Mô hình này giúp ngăn chặn lỗi lan truyền trong hệ thống phân tán bằng cách giám sát và quản lý lưu lượng truy cập dựa trên tình trạng của các dịch vụ downstream.

## Cách Hoạt Động của Circuit Breaker

Mô hình Circuit Breaker không tự động giám sát tất cả microservices - nó phải được cấu hình rõ ràng cho các dịch vụ cụ thể nơi cần khả năng phục hồi. Sau khi được kích hoạt, nó kiểm soát luồng traffic bằng cách sử dụng ba trạng thái riêng biệt.

## Ba Trạng Thái của Circuit Breaker

### 1. Trạng Thái Closed (Hoạt Động Bình Thường)

- **Trạng thái ban đầu**: Khi ứng dụng khởi động, circuit breaker bắt đầu ở trạng thái closed
- **Hành vi**: Tất cả các request đến đều được phép đi qua microservice
- **So sánh**: Tương tự như mạch điện đóng nơi dòng điện chảy tự do đến các thành phần phía sau
- **Giám sát**: Circuit breaker liên tục giám sát tất cả các request, theo dõi:
  - Tỷ lệ thành công/thất bại của response
  - Các vấn đề về mạng
  - Thời gian phản hồi và độ trễ
  - Tình trạng tổng thể của microservice

### 2. Trạng Thái Open (Chế Độ Lỗi)

**Kích hoạt chuyển đổi**: Circuit breaker chuyển từ closed sang open dựa trên **ngưỡng tỷ lệ lỗi** mà bạn cấu hình. Ví dụ: nếu 50% request thất bại, mạch sẽ mở.

**Hành vi ở trạng thái Open**:
- **Không có request nào** được chuyển tiếp đến microservice đang lỗi
- Các request **thất bại ngay lập tức** với phản hồi lỗi
- Ngăn chặn hiệu ứng gợn sóng và lỗi lan truyền đến các dịch vụ gọi
- Cho microservice đang lỗi thời gian để phục hồi

**Thời gian chờ**: Circuit breaker duy trì ở trạng thái open trong khoảng thời gian đã cấu hình (ví dụ: 90 giây), cho phép microservice có thời gian để:
- Phục hồi từ các lỗi
- Giải quyết các vấn đề về mạng
- Ổn định hiệu suất

### 3. Trạng Thái Half-Open (Kiểm Tra Phục Hồi)

**Chuyển đổi**: Sau khi hết thời gian chờ, circuit breaker chuyển sang trạng thái half-open.

**Hành vi**:
- Cho phép **số lượng request thử nghiệm giới hạn** (ví dụ: 10-20 request) đi qua
- Giám sát tỷ lệ thành công của các request thử nghiệm này
- **Nếu vẫn tiếp tục lỗi** (ví dụ: ≥50% thất bại): Quay lại trạng thái open và chờ lại
- **Nếu request thành công**: Chuyển về trạng thái closed để hoạt động bình thường

**Chu trình phục hồi**: Mô hình tuần hoàn giữa open → half-open → open cho đến khi microservice xử lý thành công các request thử nghiệm, lúc đó nó quay về trạng thái closed.

## Triển Khai với Resilience4j và Spring Boot

Mặc dù mô hình circuit breaker nghe có vẻ phức tạp, nhưng việc triển khai trong microservices Spring Boot cực kỳ đơn giản khi sử dụng thư viện **Resilience4j**.

### Các Tham Số Cấu Hình Chính

- **Failure Rate Threshold**: Phần trăm lỗi kích hoạt trạng thái open (ví dụ: 50%)
- **Wait Duration**: Thời gian duy trì ở trạng thái open trước khi kiểm tra phục hồi (ví dụ: 90 giây)
- **Permitted Calls in Half-Open**: Số lượng request thử nghiệm được phép ở trạng thái half-open (ví dụ: 10-20)
- **Minimum Number of Calls**: Số request tối thiểu cần thiết trước khi tính toán tỷ lệ lỗi

## Lợi Ích

1. **Ngăn chặn lỗi lan truyền**: Dừng việc lỗi lan rộng qua hệ thống
2. **Tự động phục hồi**: Hành vi tự chữa lành thông qua cơ chế kiểm tra half-open
3. **Thất bại nhanh**: Phản hồi lỗi ngay lập tức trong thời gian ngừng hoạt động thay vì để request treo
4. **Bảo vệ tài nguyên**: Ngăn chặn việc áp đảo dịch vụ đang gặp khó khăn với các request bổ sung
5. **Ổn định hệ thống**: Duy trì tình trạng tổng thể của hệ thống bằng cách cô lập các lỗi

## Các Bước Tiếp Theo

Để triển khai mô hình circuit breaker trong microservices của bạn:

1. Thêm dependencies Resilience4j vào dự án Spring Boot của bạn
2. Cấu hình thuộc tính circuit breaker cho các dịch vụ cụ thể
3. Áp dụng annotations circuit breaker cho các phương thức service
4. Kiểm tra hành vi trong các tình huống lỗi khác nhau

## Tài Nguyên Bổ Sung

Để biết thêm thông tin chi tiết, hãy tham khảo [tài liệu chính thức của Resilience4j](https://resilience4j.readme.io/).

---

**Lưu ý**: Đảm bảo bạn hiểu rõ ba trạng thái (closed, open, half-open) và các chuyển đổi giữa chúng trước khi triển khai mô hình này trong hệ thống production. Xem lại hướng dẫn này hoặc tài liệu Resilience4j nếu có bất kỳ khái niệm nào chưa rõ ràng.



================================================================================
FILE: 45-implementing-circuit-breaker-pattern-in-spring-cloud-gateway.md
================================================================================

# Triển Khai Mẫu Thiết Kế Circuit Breaker trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai mẫu thiết kế Circuit Breaker trong kiến trúc microservices sử dụng Spring Cloud Gateway và Resilience4j. Mẫu Circuit Breaker giúp các microservices trở nên chịu lỗi và đàn hồi bằng cách ngăn chặn các lỗi lan truyền.

## Yêu Cầu Tiên Quyết

- Kiến trúc microservices Spring Boot
- Spring Cloud Gateway làm edge server
- Netflix Eureka Server cho service discovery
- Maven để quản lý dependencies
- IntelliJ IDEA (hoặc bất kỳ Java IDE nào)

## Vị Trí Triển Khai

Mẫu Circuit Breaker sẽ được triển khai ở hai cấp độ khác nhau:
1. **Gateway Server** - Đóng vai trò là edge server
2. **Các Microservices Riêng Lẻ** - Như Accounts microservice

## Bước 1: Thiết Lập Dự Án

### Tạo Thư Mục Section Mới

1. Sao chép code từ `section_9`
2. Đổi tên thư mục thành `section_10` cho các thay đổi liên quan đến resiliency
3. Xóa thư mục `.idea`
4. Mở `section_10` trong IntelliJ IDEA
5. Thực hiện clean build và bật annotation processing cho Lombok Library

## Bước 2: Thêm Dependencies

### Maven Dependency cho Gateway Server

Thêm dependency sau vào `pom.xml` của Gateway Server (sau dependency Netflix Eureka Client):

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-reactor-resilience4j</artifactId>
</dependency>
```

**Lưu ý:** Vì Gateway Server được xây dựng trên mô hình reactive Spring WebFlux, chúng ta sử dụng phiên bản `reactor-resilience4j`.

## Bước 3: Cấu Hình Circuit Breaker Filter

### Cấu Hình Gateway Server Application

Trong class main Spring Boot của Gateway Server, thêm Circuit Breaker filter vào cấu hình routing:

```java
// Trong cấu hình routing
.route(r -> r.path("/easybank/accounts/**")
    .filters(f -> f
        .rewritePath("/easybank/accounts/(?<segment>.*)", "/${segment}")
        .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
        .circuitBreaker(config -> config
            .setName("accountCircuitBreaker")
        )
    )
    .uri("lb://ACCOUNTS")
)
```

Filter `circuitBreaker` chấp nhận cấu hình lambda, nơi bạn gán tên cho instance circuit breaker.

## Bước 4: Cấu Hình Application Properties

### Thuộc Tính Circuit Breaker trong application.yml

Thêm cấu hình sau vào `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        slidingWindowSize: 10
        permittedNumberOfCallsInHalfOpenState: 2
        failureRateThreshold: 50
        waitDurationInOpenState: 10000
```

### Giải Thích Các Thuộc Tính

| Thuộc Tính | Giá Trị | Mô Tả |
|------------|---------|-------|
| `slidingWindowSize` | 10 | Số lượng requests cần giám sát trước khi quyết định chuyển trạng thái từ CLOSED sang OPEN |
| `permittedNumberOfCallsInHalfOpenState` | 2 | Số lượng requests được phép ở trạng thái HALF_OPEN để kiểm tra xem service đã phục hồi chưa |
| `failureRateThreshold` | 50 | Phần trăm requests thất bại (50%) kích hoạt circuit breaker chuyển sang trạng thái open |
| `waitDurationInOpenState` | 10000 | Thời gian chờ tính bằng milliseconds (10 giây) trước khi chuyển sang trạng thái HALF_OPEN |

### Phạm Vi Cấu Hình

- Sử dụng `default` áp dụng các thuộc tính này cho tất cả circuit breakers trong ứng dụng
- Để cấu hình circuit breakers cụ thể, thay `default` bằng tên circuit breaker (ví dụ: `accountCircuitBreaker`)

## Bước 5: Khởi Động Các Microservices

Khởi động các services theo thứ tự sau:

1. **Config Server** - Tất cả microservices phụ thuộc vào service này
2. **Eureka Server** - Cho service discovery và registration
3. **Accounts Microservice** - Service chúng ta sẽ test
4. **Gateway Server** - Để định tuyến và áp dụng logic circuit breaker

**Lưu ý:** Không cần khởi động Cards và Loans microservices cho demo này.

## Bước 6: Testing và Monitoring

### Xác Minh Eureka Dashboard

1. Mở browser đến Eureka Dashboard
2. Xác minh Accounts và Gateway Server đã đăng ký thành công

### Actuator Endpoints để Monitoring

#### Xem Tất Cả Circuit Breakers
```
GET http://localhost:8072/actuator/circuitbreakers
```

Ban đầu trả về mảng rỗng cho đến khi các requests được xử lý.

#### Xem Circuit Breaker Events
```
GET http://localhost:8072/actuator/circuitbreakerevents?name=accountCircuitBreaker
```

Hiển thị tất cả các sự kiện chuyển trạng thái và kết quả requests.

#### Xem Trạng Thái Tổng Thể Circuit Breaker
```
GET http://localhost:8072/actuator/circuitbreakers
```

Trả về trạng thái hiện tại và thống kê:
- Trạng thái tổng thể (CLOSED, OPEN, HALF_OPEN)
- Tỷ lệ thất bại
- Tỷ lệ slow call
- Buffered calls
- Failed calls

## Bước 7: Demo Các Trạng Thái Circuit Breaker

### Testing Trạng Thái CLOSED (Hoạt Động Bình Thường)

1. Gửi request qua Postman:
   ```
   GET http://localhost:8072/easybank/accounts/api/contact-info
   ```

2. Response thành công cho biết trạng thái CLOSED:
   ```json
   {
     "message": "Contact details",
     "contactDetails": {...},
     "onCallSupport": {...}
   }
   ```

3. Kiểm tra actuator endpoint - trạng thái hiển thị là `CLOSED` với zero failed calls

### Mô Phỏng Lỗi (Kích Hoạt Trạng Thái OPEN)

Để minh họa hành vi circuit breaker:

1. Đặt breakpoint trong `AccountsController` tại endpoint contact-info
2. Gửi các requests sẽ timeout (Gateway timeout sau khi chờ)
3. Response chuyển sang `504 Gateway Timeout`
4. Tiếp tục gửi nhiều failed requests

### Chuyển Trạng Thái: CLOSED → OPEN

Sau nhiều lỗi (vượt quá 50% failure rate):

1. Response chuyển sang `503 Service Unavailable`
2. Thông báo lỗi: "Upstream service is temporarily unavailable"
3. Trạng thái circuit breaker chuyển sang `OPEN`
4. Kiểm tra actuator events để xem sự kiện chuyển trạng thái

### Lợi Ích của Trạng Thái OPEN

- Gateway Server không lãng phí tài nguyên gọi service đang lỗi
- Circuit breaker ngay lập tức trả về lỗi mà không chờ đợi
- Ngăn chặn cạn kiệt tài nguyên và blocking threads
- Bảo vệ các downstream services khỏi cascading failures

### Chuyển Trạng Thái: OPEN → HALF_OPEN

Sau khi chờ 10 giây (waitDurationInOpenState):

1. Circuit breaker tự động chuyển sang `HALF_OPEN`
2. Cho phép 2 test requests (permittedNumberOfCallsInHalfOpenState)
3. Dựa trên kết quả, quyết định trạng thái tiếp theo:
   - Nếu thành công → chuyển sang `CLOSED`
   - Nếu thất bại → quay lại `OPEN`

### Chuyển Trạng Thái: HALF_OPEN → CLOSED

Để khôi phục hoạt động bình thường:

1. Xóa breakpoint khỏi AccountsController
2. Gửi requests mới
3. Responses thành công chuyển trạng thái sang `CLOSED`
4. Kiểm tra actuator events để xác nhận: chuyển HALF_OPEN → CLOSED
5. Trạng thái tổng thể quay về `CLOSED` với thống kê bình thường

## Cách Circuit Breaker Bảo Vệ Hệ Thống

### Bảo Vệ Tài Nguyên

- **Không có Circuit Breaker:** Gateway tiếp tục cố gọi service đang lỗi, blocking threads và tiêu tốn tài nguyên
- **Có Circuit Breaker:** Ngay lập tức fail fast khi service không khả dụng, giải phóng tài nguyên

### Khả Năng Chịu Lỗi

- Ngăn chặn cascading failures giữa các microservices
- Tự động phát hiện và cô lập các services đang lỗi
- Khả năng tự phục hồi thông qua kiểm tra trạng thái HALF_OPEN

### Lợi Ích Về Hiệu Năng

- Giảm latency bằng cách fail fast thay vì chờ timeouts
- Sử dụng tài nguyên tốt hơn trong Gateway Server
- Cải thiện độ ổn định tổng thể của hệ thống

## Monitoring và Observability

### Monitoring Thời Gian Thực

Sử dụng Spring Boot Actuator endpoints để giám sát:

1. **Trạng Thái Hiện Tại:** Kiểm tra xem circuit đang CLOSED, OPEN hay HALF_OPEN
2. **Lịch Sử Events:** Xem tất cả chuyển trạng thái và kết quả requests
3. **Metrics:** Theo dõi failure rates, slow call rates và buffered calls

### Ví Dụ Actuator Response

```json
{
  "accountCircuitBreaker": {
    "state": "CLOSED",
    "failureRate": 0.0,
    "slowCallRate": -1.0,
    "bufferedCalls": 3,
    "failedCalls": 0,
    "slowCalls": 0
  }
}
```

## Best Practices (Thực Hành Tốt Nhất)

1. **Cấu Hình Phù Hợp:** Điều chỉnh ngưỡng dựa trên SLAs của service
2. **Nhiều Circuit Breakers:** Sử dụng cấu hình khác nhau cho các services khác nhau
3. **Giám Sát Tích Cực:** Thiết lập alerts cho thay đổi trạng thái circuit breaker
4. **Test Kỹ Lưỡng:** Mô phỏng các kịch bản lỗi khác nhau trong testing
5. **Tài Liệu Hóa Hành Vi:** Đảm bảo team hiểu hành vi của circuit breaker

## Kết Luận

Mẫu Circuit Breaker là thiết yếu để xây dựng microservices đàn hồi. Bằng cách triển khai nó ở cấp Gateway Server sử dụng Spring Cloud Gateway và Resilience4j, bạn có thể:

- Bảo vệ hệ thống khỏi cascading failures
- Tiết kiệm tài nguyên trong thời gian service gặp sự cố
- Cung cấp trải nghiệm người dùng tốt hơn với hành vi fail-fast
- Tự động phục hồi khi services trở lại khỏe mạnh

Triển khai này minh họa sức mạnh của mẫu circuit breaker trong việc làm cho microservices chịu lỗi và đàn hồi trong môi trường production.

## Các Bước Tiếp Theo

- Triển khai Circuit Breaker ở cấp độ individual microservice
- Khám phá các mẫu Resilience4j khác (Retry, Rate Limiter, Bulkhead)
- Cấu hình cơ chế fallback để xử lý lỗi tốt hơn
- Thiết lập monitoring và alerting cho circuit breaker events



================================================================================
FILE: 46-implementing-fallback-mechanism-circuit-breaker-gateway.md
================================================================================

# Triển Khai Cơ Chế Fallback Cho Circuit Breaker Pattern Trong Gateway Server

## Tổng Quan

Hướng dẫn này giải thích cách triển khai cơ chế fallback cho circuit breaker pattern bên trong Spring Cloud Gateway server. Cơ chế fallback cung cấp xử lý lỗi mượt mà thay vì ném các runtime exception đến các ứng dụng client.

## Vấn Đề

Hiện tại, khi circuit breaker được kích hoạt trong Gateway server mà không có cơ chế fallback, nó sẽ ném các runtime exception như:
- Lỗi service không khả dụng
- Lỗi gateway timeout
- Thông báo upstream service không khả dụng

Trong các ứng dụng kinh doanh thực tế, việc ném RuntimeException trực tiếp đến các ứng dụng client hoặc UI không phải là cách tiếp cận hợp lệ. Chúng ta cần một cơ chế fallback phù hợp để cung cấp các phản hồi có ý nghĩa.

## Các Bước Triển Khai

### Bước 1: Tạo Fallback Controller

1. Tạo package mới `controller` bên trong ứng dụng Gateway server
2. Tạo class `FallbackController` với annotation `@RestController`
3. Triển khai REST API endpoint cho phản hồi fallback

```java
@RestController
public class FallbackController {
    
    @RequestMapping("/contactsupport")
    public Mono<String> contactSupport() {
        return Mono.just("Đã xảy ra lỗi. Vui lòng thử lại sau hoặc liên hệ đội ngũ hỗ trợ.");
    }
}
```

**Lưu Ý Quan Trọng:**
- Vì Spring Cloud Gateway được xây dựng trên Spring Reactive, cần wrap String trả về với `Mono`
- Sử dụng `Mono.just()` để trả về thông báo phản hồi
- Tùy chỉnh logic fallback dựa trên yêu cầu nghiệp vụ (ví dụ: kích hoạt email, trả về phản hồi mặc định)

### Bước 2: Cấu Hình Fallback URI Trong Circuit Breaker

Thêm cấu hình fallback URI vào circuit breaker pattern trong ứng dụng Gateway server:

```java
.setFallbackUri("forward:/contactsupport")
```

Cấu hình này cho circuit breaker pattern biết cần chuyển tiếp request đến endpoint `/contactsupport` bất cứ khi nào có exception xảy ra.

### Bước 3: Build Và Test

1. Lưu các thay đổi và build ứng dụng
2. Test với Postman hoặc bất kỳ REST client nào

## Các Kịch Bản Kiểm Thử

### Luồng Request Thành Công
- Gửi request đến service
- Xác minh phản hồi thành công từ microservice thực tế
- Cơ chế fallback **không được gọi**
- Trạng thái circuit breaker hiển thị là **CLOSED**

### Mô Phỏng Phản Hồi Chậm
1. Đặt breakpoint trong accounts controller để mô phỏng phản hồi chậm
2. Gửi request - nó sẽ dừng tại breakpoint
3. Thay vì nhận "gateway timeout" hoặc "upstream service unavailable", client nhận được:
   ```
   Đã xảy ra lỗi. Vui lòng thử lại sau hoặc liên hệ đội ngũ hỗ trợ.
   ```
4. Các ứng dụng client không bao giờ biết điều gì đang xảy ra đằng sau
5. Giải phóng breakpoint - các request thành công tiếp theo sẽ bỏ qua fallback

## Tóm Tắt Các Bước Triển Khai

### 1. Thêm Maven Dependency
Thêm dependency Circuit Breaker vào `pom.xml` của Gateway Server

### 2. Cấu Hình Circuit Breaker Filter
Gọi circuit breaker filter nội bộ và định nghĩa:
- Tên circuit breaker
- Fallback URI

### 3. Cấu Hình Properties Trong application.yml
Thiết lập các thuộc tính circuit breaker sau:
- `slidingWindowSize` - Số lượng cuộc gọi cần theo dõi
- `permittedNumberOfCallsInHalfOpenState` - Số cuộc gọi được phép ở trạng thái half-open
- `failureRateThreshold` - Ngưỡng phần trăm để mở circuit
- `waitDurationInOpenState` - Thời gian chờ trước khi chuyển sang trạng thái half-open

## Lợi Ích

- **Xử Lý Lỗi Mượt Mà**: Ứng dụng client nhận được thông báo lỗi có ý nghĩa
- **Trải Nghiệm Người Dùng Tốt Hơn**: Không có runtime exception khó hiểu được hiển thị cho người dùng cuối
- **Tính Linh Hoạt**: Dễ dàng tùy chỉnh logic fallback dựa trên yêu cầu nghiệp vụ
- **Tính Minh Bạch**: Các vấn đề backend được ẩn khỏi ứng dụng client

## Các Bước Tiếp Theo

Chủ đề tiếp theo sẽ đề cập đến việc triển khai circuit breaker pattern bên trong các microservice riêng lẻ, chẳng hạn như accounts microservice, thay vì chỉ ở cấp độ gateway.

## Những Điểm Chính

- Cơ chế fallback là thiết yếu cho việc triển khai circuit breaker sẵn sàng cho production
- Spring Cloud Gateway sử dụng lập trình reactive (Mono/Flux)
- Fallback REST API chỉ thực thi khi có exception xảy ra
- Cấu hình circuit breaker là khai báo và dễ bảo trì



================================================================================
FILE: 47-implementing-circuit-breaker-pattern-in-accounts-microservice.md
================================================================================

# Triển Khai Circuit Breaker Pattern trong Accounts Microservice

## Tổng Quan

Hướng dẫn này trình bày cách triển khai circuit breaker pattern trong accounts microservice sử dụng Spring Cloud Circuit Breaker với tích hợp Resilience4j và OpenFeign.

## Vấn Đề

Accounts microservice có một REST API tên là `fetchCustomerDetails` gọi đến cả cards và loans microservices. Khi một trong các dịch vụ phụ thuộc này:
- Phản hồi rất chậm
- Hoàn toàn ngừng hoạt động
- Có vấn đề về mạng

Điều này tạo ra hiệu ứng domino ảnh hưởng đến accounts microservice và sau đó là Gateway server, có thể gây ra các lỗi liên hoàn.

## Giải Pháp: Circuit Breaker Pattern với Feign Client

Spring Cloud OpenFeign cung cấp tích hợp sẵn với circuit breaker pattern, cho phép chúng ta triển khai khả năng phục hồi với cấu hình tối thiểu.

### Bước 1: Thêm Circuit Breaker Dependency

Thêm dependency Spring Cloud Circuit Breaker Resilience4j vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
</dependency>
```

**Lưu ý:** Sử dụng `spring-cloud-starter-circuitbreaker-resilience4j` (không phải phiên bản reactive) vì accounts microservice không được xây dựng trên Spring Reactor.

### Bước 2: Kích Hoạt Circuit Breaker trong Cấu Hình

Thêm thuộc tính sau vào file `application.yml`:

```yaml
spring:
  cloud:
    openfeign:
      circuitbreaker:
        enabled: true
```

Cấu hình này kích hoạt circuit breaker cho tất cả OpenFeign clients trong accounts microservice.

### Bước 3: Thêm Các Thuộc Tính Resilience4j Bổ Sung

Bao gồm các thuộc tính cấu hình Resilience4j giống như đã sử dụng trong gateway server (kích thước cửa sổ trượt, ngưỡng tỷ lệ lỗi, thời gian chờ, v.v.).

### Bước 4: Tạo Các Fallback Classes

#### LoansFallback Class

Tạo một fallback class triển khai interface `LoansFeignClient`:

```java
@Component
public class LoansFallback implements LoansFeignClient {
    
    @Override
    public ResponseEntity<LoansDto> fetchLoanDetails(String correlationId) {
        return null;
    }
}
```

#### CardsFallback Class

Tương tự, tạo fallback class cho cards microservice:

```java
@Component
public class CardsFallback implements CardsFeignClient {
    
    @Override
    public ResponseEntity<CardsDto> fetchCardDetails(String correlationId) {
        return null;
    }
}
```

**Logic Nghiệp Vụ:** Các phương thức fallback trả về `null` thay vì ném RuntimeException. Trong môi trường production, bạn có thể:
- Trả về giá trị được lưu trong cache
- Lấy dữ liệu từ cơ sở dữ liệu thay thế
- Trả về giá trị mặc định
- Triển khai bất kỳ logic nghiệp vụ tùy chỉnh nào

### Bước 5: Cấu Hình Fallback trong Feign Clients

#### LoansFeignClient Interface

```java
@FeignClient(name = "loans", fallback = LoansFallback.class)
public interface LoansFeignClient {
    // định nghĩa các phương thức
}
```

#### CardsFeignClient Interface

```java
@FeignClient(name = "cards", fallback = CardsFallback.class)
public interface CardsFeignClient {
    // định nghĩa các phương thức
}
```

### Bước 6: Thêm Kiểm Tra Null trong Service Layer

Cập nhật `CustomerServiceImpl` để xử lý các phản hồi null tiềm năng từ các phương thức fallback:

```java
// Đối với Loans
ResponseEntity<LoansDto> loansResponseEntity = loansFeignClient.fetchLoanDetails(correlationId);
if (loansResponseEntity != null) {
    customerDetailsDto.setLoansDto(loansResponseEntity.getBody());
}

// Đối với Cards
ResponseEntity<CardsDto> cardsResponseEntity = cardsFeignClient.fetchCardDetails(correlationId);
if (cardsResponseEntity != null) {
    customerDetailsDto.setCardsDto(cardsResponseEntity.getBody());
}
```

## Lợi Ích

1. **Giảm Tải Nhẹ Nhàng:** Khi một microservice ngừng hoạt động, ứng dụng tiếp tục cung cấp dữ liệu một phần thay vì lỗi hoàn toàn
2. **Cải Thiện Trải Nghiệm Người Dùng:** Clients nhận được dữ liệu accounts và các microservice khả dụng ngay cả khi một dịch vụ bị lỗi
3. **Ngăn Chặn Lỗi Liên Hoàn:** Circuit breaker ngăn chặn hiệu ứng domino từ các lỗi dịch vụ phụ thuộc
4. **Cấu Hình Tối Thiểu:** Tận dụng tích hợp sẵn giữa Feign và Circuit Breaker

## Những Điểm Chính

- Spring Cloud OpenFeign tự động bao bọc tất cả các phương thức với circuit breaker khi được cấu hình đúng cách
- Fallback classes phải triển khai cùng interface với Feign client
- Luôn thêm kiểm tra null khi làm việc với cơ chế fallback
- Circuit breaker pattern là thiết yếu để xây dựng microservices có khả năng phục hồi
- Logic fallback cung cấp sự linh hoạt để triển khai các yêu cầu nghiệp vụ tùy chỉnh

## Tài Liệu Tham Khảo

- Tài liệu Spring Cloud OpenFeign
- Hỗ trợ Spring Cloud Circuit Breaker
- Hướng dẫn tích hợp Resilience4j



================================================================================
FILE: 48-circuit-breaker-demo-implementation-guide.md
================================================================================

# Hướng Dẫn Triển Khai Circuit Breaker Pattern với Spring Boot

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra Circuit Breaker pattern trong kiến trúc microservices sử dụng Spring Boot, Resilience4j, và OpenFeign. Circuit Breaker pattern giúp xây dựng các microservices có khả năng phục hồi bằng cách ngăn chặn lỗi lan truyền và cung cấp cơ chế giảm tải nhẹ nhàng.

## Thiết Lập Kiến Trúc

Môi trường demo bao gồm các microservices sau:

1. **Config Server** - Quản lý cấu hình tập trung
2. **Eureka Server** - Khám phá và đăng ký dịch vụ
3. **Gateway Server** - API Gateway để định tuyến yêu cầu
4. **Accounts Microservice** (Port 8080) - Dịch vụ chính có triển khai circuit breaker
5. **Cards Microservice** - Dịch vụ phụ thuộc cho thông tin thẻ
6. **Loans Microservice** - Dịch vụ phụ thuộc cho thông tin khoản vay

Tất cả microservices được đăng ký với Eureka server và có thể xác minh qua Eureka dashboard.

## Giám Sát Trạng Thái Circuit Breaker

### Các Endpoint Actuator

Spring Boot Actuator cung cấp giám sát thời gian thực của circuit breakers:

- **Trạng thái Circuit Breakers**: `/actuator/circuitbreakers`
- **Sự kiện Circuit Breaker**: `/actuator/circuitbreakerevents`

### Trạng Thái Ban Đầu

Trước khi gửi request đầu tiên, không có circuit breakers nào hiển thị trong các endpoint actuator. Circuit breakers chỉ được tạo và kích hoạt khi request đầu tiên đi qua hệ thống.

### Quy Ước Đặt Tên Circuit Breaker

Circuit breakers tuân theo mẫu đặt tên này:
```
<TênInterface>.<TênMethod>(<KiểuThamSố1>, <KiểuThamSố2>, ...)
```

**Ví dụ:**
- `cardFeignClient.fetchCardDetails(String, String)`
- `loansFeignClient.fetchLoanDetails(String, String)`

## Hướng Dẫn Demo

### Kịch Bản Thành Công

1. **Tạo Dữ Liệu Test**
   - Tạo dữ liệu accounts qua POST request
   - Tạo dữ liệu cards với cùng số điện thoại
   - Tạo dữ liệu loans với cùng số điện thoại

2. **Lấy Thông Tin Chi Tiết Khách Hàng**
   - Request: `GET /fetchCustomerDetails`
   - Response: Trả về dữ liệu khách hàng đầy đủ bao gồm accounts, cards và loans
   - Trạng thái Circuit Breaker: `CLOSED` cho cả cardFeignClient và loansFeignClient

3. **Xác Minh Qua Actuator**
   - Hai circuit breakers được tạo tự động
   - Cả hai hiển thị trạng thái: `CLOSED`
   - Events hiển thị: Request đơn lẻ với loại `SUCCESS`

### Kịch Bản Lỗi - Loans Microservice Ngừng Hoạt Động

1. **Dừng Loans Microservice**
   - Mô phỏng lỗi dịch vụ bằng cách dừng ứng dụng loans

2. **Hành Vi Request**
   - Request: `GET /fetchCustomerDetails`
   - Response: 
     - ✅ Dữ liệu Accounts: Thành công
     - ✅ Dữ liệu Cards: Thành công
     - ❌ Dữ liệu Loans: `null` (fallback được kích hoạt)

3. **Chuyển Đổi Trạng Thái Circuit Breaker**
   - Sau nhiều request thất bại, loans circuit breaker chuyển từ `CLOSED` sang `OPEN`
   - Actuator events hiển thị: `FAILURE_RATE_EXCEEDED`
   - Chuyển đổi trạng thái: `CLOSED → OPEN`

### Kịch Bản Lỗi - Nhiều Dịch Vụ Ngừng Hoạt Động

1. **Dừng Cả Cards và Loans Microservices**
   - Mô phỏng nhiều dịch vụ phụ thuộc bị lỗi

2. **Hành Vi Request**
   - Request: `GET /fetchCustomerDetails`
   - Response:
     - ✅ Dữ liệu Accounts: Thành công
     - ❌ Dữ liệu Cards: `null` (fallback được kích hoạt)
     - ❌ Dữ liệu Loans: `null` (fallback được kích hoạt)

3. **Trạng Thái Circuit Breakers**
   - Cả hai circuit breakers chuyển sang trạng thái `OPEN`
   - Events hiển thị: Trạng thái `NOT_PERMITTED` cho cả hai dịch vụ
   - Gateway và Accounts microservice tiếp tục hoạt động mà không bị ảnh hưởng lan truyền

## Ví Dụ Thực Tế: Trang Web Amazon

Xem xét kịch bản trang chủ Amazon:

- **Nhiều microservices** làm việc cùng nhau để hiển thị thông tin:
  - Danh sách sản phẩm
  - Giảm giá và banner
  - Gợi ý dựa trên lịch sử đơn hàng

- **Giảm Tải Nhẹ Nhàng**: Nếu microservice gợi ý bị lỗi:
  - ✅ Trang chủ vẫn hoạt động bình thường
  - ✅ Sản phẩm, banner và giảm giá vẫn hiển thị
  - ❌ Chỉ phần gợi ý bị ẩn
  - ✅ Người dùng có thể tiếp tục duyệt web một cách liền mạch

Cách tiếp cận này đảm bảo **trải nghiệm khả thi tối thiểu** thay vì lỗi hoàn toàn.

## Các Bước Triển Khai

### Bước 1: Thêm Dependency

Thêm dependency Resilience4j vào `pom.xml`:

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot2</artifactId>
</dependency>
```

### Bước 2: Cấu Hình Feign Client Interface

Thêm cấu hình fallback vào các Feign client interfaces:

```java
@FeignClient(name = "cards-service", fallback = CardsFallback.class)
public interface CardFeignClient {
    @GetMapping("/api/cards")
    CardsDto fetchCardDetails(@RequestParam String mobileNumber);
}
```

### Bước 3: Triển Khai Fallback Bean

Tạo fallback implementation cho mỗi Feign client:

```java
@Component
public class CardsFallback implements CardFeignClient {
    @Override
    public CardsDto fetchCardDetails(String mobileNumber) {
        // Trả về null hoặc response mặc định
        return null;
    }
}
```

### Bước 4: Cấu Hình Properties

Định nghĩa các thuộc tính circuit breaker trong `application.yml`:

```yaml
resilience4j:
  circuitbreaker:
    instances:
      cardsService:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        permittedNumberOfCallsInHalfOpenState: 3
        waitDurationInOpenState: 10s
        failureRateThreshold: 50
```

## Các Trạng Thái Circuit Breaker

1. **CLOSED**: Hoạt động bình thường, requests được xử lý
2. **OPEN**: Dịch vụ đang lỗi, requests bị chặn và fallback được gọi
3. **HALF_OPEN**: Kiểm tra xem dịch vụ đã phục hồi chưa

## Quy Trình Phục Hồi

Khi các microservices phụ thuộc (cards và loans) được khởi động lại và bắt đầu phản hồi thành công:
- Circuit breakers tự động phát hiện các phản hồi thành công
- Trạng thái chuyển từ `OPEN` về `CLOSED`
- Hoạt động bình thường được tiếp tục

## Lợi Ích Chính

✅ **Ngăn Chặn Lỗi Lan Truyền**: Cô lập các dịch vụ bị lỗi
✅ **Giảm Tải Nhẹ Nhàng**: Cung cấp chức năng một phần thay vì lỗi hoàn toàn
✅ **Cải Thiện Trải Nghiệm Người Dùng**: Người dùng nhận được một số dữ liệu thay vì lỗi
✅ **Khả Năng Phục Hồi Hệ Thống**: Gateway và các dịch vụ khác không bị ảnh hưởng
✅ **Tự Động Phục Hồi**: Circuit breakers tự chữa lành khi dịch vụ phục hồi

## Kết Luận

Circuit Breaker pattern là yếu tố thiết yếu để xây dựng kiến trúc microservices có khả năng phục hồi. Bằng cách triển khai nó với Resilience4j và OpenFeign, bạn có thể đảm bảo hệ thống của mình xử lý lỗi một cách nhẹ nhàng và cung cấp trải nghiệm tốt nhất có thể cho người dùng cuối.

## Bước Tiếp Theo

Khám phá các resilience patterns khác được cung cấp bởi Resilience4j:
- Retry Pattern (Mẫu Thử Lại)
- Rate Limiter (Giới Hạn Tốc Độ)
- Bulkhead Pattern (Mẫu Ngăn Khoang)
- Time Limiter (Giới Hạn Thời Gian)

---

*Hướng dẫn này dựa trên demo thực tế về triển khai Circuit Breaker pattern trong Spring Boot microservices.*



================================================================================
FILE: 49-configuring-timeout-in-spring-cloud-gateway.md
================================================================================

# Cấu Hình Timeout trong Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình timeout trong Spring Cloud Gateway để ngăn chặn các microservice chờ đợi phản hồi vô thời hạn, điều này có thể dẫn đến cạn kiệt tài nguyên và các vấn đề về hiệu suất.

## Vấn Đề

Khi các microservice phản hồi chậm hoặc bị treo, các ứng dụng client và gateway server có thể lãng phí tài nguyên quý giá (thread, bộ nhớ) để chờ đợi các phản hồi có thể không bao giờ đến. Nếu không có cấu hình timeout phù hợp:

- Các thread bị chặn vô thời hạn
- Tài nguyên server bị tiêu thụ không cần thiết
- Ứng dụng client có trải nghiệm người dùng kém
- Hiệu suất hệ thống giảm sút theo thời gian

### Kịch Bản Minh Họa

Khi gọi endpoint `contact-info` trong `LoansController`:
- Không có timeout: Ứng dụng chờ đợi vô thời hạn (có thể hàng phút)
- Với circuit breaker (AccountsController): Tự động timeout sau 1 giây và chuyển sang fallback
- Hành vi khác nhau tùy thuộc vào việc có triển khai Circuit Breaker pattern hay không

## Giải Pháp: Cấu Hình HTTP Timeout

Spring Cloud Gateway cung cấp hai loại cấu hình timeout:

### 1. Connection Timeout
Thời gian tối đa mà gateway server chờ để thiết lập kết nối với microservice đích.

**Trường hợp sử dụng**: Xử lý vấn đề mạng hoặc khi microservice không thể truy cập được.

### 2. Response Timeout
Thời gian tối đa mà gateway server chờ để nhận phản hồi hoàn chỉnh từ microservice.

**Trường hợp sử dụng**: Xử lý các service phản hồi chậm hoặc bị treo trong quá trình xử lý.

## Triển Khai

### Cấu Hình Timeout Toàn Cục

Thêm các thuộc tính sau vào file `application.yml` của Gateway server:

```yaml
spring:
  cloud:
    gateway:
      httpclient:
        connect-timeout: 1000        # 1 giây (đơn vị milliseconds)
        response-timeout: 2s         # 2 giây
```

**Chi Tiết Cấu Hình:**
- `connect-timeout`: 1000ms (1 giây) - Thời gian để thiết lập kết nối
- `response-timeout`: 2s - Thời gian chờ tối đa cho phản hồi

Các cài đặt toàn cục này áp dụng cho tất cả các microservice được định tuyến qua Gateway server.

### Cấu Hình Timeout Theo Từng Route

Để cấu hình timeout riêng cho từng route:

#### Sử Dụng Java DSL

```java
.route(r -> r.path("/api/loans/**")
    .metadata("response-timeout", 5000)
    .metadata("connect-timeout", 2000)
    .uri("lb://LOANS"))
```

#### Sử Dụng application.yml

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: loans-service
          uri: lb://LOANS
          metadata:
            response-timeout: 5000
            connect-timeout: 2000
```

### Vô Hiệu Hóa Timeout Cho Route Cụ Thể

Để vô hiệu hóa cấu hình timeout toàn cục cho một route cụ thể, đặt response timeout thành giá trị âm:

```yaml
metadata:
  response-timeout: -1  # Vô hiệu hóa timeout - chờ đợi vô thời hạn
```

**Cảnh báo**: Sử dụng cẩn thận vì có thể dẫn đến cạn kiệt tài nguyên.

## Hành Vi Với Circuit Breaker

Khi Circuit Breaker pattern được cấu hình (ví dụ: cho Accounts microservice):
- Timeout nội bộ của Circuit Breaker (mặc định: 1 giây) được ưu tiên
- Cấu hình timeout toàn cục của gateway bị bỏ qua
- Cơ chế fallback được kích hoạt khi xảy ra timeout
- Cấu hình timeout của Circuit Breaker có thể được ghi đè riêng biệt

## Kiểm Tra Cấu Hình

### Trước Khi Cấu Hình Timeout
1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Postman
3. Kết quả: Client chờ đợi vô thời hạn (ví dụ: hơn 2 phút)

### Sau Khi Cấu Hình Timeout
1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Postman
3. Kết quả: Lỗi "Gateway Timeout" sau 2 giây

## Thực Hành Tốt Nhất

1. **Luôn Cấu Hình Timeout**: Không bao giờ để microservice không có cấu hình timeout
2. **Điều Chỉnh Theo Yêu Cầu Nghiệp Vụ**: Đặt giá trị timeout phù hợp với trường hợp sử dụng của bạn
3. **Xem Xét Đặc Điểm Service**: Các service khác nhau có thể yêu cầu giá trị timeout khác nhau
4. **Giám Sát và Tinh Chỉnh**: Thường xuyên xem xét và điều chỉnh giá trị timeout dựa trên các chỉ số hiệu suất
5. **Sử Dụng Circuit Breaker**: Kết hợp timeout với Circuit Breaker pattern để có khả năng phục hồi tốt hơn

## Điểm Chính Cần Nhớ

- Cấu hình timeout ngăn ngừa cạn kiệt tài nguyên trong kiến trúc microservices
- Spring Cloud Gateway hỗ trợ cả cấu hình timeout toàn cục và theo từng route
- Connection timeout xử lý vấn đề thiết lập kết nối
- Response timeout xử lý phản hồi chậm hoặc bị treo
- Cấu hình timeout của Circuit Breaker ghi đè timeout toàn cục của gateway
- Cấu hình timeout phù hợp là thiết yếu cho microservices sẵn sàng triển khai production

## Các Pattern Liên Quan

- Circuit Breaker Pattern
- Fallback Mechanism
- Service Discovery
- API Gateway Design Patterns

## Tài Liệu Tham Khảo Thêm

Tham khảo tài liệu chính thức của Spring Cloud Gateway để biết:
- Các tùy chọn cấu hình timeout bổ sung
- Cấu hình định tuyến nâng cao
- Triển khai custom filter
- Tích hợp circuit breaker

---

*Hướng dẫn này minh họa tầm quan trọng của cấu hình timeout trong việc xây dựng microservices có khả năng phục hồi và hiệu suất cao với Spring Cloud Gateway.*



================================================================================
FILE: 5-docker-network-isolation-and-database-migration-strategy.md
================================================================================

# Cô Lập Mạng Docker và Chiến Lược Di Chuyển Cơ Sở Dữ Liệu

## Tổng Quan

Bài giảng này trình bày các khái niệm về mạng Docker và giải thích quyết định chiến lược di chuyển từ MySQL sang cơ sở dữ liệu H2 cho môi trường phát triển trong kiến trúc microservices.

## Minh Họa Mạng Docker

### Cấu Hình Mạng Hiện Tại

Tất cả microservices và containers hiện đang được cấu hình để chạy trong cùng một mạng Docker có tên **EazyBank**. Điều này đạt được thông qua cấu hình `network-deploy-service` mà tất cả các services đều kế thừa.

### Kiểm Tra Cô Lập Mạng

Để minh họa cô lập mạng:

1. **Tách Container Cơ Sở Dữ Liệu**: Loại bỏ cấu hình mạng khỏi các database containers bằng cách sửa file `common-config.yaml`
2. **Kết Quả Mong Đợi**: Microservices sẽ không thể giao tiếp với database containers
3. **Xác Thực**: Sử dụng profile QA để kiểm tra kịch bản này

### Các Lệnh Chính

```bash
# Dừng tất cả containers đang chạy
docker compose down

# Khởi động containers với profile QA
docker compose up -d

# Liệt kê các mạng Docker
docker network ls

# Kiểm tra mạng của container
docker inspect <container-id>
```

### Hành Vi Quan Sát Được

Khi databases bị tách khỏi mạng EazyBank:
- Các database containers (loans, accounts, cards) khởi động thành công
- Config server microservice khởi động thành công
- Các application microservices (accounts, loans, cards) ban đầu khởi động nhưng sau đó thoát
- Xảy ra lỗi kết nối vì các containers nằm trên các mạng khác nhau

### Kiến Trúc Mạng

- **Mạng Mặc Định**: Khi không chỉ định mạng, Docker Compose gán containers vào mạng `qa_default`
- **Mạng Tùy Chỉnh**: Microservices được cấu hình sử dụng mạng EazyBank
- **Nguyên Tắc Cô Lập**: Các containers trên các mạng khác nhau không thể giao tiếp trừ khi được cấu hình rõ ràng

## Di Chuyển từ MySQL sang Cơ Sở Dữ Liệu H2

### Thách Thức Kiến Trúc Hiện Tại

Hiện tại, cấu hình Docker Compose bao gồm:
- 3 database containers (các instances MySQL)
- 1 config server
- 3 microservices (accounts, loans, cards)
- **Tổng cộng: 7 containers đang chạy**

### Mối Quan Ngại về Mở Rộng Tương Lai

Các thành phần bổ sung sẽ được thêm vào:
- Eureka Server
- Gateway Server
- Grafana monitoring containers
- Các cơ sở hạ tầng microservices khác

**Kết Quả Dự Kiến**: 10-12+ containers chạy đồng thời

### Cân Nhắc về Hiệu Suất

**Vấn Đề**: Chạy nhiều containers đồng thời gây ra:
- Hệ thống chậm đáng kể
- Các vấn đề runtime tiềm ẩn
- Khó khăn trong debugging
- Mất động lực phát triển

**Tác Động**: Đặc biệt nghiêm trọng trên các hệ thống có 8GB RAM

### Giải Pháp: Di Chuyển sang H2 Database

**Quyết Định**: Di chuyển trở lại cơ sở dữ liệu H2 in-memory cho phát triển

**Lý Do**:
- Giảm số lượng containers (loại bỏ 3 MySQL containers)
- Cải thiện hiệu suất laptop
- Duy trì năng suất phát triển
- Ngăn chặn cạn kiệt tài nguyên hệ thống

### Tính Linh Hoạt

**Tùy Chọn cho Developers**:
- **Khuyến Nghị**: Sử dụng H2 database để có hiệu suất tối ưu
- **Thay Thế**: Tiếp tục với MySQL nếu sử dụng laptop cao cấp với đủ tài nguyên

Lựa chọn phụ thuộc vào khả năng phần cứng của bạn và sự sẵn sàng quản lý các vấn đề hiệu suất tiềm ẩn.

## Các File Cấu Hình

### Kế Thừa network-deploy-service

```yaml
microservices-db-config:
  extends:
    service: network-deploy-service
```

Cấu hình này đảm bảo tất cả containers khởi động trong mạng được chỉ định (EazyBank).

### Dọn Dẹp Biến Môi Trường

Loại bỏ các biến môi trường RabbitMQ đã lỗi thời từ:
- `common-config.yml` (profile QA)
- `common-config.yml` (profile mặc định)

## Những Điểm Chính Cần Nhớ

1. **Cô Lập Mạng Docker**: Docker cung cấp sự cô lập hoàn toàn giữa các mạng - giao tiếp chỉ hoạt động khi containers chia sẻ cùng một mạng
2. **Hiệu Suất vs Tính Năng**: Cân bằng giữa việc sử dụng cơ sở hạ tầng giống production (MySQL) và duy trì hiệu quả phát triển
3. **Quản Lý Tài Nguyên**: Cân nhắc tài nguyên hệ thống khi thiết kế môi trường phát triển local
4. **Tính Linh Hoạt**: Kiến trúc nên hỗ trợ cả cấu hình nhẹ (H2) và giống production (MySQL)

## Các Bước Tiếp Theo

Từ phần tiếp theo trở đi, khóa học sẽ sử dụng cơ sở dữ liệu H2 cho phát triển local trong khi vẫn duy trì tùy chọn sử dụng MySQL cho những người có đủ tài nguyên hệ thống.

---

**Lưu Ý**: Các nguyên tắc đã học với tích hợp MySQL database vẫn có giá trị và có thể được áp dụng khi triển khai lên môi trường production.



================================================================================
FILE: 50-retry-pattern-introduction-microservices.md
================================================================================

# Retry Pattern trong Microservices

## Giới thiệu

Retry Pattern (Mẫu Thử Lại) là một mẫu thiết kế về khả năng phục hồi cho phép các microservices xử lý các lỗi tạm thời một cách khéo léo bằng cách cấu hình nhiều lần thử lại khi một dịch vụ tạm thời không khả dụng. Mẫu này đặc biệt hữu ích trong các tình huống liên quan đến gián đoạn mạng, nơi các yêu cầu của client có thể thành công sau một lần thử lại.

## Các Cân nhắc Chính khi Triển khai Retry Pattern

### 1. Số lần Thử lại

Khi triển khai Retry Pattern, bạn phải xác định số lần thử lại một thao tác dựa trên logic nghiệp vụ của mình:
- 3 lần thử lại
- 5 lần thử lại
- 10 lần thử lại
- Hoặc bất kỳ số tùy chỉnh nào

Logic thử lại có thể được kích hoạt có điều kiện dựa trên nhiều yếu tố:
- Mã lỗi
- Ngoại lệ (Exceptions)
- Trạng thái phản hồi

### 2. Chiến lược Backoff

Khi thử lại các thao tác, nên tuân theo chiến lược backoff để tránh làm quá tải hệ thống.

#### Không có Chiến lược Backoff
- Các thao tác thử lại đơn giản với khoảng thời gian tĩnh
- Ví dụ: Thử lại mỗi 1, 2 hoặc 3 giây
- Độ trễ cố định giữa các lần thử lại

#### Có Chiến lược Backoff (Exponential Backoff - Lùi Theo Cấp số Nhân)
- Tăng dần độ trễ giữa mỗi lần thử lại
- Ví dụ về tiến trình:
  - Lần thử lại đầu tiên: sau 2 giây
  - Lần thử lại thứ hai: sau 4 giây
  - Lần thử lại thứ ba: sau 8 giây
  - Và cứ thế...

**Lợi ích:**
- Cho hệ thống thời gian để phục hồi
- Tăng khả năng nhận được phản hồi thành công
- Cho phép các vấn đề mạng tự giải quyết
- Ngăn chặn quá tải hệ thống

### 3. Tích hợp với Các Mẫu Khác

Retry Pattern có thể được kết hợp với các mẫu phục hồi khác, chẳng hạn như Circuit Breaker Pattern:
- Circuit breaker mở sau một số lần thử lại thất bại liên tiếp nhất định
- Nhiều mẫu phục hồi có thể hoạt động cùng nhau
- Tăng cường khả năng chịu lỗi và độ ổn định của hệ thống

### 4. Thao tác Idempotent

**Cân nhắc Quan trọng:** Chỉ triển khai Retry Pattern cho các thao tác idempotent.

#### Thao tác Idempotent là gì?

Các thao tác không tạo ra tác dụng phụ bất kể được gọi bao nhiêu lần.

#### An toàn cho Retry (Idempotent)
- **Thao tác GET** (API Fetch/Read)
  - Nhiều lần thử lại không gây hại
  - Luôn trả về cùng một phản hồi
  - Không sửa đổi dữ liệu

#### Không an toàn cho Retry (Không Idempotent)
- **Thao tác POST**
  - Có thể tạo nhiều bản ghi
  - Rủi ro trùng lặp dữ liệu

- **Thao tác PUT**
  - Có thể cập nhật bản ghi nhiều lần
  - Rủi ro hỏng dữ liệu
  - Các tác dụng phụ tiềm ẩn

## Thực hành Tốt nhất

1. **Xác định số lần thử lại** dựa trên yêu cầu nghiệp vụ
2. **Sử dụng exponential backoff** để tránh làm quá tải hệ thống
3. **Kết hợp với Circuit Breaker** để tăng cường khả năng phục hồi
4. **Chỉ thử lại các thao tác idempotent** để ngăn chặn hỏng dữ liệu
5. **Giám sát và ghi log** các lần thử lại để debug và phân tích

## Cảnh báo

⚠️ **Quan trọng:** Triển khai Retry Pattern trên các thao tác không idempotent có thể dẫn đến các tác dụng phụ nghiêm trọng:
- Hỏng dữ liệu
- Tạo nhiều bản ghi
- Trạng thái dữ liệu không nhất quán
- Vấn đề về tính toàn vẹn hệ thống

## Tóm tắt

Retry Pattern là một mẫu phục hồi mạnh mẽ cho microservices, đặc biệt khi xử lý các vấn đề mạng tạm thời. Bằng cách cân nhắc kỹ lưỡng số lần thử lại, triển khai chiến lược backoff phù hợp và đảm bảo các thao tác là idempotent, bạn có thể cải thiện đáng kể độ tin cậy và khả năng phục hồi của kiến trúc microservices.

## Bước tiếp theo

Trong các bài giảng tiếp theo, chúng ta sẽ triển khai Retry Pattern trong microservices bằng Spring Boot và khám phá cách kết hợp nó với các mẫu phục hồi khác để thiết kế hệ thống mạnh mẽ.



================================================================================
FILE: 51-implementing-retry-pattern-spring-cloud-gateway.md
================================================================================

# Triển Khai Retry Pattern với Spring Cloud Gateway

## Tổng Quan

Hướng dẫn này trình bày cách triển khai retry pattern (mẫu thử lại) trong kiến trúc microservices sử dụng Spring Cloud Gateway. Retry pattern giúp các microservices có khả năng chịu lỗi tốt hơn bằng cách tự động thử lại các request thất bại, đặc biệt hữu ích khi xử lý các vấn đề mạng tạm thời hoặc sự cố dịch vụ.

## Yêu Cầu Trước

- Spring Cloud Gateway đã được cấu hình
- Kiến trúc microservices với Eureka service discovery
- Hiểu biết cơ bản về circuit breaker pattern

## Các Bước Triển Khai

### 1. Cấu Hình Retry Filter trong Gateway Server

Thêm cấu hình retry filter vào ứng dụng Gateway Server sau các response header filters:

```java
.filter(f -> f
    .addResponseHeader(/* các header hiện có */)
    .retry(retryConfig -> retryConfig
        .setRetries(3)
        .setMethods(HttpMethod.GET)
        .setBackoff(100, 1000, 2, true)
    )
)
```

#### Các Tham Số Cấu Hình Chính

**setRetries(3)**
- Xác định số lần thử lại
- Trong ví dụ này: 3 lần thử lại (tổng cộng 4 requests bao gồm request ban đầu)

**setMethods(HttpMethod.GET)**
- Định nghĩa các phương thức HTTP nào được hỗ trợ retry
- **Quan trọng**: Chỉ sử dụng retry cho các thao tác idempotent (GET, DELETE)
- Tránh POST, PATCH, PUT để ngăn các tác động phụ

**setBackoff(firstBackoff, maxBackoff, factor, basedOnPreviousValue)**
- `firstBackoff` (100ms): Thời gian chờ ban đầu trước lần thử lại đầu tiên
- `maxBackoff` (1000ms): Thời gian chờ tối đa giữa các lần thử lại
- `factor` (2): Hệ số nhân áp dụng cho thời gian backoff
- `basedOnPreviousValue` (true): Áp dụng hệ số cho backoff trước đó (exponential backoff)

### 2. Hiểu Về Chiến Lược Backoff

Cấu hình backoff triển khai exponential backoff:

- **Lần thử lại 1**: Chờ 100ms
- **Lần thử lại 2**: Chờ 200ms (100ms × 2)
- **Lần thử lại 3**: Chờ 400ms (200ms × 2)
- **Chờ tối đa**: Giới hạn ở 1000ms bất kể phép tính

Điều này ngăn thời gian chờ quá lớn khi cấu hình số lần thử lại cao hơn.

### 3. Kiểm Tra Triển Khai

#### Thêm Logging vào Microservice

Trong `LoansController` hoặc microservice đích:

```java
@GetMapping("/contact-info")
public ResponseEntity<ContactInfoDto> getContactInfo() {
    logger.debug("Invoked loans contact-info API");
    // Logic nghiệp vụ của bạn
    return ResponseEntity.ok(contactInfo);
}
```

#### Kịch Bản Kiểm Tra 1: Timeout Exception

1. Đặt breakpoint trong endpoint của microservice
2. Gửi request qua Gateway
3. Giữ breakpoint để mô phỏng timeout
4. Quan sát Gateway timeout sau ~9 giây (4 requests × ~2 giây timeout)

#### Kịch Bản Kiểm Tra 2: Runtime Exception

Tạm thời throw exception để kiểm tra hành vi retry:

```java
@GetMapping("/contact-info")
public ResponseEntity<ContactInfoDto> getContactInfo() {
    logger.debug("Invoked loans contact-info API");
    throw new RuntimeException("Lỗi mô phỏng");
    // return ResponseEntity.ok(contactInfo);
}
```

Kết quả mong đợi:
- Console hiển thị 4 log entries (1 lần đầu + 3 lần thử lại)
- Gateway trả về 500 Internal Server Error sau khi hết lần thử lại

### 4. Các Bước Triển Khai

Sau khi thay đổi cấu hình:

1. Dừng Loans microservice
2. Dừng Gateway Server
3. Rebuild cả hai ứng dụng
4. Khởi động Loans microservice trước
5. Khởi động Gateway Server

## Best Practices (Thực Hành Tốt)

### Khi Nào Sử Dụng Retry Pattern

✅ **Nên dùng cho:**
- GET requests (thao tác đọc)
- Các thao tác idempotent
- Lỗi mạng tạm thời
- Dịch vụ tạm thời không khả dụng

❌ **Tránh dùng cho:**
- POST requests (tạo tài nguyên)
- PATCH/PUT requests (cập nhật)
- DELETE requests (nếu không chắc về điều kiện query)
- Các thao tác có tác động phụ

### Các Cân Nhắc Khi Cấu Hình

1. **Số Lần Thử Lại**: Cân bằng giữa khả năng phục hồi và thời gian phản hồi
2. **Cài Đặt Timeout**: Đảm bảo timeout toàn cục phù hợp với số lần thử lại
3. **Chiến Lược Backoff**: Ngăn việc quá tải các dịch vụ downstream
4. **Phương Thức HTTP**: Chỉ bật cho các thao tác idempotent

## Lợi Ích

- **Chịu Lỗi**: Tự động phục hồi từ các lỗi tạm thời
- **Không Cần Can Thiệp Thủ Công**: Gateway xử lý retry tự động
- **Khả Năng Phục Hồi Mạng**: Giảm thiểu các vấn đề mạng tạm thời
- **Trải Nghiệm Người Dùng Tốt Hơn**: Giảm các request thất bại do vấn đề tạm thời

## Ví Dụ Cấu Hình Hoàn Chỉnh

```java
@Bean
public RouteLocator routeConfig(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("loans_route", r -> r
            .path("/eazybank/loans/**")
            .filters(f -> f
                .rewritePath("/eazybank/loans/(?<segment>.*)", "/${segment}")
                .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
                .retry(retryConfig -> retryConfig
                    .setRetries(3)
                    .setMethods(HttpMethod.GET)
                    .setBackoff(100, 1000, 2, true)
                )
            )
            .uri("lb://LOANS")
        )
        .build();
}
```

## Xác Minh

Theo dõi logs ứng dụng để xác minh hành vi retry:

```
Invoked loans contact-info API
Invoked loans contact-info API
Invoked loans contact-info API
Invoked loans contact-info API
```

Bốn log entries xác nhận: 1 request ban đầu + 3 lần thử lại.

## Kết Luận

Retry pattern trong Spring Cloud Gateway cung cấp khả năng chịu lỗi tự động cho microservices. Bằng cách cấu hình số lần thử lại phù hợp, chiến lược backoff, và chỉ áp dụng cho các thao tác idempotent, bạn có thể cải thiện đáng kể độ tin cậy của dịch vụ mà không cần can thiệp thủ công.

## Điểm Chính Cần Nhớ

- Retry pattern giúp phục hồi từ các lỗi tạm thời
- Chỉ cấu hình retry cho các phương thức HTTP idempotent
- Sử dụng exponential backoff để tránh quá tải dịch vụ
- Gateway xử lý retry một cách minh bạch
- Kết hợp với circuit breaker để có khả năng phục hồi toàn diện

## Thuật Ngữ Kỹ Thuật

- **Retry Pattern**: Mẫu thử lại - chiến lược tự động thử lại các thao tác thất bại
- **Idempotent**: Tính idempotent - thao tác có thể thực hiện nhiều lần mà không gây tác động phụ
- **Backoff**: Thời gian chờ giữa các lần thử lại
- **Exponential Backoff**: Thời gian chờ tăng theo cấp số nhân
- **Transient Failure**: Lỗi tạm thời - lỗi ngắn hạn có thể tự phục hồi
- **Fault Tolerance**: Khả năng chịu lỗi - khả năng hoạt động khi có lỗi xảy ra



================================================================================
FILE: 52-implementing-retry-pattern-in-microservices.md
================================================================================

# Triển Khai Retry Pattern Trong Microservices Với Resilience4j

## Tổng Quan

Hướng dẫn này trình bày cách triển khai retry pattern (mẫu thử lại) trong từng microservice riêng lẻ sử dụng Resilience4j và Spring Boot, thay vì triển khai logic retry tại tầng Gateway Server. Retry pattern giúp cải thiện khả năng phục hồi của microservices bằng cách tự động thử lại các thao tác thất bại trước khi từ bỏ.

## So Sánh: Retry Tại Gateway vs Microservice

| Khía Cạnh | Retry Tại Gateway Server | Retry Tại Microservice |
|-----------|--------------------------|------------------------|
| **Số Lần Thử Lại** | 4 lần thử (bao gồm request ban đầu) | 3 lần thử (có thể cấu hình, không tính request ban đầu) |
| **Hỗ Trợ Fallback** | Hạn chế/Không có | Hỗ trợ đầy đủ cơ chế fallback |
| **Phạm Vi Cấu Hình** | Áp dụng ở tầng gateway | Áp dụng ở từng service riêng lẻ |
| **Độ Chi Tiết** | Kiểm soát ít đối với các endpoint cụ thể | Kiểm soát chi tiết từng phương thức |

## Các Bước Triển Khai

### 1. Thêm Annotation @Retry

Để triển khai retry pattern trong microservice, thêm annotation `@Retry` vào phương thức mục tiêu:

```java
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() {
    // Nội dung phương thức
}
```

**Tham Số Quan Trọng:**
- `name`: Định danh duy nhất cho cấu hình retry này (ví dụ: tên phương thức)
- `fallbackMethod`: Tên phương thức fallback sẽ thực thi sau khi tất cả retry thất bại

### 2. Tạo Phương Thức Fallback

Phương thức fallback phải tuân theo các quy tắc cụ thể:

#### Quy Tắc 1: Khớp Signature Của Phương Thức
Signature của phương thức fallback phải khớp chính xác với phương thức gốc (cùng kiểu trả về).

#### Quy Tắc 2: Thêm Tham Số Throwable
Phương thức fallback phải chấp nhận thêm một tham số kiểu `Throwable` ở cuối.

**Ví Dụ:**
```java
// Phương thức gốc (không có tham số)
public ResponseEntity<String> getBuildInfo() {
    logger.debug("getBuildInfo method invoked");
    throw new NullPointerException(); // Mô phỏng lỗi
    // return ResponseEntity.ok(buildVersion);
}

// Phương thức fallback
public ResponseEntity<String> getBuildInfoFallback(Throwable throwable) {
    logger.debug("getBuildInfoFallback method invoked");
    return ResponseEntity.ok("0.9"); // Giá trị trả về mặc định
}
```

**Lưu Ý:** Nếu phương thức gốc có 2 tham số, phương thức fallback sẽ có 3 tham số (2 từ gốc + 1 Throwable).

### 3. Cấu Hình Properties Cho Retry

Thêm cấu hình retry trong file `application.yml`:

```yaml
resilience4j:
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 100ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
```

**Các Thuộc Tính Cấu Hình:**
- `maxAttempts`: Số lần thử lại tối đa (mặc định: 3)
- `waitDuration`: Thời gian chờ ban đầu giữa các lần thử (100ms)
- `enableExponentialBackoff`: Bật chiến lược exponential backoff
- `exponentialBackoffMultiplier`: Hệ số nhân backoff (2x)

#### Cấu Hình Cụ Thể Cho Từng Instance

Để có hành vi retry khác nhau cho từng phương thức:

```yaml
resilience4j:
  retry:
    configs:
      default:
        maxAttempts: 3
        waitDuration: 100ms
    instances:
      getBuildInfo:
        maxAttempts: 5
        waitDuration: 200ms
      backendA:
        maxAttempts: 4
        waitDuration: 150ms
      backendB:
        maxAttempts: 3
        waitDuration: 100ms
```

### 4. Thêm Logger Statements

Để theo dõi các lần thử lại, thêm logging:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AccountsController {
    private static final Logger logger = LoggerFactory.getLogger(AccountsController.class);
    
    @Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
    public ResponseEntity<String> getBuildInfo() {
        logger.debug("getBuildInfo method invoked");
        throw new NullPointerException(); // Mô phỏng lỗi
    }
    
    public ResponseEntity<String> getBuildInfoFallback(Throwable throwable) {
        logger.debug("getBuildInfoFallback method invoked");
        return ResponseEntity.ok("0.9");
    }
}
```

### 5. Kiểm Tra Triển Khai

**Kết Quả Console Mong Đợi:**
```
getBuildInfo method invoked
getBuildInfo method invoked
getBuildInfo method invoked
getBuildInfoFallback method invoked
```

Điều này xác nhận có 3 lần thử lại tiếp theo là thực thi fallback.

## Tương Tác Giữa Circuit Breaker và Retry

### Cấu Hình Time Limiter

Khi sử dụng cả Circuit Breaker và Retry pattern, bạn cần xem xét cấu hình Time Limiter:

**Vấn Đề:** Timeout mặc định của Circuit Breaker (1 giây) có thể nhỏ hơn tổng thời gian retry, khiến fallback của Circuit Breaker kích hoạt thay vì fallback của Retry.

**Giải Pháp:** Cấu hình Time Limiter của Circuit Breaker để phù hợp với thao tác retry.

### Cấu Hình Time Limiter Trong Gateway Server

```java
@Configuration
public class GatewayConfig {
    
    @Bean
    public Customizer<ReactiveResilience4JCircuitBreakerFactory> defaultCustomizer() {
        return factory -> factory.configureDefault(id -> new Resilience4JConfigBuilder(id)
            .circuitBreakerConfig(CircuitBreakerConfig.ofDefaults())
            .timeLimiterConfig(TimeLimiterConfig.custom()
                .timeoutDuration(Duration.ofSeconds(4))
                .build())
            .build());
    }
}
```

**Điểm Quan Trọng:**
- Time Limiter xác định thời gian chờ tối đa cho một thao tác
- Timeout mặc định: ~1 giây
- Khuyến nghị cho retry: 4+ giây
- Ngăn Circuit Breaker kích hoạt sớm trong quá trình retry

### Điều Chỉnh Wait Duration Của Retry

**Kịch Bản 1:** Giảm thời gian chờ retry
```yaml
resilience4j:
  retry:
    configs:
      default:
        waitDuration: 100ms  # Retry nhanh hơn
```

**Kịch Bản 2:** Tăng timeout của Circuit Breaker
```java
.timeLimiterConfig(TimeLimiterConfig.custom()
    .timeoutDuration(Duration.ofSeconds(4))
    .build())
```

## Best Practices (Thực Hành Tốt Nhất)

### 1. Chọn Số Lần Retry Phù Hợp
- Bắt đầu với 3 lần thử cho hầu hết các trường hợp
- Điều chỉnh dựa trên yêu cầu SLA và đặc điểm của downstream service

### 2. Triển Khai Exponential Backoff
- Ngăn không làm quá tải downstream services
- Tăng thời gian chờ dần dần (100ms, 200ms, 400ms...)

### 3. Luôn Cung Cấp Fallback Methods
- Trả về giá trị mặc định/cached
- Trả về response lỗi nhã nhặn
- Log lỗi để theo dõi

### 4. Xem Xét Tổng Timeout
- Timeout Circuit Breaker > (số lần retry × thời gian chờ)
- Ví dụ: 4 giây > (3 × 500ms với backoff)

### 5. Giám Sát và Log
- Theo dõi số lần thử lại
- Log các lần gọi fallback
- Giám sát mẫu lỗi

### 6. Khởi Động Lại Services Sau Khi Thay Đổi Cấu Hình
- Khởi động lại microservice sau khi thay đổi config
- Khởi động lại Gateway Server để làm mới Eureka service registry
- Đảm bảo Gateway có thông tin instance service mới nhất

## Quy Trình Kiểm Tra

1. **Thực hiện thay đổi cấu hình** trong `application.yml`
2. **Build ứng dụng** (Maven/Gradle)
3. **Dừng AccountsApplication**
4. **Dừng Gateway Server**
5. **Khởi động AccountsApplication** ở chế độ debug
6. **Khởi động Gateway Server**
7. **Kiểm tra với Postman** hoặc REST client
8. **Xác minh console logs** cho các lần retry

## Tài Liệu Tham Khảo

Để biết thêm chi tiết về cấu hình Resilience4j:
- [Tài Liệu Chính Thức Resilience4j](https://resilience4j.readme.io/)
- Phần Getting Started > Configurations
- Cấu hình cụ thể cho Retry pattern
- Cấu hình Circuit Breaker

## Tóm Tắt

Triển khai retry pattern trong từng microservice riêng lẻ mang lại nhiều lợi ích:
- **Hỗ Trợ Fallback**: Khác với retry ở tầng Gateway, retry tại microservice hỗ trợ cơ chế fallback
- **Kiểm Soát Chi Tiết**: Cấu hình hành vi retry cho từng phương thức/endpoint
- **Khả Năng Phục Hồi Tốt Hơn**: Kết hợp với Circuit Breaker cho khả năng chịu lỗi toàn diện
- **Giám Sát**: Dễ dàng theo dõi và debug hành vi retry ở tầng service

Retry pattern, kết hợp với cấu hình Circuit Breaker và Time Limiter phù hợp, cải thiện đáng kể khả năng phục hồi của microservice và mang lại trải nghiệm người dùng tốt hơn trong các lỗi dịch vụ tạm thời.

---

## Chủ Đề Liên Quan
- Triển Khai Circuit Breaker Pattern
- Service Discovery Với Eureka
- Cấu Hình Spring Cloud Gateway
- Các Pattern Resilience4j Trong Microservices



================================================================================
FILE: 53-advanced-retry-pattern-configuration-microservices.md
================================================================================

# Cấu Hình Nâng Cao Retry Pattern Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày các tùy chọn cấu hình nâng cao để triển khai retry pattern trong microservices Spring Boot, bao gồm xử lý ngoại lệ, tích hợp với Spring Cloud Gateway và các phương pháp tốt nhất cho triển khai production.

## Bỏ Qua Các Ngoại Lệ Cụ Thể

### Yêu Cầu Nghiệp Vụ

Trong một số trường hợp, việc retry một số ngoại lệ nhất định là không có ý nghĩa. Ví dụ, nếu `NullPointerException` xảy ra do dữ liệu đầu vào không hợp lệ, việc retry cùng một thao tác sẽ luôn dẫn đến cùng một ngoại lệ.

### Cấu Hình

Để cấu hình các ngoại lệ không nên kích hoạt retry, thêm thuộc tính `ignoreExceptions` vào file `application.yml`:

```yaml
resilience4j:
  retry:
    instances:
      your-retry-name:
        ignoreExceptions:
          - java.lang.NullPointerException
          - java.lang.IllegalArgumentException
```

**Lưu ý:** Bạn có thể thêm nhiều ngoại lệ bằng cách liệt kê chúng với dấu gạch ngang trong định dạng YAML.

### Ví Dụ Triển Khai

```java
@GetMapping("/build-info")
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() throws TimeoutException {
    // Triển khai method
    throw new NullPointerException("Ngoại lệ mẫu");
}
```

Khi `NullPointerException` nằm trong danh sách bỏ qua, cơ chế retry sẽ bỏ qua các lần thử lại và ngay lập tức gọi phương thức fallback.

## Chỉ Retry Các Ngoại Lệ Cụ Thể

### Cấu Hình

Thay vì bỏ qua ngoại lệ, bạn có thể định nghĩa rõ ràng những ngoại lệ nào nên kích hoạt retry:

```yaml
resilience4j:
  retry:
    instances:
      your-retry-name:
        retryExceptions:
          - java.util.concurrent.TimeoutException
          - java.io.IOException
```

**Quan trọng:** Khi sử dụng `retryExceptions`, bạn không cần định nghĩa `ignoreExceptions`. Tất cả các ngoại lệ không được liệt kê trong `retryExceptions` sẽ tự động bị bỏ qua bởi Resilience4j.

### Ví Dụ Với TimeoutException

```java
@GetMapping("/build-info")
@Retry(name = "getBuildInfo", fallbackMethod = "getBuildInfoFallback")
public ResponseEntity<String> getBuildInfo() throws TimeoutException {
    throw new TimeoutException("Thao tác hết thời gian chờ");
}
```

Vì `TimeoutException` là checked exception, nó phải được khai báo trong method signature với từ khóa `throws`.

## Retry Pattern Trong Spring Cloud Gateway

### Các Tùy Chọn Cấu Hình

Spring Cloud Gateway cung cấp khả năng cấu hình retry tương tự:

```java
// Trong cấu hình Gateway
.setExceptions(TimeoutException.class, IOException.class)
.setStatuses(HttpStatus.INTERNAL_SERVER_ERROR, HttpStatus.SERVICE_UNAVAILABLE)
```

### Sự Khác Biệt Chính

- **Không có tùy chọn bỏ qua ngoại lệ:** Gateway tập trung vào việc chỉ định cụ thể (retry cái gì)
- **Retry dựa trên HTTP status:** Bạn có thể cấu hình retry dựa trên mã trạng thái HTTP
- **Cấu hình dựa trên method:** Sử dụng các phương thức setter thay vì cấu hình YAML

## Sửa Lỗi Header Trùng Lặp Trong Gateway

### Vấn Đề

Khi triển khai retry pattern trong Gateway Server với custom filters, correlation ID header có thể xuất hiện nhiều lần trong response do response filter được thực thi ở mỗi lần retry.

### Giải Pháp

Sửa đổi `ResponseTraceFilter` để kiểm tra xem header đã tồn tại chưa:

```java
@Component
public class ResponseTraceFilter implements GlobalFilter, Ordered {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            ServerHttpResponse response = exchange.getResponse();
            
            // Kiểm tra header đã tồn tại trước khi thêm
            if (!response.getHeaders().containsKey(CORRELATION_ID_HEADER)) {
                String correlationId = exchange.getRequest()
                    .getHeaders()
                    .getFirst(CORRELATION_ID_HEADER);
                    
                response.getHeaders().add(CORRELATION_ID_HEADER, correlationId);
            }
        }));
    }
}
```

### Giải Thích Logic

- **Nếu header tồn tại:** `containsKey()` trả về `true`, phép phủ định làm nó thành `false`, khối if không thực thi
- **Nếu header không tồn tại:** `containsKey()` trả về `false`, phép phủ định làm nó thành `true`, header được thêm vào

## Các Bước Cấu Hình Hoàn Chỉnh

### 1. Thêm Retry Annotation

```java
@Retry(name = "retryPatternName", fallbackMethod = "fallbackMethodName")
```

### 2. Tạo Fallback Method

```java
public ResponseEntity<String> fallbackMethodName(Exception ex) {
    return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
        .body("Phản hồi dự phòng do: " + ex.getMessage());
}
```

### 3. Cấu Hình application.yml

```yaml
resilience4j:
  retry:
    instances:
      retryPatternName:
        maxAttempts: 3
        waitDuration: 500ms
        retryExceptions:
          - java.util.concurrent.TimeoutException
        ignoreExceptions:
          - java.lang.NullPointerException
```

## Kiểm Thử Và Xác Minh

### Xác Minh Đầu Ra Console

Sau khi cấu hình thành công, bạn sẽ thấy các log statements cho biết:

1. Lần gọi method ban đầu
2. Các lần thử retry (nếu có)
3. Lần gọi fallback method (nếu tất cả retry đều thất bại)

### Ví Dụ Đầu Ra Console

```
getBuildInfo() method invoked - Attempt 1
getBuildInfo() method invoked - Attempt 2
getBuildInfo() method invoked - Attempt 3
getBuildInfoFallback() method invoked
```

## Các Phương Pháp Tốt Nhất

1. **Chọn ngoại lệ một cách khôn ngoan:** Chỉ retry các lỗi tạm thời (timeout, lỗi mạng)
2. **Tránh retry các ngoại lệ nghiệp vụ:** Lỗi logic sẽ không được giải quyết bằng retry
3. **Sử dụng thời gian chờ phù hợp:** Cân bằng giữa khả năng phản hồi và tải hệ thống
4. **Triển khai cơ chế fallback phù hợp:** Luôn cung cấp sự suy giảm graceful
5. **Giám sát các metrics retry:** Theo dõi số lần retry và tỷ lệ thành công

## Tóm Tắt

Retry pattern trong microservices nên được cấu hình cẩn thận để xử lý các lỗi tạm thời trong khi tránh các lần retry không cần thiết. Bằng cách cấu hình đúng `retryExceptions` và `ignoreExceptions`, bạn có thể tạo ra các microservices có khả năng phục hồi cao, xử lý lỗi một cách graceful và hiệu quả.

---

**Các Chủ Đề Liên Quan:**
- Circuit Breaker Pattern
- Cơ Chế Fallback
- Cấu Hình Resilience4j
- Spring Cloud Gateway Filters



================================================================================
FILE: 54-rate-limiter-pattern-in-microservices.md
================================================================================

# Mô Hình Rate Limiter Trong Microservices

## Giới Thiệu

Mô hình Rate Limiter (Giới hạn Tốc độ) là một mẫu thiết kế quan trọng trong kiến trúc microservices, giúp kiểm soát và giới hạn tốc độ các yêu cầu đến với các API hoặc microservices cụ thể. Mô hình này rất cần thiết để duy trì sự ổn định của hệ thống và đảm bảo việc sử dụng dịch vụ công bằng.

## Hiểu Về Rate Limiter Qua Một Ví Dụ

Hãy nghĩ về trò chơi bắn bóng bay ở các triển lãm. Chủ trò chơi chỉ cung cấp một số lượng tài nguyên giới hạn - thường là ba hoặc năm lần chơi dựa trên số tiền bạn trả. Bạn chỉ có thể bắn bóng trong giới hạn này. Tại sao? Bởi vì nếu cho phép chơi không giới hạn sẽ dẫn đến thua lỗ cho chủ quán. Nguyên tắc tương tự này áp dụng cho Mô hình Rate Limiter trong microservices.

## Rate Limiter Pattern Là Gì?

Sử dụng mô hình này trong microservices, chúng ta có thể kiểm soát và giới hạn tốc độ các yêu cầu đến với một API hoặc microservice cụ thể. Mô hình này chủ yếu được sử dụng để:

- **Ngăn chặn lạm dụng hệ thống**
- **Bảo vệ tài nguyên hệ thống**
- **Đảm bảo sử dụng công bằng dịch vụ** cho mọi người

## Vấn Đề Mà Nó Giải Quyết

Trong kiến trúc microservices, nhiều dịch vụ được triển khai và có thể tương tác với nhau để gửi phản hồi cho các ứng dụng client. Tuy nhiên, nếu không có các hạn chế và kiểm soát phù hợp về việc tiêu thụ yêu cầu, một số vấn đề có thể phát sinh:

### Suy Giảm Hiệu Suất
Khi một client hoặc người dùng cụ thể gửi quá nhiều yêu cầu, nó có thể dẫn đến suy giảm hiệu suất hoặc cạn kiệt tài nguyên.

### Tấn Công DoS (Denial of Service - Từ chối Dịch vụ)
Một người dùng độc hại hoặc hacker có thể cố gắng gửi các yêu cầu liên tục - có thể hàng triệu yêu cầu - đến máy chủ của bạn, cố gắng:
- Làm sập microservices của bạn
- Làm chậm mạng lưới microservices
- Gián đoạn tính khả dụng của dịch vụ

### Cạn Kiệt Tài Nguyên
Không có giới hạn tốc độ, tài nguyên hệ thống có thể nhanh chóng bị cạn kiệt bởi một số ít người dùng hoặc kẻ tấn công độc hại.

## Chiến Lược Triển Khai

Để tránh các tình huống này và đảm bảo sử dụng công bằng, hãy triển khai Mô hình Rate Limiter để áp dụng giới hạn trên các yêu cầu đến.

### Ví Dụ Tình Huống
- **Lưu lượng dự kiến**: 10,000 yêu cầu mỗi giây
- **Thiết lập hạ tầng** phù hợp
- **Cấu hình rate limiter** dựa trên tải dự kiến
- **Cơ chế cảnh báo**: Nếu đột ngột nhận 1 triệu yêu cầu, điều này cho thấy có khả năng bị lạm dụng hoặc tấn công

## Ưu Điểm Của Mô Hình Rate Limiter

1. **Bảo vệ khỏi Yêu cầu Quá tải**: Che chắn microservices khỏi các yêu cầu quá mức hoặc độc hại từ hackers
2. **Đảm bảo Ổn định**: Duy trì hiệu suất và tính khả dụng của dịch vụ
3. **Kiểm soát Truy cập**: Cung cấp quyền truy cập được kiểm soát vào tài nguyên trong microservice
4. **Môi trường Lành mạnh**: Tạo ra một hệ sinh thái nơi mọi người có thể sử dụng dịch vụ công bằng trong giới hạn tốc độ đã cấu hình

## Cách Hoạt Động

Khi vượt quá giới hạn tốc độ, hệ thống trả về **mã trạng thái HTTP 429** ("Too Many Requests" - Quá nhiều yêu cầu), cho biết rằng dịch vụ không thể chấp nhận thêm yêu cầu. Phản hồi này cho client biết họ nên thử lại sau vài giây hoặc vài phút.

## Các Chiến Lược Giới Hạn Tốc Độ

Giới hạn tốc độ có thể được áp dụng dựa trên các chiến lược khác nhau:

- **Dựa trên Session**: Giới hạn yêu cầu mỗi phiên
- **Dựa trên Địa chỉ IP**: Giới hạn yêu cầu từ các địa chỉ IP cụ thể
- **Dựa trên Người dùng**: Giới hạn yêu cầu mỗi người dùng đã đăng nhập
- **Dựa trên Tenant**: Giới hạn yêu cầu mỗi tenant trong hệ thống đa tenant
- **Dựa trên Server**: Giới hạn yêu cầu mỗi instance server

## Triển Khai Theo Gói Đăng Ký

Mô hình Rate Limiter cũng có thể được sử dụng để cung cấp các dịch vụ khác biệt dựa trên các gói đăng ký:

- **Người dùng Cơ bản (Basic)**: Giới hạn tốc độ thấp hơn
- **Người dùng Cao cấp (Premier)**: Giới hạn tốc độ trung bình
- **Người dùng Doanh nghiệp (Enterprise)**: Giới hạn tốc độ cao hơn

Điều này cho phép bạn triển khai các giới hạn tốc độ khác nhau cho các loại người dùng khác nhau dựa trên cấp độ đăng ký của họ, tạo ra một mô hình dịch vụ phân tầng.

## Kết Luận

Mô hình Rate Limiter là một thành phần thiết yếu của bất kỳ kiến trúc microservices mạnh mẽ nào. Giống như trò chơi bắn bóng bay áp dụng giới hạn để duy trì bền vững, việc giới hạn tốc độ đảm bảo các dịch vụ của bạn vẫn khả dụng, hiệu quả và công bằng cho tất cả người dùng trong khi bảo vệ chống lại các cuộc tấn công độc hại và cạn kiệt tài nguyên.

Bằng cách triển khai mô hình này một cách hiệu quả, bạn tạo ra một môi trường được kiểm soát nơi người dùng hợp pháp có thể truy cập dịch vụ một cách đáng tin cậy, trong khi ngăn chặn lạm dụng và duy trì sức khỏe hệ thống.



================================================================================
FILE: 55-implementing-rate-limiter-pattern-spring-cloud-gateway.md
================================================================================

# Triển khai Rate Limiter Pattern với Spring Cloud Gateway

## Tổng quan

Hướng dẫn này giải thích cách triển khai rate limiter pattern sử dụng Spring Cloud Gateway để kiểm soát và giới hạn số lượng requests có thể được xử lý bởi các microservices của bạn.

## Rate Limiter Pattern là gì?

Rate limiting là một kỹ thuật được sử dụng để kiểm soát tốc độ xử lý requests. Khi triển khai với Spring Cloud Gateway, nó xác định liệu một request hiện tại có được phép tiếp tục hay nên bị chặn. Nếu một request vượt quá giới hạn được định nghĩa, mã trạng thái HTTP 429 (Too Many Requests - Quá nhiều yêu cầu) sẽ được trả về theo mặc định.

## Các trường hợp sử dụng Rate Limiting

Theo kinh nghiệm triển khai của Stripe, rate limiting là cần thiết cho một số kịch bản sau:

1. **Bảo vệ khỏi Traffic Spike**: Một user duy nhất gây ra tăng đột biến traffic và ảnh hưởng đến tất cả users khác
2. **Scripts hoạt động sai**: Một user có script vô tình gửi quá nhiều requests
3. **Tấn công có chủ ý**: Một user cố ý cố gắng làm quá tải servers của bạn
4. **Quản lý ưu tiên**: Requests có độ ưu tiên thấp không nên ảnh hưởng đến traffic có độ ưu tiên cao
5. **Suy giảm hệ thống**: Khi xảy ra sự cố nội bộ, loại bỏ các requests có độ ưu tiên thấp để duy trì các hoạt động quan trọng

## Hiểu về KeyResolver

`KeyResolver` là một thành phần quan trọng xác định tiêu chí để thực thi giới hạn rate. Bạn có thể triển khai rate limiting dựa trên:

- **User**: Giới hạn requests cho từng người dùng
- **Session**: Giới hạn requests cho từng phiên làm việc
- **IP Address**: Giới hạn requests cho từng địa chỉ IP
- **Server**: Giới hạn requests cho từng server

### Triển khai mặc định

Spring cung cấp triển khai mặc định `PrincipalNameKeyResolver` hoạt động với Spring Security. Nó lấy username của người dùng hiện đang đăng nhập để thực thi giới hạn rate theo từng user.

**Quan trọng**: Nếu `KeyResolver` không tìm thấy key, các requests sẽ bị từ chối theo mặc định. Hành vi này có thể được điều chỉnh thông qua các thuộc tính cấu hình.

## Triển khai dựa trên Redis

Spring Cloud Gateway sử dụng Redis làm hệ thống lưu trữ cơ bản để triển khai rate limiting. Triển khai này dựa trên công việc được thực hiện bởi đội ngũ Stripe.

### Dependency cần thiết

Thêm dependency sau vào `pom.xml` của bạn:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

## Thuật toán Token Bucket

Rate limiter sử dụng **Thuật toán Token Bucket** với ba thuộc tính chính:

### 1. ReplenishRate

Xác định số lượng requests được phép mỗi giây (tốc độ mà tokens được thêm vào bucket).

- **Ví dụ**: Nếu `replenishRate = 100`, thì 100 tokens được thêm vào bucket mỗi giây
- Sau 2 giây mà không có tiêu thụ, bucket sẽ có 200 tokens

### 2. BurstCapacity

Xác định số lượng tokens tối đa mà bucket có thể chứa (ngăn chặn việc tràn đầy).

- **Ví dụ**: Nếu `burstCapacity = 200`, bucket không thể chứa nhiều hơn 200 tokens
- Các tokens thừa từ `replenishRate` sẽ bị loại bỏ khi bucket đã đầy

### 3. RequestedTokens

Xác định số lượng tokens mà mỗi request tiêu thụ.

- **Mặc định**: 1 token cho mỗi request
- Có thể được điều chỉnh dựa trên độ phức tạp hoặc độ ưu tiên của request

## Các ví dụ cấu hình

### Tốc độ ổn định (Không có Bursting)

Đặt `replenishRate` và `burstCapacity` cùng một giá trị:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 100
                redis-rate-limiter.requestedTokens: 1
```

Cấu hình này thêm 100 tokens mỗi giây, và các tokens không sử dụng sẽ bị loại bỏ.

### Cho phép Bursts tạm thời

Đặt `burstCapacity` cao hơn `replenishRate`:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
                redis-rate-limiter.requestedTokens: 1
```

Điều này cho phép users tích lũy tokens và sử dụng tới 200 requests trong một burst.

### Một Request mỗi Phút

Để chỉ cho phép một request mỗi phút:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: my-service
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 1
                redis-rate-limiter.burstCapacity: 60
                redis-rate-limiter.requestedTokens: 60
```

**Giải thích**:
- `replenishRate = 1`: Thêm 1 token mỗi giây (60 tokens mỗi phút)
- `burstCapacity = 60`: Tối đa 60 tokens trong bucket
- `requestedTokens = 60`: Mỗi request tiêu thụ 60 tokens

Kết quả: Chỉ có thể thực hiện 1 request mỗi phút.

## Triển khai KeyResolver tùy chỉnh

Bạn có thể tạo một bean `KeyResolver` tùy chỉnh để xác định tiêu chí giới hạn rate của mình:

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest()
                .getQueryParams()
                .getFirst("user")
    );
}
```

Ví dụ này trích xuất user từ một query parameter để thực thi giới hạn rate theo từng user.

## Cấu hình dựa trên Java

Thay vì YAML, bạn có thể cấu hình rate limiting sử dụng Java:

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("rate_limited_route", r -> r.path("/api/**")
            .filters(f -> f.requestRateLimiter(c -> c
                .setRateLimiter(redisRateLimiter())
                .setKeyResolver(userKeyResolver())))
            .uri("lb://MY-SERVICE"))
        .build();
}
```

## Lưu ý quan trọng

⚠️ **Cảnh báo**: Đặt `burstCapacity = 0` sẽ chặn tất cả các requests. Đảm bảo giá trị này luôn lớn hơn 0 để rate limiting hoạt động bình thường.

## Các bước tiếp theo

Trong các phần tiếp theo, chúng ta sẽ triển khai rate limiter pattern này trong Gateway Server với các ví dụ thực tế và trình bày cách cấu hình dựa trên các yêu cầu kinh doanh khác nhau.

## Tóm tắt

- Rate limiting bảo vệ microservices của bạn khỏi traffic spikes và các cuộc tấn công
- Thuật toán Token Bucket cung cấp rate limiting linh hoạt với ba tham số chính
- Redis cung cấp bộ nhớ lưu trữ cho distributed rate limiting
- KeyResolver xác định tiêu chí để áp dụng giới hạn rate
- Cấu hình có thể được thực hiện thông qua YAML hoặc các phương pháp dựa trên Java



================================================================================
FILE: 56-rate-limiter-redis-spring-gateway-tutorial.md
================================================================================

# Triển Khai Rate Limiter Pattern trong Spring Cloud Gateway với Redis

## Tổng Quan

Hướng dẫn này trình bày cách triển khai Rate Limiter pattern trong Spring Cloud Gateway sử dụng Redis để kiểm soát số lượng request mà người dùng có thể thực hiện trong một khoảng thời gian cụ thể.

## Yêu Cầu Tiên Quyết

- Ứng dụng Spring Cloud Gateway
- Docker đã được cài đặt và đang chạy
- Dự án Maven đã được thiết lập
- Redis container

## Bước 1: Thêm Dependency Redis

Thêm dependency Redis reactive vào file `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

Sau khi thêm dependency, thực hiện Maven reload để tải các thư viện cần thiết.

## Bước 2: Cấu Hình Các Bean Rate Limiter

Trong class `GatewayserverApplication`, tạo hai bean quan trọng:

### 1. Bean KeyResolver

Bean này xác định key mà Rate Limiter pattern sẽ hoạt động dựa trên:

```java
@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.justOrEmpty(exchange.getRequest()
            .getHeaders()
            .getFirst("user"))
            .defaultIfEmpty("anonymous");
}
```

**Giải thích:**
- Trích xuất header `user` từ request
- Nếu không có header `user`, gán giá trị mặc định là `anonymous`
- Trong môi trường production, tùy chỉnh logic này dựa trên yêu cầu của bạn

### 2. Bean RedisRateLimiter

Cấu hình các tham số giới hạn tốc độ:

```java
@Bean
public RedisRateLimiter redisRateLimiter() {
    return new RedisRateLimiter(replenishRate, burstCapacity, requestedTokens);
}
```

**Các Tham Số Cấu Hình:**
- **replenishRate**: 1 (thêm một token mỗi giây)
- **burstCapacity**: 1 (số token tối đa có sẵn)
- **requestedTokens**: 1 (chi phí mỗi request)

Với các cài đặt này, mỗi người dùng chỉ có thể thực hiện **một request mỗi giây**.

## Bước 3: Áp Dụng Rate Limiter cho Routes

Thêm filter Rate Limiter vào cấu hình routing. Ví dụ, áp dụng cho cards microservice:

```java
.route(p -> p
    .path("/eazybank/cards/**")
    .filters(f -> f
        .addResponseHeader("X-Response-Time", LocalDateTime.now().toString())
        .requestRateLimiter(c -> c
            .setRateLimiter(redisRateLimiter())
            .setKeyResolver(userKeyResolver()))
    )
    .uri("lb://CARDS"))
```

Cấu hình này áp dụng Rate Limiter pattern cho tất cả các API trong cards microservice.

## Bước 4: Khởi Động Redis Container

Khởi động Redis container sử dụng Docker:

```bash
docker run -p 6379:6379 --name eazyredis -d redis
```

**Giải thích lệnh:**
- `-p 6379:6379`: Map cổng mặc định của Redis
- `--name eazyredis`: Đặt tên cho container
- `-d`: Chạy ở chế độ detached (nền)
- `redis`: Tên image

Redis sẽ duy trì các bucket với tên người dùng và xử lý các cấu hình rate limiting.

## Bước 5: Cấu Hình Kết Nối Redis

Thêm các thuộc tính kết nối Redis vào `application.yml` trong gateway server:

```yaml
spring:
  application:
    name: gatewayserver
  config:
    import: "optional:configserver:http://localhost:8071"
  cloud:
    gateway:
      # ... các cấu hình gateway khác
  data:
    redis:
      connect-timeout: 2s
      host: localhost
      port: 6379
      timeout: 1s
```

Lưu các thay đổi và rebuild ứng dụng.

## Bước 6: Kiểm Tra Rate Limiter

### Khởi Động Các Service Cần Thiết

Đảm bảo các service sau đang chạy:
1. Config Server
2. Eureka Server
3. Cards Microservice
4. Gateway Server

### Kiểm Tra Tải với Apache Benchmark

Sử dụng Apache Benchmark (AB) để kiểm tra hành vi rate limiting:

```bash
ab -n 10 -c 2 -v 3 http://localhost:8072/eazybank/cards/api/contact-info
```

**Các Tham Số:**
- `-n 10`: Gửi tổng cộng 10 request
- `-c 2`: Duy trì mức độ đồng thời là 2 (gửi 2 request cùng lúc)
- `-v 3`: Mức độ chi tiết 3 (báo cáo chi tiết)

### Kết Quả Mong Đợi

**Tóm tắt:**
- Tổng số request: 10
- Request thành công: 1 (HTTP 200)
- Request thất bại: 9 (HTTP 429 - Too Many Requests)
- Thời gian xử lý: ~0.5 giây

**Mẫu Response:**
- Request đầu tiên: `200 OK`
- Các request còn lại: `429 Too Many Requests`

Mã trạng thái `429` cho biết giới hạn tốc độ đã bị vượt quá, xác nhận rằng Rate Limiter pattern đang hoạt động chính xác.

## Cách Hoạt Động

1. **Thuật Toán Token Bucket**: Redis duy trì một token bucket cho mỗi người dùng (được xác định bởi KeyResolver)
2. **Bổ Sung Token**: Một token được thêm vào bucket mỗi giây
3. **Xử Lý Request**: Mỗi request tiêu thụ một token
4. **Giới Hạn Tốc Độ**: Khi không còn token, các request nhận mã trạng thái `429`

## Kiểm Tra với Header User Tùy Chỉnh

Để kiểm tra với người dùng cụ thể, thêm header `user` vào request:

```bash
ab -n 10 -c 2 -v 3 -H "user: john.doe" http://localhost:8072/eazybank/cards/api/contact-info
```

**Lưu ý:** Trong môi trường local với một người dùng duy nhất, hành vi vẫn giống nhau. Sự khác biệt thực sự trở nên rõ ràng trong production với nhiều người dùng, nơi mỗi người dùng có giới hạn tốc độ riêng.

## Cài Đặt Apache Benchmark

### Unix/Mac
Apache Benchmark thường được cài đặt sẵn. Kiểm tra bằng:
```bash
ab -V
```

### Windows
1. Tải Apache HTTP Server từ trang web chính thức của Apache
2. Giải nén file archive
3. Thêm thư mục `bin` vào PATH của hệ thống
4. Kiểm tra cài đặt: `ab -V`

Để biết hướng dẫn cài đặt chi tiết, tìm kiếm các hướng dẫn "Apache Benchmark installation" cụ thể cho hệ điều hành của bạn.

## Best Practices (Thực Hành Tốt Nhất)

1. **Logic KeyResolver Tùy Chỉnh**: Triển khai KeyResolver dựa trên yêu cầu cụ thể của bạn (user ID, API key, địa chỉ IP, v.v.)
2. **Cấu Hình Rate Limit**: Điều chỉnh `replenishRate`, `burstCapacity` và `requestedTokens` dựa trên khả năng API và yêu cầu kinh doanh
3. **Giám Sát**: Giám sát hiệu suất Redis và các số liệu rate limiting trong production
4. **Xử Lý Lỗi**: Triển khai xử lý lỗi phù hợp và thông báo thân thiện với người dùng cho các request bị giới hạn tốc độ
5. **Tốc Độ Khác Nhau cho Mỗi Service**: Áp dụng các giới hạn tốc độ khác nhau cho các microservice khác nhau dựa trên mức độ quan trọng và khả năng tải

## Kết Luận

Rate Limiter pattern trong Spring Cloud Gateway cung cấp một cách hiệu quả để bảo vệ các microservice của bạn khỏi bị quá tải bởi quá nhiều request. Bằng cách tận dụng Redis và thuật toán token bucket, bạn có thể đảm bảo sử dụng công bằng và duy trì sự ổn định của service trong toàn bộ hệ thống phân tán.

## Các Pattern Liên Quan

- Circuit Breaker Pattern (cho accounts microservice)
- Retry Pattern (cho loans microservice)
- Load Balancing với Eureka
- Service Discovery

---

*Triển khai này đảm bảo rằng các microservice của bạn duy trì hiệu suất tối ưu trong khi ngăn chặn lạm dụng và đảm bảo phân phối tài nguyên công bằng cho tất cả người dùng.*



================================================================================
FILE: 57-implementing-rate-limiter-pattern-in-microservices.md
================================================================================

# Triển Khai Pattern RateLimiter Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai pattern RateLimiter trong microservices Spring Boot sử dụng Resilience4j. Khác với việc triển khai RateLimiter trong gateway server, cách tiếp cận này áp dụng giới hạn tốc độ trực tiếp trong từng microservice riêng lẻ.

## Yêu Cầu Trước

- Microservice Spring Boot (ví dụ: Accounts microservice)
- Thư viện Resilience4j
- Hiểu biết cơ bản về annotations trong Spring Boot

## Các Bước Triển Khai

### 1. Thêm Annotation RateLimiter

Đầu tiên, đánh dấu method cần giới hạn tốc độ với `@RateLimiter`:

```java
@RateLimiter(name = "getJavaVersion")
public String getJavaVersion() {
    // Phần thực thi method
}
```

Tham số `name` xác định cấu hình rate limiter cụ thể sẽ được sử dụng.

### 2. Cấu Hình Thuộc Tính RateLimiter

Thêm cấu hình sau vào file `application.yml`:

```yaml
resilience4j:
  ratelimiter:
    configs:
      default:
        limitRefreshPeriod: 5000  # 5 giây
        limitForPeriod: 1         # 1 request mỗi chu kỳ
        timeoutDuration: 1000     # Thời gian chờ 1 giây
```

### Giải Thích Các Thuộc Tính Cấu Hình

- **limitRefreshPeriod**: Chu kỳ sau đó rate limiter làm mới quota của nó (5000ms = 5 giây)
- **limitForPeriod**: Số lượng request được phép trong mỗi chu kỳ làm mới (1 request trong 5 giây trong ví dụ này)
- **timeoutDuration**: Thời gian tối đa một thread sẽ đợi để được phép thực thi (1000ms = 1 giây)

## Cách Hoạt Động

1. Khi một request đến, RateLimiter kiểm tra xem quota cho chu kỳ hiện tại có sẵn không
2. Nếu quota đã hết, thread sẽ đợi tối đa `timeoutDuration` cho chu kỳ làm mới tiếp theo
3. Nếu không được cấp phép trong khoảng timeout, một exception sẽ được throw ra
4. Mỗi `limitRefreshPeriod`, quota sẽ được làm mới

## Kiểm Tra Triển Khai

1. Khởi động ứng dụng microservice của bạn
2. Thực hiện nhiều request liên tiếp đến endpoint có rate limit
3. Sau khi vượt quá giới hạn, bạn sẽ nhận được lỗi: "RateLimiter does not permit further calls"

## Triển Khai Cơ Chế Fallback

### Thêm Method Fallback

Để xử lý exceptions về giới hạn tốc độ một cách mượt mà, thêm method fallback:

```java
@RateLimiter(name = "getJavaVersion", fallbackMethod = "getJavaVersionFallback")
public String getJavaVersion() {
    // Phần thực thi method gốc
}

public String getJavaVersionFallback(Throwable throwable) {
    return "Java 17"; // Phản hồi dự phòng
}
```

### Yêu Cầu Cho Method Fallback

- Phải có cùng signature với method gốc
- Phải bao gồm thêm tham số `Throwable`
- Có thể trả về dữ liệu từ cache, giá trị mặc định, hoặc thông báo thân thiện với người dùng

## Các Trường Hợp Sử Dụng

### Bảo Vệ Năng Lực Hạ Tầng
Nếu hạ tầng của bạn chỉ có thể xử lý 10,000 requests mỗi giây, sử dụng RateLimiter để ngăn quá tải.

### Phân Bổ Tài Nguyên Dựa Trên Độ Ưu Tiên
Áp dụng giới hạn tốc độ nghiêm ngặt hơn cho các API ưu tiên thấp, đảm bảo các API ưu tiên cao có đủ tài nguyên.

### Quản Lý Quota Tùy Chỉnh
Triển khai các giới hạn tốc độ khác nhau cho các method khác nhau dựa trên yêu cầu nghiệp vụ.

## So Sánh Với Rate Limiting Ở Tầng Gateway

### Cách Tiếp Cận Gateway Server
- Sử dụng Redis và KeyResolver
- Có thể áp dụng quota dựa trên user, địa chỉ IP, hoặc các tiêu chí khác
- Rate limiting tập trung

### Cách Tiếp Cận Tầng Microservice
- Áp dụng trực tiếp trong microservice
- Rate limiting đồng nhất cho tất cả requests đến
- Cấu hình đơn giản hơn, không cần dependencies bên ngoài (như Redis)

## Cân Nhắc Cho Môi Trường Production

- Trong production, `limitForPeriod` thường sẽ ở mức hàng nghìn
- Chọn các giá trị phù hợp dựa trên năng lực hạ tầng của bạn
- Giám sát các metrics về rate limiting để điều chỉnh cấu hình
- Cân nhắc triển khai các chiến lược fallback toàn diện

## Tổng Kết

Pattern RateLimiter trong microservices cung cấp khả năng kiểm soát chi tiết việc xử lý request:
- Bảo vệ hạ tầng khỏi quá tải
- Cho phép phân bổ tài nguyên dựa trên độ ưu tiên
- Hoạt động độc lập không cần gateway server
- Hỗ trợ cơ chế fallback cho việc giảm tải một cách mượt mà

Bây giờ bạn có hai cách tiếp cận để triển khai rate limiting:
1. **Gateway Server**: Sử dụng Spring Cloud Gateway với Redis
2. **Tầng Microservice**: Sử dụng annotations của Resilience4j

Chọn cách tiếp cận phù hợp nhất với yêu cầu nghiệp vụ và kiến trúc của bạn.



================================================================================
FILE: 58-bulkhead-pattern-in-microservices.md
================================================================================

# Mẫu Thiết Kế Bulkhead trong Microservices

## Giới Thiệu

Mẫu thiết kế Bulkhead là một mẫu thiết kế về khả năng phục hồi giúp cải thiện sự cô lập và ổn định của các thành phần hoặc dịch vụ trong kiến trúc microservice. Mẫu thiết kế này được lấy cảm hứng từ các vách ngăn thực tế được sử dụng trong tàu thuyền để ngăn nước tràn vào toàn bộ con tàu nếu một khoang bị thủng.

## Hiểu Về Mẫu Thiết Kế Bulkhead

### Phép So Sánh Với Vách Ngăn Tàu Thuyền

Mẫu thiết kế này lấy tên từ kỹ thuật phân chia khoang được sử dụng trong tàu thuyền. Giống như tàu Titanic có các vách ngăn ngăn chặn việc ngập nước toàn bộ con tàu khi va chạm với tảng băng trôi, mẫu thiết kế Bulkhead trong kiến trúc phần mềm ngăn chặn sự cố ở một thành phần ảnh hưởng đến toàn bộ hệ thống.

### Lợi Ích Chính

Với mẫu thiết kế Bulkhead, bạn có thể:

- **Cô lập sự cố**: Hạn chế tác động của sự cố hoặc tải cao ở một thành phần lan rộng sang các thành phần khác
- **Ngăn chặn cạn kiệt tài nguyên**: Đảm bảo rằng tải cao ở một phần của hệ thống không làm sập toàn bộ hệ thống
- **Cho phép hoạt động độc lập**: Cho phép các thành phần khác tiếp tục hoạt động độc lập ngay cả khi một thành phần đang chịu áp lực
- **Xác định ranh giới tài nguyên**: Phân bổ hoặc chỉ định tài nguyên cho các REST API cụ thể hoặc microservices cụ thể để tránh sử dụng tài nguyên quá mức

## Ví Dụ Thực Tế: Microservice Tài Khoản

### Không Có Mẫu Thiết Kế Bulkhead

Xem xét một microservice Tài khoản với hai REST API:

1. **API myAccount**: Một REST API đơn giản không phụ thuộc vào các microservices khác
2. **API myCustomerDetails**: Một REST API phức tạp phụ thuộc vào các microservices khác như Khoản vay và Thẻ

**Vấn đề**: Không có mẫu thiết kế Bulkhead, API `myCustomerDetails` (có độ phức tạp và thời gian xử lý cao hơn) sẽ tiêu thụ tất cả các luồng và tài nguyên có sẵn trong container Docker. Điều này ảnh hưởng đến hiệu suất của API `myAccount` đơn giản hơn, có thể không nhận đủ luồng hoặc tài nguyên để xử lý các yêu cầu từ khách hàng.

### Với Mẫu Thiết Kế Bulkhead

Bằng cách triển khai mẫu thiết kế Bulkhead:

- Xác định ranh giới rõ ràng cho mỗi REST API
- Chỉ định các luồng và tài nguyên cụ thể từ thread pool cho mỗi API
- API `myAccount` có thể hoạt động hiệu quả bất kể `myCustomerDetails` nhận bao nhiêu yêu cầu
- Mỗi API nhận được số lượng luồng tối thiểu được đảm bảo từ thread pool

## Triển Khai Với Resilience4j

### Lưu Ý Quan Trọng

Hiện tại, Spring Cloud Gateway không hỗ trợ mẫu thiết kế Bulkhead một cách tự nhiên. Bạn chỉ có thể triển khai mẫu thiết kế Bulkhead bằng cách sử dụng thư viện **Resilience4j**.

### Sử Dụng Annotation @Bulkhead

```java
@Bulkhead(name = "myBulkhead", type = Bulkhead.Type.THREADPOOL)
public Response myMethod() {
    // Logic nghiệp vụ của bạn
}
```

### Các Thuộc Tính Cấu Hình

#### Cấu Hình Bulkhead Tiêu Chuẩn

- **maxConcurrentCalls**: Số lượng cuộc gọi đồng thời tối đa mà một bulkhead cụ thể có thể hỗ trợ trên một REST API
- **maxWaitDuration**: Thời gian tối đa để chờ quyền thực thi

#### Cấu Hình Thread Pool Bulkhead

Để kiểm soát chi tiết hơn việc phân bổ luồng:

- **maxThreadPoolSize**: Kích thước tối đa của thread pool
- **coreThreadPoolSize**: Kích thước cốt lõi của thread pool
- **queueCapacity**: Dung lượng của hàng đợi cho các yêu cầu đang chờ

## Kiểm Tra Và Xác Thực

Để xác thực đúng cách việc triển khai mẫu thiết kế Bulkhead, bạn cần:

- Các công cụ kiểm tra hiệu suất thương mại (ví dụ: LoadRunner, JMeter)
- Khả năng giám sát việc sử dụng luồng và phân bổ tài nguyên
- Sự cộng tác với nhóm kiểm tra hiệu suất của bạn

## Tóm Tắt

Mẫu thiết kế Bulkhead rất cần thiết khi bạn cần:

- Xác định ranh giới tài nguyên cho các API trong microservices của bạn
- Ngăn một API độc quyền tài nguyên hệ thống
- Tăng cường khả năng phục hồi và ổn định tổng thể của kiến trúc microservice của bạn

Bằng cách tận dụng mẫu thiết kế này với kiểm tra hiệu suất phù hợp, bạn có thể đảm bảo rằng microservices của bạn duy trì sự ổn định ngay cả trong các điều kiện tải khác nhau.

## Khi Nào Sử Dụng

Cân nhắc triển khai mẫu thiết kế Bulkhead khi:

- Bạn có các API với yêu cầu tài nguyên khác nhau đáng kể
- Một số API phụ thuộc vào nhiều microservices bên ngoài
- Bạn cần đảm bảo mức hiệu suất tối thiểu cho các API quan trọng
- Bạn muốn ngăn chặn các lỗi lan rộng trong hệ thống của bạn



================================================================================
FILE: 59-resilience4j-aspect-order-and-combining-patterns.md
================================================================================

# Thứ Tự Aspect và Kết Hợp Các Pattern Resiliency trong Resilience4j

## Tổng Quan

Khi xây dựng microservices với Spring Boot, thư viện Resilience4j cung cấp nhiều pattern resiliency khác nhau để xử lý lỗi một cách linh hoạt. Trong khi việc triển khai các pattern riêng lẻ khá đơn giản, việc hiểu cách nhiều pattern hoạt động cùng nhau là rất quan trọng đối với các kịch bản nghiệp vụ phức tạp.

## Hiểu Về Thứ Tự Aspect trong Resilience4j

### Thứ Tự Thực Thi Mặc Định

Resilience4j tuân theo một thứ tự cụ thể khi nhiều pattern resiliency được áp dụng cho một API, method hoặc service duy nhất. Theo tài liệu chính thức (hướng dẫn Getting Started cho Spring Boot 2 và 3), thứ tự aspect mặc định là:

1. **Retry** (thực thi cuối cùng/ngoài cùng)
2. **Circuit Breaker**
3. **Rate Limiter**
4. **Time Limiter**
5. **Bulkhead** (thực thi đầu tiên/trong cùng)

Điều này có nghĩa là luồng thực thi hoạt động từ Bulkhead → Time Limiter → Rate Limiter → Circuit Breaker → Retry.

### Tùy Chỉnh Thứ Tự Aspect

Mặc dù thứ tự mặc định hoạt động tốt cho nhiều kịch bản, Resilience4j cho phép bạn tùy chỉnh thứ tự thực thi cho các trường hợp phức tạp. Điều này có thể dễ dàng cấu hình bằng cách sử dụng properties trong file `application.yml` của bạn.

#### Ví Dụ Cấu Hình

```yaml
resilience4j:
  retry:
    aspect-order: 2
  circuitbreaker:
    aspect-order: 1
```

Trong cấu hình này:
- **Giá trị cao hơn** cho biết **độ ưu tiên cao hơn** (thực thi trước)
- Retry có độ ưu tiên 2, do đó nó thực thi trước Circuit Breaker (độ ưu tiên 1)
- Circuit Breaker bắt đầu công việc của nó sau khi pattern Retry hoàn thành

## Thực Hành Tốt Nhất và Khuyến Nghị

### Tránh Over-Engineering

⚠️ **Lưu Ý Quan Trọng**: Không nên cố gắng kết hợp tất cả các pattern resiliency mà không cân nhắc kỹ lưỡng. Điều này có thể dẫn đến:
- Giải pháp quá phức tạp (over-engineered)
- Hành vi không mong đợi trong môi trường production
- Khó khăn trong việc debug và bảo trì

### Hướng Dẫn Triển Khai

1. **Phân Tích Yêu Cầu**: Hiểu rõ nhu cầu nghiệp vụ cụ thể trước khi kết hợp các pattern
2. **Kiểm Thử Kỹ Lưỡng**: Luôn thực hiện kiểm thử toàn diện trước khi triển khai lên production
3. **Thẩm Định Đúng Đắn**: Đánh giá sự cần thiết của từng pattern cho trường hợp sử dụng của bạn
4. **Giữ Đơn Giản**: Chỉ sử dụng các pattern cần thiết cho microservices của bạn
5. **Sẵn Sàng Production**: Chuẩn bị cho các bất ngờ tiềm ẩn nếu các pattern không được kiểm thử đúng cách

## Kết Luận

Hiểu về thứ tự aspect trong Resilience4j là điều cần thiết khi kết hợp nhiều pattern resiliency. Mặc dù thư viện cung cấp sự linh hoạt để tùy chỉnh thứ tự thực thi, việc duy trì tính đơn giản và đảm bảo kiểm thử kỹ lưỡng trước khi triển khai production là rất quan trọng.

## Tài Liệu Tham Khảo

- [Tài Liệu Chính Thức Resilience4j - Tích Hợp Spring Boot](https://resilience4j.readme.io/docs/getting-started-3)
- Hướng Dẫn Cấu Hình Aspect Order

---

*Tài liệu này đề cập đến việc kết hợp và sắp xếp thứ tự các pattern resiliency trong microservices Spring Boot sử dụng thư viện Resilience4j.*



================================================================================
FILE: 6-microservices-internal-communication-challenges.md
================================================================================

# Thách Thức Giao Tiếp Nội Bộ Giữa Các Microservices

## Giới Thiệu

Trong phần này, chúng ta sẽ khám phá các thách thức phát sinh khi xây dựng ứng dụng microservices, đặc biệt tập trung vào các mô hình giao tiếp nội bộ giữa các dịch vụ. Trước khi đi sâu vào các thách thức, điều quan trọng là phải hiểu các khái niệm và thuật ngữ chính trong kiến trúc microservices.

## Kiến Trúc Mạng Microservices

### Thiết Lập Microservices Hiện Tại

Mạng microservices của chúng ta hiện bao gồm ba microservices xử lý logic nghiệp vụ:

1. **Accounts Microservice** - Xử lý các thao tác liên quan đến tài khoản
2. **Loans Microservice** - Quản lý các thao tác về khoản vay
3. **Cards Microservice** - Xử lý các giao dịch liên quan đến thẻ

Các microservices này chịu trách nhiệm:
- Lưu trữ dữ liệu
- Truy xuất dữ liệu
- Xử lý các yêu cầu và thực thi logic nghiệp vụ
- Gửi các phản hồi phù hợp

## Mô Hình Giao Tiếp Bên Ngoài

### Mô Hình API Gateway

Trong các ứng dụng microservices triển khai thực tế, các dịch vụ không được phép truy cập trực tiếp từ các client bên ngoài. Thay vào đó, chúng ta tuân theo mô hình giao tiếp an toàn:

- Tất cả microservices được triển khai trong một **mạng microservices** (microservice network)
- Một **tường lửa** (firewall) bao quanh mạng microservices
- Các client bên ngoài (C1, C2, C3, v.v.) phải vào qua một **điểm vào duy nhất**
- Điểm vào này được gọi là **API Gateway** (hoặc Gateway)

### Lợi Ích Của API Gateway

API Gateway đóng vai trò là điểm vào duy nhất cho lưu lượng bên ngoài và cung cấp:

- **Kiểm tra bảo mật** - Xác thực và phân quyền
- **Kiểm toán** - Theo dõi và giám sát yêu cầu
- **Ghi log** - Ghi log tập trung cho tất cả các yêu cầu bên ngoài
- **Các yêu cầu phi chức năng** - Xử lý các vấn đề xuyên suốt

### Luồng Lưu Lượng Bên Ngoài

```
Client Bên Ngoài (C1, C2, C3)
        ↓
   API Gateway
        ↓
Mạng Microservices
    (Accounts, Loans, Cards)
```

Tất cả các yêu cầu từ client bên ngoài đều đi qua API Gateway trước khi đến bất kỳ microservice nào. Lưu lượng này được gọi là **lưu lượng bên ngoài** (external traffic) hoặc **giao tiếp bên ngoài** (external communication).

## Mô Hình Giao Tiếp Nội Bộ

### Giao Tiếp Giữa Các Dịch Vụ

Trong mạng microservices, các dịch vụ thường cần giao tiếp với nhau. Ví dụ:

**Kịch bản**: Một yêu cầu từ bên ngoài đến Accounts microservice thông qua API Gateway. Để hoàn thành phản hồi, Accounts microservice có thể cần:

1. Kết nối với **Loans microservice** để lấy thông tin khoản vay
2. Kết nối với **Cards microservice** để truy xuất chi tiết thẻ

Loại giao tiếp giữa các dịch vụ trong mạng microservices này được gọi là **giao tiếp nội bộ** (internal communication) hoặc **lưu lượng nội bộ** (internal traffic).

### Các Loại Giao Tiếp

| Loại Giao Tiếp | Mô Tả | Phạm Vi |
|----------------|-------|---------|
| **Giao Tiếp Bên Ngoài** | Lưu lượng từ client bên ngoài qua API Gateway | Bên ngoài → Bên trong mạng |
| **Giao Tiếp Nội Bộ** | Giao tiếp giữa các dịch vụ trong mạng | Chỉ bên trong mạng |

## Trọng Tâm Của Phần Này

Phần này đề cập cụ thể đến:

- **Trọng tâm chính**: Các thách thức giao tiếp nội bộ giữa các microservices
- **Nội dung**: Các thách thức phát sinh khi microservices giao tiếp với nhau
- **Giải pháp**: Cách khắc phục các thách thức giao tiếp nội bộ

**Lưu ý**: API Gateway và các mô hình lưu lượng bên ngoài sẽ được đề cập trong các phần tiếp theo.

## Điểm Chính Cần Nhớ

1. Microservices không bao giờ nên được truy cập trực tiếp từ các client bên ngoài
2. API Gateway cung cấp một điểm vào duy nhất, an toàn cho tất cả lưu lượng bên ngoài
3. Giao tiếp nội bộ giữa các microservices cần được xem xét cẩn thận
4. Hiểu sự khác biệt giữa lưu lượng bên ngoài và nội bộ là rất quan trọng
5. Cả hai mô hình giao tiếp đều có những thách thức riêng cần được giải quyết

## Nội Dung Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Các thách thức cụ thể trong giao tiếp nội bộ microservices
- Các giải pháp và best practices cho giao tiếp giữa các dịch vụ
- Chiến lược triển khai sử dụng Spring Boot và Java
- Các mô hình API Gateway (sẽ được đề cập trong các phần sau)

---

*Tài liệu này là một phần của khóa học toàn diện về kiến trúc microservices tập trung vào triển khai với Java Spring Boot.*



================================================================================
FILE: 60-testing-resiliency-patterns-docker-containers.md
================================================================================

# Kiểm Tra Các Mẫu Thiết Kế Khả Năng Phục Hồi trong Docker Containers

## Tổng Quan

Hướng dẫn này bao gồm việc kiểm tra các mẫu thiết kế khả năng phục hồi (resiliency patterns) trong microservices sử dụng Docker containers, bao gồm các pattern RateLimiter, Circuit Breaker và Retry với Spring Cloud Gateway và tích hợp Redis.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker và Docker Compose
- Tài khoản Docker Hub để push images
- Tất cả microservices đã cập nhật dependencies
- Redis service cho RateLimiter pattern

## Xây Dựng Docker Images

### Cập Nhật Cấu Hình Maven

Trước khi tạo Docker images, cập nhật file `pom.xml` trong tất cả microservices:

- Thay đổi tag từ `S9` sang `S10`
- Điều này đảm bảo việc quản lý phiên bản đúng cho section mới

### Tạo Images với Google Jib

Sử dụng lệnh sau để tạo Docker images:

```bash
# Lệnh tạo Docker images với Google Jib
mvn clean compile jib:dockerBuild
```

### Đẩy Images lên Docker Hub

Sau khi build images, push chúng lên Docker Hub:

```bash
# Lệnh push Docker images
docker push <ten-dockerhub-cua-ban>/<ten-image>:s10
```

Xác minh images đã có trên Docker Hub bằng cách kiểm tra repository của bạn. Tất cả microservices phải có tag `s10`.

## Cấu Hình Docker Compose

### Thêm Redis Service

Redis là bắt buộc để triển khai RateLimiter pattern với Spring Cloud Gateway.

**Cấu Hình Docker Compose:**

```yaml
redis:
  image: redis
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    timeout: 10s
    retries: 10
  extends:
    file: common-config.yml
    service: network-deploy-service
```

**Chi Tiết Cấu Hình:**
- **Tên Service:** redis
- **Image:** Redis image chính thức
- **Port Mapping:** 6379:6379
- **Health Check:** Sử dụng lệnh `redis-cli ping`
- **Network:** Mở rộng từ easybank network trong common-config

### Cấu Hình Gateway Server

Gateway Server yêu cầu cấu hình bổ sung cho tích hợp Redis.

**Dependencies:**

Thêm Redis dependency vào Gateway Server. Gateway Server có nhiều dependencies và nên khởi động sau các service khác.

**Biến Môi Trường:**

```yaml
environment:
  SPRING_DATA_REDIS_CONNECT_TIMEOUT: 2s
  SPRING_DATA_REDIS_HOST: redis
  SPRING_DATA_REDIS_PORT: 6379
  SPRING_DATA_REDIS_TIMEOUT: 1s
```

**Lưu Ý Quan Trọng:**
- Sử dụng tên service `redis` thay vì `localhost` cho host
- Cấu hình các giá trị timeout phù hợp
- Cập nhật image tag thành `s10`

### Cập Nhật Profiles

Sau khi cập nhật Docker Compose file cho production:
- Sao chép cùng cấu hình sang QA profile
- Sao chép cùng cấu hình sang default profile
- Không cần thay đổi trong `common-config.yml`

## Triển Khai và Kiểm Tra

### Khởi Động Containers

Di chuyển đến thư mục production profile và thực thi:

```bash
docker compose up -d
```

Lệnh này khởi động tất cả containers ở chế độ detached. Quá trình mất khoảng 1-2 phút.

### Xác Minh Triển Khai

**Kiểm Tra Docker Desktop:**
1. Mở Docker Desktop
2. Điều hướng đến logs của Gateway Server
3. Xác nhận message: "GatewayserverApplication started successfully"

**Kiểm Tra Trạng Thái Container:**

```bash
docker ps
```

Xác minh tất cả sáu services đang chạy với trạng thái healthy.

## Kiểm Tra Các Resiliency Patterns

### Kiểm Tra RateLimiter trong Accounts Microservice

**API Endpoint:**

```
GET http://localhost:8072/easybank/accounts/api/java-version
```

**Kiểm Tra Request Đơn:**
- Gửi một request đơn
- Kết quả mong đợi: Thông tin phiên bản Java (ví dụ: "Java 17")

**Kiểm Tra Nhiều Requests:**
- Gửi nhiều requests trong vòng một giây
- Kết quả mong đợi: Cơ chế fallback được kích hoạt
- Response cho biết đã vượt quá giới hạn rate

### Kiểm Tra RateLimiter trong Gateway Server

Sử dụng Apache Benchmark để kiểm tra RateLimiter pattern với RedisRateLimiter.

**Lệnh:**

```bash
ab -n 10 -c 2 http://localhost:8072/easybank/accounts/api/contact-info
```

**Kết Quả Mong Đợi:**
- Tổng requests: 10
- Failed requests: 8 (xấp xỉ)
- HTTP Status: 429 Too Many Requests
- Điều này xác nhận rate limiter hoạt động đúng

### Kiểm Tra Các Patterns Khác

**Circuit Breaker và Retry Patterns:**

Mặc dù các patterns này đã được triển khai và kiểm tra locally, việc kiểm tra chúng trong Docker yêu cầu:
- Cố ý tạo RuntimeExceptions
- Tạo lại Docker images với test code

Vì các patterns này đã được xác minh trong môi trường local, chúng sẽ hoạt động tương tự trong Docker containers.

## Thực Hành Tốt Nhất

### Cấu Hình Rate Limiting

- Cấu hình các giới hạn rate phù hợp dựa trên nhu cầu ứng dụng
- Triển khai cơ chế fallback để có trải nghiệm người dùng tốt hơn
- Giám sát các metrics về rate limit trong production

### Quản Lý Docker Image

- Sử dụng tags có ý nghĩa cho versioning (ví dụ: s10 cho section 10)
- Giữ Docker Hub repository được tổ chức tốt
- Ghi chép các thay đổi giữa các phiên bản

### Chiến Lược Kiểm Tra

- Kiểm tra trong môi trường local trước
- Xác thực với Docker containers trước khi production
- Sử dụng các công cụ như Apache Benchmark cho load testing
- Giám sát logs và health checks

## Code Repository

Tất cả các thay đổi code cho section này có sẵn trong GitHub repository:

**Repository:** microservices
**Branch/Tag:** section_10

Xem xét repository để tìm:
- Cấu hình Docker Compose hoàn chỉnh
- Code microservice đã cập nhật
- Configuration files cho tất cả profiles

## Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp

**Vấn Đề Kết Nối Redis:**
- Xác minh Redis container đang chạy
- Kiểm tra cấu hình network
- Đảm bảo hostname đúng (sử dụng tên service, không phải localhost)

**Rate Limiter Không Hoạt Động:**
- Xác nhận Redis dependency đã được thêm
- Kiểm tra environment variables trong Gateway Server
- Xác minh Redis có thể truy cập từ Gateway

**Vấn Đề Khởi Động Container:**
- Kiểm tra thứ tự dependency trong Docker Compose
- Xem xét cấu hình health check
- Kiểm tra container logs để tìm lỗi

## Tóm Tắt

Trong section này, chúng ta đã:

1. **Build và Deploy:** Tạo Docker images với tag `s10` và push lên Docker Hub
2. **Cấu Hình Redis:** Thêm Redis service để hỗ trợ RateLimiter pattern
3. **Cập Nhật Gateway:** Cấu hình Spring Cloud Gateway với tích hợp Redis
4. **Kiểm Tra Patterns:** Xác thực chức năng RateLimiter trong cả Accounts microservice và Gateway Server
5. **Xác Minh Triển Khai:** Xác nhận tất cả services chạy thành công trong môi trường Docker

Các microservices hiện tại đã trưởng thành hơn và có khả năng chịu lỗi tốt hơn với các resiliency patterns được triển khai hoạt động đúng trong môi trường container hóa.

## Các Bước Tiếp Theo

- Nghỉ ngơi để tiếp thu các khái niệm đã học
- Đừng vội vàng xem hết tài liệu khóa học
- Thực hành triển khai các patterns này trong dự án của riêng bạn
- Chuyển sang section tiếp theo khi đã sẵn sàng

---

**Quan Trọng:** Học các khái niệm phức tạp cần thời gian và nghỉ ngơi. Đừng cố gắng hoàn thành mọi thứ trong một lần. Hãy nghỉ ngơi, thực hành, và quay lại với tinh thần sảng khoái cho section tiếp theo.



================================================================================
FILE: 61-observability-and-monitoring-microservices-introduction.md
================================================================================

# Giới Thiệu Về Observability và Monitoring Trong Microservices

## Tổng Quan

Tài liệu này giới thiệu về **Thách thức #8** trong kiến trúc microservices: **Observability và Monitoring** (Khả năng quan sát và giám sát). Khi hệ thống microservices ngày càng phức tạp, các phương pháp debug và giám sát truyền thống trở nên không còn hiệu quả. Phần này khám phá các vấn đề cơ bản và giới thiệu giải pháp để triển khai observability và monitoring hiệu quả trong hệ thống phân tán.

## Các Thách Thức Chính Trong Microservices

### 1. Debug Hệ Thống Phân Tán

**Vấn đề**: Làm thế nào để debug microservices khi có sự cố xảy ra?

Trong ứng dụng nguyên khối (monolithic), việc debug khá đơn giản - chỉ có một ứng dụng duy nhất để kiểm tra. Tuy nhiên, trong kiến trúc microservices:
- Các request di chuyển qua nhiều services và containers
- Việc tracing giao dịch trở nên phức tạp qua các thành phần phân tán
- Việc xác định vị trí chính xác của lỗi yêu cầu công cụ hỗ trợ phức tạp

**Thách thức**: Truy vết các giao dịch qua nhiều services và containers để xác định nguyên nhân gốc rễ của vấn đề.

### 2. Quản Lý Log Tập Trung

**Vấn đề**: Làm thế nào để quản lý logs từ nhiều microservices?

**Cách tiếp cận với Monolithic**:
- Một ứng dụng duy nhất tạo logs ở một vị trí
- Dễ dàng tải xuống và phân tích logs
- Quy trình bảo trì và debug đơn giản

**Thực tế với Microservices**:
- Nhiều containers và services tạo logs độc lập
- Logs phân tán ở nhiều vị trí khác nhau
- Một request đơn có thể đi qua hơn 20 microservices
- Thu thập logs thủ công từ từng container là không khả thi

**Giải pháp cần thiết**: Hệ thống logging tập trung cho phép:
- Đánh chỉ mục và tìm kiếm hiệu quả
- Lọc và nhóm logs một cách hiệu quả
- Phân tích để xác định các mẫu và vấn đề

### 3. Giám Sát Hiệu Năng

**Vấn đề**: Làm thế nào để giám sát hiệu năng qua các service calls?

**Các mối quan tâm chính**:
- Các request đơn lẻ di chuyển qua nhiều microservices
- Cần theo dõi đường đi hoàn chỉnh của request qua chuỗi services
- Phải đo thời gian xử lý tại mỗi microservice
- Các điểm nghẽn hiệu năng khó xác định nếu không có công cụ phù hợp

**Yêu cầu**:
- Theo dõi độ trễ request qua toàn bộ chuỗi services
- Xác định microservice nào đang gây ra suy giảm hiệu năng
- Cho phép debug có mục tiêu các services chậm

### 4. Giám Sát Metrics và Sức Khỏe Hệ Thống

**Vấn đề**: Làm thế nào để giám sát sức khỏe của hàng trăm microservices và containers?

**Các Metrics cần giám sát**:
- Mức sử dụng CPU
- Tiêu thụ bộ nhớ
- JVM metrics
- Tính khả dụng của service
- Sức khỏe container

**Các thách thức**:
- Giám sát thủ công từng service với Actuator không khả thi ở quy mô lớn
- Cần dashboard tập trung cho tất cả microservices
- Yêu cầu cảnh báo và thông báo tự động cho hành vi bất thường

**Tại sao cần Cảnh báo Tự động?**:
- Giám sát thủ công 24/7 không khả thi
- Team cần được thông báo ngay lập tức khi có sự cố
- Phát hiện chủ động giúp ngăn chặn sự cố

## Giải Pháp: Observability và Monitoring

Bằng cách triển khai các phương pháp observability và monitoring phù hợp, chúng ta có thể:

✅ **Giải quyết thách thức debug** thông qua distributed tracing  
✅ **Tập trung quản lý log** để phân tích dễ dàng hơn  
✅ **Giám sát hiệu năng** qua toàn bộ chuỗi services  
✅ **Theo dõi metrics và sức khỏe** trong dashboard thống nhất  
✅ **Ngăn chặn sự cố** thông qua giám sát chủ động  
✅ **Nhận cảnh báo tự động** cho hành vi bất thường  

## Tiếp Theo Là Gì?

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Các khái niệm chi tiết về observability và monitoring
- Các công cụ và framework để triển khai các phương pháp này
- Triển khai thực tế trong Spring Boot microservices
- Best practices cho môi trường production

## Những Điểm Chính Cần Nhớ

1. **Observability và monitoring là thiết yếu** cho microservices ở quy mô lớn
2. **Các phương pháp debug truyền thống không hiệu quả** trong hệ thống phân tán
3. **Các giải pháp tập trung** là cần thiết cho logs, metrics, và tracing
4. **Giám sát và cảnh báo tự động** ngăn chặn chi phí thủ công và sự cố
5. **Theo dõi hiệu năng** qua các services là quan trọng cho tối ưu hóa

---

*Đây là một phần của loạt bài toàn diện về microservices tập trung vào Spring Boot và kiến trúc microservices Java.*



================================================================================
FILE: 62-observability-and-monitoring-in-microservices.md
================================================================================

# Khả Năng Quan Sát và Giám Sát trong Kiến Trúc Microservices

## Giới Thiệu

Trong bối cảnh kiến trúc microservices, việc hiểu được trạng thái nội bộ và tình trạng sức khỏe của hệ thống phân tán là vô cùng quan trọng. Tài liệu này sẽ khám phá các khái niệm về khả năng quan sát (observability) và giám sát (monitoring), sự khác biệt giữa chúng, và cách chúng phối hợp với nhau để đảm bảo độ tin cậy của hệ thống.

## Khả Năng Quan Sát (Observability) Là Gì?

**Khả năng quan sát** là khả năng hiểu được trạng thái nội bộ của một hệ thống thông qua việc quan sát đầu ra của nó. Trong microservices, khả năng quan sát đạt được bằng cách thu thập và phân tích dữ liệu từ nhiều nguồn khác nhau để hiểu:

- Các microservices đang hoạt động như thế nào bên trong
- Một microservice cụ thể xử lý các yêu cầu đến hiệu quả đến mức nào
- Microservice đang gặp phải bao nhiêu lỗi
- Hành vi và hiệu suất tổng thể của hệ thống

### Ba Trụ Cột của Khả Năng Quan Sát

#### 1. Số Liệu (Metrics)
Số liệu là các phép đo định lượng về tình trạng sức khỏe của hệ thống. Chúng giúp theo dõi:
- Mức sử dụng CPU
- Mức sử dụng bộ nhớ
- Thời gian phản hồi
- Các chỉ số hiệu suất và sức khỏe hệ thống

#### 2. Nhật Ký (Logs)
Nhật ký là các bản ghi về các sự kiện xảy ra bên trong hệ thống. Chúng cho phép theo dõi:
- Lỗi và ngoại lệ
- Các sự kiện không mong muốn
- Luồng thực thi phương thức
- Thông tin gỡ lỗi

Nhật ký là thiết yếu cho việc gỡ lỗi, đặc biệt trong môi trường production nơi khả năng truy cập trực tiếp có thể bị hạn chế.

#### 3. Dấu Vết (Traces)
Dấu vết là bản ghi về đường đi mà một yêu cầu đi qua hệ thống. Trong mạng lưới microservices với hàng trăm dịch vụ, dấu vết giúp:
- Hiểu hành trình của yêu cầu qua nhiều microservices
- Theo dõi hiệu suất tại từng microservice hoặc cấp độ phương thức
- Xác định các nút thắt cổ chai về hiệu suất
- Phân tích luồng yêu cầu từ đầu đến cuối

### Lợi Ích của Khả Năng Quan Sát

Bằng cách thu thập dữ liệu từ ba trụ cột này, các nhà phát triển có thể:
- Xác định và khắc phục sự cố một cách hiệu quả
- Phát hiện các nút thắt cổ chai về hiệu suất
- Cải thiện hiệu suất hệ thống
- Đảm bảo sức khỏe tổng thể của hệ thống

## Giám Sát (Monitoring) Là Gì?

**Giám sát** trong microservices liên quan đến việc kiểm tra dữ liệu telemetry có sẵn cho ứng dụng và xác định các cảnh báo cho các trạng thái lỗi đã biết.

### Các Khía Cạnh Chính của Giám Sát

Giám sát xây dựng dựa trên dữ liệu quan sát bằng cách tạo:
- **Bảng Điều Khiển (Dashboards)**: Biểu diễn trực quan cho đội ngũ vận hành giám sát sức khỏe tổng thể của microservices
- **Cảnh Báo (Alerts)**: Thông báo tự động khi các ngưỡng cụ thể bị vượt quá (ví dụ: sử dụng CPU > 80%)
- **Thông Báo (Notifications)**: Cập nhật thời gian thực về trạng thái hệ thống và các vấn đề

### Tầm Quan Trọng của Giám Sát

Giám sát là quan trọng trong microservices vì nó:

1. **Xác Định Vấn Đề Chủ Động**: Phát hiện sự cố trước khi chúng gây ra ngừng hoạt động hoặc gián đoạn
2. **Cho Phép Quyết Định Mở Rộng**: Thêm các instance khi tài nguyên bị hạn chế (ví dụ: sử dụng CPU cao)
3. **Theo Dõi Sức Khỏe**: Hiểu microservice nào đang hoạt động kém hoặc gặp vấn đề
4. **Tối Ưu Hiệu Suất**: Đưa ra quyết định sáng suốt về việc mở rộng, thu hẹp hoặc thay thế các instance
5. **Cải Thiện Độ Tin Cậy**: Duy trì sự ổn định của hệ thống thông qua giám sát liên tục

Với hàng trăm microservices chạy trong các container và máy ảo khác nhau, việc giám sát thủ công 24/7 là không thể. Các hệ thống giám sát tự động làm cho điều này trở nên khả thi.

## So Sánh Khả Năng Quan Sát và Giám Sát

### Ẩn Dụ Tảng Băng Trôi

Hãy nghĩ về giám sát và khả năng quan sát như hai mặt của một đồng xu:

- **Giám Sát (Trên Mặt Nước)**: Những gì bạn có thể dễ dàng nhìn thấy - bảng điều khiển hiển thị mức sử dụng CPU, số lượng thread, các số liệu sức khỏe, cảnh báo và thông báo
- **Khả Năng Quan Sát (Dưới Mặt Nước)**: Thông tin ẩn đòi hỏi điều tra sâu hơn - ngoại lệ runtime, vấn đề hiệu suất, trạng thái nội bộ cần phân tích nhật ký và dấu vết

### Sự Khác Biệt Chính

| Khía Cạnh | Giám Sát | Khả Năng Quan Sát |
|-----------|----------|-------------------|
| **Mục Đích** | Xác định và khắc phục sự cố | Hiểu trạng thái nội bộ của hệ thống |
| **Dữ Liệu Sử Dụng** | Số liệu, dấu vết và nhật ký | Số liệu, dấu vết, nhật ký và dữ liệu telemetry khác |
| **Mục Tiêu** | Xác định vấn đề | Hiểu cách hệ thống hoạt động |
| **Cách Tiếp Cận** | Phản ứng - đáp ứng khi vấn đề xảy ra | Chủ động - xác định vấn đề trước khi chúng trở nên nghiêm trọng |
| **Trọng Tâm** | Thu thập dữ liệu và phản hồi cảnh báo | Hiểu dữ liệu và khắc phục nguyên nhân gốc rễ |

### Cách Tiếp Cận Phản Ứng vs Chủ Động

**Giám Sát (Phản Ứng)**:
- Đội ngũ vận hành phản ứng khi vấn đề xảy ra
- Phản hồi được kích hoạt bởi cảnh báo (ví dụ: vấn đề mạng, vấn đề hiệu suất)
- Hành động được thực hiện sau khi các sự kiện được phát hiện

**Khả Năng Quan Sát (Chủ Động)**:
- Nhà phát triển chủ động xác định vấn đề
- Phát hiện các ngoại lệ hiếm hoặc không thường xuyên (ví dụ: NullPointerExceptions)
- Cung cấp bản sửa lỗi trong các phiên bản tương lai trước khi các vấn đề lớn phát sinh

## Tóm Tắt

Cả giám sát và khả năng quan sát đều dựa vào cùng các loại dữ liệu telemetry (số liệu, dấu vết và nhật ký) nhưng phục vụ các mục đích khác nhau:

- **Giám Sát**: Thu thập dữ liệu và phản ứng với các vấn đề thông qua cảnh báo, bảng điều khiển và thông báo
- **Khả Năng Quan Sát**: Hiểu dữ liệu và khắc phục sự cố theo thời gian thực bằng cách đào sâu vào các trạng thái nội bộ của hệ thống

**Nói một cách đơn giản**:
- Giám sát giúp bạn **xác định và khắc phục sự cố**
- Khả năng quan sát giúp bạn **hiểu trạng thái nội bộ của hệ thống**

Cùng nhau, chúng tạo thành một cách tiếp cận toàn diện để duy trì kiến trúc microservices khỏe mạnh và đáng tin cậy.

## Thực Hành Tốt Nhất

1. Triển khai cả ba trụ cột của khả năng quan sát (số liệu, nhật ký, dấu vết)
2. Thiết lập bảng điều khiển giám sát toàn diện cho đội ngũ vận hành
3. Xác định các cảnh báo có ý nghĩa dựa trên ngưỡng kinh doanh và kỹ thuật
4. Sử dụng các thực hành quan sát chủ động để xác định và khắc phục sự cố sớm
5. Cân bằng giữa giám sát phản ứng và nỗ lực quan sát chủ động
6. Tận dụng dữ liệu telemetry để cải thiện hệ thống liên tục

---

*Tài liệu này là một phần của loạt bài về kiến trúc microservices tập trung vào việc xây dựng các hệ thống phân tán có khả năng phục hồi, có thể quan sát được và dễ bảo trì bằng Java và Spring Boot.*



================================================================================
FILE: 63-log-aggregation-in-microservices.md
================================================================================

# Tập Trung Hóa Log trong Kiến Trúc Microservices

## Giới Thiệu

Trong kiến trúc microservices, khả năng quan sát (observability) và giám sát (monitoring) được xây dựng dựa trên ba trụ cột cơ bản:
- **Logging** (Ghi nhật ký)
- **Metrics** (Số liệu)
- **Traces** (Theo dấu)

Để giám sát microservices hiệu quả, chúng ta phải triển khai các khái niệm này để tạo ra dữ liệu giúp hiểu được trạng thái nội bộ của các dịch vụ.

## Hiểu Về Logs

### Logs Là Gì?

Logs là các bản ghi rời rạc về các sự kiện xảy ra trong một ứng dụng phần mềm theo thời gian. Mỗi mục log thường chứa:

- **Timestamp** (Dấu thời gian): Cho biết khi nào sự kiện xảy ra
- **Thông tin sự kiện**: Chi tiết về những gì đã xảy ra
- **Ngữ cảnh**: Dữ liệu ngữ cảnh bổ sung (ID luồng, người dùng, tenant, v.v.)

### Các Câu Hỏi Chính Mà Logs Giúp Trả Lời

- Điều gì đã xảy ra tại một thời điểm cụ thể?
- Luồng (thread) nào đang xử lý sự kiện?
- Người dùng hoặc tenant nào đang trong ngữ cảnh?

### Các Mức Độ Nghiêm Trọng Của Log

Logs được phân loại theo mức độ nghiêm trọng để kiểm soát độ chi tiết trong các môi trường khác nhau:

- **TRACE**: Thông tin chi tiết nhất
- **DEBUG**: Thông tin gỡ lỗi chi tiết
- **INFO**: Thông báo thông tin chung
- **WARN**: Thông báo cảnh báo
- **ERROR**: Sự kiện lỗi

## Thực Hành Tốt Nhất Về Logging

### Logging Dựa Trên Môi Trường

- **Production (Sản xuất)**: Chỉ ghi lại các sự kiện nghiêm trọng (WARN, ERROR) để giảm thiểu tác động hiệu suất
- **Development/Testing (Phát triển/Kiểm thử)**: Sử dụng logging chi tiết hơn (DEBUG, INFO) để có cái nhìn sâu sắc

### Tránh Ghi Log Quá Mức

Ghi log quá nhiều có thể dẫn đến:
- Giảm hiệu suất
- Vấn đề lưu trữ
- Khó tìm thông tin liên quan

**Khuyến nghị**: Ghi lại exceptions và lỗi nghiêm trọng trong production; sử dụng logging toàn diện trong môi trường không phải production.

## Thách Thức Trong Logging Microservices

### Ứng Dụng Nguyên Khối vs Microservices

**Ứng Dụng Nguyên Khối (Monolithic):**
- Tất cả code trong một codebase duy nhất
- Logs được lưu trữ tại một vị trí/máy chủ duy nhất
- Dễ dàng tìm kiếm và khắc phục sự cố

**Kiến Trúc Microservices:**
- Mỗi dịch vụ có logs riêng
- Logs phân tán trên nhiều container và vị trí
- Nhà phát triển phải kiểm tra logs từ nhiều nguồn để gỡ lỗi
- Khắc phục sự cố phức tạp và tốn thời gian

## Giải Pháp Tập Trung Hóa Log

### Tập Trung Hóa Log Là Gì?

Tập trung hóa log là thực hành thu thập logs từ tất cả các dịch vụ và lưu trữ chúng tại một vị trí tập trung duy nhất.

### Lợi Ích

- **Đơn Giản Hóa Khắc Phục Sự Cố**: Nhà phát triển chỉ cần tìm ở một nơi thay vì hàng trăm dịch vụ
- **Giải Quyết Vấn Đề Nhanh Hơn**: Truy cập nhanh vào tất cả logs liên quan
- **Cải Thiện Khả Năng Quan Sát**: Cái nhìn toàn diện về toàn bộ hệ thống

### Các Phương Pháp Triển Khai

#### Phương Pháp Do Developer Xử Lý (Không Khuyến Nghị)

Nhà phát triển viết logic tùy chỉnh để truyền logs từ container đến vị trí tập trung.

**Nhược Điểm:**
- Lãng phí thời gian của nhà phát triển vào logic không liên quan đến business
- Tăng độ phức tạp trong code microservice
- Chuyển hướng sự tập trung khỏi việc giải quyết các vấn đề business thực sự

#### Phương Pháp Khuyến Nghị

Sử dụng các công cụ tập trung hóa log chuyên dụng thực hiện việc tập trung hóa **mà không yêu cầu thay đổi code microservice**.

Phương pháp này cho phép nhà phát triển tập trung vào:
- Các vấn đề của khách hàng
- Logic nghiệp vụ
- Chức năng cốt lõi

## Các Bước Tiếp Theo

Trong các phần tiếp theo, chúng ta sẽ khám phá các sản phẩm và công cụ tập trung hóa log hiện đại cung cấp khả năng logging tập trung sẵn có cho kiến trúc microservices.

## Tài Nguyên Bổ Sung

Để có hướng dẫn chi tiết về triển khai logging trong ứng dụng Spring Boot, bao gồm:
- Thiết lập các mức độ nghiêm trọng khác nhau
- Cấu hình dựa trên môi trường
- Các thực hành tốt nhất về logging

Hãy tham khảo các khóa học Spring Boot toàn diện có phần riêng về triển khai logging.

---

**Điểm Chính**: Tập trung hóa log là điều thiết yếu cho khả năng quan sát microservices. Chọn các công cụ xử lý tập trung hóa log tự động, cho phép team phát triển tập trung vào việc mang lại giá trị business.



================================================================================
FILE: 64-implementing-log-aggregation-with-grafana-loki.md
================================================================================

# Triển Khai Log Aggregation với Grafana Loki

## Giới Thiệu về Grafana cho Observability và Monitoring

Là các nhà phát triển microservice, chúng ta không nên bị buộc phải tự triển khai toàn bộ logic observability và monitoring. Thay vào đó, chúng ta nên tận dụng các công cụ và best practices chuyên biệt giúp triển khai các tính năng này với nỗ lực tối thiểu.

Trong hướng dẫn này, chúng ta sẽ khám phá các công cụ và plugin có sẵn trong hệ sinh thái Grafana để triển khai observability và monitoring trong các ứng dụng microservices.

## Grafana là gì?

**Grafana** là một công ty xây dựng bộ công cụ và plugin toàn diện để triển khai observability và monitoring cho nhiều loại ứng dụng khác nhau:

- Kiến trúc microservices
- Ứng dụng web
- Ứng dụng IoT
- Bất kỳ loại ứng dụng nào cần monitoring

### Tại Sao Chọn Grafana?

Grafana cung cấp **các công cụ mã nguồn mở** cho nhiều kịch bản observability khác nhau:

- **Log Aggregation (Thu thập log tập trung)**: Grafana Loki
- **Metrics (Chỉ số)**: Tích hợp Prometheus với Grafana dashboards và alerts
- **Tracing (Theo dõi)**: Grafana Tempo
- **Integration (Tích hợp)**: Khả năng tương thích tuyệt vời với các tiêu chuẩn như OpenTelemetry và Prometheus

Grafana đã trở thành kỹ năng bắt buộc cho các kỹ sư operations và platform, và là kiến thức thiết yếu cho các nhà phát triển microservice muốn xuất sắc trong vai trò của mình.

## Vai Trò của Developer trong Observability

Mặc dù triển khai observability và monitoring không chỉ là trách nhiệm của developer, nhưng hiểu các khái niệm này là rất quan trọng để:

- Cộng tác hiệu quả với các team operations và platform
- Cung cấp hướng dẫn và định hướng về các thách thức observability
- Xây dựng các ứng dụng demo với monitoring phù hợp
- Thành công trong các buổi phỏng vấn về microservice developer
- Trở thành developer nổi bật trong dự án của bạn

**Quan trọng**: Trong bất kỳ buổi phỏng vấn microservices nào, bạn sẽ được hỏi về cách triển khai observability và monitoring. Bạn không thể đơn giản nói rằng business logic là trách nhiệm duy nhất của mình - bạn cần hiểu bức tranh toàn cảnh.

## Triển Khai Log Aggregation với Grafana

Khi quản lý logs với Grafana, chúng ta cần sử dụng các công cụ cụ thể từ hệ sinh thái Grafana:

### Các Thành Phần Cốt Lõi

#### 1. Grafana
- Ứng dụng web mã nguồn mở cho phân tích và visualization tương tác
- Cung cấp các tính năng như charts, graphs và alerts
- Kết nối với các công cụ hỗ trợ như Loki và Promtail
- Có thể dễ dàng cài đặt bằng Docker, Docker Compose hoặc Kubernetes
- Công cụ phổ biến được sử dụng bởi các tổ chức ở mọi quy mô, từ startup đến doanh nghiệp lớn

#### 2. Grafana Loki
- Hệ thống log aggregation có khả năng **mở rộng theo chiều ngang**, highly available
- Được thiết kế để lưu trữ bất kỳ số lượng logs nào từ microservices và applications
- Hoạt động như một vị trí lưu trữ tập trung cho tất cả logs của microservice
- Phục vụ như hệ thống log aggregation (tương tự như một thư mục tập trung cho logs)

#### 3. Promtail
- Log agent nhẹ
- Chạy trong cùng network với các containers của bạn
- Đọc tất cả logs được tạo ra từ các containers
- Thu thập và chuyển tiếp logs đến Grafana Loki

### Cách Hệ Thống Log Aggregation Hoạt Động

```
Microservices (Containers)
         ↓
    Promtail (Agent)
         ↓
   Grafana Loki (Storage)
         ↓
  Grafana (Visualization)
```

**Luồng Hoạt Động Hoàn Chỉnh:**

1. **Microservices** chạy trong các containers và tạo ra logs
2. **Promtail** (agent) chạy trong cùng network với các microservice containers
3. Promtail tự động fetch và collect tất cả logs từ các containers
4. Logs được chuyển tiếp đến **Loki** (hệ thống lưu trữ tập trung/log aggregation)
5. **Grafana** tích hợp với Loki để cung cấp khả năng visualization và querying

### Các Lợi Ích Chính

**Không Tốn Công Sức của Developer**: Là developer, bạn không cần làm gì đặc biệt để gửi logs đến Promtail, Loki hoặc Grafana. Hệ thống tự động thu thập logs từ các containers của bạn.

**Centralized Logging (Logging Tập Trung)**: Tất cả logs từ tất cả containers được lưu trữ ở một vị trí tập trung (Loki), giúp dễ dàng troubleshoot trong toàn bộ kiến trúc microservices của bạn.

**Visualization Mạnh Mẽ**: Thay vì phải tìm kiếm thủ công trong các file log, Grafana cung cấp:
- Khám phá logs trực quan
- Khả năng querying nâng cao
- Tìm kiếm dựa trên tiêu chí tùy chỉnh
- Giao diện thống nhất cho tất cả logs của ứng dụng

## Lợi Ích của Grafana, Loki và Promtail Khi Kết Hợp

Khi kết hợp, ba công cụ này cung cấp một giải pháp logging mạnh mẽ giúp bạn:

- **Hiểu** các ứng dụng của bạn tốt hơn
- **Troubleshoot** các vấn đề nhanh chóng và hiệu quả
- **Query** logs dựa trên tiêu chí cụ thể
- **Visualization** dữ liệu log trong giao diện thân thiện với người dùng
- **Scale** theo chiều ngang khi hệ thống của bạn phát triển

## Kết Luận

Hệ sinh thái của Grafana cung cấp các công cụ toàn diện để triển khai observability và monitoring trong microservices. Sự kết hợp của Grafana, Loki và Promtail tạo ra một hệ thống log aggregation tự động, hiệu quả, yêu cầu sự can thiệp tối thiểu từ developer trong khi vẫn cung cấp khả năng mạnh mẽ cho troubleshooting và monitoring.

Trong các phần tiếp theo, chúng ta sẽ đi sâu vào các chi tiết triển khai thực tế và xem các công cụ này hoạt động thông qua các demo.

---

*Hướng dẫn này là một phần của khóa học microservices toàn diện bao gồm Spring Boot và các observability patterns.*



================================================================================
FILE: 65-promtail-to-alloy-migration-guide.md
================================================================================

# Lưu Ý Quan Trọng Về Việc Di Chuyển Từ Promtail

## Promtail Đã Được Thay Thế Bởi Alloy

### Tổng Quan

Từ **Grafana Loki phiên bản 3.0** trở đi, Promtail - công cụ chịu trách nhiệm thu thập các dòng log, đã được thay thế bằng một sản phẩm mới có tên là **Alloy**.

### Những Điều Bạn Cần Biết

Mặc dù các bài giảng sắp tới sẽ thảo luận về Promtail, nhưng **Alloy sẽ hoạt động tương tự**. Vì đây là các thành phần nội bộ của Grafana Loki, nên thay đổi này sẽ không có tác động đáng kể đến việc triển khai của bạn.

### Các Thay Đổi Chính

- **Promtail** (Cũ) → **Alloy** (Hiện tại)
- Alloy phục vụ cùng mục đích: thu thập các dòng log
- Tác động tối thiểu đến kiến trúc microservices của bạn
- Các file cấu hình cần được cập nhật để sử dụng Alloy thay vì Promtail

### Các File Docker Compose Đã Được Cập Nhật

Tất cả các file Docker Compose đã được cập nhật với các thay đổi liên quan đến Alloy bên trong kho lưu trữ GitHub.

### Tài Liệu

Bạn có thể tìm tài liệu đầy đủ về Alloy cùng với Loki tại liên kết sau:

🔗 [Hướng Dẫn Bắt Đầu Nhanh Grafana Loki](https://grafana.com/docs/loki/latest/get-started/quick-start/)

### Làm Việc Với Các Phiên Bản Cũ

Nếu vì lý do nào đó các dự án thực tế của bạn sử dụng **phiên bản cũ của Grafana Loki** (trước phiên bản 3.0), thì bạn sẽ cần sử dụng **Promtail**.

Các thay đổi liên quan đến Promtail có sẵn trong các **nhánh cũ hơn** của kho lưu trữ GitHub của khóa học.

---

## Tóm Tắt

- ✅ Sử dụng **Alloy** cho Grafana Loki 3.0 trở lên
- ✅ Cập nhật các file cấu hình để sử dụng cấu hình Alloy thay vì Promtail
- ✅ Tham khảo kho lưu trữ GitHub cho các file Docker Compose đã được cập nhật
- ⚠️ Chỉ sử dụng Promtail cho các phiên bản Grafana Loki cũ hơn (< 3.0)

---

*Hướng dẫn này là một phần của tài liệu khóa học Microservices với Spring Boot.*



================================================================================
FILE: 66-implementing-log-aggregation-with-grafana-loki-prompttail.md
================================================================================

# Triển Khai Log Aggregation với Grafana, Loki và Promtail

## Tổng Quan

Trong hướng dẫn này, chúng ta sẽ khám phá cách triển khai tập hợp log (log aggregation) trong hệ thống microservices sử dụng Grafana, Loki và Promtail mà không cần thay đổi code của các microservice. Cách tiếp cận này tuân theo khuyến nghị của phương pháp luận 12-factor về việc xử lý logs như các luồng sự kiện.

## Tổng Quan Kiến Trúc

Hệ thống tập hợp log được Grafana khuyến nghị bao gồm nhiều thành phần hoạt động cùng nhau:

### Các Thành Phần

1. **Application Layer (Tầng Ứng Dụng)**: Các microservices của bạn sinh ra và phát ra logs liên tục
2. **Promtail**: Một log agent chạy trong cùng mạng với các ứng dụng
3. **Gateway**: Một edge server định tuyến các request giữa Promtail và Loki
4. **Loki Write Component**: Xử lý dữ liệu log đến từ Promtail
5. **Loki Read Component**: Xử lý các request đọc log từ Grafana
6. **Minio**: Hệ thống lưu trữ nơi logs được lưu giữ
7. **Grafana**: Ứng dụng UI để tìm kiếm và trực quan hóa logs

### Cách Thức Hoạt Động

#### Luồng Thu Thập Log

1. **Sinh Log**: Các microservices liên tục sinh ra logs trong containers của chúng
2. **Thu Thập Log**: Promtail, chạy trong cùng mạng, đọc và thu thập các logs mới khi chúng được tạo ra
3. **Truyền Log**: Promtail gửi các logs đã thu thập đến Gateway (không gửi trực tiếp đến Loki)
4. **Định Tuyến**: Gateway kiểm tra URL được Promtail gọi và chuyển hướng request đến Loki Write Component
5. **Lưu Trữ**: Loki Write Component lưu trữ logs vào Minio, một hệ thống lưu trữ tập trung

#### Luồng Truy Xuất Log

1. **Yêu Cầu Tìm Kiếm**: Developer tìm kiếm logs trong giao diện Grafana
2. **Định Tuyến Gateway**: Request đi đến Gateway, Gateway chuyển tiếp đến Loki Read Component
3. **Truy Xuất Log**: Loki Read Component đọc logs từ Minio
4. **Hiển Thị**: Logs được gửi trả về Grafana nơi developer có thể xem chúng trong UI

## Tại Sao Lại Dùng Kiến Trúc Này?

### Khả Năng Mở Rộng

Loki được thiết kế để xử lý bất kỳ lượng dữ liệu log nào. Đội ngũ Grafana xây dựng các thành phần riêng biệt (Read và Write) để làm cho hệ thống có khả năng mở rộng và xử lý khối lượng lớn logs một cách hiệu quả.

### Phân Tách Trách Nhiệm

Kiến trúc phân tách:
- **Thao tác ghi**: Được xử lý bởi Loki Write Component
- **Thao tác đọc**: Được xử lý bởi Loki Read Component
- **Định tuyến**: Được quản lý bởi Gateway

Sự phân tách này đảm bảo hiệu suất và khả năng mở rộng tối ưu.

## Cách Tiếp Cận Triển Khai

### Những Gì Bạn Cần

Tất cả các thành phần cần thiết đều sẵn có:
- Gateway
- Loki Read Component
- Loki Write Component
- Promtail
- Minio

Bạn không cần phát triển các thành phần này từ đầu. Chúng có thể được triển khai bằng Docker và Docker Compose.

### Các Microservices Của Bạn

Thay vì sử dụng ứng dụng mẫu, các microservices hiện có của bạn sẽ:
- Tiếp tục sinh logs như bình thường
- Không cần thay đổi code
- Logs của chúng được Promtail tự động thu thập

## Tuân Thủ Phương Pháp Luận 12-Factor

Cách tiếp cận này triển khai khuyến nghị **Logs** từ phương pháp luận 12-factor:

> "Xử lý logs như các luồng sự kiện đến đầu ra chuẩn và không quan tâm đến cách chúng được xử lý hoặc lưu trữ."

### Các Nguyên Tắc Chính

- **Microservices không phụ thuộc**: Các microservices và developers không cần lo lắng về việc streaming hay lưu trữ log
- **Xử lý log bên ngoài**: Toàn bộ việc tập hợp log xảy ra từ bên ngoài ứng dụng
- **Không thay đổi code**: Developers có thể tập trung vào logic nghiệp vụ trong khi việc quản lý log được xử lý bên ngoài

## Bắt Đầu

Đội ngũ Grafana cung cấp:
- Tài liệu chính thức với sơ đồ kiến trúc chi tiết
- Các file cấu hình YAML
- Hướng dẫn từng bước

Các tài nguyên này giúp việc triển khai trở nên đơn giản, mặc dù kiến trúc có thể trông phức tạp ban đầu.

## Lợi Ích

1. **Logging Tập Trung**: Tất cả logs được lưu trữ tại một vị trí (Minio + Loki)
2. **Tìm Kiếm Dễ Dàng**: Tìm kiếm logs trên tất cả microservices từ giao diện Grafana
3. **Không Thay Đổi Ứng Dụng**: Triển khai mà không cần sửa code microservice
4. **Khả Năng Mở Rộng**: Xử lý bất kỳ khối lượng dữ liệu log nào
5. **Thân Thiện Với Docker**: Triển khai dễ dàng với Docker Compose

## Các Bước Tiếp Theo

Trong các bài học tiếp theo, chúng ta sẽ thực hiện:
1. Thiết lập cấu hình Docker Compose
2. Triển khai tất cả các thành phần
3. Cấu hình Promtail để thu thập logs từ microservices
4. Sử dụng Grafana để tìm kiếm và trực quan hóa logs

## Tài Nguyên

- Tài liệu chính thức Grafana Loki: Hướng dẫn Bắt đầu
- Các cấu hình YAML được cung cấp bởi đội ngũ Grafana
- GitHub repository với các ví dụ triển khai chi tiết

## Tóm Tắt

Log aggregation với Grafana, Loki và Promtail cung cấp một giải pháp mạnh mẽ, có khả năng mở rộng để quản lý logs trên các microservices. Kiến trúc phân tách trách nhiệm hiệu quả, xử lý bất kỳ khối lượng logs nào, và không yêu cầu thay đổi các microservices hiện có của bạn. Với Docker và các cấu hình được cung cấp, việc triển khai trở nên đơn giản và tuân theo các thực tiễn tốt nhất trong ngành.



================================================================================
FILE: 67-implementing-log-aggregation-with-grafana-loki-promtail.md
================================================================================

# Triển khai Log Aggregation với Grafana, Loki và Promtail

## Tổng quan

Hướng dẫn này sẽ giúp bạn triển khai tập hợp log (log aggregation) trong kiến trúc microservices sử dụng Grafana, Loki và Promtail. Giải pháp này cho phép ghi log tập trung cho các microservices Spring Boot chạy trên Docker.

## Yêu cầu trước khi bắt đầu

- Đã cài đặt Docker trên hệ thống
- Đã cài đặt Docker Compose
- Có sẵn dự án microservices (Section 11)

## Thiết lập dự án ban đầu

### 1. Chuẩn bị Workspace

1. Copy code từ section trước vào workspace của bạn
2. Đổi tên thư mục thành `section11`
3. Xóa các file cấu hình ẩn của IntelliJ IDEA
4. Mở project trong IntelliJ IDEA

### 2. Cập nhật Maven Projects

**Cập nhật Docker Image Tags:**
- Thay đổi tất cả Docker image tags từ `s10` thành `s11` trong các file `pom.xml`
- Build các projects và enable annotation processing

### 3. Cấu hình Timeout cho Gateway Server

Trong file `application.yml` của gateway server:

```yaml
# Tăng response timeout từ 2s lên 10s
response-timeout: 10s
```

**Lý do:** Khi chạy nhiều container trên local với bộ nhớ hạn chế, 2 giây có thể không đủ. Tăng lên 10 giây giúp tránh các vấn đề timeout khi test trên môi trường local.

## Hiểu về Log Aggregation Stack

### Kiến trúc các thành phần

1. **Grafana** - Giao diện trực quan hóa và truy vấn
2. **Loki** - Hệ thống tập hợp log (các thành phần Read/Write)
3. **Promtail** - Agent thu thập log
4. **Minio** - Backend lưu trữ local
5. **Nginx Gateway** - Định tuyến cho các thành phần Loki

## Cấu hình Docker Compose

### Các file YAML cần thiết

Download 3 file cấu hình:
1. `docker-compose.yml`
2. `promtail-local-config.yml`
3. `loki-config.yml`

### Hiểu về docker-compose.yml

#### Cấu hình Network

```yaml
version: "3"
networks:
  loki:
    driver: bridge
```

Tất cả services chạy trên cùng network `loki` để các container có thể giao tiếp với nhau.

#### Loki Read Component

```yaml
services:
  read:
    image: grafana/loki
    command: "-config.file=/etc/loki/config.yaml -target=read"
    ports:
      - "3101:3101"
    volumes:
      - ./loki-config.yml:/etc/loki/config.yaml
    depends_on:
      - minio
    healthcheck:
      # Cấu hình health check
    networks:
      loki:
        aliases:
          - loki
```

**Điểm chính:**
- Expose port `3101`
- Mount file `loki-config.yml` từ local vào container
- Sử dụng anchor `&loki-dns` để tái sử dụng cấu hình network

#### Loki Write Component

```yaml
  write:
    image: grafana/loki
    command: "-config.file=/etc/loki/config.yaml -target=write"
    ports:
      - "3102:3102"
    volumes:
      - ./loki-config.yml:/etc/loki/config.yaml
    depends_on:
      - minio
    networks:
      <<: *loki-dns  # Merge tham chiếu anchor
```

**Điểm chính:**
- Expose port `3102`
- Sử dụng merge operator `<<:` và alias `*loki-dns` để tái sử dụng cấu hình network

#### Promtail Service

```yaml
  promtail:
    image: grafana/promtail
    volumes:
      - ./promtail-local-config.yml:/etc/promtail/config.yml:ro
      - /var/run/docker.sock:/var/run/docker.sock
    command: "-config.file=/etc/promtail/config.yml"
    depends_on:
      - gateway
    networks:
      - loki
```

**Điểm chính:**
- Mount config dưới dạng read-only (`:ro`)
- Truy cập Docker socket để đọc log từ containers
- Phụ thuộc vào gateway để forward log

#### Minio Storage Service

```yaml
  minio:
    image: minio/minio
    entrypoint:
      - sh
      - -euc
      - mkdir -p /data/loki-data /data/loki-ruler && minio server /data
    environment:
      - MINIO_ROOT_USER=loki
      - MINIO_ROOT_PASSWORD=supersecret
    ports:
      - "9000:9000"
    volumes:
      - ./.data/minio:/data
```

**Điểm chính:**
- Tạo thư mục để lưu trữ log khi khởi động
- Lưu log trong thư mục local `.data/minio`
- Có thể thay thế bằng cloud storage (S3) trong môi trường production

#### Grafana Service

```yaml
  grafana:
    image: grafana/grafana
    environment:
      - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
    entrypoint:
      - sh
      - -euc
      - |
        mkdir -p /etc/grafana/provisioning/datasources
        cat <<EOF > /etc/grafana/provisioning/datasources/ds.yml
        apiVersion: 1
        datasources:
          - name: Loki
            type: loki
            access: proxy
            url: http://gateway:3100
        EOF
        /run.sh
    ports:
      - "3000:3000"
    depends_on:
      - gateway
    networks:
      - loki
```

**Điểm chính:**
- Tự động cấu hình Loki datasource khi khởi động
- Expose UI trên port `3000`
- Kết nối với Loki thông qua gateway tại port `3100`

#### Nginx Gateway Service

```yaml
  gateway:
    image: nginx
    depends_on:
      - read
      - write
    entrypoint:
      - sh
      - -euc
      - |
        # Cấu hình routing Nginx
        # Route /loki/api/v1/push tới write component
        # Route các API khác tới read component
    ports:
      - "3100:3100"
    networks:
      - loki
```

**Điểm chính:**
- Route các write requests tới write component (port 3100)
- Route các read/query requests tới read component
- Cung cấp điểm truy cập duy nhất cho Loki services

### Hiểu về promtail-local-config.yml

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

clients:
  - url: http://gateway:3100/loki/api/v1/push

scrape_configs:
  - job_name: flog_scrape
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
```

**Điểm chính:**
- Lắng nghe trên port `9080` cho HTTP
- Push log tới gateway tại port `3100`
- Scrape log từ Docker containers qua socket
- Refresh mỗi 5 giây
- Gán nhãn log với tên container

### Hiểu về loki-config.yml

```yaml
server:
  http_listen_port: 3100

common:
  storage:
    s3:
      endpoint: minio:9000
      bucketnames: loki-data
      access_key_id: loki
      secret_access_key: supersecret
      s3forcepathstyle: true
```

**Điểm chính:**
- Loki lắng nghe trên port `3100`
- Sử dụng Minio làm storage tương thích S3
- Lưu log trong bucket `loki-data`
- Có thể cấu hình cho cloud storage trong production

## Các khái niệm YAML được sử dụng

### Volumes
Map files/directories từ host vào container:
```yaml
volumes:
  - ./local-file.yml:/container/path/file.yml:ro
```

### Anchors và Aliases
Tạo các khối cấu hình có thể tái sử dụng:
```yaml
networks:
  loki:
    aliases:
      - loki
  &loki-dns  # Định nghĩa anchor

# Tham chiếu sau:
networks:
  <<: *loki-dns  # Merge nội dung anchor
```

### Merge Operator
`<<:` merge cấu hình được tham chiếu vào khối hiện tại

## Các bước triển khai

1. **Download các file cấu hình**
   - Đặt cả 3 file YAML vào cùng thư mục với file Docker Compose của bạn

2. **Cập nhật Docker Compose**
   - Tích hợp cấu hình Loki stack
   - Xóa service `flog` (không cần thiết cho microservices thực tế)

3. **Cấu hình Microservices**
   - Đảm bảo microservices tạo ra log đúng cách
   - Không cần thay đổi code để thu thập log

4. **Khởi động Stack**
   ```bash
   docker-compose up -d
   ```

5. **Truy cập Grafana**
   - Mở trình duyệt tại `http://localhost:3000`
   - Đăng nhập với thông tin mặc định
   - Bắt đầu truy vấn log từ Loki datasource

## Cân nhắc cho môi trường Production

### Lưu trữ
- Thay thế Minio bằng cloud storage (AWS S3, Azure Blob Storage, GCS)
- Cập nhật `loki-config.yml` với thông tin đăng nhập cloud provider

### Hiệu năng
- Điều chỉnh scrape intervals dựa trên khối lượng log
- Cấu hình retention policies
- Scale các read/write components khi cần

### Bảo mật
- Thay đổi mật khẩu mặc định
- Sử dụng secrets management
- Enable authentication trên Grafana

## Lợi ích

1. **Log tập trung** - Tất cả log của microservices ở một nơi
2. **Dễ dàng debug** - Tìm kiếm trên tất cả services cùng lúc
3. **Khả năng quan sát** - Hiểu rõ hơn về hành vi hệ thống
4. **Có thể mở rộng** - Xử lý log từ nhiều microservices

## Các bước tiếp theo

- Tích hợp cấu hình vào Docker Compose hiện có
- Test thu thập log từ microservices của bạn
- Tạo custom Grafana dashboards
- Thiết lập alerting dựa trên log patterns

## Tóm tắt

Implementation này cung cấp giải pháp log aggregation hoàn chỉnh cho microservices sử dụng:
- **Promtail** để thu thập log từ Docker containers
- **Loki** để lưu trữ và đánh index log hiệu quả
- **Grafana** để trực quan hóa và truy vấn
- **Minio** để lưu trữ local (có thể thay thế bằng cloud storage)

Giải pháp này sẵn sàng cho production với các điều chỉnh cấu hình phù hợp cho môi trường cụ thể của bạn.



================================================================================
FILE: 68-implementing-loki-promtail-docker-compose-configuration.md
================================================================================

# Triển Khai Loki và Promtail trong Cấu Hình Docker Compose

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cấu hình Grafana Loki và Promtail để tổng hợp log trong kiến trúc microservices Spring Boot sử dụng Docker Compose.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Dự án microservices Spring Boot
- Hiểu biết cơ bản về Docker Compose
- IntelliJ IDEA (hoặc IDE bất kỳ)

## Bước 1: Tải Xuống Các File Cấu Hình

Đầu tiên, tải xuống các file cấu hình cần thiết:
- `loki-config.yml`
- `promtail-local-config.yml`

Các file cấu hình này rất quan trọng cho việc thiết lập dịch vụ Loki và Promtail.

## Bước 2: Tạo Cấu Trúc Thư Mục

Tạo cấu trúc thư mục có tổ chức cho các công cụ observability:

```
observability/
├── loki/
│   └── loki-config.yml
└── promtail/
    └── promtail-local-config.yml
```

### Tạo Các Thư Mục

1. Tạo thư mục mới tên `observability` trong thư mục gốc dự án
2. Trong `observability`, tạo thư mục `loki`
3. Copy file `loki-config.yml` vào thư mục `loki`
4. Tạo thư mục `promtail` trong `observability`
5. Copy file `promtail-local-config.yml` vào thư mục `promtail`

## Bước 3: Cập Nhật File Docker Compose

### Chọn Profile Môi Trường

Chọn file Docker Compose để chỉnh sửa (default, prod, hoặc qa). Trong ví dụ này, chúng ta sẽ sử dụng file `docker-compose.yml` trong thư mục `prod`.

Sau khi test trong prod, cấu hình tương tự có thể được copy sang các profile khác.

### Xóa Các Service Không Cần Thiết

Để tối ưu tài nguyên hệ thống, xóa container Redis (từ phần rate limiter pattern trước đó):

1. Xóa định nghĩa service Redis
2. Xóa các biến môi trường liên quan đến Redis khỏi cấu hình gateway server
3. Xóa các dependency Redis khỏi gateway server

### Cập Nhật Version Tags

Thay thế tất cả các tag `s10` bằng tag `s11` để sử dụng phiên bản mới nhất của các service.

## Bước 4: Thêm Các Service Loki và Promtail

### Cấu Hình Loki Read Component

Thêm service Loki read với các lưu ý sau:

**Cấu Hình Volume:**
```yaml
volumes:
  - ./observability/loki/loki-config.yml:/etc/loki/config.yml
```

**Cấu Hình Network:**
- Thay đổi tên network từ `loki` thành `easybank` (khớp với common-config.yml của bạn)
- Giữ alias là `loki` để tham chiếu nội bộ
- Đặt anchor cho cấu hình với tên `loki-dns`

### Cấu Hình Loki Write Component

Tương tự như read component:
- Cập nhật đường dẫn volume để trỏ đến `./observability/loki/loki-config.yml`
- Sử dụng cùng cấu hình network `loki-dns`
- Đảm bảo nó tham chiếu đến network `easybank`

### Cấu Hình Promtail Service

**Cấu Hình Volume:**
```yaml
volumes:
  - ./observability/promtail/promtail-local-config.yml:/etc/promtail/config.yml
```

**Cấu Hình Network:**
Thay vì hardcode tên network, tham chiếu đến cấu hình chung:

```yaml
extends:
  file: common-config.yml
  service: network-deploy-service
```

### Cấu Hình MinIO Service

Chỉ cập nhật cấu hình network để sử dụng pattern extends:

```yaml
extends:
  file: common-config.yml
  service: network-deploy-service
```

### Cấu Hình Grafana Service

Cập nhật cấu hình network để sử dụng pattern extends, tương tự như các service khác.

### Cập Nhật Gateway Service

Cuộn xuống cuối định nghĩa gateway service và thêm cấu hình network sử dụng pattern extends.

## Bước 5: Tạo Docker Images

Tạo Docker images mới với tag `S11` cho tất cả các microservices để đảm bảo tương thích với cấu hình đã cập nhật.

## Tổng Kết

Trong quá trình triển khai này, chúng ta đã:

1. ✅ Tạo cấu trúc thư mục có tổ chức cho cấu hình Loki và Promtail
2. ✅ Cập nhật file Docker Compose với volume mappings phù hợp
3. ✅ Cấu hình network settings để sử dụng cấu hình chung
4. ✅ Thêm các service Loki (read/write), Promtail, MinIO và Grafana
5. ✅ Tối ưu hóa thiết lập bằng cách xóa các service không cần thiết (Redis)
6. ✅ Cập nhật tất cả các tag service lên phiên bản S11

## Các Bước Tiếp Theo

Sau khi tạo Docker images, bạn có thể:
- Test thiết lập log aggregation
- Truy cập Grafana dashboards
- Xem các log được tổng hợp từ tất cả microservices
- Cấu hình các truy vấn log và cảnh báo tùy chỉnh

## Lợi Ích

Thiết lập Grafana Loki và Promtail cung cấp:
- Tổng hợp log tập trung
- Truy vấn và lọc log dễ dàng
- Phân tích log trực quan thông qua Grafana
- Lưu trữ log có khả năng mở rộng với MinIO
- Giám sát log thời gian thực trên các microservices

---

*Lưu ý: Đảm bảo tất cả các file cấu hình được đặt đúng vị trí trong các thư mục tương ứng trước khi chạy Docker Compose.*



================================================================================
FILE: 69-log-aggregation-with-grafana-loki-promtail-implementation.md
================================================================================

# Triển khai Thu thập Log Tập trung với Grafana, Loki và Promtail

## Tổng quan

Hướng dẫn này trình bày cách triển khai thu thập log tập trung trong kiến trúc microservices sử dụng Grafana, Loki và Promtail, mà không cần thay đổi bất kỳ dòng code nào trong các microservices hiện có.

## Yêu cầu tiên quyết

- Docker và Docker Compose đã được cài đặt
- Nhiều microservices (Accounts, Cards, Loans, Gateway Server, Eureka Server)
- Các Docker images đã được build với tag `s11`

## Các thành phần kiến trúc

### 1. **Grafana**
- Nền tảng trực quan hóa và phân tích dựa trên web
- Chạy trên cổng 3000
- Cung cấp giao diện người dùng để tìm kiếm và xem logs

### 2. **Loki**
- Hệ thống thu thập log của Grafana Labs
- Lưu trữ và đánh index logs hiệu quả
- Tách thành các thành phần đọc và ghi để tăng khả năng mở rộng

### 3. **Promtail**
- Agent thu thập logs
- Scrape logs từ các Docker containers
- Đẩy logs lên Loki

### 4. **Minio**
- Object storage để lưu trữ logs lâu dài
- Giải pháp thay thế cục bộ cho cloud storage (AWS S3)

## Các bước triển khai

### Bước 1: Cấu hình Docker Compose

Đảm bảo file `docker-compose.yml` của bạn bao gồm tất cả các services cần thiết với căn lề đúng:

```yaml
services:
  # Microservices
  accounts:
    # ... cấu hình
  
  cards:
    # ... cấu hình
  
  loans:
    # ... cấu hình
  
  gateway:
    # ... cấu hình
  
  # Log aggregation stack
  grafana:
    # ... cấu hình
  
  loki-read:
    # ... cấu hình
  
  loki-write:
    # ... cấu hình
  
  promtail:
    # ... cấu hình
  
  minio:
    # ... cấu hình
```

**Quan trọng**: Đảm bảo căn lề YAML đúng. Tất cả services phải có cùng mức độ căn lề.

### Bước 2: Cấu hình Data Source cho Grafana

Cấu hình Grafana để kết nối với Loki tự động qua Docker Compose entry point:

```yaml
grafana:
  entrypoint:
    - sh
    - -euc
    - |
      mkdir -p /etc/grafana/provisioning/datasources
      cat <<EOF > /etc/grafana/provisioning/datasources/ds.yaml
      apiVersion: 1
      datasources:
        - name: Loki
          type: loki
          access: proxy
          url: http://loki-read:3100
          jsonData:
            httpHeaderName1: "X-Scope-OrgID"
          secureJsonData:
            httpHeaderValue1: "tenant1"
      EOF
      /run.sh
```

### Bước 3: Cấu hình Promtail

Cấu hình Promtail để scrape logs từ Docker containers:

```yaml
scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log
    relabel_configs:
      - source_labels: ['__path__']
        target_label: 'container'
```

Label `container` sẽ chứa tên Docker container để dễ dàng lọc.

### Bước 4: Cấu hình Storage

Mount local storage cho Minio:

```yaml
minio:
  volumes:
    - ./data/minio:/data
```

Điều này tạo thư mục `.data` trong thư mục làm việc của bạn để lưu trữ logs cục bộ.

## Triển khai

### 1. Di chuyển đến Production Profile

```bash
cd section_11/docker-compose/prod
```

### 2. Khởi động tất cả Services

```bash
docker-compose up -d
```

### 3. Kiểm tra trạng thái Container

Đợi 1-2 phút để tất cả containers khởi động. Kiểm tra logs của gateway server để xác nhận:

```bash
docker logs gatewayserver-ms
```

Tìm dòng: "Started Gateway server successfully"

## Xử lý sự cố

### Vấn đề căn lề YAML

Nếu gặp lỗi khi chạy `docker-compose up`, kiểm tra căn lề YAML:
- Chọn các services bị lệch
- Nhấn `Shift + Tab` để di chuyển chúng về lại một mức căn lề
- Đảm bảo tất cả services ở cùng mức độ

### Vấn đề tài nguyên thấp

Nếu containers không khởi động được do thiếu memory/CPU:

```yaml
healthcheck:
  interval: 20s  # Tăng từ 10s
  retries: 20    # Tăng từ 10
```

## Kiểm tra thiết lập

### 1. Tạo Logs

Sử dụng Postman hoặc bất kỳ API client nào để gọi các endpoints của microservices:

```http
POST http://localhost:8080/api/create
GET http://localhost:8080/api/fetchCustomerDetails?mobileNumber=1234567890
```

### 2. Truy cập Grafana

Mở trình duyệt và truy cập:
```
http://localhost:3000
```

### 3. Xem Logs trong Grafana

1. Click vào **Toggle Menu** → **Connections** → **Data Sources**
2. Xác nhận data source Loki đã được cấu hình
3. Điều hướng đến phần **Explore**
4. Chọn label: `container`
5. Chọn tên container (ví dụ: `accounts-ms`, `cards-ms`, `gateway-ms`)
6. Click **Run Query**

### 4. Live Streaming

Bật live streaming để xem logs theo thời gian thực khi chúng được tạo (làm mới mỗi 5 giây).

## Lọc Log nâng cao

### Lọc theo nội dung văn bản

Tìm kiếm các mẫu văn bản cụ thể trong logs:

1. Chọn container (ví dụ: `gateway-ms`)
2. Chọn loại filter: **Line contains**
3. Nhập từ khóa tìm kiếm (ví dụ: `easybank-correlation-id`)
4. Click **Run Query**

### Các tùy chọn Filter có sẵn

- **Line contains**: Tìm kiếm văn bản không phân biệt chữ hoa chữ thường
- **Line does not contain**: Loại trừ các dòng có văn bản cụ thể
- **Line contains case sensitive**: Khớp chính xác chữ hoa chữ thường
- **Regex match**: Tìm kiếm dựa trên pattern
- **Line filter expression**: Biểu thức LogQL nâng cao

## Vị trí lưu trữ Log

### Development cục bộ

Logs được lưu trữ tại:
```
section_11/docker-compose/prod/.data/
├── loki-data/
└── loki-ruler/
```

### Triển khai Production

Đối với production, thay thế Minio bằng cloud storage:
- **AWS S3**
- **Google Cloud Storage**
- **Azure Blob Storage**

Điều này cho phép lưu trữ logs không giới hạn cho bất kỳ số lượng microservices nào.

## Lợi ích chính

### 1. **Không thay đổi Code**
Không cần sửa đổi code trong microservices - hoàn toàn là giải pháp dựa trên infrastructure.

### 2. **Truy cập tập trung**
Tất cả logs của microservices có thể truy cập từ một giao diện duy nhất.

### 3. **Kiến trúc có khả năng mở rộng**
Hỗ trợ 100+ microservices trong môi trường production.

### 4. **Tìm kiếm mạnh mẽ**
Tìm kiếm trên tất cả logs sử dụng text filters, regex và LogQL queries.

### 5. **Giám sát thời gian thực**
Live streaming hiển thị logs khi chúng được tạo ra.

## Development cục bộ vs Production

### Development cục bộ
- Sử dụng console output của IDE
- Đặt breakpoints để debug
- Truy cập trực tiếp vào application logs
- Không cần thiết lập log aggregation phức tạp

### Môi trường Dev/Production
- Triển khai Grafana + Loki + Promtail
- Quản lý log tập trung
- Cộng tác giữa các nhóm phát triển
- Bắt buộc đối với microservices phân tán

## Cấu hình Health Check

Cấu hình health checks phù hợp cho container orchestration:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
  interval: 10s
  timeout: 5s
  retries: 10
  start_period: 40s
```

## Best Practices (Thực hành tốt nhất)

1. **Phân bổ tài nguyên**: Đảm bảo đủ CPU, memory và RAM cho production
2. **Hợp tác với Platform Team**: Làm việc với platform team để cấu hình cloud storage
3. **Chính sách lưu giữ Log**: Định nghĩa logs nên được lưu trong bao lâu
4. **Kiểm soát truy cập**: Triển khai xác thực phù hợp cho Grafana trong production
5. **Phân đoạn mạng**: Sử dụng Docker networks để cô lập services

## Các trụ cột của Observability (Khả năng quan sát)

Triển khai này giải quyết trụ cột **Logs** của observability:

✅ **Logs** - Thu thập log tập trung (đã đề cập trong hướng dẫn này)  
⏭️ **Metrics** - Các chỉ số hiệu suất ứng dụng (chủ đề tiếp theo)  
⏭️ **Traces** - Distributed tracing qua các services

## Triển khai Correlation ID

Hướng dẫn đề cập đến việc sử dụng correlation IDs (ví dụ: `easybank-correlation-id`) để theo dõi requests qua các microservices. Điều này giúp:

- Theo dõi một request duy nhất qua nhiều services
- Debug các distributed transactions
- Phân tích hiệu suất của các flows end-to-end

## Kết luận

Bây giờ bạn đã có một hệ thống thu thập log hoàn chỉnh:
- Thu thập logs từ tất cả microservices tự động
- Cung cấp tìm kiếm và trực quan hóa tập trung
- Không yêu cầu thay đổi code ứng dụng
- Mở rộng để hỗ trợ kiến trúc microservices lớn

Giải pháp này giúp các developers hiểu trạng thái bên trong của microservices và nhanh chóng xử lý sự cố trong môi trường phân tán.

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **Metrics** - trụ cột thứ hai của observability và monitoring cho microservices.



================================================================================
FILE: 7-service-discovery-and-registration-challenge.md
================================================================================

# Thách Thức về Service Discovery và Registration trong Microservices

## Tổng Quan

Phần này giới thiệu **Thách thức #5** khi xây dựng microservices: cách các microservices khám phá lẫn nhau và đăng ký chính mình trong mạng lưới microservices.

## Vấn Đề Cốt Lõi

Khi xây dựng kiến trúc microservices, chúng ta cần giải quyết một vấn đề cơ bản: **Làm thế nào để các microservices xác định vị trí và giao tiếp với nhau trong một môi trường động?**

## Các Thách Thức Chính

### 1. Định Vị Service Động

**Câu hỏi:** Làm thế nào một microservice xác định vị trí các microservices khác trong mạng?

**Vấn đề:**
- Trong ứng dụng nguyên khối (monolithic), các service có endpoint và port cố định
- Trong microservices, các container được tạo và hủy động dựa trên yêu cầu
- Endpoint thay đổi liên tục trong quá trình scaling hoặc thay thế container
- Việc theo dõi địa chỉ IP thủ công trở nên không thể thực hiện trong môi trường động

**Ví dụ tình huống:**
Khi scale up hoặc thay thế container không khỏe mạnh, địa chỉ IP mới được gán. Các microservices khác không thể theo dõi những thay đổi này nếu không có cơ chế phù hợp.

### 2. Đăng Ký Instance Service

**Câu hỏi:** Làm thế nào một instance service mới có thể tham gia vào mạng microservices?

**Vấn đề:**
- Triển khai production có thể bắt đầu với một instance cho mỗi microservice (accounts, loans, cards)
- Trong lúc traffic cao, số instance có thể scale từ 1 lên 5 hoặc nhiều hơn
- Các instance mới cần thông báo sự hiện diện của chúng cho các service khác
- Không có đăng ký phù hợp, các instance đã scale sẽ không bao giờ được gọi

**Ví dụ tình huống:**
- Thiết lập ban đầu: 1 instance cho mỗi microservice accounts, loans, và cards
- Đợt traffic tăng đột biến kích hoạt scaling lên 5 instance mỗi loại
- Microservice accounts có thể vẫn nghĩ chỉ có 1 instance loans tồn tại
- 4 instance loans mới sẽ vô hình nếu không có service registration đúng cách

### 3. Cân Bằng Tải Giữa Các Instance

**Câu hỏi:** Cân bằng tải hoạt động như thế nào khi nhiều instance của một microservice được triển khai?

**Vấn đề:**
- Nhiều container song song của cùng một microservice chạy đồng thời
- Các microservice client cần phân phối traffic đều
- Không có cân bằng tải, một instance bị quá tải trong khi các instance khác nhàn rỗi

**Ví dụ tình huống:**
- Microservice accounts gọi microservice loans
- Microservice loans có 5 container đang chạy
- Instance nào nên xử lý request?
- Traffic nên được phân phối đều, không chỉ gửi đến một instance

## Giải Pháp

Để vượt qua những thách thức này, chúng ta triển khai ba pattern chính:

### 1. **Service Discovery (Khám Phá Service)**
Cho phép các microservices tìm và định vị các service khác một cách động trong mạng.

### 2. **Service Registration (Đăng Ký Service)**
Cho phép các microservices đăng ký chính mình và thông báo tính khả dụng của chúng cho mạng.

### 3. **Load Balancing (Cân Bằng Tải)**
Phân phối các request đến một cách đều đặn giữa nhiều instance của một microservice.

## Tại Sao Các Pattern Này Quan Trọng

- **Môi Trường Động:** Container được tạo, hủy và thay thế liên tục
- **Khả Năng Mở Rộng:** Scale up và down liền mạch mà không cần cấu hình thủ công
- **Tính Sẵn Sàng Cao:** Tự động phát hiện và định tuyến tránh các instance không khỏe mạnh
- **Sử Dụng Tài Nguyên Hiệu Quả:** Phân phối tải đúng cách đảm bảo tận dụng tài nguyên tối ưu

## Những Điểm Chính Cần Nhớ

- Microservices hoạt động trong môi trường động nơi endpoint thay đổi liên tục
- Theo dõi thủ công vị trí service là không thực tế và dễ lỗi
- Service discovery, registration và load balancing là các pattern thiết yếu
- Các pattern này cho phép quản lý service tự động trong kiến trúc microservices
- Triển khai đúng cách đảm bảo khả năng mở rộng, độ tin cậy và sử dụng tài nguyên hiệu quả

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Service discovery hoạt động như thế nào chi tiết
- Triển khai các cơ chế service registration
- Các chiến lược cân bằng tải cho microservices
- Công cụ và framework hỗ trợ các pattern này (ví dụ: Eureka, Consul, Kubernetes)

---

*Tài liệu này là một phần của chuỗi bài về kiến trúc microservices tập trung vào Spring Boot và Java.*



================================================================================
FILE: 70-metrics-and-monitoring-with-prometheus-grafana.md
================================================================================

# Metrics và Giám Sát trong Microservices: Giới Thiệu về Prometheus và Grafana

## Tổng Quan

Hướng dẫn này giới thiệu trụ cột thứ hai của khả năng quan sát và giám sát trong kiến trúc microservices: **Metrics (Số liệu)**. Trong khi logging giúp chúng ta hiểu các sự kiện cụ thể, metrics cung cấp thông tin chi tiết toàn diện về tình trạng và hiệu suất của ứng dụng.

## Tại Sao Metrics Quan Trọng

### Hạn Chế Của Việc Chỉ Sử Dụng Logs

Event logs giúp chúng ta hiểu điều gì đã xảy ra trong các tình huống hoặc phương thức cụ thể, nhưng chúng có những hạn chế:
- Không thể cung cấp trạng thái sức khỏe tổng thể của microservices
- Không đưa ra thông tin chi tiết về hiệu suất theo thời gian thực
- Thiếu các chế độ xem tổng hợp trên nhiều instances

### Metrics Cung Cấp Gì

Metrics cung cấp các phép đo số về hiệu suất ứng dụng, bao gồm:
- Mức sử dụng CPU
- Mức sử dụng bộ nhớ
- Mức sử dụng heap dump
- Số lượng threads
- Connection pools
- Tỷ lệ lỗi
- Và nhiều chỉ số hiệu suất khác

## Các Thành Phần Của Kiến Trúc Giám Sát

### 1. Spring Boot Actuator

**Vai trò**: Tạo metrics ở mức microservice

- Expose (công khai) metrics cho mỗi microservice instance
- Truy cập qua endpoint `/actuator/metrics`
- Cung cấp các metrics ứng dụng toàn diện ngay từ đầu
- Phải được thêm vào dưới dạng dependency cho tất cả microservices

**Thách thức**: Kiểm tra thủ công các actuator endpoints cho nhiều instances rất tốn thời gian và không thực tế ở quy mô lớn (hãy tưởng tượng 100 microservices với nhiều instances mỗi cái).

### 2. Micrometer

**Vai trò**: Chuyển đổi định dạng metrics và trừu tượng hóa vendor

Micrometer đóng vai trò như một facade quan sát ứng dụng trung lập với vendor, tương tự như SLF4J đối với logging.

#### Tính Năng Chính:
- Chuyển đổi metrics từ Spring Boot Actuator từ định dạng JSON sang các định dạng cụ thể cho từng hệ thống giám sát
- Cung cấp giao diện trung lập với vendor để thu thập metrics
- Hỗ trợ nhiều hệ thống giám sát thông qua các dependencies khác nhau

#### Các Vendor Được Hỗ Trợ:
- Prometheus
- App Optics
- Azure Monitor
- CloudWatch
- Datadog
- Dynatrace
- Elastic
- Graphite
- OpenTelemetry
- Và nhiều hơn nữa

#### Tương Tự Với SLF4J:
Giống như SLF4J (Simple Logging Framework for Java) trừu tượng hóa các logging frameworks (Java Util Logging, Log4j, Logback), Micrometer trừu tượng hóa việc thu thập metrics cho các hệ thống giám sát khác nhau.

**Triển Khai**: Chỉ cần thêm dependency Micrometer dành riêng cho vendor (ví dụ: micrometer-prometheus), và nó sẽ xử lý mọi độ phức tạp ở phía sau.

### 3. Prometheus

**Vai trò**: Tổng hợp và lưu trữ metrics

- Giải pháp giám sát mã nguồn mở
- Định kỳ scrape (thu thập) metrics từ các microservice containers
- Tổng hợp metrics từ tất cả các instances vào một vị trí duy nhất
- Tương tự như Loki (tổng hợp logs), nhưng dành cho metrics
- Cung cấp UI để giám sát và trực quan hóa cơ bản

#### Khả Năng Chính:
- Thu thập metrics từ các microservices riêng lẻ
- Lưu trữ metrics được hợp nhất ở một vị trí
- Xây dựng các dashboards và đồ thị cơ bản
- Cho phép giám sát tập trung

### 4. Grafana

**Vai trò**: Trực quan hóa nâng cao và cảnh báo

#### Tại Sao Cần Grafana Khi Đã Có Prometheus?

Mặc dù Prometheus cung cấp giám sát cơ bản, nhưng nó có những hạn chế:
- Không thể xây dựng các dashboards phức tạp, có thể tùy chỉnh
- Khả năng cảnh báo và thông báo hạn chế

#### Ưu Điểm Của Grafana:
- Tạo các dashboards tinh vi, tương tác
- Cung cấp hệ thống cảnh báo và thông báo nâng cao
- Tích hợp liền mạch với Prometheus (tương tự như tích hợp Loki)
- Cung cấp công cụ trực quan hóa cấp chuyên nghiệp

## Quy Trình Giám Sát

1. **Tạo Metrics**: Spring Boot Actuator expose metrics ở định dạng JSON
2. **Chuyển Đổi Định Dạng**: Micrometer chuyển đổi metrics sang định dạng tương thích với Prometheus
3. **Tổng Hợp**: Prometheus định kỳ scrape và hợp nhất metrics từ tất cả các instances
4. **Trực Quan Hóa**: Grafana truy vấn Prometheus để xây dựng dashboards và thiết lập cảnh báo

## Chiến Lược Triển Khai

Giải pháp giám sát hoàn chỉnh bao gồm:

1. Thêm Spring Boot Actuator dependency vào tất cả microservices
2. Thêm Micrometer Prometheus dependency để chuyển đổi định dạng
3. Cấu hình Prometheus để scrape các metrics endpoints
4. Tích hợp Prometheus với Grafana
5. Xây dựng các custom dashboards trong Grafana
6. Thiết lập cảnh báo và thông báo khi vượt ngưỡng

## Lợi Ích Của Giám Sát Dựa Trên Metrics

- **Giám Sát Sức Khỏe Theo Thời Gian Thực**: Đội ngũ vận hành có thể liên tục giám sát tình trạng microservices
- **Theo Dõi Hiệu Suất**: Xác định các điểm nghẽn và suy giảm hiệu suất
- **Cảnh Báo Chủ Động**: Nhận thông báo trước khi các vấn đề trở nên nghiêm trọng
- **Khả Năng Mở Rộng**: Giám sát hàng trăm microservices và instances một cách hiệu quả
- **Phân Tích Lịch Sử**: Theo dõi xu hướng hiệu suất theo thời gian
- **Lập Kế Hoạch Năng Lực**: Đưa ra quyết định sáng suốt về phân bổ tài nguyên

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ triển khai từng bước các thành phần này và chứng minh cách chúng hoạt động cùng nhau để cung cấp giám sát toàn diện cho các ứng dụng microservices.

---

**Tóm Tắt**: Metrics là yếu tố thiết yếu để giám sát tình trạng và hiệu suất của microservices. Sự kết hợp của Spring Boot Actuator, Micrometer, Prometheus và Grafana cung cấp một giải pháp giám sát mạnh mẽ, có khả năng mở rộng, cho phép các đội ngũ vận hành duy trì các kiến trúc microservices hoạt động tốt và hiệu suất cao.



================================================================================
FILE: 71-implementing-micrometer-prometheus-microservices.md
================================================================================

# Triển khai Micrometer và Prometheus trong Microservices

## Tổng quan

Hướng dẫn này sẽ trình bày cách triển khai Micrometer và Prometheus để giám sát các microservices. Việc tích hợp này cho phép bạn xuất các metrics của actuator ở định dạng mà Prometheus có thể hiểu được, từ đó giúp giám sát hiệu quả kiến trúc microservices của bạn.

## Yêu cầu trước khi bắt đầu

- Các microservices Spring Boot (Accounts, Loans, Cards)
- Config Server
- Eureka Server
- Gateway Server
- Công cụ build Maven

## Các bước triển khai

### Bước 1: Thêm dependency Micrometer

Thêm dependency Micrometer Prometheus registry vào file `pom.xml` của mỗi microservice, ngay sau dependency actuator:

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

**Những điểm quan trọng:**
- Dependency này yêu cầu Micrometer xuất các metrics của actuator ở định dạng Prometheus
- Nếu tổ chức của bạn sử dụng hệ thống giám sát khác, chỉ cần thay đổi `artifactId`
- Thêm dependency này vào tất cả các microservices: Accounts, Loans, Cards, Eureka Server, Config Server và Gateway Server

### Bước 2: Cấu hình thuộc tính ứng dụng

Thêm thuộc tính sau vào file `application.yml` của mỗi microservice trong phần `management`:

```yaml
management:
  metrics:
    tags:
      application: ${spring.application.name}
```

**Mục đích:**
- Thuộc tính này nhóm tất cả metrics của mỗi microservice dưới tên ứng dụng của nó
- Giúp xác định metrics nào thuộc về microservice nào
- Giá trị được gán động từ thuộc tính `spring.application.name`

### Bước 3: Build và khởi động các services

1. **Clean Build**: Thực hiện clean Maven build cho tất cả các microservices

2. **Khởi động các services theo thứ tự**:
   - Khởi động **Config Server** đầu tiên
   - Khởi động **Eureka Server** thứ hai
   - Khởi động các microservices **Accounts**, **Loans** và **Cards** (có thể khởi động song song)
   - Khởi động **Gateway Server** cuối cùng

### Bước 4: Kiểm tra các endpoints metrics

#### Endpoint Actuator Metrics

Truy cập endpoint metrics tổng quát của bất kỳ microservice nào:

```
http://localhost:8080/actuator/metrics
```

Endpoint này hiển thị tất cả các metrics có sẵn được xuất bởi actuator.

#### Chi tiết metrics cụ thể

Để xem chi tiết của một metric cụ thể:

```
http://localhost:8080/actuator/metrics/system.cpu.usage
http://localhost:8080/actuator/metrics/process.uptime
```

**Ví dụ Response:**
- CPU usage: Hiển thị mức sử dụng CPU hiện tại (ví dụ: 0.0)
- Process uptime: Hiển thị service đã chạy được bao lâu (ví dụ: 172 giây)

#### Endpoint Prometheus

Endpoint quan trọng cho việc tích hợp Prometheus:

```
http://localhost:8080/actuator/prometheus
```

Endpoint này xuất tất cả metrics ở định dạng Prometheus, mà Prometheus sẽ thu thập (scrape) theo các khoảng thời gian đều đặn (ví dụ: mỗi 5, 10 hoặc 60 giây tùy theo cấu hình).

### Cổng của các Microservices

| Service | Cổng |
|---------|------|
| Accounts | 8080 |
| Loans | 8090 |
| Cards | 9000 |
| Eureka Server | 8070 |
| Config Server | 8071 |
| Gateway Server | 8072 |

### Danh sách kiểm tra

Kiểm tra endpoint Prometheus cho tất cả các services:

- ✓ Accounts: `http://localhost:8080/actuator/prometheus`
- ✓ Loans: `http://localhost:8090/actuator/prometheus`
- ✓ Cards: `http://localhost:9000/actuator/prometheus`
- ✓ Eureka Server: `http://localhost:8070/actuator/prometheus`
- ✓ Config Server: `http://localhost:8071/actuator/prometheus`
- ✓ Gateway Server: `http://localhost:8072/actuator/prometheus`

## Lợi ích chính

1. **Ít thay đổi code**: Chỉ cần thêm dependency và cấu hình
2. **Metrics chuẩn hóa**: Tất cả metrics được xuất ở định dạng tương thích với Prometheus
3. **Giám sát dễ dàng**: Prometheus tự động thu thập metrics từ tất cả các microservices
4. **Linh hoạt**: Có thể chuyển sang các hệ thống giám sát khác bằng cách thay đổi artifact ID
5. **Khả năng quan sát tập trung**: Tất cả metrics của microservices có sẵn trong một hệ thống giám sát

## Cách hoạt động

1. **Micrometer** đóng vai trò như một facade để thu thập metrics
2. **Prometheus registry** định dạng metrics theo chuẩn tương thích với Prometheus
3. **Prometheus server** định kỳ thu thập (scrape) endpoint `/actuator/prometheus`
4. Metrics được gắn thẻ với tên ứng dụng để dễ dàng nhận diện
5. Tất cả metrics có sẵn để truy vấn và trực quan hóa

## Tóm tắt

Bằng cách thêm dependency Micrometer Prometheus và cấu hình các thuộc tính ứng dụng, tất cả các microservices giờ đây đã xuất các metrics của actuator ở định dạng mà Prometheus có thể hiểu được. Điều này cho phép giám sát toàn diện và khả năng quan sát trên toàn bộ kiến trúc microservices của bạn mà không cần thay đổi nhiều logic nghiệp vụ hoặc code Java.



================================================================================
FILE: 72-setting-up-prometheus-and-grafana-integration.md
================================================================================

# Thiết Lập Tích Hợp Prometheus và Grafana cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập Prometheus để giám sát microservices và tích hợp với Grafana để trực quan hóa dữ liệu. Chúng ta sẽ cấu hình Prometheus để thu thập metrics từ các microservices Spring Boot và thiết lập kết nối với Grafana bằng Docker Compose.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Các microservices Spring Boot đang expose metrics qua Actuator và Micrometer
- Có cấu trúc thư mục observability trong dự án
- Các microservices đang chạy (accounts, loans, cards, gateway server, Eureka, config server)

## Bước 1: Tạo Cấu Hình Prometheus

Đầu tiên, tạo một thư mục mới cho Prometheus bên trong thư mục observability:

```
observability/
  └── prometheus/
      └── prometheus.yml
```

### File Cấu Hình Prometheus (prometheus.yml)

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'accounts'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['accounts:8080']
  
  - job_name: 'loans'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['loans:8090']
  
  - job_name: 'cards'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['cards:9000']
  
  - job_name: 'gatewayserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['gatewayserver:8072']
  
  - job_name: 'eurekaserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['eurekaserver:8070']
  
  - job_name: 'configserver'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['configserver:8071']
```

### Giải Thích Cấu Hình

- **scrape_interval**: Prometheus thu thập metrics từ microservices mỗi 5 giây
- **evaluation_interval**: Prometheus đánh giá và cập nhật dashboard mỗi 5 giây
- **scrape_configs**: Định nghĩa các job cho từng microservice
  - **job_name**: Định danh microservice đang được giám sát
  - **metrics_path**: Đường dẫn mà Actuator expose metrics Prometheus (`/actuator/prometheus`)
  - **static_configs/targets**: Tên service và port theo định dạng mạng Docker

## Bước 2: Cấu Hình Prometheus trong Docker Compose

Thêm service Prometheus vào file `docker-compose.yml` trong profile prod:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    extends:
      file: network-deploy-service.yml
      service: network-deploy-service
```

### Chi Tiết Cấu Hình

- **image**: Image Docker chính thức của Prometheus
- **ports**: Expose giao diện Prometheus UI trên port 9090
- **volumes**: Mount file cấu hình prometheus.yml vào container
- **extends**: Đảm bảo Prometheus chạy trong cùng mạng Docker với các microservices khác

## Bước 3: Tạo Cấu Hình Data Source cho Grafana

Tạo thư mục Grafana bên trong observability và thêm file cấu hình datasource:

```
observability/
  └── grafana/
      └── datasource.yml
```

### Cấu Hình Data Source (datasource.yml)

```yaml
apiVersion: 1

deleteDatasources:
  - name: Prometheus
  - name: Loki

datasources:
  - name: Prometheus
    type: prometheus
    uid: prometheus-uid
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: "5s"
  
  - name: Loki
    type: loki
    uid: loki-uid
    access: proxy
    url: http://loki:3100
    editable: true
```

### Giải Thích Cấu Hình

- **apiVersion**: Phiên bản API chuẩn cho datasources của Grafana
- **deleteDatasources**: Xóa các datasources hiện có cùng tên để tránh xung đột
- **datasources**: Định nghĩa chi tiết kết nối cho Prometheus và Loki
  - **url**: Sử dụng tên service Docker (prometheus:9090, loki:3100) cho giao tiếp mạng nội bộ
  - **access**: Chế độ proxy cho phép Grafana truy cập data sources thay mặt người dùng

## Bước 4: Cập Nhật Service Grafana trong Docker Compose

Thay thế cấu hình entrypoint trước đó của Grafana bằng volume mount:

```yaml
services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./observability/grafana/datasource.yml:/etc/grafana/provisioning/datasources/datasource.yml
    extends:
      file: network-deploy-service.yml
      service: network-deploy-service
```

### Những Thay Đổi Chính

- **Đã xóa**: Các lệnh entrypoint phức tạp tạo ds.yml trực tiếp
- **Đã thêm**: Volume mount cho file datasource.yml
- **Lợi ích**: Cấu hình Docker Compose gọn gàng hơn với định nghĩa data source được tách riêng

## Bước 5: Triển Khai với Docker Compose

1. Dừng tất cả các instances đang chạy
2. Khởi động các services:

```bash
docker-compose -f docker-compose-prod.yml up -d
```

3. Kiểm tra các services đang chạy:

```bash
docker-compose -f docker-compose-prod.yml ps
```

## Truy Cập Các Services

- **Prometheus UI**: http://localhost:9090
- **Grafana Dashboard**: http://localhost:3000

## Các Bước Kiểm Tra

1. Mở Prometheus UI và điều hướng đến Status > Targets để xác minh tất cả microservices đang được scrape
2. Mở Grafana và kiểm tra Configuration > Data Sources để xác nhận kết nối Prometheus và Loki
3. Tạo dashboards trong Grafana sử dụng Prometheus làm data source

## Kiến Trúc Mạng

Tất cả các services chạy trong cùng một mạng Docker, cho phép service discovery theo tên:
- Microservices expose metrics tại `/actuator/prometheus`
- Prometheus scrape metrics sử dụng tên service (ví dụ: `accounts:8080`)
- Grafana kết nối với Prometheus sử dụng `prometheus:9090`

## Thực Hành Tốt Nhất

1. **Scrape Interval**: Điều chỉnh dựa trên nhu cầu giám sát và ràng buộc tài nguyên
2. **Service Discovery**: Sử dụng tên service Docker thay vì localhost cho giao tiếp giữa các container
3. **Quản Lý Data Source**: Sử dụng provisioning files (datasource.yml) thay vì cấu hình thủ công
4. **Lưu Trữ Volume**: Cân nhắc thêm volumes để lưu trữ dữ liệu Prometheus trong môi trường production

## Khắc Phục Sự Cố

- **Targets Down**: Kiểm tra xem microservices có đang chạy và expose metrics không
- **Connection Refused**: Xác minh tất cả services đều trong cùng mạng Docker
- **Không Có Dữ Liệu trong Grafana**: Xác nhận Prometheus đang scrape metrics thành công từ targets

## Các Bước Tiếp Theo

- Cấu hình các dashboards Grafana tùy chỉnh cho microservices của bạn
- Thiết lập các alerting rules trong Prometheus
- Khám phá các Grafana dashboards có sẵn cho ứng dụng Spring Boot

## Kết Luận

Bạn đã thiết lập thành công Prometheus để thu thập metrics và tích hợp với Grafana để trực quan hóa. Stack observability này cho phép giám sát thời gian thực kiến trúc microservices của bạn.



================================================================================
FILE: 73-prometheus-monitoring-demo-and-integration.md
================================================================================

# Demo Giám Sát Prometheus và Tích Hợp với Grafana

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và sử dụng Prometheus để giám sát các microservices trong ứng dụng Spring Boot, bao gồm tích hợp với Grafana để nâng cao khả năng trực quan hóa.

## Yêu Cầu Tiên Quyết

- Đã cài đặt Docker và Docker Compose
- Các microservices đã cấu hình dependencies Micrometer
- Đã cập nhật `application.yml` và `pom.xml` với cấu hình Micrometer

## Tái Tạo Docker Images

Trước khi khởi động containers, đảm bảo tất cả Docker images được tái tạo với các thay đổi mã nguồn mới nhất liên quan đến Micrometer:

1. **Cập Nhật Dependencies**: Đảm bảo `pom.xml` bao gồm các dependencies Micrometer
2. **Cấu Hình Metrics**: Cập nhật `application.yml` với cấu hình endpoints Prometheus
3. **Tái Tạo Images**: Tạo Docker images mới với tag (ví dụ: S11) sau khi thực hiện thay đổi

```bash
# Build images cho tất cả microservices
docker build -t <tên-service>:S11 .
```

## Khởi Động Services với Docker Compose

Di chuyển đến thư mục Docker Compose và khởi động tất cả services:

```bash
# Di chuyển đến thư mục docker-compose
cd docker-compose/prod

# Khởi động tất cả services ở chế độ detached
docker compose up -d
```

Đợi 1-2 phút để tất cả containers khởi động hoàn toàn.

## Kiểm Tra Trạng Thái Container

### Sử Dụng Docker Desktop

1. Mở Docker Desktop
2. Kiểm tra tất cả containers đang ở trạng thái "Running"
3. Xác minh container Prometheus đang chạy trên port 9090
4. Xác nhận Gateway Server đã khởi động thành công

### Kiểm Tra Actuator Endpoints

Kiểm tra endpoint actuator Prometheus cho bất kỳ microservice nào:

```
GET http://localhost:<port>/actuator/prometheus
```

Ví dụ cho accounts microservice:
```
GET http://localhost:8080/actuator/prometheus
```

Bạn sẽ nhận được dữ liệu metrics ở định dạng Prometheus.

## Truy Cập Dashboard Prometheus

### Xem Targets

1. Mở trình duyệt và truy cập: `http://localhost:9090/targets`
2. Xem tất cả microservices được giám sát và trạng thái sức khỏe của chúng
3. Click "unhealthy" để xem các instances lỗi
4. Click "all" để xem tất cả containers được giám sát

**Các Services Dự Kiến:**
- accounts
- cards
- configserver
- eurekaserver
- gatewayserver
- loans

### Xem Chi Tiết Target

Click "show more" trên bất kỳ target nào để xem:
- Trạng thái (up/down)
- Thông tin label
- Chi tiết cấu hình job
- Thời gian scrape cuối cùng
- Thời gian scrape

## Làm Việc với Metrics và Graphs

### Tìm Kiếm Metrics

1. Di chuyển đến tab "Graph"
2. Tìm kiếm metrics cụ thể trong ô query
3. Click "Execute" để hiển thị dữ liệu

### Các Metrics Phổ Biến

**Sử Dụng CPU:**
```
system_cpu_usage
```

**Thời Gian Hoạt Động Process:**
```
process_uptime_seconds
```

**Thông Tin Thread:**
```
jvm_threads_live
jvm_threads_daemon
```

**Metrics Kết Nối Database:**
```
hikaricp_connections_active
hikaricp_connections_idle
```

### Trực Quan Hóa Dữ Liệu

**Chế Độ Xem Bảng:**
- Click "Execute" để xem giá trị metrics ở định dạng bảng
- Hiển thị dữ liệu cho tất cả instances microservice

**Chế Độ Xem Đồ Thị:**
- Click tab "Graph" để xem trực quan hóa chuỗi thời gian
- Di chuột qua các đường để làm nổi bật dữ liệu microservice cụ thể
- Điều chỉnh khoảng thời gian (ví dụ: 15 phút, 1 giờ)
- Phóng to/thu nhỏ để xem rõ hơn

**Kiểu Đồ Thị:**
- Chuyển đổi giữa các kiểu trực quan hóa khác nhau
- Lọc để hiển thị metrics microservice cụ thể
- Xem dữ liệu service riêng lẻ hoặc kết hợp

### Metrics Explorer

Để khám phá các metrics có sẵn:

1. Click biểu tượng quả địa cầu trong query builder
2. Duyệt danh sách đầy đủ các metrics được theo dõi
3. Chọn bất kỳ metric nào để thêm vào query của bạn
4. Metrics được thu thập tự động thông qua tích hợp Micrometer

## Tùy Chỉnh Dashboard

### Tùy Chọn Theme

- Click biểu tượng chuyển đổi theme để chuyển giữa chế độ tối và sáng
- Chế độ sáng cung cấp khả năng phân biệt màu tốt hơn cho nhiều đồ thị

### Lựa Chọn Khoảng Thời Gian

- Sử dụng bộ chọn khoảng thời gian để tập trung vào các giai đoạn cụ thể
- Khoảng thời gian ngắn hơn cung cấp độ phân giải đồ thị chi tiết hơn
- Các khoảng phổ biến: 5m, 15m, 1h, 6h, 24h

## Giám Sát Sức Khỏe Container

### Giám Sát Trạng Thái Sức Khỏe

Prometheus liên tục giám sát sức khỏe microservice bằng cách:
- Định kỳ scrape các endpoints `/actuator/prometheus`
- Đánh dấu services là "up" khi phản hồi thành công
- Đánh dấu services là "down" khi không thể truy cập

### Kiểm Tra Phát Hiện Sức Khỏe

**Mô Phỏng Lỗi Service:**

1. Dừng một container microservice (ví dụ: cards service)
2. Đợi 10-15 giây để Prometheus phát hiện lỗi
3. Refresh trang targets
4. Service đã dừng xuất hiện màu đỏ trong "unhealthy"
5. Click "show more" để xem chi tiết lỗi (ví dụ: "no such host")

**Khôi Phục Service:**

1. Khởi động lại container đã dừng
2. Đợi 10-15 giây để Prometheus phát hiện khôi phục
3. Refresh trang targets
4. Service quay trở lại trạng thái "healthy" với state "up"

## Hạn Chế của Prometheus

Mặc dù Prometheus cung cấp khả năng giám sát thiết yếu, nó có hạn chế cho môi trường doanh nghiệp:

- **Trực Quan Hóa Hạn Chế**: Chức năng đồ thị cơ bản có thể không đủ cho nhu cầu giám sát phức tạp
- **Xem Metric Đơn Lẻ**: UI mặc định tập trung vào metrics riêng lẻ thay vì dashboards toàn diện
- **Không Có UI Quản Lý Alert**: Thiếu dashboard cảnh báo tích hợp
- **Phân Tích Lịch Sử Hạn Chế**: Trực quan hóa chuỗi thời gian cơ bản

## Tích Hợp với Grafana

Đối với môi trường production và các dự án phức tạp, tích hợp Prometheus với Grafana để có được:

- **Dashboards Nâng Cao**: Tạo dashboards toàn diện, đa metrics
- **Trực Quan Hóa Tốt Hơn**: Các loại biểu đồ phong phú và tùy chọn tùy chỉnh
- **Quản Lý Alert**: Cấu hình và quản lý cảnh báo trực quan
- **Template Variables**: Lọc dashboard động
- **Tương Quan Dữ Liệu**: Kết hợp metrics từ nhiều nguồn

### Cấu Hình Grafana

Tích hợp Grafana được cấu hình thông qua cài đặt data source:

1. Thêm Prometheus làm data source trong Grafana
2. Cấu hình URL Prometheus (thường là `http://prometheus:9090`)
3. Kiểm tra kết nối
4. Tạo dashboards sử dụng metrics Prometheus

## Thực Hành Tốt Nhất

1. **Giám Sát Thường Xuyên**: Kiểm tra trang targets Prometheus thường xuyên để xem sức khỏe service
2. **Lựa Chọn Metric**: Chọn metrics liên quan dựa trên yêu cầu giám sát của bạn
3. **Tối Ưu Khoảng Thời Gian**: Điều chỉnh khoảng thời gian để đồ thị rõ ràng tối ưu
4. **Cấu Hình Alert**: Thiết lập quy tắc cảnh báo cho các metrics quan trọng
5. **Lập Kế Hoạch Tài Nguyên**: Giám sát CPU, bộ nhớ và metrics connection pool để lập kế hoạch năng lực
6. **Tổ Chức Dashboard**: Sử dụng Grafana để tổ chức metrics thành các dashboards logic

## Khắc Phục Sự Cố

### Service Hiển Thị Down

1. Kiểm tra xem container có đang chạy trong Docker Desktop không
2. Xác minh service có thể truy cập trên port được chỉ định
3. Kiểm tra logs service để tìm lỗi khởi động
4. Đảm bảo endpoint `/actuator/prometheus` được kích hoạt

### Không Hiển Thị Metrics

1. Xác minh dependencies Micrometer trong `pom.xml`
2. Kiểm tra `application.yml` cho cấu hình Prometheus
3. Đảm bảo Docker images đã được tái tạo sau khi thay đổi cấu hình
4. Xác minh cấu hình scrape Prometheus

### Vấn Đề Kết Nối

1. Kiểm tra cấu hình mạng Docker
2. Xác minh service discovery đang hoạt động chính xác
3. Đảm bảo quy tắc firewall cho phép giao tiếp giữa các containers
4. Kiểm tra file cấu hình Prometheus cho định nghĩa target chính xác

## Kết Luận

Prometheus cung cấp nền tảng vững chắc cho giám sát microservices với thu thập metrics thời gian thực và trực quan hóa cơ bản. Đối với các ứng dụng doanh nghiệp yêu cầu khả năng giám sát nâng cao, tích hợp Prometheus với Grafana mang lại dashboards giám sát toàn diện và thông tin chi tiết vận hành nâng cao.

## Các Bước Tiếp Theo

- Khám phá tạo dashboard Grafana
- Cấu hình quy tắc cảnh báo trong Prometheus
- Thiết lập lưu trữ metrics dài hạn
- Triển khai metrics tùy chỉnh trong microservices của bạn
- Tạo service-level objectives (SLOs) dựa trên metrics đã thu thập



================================================================================
FILE: 74-grafana-prometheus-integration-demo.md
================================================================================

# Demo Tích Hợp Grafana và Prometheus

## Tổng Quan

Hướng dẫn này trình bày cách tích hợp giữa Grafana và Prometheus để giám sát các microservices. Grafana cung cấp khả năng trực quan hóa mạnh mẽ cho các số liệu được thu thập bởi Prometheus, giúp việc giám sát và phân tích kiến trúc microservices của bạn trở nên dễ dàng hơn.

## Yêu Cầu Trước Khi Bắt Đầu

- Grafana đang chạy trên cổng 3000
- Prometheus đã được cấu hình và đang chạy
- Các microservices đã được cấu hình với các endpoint metrics của Prometheus

## Truy Cập Grafana

1. Mở trình duyệt và truy cập Grafana tại cổng 3000
2. Bạn sẽ thấy trang chủ của Grafana

## Quản Lý Kết Nối Nguồn Dữ Liệu

### Xem Các Kết Nối Hiện Có

1. Nhấp vào biểu tượng **menu** trong Grafana
2. Điều hướng đến **Connections** (Kết nối)
3. Trong phần Connections, bạn có thể:
   - Tạo kết nối mới
   - Xem các kết nối hiện có trong **Data Sources** (Nguồn Dữ Liệu)

### Các Nguồn Dữ Liệu Đã Cấu Hình

Hiện tại, đã có hai kết nối được cấu hình:
- **Loki** - Để tổng hợp và tìm kiếm log
- **Prometheus** - Để thu thập và trực quan hóa metrics

## Cấu Hình Prometheus

### Chi Tiết Kết Nối

Kết nối Prometheus được cấu hình bằng cách sử dụng file `datasource.yml` nằm trong thư mục `observability/grafana`. Các thông tin cấu hình chính:

- **URL**: `prometheus:9090`
- Kết nối giữa Prometheus và Grafana được thiết lập sử dụng các cài đặt này

### Xem Cấu Hình Prometheus

1. Nhấp vào tab **Prometheus** trong phần Data Sources
2. Xem lại tất cả chi tiết cấu hình từ file `datasource.yml`

## Khám Phá Metrics với Prometheus

### Truy Cập Trang Explore

1. Điều hướng đến trang **Home** (Trang chủ)
2. Nhấp vào nút **Explore** (Khám phá)

### Truy Vấn System CPU Usage

#### Tạo Truy Vấn Cơ Bản

1. Chọn **Prometheus** làm nguồn dữ liệu
2. Trong phần **Metric**, chọn `system_cpu_usage`
3. Chọn **Label** là `application`
4. Tùy chọn, lọc theo microservice cụ thể hoặc để trống để xem tất cả các services
5. Nhấp **Run Query** (Chạy Truy Vấn)

#### Xem Kết Quả

- Biểu đồ sẽ hiển thị dữ liệu cho một giờ gần nhất theo mặc định
- Mỗi màu đại diện cho một microservice khác nhau:
  - Accounts service
  - Cards service
  - Config Server
  - Eureka Server
  - Loans service
  - Gateway Server

#### Tùy Chỉnh Khoảng Thời Gian

- Thay đổi khoảng thời gian (ví dụ: 15 phút) để cập nhật biểu đồ tương ứng
- Biểu đồ sẽ tự động làm mới với khoảng thời gian mới

### Tùy Chọn Trực Quan Hóa

Grafana cung cấp nhiều kiểu trực quan hóa:

- **Lines** - Biểu đồ đường
- **Bars** - Biểu đồ cột
- **Points** - Hiển thị điểm dữ liệu
- **Stack Lines** - Biểu đồ đường xếp chồng
- **Stacked Bars** - Biểu đồ cột xếp chồng

Chọn kiểu phù hợp nhất với nhu cầu giám sát của bạn.

## Truy Vấn Nâng Cao

### Thêm Nhiều Metrics

1. Nhấp vào nút **Add Query** để tạo các truy vấn bổ sung
2. Ví dụ: Thêm metric `up`
   - Chọn metric: `up`
   - Chọn label: `job`
   - Chạy truy vấn

### Xem Các Metrics Kết Hợp

Khi có nhiều truy vấn đang hoạt động:
- Biểu đồ hiển thị thông tin kết hợp từ tất cả các metrics
- Các metrics khác nhau được hiển thị rõ ràng trong chế độ xem dạng đường
- Đường ở trên cùng có thể chỉ ra một metric (ví dụ: `up`)
- Các biểu đồ phía dưới hiển thị các metrics khác (ví dụ: `system_cpu_usage`)

### Các Phương Pháp Tốt Nhất

- Mặc dù bạn có thể thêm nhiều metrics, nhưng nên **tìm kiếm một metric tại một thời điểm** để rõ ràng hơn
- Cách tiếp cận này giúp phân tích trở nên đơn giản và dễ hiểu hơn

## Những Điểm Chính Cần Nhớ

- **Grafana** cung cấp khả năng trực quan hóa vượt trội so với giao diện tích hợp của Prometheus
- **Prometheus** thu thập và lưu trữ dữ liệu metrics
- **Tích hợp** giữa hai công cụ tạo ra một giải pháp giám sát mạnh mẽ
- File `datasource.yml` quản lý cấu hình kết nối
- Nhiều microservices có thể được giám sát đồng thời
- Các tùy chọn truy vấn và trực quan hóa linh hoạt cho phép giám sát toàn diện

## Các Bước Tiếp Theo

Demo này bao gồm các kiến thức cơ bản về tích hợp Grafana và Prometheus. Còn rất nhiều điều để khám phá với cả hai công cụ, bao gồm:

- Tạo dashboard tùy chỉnh
- Thiết lập cảnh báo
- Kỹ thuật truy vấn nâng cao
- Chia sẻ và cộng tác dashboard

Tiếp tục khám phá các công cụ mạnh mẽ này để xây dựng giải pháp giám sát toàn diện cho kiến trúc microservices của bạn.

---

**Lưu ý**: Hướng dẫn này là một phần của loạt bài về giám sát microservices sử dụng các ứng dụng Java Spring Boot.



================================================================================
FILE: 75-monitoring-microservices-with-grafana-prometheus-dashboards.md
================================================================================

# Giám Sát Microservices với Grafana và Prometheus Dashboards

## Tổng Quan

Hướng dẫn này trình bày khả năng mạnh mẽ của Grafana và Prometheus khi làm việc cùng nhau để giám sát các microservices Java Spring Boot. Chúng ta sẽ khám phá cách thiết lập các dashboard có sẵn và tạo các giải pháp giám sát tùy chỉnh cho kiến trúc microservices của bạn.

## Dashboard Có Sẵn Từ Grafana

### Tìm Kiếm Dashboard Template

1. Truy cập [tài liệu Prometheus](https://prometheus.io) → Get Started → tab Visualization
2. Vào phần Grafana cung cấp thông tin về:
   - Cài đặt Grafana
   - Tạo nguồn dữ liệu Prometheus
   - Xây dựng biểu đồ Prometheus với Grafana

3. Truy cập [kho dashboard Grafana](https://grafana.com/grafana/dashboards/) nơi đội ngũ Grafana và cộng đồng mã nguồn mở đã xây dựng nhiều dashboard được cấu hình sẵn

### Các Tùy Chọn Dashboard Có Sẵn

Thư viện dashboard Grafana bao gồm trực quan hóa cho:
- Dữ liệu Jira
- MongoDB
- Kubernetes
- Datadog
- JVM ecosystem
- Và nhiều thành phần khác

## Thiết Lập Dashboard JVM

### Bước 1: Tìm Kiếm Dashboard JVM

1. Tìm kiếm "JVM" trong kho dashboard Grafana
2. Tìm các dashboard có lượng tải xuống cao (ví dụ: 5+ triệu lượt tải)
3. Chọn một dashboard JVM Micrometer phổ biến

### Bước 2: Import Dashboard

1. Đăng nhập vào Grafana instance của bạn:
   - Thông tin đăng nhập mặc định: `admin` / `admin`
   - Bỏ qua thông báo đổi mật khẩu (tùy chọn)

2. Điều hướng đến Menu → New → Import
3. Dán URL dashboard từ kho Grafana
4. Click "Load"
5. Chọn nguồn dữ liệu Prometheus từ dropdown
6. Click "Import"

### Bước 3: Xem Các Chỉ Số Dashboard

Sau khi import, dashboard hiển thị các chỉ số toàn diện bao gồm:

- **Uptime**: Thông tin thời gian hoạt động của service
- **Start Time**: Khi nào service được khởi động
- **Sử Dụng Bộ Nhớ**:
  - Sử dụng Heap
  - Sử dụng Non-heap
- **Chỉ Số Hiệu Suất**:
  - Thời lượng
  - Tỷ lệ sử dụng
  - Tỷ lệ lỗi
- **Chi Tiết JVM**:
  - JVM heap
  - JVM non-heap
  - Thông tin Thread
- **Chỉ Số Hệ Thống**:
  - Sử dụng CPU
  - Sự kiện Log
  - Áp lực Garbage collector
- **Memory Spaces**:
  - Eden Space
  - Survivor Space
  - Tenured Gen

### Giám Sát Nhiều Microservices

- Chuyển đổi giữa các microservices bằng cách chọn các instance khác nhau từ dropdown
- Ví dụ: Xem chỉ số cho microservice `accounts:8080` hoặc `cards`
- Tất cả trực quan hóa dashboard tự động cập nhật dựa trên service đã chọn

## Thiết Lập Dashboard Spring Boot System Monitor

### Bước 1: Tìm Dashboard Spring Boot

1. Điều hướng đến dashboards Grafana
2. Tìm kiếm "Spring Boot"
3. Chọn "Spring Boot 2.1 System Monitor" (492K+ lượt tải)
4. Copy URL dashboard

### Bước 2: Import và Cấu Hình

1. Trong Grafana, vào New → Import
2. Dán URL dashboard
3. Click "Load"
4. Chọn nguồn dữ liệu Prometheus
5. Click "Import"

### Bước 3: Tùy Chỉnh Khoảng Thời Gian

- Chế độ xem mặc định hiển thị dữ liệu giờ gần nhất
- Điều chỉnh theo khoảng thời gian ưa thích (ví dụ: 15 phút gần nhất)
- Chọn các microservices khác nhau để xem chỉ số cụ thể của chúng

## Tạo Dashboard Tùy Chỉnh

### Tại Sao Tạo Dashboard Tùy Chỉnh?

Đôi khi các dashboard có sẵn không đáp ứng các yêu cầu cụ thể. Dashboard tùy chỉnh cho phép bạn:
- Giám sát các chỉ số cụ thể liên quan đến ứng dụng của bạn
- Tổ chức thông tin theo nhu cầu của nhóm
- Tập trung vào các chỉ số hiệu suất chính

### Hướng Dẫn Từng Bước Tạo Dashboard Tùy Chỉnh

#### 1. Tạo Dashboard Mới

1. Điều hướng đến Dashboards → New → New Dashboard
2. Lưu dashboard với tên mô tả (ví dụ: "easybank")
3. Lưu vào thư mục phù hợp (ví dụ: "General")

#### 2. Thêm Row cho Microservice

1. Click "Add" → Chọn "Row"
2. Cấu hình cài đặt row
3. Đặt tiêu đề: "Accounts Microservice"
4. Click "Update"

#### 3. Thêm Trực Quan Hóa Uptime

1. Click "Add" → "Add Visualization"
2. Cấu hình panel:
   - **Tên panel**: "Uptime"
   - **Nguồn dữ liệu**: Prometheus
   - **Metric**: `process_uptime_seconds`
   - **Label**: application
   - **Value**: accounts microservice

3. Chọn loại trực quan hóa:
   - Time series (mặc định)
   - Bar charts
   - Statistics
   - Gauge
   - Bar gauge
   - Pie chart

4. Click "Apply"
5. Kéo panel xuống dưới row "Accounts Microservice"

#### 4. Thêm Trực Quan Hóa Trạng Thái Service

1. Click "Add Visualization"
2. Cấu hình panel:
   - **Nguồn dữ liệu**: Prometheus
   - **Metric**: `up`
   - **Label filter**: job
   - **Value**: accounts
   - **Tiêu đề panel**: "Up"

3. Chọn kiểu "Gauge" cho biểu đồ
4. Click "Apply"
5. Định vị panel phù hợp (ví dụ: kéo sang phía bên phải)

#### 5. Thêm Nhiều Panel Hơn

Tiếp tục thêm các row và panel cần thiết để giám sát:
- Sử dụng bộ nhớ
- Tỷ lệ request
- Tỷ lệ lỗi
- Kết nối database
- Chỉ số ứng dụng tùy chỉnh

### Tổ Chức Panels

- Kéo và thả các panel để sắp xếp chúng một cách logic
- Nhóm các chỉ số liên quan dưới cùng một row
- Thu gọn/mở rộng các row để quản lý độ phức tạp của dashboard

## Quản Lý Dashboard

### Lưu Dashboard

- Click nút "Save" thường xuyên để bảo toàn các thay đổi
- Cung cấp tên mô tả để dễ dàng nhận dạng
- Tổ chức các dashboard trong thư mục

### Truy Cập Dashboard

1. Điều hướng đến menu Dashboards
2. Xem tất cả các dashboard có sẵn
3. Chọn bất kỳ dashboard nào để xem chỉ số thời gian thực

## Lợi Ích của Grafana và Prometheus

### Cho Đội Ngũ Phát Triển

- **Giám Sát Thời Gian Thực**: Khả năng hiển thị tức thì về tình trạng microservice
- **Phân Tích Lịch Sử**: Xem xét hiệu suất trong quá khứ và xác định xu hướng
- **Khắc Phục Sự Cố Nhanh Chóng**: Nhanh chóng xác định vấn đề khi chúng xảy ra

### Cho Đội Ngũ Vận Hành

- **Khả Năng Hiển Thị Toàn Diện**: Giám sát toàn bộ hệ sinh thái microservices
- **Template Có Sẵn**: Tận dụng dashboard cộng đồng để bắt đầu nhanh chóng
- **Tùy Chỉnh**: Tạo dashboard chuyên biệt cho nhu cầu cụ thể

## Thực Hành Tốt Nhất

1. **Bắt Đầu với Dashboard Có Sẵn**: Sử dụng template cộng đồng làm nền tảng
2. **Tùy Chỉnh Dần Dần**: Thêm panel tùy chỉnh khi nhu cầu cụ thể phát sinh
3. **Tổ Chức Hợp Lý**: Nhóm các chỉ số liên quan lại với nhau
4. **Đặt Khoảng Thời Gian Phù Hợp**: Cân bằng chi tiết với hiệu suất
5. **Giám Sát Chỉ Số Chính**: Tập trung vào các chỉ số quan trọng nhất đối với ứng dụng của bạn

## Kết Luận

Grafana và Prometheus cung cấp khả năng giám sát mạnh mẽ cho các microservices Spring Boot. Bằng cách tận dụng các dashboard có sẵn và tạo trực quan hóa tùy chỉnh, đội ngũ phát triển và vận hành có thể duy trì khả năng hiển thị toàn diện vào hệ thống phân tán của họ.

### Điểm Chính Cần Nhớ

- Dashboard có sẵn cung cấp thiết lập nhanh cho nhu cầu giám sát phổ biến
- Dashboard tùy chỉnh cung cấp tính linh hoạt cho yêu cầu cụ thể
- Nhà phát triển nên hiểu các kiến thức cơ bản về giám sát
- Đội ngũ platform/vận hành nên tìm hiểu sâu hơn về khả năng của Grafana

### Học Tập Nâng Cao

Đối với nhà phát triển, những kiến thức cơ bản được đề cập ở đây là đủ cho công việc hàng ngày. Tuy nhiên, nếu bạn quan tâm đến việc trở thành chuyên gia Grafana (đặc biệt cho vai trò platform hoặc vận hành), hãy cân nhắc đăng ký một khóa học Grafana toàn diện bao gồm các chủ đề nâng cao chi tiết.

## Bước Tiếp Theo

Với các dashboard đã được cấu hình, các thành viên trong nhóm có thể nhanh chóng đánh giá tình trạng tổng thể của microservices bất cứ lúc nào. Nền tảng giám sát này cho phép phát hiện vấn đề chủ động và giải quyết sự cố nhanh hơn.



================================================================================
FILE: 76-configuring-grafana-alerts-for-microservices.md
================================================================================

# Cấu Hình Cảnh Báo Grafana Cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình cảnh báo và thông báo trong Grafana để giám sát microservices. Bạn sẽ học cách thiết lập các quy tắc cảnh báo, định nghĩa ngưỡng và cấu hình các kênh thông báo để nhận cảnh báo khi các điều kiện cụ thể được đáp ứng.

## Yêu Cầu Tiên Quyết

- Grafana đã được cài đặt và đang chạy
- Prometheus làm nguồn dữ liệu
- Microservices với metrics được expose
- Docker Desktop (để kiểm thử)

## Tạo Quy Tắc Cảnh Báo

### Bước 1: Điều Hướng Đến Alerting

1. Mở menu Grafana
2. Chọn tùy chọn **Alerting**
3. Nhấp vào **Alert Rules**
4. Nhấp **Create Alert Rule**

### Bước 2: Cấu Hình Thiết Lập Cảnh Báo Cơ Bản

1. **Rule Name**: Nhập tên mô tả (ví dụ: `accounts`)
2. **Alert Type**: Chọn **Grafana managed alert**
   - Điều này cho phép Grafana quản lý các cảnh báo

### Bước 3: Định Nghĩa Tiêu Chí Cảnh Báo

#### Cấu Hình Nguồn Dữ Liệu

1. **Data Source**: Chọn `Prometheus`
2. **Metric**: Chọn metric `up`
   - Metric này cho biết liệu ứng dụng có đang chạy hay không
   - Giá trị `1` = ứng dụng đang chạy
   - Giá trị `0` = ứng dụng đã dừng

3. **Labels**: Cấu hình như sau:
   - **Label**: `job`
   - **Value**: `accounts microservice`

#### Hàm Reduce

1. Chọn hàm **Reduce**
2. Chọn **Last** làm loại hàm
   - Điều này kích hoạt cảnh báo dựa trên giá trị cuối cùng nhận được
3. Đặt **Input**: Query A
4. Đặt **Mode**: Strict

#### Cấu Hình Ngưỡng

1. Định nghĩa điều kiện cảnh báo: **IS BELOW** `1`
   - Khi giá trị metric `up` giảm xuống dưới 1, cảnh báo được kích hoạt
   - Điều này cho biết microservice đã dừng

## Tổ Chức Cảnh Báo

### Cấu Trúc Thư Mục

1. Tạo thư mục: `accounts`
   - Tổ chức tất cả các cảnh báo liên quan đến accounts

### Nhóm Cảnh Báo

1. Tạo nhóm: `accounts`
2. Đặt **Evaluation Interval**: `10s`
   - Tần suất Grafana đánh giá cảnh báo
   - Giá trị tối thiểu là 10 giây

3. Đặt **Evaluation Period**: `30s`
   - Thời gian chờ trước khi gửi thông báo
   - Ngăn chặn cảnh báo giả

## Chi Tiết Cảnh Báo

### Tóm Tắt và Mô Tả

1. **Summary**: `Account service is down`
2. **Description**: Cung cấp thông tin hành động (ví dụ: `please do something`)

### Lưu Quy Tắc

1. Nhấp **Save rule and exit**
2. Cảnh báo sẽ xuất hiện ở trạng thái **Normal** khi dịch vụ đang chạy

## Cấu Hình Kênh Thông Báo

### Điểm Liên Hệ

Grafana hỗ trợ nhiều kênh thông báo:

- Email
- Webhook
- Slack
- Microsoft Teams
- Telegram
- Discord
- Cisco Webex Teams
- PagerDuty
- Và nhiều hơn nữa

### Thiết Lập Thông Báo Webhook

#### Bước 1: Tạo URL Webhook

1. Truy cập [webhook.site](https://webhook.site) hoặc sử dụng [hookdeck.com](https://hookdeck.com)
2. Nhấp nút **Test Webhook**
3. Sao chép URL webhook được tạo

#### Bước 2: Cấu Hình Contact Point

1. Điều hướng đến **Contact Points**
2. Nhấp **Add Contact Point**
3. **Name**: `EasyBankWebhook`
4. **Integration**: Chọn `Webhook`
5. **URL**: Dán URL webhook
6. Nhấp **Test** để gửi thông báo kiểm tra
7. Nhấp **Save**

### Cấu Hình Chính Sách Thông Báo

1. Vào **Notification Policies**
2. Nhấp **Settings** → **Edit**
3. Đặt **Default Contact Point**: `EasyBankWebhook`

#### Tùy Chọn Thời Gian

Cấu hình thời gian cảnh báo để ngăn spam thông báo:

- **Group Wait**: `10s` (để kiểm tra; mặc định là 30s)
- **Group Interval**: `10s` (để kiểm tra; mặc định là 5 phút)
- **Repeat Interval**: `10s` (để kiểm tra; mặc định là 4 giờ)
  - Thời gian chờ trước khi gửi lại cảnh báo

4. Nhấp **Update Default Policy**

## Kiểm Tra Cảnh Báo

### Kích Hoạt Cảnh Báo

1. Mở Docker Desktop
2. Dừng accounts microservice
3. Quan sát các thay đổi trạng thái cảnh báo:
   - **Normal** → **Pending** (đang chờ giai đoạn đánh giá)
   - **Pending** → **Firing** (cảnh báo được kích hoạt)

### Xác Minh Thông Báo

1. Kiểm tra URL webhook
2. Bạn sẽ nhận được thông báo với:
   - Status: `Firing`
   - Summary: `Account service is down`
   - Description: `please do something`

### Giải Quyết Cảnh Báo

1. Khởi động lại accounts microservice trong Docker Desktop
2. Chờ dịch vụ khởi động hoàn toàn
3. Trạng thái cảnh báo thay đổi: **Firing** → **Normal**
4. Webhook nhận được thông báo trạng thái **Resolved**

## Các Trạng Thái Cảnh Báo

| Trạng Thái | Mô Tả |
|------------|-------|
| **Normal** | Dịch vụ đang chạy bình thường, không phát hiện vấn đề |
| **Pending** | Điều kiện cảnh báo được đáp ứng, đang chờ giai đoạn đánh giá |
| **Firing** | Cảnh báo đang hoạt động và thông báo đang được gửi |
| **Resolved** | Cảnh báo trước đó đã firing đã trở lại bình thường |

## Các Phương Pháp Hay Nhất

1. **Evaluation Intervals**: Đặt khoảng thời gian phù hợp dựa trên nhu cầu giám sát
   - Quá thường xuyên = tăng tải cho Grafana
   - Quá hiếm = phát hiện cảnh báo chậm

2. **Evaluation Periods**: Sử dụng giai đoạn đánh giá để tránh cảnh báo giả
   - Các vấn đề tạm thời sẽ không kích hoạt cảnh báo ngay lập tức

3. **Repeat Intervals**: Cấu hình khoảng lặp lại hợp lý
   - Ngăn chặn mệt mỏi thông báo
   - Môi trường production: khuyến nghị 1-4 giờ

4. **Contact Points**: Sử dụng nhiều kênh thông báo
   - Email cho cảnh báo không khẩn cấp
   - Slack/Teams để nhóm nhận thức
   - PagerDuty cho cảnh báo quan trọng

5. **Tổ Chức Cảnh Báo**: Sử dụng thư mục và nhóm
   - Dễ dàng quản lý nhiều cảnh báo
   - Phân tách logic theo dịch vụ hoặc nhóm

## Khắc Phục Sự Cố

### Cảnh Báo Không Kích Hoạt

- Xác minh nguồn dữ liệu Prometheus được cấu hình đúng
- Kiểm tra tên metric và labels khớp với dịch vụ của bạn
- Đảm bảo evaluation interval và period phù hợp

### Không Nhận Được Thông Báo

- Kiểm tra contact point bằng nút **Test**
- Xác minh URL webhook đúng và có thể truy cập
- Kiểm tra notification policy đang sử dụng contact point đúng

### Cảnh Báo Giả

- Tăng giai đoạn đánh giá
- Điều chỉnh giá trị ngưỡng
- Sử dụng các hàm reduce khác (ví dụ: Average thay vì Last)

## Các Bước Tiếp Theo

- Khám phá cấu hình cảnh báo dựa trên dashboard
- Cấu hình nhiều quy tắc cảnh báo cho các dịch vụ khác nhau
- Thiết lập nhóm và định tuyến cảnh báo
- Triển khai tắt tiếng cảnh báo cho cửa sổ bảo trì

## Kết Luận

Hệ thống cảnh báo của Grafana cung cấp khả năng giám sát mạnh mẽ cho microservices. Bằng cách cấu hình ngưỡng, khoảng đánh giá và kênh thông báo phù hợp, bạn có thể đảm bảo nhận thức kịp thời về các vấn đề dịch vụ và duy trì tính khả dụng cao.



================================================================================
FILE: 77-grafana-alerts-from-dashboards.md
================================================================================

# Tạo Cảnh Báo từ Dashboard Grafana

## Tổng Quan

Hướng dẫn này trình bày một phương pháp thay thế để tạo cảnh báo trong Grafana bằng cách kích hoạt chúng trực tiếp từ dashboard, thay vì định nghĩa chúng riêng lẻ trong các quy tắc cảnh báo. Phương pháp này cung cấp quy trình làm việc tích hợp hơn cho việc giám sát microservices.

## Yêu Cầu Tiên Quyết

- Grafana instance với Prometheus làm nguồn dữ liệu
- Các microservices expose metrics thông qua Micrometer và Actuator
- Prometheus được cấu hình để scrape metrics từ microservices
- Môi trường Docker để triển khai microservices

## Tạo Cảnh Báo Dựa Trên Dashboard

### Bước 1: Tạo Dashboard Mới

1. Điều hướng đến phần dashboards của Grafana
2. Nhấp vào **New Dashboard**
3. Đặt tên cho dashboard (ví dụ: "AlertsDemo")
4. Lưu dashboard

### Bước 2: Thêm Panel Visualization

1. Nhấp vào **Add Visualization**
2. Chọn **Time Series** làm loại visualization
3. Chọn **Prometheus** làm nguồn dữ liệu

### Bước 3: Cấu Hình Query Metric

Để giám sát microservice Cards:

```
Metric: up
Label: job
Value: cards
```

Query này kiểm tra xem microservice Cards có đang chạy (giá trị 1) hay đã dừng (giá trị 0).

### Bước 4: Cấu Hình Cảnh Báo

1. Nhấp vào tab **Alert** trong panel editor
2. Cung cấp tiêu đề mô tả cho panel (ví dụ: "cards up")
3. Nhấp **Apply** để lưu panel
4. Nhấp **Edit** và điều hướng đến phần **Alert**
5. Nhấp **Create Alert Rule**
6. Lưu dashboard khi được yêu cầu

### Bước 5: Định Nghĩa Điều Kiện Cảnh Báo

Cấu hình các tham số cảnh báo sau:

**Hàm Reduce:**
- Function: `Last`

**Ngưỡng (Threshold):**
- Điều kiện: `Is below`
- Giá trị: `1`

**Tổ Chức:**
- Folder: Tạo folder mới "cards"
- Group: Tạo group mới "cards"

**Chu Kỳ Đánh Giá:**
- Khoảng đánh giá: `10s`
- Thời gian chờ: `30s`

### Bước 6: Thêm Chú Thích Cảnh Báo

Thêm các chú thích mô tả để tài liệu hóa cảnh báo tốt hơn:

1. **Summary**: "Cards microservice is down"
2. **Description**: "Please do something"

Dashboard UID và Panel ID được tự động điền.

### Bước 7: Lưu Quy Tắc Cảnh Báo

Nhấp **Save rule and exit** để hoàn tất cấu hình cảnh báo.

## Kiểm Tra Cảnh Báo

### Xem Trạng Thái Bình Thường

1. Điều hướng đến dashboard
2. Đặt khoảng thời gian thành 5 phút gần nhất
3. Quan sát biểu tượng trái tim màu xanh lá cho biết trạng thái healthy
4. Giá trị metric nên là `1` (service đang chạy)

### Kích Hoạt Cảnh Báo

1. Dừng microservice Cards trong Docker Desktop:
   - Chọn cards microservice
   - Nhấp Stop

2. Quan sát các thay đổi trạng thái cảnh báo:
   - **Pending**: Biểu tượng trái tim chuyển sang màu vàng/cam
   - **Firing**: Biểu tượng trái tim chuyển sang màu đỏ (sau ~30s)
   - Đường màu vàng xuất hiện trên panel tại điểm kích hoạt cảnh báo

3. Kiểm tra thông báo webhook cho các tin nhắn cảnh báo

### Giải Quyết Cảnh Báo

1. Khởi động microservice Cards trong Docker Desktop
2. Đợi khoảng 20 giây để service khởi động
3. Quan sát trạng thái cảnh báo trở về OK (biểu tượng trái tim màu xanh lá)
4. Giá trị metric trở về `1`

## Kiến Trúc Giám Sát Microservices

### Tổng Quan Các Thành Phần

```
Microservices (với Micrometer & Actuator)
    ↓ (expose metrics)
Prometheus
    ↓ (scrape metrics)
Prometheus UI (visualization cơ bản)
    ↓ (nguồn dữ liệu)
Grafana (dashboards & alerts nâng cao)
    ↓ (thông báo)
Webhook/Kênh Thông Báo
```

### Các Thành Phần Chính

1. **Microservices**: Expose metrics thông qua Micrometer và Spring Boot Actuator
2. **Prometheus**: Scrape và lưu trữ dữ liệu metrics từ microservices
3. **Grafana**: Cung cấp khả năng visualization nâng cao, dashboards và alerting
4. **Kênh Thông Báo**: Webhook hoặc các kênh khác để gửi cảnh báo

## Best Practices (Thực Hành Tốt Nhất)

### Cho Developers

- Hiểu kiến trúc microservices từ đầu đến cuối
- Biết kiến thức cơ bản về Grafana để giám sát và khắc phục sự cố
- Có khả năng cấu hình các cảnh báo và dashboards cơ bản
- Cung cấp hướng dẫn cho các team platform và operations

### Cho Platform Teams

- Tuân theo các cấu hình được khuyến nghị cho môi trường production
- Thiết lập các khoảng đánh giá phù hợp dựa trên mức độ quan trọng của service
- Cấu hình nhiều kênh thông báo để đảm bảo dự phòng
- Tài liệu hóa các quy trình phản hồi cảnh báo

## Những Điểm Chính

1. **Cảnh báo dựa trên dashboard** cung cấp phương pháp giám sát tích hợp
2. **Trạng thái cảnh báo** chuyển qua: OK → Pending → Firing → OK
3. **Chỉ báo trực quan** (biểu tượng trái tim và đường có màu) cung cấp cái nhìn tổng quan nhanh về trạng thái
4. **Chú thích** giúp tài liệu hóa cảnh báo cho sự cộng tác của team
5. **Stack giám sát hoàn chỉnh** (Micrometer + Prometheus + Grafana) cho phép khả năng quan sát toàn diện

## Kết Luận

Hiểu được pipeline giám sát metrics hoàn chỉnh từ microservices đến Grafana là điều cần thiết cho việc phát triển microservice hiện đại. Kiến thức này giúp developers:

- Vượt qua các cuộc phỏng vấn liên quan đến microservices
- Trở thành thành viên có giá trị trong team với kiến thức từ đầu đến cuối
- Cung cấp hướng dẫn kỹ thuật cho các team operations
- Demo các khả năng giám sát một cách hiệu quả

Khả năng tạo, cấu hình và quản lý cảnh báo từ dashboards Grafana là một kỹ năng quan trọng để duy trì các kiến trúc microservice đáng tin cậy.



================================================================================
FILE: 78-distributed-tracing-in-microservices.md
================================================================================

# Distributed Tracing trong Microservices

## Giới thiệu về Trụ cột thứ ba của Observability

Trước đây, chúng ta đã thảo luận về hai trụ cột của observability và monitoring: **logs** và **metrics**. Trong bài giảng này, chúng ta sẽ tập trung vào trụ cột thứ ba của observability và monitoring: **tracing**.

Với logs và metrics, chúng ta chỉ có thể suy ra tình trạng nội bộ của ứng dụng hoặc tình trạng tổng thể của ứng dụng. Tuy nhiên, thông tin thu được thông qua event logs, health probes và metrics lại không giúp các developer trong việc debug các vấn đề, đặc biệt là trong môi trường phân tán như microservices hoặc ứng dụng cloud-native.

## Thách thức trong Hệ thống Phân tán

Trong các ứng dụng phân tán như microservices, một request của người dùng có thể đi qua nhiều ứng dụng hoặc nhiều microservices. Với độ phức tạp này, chúng ta cần một cơ chế để các developer hiểu được:

- Request đã đi qua microservice hoặc ứng dụng nào
- Mất bao nhiêu thời gian ở mỗi service
- Vị trí chính xác nơi xảy ra vấn đề trong các ứng dụng phân tán

## Distributed Tracing là gì?

**Distributed tracing** là một kỹ thuật được sử dụng đặc biệt trong microservices hoặc ứng dụng cloud-native để hiểu và phân tích luồng request khi chúng lan truyền qua nhiều services và components trong môi trường phân tán.

Với thông tin tracing, các developer có thể chẩn đoán bất kỳ loại vấn đề nào trong các hệ thống phức tạp và phân tán.

### Kịch bản Thực tế

Trong các dự án thực tế, sẽ có hàng trăm microservices được triển khai. Nếu một request phải đi qua hơn mười microservices để nhận được response thành công, developer phải có thông tin rõ ràng về:

- Request đang đi qua mỗi microservice như thế nào
- Method nào được gọi
- Mất bao nhiêu thời gian ở mỗi method

Nếu không có thông tin distributed tracing, developers không thể debug các vấn đề trong hệ thống phân tán.

## Triển khai Distributed Tracing

### Giải pháp Correlation ID

Một trong những giải pháp tốt nhất để triển khai distributed tracing là tạo một định danh duy nhất được gọi là **correlationId**, được tạo cho mỗi request tại điểm vào của hệ thống phân tán hoặc microservices của bạn.

Trước đây, chúng ta đã thảo luận về một kịch bản trong Gateway server nơi:
- Tại điểm vào, chúng ta tạo một correlationId
- CorrelationId tương tự được gửi đến các microservices accounts, loans và cards
- Với correlationId, chúng ta có thể dễ dàng theo dõi request đi từ gateway server đến accounts, và từ accounts đến cards và loans microservices

CorrelationId có thể được sử dụng như một giải pháp hoàn hảo cho distributed tracing vì nó cho phép chúng ta theo dõi:
- Request của microservice đang đi đâu
- Đi đến điểm nào
- Exception nào được throw

### Thách thức với Triển khai Thủ công

Tuy nhiên, việc tạo correlationId và gắn nó vào tất cả các logs trong mạng microservices không phải là một phương án khả thi cho developers. Tại sao? Vì developer phải:
- Truy cập từng log có trong microservice
- Đảm bảo họ đang thêm correlationId được tạo bởi gateway server

Đây là một nhiệm vụ cực kỳ phức tạp và đầy thách thức. Đó là lý do tại sao chúng ta cần tìm kiếm một phương án tốt hơn để triển khai distributed tracing trong microservices.

## Tiêu chuẩn cho Distributed Tracing

Trước khi hiểu các best practices, hãy tìm hiểu các tiêu chuẩn chúng ta cần tuân theo khi tạo chi tiết distributed tracing. Distributed tracing luôn khuyến nghị tuân theo ba thành phần quan trọng:

### 1. Tags (Metadata)

Sử dụng tags, chúng ta có thể xây dựng metadata cung cấp các chi tiết như:
- Username của người dùng đã xác thực
- Định danh microservice

Nếu bạn gắn thông tin metadata này vào các logs, bạn có thể dễ dàng xác định từ log statement xem log cụ thể đó thuộc về microservice hoặc thông tin metadata nào.

**Ví dụ:** Nếu bạn gắn tên ứng dụng cho tất cả các logs của mình (như accounts, cards và loans), sẽ cực kỳ dễ dàng để xác định ứng dụng microservice nào mà một log distributed tracing cụ thể thuộc về.

### 2. Trace ID

**Trace ID** phải được tạo ở điểm bắt đầu của request, thường là khi request vào mạng microservice của bạn tại Edge server.

Đặc điểm chính:
- Được tạo tại điểm vào (ví dụ: Edge server)
- Trace ID tương tự được gắn vào tất cả các logs liên quan đến request đó
- Hiện diện bất kể request đang đi đâu trong mạng microservice của bạn
- Chung cho tất cả các microservices nơi một request cụ thể đang được xử lý

### 3. Span ID

**Span ID** đại diện cho từng giai đoạn xử lý request riêng lẻ.

Đặc điểm chính:
- Mỗi service có Span ID riêng của nó
- Trong accounts microservice, bạn có thể gọi nhiều methods; tương tự, các microservices khác triển khai nhiều methods
- Chúng ta gán một giá trị ID cụ thể cho mỗi microservice
- Tất cả các logs được tạo trong accounts microservice có cùng Span ID cùng với Trace ID chung cho tất cả các microservices

## Ví dụ Thực tế

Hãy xem một kịch bản trong đó người dùng gọi API `customerDetails` có trong accounts microservice bằng cách gửi requests đến edge server.

### Cơ chế Hoạt động

Khi chúng ta triển khai distributed tracing trong microservices của mình:

1. **Tại Edge Server:** Khi service đầu tiên trong mạng được gọi, một Trace ID được tạo

2. **Tag (Metadata):** Đầu tiên, chúng ta có thông tin metadata là một tag. Với tag, chúng ta có thể dễ dàng xác định log statement cụ thể thuộc về service nào. Ví dụ, với tag "gateway server", chúng ta có thể xác nhận rằng một log cụ thể thuộc về gateway server.

3. **Trace ID:** Sau tag, có thông tin Trace ID. Trace ID tương tự hiện diện trong tất cả các logs được tạo trong khi xử lý request. Nếu request đi đến tất cả các microservices khác, Trace ID (thành phần thứ hai) vẫn giữ nguyên ở tất cả các nơi, trong khi tên tag và thông tin metadata thay đổi (như gateway server, loans, accounts và cards).

4. **Span ID:** Bên trong mỗi microservice hoặc ứng dụng, một Span ID duy nhất được tạo:
   - Gateway có giá trị Span ID riêng của nó
   - Accounts microservice có Span ID riêng của nó
   - Loans và cards có Span IDs riêng của chúng
   - Span ID tương tự hiện diện trong tất cả các log statements trong một microservice cụ thể

**Ví dụ với Loans Microservice:** Nếu có hai logger statements (logger statement 1, logger statement 2), tất cả các logs đều có cùng Span ID vì tất cả các logs này được tạo bên trong cùng một microservice. Điều tương tự áp dụng cho cards microservice.

## Tóm tắt các Thành phần

### Thông tin Tag
- Giúp xác định ứng dụng microservice hoặc thông tin metadata nào mà một log cụ thể thuộc về
- Thay vì tên ứng dụng, bạn có thể giữ chi tiết username đã đăng nhập để dễ dàng theo dõi tất cả các logs được tạo do các hành động được thực hiện bởi một người dùng cụ thể

### Trace ID
- Chung cho tất cả các microservices
- Request tương tự đi qua các microservices khác nhau

### Span ID
- Duy nhất cho mỗi ứng dụng microservice
- Cho phép developers dễ dàng theo dõi request đã được xử lý đến điểm nào
- Giúp xác định exception xảy ra trong service nào

## Điểm Chính Cần Nhớ

Khi triển khai distributed tracing, chúng ta nên tuân theo các tiêu chuẩn sau:

1. **Tags** cho thông tin metadata
2. **Trace ID** cho việc theo dõi request qua các services
3. **Span ID** cho việc theo dõi trong từng service riêng lẻ

Khi chúng ta trước đây triển khai correlation ID với gateway server, chúng ta chỉ đơn giản tạo một ID, nhưng chúng ta không có metadata tag hoặc Span IDs. Trong các bài giảng tiếp theo, với sự trợ giúp của distributed tracing, chúng ta sẽ triển khai các tiêu chuẩn này một cách đúng đắn.

## Kết luận

Distributed tracing là điều cần thiết cho việc debugging và monitoring các kiến trúc microservices. Bằng cách tuân theo tiêu chuẩn ba thành phần (Tags, Trace ID và Span ID), các developer có thể theo dõi hiệu quả các requests qua các hệ thống phân tán phức tạp và nhanh chóng xác định các vấn đề.

Khi bạn xem tất cả điều này trong demo, nó sẽ trở nên rõ ràng hơn nhiều. Cảm ơn bạn và hẹn gặp lại ở bài giảng tiếp theo!



================================================================================
FILE: 79-distributed-tracing-implementation-options.md
================================================================================

# Các Tùy Chọn Triển Khai Distributed Tracing cho Microservices

## Tổng Quan

Tài liệu này khám phá các tùy chọn có sẵn để triển khai distributed tracing (truy vết phân tán) trong microservices Java Spring Boot, so sánh các phương pháp khác nhau và giải thích tại sao OpenTelemetry là giải pháp được khuyến nghị.

## Các Tùy Chọn Có Sẵn

### 1. Spring Cloud Sleuth (Đã Ngừng Phát Triển)

Spring Cloud Sleuth là một dự án Spring Cloud được thiết kế để giúp triển khai distributed tracing trong microservices.

**Cách thức hoạt động:**
- Tự động thêm thông tin metadata, trace ID và span ID vào tất cả logs được tạo trong microservices
- Nhà phát triển không cần phải sửa đổi các câu lệnh log
- Chỉ cần thêm dependencies của Spring Cloud Sleuth
- Có thể tích hợp với Zipkin để xác định chi tiết truy vết và các điểm nghẽn hiệu suất

**Tại sao chúng ta không sử dụng:**
- Nhóm Spring Cloud Sleuth đã thông báo rằng phiên bản 3.1 sẽ là phiên bản nhỏ cuối cùng
- Dự án đang bị ngừng phát triển vì chức năng tracing đang được chuyển sang Micrometer Tracing
- Được coi là phương pháp lỗi thời mặc dù nhiều blog và khóa học vẫn đang giảng dạy nó

### 2. Micrometer Tracing

Micrometer Tracing là sản phẩm kế nhiệm của Spring Cloud Sleuth, được xây dựng trong cùng dự án Micrometer cung cấp khả năng expose metrics cho Prometheus.

**Tính năng:**
- Tài liệu toàn diện về dependencies, chi tiết triển khai, span IDs và trace IDs
- Tích hợp với Open Zipkin và OpenTelemetry
- Là một phần của hệ sinh thái Micrometer đã được thiết lập

**Hạn chế:**
- Yêu cầu nhiều thay đổi cấu hình và thiết lập properties từ nhà phát triển
- **Chỉ dành cho Java**: Chỉ có thể được sử dụng trong các ứng dụng Java
- Triển khai phức tạp hơn so với các phương án thay thế

### 3. OpenTelemetry (Được Khuyến Nghị)

OpenTelemetry là một framework observability mã nguồn mở, không phụ thuộc vào nhà cung cấp, được duy trì bởi Cloud Native Computing Foundation (CNCF).

**Ưu điểm:**
- **Hỗ trợ đa ngôn ngữ**: Hoạt động với C++, .NET, Erlang, Go, Java, JavaScript, PHP, Python, Ruby, Rust, Swift và nhiều ngôn ngữ khác
- **Triển khai dễ dàng**: Cực kỳ dễ dàng để thiết lập distributed tracing
- **Tích hợp framework**: Tích hợp với các framework phổ biến như Spring, ASP.NET, Express và Quarkus
- **Bền vững**: Có thể được sử dụng trên các ngăn xếp công nghệ khác nhau trong tổ chức của bạn

## Triển Khai OpenTelemetry

### Phương Pháp Automatic Instrumentation

OpenTelemetry cung cấp cả manual và automatic instrumentation. Chúng ta sẽ sử dụng **automatic instrumentation** vì nó yêu cầu ít thay đổi mã nguồn nhất.

### Các Bước Triển Khai

1. **Thêm OpenTelemetry Java Agent JAR** vào classpath của ứng dụng

2. **Cấu hình Java Agent** bằng một trong các phương pháp sau:

   **Tùy chọn A: Tham số dòng lệnh**
   ```bash
   java -javaagent:path/to/opentelemetry-javaagent.jar -jar your-application.jar
   ```

   **Tùy chọn B: Biến môi trường**
   ```bash
   JAVA_TOOL_OPTIONS=-javaagent:path/to/opentelemetry-javaagent.jar
   ```

3. **Đặt tên service** bằng một trong các phương pháp sau:

   **Tùy chọn A: System property**
   ```bash
   -Dotel.service.name=your-service-name
   ```

   **Tùy chọn B: Biến môi trường**
   ```bash
   OTEL_SERVICE_NAME=your-service-name
   ```

### Lợi Ích Chính

- **Thay đổi mã nguồn tối thiểu**: Không cần sửa đổi mã ứng dụng hiện có
- **Automatic instrumentation**: Chỉ cần đảm bảo JAR có trong classpath
- **Theo dõi metadata**: Tên service trở thành một phần của metadata trong distributed tracing
- **Tương thích đa nền tảng**: Cùng một phương pháp hoạt động trên các ngôn ngữ lập trình khác nhau

## Kết Luận

OpenTelemetry là phương pháp được khuyến nghị để triển khai distributed tracing trong microservices vì:
- Dễ dàng triển khai với cấu hình tối thiểu
- Hỗ trợ đa ngôn ngữ cho các ngăn xếp công nghệ đa dạng
- Được duy trì tích cực dưới CNCF
- Không phụ thuộc nhà cung cấp và mã nguồn mở
- Tích hợp mạnh mẽ với các framework hiện đại

Bằng cách sử dụng automatic instrumentation với OpenTelemetry Java Agent, bạn có thể triển khai distributed tracing với những thay đổi rất tối thiểu đối với kiến trúc microservices của mình.

## Tài Liệu Tham Khảo

- [Tài Liệu Chính Thức OpenTelemetry](https://opentelemetry.io/docs/)
- [OpenTelemetry Java - Automatic Instrumentation](https://opentelemetry.io/docs/languages/java/automatic/)
- [Cloud Native Computing Foundation](https://www.cncf.io/)



================================================================================
FILE: 8-service-discovery-and-traditional-load-balancer-challenges.md
================================================================================

# Thách Thức Về Service Discovery và Traditional Load Balancer Trong Microservices

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá các thách thức và nhược điểm khi sử dụng phương pháp truyền thống của kiến trúc nguyên khối (monolithic) cho việc giao tiếp nội bộ trong môi trường microservices, đặc biệt khi các khái niệm service discovery và service registration không được sử dụng.

## Phương Pháp Giao Tiếp Truyền Thống

### Yêu Cầu Cơ Bản

Trong một mạng web, khi một service hoặc ứng dụng cần giao tiếp với service khác, nó cần các thông tin định vị thiết yếu như:
- **Địa chỉ IP**
- **Tên DNS** (Domain Name - Tên miền)

### Kịch Bản Đơn Giản: Giao Tiếp Giữa Hai Microservices

Hãy xem xét một kịch bản trong đó hai microservices, **Accounts** và **Loans**, cần giao tiếp với nhau:

#### Thuật Ngữ
- **Upstream Service**: Service phụ thuộc (ví dụ: Accounts microservice)
- **Downstream Service**: Service được phụ thuộc vào (ví dụ: Loans microservice)
- **Backing Service**: Một service mà service khác phải dựa vào để gửi phản hồi thành công

#### Cấu Hình Ví Dụ
- **Accounts Microservice**: Được triển khai như upstream service
- **Loans Microservice**: Được triển khai tại IP `127.54.37.23` như downstream service

### Phương Pháp Giao Tiếp

Accounts microservice có thể giao tiếp với Loans microservice bằng hai cách:

1. **Hardcode địa chỉ IP**: Nhúng trực tiếp địa chỉ IP vào code
2. **DNS/Hostname**: Sử dụng tên miền được ánh xạ tới địa chỉ IP

Phương pháp truyền thống này không sử dụng service discovery hay load balancing - chỉ đơn giản là giao tiếp trực tiếp qua hostname, DNS hoặc địa chỉ IP.

## Thách Thức Với Triển Khai Đơn Instance

### Khi Nào Hoạt Động Tốt

Phương pháp truyền thống hoạt động tốt khi:
- Chỉ có **một instance** của Loans microservice đang chạy
- Việc quản lý ánh xạ tên DNS sang địa chỉ IP là đơn giản
- Môi trường tương đối tĩnh

### Lợi Ích Của DNS

Sử dụng tên DNS thay vì hardcode địa chỉ IP mang lại:
- **Tính linh hoạt**: Thay đổi địa chỉ IP chỉ cần cập nhật ánh xạ DNS
- **Không cần thay đổi code**: Code của Accounts microservice không cần thay đổi khi IP thay đổi
- **Quản lý tập trung**: Đội ngũ platform/operations xử lý việc ánh xạ

## Vấn Đề Trong Môi Trường Cloud

### Thách Thức Với Nhiều Instances

Trong môi trường cloud với nhiều instances, phương pháp truyền thống thất bại vì:

1. **Nhiều địa chỉ IP**: Mỗi instance có địa chỉ IP riêng
2. **Quản lý DNS phức tạp**: Phải duy trì ánh xạ giữa DNS và nhiều địa chỉ IP
3. **Hạn chế của Round Robin**: Mặc dù các thuật toán như Round Robin có thể phân phối traffic, việc quản lý DNS records trở nên phức tạp

### Tại Sao Hoạt Động Tốt Cho Ứng Dụng Nguyên Khối

Phương pháp dựa trên DNS truyền thống phù hợp với ứng dụng monolithic/SOA vì:
- Số lượng services hạn chế
- Triển khai tĩnh trên máy vật lý hoặc VMs chạy lâu dài
- Địa chỉ IP không đổi trừ khi thay đổi thủ công

### Tại Sao Thất Bại Với Microservices

Môi trường microservices đối mặt với những thách thức đặc biệt:

#### 1. Thay Đổi Nhanh Chóng
- Containers được triển khai và hủy bỏ thường xuyên
- Auto-scaling đưa instances mới vào và loại bỏ chúng dựa trên traffic
- Instances lỗi được thay thế bằng instances mới có địa chỉ IP khác

#### 2. Bản Chất Tạm Thời (Ephemeral)
- **Ephemeral** nghĩa là có tuổi thọ ngắn và có thể bị hủy bất cứ lúc nào
- Containers có tuổi thọ ngắn hơn so với triển khai truyền thống
- Không thể duy trì DNS records chính xác với địa chỉ IP liên tục thay đổi

#### 3. Scale Động
- Scale up trong thời gian traffic cao
- Scale down trong thời gian traffic thấp
- Tự động thay thế instances không phản hồi

## Kiến Trúc Traditional Load Balancer

### Thiết Lập Điển Hình

```
Ứng Dụng Client
        ↓
    Tên DNS (services.easybank.com)
        ↓
Primary Load Balancer
        ↓
    Bảng Định Tuyến
        ↓
Microservices (Accounts, Cards, Loans)
        ↓
Secondary Load Balancer (Dự phòng)
```

### Cách Hoạt Động

1. **Yêu cầu từ Client**: Ứng dụng gọi microservices qua tên DNS
2. **Primary Load Balancer**: Xử lý các yêu cầu đến
3. **Bảng định tuyến**: Chứa ánh xạ địa chỉ IP được cấu hình thủ công
4. **Chuyển tiếp yêu cầu**: Định tuyến traffic đến microservices phù hợp
5. **Secondary Load Balancer**: Giám sát primary và thay thế nếu nó lỗi

## Nhược Điểm Của Traditional Load Balancers

### 1. Khả Năng Scale Ngang Hạn Chế và Chi Phí License

- **Cấu hình thủ công**: Địa chỉ IP phải được biết trước và cấu hình
- **Bảng định tuyến tĩnh**: Yêu cầu duy trì thủ công các địa chỉ IP
- **Không scale động**: Không thể thực hiện scale-up và scale-down động hiệu quả
- **Chi phí license**: Các nhà cung cấp cloud tính phí cho traditional load balancers
- **Tác động ngân sách**: Cần phân bổ ngân sách bổ sung

### 2. Single Point of Failure (Điểm Lỗi Duy Nhất)

- **Dự phòng hạn chế**: Ngay cả với primary và secondary load balancers, cả hai có thể lỗi
- **Khó cluster hóa**: Không thể scale load balancers dễ dàng trong môi trường cluster
- **Điểm nghẽn traffic**: Tất cả yêu cầu đến được tập trung tại một vị trí
- **Rủi ro gián đoạn hoàn toàn**: Lỗi load balancers ảnh hưởng toàn bộ hệ thống

### 3. Quản Lý Cấu Hình IP Thủ Công

- **Nhiệm vụ bất khả thi**: Cập nhật cấu hình IP thủ công là không thực tế cho microservices
- **Thay đổi liên tục**: Vòng đời container yêu cầu cập nhật thường xuyên
- **Lỗi con người**: Quy trình thủ công dễ mắc sai lầm
- **Chi phí vận hành**: Đầu tư thời gian và tài nguyên đáng kể

### 4. Phức Tạp và Không Tương Thích Với Container

- **Bản chất phức tạp**: Traditional load balancers yêu cầu bảo trì phức tạp
- **Quản lý thủ công**: Không thể tự động hóa dễ dàng
- **Không thân thiện với container**: Không tương thích với Docker containers
- **Môi trường động**: Containers có thể được tạo hoặc hủy bất cứ lúc nào

## Vấn Đề Chính: Duy Trì Bảng Định Tuyến Thủ Công

Thách thức lớn nhất với traditional load balancers trong microservices là yêu cầu **duy trì thủ công bảng định tuyến**. Điều này không thực tế vì:

- Containers và microservices có tính **ephemeral** (tạm thời)
- Instances liên tục được tạo và hủy
- Địa chỉ IP thay đổi động
- Không có thời gian cho can thiệp thủ công

## Tóm Tắt

Các phương pháp load balancing truyền thống và giao tiếp service dựa trên DNS:

✅ **Hoạt động tốt cho**:
- Ứng dụng monolithic
- Ứng dụng SOA
- Triển khai tĩnh
- Số lượng services nhỏ

❌ **Thất bại với**:
- Ứng dụng cloud-native
- Kiến trúc microservices
- Môi trường container động
- Các kịch bản auto-scaling

Vấn đề cốt lõi là các phương pháp truyền thống yêu cầu cấu hình tĩnh, được quản lý thủ công, không tương thích với bản chất động và tạm thời của cloud-native microservices.

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các giải pháp để vượt qua những thách thức này cho các ứng dụng cloud-native và microservices, bao gồm:
- Các pattern Service Discovery
- Cơ chế Service Registration
- Phương pháp load balancing hiện đại
- Giải pháp thân thiện với container

---

**Ghi chú**: Nội dung này dựa trên bài giảng kỹ thuật về kiến trúc microservices sử dụng Java Spring Boot framework.



================================================================================
FILE: 80-implementing-opentelemetry-distributed-tracing-microservices.md
================================================================================

# Triển Khai OpenTelemetry Cho Distributed Tracing Trong Microservices

## Tổng Quan

Hướng dẫn này trình bày cách triển khai OpenTelemetry để theo dõi phân tán (distributed tracing) trong các microservices Spring Boot. OpenTelemetry (OTel) là một framework quan sát mã nguồn mở, độc lập với nhà cung cấp, tự động thêm công cụ đo lường vào ứng dụng của bạn để tạo, thu thập và xuất dữ liệu đo lường từ xa bao gồm traces, metrics và logs.

## Yêu Cầu Trước Khi Bắt Đầu

- Ứng dụng microservices Spring Boot
- Docker và Docker Compose
- Maven để quản lý dependencies
- Hiểu biết cơ bản về distributed tracing

## Các Bước Triển Khai

### 1. Dừng Các Container Đang Chạy

Trước khi thực hiện thay đổi, hãy dừng tất cả các container đang chạy:

```bash
docker compose down
```

### 2. Thêm Dependency OpenTelemetry

Điều hướng đến file `pom.xml` trong microservice accounts và thêm dependency OpenTelemetry.

#### Định Nghĩa Phiên Bản OpenTelemetry

Thêm thuộc tính version trong `pom.xml`:

```xml
<properties>
    <otelVersion>1.27.0</otelVersion>
</properties>
```

**Lưu ý:** Luôn kiểm tra repository GitHub để biết phiên bản mới nhất, vì các phiên bản được cập nhật hàng quý.

#### Thêm Dependency OpenTelemetry Java Agent

Thêm dependency sau dependency actuator:

```xml
<dependency>
    <groupId>io.opentelemetry.javaagent</groupId>
    <artifactId>opentelemetry-javaagent</artifactId>
    <version>${otelVersion}</version>
    <scope>runtime</scope>
</dependency>
```

Scope `runtime` đảm bảo rằng thư viện OpenTelemetry chỉ được sử dụng trong thời gian chạy ứng dụng, không phải trong quá trình biên dịch. Dependency này sẽ được đóng gói và có sẵn trong Docker image.

#### Refresh Maven Dependencies

Sau khi thêm dependency, thực hiện Maven refresh để tải xuống các thư viện cần thiết.

### 3. Cấu Hình Logging Pattern

Mở file `application.yml` trong microservice accounts và thêm custom logging pattern.

Thêm cấu hình sau vào phần logging:

```yaml
logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{trace_id:},%X{span_id:}]"
```

#### Giải Thích Pattern

- `%5p`: Dành 5 ký tự cho mức độ nghiêm trọng của log (DEBUG, INFO, WARNING, ERROR)
- `${spring.application.name:}`: Chèn metadata tên ứng dụng
- `%X{trace_id:}`: Chèn trace ID được tạo bởi OpenTelemetry tại runtime
- `%X{span_id:}`: Chèn span ID được tạo bởi OpenTelemetry tại runtime

Pattern này đảm bảo rằng tất cả các câu lệnh log được tạo bởi microservice của bạn đều bao gồm thông tin distributed tracing.

### 4. Cập Nhật Các Controller Class Với Logging

#### CustomerController

Thay thế logging correlation ID hiện tại bằng logging được tăng cường bởi OpenTelemetry:

```java
logger.info("fetchCustomerDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchCustomerDetails() method end");
```

#### LoansController

Thêm các câu lệnh logging tương tự:

```java
logger.info("fetchLoanDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchLoanDetails() method end");
```

#### CardsController

Thêm logging vào fetch API:

```java
logger.info("fetchCardDetails() method start");
// ... logic nghiệp vụ ...
logger.info("fetchCardDetails() method end");
```

**Quan trọng:** Xóa các câu lệnh logging dựa trên correlation ID cũ, vì OpenTelemetry sẽ tự động chèn trace và span IDs vào tất cả logs dựa trên pattern đã cấu hình.

### 5. Áp Dụng Thay Đổi Cho Tất Cả Microservices

Lặp lại các bước 2-4 cho tất cả các microservices trong kiến trúc của bạn để đảm bảo distributed tracing nhất quán trên toàn bộ hệ thống.

## Hiểu Về Hệ Sinh Thái OpenTelemetry

### Cách Hoạt Động Của OpenTelemetry

OpenTelemetry hoạt động bằng cách gắn bytecode vào ứng dụng microservice của bạn tại runtime. Bytecode này tự động thêm thông tin tracing, thông tin span và các metadata khác vào logs và dữ liệu đo lường từ xa của bạn.

### Grafana Tempo Để Lưu Trữ Trace

Sau khi OpenTelemetry tạo logs với thông tin tracing, chúng ta sử dụng **Grafana Tempo** để lập chỉ mục và lưu trữ dữ liệu tracing:

- **Mục đích**: Tương tự như Loki cho logs và Prometheus cho metrics, Tempo được thiết kế đặc biệt cho traces
- **Lợi ích**: Giải pháp mã nguồn mở, khả năng mở rộng cao và tiết kiệm chi phí
- **Chức năng**: Lưu trữ và phân tích thông tin trace cho các hệ thống phân tán

### Tích Hợp Grafana UI

Grafana cung cấp một giao diện thống nhất kết nối với các nguồn dữ liệu khác nhau:

- **Loki**: Cho log aggregation
- **Prometheus**: Cho metrics
- **Tempo**: Cho distributed tracing

Hệ sinh thái Grafana cung cấp một giao diện chung nơi bạn có thể tìm kiếm logs, thông tin tracing hoặc metrics dựa trên yêu cầu của bạn. Cách tiếp cận thống nhất này khiến việc hiểu Grafana và các thành phần của nó trở nên thiết yếu đối với các nhà phát triển microservices, kỹ sư nền tảng và các thành viên trong nhóm vận hành.

### Lợi Ích Của Visualization

Grafana hiển thị thông tin distributed tracing ở định dạng trực quan dễ hiểu, giúp đơn giản hóa việc:

- Theo dõi các request qua nhiều microservices
- Xác định các nút thắt về hiệu suất
- Debug các vấn đề trong hệ thống phân tán
- Hiểu các phụ thuộc giữa các services

## Các Bước Tiếp Theo

### Tạo Docker Images

Sau khi triển khai các thay đổi OpenTelemetry:

1. Xóa các Docker images hiện có
2. Tạo Docker images mới với tag name **S11**
3. Đảm bảo tất cả các microservices được build với cấu hình OpenTelemetry mới nhất

### Cập Nhật Docker Compose

File Docker Compose cần được cập nhật để:

- Bao gồm cấu hình container Tempo
- Cấu hình tích hợp giữa Tempo và Grafana
- Thiết lập networking phù hợp cho distributed tracing

### Chuẩn Bị Demo

Sau khi Docker images được tạo và Docker Compose được cấu hình, bạn sẽ có thể thấy distributed tracing hoạt động thông qua giao diện Grafana UI.

## Điểm Chính Cần Nhớ

- OpenTelemetry tự động thêm công cụ đo lường vào ứng dụng của bạn cho distributed tracing
- Custom logging patterns đảm bảo trace và span IDs được bao gồm trong tất cả logs
- Hệ sinh thái Grafana (Loki, Prometheus, Tempo) cung cấp khả năng quan sát toàn diện
- Triển khai đúng cách yêu cầu cập nhật trên tất cả các microservices
- Visualization thông qua Grafana làm cho việc debug các hệ thống phân tán trở nên dễ dàng hơn đáng kể

## Best Practices Về Logging

Bạn có thể thêm các câu lệnh log ở bất kỳ lớp nào của ứng dụng:

- **Controller Layer**: Theo dõi các request đến và response đi
- **Service Layer**: Giám sát việc thực thi logic nghiệp vụ
- **DAO Layer**: Theo dõi các tương tác với database

Tất cả logs sẽ tự động bao gồm thông tin distributed tracing dựa trên pattern đã cấu hình, loại bỏ nhu cầu quản lý correlation ID thủ công.

---

**Phiên bản**: S11  
**Cập nhật lần cuối**: Dựa trên OpenTelemetry 1.27.0  
**Lưu ý**: Kiểm tra repository GitHub hàng quý để biết các cập nhật phiên bản và best practices mới nhất.



================================================================================
FILE: 81-configuring-opentelemetry-tempo-grafana-integration.md
================================================================================

# Cấu hình Tích hợp OpenTelemetry, Tempo và Grafana cho Distributed Tracing

## Tổng quan

Hướng dẫn này sẽ giúp bạn cập nhật cấu hình Docker Compose để tích hợp OpenTelemetry, Tempo và Grafana nhằm theo dõi phân tán (distributed tracing) trong kiến trúc microservices Spring Boot.

## Yêu cầu

- Đã cài đặt Docker và Docker Compose
- Kiến trúc microservices hiện có với Grafana và Prometheus
- Đã thêm dependency OpenTelemetry vào pom.xml

## Bước 1: Cấu hình Thuộc tính Môi trường Chung

Mở file `common-config.yml` trong thư mục docker-compose (profile prod).

Thêm các thuộc tính môi trường vào `microservice-base-config` (không phải `microservice-configserver-config` để đảm bảo tất cả microservices đều nhận được các thuộc tính này):

```yaml
microservice-base-config:
  environment:
    JAVA_TOOL_OPTIONS: "-javaagent:/path/to/opentelemetry-javaagent.jar"
    OTEL_EXPORTER_OTLP_ENDPOINT: "http://tempo:4317"
    OTEL_METRICS_EXPORTER: "none"
```

### Chi tiết Cấu hình

- **JAVA_TOOL_OPTIONS**: Chỉ định tham số javaagent với đường dẫn đến file JAR của OpenTelemetry (có sẵn trong containers sau khi thêm dependency vào pom.xml)
- **OTEL_EXPORTER_OTLP_ENDPOINT**: Định nghĩa endpoint của dịch vụ Tempo nơi OpenTelemetry sẽ gửi thông tin tracing
- **OTEL_METRICS_EXPORTER**: Đặt giá trị "none" vì Prometheus đã được sử dụng để xuất metrics

## Bước 2: Cấu hình Biến Môi trường cho từng Service

Trong file `docker-compose.yml`, thêm thuộc tính môi trường `OTEL_SERVICE_NAME` cho mỗi microservice:

### Config Server
```yaml
configserver:
  environment:
    OTEL_SERVICE_NAME: "configserver"
```

### Eureka Server
```yaml
eurekaserver:
  environment:
    OTEL_SERVICE_NAME: "eurekaserver"
```

### Accounts Microservice
```yaml
accounts:
  environment:
    OTEL_SERVICE_NAME: "accounts"
```

### Loans Microservice
```yaml
loans:
  environment:
    OTEL_SERVICE_NAME: "loans"
```

### Cards Microservice
```yaml
cards:
  environment:
    OTEL_SERVICE_NAME: "cards"
```

### Gateway Server
```yaml
gatewayserver:
  environment:
    OTEL_SERVICE_NAME: "gatewayserver"
```

**Lưu ý**: `OTEL_SERVICE_NAME` nên khớp với `SPRING_APPLICATION_NAME` để đảm bảo tính nhất quán, mặc dù điều này không bắt buộc.

## Bước 3: Tạo Cấu hình Tempo

Tạo cấu trúc thư mục mới: `observability/tempo/`

Tạo file cấu hình `tempo.yml` với nội dung sau:

```yaml
server:
  http_listen_port: 3100

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
        http:

storage:
  trace:
    backend: local
    local:
      path: /tmp/tempo/traces
    wal:
      path: /tmp/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000

query_frontend:
  search:
    max_duration: 0s

compactor:
  compaction:
    block_retention: 1h

metrics_generator:
  registry:
    external_labels:
      source: tempo
  storage:
    path: /tmp/tempo/generator/wal
```

### Các Tham số Cấu hình

- **http_listen_port**: 3100 - Cổng mà Tempo lắng nghe các yêu cầu HTTP
- **trace_idle_period**: 10 giây - Thời gian trước khi coi một trace là idle
- **max_block_bytes**: Kích thước tối đa của các block trace
- **max_block_duration**: Thời gian tối đa cho các block trace

**Lưu ý**: Các cấu hình này nên tuân theo tài liệu chính thức của Tempo và thường được quản lý bởi đội platform trong môi trường production.

## Bước 4: Thêm Service Tempo vào Docker Compose

Thêm service Tempo trong file `docker-compose.yml` (phía trên service Grafana):

```yaml
tempo:
  image: grafana/tempo:latest
  container_name: tempo
  command: [ "-config.file=/etc/tempo-config.yml" ]
  ports:
    - "3110:3100"  # Cổng external khác vì 3100 đã được gateway sử dụng
    - "4317:4317"
  volumes:
    - ./observability/tempo/tempo.yml:/etc/tempo-config.yml:ro
  networks:
    - microservices-network
```

**Quan trọng**: Cổng 3100 được map sang 3110 ở bên ngoài vì cổng 3100 đã được gateway service sử dụng.

## Bước 5: Cấu hình Data Source Grafana cho Tempo

Cập nhật file `datasource.yml` trong thư mục cấu hình Grafana.

Thêm data source Tempo cùng với Prometheus và Loki hiện có:

```yaml
apiVersion: 1

deleteDatasources:
  - name: Tempo
    orgId: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100

  - name: Tempo
    type: tempo
    access: proxy
    uid: tempo
    url: http://tempo:3100
    jsonData:
      httpMethod: GET
      tracesToLogs:
        datasourceUid: loki
```

### Cấu hình Data Source

- **name**: Tempo
- **type**: tempo
- **uid**: tempo (định danh duy nhất)
- **url**: http://tempo:3100 - Grafana kết nối với Tempo thông qua tên service và cổng này

## Tổng quan Kiến trúc

```
Microservices (với OpenTelemetry Agent)
    ↓ (traces qua OTLP)
Tempo (Cổng 4317)
    ↓ (truy vấn traces)
Grafana (Cổng 3000)
    → Tempo Data Source
```

## Kiểm tra

Sau khi áp dụng các thay đổi này:

1. Khởi động tất cả ứng dụng bằng Docker Compose
2. Truy cập Grafana dashboard
3. Điều hướng đến Explore → Chọn data source Tempo
4. Thực hiện một số request qua các microservices của bạn
5. Xem distributed traces trong Grafana

## Lợi ích

- **Tầm nhìn end-to-end**: Theo dõi các request qua nhiều microservices
- **Tối ưu hiệu suất**: Xác định các điểm nghẽn và vấn đề về độ trễ
- **Debug**: Theo dõi luồng request qua hệ thống
- **Tích hợp**: Tích hợp liền mạch với Grafana, Prometheus và Loki hiện có

## Bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khởi động tất cả các ứng dụng và xem distributed tracing hoạt động.

## Tóm tắt

Cấu hình này cho phép distributed tracing cho các microservices Spring Boot sử dụng:
- **OpenTelemetry**: Instrumentation tracing dựa trên agent
- **Tempo**: Backend distributed tracing
- **Grafana**: Giao diện trực quan hóa và truy vấn

Thiết lập này cung cấp khả năng quan sát toàn diện cùng với hạ tầng metrics (Prometheus) và logs (Loki) hiện có.



================================================================================
FILE: 82-distributed-tracing-demo-with-opentelemetry.md
================================================================================

# Demo Distributed Tracing với OpenTelemetry

## Tổng quan

Hướng dẫn này trình bày cách triển khai và kiểm tra distributed tracing trong kiến trúc microservices sử dụng OpenTelemetry, Docker Compose và Grafana.

## Yêu cầu

- Tất cả Docker images của microservices đã được tạo với tích hợp OpenTelemetry
- Docker Compose đã được cài đặt
- Postman để kiểm tra API

## Khởi động Microservices

### Thiết lập ban đầu

Khởi động tất cả containers từ production profile sử dụng Docker Compose:

```bash
docker-compose up -d
```

**Quan trọng**: Đảm bảo tất cả Docker images của microservices đã được build với các thay đổi mới nhất liên quan đến OpenTelemetry trước khi chạy lệnh này.

## Xử lý sự cố Health Checks của Container

### Vấn đề: Containers thất bại trong Health Checks

Khi khởi động containers, bạn có thể gặp lỗi với accounts, cards và loans microservices. Điều này xảy ra vì:

1. OpenTelemetry Java agent JAR (20-30 MB) cần được load vào bộ nhớ
2. Quá trình loading này tốn thêm thời gian trong quá trình khởi động
3. Cấu hình health check mặc định không cho phép đủ thời gian để khởi tạo

### Giải pháp: Điều chỉnh tham số Health Check

Chỉnh sửa cài đặt health check trong file Docker Compose cho tất cả microservices:

**Cấu hình ban đầu:**
- Interval: 10s
- Retries: 10

**Cấu hình cập nhật:**
- Interval: 20s
- Retries: 20

Áp dụng những thay đổi này cho:
- Config Server
- Eureka Server
- Accounts Microservice
- Loans Microservice
- Cards Microservice
- Gateway Server (không cần health check)

### Khởi động lại Containers

Sau khi cập nhật cấu hình:

```bash
# Dừng và xóa các containers hiện tại
docker-compose down

# Khởi động containers với cấu hình đã cập nhật
docker-compose up -d
```

**Lưu ý**: Quá trình khởi động bây giờ sẽ mất khoảng 4+ phút do khoảng thời gian retry được mở rộng.

## Xác minh triển khai

### Kiểm tra trạng thái Container

1. Mở Docker Desktop
2. Xác minh tất cả containers đang chạy thành công
3. Kiểm tra logs của từng microservice

### Xác minh OpenTelemetry Agent được load

Trong logs của accounts microservice, bạn sẽ thấy:

```
Loading the Java Agent Library present inside /app/libs
```

Cấu trúc container bao gồm:
- Thư mục `/app/libs/` chứa tất cả JARs từ pom.xml
- OpenTelemetry JAR được load thông qua `JAVA_TOOL_OPTIONS` được định nghĩa trong Docker Compose

### Xác nhận Gateway Server

Xác minh Gateway Server đang chạy trên cổng 8072.

## Kiểm tra APIs

Sử dụng Postman để kiểm tra các endpoints sau:

### 1. Tạo tài khoản
- **Endpoint**: POST `/create` (Accounts Microservice)
- **Kết quả mong đợi**: 
  - Status Code: 201
  - Message: "Account created successfully"

### 2. Tạo thông tin thẻ
- **Endpoint**: POST `/create` (Cards Microservice)
- **Kết quả mong đợi**: 
  - Status: "Card details created successfully"

### 3. Tạo thông tin khoản vay
- **Endpoint**: POST `/create` (Loans Microservice)
- **Kết quả mong đợi**: 
  - Status: "Loan created successfully"

### 4. Lấy thông tin khách hàng
- **Endpoint**: GET `/fetchCustomerDetails`
- **Kết quả mong đợi**: 
  - Thông tin tài khoản
  - Thông tin khoản vay
  - Thông tin thẻ

## Xem Distributed Tracing trong Grafana

Sau khi kiểm tra thành công các APIs, truy cập Grafana để xem thông tin distributed tracing.

Dữ liệu tracing sẽ hiển thị:
- Luồng request qua các microservices
- Các phụ thuộc giữa các services
- Metrics về hiệu suất
- Độ trễ của request

## Những điểm chính

1. **Tích hợp OpenTelemetry**: Java agent tự động instrument các microservices của bạn cho distributed tracing
2. **Cấu hình Health Check**: Điều chỉnh các tham số health check dựa trên yêu cầu khởi động của ứng dụng
3. **Thời gian khởi động Container**: Việc load OpenTelemetry agent tăng thêm overhead khi khởi động
4. **End-to-End Tracing**: Tất cả API calls được trace qua toàn bộ hệ sinh thái microservices

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách phân tích và diễn giải thông tin tracing trong Grafana, bao gồm:
- Hiểu về trace spans
- Xác định các bottleneck về hiệu suất
- Phân tích các phụ thuộc giữa services
- Thiết lập alerts dựa trên dữ liệu tracing



================================================================================
FILE: 83-distributed-tracing-demo-with-grafana-tempo.md
================================================================================

# Demo Distributed Tracing với Grafana và Tempo

## Tổng quan

Hướng dẫn này trình bày cách triển khai distributed tracing trong các microservices Spring Boot sử dụng Grafana, Loki, Prometheus và Tempo. Chúng ta sẽ khám phá cách theo dõi các request qua nhiều microservices và phân tích các điểm nghẽn hiệu suất.

## Yêu cầu trước

- Các microservices Spring Boot (accounts, cards, loans, gateway)
- Thiết lập Grafana với các nguồn dữ liệu:
  - Loki (cho logs)
  - Prometheus (cho metrics)
  - Tempo (cho distributed tracing)

## Xem Logs với Loki

### Truy cập Logs

1. Điều hướng đến Grafana và chọn **Loki** làm nguồn dữ liệu
2. Truy vấn logs cho microservice accounts
3. Kiểm tra các mục log với thông tin tracing

### Cấu trúc mẫu Log

Mẫu logging tuân theo cấu trúc sau:

```
[MỨC ĐỘ] [TÊN_ỨNG_DỤNG, TRACE_ID, SPAN_ID]
```

**Các thành phần:**
- **Mức độ (Severity)**: 5 ký tự đầu tiên chỉ mức độ log (DEBUG, INFO, WARN)
- **Tên ứng dụng**: Tên microservice (ví dụ: accounts)
- **Trace ID**: Định danh chung cho tất cả microservices trong một request
- **Span ID**: Định danh duy nhất cho mỗi lần gọi service/method

### Ví dụ câu lệnh Log

```
INFO [accounts, 1a2b3c4d5e6f7g8h, 9i0j1k2l3m4n] fetchCustomerDetails() method end
```

## Tracing qua các Microservices

### Tìm kiếm Logs liên quan

1. Trích xuất **Trace ID** từ log của bất kỳ microservice nào
2. Tìm kiếm cùng Trace ID trong các microservices khác (cards, loans, gateway)
3. Mỗi microservice sẽ có cùng Trace ID nhưng khác Span ID

**Điểm quan trọng**: Trace ID không đổi trên tất cả microservices, trong khi Span ID thay đổi cho mỗi service hoặc method được gọi.

### Các trường hợp sử dụng

- Theo dõi các method được thực thi qua các services
- Debug các tình huống ngoại lệ với các câu lệnh log có liên quan
- Hiểu luồng request hoàn chỉnh qua các microservices của bạn

## Trực quan hóa Traces với Tempo

### Truy cập Tempo

1. Trong Grafana, chọn **Tempo** làm nguồn dữ liệu
2. Tìm kiếm sử dụng Trace ID từ bất kỳ microservice nào
3. Chạy truy vấn để xem trực quan hóa trace

### Hiểu về Trực quan hóa Trace

Giao diện Tempo cung cấp biểu đồ waterfall đẹp mắt hiển thị:

#### Luồng Request

```
Gateway Server
  └─> API fetchCustomerDetails (Accounts)
      ├─> CustomerController.fetchCustomerDetails
      │   └─> Repository Layer (lấy dữ liệu account)
      ├─> Microservice Loans
      │   └─> Lấy thông tin khoản vay
      └─> Microservice Cards
          └─> Lấy thông tin thẻ
```

### Tính năng chính

1. **Khả năng hiển thị cấp method**: Xem tất cả các method được gọi và thời gian thực thi
2. **Phân tích hiệu suất**: Xác định method hoặc service nào tiêu tốn nhiều thời gian nhất
3. **Thời gian tổng hợp**: Các service cha hiển thị thời gian tích lũy bao gồm cả các lời gọi service con
4. **Thời gian riêng lẻ**: Mỗi service hiển thị thời gian thực thi của chính nó

### Phân tích điểm nghẽn hiệu suất

- **Thời gian cấp cao nhất**: Hiển thị thời gian tổng hợp cho tất cả các lời gọi downstream
- **Thời gian cấp thấp hơn**: Hiển thị thời gian thực thi của từng service/method riêng lẻ
- Dễ dàng xác định các service hoặc method chậm gây ra trзадержки

### Lợi ích khi Debug

- Theo dõi hành trình request qua toàn bộ mạng microservice
- Xác định chính xác nơi request thất bại hoặc bị kẹt
- Hiểu đặc điểm hiệu suất của từng service

## So sánh với các công cụ khác

### Zipkin

**Khả năng:**
- Trực quan hóa distributed tracing
- Tương tự Tempo để xem thông tin trace

**Hạn chế:**
- Chỉ cung cấp thông tin tracing
- Không có chế độ xem logs tích hợp
- Sản phẩm riêng biệt không có dashboard thống nhất

### Jaeger (của Red Hat)

**Khả năng:**
- Xác định distributed tracing
- Tốt cho trực quan hóa trace

**Hạn chế:**
- Không có thông tin logs tích hợp
- Thiếu dashboard observability thống nhất

### Ưu điểm của Tempo

**Tại sao Tempo là lựa chọn tốt nhất:**

1. **Tích hợp Grafana**: Hoạt động liền mạch trong hệ sinh thái Grafana
2. **Dashboard thống nhất**: Truy cập logs, metrics và traces ở một nơi
3. **Observability hoàn chỉnh**: Kết hợp:
   - **Loki** cho logs
   - **Prometheus** cho metrics
   - **Tempo** cho traces
4. **Ba trụ cột của Observability**: Logs, metrics và traces tất cả trong một sản phẩm

## Ba trụ cột của Observability

1. **Logs**: Thông tin chi tiết về sự kiện (Loki)
2. **Metrics**: Đo lường hiệu suất (Prometheus)
3. **Traces**: Theo dõi luồng request (Tempo)

## Các phương pháp hay nhất

1. **Sử dụng Trace IDs nhất quán** trên tất cả microservices
2. **Thêm các câu lệnh log có ý nghĩa** tại các điểm thực thi quan trọng
3. **Giám sát thời gian tổng hợp và riêng lẻ** để xác định điểm nghẽn
4. **Tận dụng giao diện thống nhất của Grafana** cho observability toàn diện
5. **Triển khai các mẫu logging phù hợp** với mức độ nghiêm trọng, tên ứng dụng và thông tin trace

## Tóm tắt

Distributed tracing với Grafana Tempo cung cấp các khả năng mạnh mẽ để:
- Hiểu luồng request qua các microservices
- Xác định điểm nghẽn hiệu suất
- Debug các hệ thống phân tán phức tạp
- Đạt được observability hoàn chỉnh với logs, metrics và traces

Sự tích hợp của Tempo, Loki và Prometheus trong Grafana cung cấp giải pháp toàn diện cho observability và monitoring của microservices.

---

**Các bước tiếp theo**: Khám phá các tính năng nâng cao của Grafana và thiết lập cảnh báo tùy chỉnh dựa trên các metrics từ trace.



================================================================================
FILE: 84-integrating-loki-tempo-derived-fields-grafana.md
================================================================================

# Tích Hợp Loki với Tempo Sử Dụng Derived Fields trong Grafana

## Tổng Quan

Hướng dẫn này trình bày cách tạo điều hướng liền mạch giữa log Loki và distributed tracing Tempo trong Grafana sử dụng derived fields. Tích hợp này cho phép các nhà phát triển truy cập trực tiếp thông tin trace từ các câu lệnh log mà không cần tra cứu trace ID thủ công.

## Vấn Đề Đặt Ra

Với cấu hình cơ bản, trace ID và span ID hiển thị trong log Loki. Tuy nhiên, để xem thông tin tracing chi tiết trong Tempo, các nhà phát triển phải:
1. Sao chép trace ID từ log
2. Điều hướng đến Tempo
3. Tìm kiếm trace ID theo cách thủ công

Quy trình làm việc này không hiệu quả và làm gián đoạn quá trình gỡ lỗi.

## Giải Pháp: Derived Fields

Derived fields trong Loki cho phép tự động trích xuất dữ liệu từ log message và liên kết với các data source khác của Grafana như Tempo.

## Các Bước Cấu Hình

### Phương Pháp 1: Cấu Hình Qua Giao Diện

1. **Điều Hướng đến Loki Data Source**
   - Vào Connections → Data Sources
   - Chọn Loki data source

2. **Thêm Derived Field**
   - Trong phần "Derived fields", nhấp "Add"
   - Cấu hình các thông tin sau:
     - **Field Name**: `trace_id`
     - **Regex Pattern**: Tạo pattern để khớp với định dạng log của bạn
     - **Internal Link**: Chọn Tempo làm data source đích
     - **Query**: `${__value.raw}` (truyền giá trị đã trích xuất cho Tempo)

3. **Kiểm Tra Pattern**
   - Sử dụng tính năng debug log message
   - Dán một mẫu log entry từ microservice của bạn
   - Xác minh rằng trace ID được trích xuất chính xác

4. **Lưu Cấu Hình**
   - Nhấp "Save and Test"

5. **Xác Minh Tích Hợp**
   - Vào Explore
   - Truy vấn logs: `{container="accounts-microservice"}`
   - Nhấp vào bất kỳ log entry nào có thông tin trace
   - Một link "Tempo" sẽ xuất hiện bên cạnh trường trace ID
   - Nhấp vào link sẽ mở thông tin tracing đầy đủ

### Phương Pháp 2: File Cấu Hình (Được Khuyến Nghị)

Để cấu hình tồn tại qua các lần khởi động lại Grafana, định nghĩa derived fields trong file `datasource.yml`:

```yaml
datasources:
  - name: Loki
    type: loki
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "trace_id=(\\w+)"
          name: trace_id
          url: "$${__value.raw}"
```

**Lưu Ý Quan Trọng:**
- Tham chiếu đến Tempo data source UID (thường là `tempo`)
- Sử dụng dấu gạch chéo ngược kép (`\\`) trong regex pattern để escape trong YAML
- Sử dụng ký hiệu đô la kép (`$$`) cho tham chiếu biến trong YAML

## Lợi Ích

1. **Cải Thiện Trải Nghiệm Nhà Phát Triển**: Điều hướng trực tiếp từ logs đến traces
2. **Gỡ Lỗi Nhanh Hơn**: Không cần sao chép trace ID thủ công
3. **Tích Hợp Liền Mạch**: Hoạt động tự động cho tất cả log entries
4. **Cấu Hình Bền Vững**: Cấu hình dựa trên file tồn tại qua các lần khởi động lại Grafana

## Ví Dụ Use Case

Khi điều tra các vấn đề trong accounts microservice:
1. Truy vấn logs trong Grafana Explore
2. Tìm log entry liên quan
3. Nhấp vào link Tempo bên cạnh trace ID
4. Xem distributed trace đầy đủ với tất cả các tương tác service

## Chi Tiết Kỹ Thuật

- **Data Sources**: Loki (logs) và Tempo (traces)
- **Pattern Matching**: Regular expressions trích xuất trace ID từ log messages
- **Phương Thức Tích Hợp**: Liên kết nội bộ giữa các Grafana data sources
- **Query Parameter**: `${__value.raw}` truyền trace ID đã trích xuất

## Kết Luận

Derived fields cung cấp một cách mạnh mẽ để kết nối các data source observability khác nhau trong Grafana. Bằng cách liên kết Loki logs với Tempo traces, các nhà phát triển có thể điều hướng liền mạch giữa log messages và thông tin distributed tracing, cải thiện đáng kể trải nghiệm gỡ lỗi và khắc phục sự cố trong kiến trúc microservices.

## Chủ Đề Liên Quan

- Distributed Tracing với OpenTelemetry
- Cấu Hình Grafana Tempo
- Loki Log Aggregation
- Microservices Observability
- Tích Hợp Spring Boot với Grafana Stack



================================================================================
FILE: 85-observability-monitoring-section-summary.md
================================================================================

# Khả Năng Quan Sát và Giám Sát trong Microservices - Tóm Tắt Phần

## Tổng Quan

Phần này đã đề cập đến các chủ đề toàn diện về khả năng quan sát và giám sát trong kiến trúc microservices sử dụng hệ sinh thái Grafana và các công cụ tracing hiện đại.

## Triển Khai Distributed Tracing

### Luồng Kiến Trúc

Việc triển khai distributed tracing tuân theo luồng sau:

1. **Microservices** - Các ứng dụng được tích hợp OpenTelemetry Agent JAR
2. **OpenTelemetry Agent** - Tự động chèn thông tin trace vào microservices
3. **Tempo** - Tổng hợp tất cả thông tin tracing từ nhiều dịch vụ
4. **Grafana** - Truy vấn và trực quan hóa traces để phân tích

### Các Thành Phần Chính

- **OpenTelemetry Agent JAR**: Tự động instrument các ứng dụng Java để thu thập dữ liệu trace
- **Tempo**: Backend distributed tracing lưu trữ và truy xuất dữ liệu trace
- **Grafana**: Cung cấp giao diện người dùng để truy vấn và trực quan hóa traces

## Những Điểm Chính Cần Ghi Nhớ

### Điểm Học Tập

1. **Phạm Vi Toàn Diện**: Nhiều chủ đề về khả năng quan sát và giám sát đã được thảo luận trong phần này
2. **Hệ Sinh Thái Grafana**: Nhiều sản phẩm khác nhau trong hệ sinh thái Grafana được giới thiệu cho các nhu cầu giám sát khác nhau
3. **Triển Khai Thực Tế**: Các bản demo thực hành cho thấy các tình huống triển khai trong thế giới thực

### Khuyến Nghị Quan Trọng

- **Dành Thời Gian Tiếp Thu**: Phần này đề cập đến nhiều chủ đề và công cụ phức tạp
- **Làm Quen Với Các Công Cụ**: Dành thời gian thực hành với các sản phẩm trong hệ sinh thái Grafana
- **Tài Liệu Tham Khảo**: Tất cả các chi tiết đã thảo luận đều có trong slides để tham khảo nhanh
- **Chuẩn Bị Phỏng Vấn**: Sử dụng các tài liệu này để chuẩn bị cho các buổi phỏng vấn liên quan đến microservice

## Mã Nguồn và Tài Nguyên

### GitHub Repository

Tất cả các thay đổi mã nguồn cho phần này đã được commit vào GitHub repository:

- **Repository**: `eazybytes/microservices`
- **Phần**: Section 11
- **Commit Message**: "Observability and Monitoring in Microservices"

### Cấu Hình Docker Compose

- Các thay đổi Docker Compose của production profile đã được sao chép sang:
  - Default profile
  - QA profile
- Điều này đảm bảo tính nhất quán giữa các môi trường khác nhau

### Docker Images

Tất cả các Docker images của microservices đã được đẩy lên Docker Hub với tag: **S11**

Bạn có thể tìm thấy các images này trong các repository microservice tương ứng trên Docker Hub.

## Phép So Sánh về Kỹ Năng Observability

### Tham Chiếu Phim "Taken"

Một phép tương tự đáng nhớ được rút ra từ bộ phim "Taken 3" để minh họa sức mạnh của observability:

> "Tôi không biết bạn đang ẩn đâu trong mạng lưới microservice của tôi. Tôi không biết bạn ở đâu, nhưng tôi có một bộ kỹ năng đặc biệt liên quan đến khả năng quan sát và giám sát mà tôi đã học được từ khóa học microservice của eazybytes. Sử dụng những kỹ năng đó, tôi sẽ tìm thấy bạn và tôi sẽ sửa chữa bạn."

Sự so sánh hài hước này nhấn mạnh cách các công cụ observability giúp developers có thể:
- **Phát Hiện** các lỗi ẩn trong mạng lưới microservice phức tạp
- **Định Vị** các vấn đề trên các hệ thống phân tán
- **Giải Quyết** các vấn đề một cách hiệu quả bằng cách sử dụng kỹ năng giám sát

## Kết Luận

Phần này đã kết thúc thành công các cuộc thảo luận về khả năng quan sát và giám sát cho kiến trúc microservices. Với các kỹ năng và công cụ đã được đề cập, các developers giờ đây đã được trang bị để:

- Triển khai distributed tracing trong Spring Boot microservices
- Giám sát hiệu suất và tình trạng của ứng dụng
- Khắc phục sự cố trong môi trường production
- Xây dựng kiến trúc microservice có khả năng phục hồi và quan sát được

---

*Chúc bạn học tốt và hẹn gặp lại ở phần tiếp theo!*



================================================================================
FILE: 86-securing-microservices-challenge-9-introduction.md
================================================================================

# Bảo Mật Microservices - Giới Thiệu Thách Thức 9

## Tổng Quan

Phần này tập trung vào **Thách thức 9** trong kiến trúc microservices: **Bảo Mật Microservices**. Bảo mật là một khía cạnh quan trọng của bất kỳ ứng dụng microservices nào, vì không có các biện pháp bảo mật phù hợp, dữ liệu nhạy cảm sẽ bị lộ cho những người dùng trái phép.

## Tại Sao Bảo Mật Quan Trọng

Dù ứng dụng web, ứng dụng di động, hoặc microservices của bạn được thiết kế tốt đến đâu, chúng cũng trở nên vô giá trị nếu không có triển khai bảo mật phù hợp. Các tổ chức không thể để lộ dữ liệu nhạy cảm cho mọi người, và các ứng dụng không có bảo mật sẽ không bao giờ nhận được sự tin tưởng hoặc đề xuất từ người dùng.

## Các Thách Thức Bảo Mật Chính

### 1. Bảo Vệ Chống Truy Cập Trái Phép

**Vấn Đề Hiện Tại:**
- Bất kỳ ai cũng có thể gọi các microservices của chúng ta
- Người dùng có thể lấy thông tin tài khoản của người khác chỉ bằng cách cung cấp số điện thoại
- Không có bảo vệ chống lại truy cập trái phép

**Câu hỏi:** Làm thế nào chúng ta sẽ bảo mật microservices khỏi người dùng trái phép?

### 2. Xác Thực và Ủy Quyền

Hiểu sự khác biệt giữa hai khái niệm quan trọng này:

#### Xác Thực (Authentication)
- **Định nghĩa:** Quá trình xác định người hoặc ứng dụng đang cố gắng gọi microservices của bạn
- **Mục đích:** Xác minh "ai" đang thực hiện yêu cầu

#### Ủy Quyền (Authorization)
- **Định nghĩa:** Một cơ chế thực thi quyền truy cập đặc quyền sau khi xác thực
- **Mục đích:** Xác định "cái gì" mà người dùng đã xác thực có thể truy cập
- Chỉ những người dùng/ứng dụng có đủ đặc quyền mới có thể truy cập các microservices hoặc ứng dụng web cụ thể

### 3. Quản Lý Danh Tính và Truy Cập Tập Trung (IAM)

**Vấn Đề với Bảo Mật Phân Tán:**
- Triển khai logic bảo mật trong từng microservice riêng lẻ là không thực tế
- Với hàng trăm microservices, việc bảo trì trở thành cơn ác mộng
- Bất kỳ thay đổi yêu cầu bảo mật nào cũng sẽ cần cập nhật trên tất cả microservices

**Giải Pháp:**
- Có một thành phần tập trung riêng biệt chịu trách nhiệm cho:
  - Lưu trữ tất cả thông tin xác thực người dùng
  - Xử lý xác thực
  - Quản lý ủy quyền
  - Phục vụ toàn bộ mạng microservices

## Kiến Trúc Giải Pháp

Để vượt qua các thách thức bảo mật này, chúng ta sẽ tận dụng các công nghệ sau:

### 1. Các Tiêu Chuẩn Bảo Mật
- **OAuth2:** Giao thức tiêu chuẩn ngành cho ủy quyền
- **OpenID Connect:** Lớp xác thực trên OAuth2

### 2. Sản Phẩm IAM
- **Keycloak:** Giải pháp Quản lý Danh tính và Truy cập mã nguồn mở

### 3. Framework Bảo Mật
- **Spring Security:** Framework bảo mật toàn diện của Spring cho các ứng dụng Java

## Những Gì Bạn Sẽ Học

Trong suốt phần này, bạn sẽ:
1. Triển khai các tiêu chuẩn OAuth2 và OpenID Connect
2. Cấu hình và tích hợp Keycloak làm giải pháp IAM của bạn
3. Bảo mật microservices sử dụng framework Spring Security
4. Xử lý xác thực và ủy quyền ở quy mô lớn
5. Triển khai quản lý bảo mật tập trung

## Điều Kiện Tiên Quyết

### Kiến Thức Spring Security

Mặc dù khóa học này đề cập đến Spring Security ở mức độ cao, nếu bạn mới với framework này, hãy cân nhắc việc nâng cao kiến thức của mình thông qua các khóa học Spring Security chuyên sâu. Spring Security là một kỹ năng bắt buộc cho:
- Lập trình viên Java
- Lập trình viên full-stack
- Kiến trúc sư phần mềm
- Lập trình viên cấp cao

Hiểu biết toàn diện về Spring Security (bao gồm JWT tokens và OAuth2) là cần thiết để xây dựng các ứng dụng bảo mật, sẵn sàng cho sản xuất.

## Phương Pháp Tiếp Cận Khóa Học

Phần này sẽ:
- Giải thích các khái niệm Spring Security ở mức độ cao
- Trình diễn triển khai thực tế
- Cho thấy cách tích hợp tất cả các thành phần bảo mật
- Tập trung vào các mẫu bảo mật cụ thể cho microservices

**Lưu ý:** Để có nội dung Spring Security chuyên sâu (15+ giờ nội dung), hãy cân nhắc đăng ký các khóa học Spring Security chuyên biệt bao quát framework từ cơ bản đến nâng cao.

## Tóm Tắt

Bảo mật là không thể thương lượng trong kiến trúc microservices. Bằng cách triển khai xác thực, ủy quyền phù hợp và quản lý danh tính tập trung sử dụng OAuth2, OpenID Connect, Keycloak và Spring Security, bạn có thể xây dựng các microservices mạnh mẽ, bảo mật để bảo vệ dữ liệu nhạy cảm và đảm bảo chỉ những người dùng được ủy quyền mới có quyền truy cập vào hệ thống của bạn.

---

**Các Bước Tiếp Theo:** Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào việc triển khai các biện pháp bảo mật này trong kiến trúc microservices của chúng ta.



================================================================================
FILE: 87-oauth2-introduction-and-basic-authentication-problems.md
================================================================================

# Giới thiệu OAuth2 và Vấn đề của Xác thực Cơ bản

## Tổng quan

Tài liệu này giải thích các khái niệm cơ bản về OAuth2, các vấn đề mà nó giải quyết, và lý do tại sao nó được ưu tiên hơn phương thức xác thực cơ bản truyền thống trong việc bảo mật microservices và ứng dụng web.

## OAuth2 là gì?

OAuth2 là một tiêu chuẩn bảo mật hoặc đặc tả bảo mật mà bất kỳ tổ chức nào cũng có thể tuân theo để bảo mật:
- Ứng dụng web
- Ứng dụng di động
- Microservices

Các tổ chức có thể tận dụng đặc tả OAuth2 để bảo mật ứng dụng của họ bất kể loại ứng dụng nào.

## Vấn đề với Xác thực Cơ bản

### Cách Xác thực Cơ bản Hoạt động

Trong những ngày đầu phát triển web, xác thực tuân theo quy trình sau:

1. Các trang web yêu cầu thông tin đăng nhập của người dùng thông qua biểu mẫu HTML
2. Người dùng nhập thông tin đăng nhập của họ
3. Thông tin đăng nhập được gửi đến máy chủ backend
4. Máy chủ backend thực hiện xác thực
5. Sau khi xác thực thành công, máy chủ tạo ra một giá trị phiên (session)
6. Phiên được lưu trữ trong cookie của trình duyệt
7. Người dùng có thể truy cập các tài nguyên được bảo vệ trong khi phiên còn hoạt động

### Nhược điểm của Xác thực Cơ bản

#### 1. Sự Kết hợp Chặt chẽ giữa Logic Nghiệp vụ và Logic Xác thực

- Máy chủ backend chứa cả logic nghiệp vụ và logic xác thực được kết hợp chặt chẽ
- Thay đổi logic xác thực đòi hỏi phải kiểm tra cẩn thận để đảm bảo logic nghiệp vụ không bị ảnh hưởng
- Cần kiểm thử hồi quy rộng rãi
- Không thân thiện với thiết bị di động hoặc REST API

#### 2. Không có Giải pháp Thích hợp cho Quyền truy cập Tạm thời của Bên thứ ba

**Ví dụ Tình huống:**
- Bạn lưu trữ ảnh trong Google Photos
- Một trang web bên thứ ba cung cấp tính năng chỉnh sửa ảnh (collage, bộ lọc, v.v.)
- Để sử dụng các tính năng này, bạn cần nhập ảnh từ Google Photos

**Vấn đề:**
- Với xác thực cơ bản, bạn phải chia sẻ thông tin đăng nhập Google của mình với trang web bên thứ ba
- Bạn phải tin tưởng rằng họ sẽ không lạm dụng thông tin đăng nhập của bạn
- Đây là một rủi ro bảo mật nghiêm trọng

**Giải pháp OAuth2:**
- OAuth2 cung cấp cơ chế thích hợp để tạm thời cấp quyền truy cập vào Google Photos
- Không cần chia sẻ thông tin đăng nhập Google thực tế của bạn
- Bên thứ ba nhận được quyền truy cập hạn chế, tạm thời

## Các Vấn đề mà OAuth2 Giải quyết

### Vấn đề 1: Xác thực và Ủy quyền Tập trung

**Ví dụ Thực tế: Các Sản phẩm của Google**

Google có nhiều sản phẩm:
- Gmail
- Google Maps
- YouTube
- Google Photos
- Google Drive

**Làm thế nào Google cho phép sử dụng cùng một tài khoản trên tất cả các sản phẩm?**

Google sử dụng framework OAuth2 với các tính năng chính sau:

1. **Máy chủ Ủy quyền Riêng biệt**: Tất cả logic xác thực và ủy quyền được tách ra thành một thành phần chuyên dụng gọi là máy chủ ủy quyền (authorization server hoặc authentication server)

2. **Điểm Xác thực Duy nhất**: Khi người dùng đăng nhập vào bất kỳ sản phẩm Google nào, thông tin đăng nhập được gửi đến cùng một auth server

3. **Lợi ích**:
   - Vị trí duy nhất cho logic bảo mật bất kể số lượng ứng dụng/microservices
   - Thay đổi logic bảo mật diễn ra ở một nơi
   - Dễ dàng bảo trì và cập nhật hơn

### Vấn đề 2: Truy cập Bên thứ ba An toàn Không cần Chia sẻ Thông tin Đăng nhập

**Ví dụ Thực tế: Đăng ký StackOverflow**

Khi đăng ký StackOverflow, bạn có nhiều tùy chọn:
- Truyền thống: Nhập tên, email và mật khẩu
- OAuth2: Đăng ký với Google, GitHub hoặc Facebook

**Cách OAuth2 Hoạt động trong Tình huống này:**

1. **Hành động của Người dùng**: Nhấp vào "Đăng ký với GitHub" trên StackOverflow
2. **Chuyển hướng**: Người dùng được chuyển hướng đến GitHub.com
3. **Xác thực**: Người dùng nhập thông tin đăng nhập GitHub trên trang web GitHub (không phải trên StackOverflow)
4. **Bảo mật Thông tin Đăng nhập**: StackOverflow không bao giờ thấy thông tin đăng nhập GitHub của bạn
5. **Chia sẻ Tài nguyên**: Sau khi xác thực thành công, GitHub chia sẻ thông tin cơ bản (tên, email) với StackOverflow
6. **Access Token**: GitHub phát hành một access token cho StackOverflow
7. **Đặc quyền Hạn chế**: Access token có đặc quyền hạn chế (ví dụ: chỉ đọc thông tin hồ sơ)
8. **Không có Quyền truy cập Nâng cao**: StackOverflow không thể thực hiện các thao tác nâng cao như tạo repositories

**Lợi ích Chính:**
- Không chia sẻ thông tin đăng nhập với ứng dụng bên thứ ba
- Quyền truy cập tạm thời với đặc quyền hạn chế
- Thông tin đăng nhập chính vẫn an toàn
- Bên thứ ba chỉ có thể truy cập các tài nguyên được cấp phép rõ ràng
- Có thể đăng nhập tự động bằng access token trong các phiên tương lai

## Tóm tắt

OAuth2 giải quyết các vấn đề bảo mật quan trọng mà xác thực cơ bản không thể xử lý:

1. **Tách biệt Mối quan tâm**: Tách rời xác thực/ủy quyền khỏi logic nghiệp vụ
2. **Bảo mật Tập trung**: Một auth server duy nhất cho tất cả ứng dụng và microservices
3. **Ủy quyền An toàn**: Quyền truy cập tạm thời, hạn chế mà không cần chia sẻ thông tin đăng nhập
4. **Thân thiện với Di động và REST API**: Được thiết kế cho kiến trúc ứng dụng hiện đại
5. **Tích hợp Bên thứ ba**: Cách an toàn để tích hợp với các dịch vụ bên ngoài

## Kết luận

OAuth2 đã trở thành tiêu chuẩn thực tế để bảo mật các ứng dụng hiện đại vì nó giải quyết các vấn đề cơ bản mà xác thực cơ bản không thể giải quyết. Bằng cách triển khai OAuth2, các tổ chức có thể cung cấp bảo mật tốt hơn, bảo trì dễ dàng hơn và tích hợp bên thứ ba an toàn hơn.

---

**Bước tiếp theo**: Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào các thành phần OAuth2, các luồng hoạt động và chi tiết triển khai cho microservices sử dụng Spring Boot.



================================================================================
FILE: 88-introduction-to-oauth2-framework.md
================================================================================

# Giới Thiệu Về OAuth2 Framework

## OAuth2 Là Gì?

**OAuth** là viết tắt của **Open Authorization** (Ủy quyền Mở). Đây là một giao thức miễn phí và mã nguồn mở được xây dựng dựa trên các tiêu chuẩn IETF, với giấy phép được cung cấp bởi Open Web Foundation. Điều này có nghĩa là bất kỳ ai cũng có thể sử dụng các đặc tả của OAuth framework trong ứng dụng của họ.

### Lịch Sử Phiên Bản

- **Phiên bản hiện tại**: OAuth 2.0 (thường được gọi là OAuth2)
- **Phiên bản tương lai**: OAuth 2.1 đang trong quá trình phát triển

## Khái Niệm Cốt Lõi

OAuth2 cho phép các ứng dụng cấp quyền truy cập dữ liệu của bạn cho các ứng dụng bên thứ ba. Quá trình này được gọi là **authorization** (ủy quyền) hoặc **delegated authorization** (ủy quyền được ủy nhiệm).

Lợi ích chính là bạn có thể ủy quyền cho một ứng dụng truy cập dữ liệu của bạn trong ứng dụng khác thay mặt bạn **mà không cần chia sẻ mật khẩu**.

## Các Lợi Thế Chính Của OAuth2

### 1. Hỗ Trợ Đa Dạng Ứng Dụng

OAuth2 hỗ trợ mọi loại ứng dụng và kịch bản trong thế giới web, bất kể loại ứng dụng nào. Nó cung cấp các **grant flows** (luồng cấp quyền) khác nhau cho nhiều kịch bản:

- **Giao tiếp Backend-to-Backend**: Luồng cấp quyền đặc biệt cho giao tiếp giữa các server
- **Ứng dụng UI/Mobile**: Luồng cấp quyền dành riêng cho ứng dụng frontend giao tiếp với backend server
- **Thiết bị IoT, Console, Smart TV**: Luồng cấp quyền chuyên biệt cho các thiết bị này

Bất kể loại giao tiếp nào bạn cần thiết lập giữa các ứng dụng hoặc thiết bị, OAuth2 đều có giải pháp thông qua các grant flows đa dạng.

### 2. Tách Biệt Logic Xác Thực

OAuth2 khuyến nghị xây dựng một thành phần riêng biệt gọi là **Authorization Server** (Máy chủ Ủy quyền). Server này chịu trách nhiệm:

- Nhận yêu cầu từ các client
- Cung cấp access token dựa trên xác thực thành công
- Đóng vai trò là điểm xác thực tập trung cho tất cả ứng dụng trong tổ chức

#### Lợi Ích Chính:

- **Điểm Xác Thực Duy Nhất**: Tất cả ứng dụng (bất kể loại hoặc số lượng) có thể kết nối đến cùng một auth server
- **Truy Cập Bên Thứ Ba**: Auth server có thể được truy cập bởi các ứng dụng bên ngoài (ví dụ: Stack Overflow truy cập auth server của GitHub)
- **Quản Lý Thông Tin Đăng Nhập Tập Trung**: Tất cả thông tin đăng nhập của người dùng và ứng dụng client được duy trì ở một vị trí bảo mật

Bằng cách tách biệt logic ủy quyền khỏi logic nghiệp vụ, các tổ chức có thể an toàn expose các authentication endpoint cho các ứng dụng khác.

### 3. Bảo Mật Nâng Cao - Không Chia Sẻ Mật Khẩu

Đây là **lợi thế chính** của OAuth2. Người dùng cuối không bao giờ phải chia sẻ thông tin đăng nhập khi cấp quyền truy cập cho ứng dụng bên thứ ba.

#### Ví Dụ Về Thẻ Truy Cập Khách Sạn

Hãy nghĩ về OAuth2 như quy trình check-in khách sạn:

1. **Check-in**: Khi bạn đến khách sạn và xác nhận đặt phòng, lễ tân cung cấp một thẻ truy cập
2. **Quyền Truy Cập Hạn Chế**: Thẻ chỉ mở được phòng cụ thể của bạn và cho phép sử dụng thang máy đến tầng có phòng của bạn
3. **Tạm Thời & Có Thể Thu Hồi**: Nếu bạn mất thẻ, khách sạn có thể vô hiệu hóa từ xa và cấp thẻ mới
4. **Đặc Quyền Theo Vai Trò**: Các thẻ khác nhau có đặc quyền khác nhau:
   - Thẻ khách: Chỉ truy cập phòng của bạn
   - Thẻ bộ phận dọn phòng: Truy cập bất kỳ phòng nào

#### Access Token Của OAuth2 Hoạt Động Tương Tự

- Auth server cấp **access token tạm thời** thay vì chia sẻ mật khẩu
- Token được cấp dựa trên **cấp độ đặc quyền** theo yêu cầu nghiệp vụ
- Người dùng khác nhau nhận các token khác nhau dựa trên nhu cầu truy cập của họ
- Token có thể bị thu hồi mà không ảnh hưởng đến thông tin đăng nhập thực tế

## Tổng Kết

OAuth2 cung cấp một cách an toàn, linh hoạt và chuẩn hóa để xử lý ủy quyền trên các loại ứng dụng và thiết bị khác nhau. Bằng cách sử dụng access token thay vì mật khẩu và duy trì một authorization server tập trung, nó cho phép truy cập được ủy quyền an toàn trong khi bảo vệ thông tin đăng nhập người dùng.

## Ứng Dụng Trong Microservices với Java Spring Boot

OAuth2 được tích hợp mạnh mẽ trong hệ sinh thái Spring Boot thông qua Spring Security OAuth2. Framework này cho phép:

- Xây dựng Authorization Server với Spring Authorization Server
- Bảo vệ các microservices với Resource Server
- Cấu hình các grant flows khác nhau phù hợp với kiến trúc microservices
- Tích hợp với các nhà cung cấp OAuth2 phổ biến (GitHub, Google, Facebook, etc.)

---

*Tài liệu này cung cấp cái nhìn tổng quan về OAuth2 framework và các lợi thế cốt lõi của nó trong phát triển ứng dụng hiện đại.*



================================================================================
FILE: 89-oauth2-terminology-and-roles-guide.md
================================================================================

# Khung OAuth2: Hướng Dẫn Thuật Ngữ và Vai Trò

## Giới Thiệu

Hiểu rõ thuật ngữ OAuth2 là rất quan trọng để triển khai bảo mật trong microservices và giao tiếp hiệu quả về framework trong môi trường chuyên nghiệp. Hướng dẫn này giải thích các thuật ngữ và vai trò chính trong khung OAuth2.

## Tại Sao Những Thuật Ngữ Này Quan Trọng

Khi triển khai bảo mật trong microservices hoặc thảo luận về OAuth2 trong phỏng vấn, việc sử dụng thuật ngữ phù hợp thể hiện chuyên môn và hiểu biết về framework. Những khái niệm này tạo nền tảng cho tất cả các luồng và triển khai OAuth2.

## Các Vai Trò và Thuật Ngữ OAuth2 Chính

### 1. Resource Owner (Chủ Sở Hữu Tài Nguyên)

**Định nghĩa:** Người dùng cuối sở hữu tài nguyên và có thẩm quyền cấp quyền truy cập vào chúng.

**Ví Dụ Kịch Bản:**
- Trong kịch bản Stack Overflow, bạn (người dùng cuối) là chủ sở hữu tài nguyên
- Bạn sở hữu tài nguyên trên máy chủ GitHub (địa chỉ email, tên hiển thị, chi tiết hồ sơ)
- Bạn ủy quyền cho Stack Overflow truy cập thông tin GitHub của bạn
- Trong kịch bản Google Photos, bạn sở hữu các bức ảnh được lưu trữ trên máy chủ của Google

**Điểm Chính:** Chủ sở hữu tài nguyên luôn là người sở hữu dữ liệu được truy cập.

### 2. Client (Khách Hàng/Ứng Dụng Khách)

**Định nghĩa:** Trang web, ứng dụng di động hoặc API muốn truy cập tài nguyên được bảo mật thay mặt cho chủ sở hữu tài nguyên.

**Đặc Điểm:**
- Gửi yêu cầu đến máy chủ ủy quyền
- Truy cập tài nguyên thay mặt cho chủ sở hữu tài nguyên
- Yêu cầu ủy quyền phù hợp trước khi truy cập tài nguyên được bảo vệ

**Ví Dụ:**
- Trang web Stack Overflow là client
- Nó kết nối với máy chủ ủy quyền của GitHub thay mặt bạn
- Nó lấy thông tin của bạn từ GitHub sau khi được ủy quyền

### 3. Authorization Server (Máy Chủ Ủy Quyền)

**Định nghĩa:** Thành phần máy chủ chịu trách nhiệm xác thực chủ sở hữu tài nguyên và cấp access token.

**Trách Nhiệm Chính:**
- Xác thực chủ sở hữu tài nguyên (người dùng cuối)
- Duy trì thông tin tài khoản người dùng
- Cấp access token sau khi xác thực thành công
- Quản lý luồng đồng ý và ủy quyền

**Yêu Cầu:**
- Chủ sở hữu tài nguyên phải có tài khoản đã đăng ký
- Xử lý thông tin xác thực (email, mật khẩu)
- Kiểm soát quy trình ủy quyền

**Ví Dụ:** Máy chủ xác thực của GitHub xác minh danh tính của bạn và cấp token cho Stack Overflow.

### 4. Resource Server (Máy Chủ Tài Nguyên)

**Định nghĩa:** Máy chủ lưu trữ các tài nguyên được bảo vệ của chủ sở hữu tài nguyên.

**Chức Năng:**
- Lưu trữ các tài nguyên thực tế (dữ liệu, ảnh, thông tin hồ sơ)
- Xác thực access token nhận được từ ứng dụng client
- Chỉ cung cấp tài nguyên khi có access token hợp lệ
- Thường tách biệt với máy chủ ủy quyền trong các hệ thống doanh nghiệp

**Ví Dụ:**
- Máy chủ tài nguyên của GitHub lưu trữ email và dữ liệu hồ sơ của bạn
- Máy chủ tài nguyên Google Photos lưu trữ ảnh của bạn
- Phản hồi các yêu cầu của client khi có ủy quyền phù hợp

### 5. Scopes (Phạm Vi/Quyền Hạn)

**Định nghĩa:** Các quyền chi tiết xác định hành động mà ứng dụng client có thể thực hiện và dữ liệu nào nó có thể truy cập.

**Mục Đích:**
- Kiểm soát đặc quyền của ứng dụng client
- Xác định quyền cụ thể (đọc, ghi, xóa)
- Bảo vệ dữ liệu của chủ sở hữu tài nguyên bằng kiểm soát truy cập chi tiết

**Cách Hoạt Động Của Scopes:**
1. Client yêu cầu các scope cụ thể từ máy chủ ủy quyền
2. Chủ sở hữu tài nguyên thấy màn hình đồng ý hiển thị các quyền được yêu cầu
3. Máy chủ ủy quyền cấp access token với các scope đã được phê duyệt
4. Máy chủ tài nguyên thực thi kiểm soát truy cập dựa trên scope

### Ví Dụ Thực Tế: Stack Overflow và GitHub

**Luồng Kịch Bản:**
1. Bạn nhấp vào "Sign up with GitHub" trên Stack Overflow
2. GitHub hiển thị màn hình đồng ý yêu cầu quyền
3. Scope được yêu cầu: "Email address (read only)" - Địa chỉ email (chỉ đọc)
4. Giải thích: "Ứng dụng này sẽ có thể đọc địa chỉ email riêng tư của bạn"
5. Bạn ủy quyền cho Stack Exchange
6. GitHub cấp access token với scope đọc email
7. Stack Overflow sử dụng token để lấy email và tên hiển thị của bạn
8. Tài khoản được tạo với thông tin đã lấy

### Ví Dụ Scope Của GitHub

**Scope Đặc Quyền Cao:**
- `repo`: Quyền truy cập đầy đủ vào kho lưu trữ công khai và riêng tư (đọc và ghi)
- Nên cấp một cách thận trọng

**Scope Đặc Quyền Hạn Chế:**
- `user:email`: Quyền đọc địa chỉ email của người dùng
- `read:user`: Quyền đọc dữ liệu hồ sơ của người dùng
- Phù hợp hơn cho các kịch bản xác thực cơ bản

## Thực Hành Tốt Nhất

1. **Nguyên Tắc Scope Tối Thiểu:** Chỉ yêu cầu các scope cần thiết cho chức năng của ứng dụng
2. **Đồng Ý Người Dùng:** Luôn tôn trọng quyết định của người dùng về quyền
3. **Tài Liệu Scope:** Ghi chú rõ ràng về các scope mà ứng dụng của bạn yêu cầu và lý do
4. **Nhận Thức An Ninh:** Thận trọng với các scope đặc quyền cao như quyền truy cập kho lưu trữ

## Triển Khai Doanh Nghiệp

Trong các tổ chức doanh nghiệp (GitHub, Google, Facebook), cơ sở hạ tầng OAuth2 thường bao gồm:
- Máy chủ ủy quyền riêng biệt cho xác thực
- Máy chủ tài nguyên chuyên dụng để lưu trữ dữ liệu
- Phân cấp scope được xác định rõ ràng
- Cơ chế xác thực token mạnh mẽ

## Tóm Tắt

Hiểu thuật ngữ OAuth2 giúp bạn:
- Triển khai kiến trúc microservices an toàn
- Giao tiếp hiệu quả về triển khai bảo mật
- Đưa ra quyết định sáng suốt về thiết kế scope và quyền
- Giải thích luồng xác thực trong phỏng vấn kỹ thuật

**Điểm Chính:** Năm khái niệm này (Resource Owner, Client, Authorization Server, Resource Server và Scopes) tạo nền tảng cho tất cả các triển khai OAuth2 và phải được hiểu kỹ lưỡng để có kiến trúc bảo mật thành công.

## Bước Tiếp Theo

Với những kiến thức nền tảng này, giờ bạn có thể khám phá:
- Các loại grant OAuth2 khác nhau
- Mẫu triển khai cho microservices
- Chiến lược quản lý token
- Cấu hình bảo mật nâng cao

---

*Hướng dẫn này cung cấp kiến thức nền tảng cần thiết để làm việc với OAuth2 trong môi trường microservices, đặc biệt với các ứng dụng Spring Boot.*



================================================================================
FILE: 9-service-discovery-and-registration-pattern.md
================================================================================

# Mẫu Khám Phá và Đăng Ký Dịch Vụ trong Microservices

## Tổng Quan

Trong các ứng dụng cloud-native và kiến trúc microservices, mẫu Service Discovery (Khám phá dịch vụ) cung cấp giải pháp hiệu quả để khắc phục những hạn chế của load balancer truyền thống. Mẫu này giải quyết thách thức cơ bản về cách các microservices giao tiếp với nhau trong môi trường động, nơi địa chỉ IP thay đổi thường xuyên.

## Service Discovery là gì?

Mẫu Service Discovery liên quan đến việc theo dõi và lưu trữ tất cả thông tin về các instance dịch vụ đang chạy trong một **service registry** (sổ đăng ký dịch vụ). Cách tiếp cận tập trung này cho phép các microservices định vị và giao tiếp với nhau một cách hiệu quả trên mạng.

### Các Thành Phần Chính

1. **Service Registry (Sổ đăng ký dịch vụ)**: Một máy chủ trung tâm (hoặc nhiều máy chủ) duy trì cái nhìn toàn cục về tất cả các instance dịch vụ đang chạy và địa chỉ của chúng.

2. **Service Registration (Đăng ký dịch vụ)**: Quá trình mà các instance microservice tự đăng ký với service registry khi chúng khởi động.

3. **Service Discovery (Khám phá dịch vụ)**: Cơ chế cho phép các microservices truy vấn registry để tìm và kết nối với các dịch vụ khác.

## Cách Thức Hoạt Động

### Quy Trình Đăng Ký

Khi một instance microservice mới khởi động:

1. **Đăng ký ban đầu**: Instance microservice kết nối với máy chủ trung tâm và đăng ký địa chỉ IP và thông tin cổng của nó
2. **Giám sát sức khỏe**: Instance gửi heartbeat định kỳ để xác nhận trạng thái sức khỏe của nó
3. **Hủy đăng ký tự động**: Khi heartbeat dừng lại hoặc instance tắt, nó sẽ tự động bị xóa khỏi registry

### Khám Phá và Giao Tiếp

Khi một microservice cần giao tiếp với dịch vụ khác:

1. Dịch vụ gọi (ví dụ: accounts microservice) truy vấn service registry
2. Registry trả về các instance khả dụng của dịch vụ đích (ví dụ: loans microservice)
3. Nếu có nhiều instance, load balancing sẽ tự động được áp dụng để phân phối workload

## Cân Bằng Tải (Load Balancing)

Service registry công nhận rằng nhiều instance của cùng một ứng dụng có thể hoạt động đồng thời. Khi có nhiều instance khả dụng:

- Registry thực hiện tra cứu để xác định các địa chỉ IP khả dụng
- Bên dưới, nó áp dụng chiến lược cân bằng tải
- Workload được phân phối đều cho tất cả các instance đang chạy

## Các Loại Service Discovery

### 1. Client-Side Service Discovery (Khám phá dịch vụ phía client)
- Client (microservice gọi) chịu trách nhiệm xác định vị trí mạng của các instance dịch vụ khả dụng
- Client truy vấn service registry và thực hiện load balancing
- **Cách tiếp cận này được đề cập trong phần này**

### 2. Server-Side Service Discovery (Khám phá dịch vụ phía server)
- Một router hoặc load balancer truy vấn service registry
- Client thực hiện request đến router, router xử lý service discovery
- **Cách tiếp cận này sẽ được demo sau khi triển khai với Kubernetes**

## Lợi Ích

1. **Hỗ trợ môi trường động**: Xử lý thay đổi địa chỉ IP trong quá trình auto-scaling hoặc các tình huống lỗi
2. **Load Balancing tự động**: Phân phối traffic giữa nhiều instance mà không cần cấu hình thủ công
3. **Tính khả dụng cao**: Tự động loại bỏ các instance không khỏe mạnh khỏi rotation
4. **Giao tiếp đơn giản**: Microservices không cần biết vị trí chính xác của các dịch vụ khác

## Chiến Lược Triển Khai

Để triển khai mẫu này:

1. Tạo một máy chủ trung tâm riêng biệt dành cho service discovery và registration
2. Cấu hình microservices tự đăng ký khi khởi động
3. Triển khai cơ chế heartbeat để giám sát sức khỏe
4. Cho phép microservices truy vấn registry để tìm vị trí dịch vụ
5. Cấu hình các chiến lược load balancing phía client

## Tóm Tắt

Mẫu Service Discovery và Registration rất quan trọng đối với kiến trúc microservices vì nó:

- Giải quyết vấn đề về cách các microservices giao tiếp với nhau
- Loại bỏ nhu cầu hardcode địa chỉ IP và cổng
- Cung cấp khả năng load balancing tự động
- Thích ứng với các tình huống scaling động và lỗi
- Duy trì cái nhìn tập trung về tất cả các instance dịch vụ đang chạy

Mẫu này là nền tảng để xây dựng các ứng dụng cloud-native có khả năng phục hồi và mở rộng, nơi các instance dịch vụ có thể được tạo, hủy và scale động mà không cần can thiệp thủ công.

## Các Bước Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu vào:
- Triển khai chi tiết client-side service discovery
- Ví dụ thực tế sử dụng Spring Boot và Spring Cloud
- Cấu hình và các phương pháp hay nhất
- Tích hợp với các mẫu microservices khác



================================================================================
FILE: 90-openid-connect-and-oauth2-explained.md
================================================================================

# Hiểu về OpenID Connect và OAuth2

## Tổng quan

Tài liệu này giải thích mối quan hệ giữa OpenID Connect (OIDC) và OAuth2 framework, làm rõ những hiểu lầm phổ biến và trình bày cách hai công nghệ này hoạt động cùng nhau để cung cấp giải pháp quản lý định danh và truy cập toàn diện trong kiến trúc microservices.

## Những hiểu lầm phổ biến

Nhiều developers thường hiểu sai rằng:
- OpenID Connect là sự thay thế cho OAuth2
- OpenID Connect tốt hơn OAuth2
- Bạn nên dùng OIDC thay vì OAuth2

**Sự thật là**: OpenID Connect được xây dựng **trên nền tảng** OAuth2, không phải để thay thế. Bạn không thể có OpenID Connect mà không có OAuth2.

## OAuth2 Framework

### Mục đích
OAuth2 được xây dựng chủ yếu để hỗ trợ **ủy quyền (authorization)**, không phải xác thực (authentication).

### Các khái niệm chính

**Authentication vs Authorization:**
- **Authentication (Xác thực)**: Xác nhận người dùng hợp lệ bằng cách kiểm tra thông tin đăng nhập
- **Authorization (Ủy quyền)**: Thực thi các quyền và kiểm soát truy cập dựa trên vai trò sau khi xác thực

OAuth2 cho phép ứng dụng:
- Cung cấp quyền truy cập tạm thời cho ứng dụng bên thứ ba
- Cấp quyền truy cập hạn chế vào tài nguyên được bảo vệ
- Kiểm soát quyền truy cập thông qua scopes

### OAuth2 trong thực tế: Ví dụ Stack Overflow

Xem xét kịch bản xác thực Stack Overflow sử dụng GitHub:

1. Người dùng không có tài khoản Stack Overflow
2. Stack Overflow xác thực người dùng thông qua thông tin đăng nhập GitHub
3. GitHub cấp access token với giả định Stack Overflow chỉ cần thông tin email
4. Đằng sau hậu trường, Stack Overflow sử dụng access token này cho xác thực
5. Stack Overflow tạo tài khoản sử dụng địa chỉ email từ GitHub

Kịch bản này tiết lộ một "lỗ hổng" - các tổ chức tìm cách sử dụng OAuth2 cho cả xác thực và ủy quyền, mặc dù nó chỉ được thiết kế cho ủy quyền.

## Sự cần thiết của OpenID Connect

### Tại sao OIDC được tạo ra?

Vì các tổ chức đang sử dụng OAuth2 cho cả xác thực và ủy quyền mà không có phương pháp chuẩn, nhiều vấn đề nổi lên:

- Access tokens không cung cấp thông tin cụ thể về người dùng cuối
- Không có cách chuẩn để chia sẻ thông tin người dùng
- Các tổ chức sử dụng các phương pháp khác nhau (nhúng email, số điện thoại trong access tokens, v.v.)
- Thiếu tiêu chuẩn toàn ngành để chia sẻ thông tin định danh

### OpenID Connect là gì?

OpenID Connect là một **giao thức được xây dựng trên OAuth2** có các đặc điểm:

- Cung cấp khả năng xác thực
- Giới thiệu **ID Token** mới chứa thông tin người dùng
- Thiết lập tiêu chuẩn ngành để chia sẻ chi tiết định danh

## Kiến trúc công nghệ

```
┌─────────────────────────────────┐
│   OpenID Connect (OIDC)         │  ← Xác thực
│   (Lớp định danh)               │
├─────────────────────────────────┤
│   OAuth2 Framework              │  ← Ủy quyền
│   (Lớp ủy quyền)                │
├─────────────────────────────────┤
│   HTTP Protocol                 │  ← Giao thức cơ sở
└─────────────────────────────────┘
```

## So sánh OAuth2 và OpenID Connect

| Khía cạnh | OAuth2 | OpenID Connect |
|-----------|--------|----------------|
| **Mục đích chính** | Ủy quyền | Xác thực |
| **Loại Token** | Access Token | Access Token + ID Token |
| **Tập trung vào** | Quản lý truy cập | Quản lý định danh |
| **Ví dụ Scope** | read, write, admin | openid, profile, email, address |

### Khái niệm biểu đồ Venn

```
┌──────────────┐         ┌──────────────┐
│   OpenID     │         │   OAuth2     │
│   Connect    │         │              │
│              │         │              │
│   Xác thực   │◄──────►│  Ủy quyền    │
│              │   IAM   │              │
│  Quản lý     │         │  Quản lý     │
│  Định danh   │         │  Truy cập    │
└──────────────┘         └──────────────┘
```

Khi kết hợp, chúng tạo ra **IAM (Identity and Access Management - Quản lý Định danh và Truy cập)**.

## Cách OpenID Connect hoạt động

### OpenID Scope

Để kích hoạt OpenID Connect:
1. Gửi tham số scope với giá trị `openid`
2. Authorization server phát hiện scope này
3. Server cấp **hai tokens**:
   - **Access Token**: Để truy cập tài nguyên được bảo vệ
   - **ID Token**: Chứa thông tin định danh người dùng

Không có scope `openid`, bạn chỉ nhận được access token (luồng OAuth2 chuẩn).

## Ba lợi ích chính của OIDC

### 1. Scopes chuẩn hóa

Cách chuẩn để yêu cầu thông tin người dùng thông qua scopes:

- **`openid`**: Xác thực cơ bản
- **`profile`**: Thông tin hồ sơ người dùng
- **`email`**: Chi tiết địa chỉ email
- **`address`**: Thông tin địa chỉ

### 2. Tokens theo chuẩn JWT

Cả Access Token và ID Token đều tuân theo chuẩn **JWT (JSON Web Token)**, đảm bảo:
- Định dạng token nhất quán
- Thông tin người dùng tự chứa
- Xác minh chữ ký mật mã
- Khả năng tương tác giữa các hệ thống

### 3. Endpoint /userinfo chuẩn hóa

OpenID Connect cung cấp endpoint chuẩn: `/userinfo`

Ứng dụng client có thể gọi endpoint này bất cứ lúc nào để lấy:
- Chi tiết về người dùng đã đăng nhập
- Thông tin resource owner
- Dữ liệu hồ sơ

## Triển khai trong Microservices

Khi triển khai OAuth2 và OpenID Connect trong microservices:

1. **Cấu hình Authorization Server**: Thiết lập để hỗ trợ cả OAuth2 và OIDC
2. **Yêu cầu Tokens**: Bao gồm scope `openid` trong các yêu cầu ủy quyền
3. **Nhận Tokens**: Nhận cả access token và ID token
4. **Sử dụng ID Token**: Trích xuất thông tin định danh người dùng
5. **Sử dụng Access Token**: Truy cập tài nguyên microservice được bảo vệ
6. **Gọi /userinfo**: Lấy thông tin người dùng bổ sung khi cần

## Best Practices (Thực hành tốt nhất)

1. **Sử dụng cả hai cùng nhau**: Kết hợp OAuth2 và OIDC cho khả năng IAM hoàn chỉnh
2. **Yêu cầu Scopes phù hợp**: Chỉ yêu cầu các scopes bạn cần
3. **Xác thực Tokens**: Luôn xác thực chữ ký JWT
4. **Lưu trữ Token an toàn**: Lưu trữ tokens một cách an toàn ở phía client
5. **Token hết hạn**: Xử lý làm mới token một cách phù hợp

## Những điểm chính cần nhớ

✅ **NÊN:**
- Hiểu rằng OIDC được xây dựng trên OAuth2
- Sử dụng OIDC + OAuth2 cùng nhau cho quản lý định danh và truy cập
- Sử dụng scopes chuẩn hóa để yêu cầu thông tin người dùng

❌ **KHÔNG NÊN:**
- Nói OIDC là sự thay thế cho OAuth2
- Tuyên bố OIDC tốt hơn OAuth2
- Sử dụng OIDC mà không hiểu OAuth2

## Kết luận

OpenID Connect và OAuth2 là các công nghệ bổ sung cho nhau:

- **OAuth2** cung cấp nền tảng cho ủy quyền và kiểm soát truy cập
- **OpenID Connect** thêm xác thực và quản lý định danh lên trên
- Cùng nhau, chúng cung cấp khả năng **IAM (Identity and Access Management)** toàn diện

Bằng cách kết hợp các tiêu chuẩn này, ứng dụng client có thể:
- Xác thực người dùng một cách an toàn
- Kiểm soát quyền truy cập vào tài nguyên
- Quản lý thông tin định danh người dùng
- Tuân theo các giao thức tiêu chuẩn ngành

Hiểu cả hai công nghệ và mối quan hệ của chúng là rất quan trọng để xây dựng kiến trúc microservices hiện đại, an toàn với Spring Boot và các frameworks khác.

---

**Các chủ đề liên quan:**
- JWT (JSON Web Tokens)
- Spring Security OAuth2
- Bảo mật Microservices
- Xác thực API Gateway
- Xác thực Service-to-Service



================================================================================
FILE: 91-authorization-server-products-and-keycloak-overview.md
================================================================================

# Tổng Quan về Các Sản Phẩm Authorization Server và Keycloak

## Giới Thiệu

OAuth2 và OpenID Connect là các đặc tả (specifications) định nghĩa các tiêu chuẩn để triển khai bảo mật trong các ứng dụng web. Tuy nhiên, chỉ riêng các đặc tả này thì chưa đủ - chúng ta cần các triển khai thực tế để bảo mật ứng dụng của mình.

## Tại Sao Cần Các Sản Phẩm Authorization Server?

Vì bảo mật là yêu cầu chung của nhiều tổ chức, nhiều công ty đã xây dựng các sản phẩm dựa trên đặc tả OAuth2 và OpenID Connect. Trong khi các tổ chức lớn như Google, GitHub, Facebook và Twitter có thể tự xây dựng authorization server từ đầu, các tổ chức nhỏ hơn hoặc những tổ chức không muốn xây dựng từ đầu cần các giải pháp thay thế.

## Keycloak - Quản Lý Danh Tính và Truy Cập Mã Nguồn Mở

### Tổng Quan

**Keycloak** là một sản phẩm quản lý danh tính và truy cập mã nguồn mở được tài trợ bởi Red Hat. Nó cung cấp cách dễ dàng để thiết lập authorization server cho bất kỳ tổ chức nào.

### Tính Năng Chính

- **Hỗ Trợ Giao Thức Chuẩn**: OpenID Connect, OAuth2, SAML
- **Đăng Nhập Mạng Xã Hội**: Tích hợp với các nhà cung cấp danh tính xã hội
- **Single Sign-On (SSO)**: Xác thực thống nhất trên các ứng dụng
- **Mã Nguồn Mở**: Miễn phí sử dụng và chỉnh sửa
- **Sẵn Sàng Cho Doanh Nghiệp**: Được hỗ trợ bởi Red Hat

### Tại Sao Chọn Keycloak Cho Khóa Học Này?

Keycloak được chọn cho khóa học này vì:
1. Hoàn toàn mã nguồn mở
2. Không yêu cầu giấy phép thương mại để thực hành
3. Dựa trên các tiêu chuẩn OAuth2 và OpenID Connect
4. Sẵn sàng cho môi trường production và được áp dụng rộng rãi

## Các Sản Phẩm Authorization Server Khác

### Giải Pháp Thương Mại

1. **Okta**
   - Rất phổ biến cho các ứng dụng doanh nghiệp
   - Quản lý danh tính và truy cập có khả năng mở rộng
   - Định giá cao cấp

2. **Amazon Cognito**
   - Giải pháp tích hợp AWS
   - Quản lý danh tính và truy cập mở rộng theo mọi mức lưu lượng
   - Mô hình thanh toán theo mức sử dụng

3. **FusionAuth**
   - Nền tảng xác thực hướng đến nhà phát triển
   - Tùy chọn triển khai linh hoạt

4. **ForgeRock**
   - Nền tảng danh tính doanh nghiệp
   - Giải pháp IAM toàn diện

### Spring Authorization Server

Đội ngũ Spring đã phát triển **Spring Authorization Server** - một dự án mới cho phép các tổ chức xây dựng authorization server riêng của họ.

**Lưu Ý Quan Trọng:**
- Đây là dự án tương đối mới trong hệ sinh thái Spring
- Vẫn đang trưởng thành so với các sản phẩm đã được thiết lập như Keycloak, Okta và Cognito
- Lựa chọn tốt nếu bạn muốn xây dựng authorization server tùy chỉnh
- Yêu cầu nhiều nỗ lực phát triển hơn so với các giải pháp có sẵn

## Kết Luận

Đối với khóa học microservices này, **Keycloak** là lựa chọn ưu tiên do:
- Bản chất mã nguồn mở
- Độ trưởng thành và ổn định
- Hỗ trợ cộng đồng mạnh mẽ
- Không có chi phí giấy phép để học tập và thực hành

Các tổ chức muốn triển khai authorization server nên đánh giá nhu cầu cụ thể, nguồn lực của họ và xem xét sử dụng sản phẩm có sẵn hay tự xây dựng bằng các framework như Spring Authorization Server.

---

**Bước Tiếp Theo**: Trong các bài giảng tiếp theo, chúng ta sẽ triển khai Keycloak làm authorization server trong mạng lưới microservice của chúng ta.


