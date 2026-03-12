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