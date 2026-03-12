# Tạo Dự Án BOM Cho Microservices: Hướng Dẫn Từng Bước

## Tổng Quan

Hướng dẫn này trình bày cách tạo dự án Bill of Materials (BOM) từ đầu để quản lý tập trung các dependencies trong các microservices Spring Boot. Dự án BOM hoạt động như một parent cho tất cả microservices, cung cấp quản lý phiên bản dependencies nhất quán.

## Bước 1: Tạo Dự Án Maven Spring Boot Mới

### Tạo Module

1. Nhấp chuột phải vào thư mục `section_20`
2. Chọn **New Module**
3. Trong cửa sổ tạo module, chọn tùy chọn **Spring Boot**
4. Cấu hình dự án với các thông tin sau:
   - **Tên**: `eazy-bom` (BOM là viết tắt của Bill of Materials)
   - **Ngôn ngữ**: Java
   - **Loại**: Maven
   - **Group**: `com.eazybyte`
   - **Artifact**: `eazy-bom`
   - **Tên Package**: `com.eazybyte.eazybom`
   - **Phiên bản JDK**: 21
   - **Phiên bản Java**: 21
   - **Packaging**: Jar (sẽ được thay đổi thành POM sau)

5. Nhấp nút **Next**
6. **Quan trọng**: Không thêm bất kỳ Spring Boot starter dependencies nào
7. Nhấp nút **Create**

Điều này tạo ra một dự án Maven Spring Boot mới có tên `eazy-bom`.

## Bước 2: Dọn Dẹp Cấu Trúc Dự Án

### Xóa Thư Mục Source

Vì dự án BOM chỉ nên chứa thông tin quản lý dependencies và không có mã nguồn thực tế:

1. Mở dự án `eazy-bom` vừa tạo
2. Xóa toàn bộ thư mục `src`

> **Thực Hành Tốt Nhất**: Đây là thực hành tốt để chỉ duy trì thông tin liên quan đến dependencies trong dự án BOM, không có bất kỳ mã nguồn nào. Điều này giữ cho BOM sạch sẽ và chỉ tập trung vào quản lý dependencies.

## Bước 3: Chỉnh Sửa File pom.xml

Mở file `pom.xml`. Bạn sẽ thấy một file `pom.xml` thông thường của microservice Spring Boot. Chúng ta cần thực hiện các thay đổi đáng kể để biến nó thành file BOM.

### 3.1 Xóa Thông Tin Parent

Xóa toàn bộ phần `<parent>` tham chiếu đến Spring Boot starter parent:

```xml
<!-- XÓA PHẦN NÀY -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>x.x.x</version>
    <relativePath/>
</parent>
```

### 3.2 Thêm Mô Tả

Thêm tag description sau thông tin dự án cơ bản:

```xml
<description>Common BOM cho EazyBank Microservices</description>
```

Bạn có thể viết bất cứ điều gì có ý nghĩa với bạn trong phần mô tả này.

### 3.3 Thêm Metadata Dự Án Tùy Chọn

Các tag này là tùy chọn nhưng được khuyến nghị cho một thiết lập dự án hoàn chỉnh:

```xml
<url>https://www.eazybytes.com</url>

<licenses>
    <license>
        <name>Apache License, Version 2.0</name>
        <url>https://www.apache.org/licenses/LICENSE-2.0</url>
    </license>
</licenses>

<developers>
    <developer>
        <id>eazybytes</id>
        <name>EazyBytes Team</name>
        <email>info@eazybytes.com</email>
    </developer>
</developers>

<scm>
    <connection>scm:git:git://github.com/eazybytes/eazybank.git</connection>
    <developerConnection>scm:git:ssh://github.com/eazybytes/eazybank.git</developerConnection>
    <url>https://github.com/eazybytes/eazybank</url>
</scm>
```

> **Lưu ý**: Các tag này (URL, licenses, developers, SCM) là tùy chọn và không liên quan cụ thể đến chức năng BOM. Bạn có thể xóa chúng nếu muốn, nhưng chúng là thực hành tốt cho tài liệu dự án.

### 3.4 Đặt Loại Packaging Thành POM (Quan Trọng!)

Ngay sau tag `<description>`, thêm tag packaging:

```xml
<packaging>pom</packaging>
```

> **Cực Kỳ Quan Trọng**: Nếu không đề cập `pom` làm loại packaging, bạn không thể sử dụng tính năng BOM (Bill of Materials). Đây là điều phân biệt dự án BOM với dự án thông thường.

