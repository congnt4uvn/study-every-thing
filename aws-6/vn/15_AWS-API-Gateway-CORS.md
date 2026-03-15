# AWS API Gateway - CORS (Chia sẻ Tài nguyên Liên Nguồn)

## Tổng quan
API Gateway hỗ trợ tính năng bảo mật của trình duyệt cho việc chia sẻ tài nguyên liên nguồn (CORS). CORS phải được bật nếu bạn muốn nhận các cuộc gọi API từ một domain khác.

## Các Khái niệm Chính

### CORS là gì?
CORS (Cross-Origin Resource Sharing - Chia sẻ Tài nguyên Liên Nguồn) là một tính năng bảo mật được triển khai bởi các trình duyệt web để kiểm soát cách các trang web từ một domain có thể yêu cầu tài nguyên từ domain khác.

### Tại sao cần CORS trong API Gateway
Khi ứng dụng web của bạn được lưu trữ trên một domain (ví dụ: `www.example.com`) cần thực hiện các cuộc gọi API đến API Gateway được lưu trữ trên một domain khác (ví dụ: `api.example.com`), CORS phải được bật để cho phép các yêu cầu liên nguồn này.

## Cách CORS hoạt động với API Gateway

### Yêu cầu Pre-flight (Kiểm tra trước)
1. **Phương thức OPTIONS**: API Gateway tạo một yêu cầu pre-flight OPTIONS
2. **Kiểm tra Bảo mật**: Trình duyệt web gửi yêu cầu này trước cuộc gọi API thực tế như một biện pháp bảo mật
3. **Phản hồi**: API Gateway phản hồi với các nguồn và phương thức được cho phép

### Các Header CORS Bắt buộc
Phản hồi pre-flight OPTIONS phải chứa các header sau:
- `Access-Control-Allow-Methods` - Chỉ định các phương thức HTTP nào được cho phép
- `Access-Control-Allow-Headers` - Chỉ định các header nào có thể được sử dụng
- `Access-Control-Allow-Origins` - Chỉ định các nguồn nào được cho phép thực hiện yêu cầu

### Cấu hình
Các cài đặt CORS này có thể được cấu hình trực tiếp từ AWS Console.

## Ví dụ Thực tế

### Kịch bản
```
1. Trình duyệt Web → S3 Bucket (www.example.com)
   - Trình duyệt lấy nội dung trang web tĩnh
   
2. JavaScript (từ S3) → API Gateway (api.example.com)
   - JavaScript cần thực hiện các cuộc gọi API đến domain khác
   
3. Trình duyệt Web → API Gateway
   - Gửi yêu cầu pre-flight OPTIONS (kiểm tra bảo mật)
   
4. API Gateway → Trình duyệt Web
   - Trả về phản hồi pre-flight (nếu nguồn được cho phép)
   
5. Trình duyệt Web ↔ API Gateway
   - Nếu được chấp thuận, trình duyệt và API Gateway có thể giao tiếp
```

## Mẹo cho Kỳ thi

Đối với các kỳ thi chứng chỉ AWS, hãy nhớ:
- **CORS phải được bật** trên API Gateway cho các yêu cầu liên nguồn
- Yêu cầu pre-flight sử dụng phương thức **OPTIONS**
- CORS có thể được cấu hình từ **AWS Console**
- Tìm kiếm các kịch bản liên quan đến ứng dụng web thực hiện cuộc gọi API đến các domain khác

## Tóm tắt
- CORS là một tính năng bảo mật của trình duyệt
- Bắt buộc khi API Gateway nhận các cuộc gọi từ các domain khác
- Sử dụng yêu cầu pre-flight OPTIONS để xác minh quyền
- Cấu hình bao gồm Allow-Methods, Allow-Headers và Allow-Origins
- Thiết yếu cho các ứng dụng web hiện đại với frontend và backend được tách biệt
