# AWS CloudTrail — Ghi chú học (Practitioner)

## CloudTrail là gì?
- **AWS CloudTrail** ghi lại **các lệnh gọi API** và **hoạt động của người dùng** trong tài khoản AWS.
- Có thể hiểu như **nhật ký kiểm toán (audit trail)**: giúp trả lời câu hỏi “**ai** làm **gì**, ở **đâu**, vào **lúc nào**?”.

## Xem trong console (Event history)
- Trong CloudTrail console, mục **Event history** hiển thị **management events** trong **90 ngày gần nhất**.
- Bạn có thể xem theo dòng thời gian các API call và mở từng event để xem chi tiết.

## Ví dụ theo nội dung file: terminate EC2 instance
Khi bạn terminate một EC2 instance, CloudTrail có thể ghi nhận event như **TerminateInstances**.

Một số trường thông tin thường thấy trong event (đúng như mô tả trong file):
- **Event source** (ví dụ: **EC2**)
- **Access key** đã sử dụng
- **Region** đã sử dụng
- Toàn bộ nội dung event (payload/chi tiết đầy đủ)

## Vì sao quan trọng? (các tình huống hay dùng)
- **Bảo mật / kiểm toán**: điều tra hành động bất thường.
- **Vận hành**: truy vết thay đổi (ví dụ: “ai đã xóa/terminate instance?”).
- **Tuân thủ**: chứng minh khả năng truy vết và trách nhiệm.

## Ghi nhớ cho kỳ thi Practitioner
- CloudTrail tập trung vào **theo dõi hành động (API calls)**, không phải đo CPU/RAM.
- Khi có thao tác qua Console/CLI/SDK, CloudTrail giúp bạn **tìm lại event API tương ứng**.
- **Event history** là nơi xem nhanh hoạt động gần đây (management events **90 ngày**).

## Tự kiểm tra nhanh (Hỏi & Đáp)
1. CloudTrail chủ yếu ghi lại điều gì?
   - API calls / hoạt động trong tài khoản.
2. Xem nhanh management activity gần đây ở đâu?
   - CloudTrail **Event history**.
3. Sau khi terminate EC2 instance, có thể thấy event nào?
   - API call **TerminateInstances**.

## Flashcards mini
- CloudTrail → *nhật ký kiểm toán hoạt động API*
- Event history → *90 ngày gần nhất (management events)*
- Terminate EC2 instance → *xuất hiện event TerminateInstances*
