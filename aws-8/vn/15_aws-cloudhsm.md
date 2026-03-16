# AWS CloudHSM – Tài Liệu Học Tập

## Tổng Quan

| Dịch vụ | Ai quản lý khóa | Ai quản lý phần cứng |
|---------|----------------|---------------------|
| **KMS** | AWS quản lý phần mềm & khóa | AWS |
| **CloudHSM** | **Bạn** tự quản lý khóa hoàn toàn | AWS cung cấp phần cứng |

---

## CloudHSM Là Gì?

- **HSM** = Hardware Security Module (Mô-đun Bảo Mật Phần Cứng) — là **thiết bị vật lý chuyên dụng** do AWS cung cấp bên trong đám mây.
- Bạn có **toàn quyền kiểm soát** các khóa mã hóa; AWS **không thể truy cập** vào chúng.
- Đạt chuẩn **FIPS 140-2 Level 3** (chống giả mạo — mọi nỗ lực truy cập vật lý đều bị chặn và ngăn chặn).
- Hỗ trợ cả khóa mã hóa **đối xứng** lẫn **bất đối xứng** (ví dụ: khóa SSL/TLS).
- **Không có gói miễn phí (free tier)**.
- Yêu cầu sử dụng **phần mềm CloudHSM client** để kết nối vào dịch vụ.

---

## Các Khái Niệm Quan Trọng

### Các Loại Khóa Mã Hóa Được Hỗ Trợ
| Loại | Hỗ trợ |
|------|--------|
| Đối xứng (Symmetric) | ✅ |
| Bất đối xứng (Asymmetric) | ✅ |
| Ký số (Digital Signing) | ✅ |
| Băm (Hashing) | ✅ |

### IAM vs Phần Mềm CloudHSM
- **Quyền IAM** → dùng để **tạo, đọc, cập nhật, xóa** *cluster* HSM ở mức cao.
- **Phần mềm CloudHSM** → dùng để **quản lý khóa, người dùng và quyền truy cập** bên trong cluster.
- Khác với KMS, nơi **tất cả được quản lý qua IAM**.

---

## Tính Sẵn Sàng Cao (High Availability)

- Cluster CloudHSM có thể được triển khai trên **nhiều Vùng Khả Dụng (AZ)**.
- Các thiết bị HSM được **sao chép** qua các AZ.
- CloudHSM client có thể kết nối tới **bất kỳ** thiết bị HSM nào trong cluster một cách minh bạch.

---

## Tích Hợp với Các Dịch Vụ AWS

### CloudHSM + KMS (Custom Key Store)
1. Tạo một **CloudHSM cluster**.
2. Định nghĩa một **KMS Custom Key Store** được hỗ trợ bởi cluster CloudHSM đó.
3. Lúc này mã hóa KMS cho **EBS, S3, RDS**, v.v. sẽ dùng khóa lưu trong CloudHSM **của bạn**.
4. Mọi lệnh gọi API qua KMS đều được **ghi lại trong CloudTrail**.

### CloudHSM + Redshift
- Tích hợp trực tiếp cho **mã hóa cơ sở dữ liệu và quản lý khóa**.

### CloudHSM + S3 (SSE-C)
- Lý tưởng cho **Mã hóa phía server với khóa do khách hàng cung cấp (SSE-C)** trên S3.
- Bạn tự quản lý và lưu trữ khóa trong CloudHSM.

---

## So Sánh CloudHSM và KMS

| Tính năng | KMS | CloudHSM |
|-----------|-----|----------|
| Mô hình thuê | Nhiều người dùng (Multi-tenant) | **Một người dùng (Single-tenant)** |
| Quản lý khóa | AWS sở hữu / AWS quản lý / Khách hàng quản lý | **Chỉ** khách hàng quản lý |
| Loại khóa | Đối xứng, Bất đối xứng, Ký số | Đối xứng, Bất đối xứng, Ký số, **Băm** |
| Khả năng truy cập khóa | Nhiều region (gốc) | Dựa trên VPC; chia sẻ qua **VPC Peering** |
| Tăng tốc mã hóa | Không có | Tăng tốc **SSL/TLS**; Tăng tốc **Oracle TDE** |
| Xác thực & Phân quyền | **IAM** | Hệ thống **người dùng/quyền riêng** của CloudHSM |
| Tính sẵn sàng cao | Dịch vụ được quản lý (luôn sẵn sàng) | Nhiều thiết bị HSM trên **nhiều AZ** |
| Giám sát | CloudTrail + CloudWatch | CloudTrail + CloudWatch + **Hỗ trợ MFA** |
| Gói miễn phí | ✅ Có | ❌ Không |

---

## Điểm Mấu Chốt Cần Nhớ

- Dùng **KMS** khi bạn muốn một dịch vụ mã hóa đơn giản, được quản lý hoàn toàn và tích hợp với IAM.
- Dùng **CloudHSM** khi bạn cần:
  - **Phần cứng chuyên dụng** với mô hình cô lập single-tenant.
  - **Toàn quyền sở hữu** khóa mã hóa (AWS không bao giờ động vào).
  - Tuân thủ chuẩn **FIPS 140-2 Level 3**.
  - Tăng tốc phần cứng cho **SSL/TLS hoặc Oracle TDE**.
- Bạn có thể kết hợp cả hai: dùng **CloudHSM làm KMS custom key store** để có lợi ích ghi log CloudTrail với khóa phần cứng của riêng bạn.

---

## Câu Hỏi Ôn Tập Nhanh

1. Ai quản lý các khóa mã hóa trong CloudHSM?
2. CloudHSM đáp ứng tiêu chuẩn tuân thủ nào?
3. Sự khác biệt giữa quản lý cluster CloudHSM qua IAM và qua phần mềm CloudHSM là gì?
4. CloudHSM có thể được sử dụng với mã hóa S3 như thế nào?
5. CloudHSM có nằm trong gói miễn phí của AWS không?

<details>
<summary>Đáp Án</summary>

1. **Khách hàng** — AWS không có quyền truy cập vào các khóa CloudHSM.
2. **FIPS 140-2 Level 3**.
3. IAM = thao tác ở cấp cluster (tạo/xóa cluster). Phần mềm CloudHSM = quản lý khóa và người dùng bên trong cluster.
4. Thông qua **SSE-C** (Mã hóa phía server với khóa do khách hàng cung cấp) — khóa được lưu trữ trong CloudHSM.
5. **Không**, CloudHSM không có gói miễn phí.

</details>
