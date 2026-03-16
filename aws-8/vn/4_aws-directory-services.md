# Hướng Dẫn Học AWS Directory Services

## 1. Microsoft Active Directory (AD) là gì?

Microsoft Active Directory là phần mềm được cài trên **Windows Server** với **AD Domain Services**. Về cơ bản, đây là một **cơ sở dữ liệu các đối tượng**, bao gồm:

- Tài khoản người dùng
- Máy tính
- Máy in
- Chia sẻ tệp (File shares)
- Nhóm bảo mật (Security groups)

### Các Khái Niệm Chính

| Thuật ngữ | Mô tả |
|-----------|-------|
| **Domain Controller** | Máy chủ trung tâm quản lý tất cả các đối tượng trong AD |
| **Tree (Cây)** | Cấu trúc phân cấp của các đối tượng trong AD |
| **Forest (Rừng)** | Một nhóm các Tree |

### Cách Hoạt Động (Ví dụ đơn giản)

1. Thiết lập một Domain Controller.
2. Tạo một tài khoản (ví dụ: tên đăng nhập: `John`, mật khẩu: `password`).
3. Tất cả các máy Windows trong mạng đều kết nối với Domain Controller.
4. Khi người dùng đăng nhập trên bất kỳ máy nào, máy đó sẽ kiểm tra thông tin xác thực với Domain Controller.
5. Người dùng có thể truy cập bất kỳ máy nào trong mạng chỉ bằng một tài khoản duy nhất.

---

## 2. AWS Directory Services

AWS Directory Services cung cấp cách thức để **tạo và sử dụng Active Directory trên AWS**. Có **ba loại chính**:

---

### 2.1 AWS Managed Microsoft AD

- Tạo **Active Directory của riêng bạn trên AWS**.
- Quản lý người dùng **trực tiếp trong AWS**.
- Hỗ trợ **Xác thực Đa yếu tố (MFA)**.
- Có thể thiết lập **kết nối tin cậy (trust connection)** với **AD on-premise** của bạn.
  - AWS AD tin tưởng AD on-premise và ngược lại.
  - Người dùng có thể xác thực với cả hai directory.
  - Người dùng được **chia sẻ** giữa AWS AD và AD on-premise.

**Các phiên bản:**
| Phiên bản | Số đối tượng tối đa |
|-----------|---------------------|
| Standard  | Lên đến 30.000 đối tượng |
| Enterprise | Lên đến 500.000 đối tượng |

> **Trường hợp sử dụng:** Bạn muốn quản lý người dùng **cả trên AWS và on-premise**, có hỗ trợ MFA.

---

### 2.2 AD Connector

- Hoạt động như một **cổng kết nối/proxy trực tiếp** để chuyển tiếp yêu cầu xác thực đến **AD on-premise** của bạn.
- Hỗ trợ **MFA**.
- Người dùng được **quản lý hoàn toàn ở AD on-premise**.
- AD Connector **không lưu trữ** bất kỳ dữ liệu người dùng nào — chỉ làm nhiệm vụ proxy.

**Kích cỡ:**
| Loại Connector | Số người dùng tối đa |
|----------------|----------------------|
| Nhỏ (Small)    | Lên đến 500 người dùng |
| Lớn (Large)    | Lên đến 5.000 người dùng |

> **Trường hợp sử dụng:** Bạn muốn **proxy người dùng đến AD on-premise** mà không lưu trữ gì trên AWS.

---

### 2.3 Simple AD

- Là một **directory độc lập, được quản lý, tương thích với AD** trên AWS.
- **KHÔNG** sử dụng công nghệ Microsoft Active Directory thực sự.
- **Không thể** kết nối hoặc tích hợp với Active Directory on-premise.

> **Trường hợp sử dụng:** Bạn **không có AD on-premise** và chỉ cần một directory đơn giản, độc lập cho tài nguyên AWS.

---

## 3. Bảng So Sánh

| Tính năng | AWS Managed Microsoft AD | AD Connector | Simple AD |
|-----------|--------------------------|--------------|-----------|
| Quản lý user trong AWS | Có | Không | Có |
| Quản lý user on-premise | Có (qua trust) | Có (duy nhất) | Không |
| Hỗ trợ MFA | Có | Có | Không |
| Trust với AD on-premise | Có | Không (proxy) | Không |
| Công nghệ Microsoft AD | Có | Chỉ proxy | Không |
| Hoạt động độc lập | Có | Không | Có |

---

## 4. Tại Sao Dùng AWS Directory Services Với EC2?

- Các EC2 instance chạy **Windows** có thể tham gia vào một domain controller.
- Điều này cho phép các Windows EC2 instance **chia sẻ thông tin đăng nhập và xác thực**.
- Có một directory trong AWS giúp giữ nó **gần với EC2 instance hơn**, giảm độ trễ.

---

## 5. Mẹo Thi

- **AD Connector** → Proxy người dùng đến AD on-premise (không quản lý user trong AWS).
- **AWS Managed Microsoft AD** → Quản lý user trên cloud (AWS) với MFA + tùy chọn trust với on-premise.
- **Simple AD** → Không có AD on-premise; chỉ cần một directory độc lập trong AWS.

> **Lưu ý:** Amazon Cognito User Pool đôi khi được liệt kê cùng với directory services trong console AWS nhưng là một **dịch vụ riêng biệt** — nó **không** tính là directory service.