**Dự án BOM là gì?**
- BOM = **Project Object Model**
- Đây là loại dự án Maven đặc biệt được thiết kế cho quản lý dependencies

## Bước 4: Định Nghĩa Properties

Trong phần `<properties>`, định nghĩa tất cả các properties cần thiết cho microservices của bạn.

Thay thế các properties hiện có bằng:

```xml
<properties>
    <!-- Phiên bản Java -->
    <java.version>21</java.version>
    
    <!-- Phiên bản Spring Framework -->
    <spring-boot.version>3.2.0</spring-boot.version>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
    
    <!-- Phiên bản Thư Viện Bên Thứ Ba -->
    <lombok.version>1.18.30</lombok.version>
    <h2.version>2.2.224</h2.version>
    <springdoc.version>2.3.0</springdoc.version>
    
    <!-- Observability -->
    <opentelemetry.version>1.32.0</opentelemetry.version>
    <micrometer.version>1.12.0</micrometer.version>
    
    <!-- Build Tools -->
    <jib.version>3.4.0</jib.version>
    <image.tag>latest</image.tag>
</properties>
```

### Hiểu Về Properties

Tất cả properties đều dễ hiểu và sẽ được microservices sử dụng. Các điểm chính:

#### Thư Viện Bên Thứ Ba
Đối với bất kỳ thư viện bên thứ ba nào được sử dụng bên ngoài hệ sinh thái Spring Boot, bạn **phải** chỉ định phiên bản chính xác:
- SpringDoc (tài liệu OpenAPI/Swagger)
- H2 Database
- Lombok
- OpenTelemetry
- Micrometer

#### Tại Sao Phải Chỉ Định Phiên Bản Thư Viện Bên Thứ Ba?

Mặc dù microservices có thể hoạt động mà không cần phiên bản rõ ràng (các dependencies Spring Boot có thể tự động áp dụng phiên bản mới nhất), **bạn không bao giờ nên dựa vào điều này**. Luôn duy trì kiểm soát bằng cách chỉ định phiên bản chính xác vì:
- Ngăn chặn các thay đổi breaking không mong muốn
- Đảm bảo tính nhất quán trên tất cả microservices
- Làm cho việc nâng cấp phiên bản có chủ đích và được kiểm soát
- Đơn giản hóa việc khắc phục sự cố

#### Properties Khác
- **jib.version**: Phiên bản của Google Jib Maven plugin để tạo Docker image
- **image.tag**: Tên tag của Docker image (ví dụ: "latest")

## Bước 5: Cấu Hình Dependency Management

### 5.1 Xóa Dependencies Mặc Định

Xóa toàn bộ phần `<dependencies>` chứa các dependencies Spring Boot mặc định:

```xml
<!-- XÓA TOÀN BỘ PHẦN NÀY -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
</dependencies>
```

Giữ tag `<dependencies>` trống hoặc xóa nó hoàn toàn.

### 5.2 Tạo Phần Dependency Management

Thêm phần `<dependencyManagement>` mới với tất cả dependencies cần thiết:

```xml
<dependencyManagement>
    <dependencies>
        
        <!-- Spring Boot Dependencies BOM -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- H2 Database -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <version>${h2.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- SpringDoc OpenAPI -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi</artifactId>
            <version>${springdoc.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Spring Boot Starter Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>${spring-boot.version}</version>
        </dependency>

        <!-- Spring Cloud Dependencies -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

    </dependencies>
</dependencyManagement>
```

### Hiểu Từng Dependency

