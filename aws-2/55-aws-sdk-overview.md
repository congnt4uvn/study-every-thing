# Tổng Quan Về AWS SDK

## Giới Thiệu

AWS Software Development Kit (SDK) là một công cụ mạnh mẽ cho phép các nhà phát triển tương tác với các dịch vụ AWS trực tiếp từ mã ứng dụng của họ, mà không cần dựa vào AWS Command Line Interface (CLI).

## AWS SDK Là Gì?

SDK (Software Development Kit - Bộ công cụ phát triển phần mềm) cho phép bạn thực hiện các hành động trên AWS trực tiếp từ mã ứng dụng của bạn. Thay vì sử dụng các lệnh CLI, bạn có thể tương tác với các dịch vụ AWS theo cách lập trình thông qua ngôn ngữ lập trình ưa thích của mình.

## Các Ngôn Ngữ Được Hỗ Trợ

AWS cung cấp các SDK chính thức cho nhiều ngôn ngữ lập trình, bao gồm:

- **Java**
- **.NET**
- **Node.js**
- **PHP**
- **Python** (Boto3)
- **Go**
- **Ruby**
- **C++**

Danh sách các ngôn ngữ được hỗ trợ tiếp tục phát triển theo thời gian khi AWS mở rộng các SDK của mình.

## Mối Liên Hệ Giữa Python SDK và CLI

Một điều thú vị về AWS CLI là nó được xây dựng bằng Python và tận dụng SDK **Boto3**. Khi bạn sử dụng AWS CLI, thực tế bạn đang sử dụng Python SDK ở bên dưới.

## Khi Nào Sử Dụng SDK

SDK được sử dụng khi bạn cần:

- Thực hiện các lệnh gọi API đến các dịch vụ AWS từ mã ứng dụng của bạn
- Tương tác với các dịch vụ như Amazon DynamoDB hoặc Amazon S3 theo cách lập trình
- Xây dựng các ứng dụng cần tự động hóa các hoạt động AWS
- Tích hợp chức năng AWS trực tiếp vào phần mềm của bạn

## Ứng Dụng Thực Tế

Bạn sẽ gặp SDK trong thực tế khi làm việc với AWS Lambda functions, nơi bạn có thể thấy cách SDK hoạt động trong các triển khai mã thực tế. Trải nghiệm thực hành này sẽ minh họa cách sử dụng AWS SDK trong thế giới thực.

## Những Điểm Cần Nhớ

- SDK cho phép tương tác trực tiếp với AWS từ mã ứng dụng
- Có nhiều tùy chọn ngôn ngữ để phù hợp với các môi trường phát triển khác nhau
- AWS CLI được xây dựng trên Python SDK (Boto3)
- Hiểu khi nào sử dụng SDK là quan trọng cho các kỳ thi chứng chỉ AWS
- Kinh nghiệm thực tế với Lambda functions sẽ cung cấp cách sử dụng SDK thực hành

---

*Tổng quan này cung cấp sự hiểu biết cơ bản về AWS SDK và vai trò của chúng trong phát triển ứng dụng đám mây.*