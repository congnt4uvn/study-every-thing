# AWS Step Functions kết hợp Lambda – Tài Liệu Học Tập

## Tổng Quan

Tài liệu này hướng dẫn cách tạo **AWS Step Functions State Machine** tích hợp với **AWS Lambda**, bao gồm xây dựng luồng xử lý, cấu hình điều kiện rẽ nhánh và chạy thực thi state machine.

---

## Các Khái Niệm Quan Trọng

| Khái niệm | Mô tả |
|---|---|
| **State Machine** | Luồng công việc được định nghĩa trong Step Functions để điều phối các dịch vụ |
| **Lambda Invoke** | Trạng thái gọi một hàm AWS Lambda |
| **Choice State** | Trạng thái phân nhánh, định tuyến luồng thực thi dựa trên điều kiện |
| **Pass State** | Trạng thái chuyển tiếp đầu vào sang đầu ra mà không xử lý gì |
| **Execution Role** | IAM role được tự động tạo để state machine có quyền gọi các dịch vụ AWS |
| **ARN** | Amazon Resource Name — định danh duy nhất cho tài nguyên AWS |

---

## Hướng Dẫn Từng Bước: Xây Dựng State Machine

### 1. Tạo State Machine Mới

- Vào **AWS Step Functions** → Nhấn **Create state machine**
- Chọn định dạng **Blank** (trống)
- Dùng tab **designer** (kéo thả) hoặc tab **Code** để định nghĩa luồng

### 2. Định Nghĩa Luồng Công Việc (state-machine.json)

Luồng gồm ba trạng thái:

```
Lambda Invoke → Choice State → Is Teacher (Pass)
                             → Not Teacher (Fail)
```

**Logic luồng:**
- **Lambda Invoke** — gọi hàm `HelloFunction` với payload đầu vào
- **Choice State** — kiểm tra xem từ `Stephane` có xuất hiện trong kết quả Lambda không
  - Nếu **có** → chuyển sang trạng thái **Is Teacher** → kết quả: `"Woohoo!"`
  - Nếu **không** → chuyển sang trạng thái **Not Teacher** → kết quả: thông báo lỗi

### 3. Tạo Hàm Lambda

- Vào **AWS Lambda** → **Create function** → **Author from scratch**
- **Tên hàm:** `HelloFunction`
- **Runtime:** Node.js (phiên bản mới nhất)
- **Code (function.js):**

```javascript
export const handler = async (event) => {
  const who = event.who;
  return `Hello, ${who}!`;
};
```

**Các trường hợp kiểm thử:**
| Đầu vào (`who`) | Đầu ra |
|---|---|
| `Stephane` | `Hello, Stephane!` |
| `John` | `Hello, John!` |
| `Alice` | `Hello, Alice!` |

### 4. Liên Kết Lambda với State Machine

- Sao chép **ARN** của hàm Lambda
- Trong designer của state machine, chọn trạng thái **Lambda Invoke**
- Dán ARN vào ô **Enter function name**

### 5. Phân Quyền IAM

- Step Functions **tự động tạo execution role** khi state machine gọi Lambda (và tùy chọn X-Ray)
- Role này cấp quyền cần thiết mà không cần thiết lập thủ công

### 6. Chạy Thực Thi State Machine

Vào state machine → **Start execution** → nhập payload đầu vào:

**Thực thi 1 — Thành công:**
```json
{ "who": "Stephane Maarek" }
```
- Lambda trả về: `Hello, Stephane Maarek!`
- Choice State phát hiện `Stephane` → chuyển sang **Is Teacher**
- Kết quả cuối: `Woohoo!`

**Thực thi 2 — Lỗi:**
```json
{ "who": "John Doe" }
```
- Lambda trả về: `Hello, John Doe!`
- Choice State **không** tìm thấy `Stephane` → chuyển sang **Not Teacher**
- Kết quả cuối: Lỗi — *"Stephane the teacher wasn't found in the output of the Lambda Function"*

---

## Xem Lịch Sử Thực Thi

- Sau khi thực thi, chọn một lần chạy để xem:
  - Từng **sự kiện** theo từng bước
  - **Thời gian** thực thi từng trạng thái
  - **Đầu vào / Đầu ra** tại mỗi giai đoạn
- Rất hữu ích để gỡ lỗi và kiểm tra luồng hoạt động

---

## Sơ Đồ Kiến Trúc

```
┌─────────────────────┐
│    Payload Đầu Vào  │
│   { who: "..." }    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Lambda Invoke    │  ──► HelloFunction(event.who)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Choice State     │
└────┬────────────┬───┘
     │            │
Có "Stephane"  Không có "Stephane"
trong kết quả?  trong kết quả?
     │            │
     ▼            ▼
┌──────────┐  ┌──────────────┐
│Is Teacher│  │ Not Teacher  │
│ Woohoo! │  │  Mã Lỗi      │
└──────────┘  └──────────────┘
```

---

## Điểm Cần Nhớ

1. Step Functions dùng **JSON** để định nghĩa state machine (`state-machine.json`)
2. **Choice State** cho phép phân nhánh có điều kiện dựa trên giá trị đầu ra
3. Hàm Lambda được liên kết thông qua **ARN**
4. Step Functions **tự tạo IAM role** để cấp quyền cho Lambda/X-Ray
5. Lịch sử thực thi cung cấp đầy đủ thông tin đầu vào, đầu ra và thời gian của từng trạng thái

---

## Câu Hỏi Ôn Tập

1. AWS Step Functions sử dụng định dạng nào để định nghĩa state machine?
2. Mục đích của **Choice State** trong luồng này là gì?
3. State machine nhận quyền gọi Lambda bằng cách nào?
4. Điều gì xảy ra khi kết quả Lambda **không** chứa từ `Stephane`?
5. Tìm ARN của hàm Lambda ở đâu để liên kết với state machine?

---

*Chủ đề: AWS Step Functions | AWS Lambda | Điều Phối Serverless*