#### 1. Spring Boot Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-dependencies</artifactId>
    <version>${spring-boot.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Spring Boot framework có file BOM riêng của nó
- Chúng ta import nó để làm cho tất cả dependencies Spring Boot có sẵn cho các microservices con
- Sử dụng property `${spring-boot.version}` đã định nghĩa trước đó
- **type**: Phải là `pom` cho BOM imports
- **scope**: Phải là `import` cho BOM imports

#### 2. Lombok
```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>${lombok.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Lombok là thư viện bên thứ ba ngoài hệ sinh thái Spring Boot
- Phải được thêm riêng với phiên bản rõ ràng
- Theo cùng cấu trúc: groupId, artifactId, version từ properties
- type: `pom`, scope: `import`

#### 3. H2 Database
```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <version>${h2.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- H2 cũng là một dependency bên thứ ba
- Yêu cầu chỉ định phiên bản rõ ràng
- Cùng mẫu BOM import

#### 4. SpringDoc OpenAPI
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi</artifactId>
    <version>${springdoc.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Được sử dụng để tài liệu hóa microservices với đặc tả OpenAPI và Swagger
- Thư viện bên thứ ba yêu cầu phiên bản rõ ràng

#### 5. Spring Boot Starter Test (Trường Hợp Đặc Biệt)
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <version>${spring-boot.version}</version>
</dependency>
```

**Lưu ý sự khác biệt**: Dependency này KHÔNG có `<type>pom</type>` và `<scope>import</scope>`!

**Tại sao?**
- Spring Boot Starter Test không hỗ trợ import kiểu POM
- Đây là thư viện nhỏ với sub-dependencies tối thiểu
- Chỉ hỗ trợ chức năng unit testing
- Được thêm như một dependency thông thường chỉ với groupId, artifactId và version

#### 6. Spring Cloud Dependencies
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-dependencies</artifactId>
    <version>${spring-cloud.version}</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

- Spring Cloud chứa nhiều sub-projects khác nhau (Eureka, Config Server, Gateway, v.v.)
- Chúng ta muốn sử dụng chúng trong microservices của mình
- Import toàn bộ file BOM Spring Cloud
- type: `pom`, scope: `import`

### Tham Chiếu Properties

Lưu ý cú pháp để tham chiếu các properties đã định nghĩa trước đó:

```xml
<version>${tên-property}</version>
```

Ví dụ:
- `${spring-boot.version}` tham chiếu property phiên bản Spring Boot
- `${lombok.version}` tham chiếu property phiên bản Lombok

## Bước 6: Cấu Hình Build (Không Cần Thay Đổi)

Phần `<build>` không yêu cầu bất kỳ thay đổi nào cho dự án BOM. Bạn có thể để nó như vậy hoặc xóa các build plugins không cần thiết cho dự án BOM.

## Tóm Tắt Các Thay Đổi

Để tạo dự án BOM, bạn cần:

1. ✅ Tạo dự án Maven Spring Boot
2. ✅ Xóa thư mục `src` (không có mã nguồn trong BOM)
3. ✅ Xóa phần `<parent>` khỏi `pom.xml`
4. ✅ Thêm description và metadata tùy chọn
5. ✅ **Đặt `<packaging>pom</packaging>` (Quan trọng!)**
6. ✅ Định nghĩa tất cả properties cần thiết với phiên bản
7. ✅ Xóa phần `<dependencies>` mặc định
8. ✅ Tạo phần `<dependencyManagement>` với tất cả dependencies
9. ✅ Sử dụng `<type>pom</type>` và `<scope>import</scope>` cho BOM imports
10. ✅ Giữ phần `<build>` không thay đổi

## Những Điểm Chính

### Các Yếu Tố Bắt Buộc Cho BOM
- **packaging**: Phải là `pom`
- **dependencyManagement**: Chứa tất cả dependencies được quản lý
- **properties**: Định nghĩa tất cả phiên bản tập trung

### Mẫu Import Dependency
Đối với hầu hết dependencies hỗ trợ BOM:
```xml
<type>pom</type>
<scope>import</scope>
```

Đối với dependencies không hỗ trợ BOM (như starter-test):
- Chỉ chỉ định groupId, artifactId và version

### Triết Lý Kiểm Soát Phiên Bản
- Luôn chỉ định phiên bản cho thư viện bên thứ ba
- Không bao giờ dựa vào resolution phiên bản tự động
- Duy trì kiểm soát rõ ràng đối với tất cả dependencies
- Tham chiếu phiên bản từ properties sử dụng `${tên-property}`

## Bước Tiếp Theo?

Trong bài giảng tiếp theo, chúng ta sẽ:
- Áp dụng dự án `eazy-bom` này vào các microservices riêng lẻ
- Thấy được sự kỳ diệu của quản lý dependencies tập trung
- Học cách các microservices con kế thừa phiên bản tự động
- Hiểu cách cập nhật phiên bản ở một nơi cho tất cả services

## Lợi Ích Bạn Sẽ Trải Nghiệm

Sau khi áp dụng BOM này trong microservices của bạn:
- ✅ Không còn phiên bản hard-coded trong các microservices riêng lẻ
- ✅ Cập nhật phiên bản ở một nơi
- ✅ Phiên bản dependencies nhất quán trên tất cả services
- ✅ Bảo trì và nâng cấp dễ dàng hơn
- ✅ Kiểm soát tốt hơn các phiên bản thư viện bên thứ ba
- ✅ Giảm cấu hình trùng lặp

Cảm ơn bạn!