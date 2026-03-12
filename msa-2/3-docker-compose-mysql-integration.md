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