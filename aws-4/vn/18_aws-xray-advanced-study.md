# AWS X-Ray — Khái niệm nâng cao (Tài liệu học)

> Nguồn: tóm tắt/biên soạn lại từ `file.txt` (instrumentation, segment/subsegment/trace, annotations vs metadata, sampling rules, daemon cross-account).

## 1) Instrumentation là gì?
**Instrumentation** (gắn đo lường vào hệ thống) trong kỹ thuật phần mềm nghĩa là thêm các “móc đo” để:
- Đo hiệu năng của sản phẩm/hệ thống
- Chẩn đoán lỗi
- Ghi và gửi thông tin trace

Trong ngữ cảnh AWS X-Ray, instrumentation thường là **sửa một chút code và dùng X-Ray SDK** (đôi khi chỉ cần cấu hình nhỏ) để ứng dụng gửi trace lên dịch vụ X-Ray.

## 2) Instrument code với X-Ray SDK (Node.js / Express)
Ý tưởng: thêm một ít mã SDK để mỗi request được bọc trong segment và được gửi lên X-Ray.

Ví dụ (Express):

```js
const express = require('express');
const AWSXRay = require('aws-xray-sdk');

const app = express();

// Mở segment cho mỗi request vào
app.use(AWSXRay.express.openSegment('MyService'));

app.get('/health', (req, res) => res.send('ok'));

// Đóng segment
app.use(AWSXRay.express.closeSegment());

app.listen(3000);
```

### Tuỳ biến trace (mức nâng cao)
Ngoài phần “tối thiểu”, bạn có thể tuỳ biến cách X-Ray hoạt động trong code bằng các cơ chế như:
- Interceptors
- Filters
- Handlers
- Middleware

Mục tiêu: thay đổi dữ liệu được capture, thêm ngữ cảnh (context), hoặc điều chỉnh cách X-Ray gửi dữ liệu.

## 3) Segment, Subsegment, Trace
- **Segment**: đơn vị chính mà ứng dụng/dịch vụ gửi lên X-Ray (thường là thứ bạn đang xem trong UI).
- **Subsegment**: chi tiết nhỏ hơn *bên trong* segment (dùng khi muốn “đào sâu” hơn).
- **Trace**: bức tranh end-to-end được tạo ra khi nhiều segment liên quan được gom lại cho cùng một request/call.

## 4) Annotations vs Metadata (rất quan trọng)
Cả hai đều là cặp key–value, nhưng khác nhau ở khả năng tìm kiếm:

- **Annotations**
  - Có index
  - Dùng để filter/tìm trace
  - Nên dùng cho các trường bạn muốn query (ví dụ `customerTier=premium`, `region=ap-southeast-1`)

- **Metadata**
  - Không có index
  - Không dùng để tìm kiếm/filter được
  - Dùng để lưu thêm thông tin tham khảo

## 5) X-Ray daemon/agent và gửi trace cross-account
X-Ray daemon/agent có thể cấu hình để **gửi trace qua nhiều AWS account**.
- Cần đảm bảo quyền IAM đúng.
- Agent có thể assume role phù hợp để tập trung tracing/logging về một “central account”.

## 6) Sampling (kiểm soát chi phí + dữ liệu)
Sampling giúp giảm số request được ghi và gửi lên X-Ray.
- Gửi càng nhiều trace ⇒ chi phí càng cao.
- Bạn có thể thay đổi sampling rules **mà không cần sửa code** (chỉ chỉnh rules).

### Sampling mặc định (theo nội dung nguồn)
- Ghi **request đầu tiên mỗi giây** (gọi là **reservoir**)
- Sau đó ghi thêm **5%** các request còn lại (gọi là **rate**)

Định nghĩa:
- **Reservoir**: đảm bảo mức tối thiểu trace (ví dụ ít nhất 1 trace/giây khi hệ thống có request).
- **Rate**: tỷ lệ % sampling cho phần request vượt quá reservoir.

### Custom sampling rules
Bạn có thể tạo rule riêng và đặt reservoir + rate cho từng loại traffic.
Ví dụ trong nội dung nguồn:
- Với request `POST`: reservoir = **10** request/giây
- Sau đó sampling **10%** phần request còn lại

## Checklist ôn tập
- Giải thích “instrumentation” bằng lời của bạn.
- Khi nào cần dùng subsegment?
- Vì sao annotations “cực kỳ quan trọng” khi cần search?
- Sampling giúp gì và ảnh hưởng chi phí ra sao?
- Reservoir và rate là gì? Giá trị mặc định là bao nhiêu?

## Câu hỏi tự kiểm tra
1. Instrumentation giúp bạn làm được những việc gì trong hệ thống production?
2. Segment khác trace như thế nào?
3. Vì sao annotations có thể dùng để filter còn metadata thì không?
4. Một sampling rule gồm những “núm chỉnh” nào?
5. Ở rule mặc định, điều gì được đảm bảo mỗi giây?
