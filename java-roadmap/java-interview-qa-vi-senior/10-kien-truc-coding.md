# 10) Kiến trúc & Coding (91–100)

## 91. Làm sao bạn chọn cấu trúc package/module cho dự án lớn?

**Đáp:** Tối thiểu: tách theo domain/bounded context hoặc theo layer rõ ràng. Tránh “god package”. Mục tiêu: cohesion cao, coupling thấp, và dependency hướng vào trong.

## 92. “Hexagonal / Ports and Adapters” giúp gì?

**Đáp:** Tách core logic khỏi hạ tầng (DB, HTTP). Giúp test dễ, thay adapter dễ, và giảm lock-in công nghệ.

## 93. Làm sao giảm coupling giữa modules?

**Đáp:** Dùng interface/DTO ổn định, tránh chia sẻ model persistence ra ngoài, và kiểm soát dependency (không cho module ngoài “đi tắt” vào bên trong).

## 94. Bạn đánh giá một PR “tốt” theo tiêu chí nào?

**Đáp:** Đúng chức năng, test phù hợp, rõ ràng dễ đọc, không làm tăng rủi ro vận hành (timeouts, limits), có logging/metrics hợp lý, và không phá backward compatibility.

## 95. Khi nào dùng `Optional` trong API public?

**Đáp:** Thường dùng cho return value “có thể không có”. Tránh dùng `Optional` cho tham số hoặc field nếu làm API rối; cân nhắc overload hoặc builder.

## 96. Bạn xử lý “resource lifecycle” như thế nào?

**Đáp:** Dùng try-with-resources cho mọi resource close được, đóng ở đúng nơi sở hữu, và đảm bảo shutdown thread pool/HTTP client khi app dừng.

## 97. Vì sao “immutability by default” hữu ích cho hệ thống lớn?

**Đáp:** Giảm bug do state thay đổi bất ngờ, dễ share giữa thread, và làm API dễ dự đoán. Khi cần mutable, khoanh vùng rõ.

## 98. Bạn viết code “defensive” ở đâu là hợp lý?

**Đáp:** Ở boundary (nhận input từ network/DB), validate sớm, và fail-fast với message rõ. Trong core logic, ưu tiên giữ invariant mạnh để giảm check lặp.

## 99. Làm sao tránh “leaky abstraction” khi dùng thư viện/framework?

**Đáp:** Bọc thư viện bằng adapter nhỏ, không rải API framework khắp codebase, và giới hạn điểm phụ thuộc để dễ thay thế/nâng cấp.

## 100. Bạn dạy junior xử lý bug production như thế nào?

**Đáp:** Dạy quy trình: tái tạo (nếu được), thu thập evidence, giả thuyết, kiểm tra giả thuyết bằng đo đạc, fix nhỏ có rollback plan, và viết postmortem/guardrails.
