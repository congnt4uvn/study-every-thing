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