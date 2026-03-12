# Bài 06 — Schema & serialization: JSON vs Avro/Protobuf, compatibility

## Mục tiêu
- Hiểu vì sao schema quan trọng với event stream sống lâu
- So sánh JSON vs Avro vs Protobuf ở mức tổng quan
- Học tư duy schema evolution và compatibility

## Vì sao schema quan trọng
Kafka topic thường tồn tại nhiều năm và có nhiều team cùng consume.

Nếu không có kỷ luật schema:
- Thay đổi “gãy” làm consumer crash
- Trường dữ liệu mơ hồ, payload không nhất quán
- Refactor chậm và rủi ro

Một chiến lược schema tốt giúp:
- Quy tắc tương thích (backward/forward)
- Validation ở biên (edge)
- Ownership và versioning rõ ràng

## Các lựa chọn serialization (tổng quan thực tế)
### JSON
Ưu:
- Dễ đọc
- Dễ debug

Nhược:
- Không có schema chặt mặc định
- Payload lớn
- Dễ mơ hồ kiểu dữ liệu (number, date)

### Avro
Ưu:
- Binary gọn
- Pattern tiến hoá schema tốt
- Hệ sinh thái tốt với Schema Registry

Nhược:
- Cần tooling
- Debug khó hơn nếu thiếu tooling

### Protobuf
Ưu:
- Binary gọn
- Typing mạnh và code generation

Nhược:
- Có quy tắc evolution nhưng khác Avro
- Môi trường nhiều team vẫn cần registry/governance

## Compatibility (ý tưởng cốt lõi)
Khi producer và consumer deploy độc lập, bạn cần thay đổi schema an toàn.

Một số mode phổ biến (khái niệm):
- **Backward compatible**: consumer mới đọc được message cũ
- **Forward compatible**: consumer cũ đọc được message mới
- **Full**: cả hai chiều

Mẹo thực tế:
- Thêm field dạng optional kèm default
- Tránh đổi nghĩa field
- Tránh tái sử dụng tên field cho nghĩa khác

## Lab (tập trung quy trình, không phụ thuộc vendor)
1. Với payload `demo.orders`, viết “hợp đồng schema”:
   - Field bắt buộc
   - Field tuỳ chọn
   - Enum/giá trị cho phép

2. Đề xuất 2 thay đổi:
   - An toàn: thêm optional field `source`
   - Rủi ro: đổi tên `orderId` thành `id`

3. Chọn policy compatibility và kế hoạch để không làm consumer hỏng.

## Checklist
- Tôi giải thích được vì sao schema tránh breaking change
- Tôi so sánh JSON vs Avro vs Protobuf theo tradeoff
- Tôi phân biệt được thay đổi an toàn vs nguy hiểm

## Lỗi hay gặp
- Coi schema evolution là “cứ đổi JSON thôi”
- Làm gãy consumer do đổi tên/xoá field bắt buộc
