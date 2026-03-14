# Ghi chú học AWS — Quy tắc lấy mẫu (Sampling Rules) cho X-Ray trong CloudWatch

## Vị trí cấu hình
- AWS Console → **CloudWatch**
- Thanh bên trái → **Settings**
- Trong **CloudWatch settings** → **Traces**
- Mở **Sampling rules** (thường cũng có encryption rules và group rules)

## Sampling rules dùng để làm gì (X-Ray)
Sampling rules quyết định bao nhiêu request được ghi lại thành **AWS X-Ray traces**, giúp cân bằng:
- Quan sát hệ thống tốt hơn (nhiều trace hơn)
- Chi phí / lưu trữ / nhiễu (ít trace hơn)

## Quy tắc mặc định (Default rule)
- Có **default rule** với priority **10.000**.
- Rule này match **tất cả** request.
- Bạn **không thể sửa phần điều kiện match** (matching criteria) của default rule.
- Bạn *có thể* chỉnh **giới hạn** (limits), ví dụ:
  - **Reservoir size** (số request tối đa được sample mỗi giây)
  - **Fixed rate** (tỷ lệ % sample thêm)

## Tạo quy tắc lấy mẫu tùy chỉnh
Trong **Create sampling rule**, bạn có thể cấu hình:

### 1) Tên rule
Ví dụ: `DemoSampling`

### 2) Priority
- Khoảng: **1–9.999**
- **Số càng nhỏ → ưu tiên càng cao**
- Ví dụ: priority **5.000** sẽ ưu tiên hơn default (**10.000**) nếu cùng match

### 3) Giới hạn lấy mẫu
- **Reservoir size**: số request tối đa được sample **mỗi giây**
  - Ví dụ: reservoir size **1**
- **Fixed rate**: tỷ lệ % (ví dụ **100%**)

### 4) Điều kiện match (nhắm mục tiêu)
Để chỉ lấy mẫu một phần traffic cụ thể, có thể điền:
- **Service name** (ví dụ trong bài: `MYSERVICE`)
- **HTTP method** (ví dụ: `POST`)
- **URL path**

Nhờ đó bạn có thể, ví dụ, lấy trace cho mọi request `POST` vào một path nhất định của một service.

## Hành vi vận hành (điểm quan trọng)
- Sau khi tạo rule, bạn **không cần restart X-Ray daemon**.
- Rule sẽ được áp dụng tự động và bạn sẽ thấy hiệu lực trong **X-Ray console**.

## Câu hỏi tự kiểm tra
1. Vào đâu trong CloudWatch để cấu hình X-Ray sampling rules?
2. Default rule chỉnh được gì và không chỉnh được gì?
3. Nếu hai rule đều match, priority 5.000 hay 10.000 sẽ thắng?
4. Reservoir size khác fixed rate như thế nào?
5. Kể tên 3 tiêu chí match để nhắm đúng traffic.
