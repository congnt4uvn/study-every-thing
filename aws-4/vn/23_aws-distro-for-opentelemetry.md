# AWS Distro for OpenTelemetry (ADOT) — Ghi chú học tập

## Bạn đang học gì
Tài liệu này tóm tắt **AWS Distro for OpenTelemetry (ADOT)** dựa trên nội dung trong `file.txt`.

## OpenTelemetry (OTel) trong 1 phút
**OpenTelemetry** là một chuẩn mã nguồn mở, cung cấp:
- Một bộ **API, thư viện, agent và dịch vụ collector** thống nhất
- Để thu thập **distributed traces (dấu vết phân tán)** và **metrics (chỉ số)** cho ứng dụng
- Đồng thời có thể thu thập **metadata/ngữ cảnh** từ các tài nguyên và dịch vụ AWS

Có thể hiểu đơn giản: “chuẩn hoá cách instrument (gắn đo đạc) telemetry” cho nhiều môi trường.

## AWS Distro for OpenTelemetry (ADOT) là gì?
**ADOT** là một **bản phân phối (distribution) của OpenTelemetry** do **AWS hỗ trợ**, được mô tả là **an toàn** và **sẵn sàng cho production**.

Về thực tế, ADOT giúp bạn:
- Instrument ứng dụng theo chuẩn OpenTelemetry
- Thu thập traces/metrics ở quy mô lớn
- Gửi telemetry tới **dịch vụ AWS** và **giải pháp giám sát của đối tác**

## Ứng dụng có thể chạy ở đâu (nơi instrument)
Theo transcript, các workload có thể nằm:
- **EC2**
- **ECS**
- **EKS**
- **Fargate**
- **Lambda**
- Ứng dụng **on-premises**

## Dữ liệu được thu thập
- **Traces**: theo dõi luồng request end-to-end qua hệ thống phân tán
- **Metrics**: các chỉ số đo lường (ví dụ độ trễ, lỗi, v.v.)
- **Dữ liệu ngữ cảnh về tài nguyên AWS** (nhờ bản phân phối của AWS)

## Có thể gửi dữ liệu đi đâu (đích đến)
Ví dụ được nhắc trong transcript:
- **AWS X-Ray** (traces)
- **Amazon CloudWatch** (metrics)
- **Amazon Managed Service for Prometheus** (telemetry theo OpenTelemetry)
- **Giải pháp đối tác** (ví dụ: Datadog)

Ý chính: OpenTelemetry có thể hỗ trợ gửi telemetry tới **nhiều đích cùng lúc**.

## OpenTelemetry vs AWS X-Ray (theo mô tả)
OpenTelemetry được nói là **tương tự X-Ray**, nhưng:
- **OTel là chuẩn mã nguồn mở**
- Bạn có thể chuyển từ X-Ray sang ADOT nếu muốn:
  - Chuẩn hoá theo API mã nguồn mở
  - Gửi trace/metric tới **nhiều đích đồng thời**

## Auto-instrumentation (vì sao quan trọng)
Agent có thể **auto-instrument** để thu thập traces **mà không cần sửa code** (cảm giác tương tự cách instrument của X-Ray).

## Gợi ý ôn thi
Nếu gặp trong bối cảnh đề thi AWS, thường chỉ hỏi **mức tổng quan**. Cần nhớ:
- ADOT = bản phân phối OTel do AWS hỗ trợ
- OTel thu thập **traces + metrics** (và metadata/ngữ cảnh AWS)
- Có thể export sang X-Ray/CloudWatch/Prometheus/đối tác
- Điểm khác so với chỉ dùng X-Ray: **chuẩn mở + multi-destination export**

## Tự kiểm tra nhanh (câu hỏi)
1. OpenTelemetry cung cấp những thành phần nào?
2. Hai loại telemetry chính được nhắc tới là gì?
3. Kể 3 môi trường/workload có thể instrument.
4. Kể 2 đích AWS và 1 đích đối tác có thể nhận telemetry.
5. Vì sao chọn ADOT thay vì chỉ dùng X-Ray?
