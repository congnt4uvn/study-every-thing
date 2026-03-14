# AWS Lambda: Đối Tượng Event và Context

## Tổng Quan

Hiểu rõ về **event** và **context** là rất quan trọng khi làm việc với AWS Lambda. Hai đối tượng này cung cấp tất cả thông tin cần thiết để Lambda function của bạn thực thi đúng cách.

## Đối Tượng Event (Event Object)

### Event Object là gì?

Event object là một tài liệu định dạng JSON chứa dữ liệu để hàm xử lý. Nó được tạo và truyền bởi dịch vụ gọi hàm (như EventBridge, SQS, SNS, v.v.) đến Lambda function của bạn.

### Đặc Điểm Chính

- **Định dạng**: Tài liệu định dạng JSON
- **Nguồn**: Được tạo bởi dịch vụ AWS gọi hàm
- **Mục đích**: Chứa tất cả dữ liệu và thông tin cần thiết để Lambda function xử lý sự kiện
- **Chuyển đổi Runtime**: Được chuyển đổi sang cấu trúc dữ liệu phù hợp dựa trên runtime
  - Với Python: Chuyển đổi thành dictionary
  - Với ngôn ngữ khác: Chuyển đổi sang cấu trúc dữ liệu tương đương

### Nội Dung Event Object

Event object bao gồm:
- Chi tiết về chính sự kiện đó
- Dịch vụ nguồn phát ra sự kiện
- Region nơi sự kiện được phát sinh
- Dữ liệu cụ thể của dịch vụ liên quan đến sự kiện
- Bất kỳ tham số hay đối số nào từ dịch vụ gọi hàm

### Ví Dụ Trường Hợp Sử Dụng

Khi EventBridge gọi Lambda function của bạn:
1. EventBridge tạo một event
2. Event được truyền đến Lambda function
3. Function nhận nó dưới dạng event object
4. Function xử lý dữ liệu chứa trong event

## Đối Tượng Context (Context Object)

### Context Object là gì?

Context object cung cấp metadata và các phương thức về chính invocation của Lambda function và môi trường runtime. Nó được truyền đến Lambda function tại thời điểm runtime.

### Đặc Điểm Chính

- **Định dạng**: Object với các phương thức và thuộc tính
- **Nguồn**: Tự động được cung cấp bởi AWS Lambda runtime
- **Mục đích**: Cung cấp metadata về môi trường thực thi function
- **Thời điểm**: Được truyền tại runtime

### Nội Dung Context Object

Context object bao gồm:
- AWS request ID
- Tên function
- Log group liên kết
- Giới hạn bộ nhớ (tính bằng megabytes)
- Thông tin môi trường runtime
- Metadata khác về invocation

## Sử Dụng Event và Context Trong Code

### Ví Dụ Python

```python
def handler(event, context):
    # Truy cập dữ liệu event
    event_source = event.get('source')
    event_region = event.get('region')
    
    # Truy cập thông tin context
    request_id = context.aws_request_id
    function_name = context.function_name
    memory_limit = context.memory_limit_in_mb
    
    # Xử lý logic của bạn ở đây
    print(f"Nguồn event: {event_source}")
    print(f"Request ID: {request_id}")
    
    return {
        'statusCode': 200,
        'body': 'Thành công'
    }
```

## Sự Khác Biệt Chính

| Khía Cạnh | Event Object | Context Object |
|-----------|--------------|----------------|
| **Mục đích** | Chứa dữ liệu event để xử lý | Chứa metadata về invocation |
| **Nguồn** | Dịch vụ gọi hàm (EventBridge, SQS, v.v.) | AWS Lambda runtime |
| **Nội dung** | Dữ liệu nghiệp vụ/sự kiện | Metadata về thực thi function |
| **Định dạng** | JSON (chuyển đổi sang object runtime) | Runtime object với các phương thức |

## Tổng Kết

- **Event Object**: Cái gì cần xử lý (dữ liệu)
- **Context Object**: Thông tin về môi trường xử lý (metadata)
- Cả hai đối tượng đều bổ sung lẫn nhau và rất quan trọng cho việc thực thi Lambda function
- Luôn có sẵn trong Lambda handler function của bạn
