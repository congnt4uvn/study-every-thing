# 06) Classloading, Modules & Reflection (51–60)

## 51. Parent delegation model là gì?

**Đáp:** Classloader thường hỏi parent trước khi tự load class. Mục tiêu: tránh load trùng các core class và đảm bảo tính nhất quán.

## 52. Khi nào parent delegation bị “phá vỡ” và vì sao?

**Đáp:** Plugin/app server đôi khi dùng “child-first” để cách ly version thư viện. Trade-off: dễ gây ClassCastException do cùng tên class nhưng khác classloader.

## 53. Vì sao có `ClassCastException` dù tên class giống nhau?

**Đáp:** Trong JVM, “định danh” class = (tên class + classloader). Hai class cùng tên nhưng khác classloader là hai kiểu khác nhau.

## 54. JPMS giúp gì so với classpath?

**Đáp:** Khai báo dependency rõ, encapsulation mạnh, giảm “jar hell”, và hỗ trợ runtime image tối ưu. Đổi lại: cấu hình module phức tạp hơn với hệ sinh thái cũ.

## 55. “Split package” là gì trong modules?

**Đáp:** Một package xuất hiện trong nhiều module/jar. JPMS không thích split package vì gây mơ hồ và xung đột.

## 56. Multi-release JAR là gì?

**Đáp:** Một JAR chứa class khác nhau theo version Java để tận dụng API mới mà vẫn tương thích Java cũ. Cần build đúng và test cẩn thận.

## 57. Vì sao “illegal reflective access” xảy ra?

**Đáp:** Do code phản chiếu vào package không được mở/export theo module rules. Giải pháp: nâng cấp lib, cấu hình module hợp lệ; flags chỉ là tạm thời.

## 58. ServiceLoader dùng để làm gì?

**Đáp:** Cơ chế phát hiện và load implementation tại runtime (SPI). Dùng cho plugin nhẹ, tách interface và implement.

## 59. Annotation processing (APT) là gì và dùng khi nào?

**Đáp:** Xử lý annotation lúc compile để sinh code/metadata (vd mapstruct, lombok). Lợi ích: runtime nhẹ hơn reflection, nhưng build phức tạp hơn.

## 60. Bạn chẩn đoán lỗi classpath/version conflict thế nào?

**Đáp:** Xem dependency tree (Maven/Gradle), kiểm tra jar chứa class, chú ý “nearest wins”/resolution rule, và tìm stacktrace liên quan `NoSuchMethodError`/`ClassNotFoundException`.
