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