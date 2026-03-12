# Cập Nhật Quan Trọng Về Bitnami Images & Helm Charts

## Tổng Quan

Tài liệu này cung cấp thông tin quan trọng về những thay đổi trong mô hình cấp phép của Bitnami và cách nó ảnh hưởng đến việc triển khai các thành phần microservices sử dụng Helm Charts trong môi trường Kubernetes.

## Cập Nhật Quan Trọng: Bitnami Không Còn Là Mã Nguồn Mở

Trong các bài giảng sắp tới, chúng ta sẽ sử dụng Helm Charts để triển khai một số thành phần như:
- Kafka
- Keycloak
- Prometheus
- Loki
- Alloy
- Tempo
- Grafana

### Điều Gì Đã Thay Đổi?

Trước đây, các charts và images này được cung cấp bởi **Bitnami**, vốn là mã nguồn mở và miễn phí cho tất cả mọi người. Tuy nhiên, Bitnami hiện đã chuyển đổi thành một **sản phẩm thương mại**, và các tổ chức doanh nghiệp phải trả hàng nghìn đô la mỗi tháng để sử dụng các images và Helm Charts cấp độ production của họ.

**Thông Báo Chính Thức:**  
👉 [Cách Chuẩn Bị Cho Những Thay Đổi Của Bitnami Sắp Tới](https://docs.bitnami.com/tutorials/prepare-for-bitnami-changes/)

## Chúng Ta Sẽ Sử Dụng Gì Thay Thế

Để đảm bảo bạn có thể tiếp tục học tập một cách liền mạch, các Helm Charts tùy chỉnh đã được chuẩn bị sẵn với mục đích tương tự như Bitnami — và chúng đã sẵn sàng để sử dụng cho tất cả các bài thực hành trong khóa học này.

### GitHub Repository

Bạn có thể tìm thấy các Helm Charts tùy chỉnh trong repository GitHub dưới thư mục `helm-new`:

🔗 **Link Repository:** [https://github.com/eazybytes/microservices/tree/3.4.1/section_16/helm-new](https://github.com/eazybytes/microservices/tree/3.4.1/section_16/helm-new)

**Lưu Ý:** Không cần phải sửa đổi bất cứ điều gì bên trong các charts này — chúng đã được cấu hình đầy đủ cho các bài tập thực hành.

## Thứ Tự Triển Khai

Vui lòng cài đặt các Helm charts theo thứ tự sau, chờ **1–2 phút** giữa mỗi lần triển khai:

1. **Keycloak**
2. **Kafka**
3. **Prometheus**
4. **Loki**
5. **Alloy**
6. **Tempo**
7. **Grafana**
8. **EazyBank**

### Tại Sao Thứ Tự Này Quan Trọng

Chuỗi triển khai đảm bảo rằng các phụ thuộc được thiết lập đúng cách trước khi các dịch vụ phụ thuộc được triển khai. Việc chờ đợi giữa các lần triển khai cho phép Kubernetes khởi tạo các pods và services một cách hợp lý.

## Về Demo Charts

Các charts mà chúng ta sẽ sử dụng là **phiên bản đơn giản hóa**, nhưng các khái niệm và quy trình làm việc vẫn hoàn toàn giống như bạn sẽ trải nghiệm với các Bitnami charts cấp độ production. Điều này đảm bảo rằng:

- Bạn học được các khái niệm cơ bản giống nhau
- Kiến thức có thể chuyển đổi sang môi trường production
- Trải nghiệm học tập vẫn thực tế và thực hành

## Lưu Ý Quan Trọng

⚠️ Demo/sample Helm chart được thảo luận trong bài giảng tiếp theo dựa trên Bitnami, vốn không còn là mã nguồn mở nữa.

**Vui lòng không cài đặt hoặc chạy chart đó** — chỉ cần xem bài giảng để hiểu các khái niệm và cấu trúc của Helm chart.

## Kết Luận

Hãy tiếp tục hành trình học tập thực hành của chúng ta — chúc bạn vui vẻ khám phá Helm và Kubernetes! 🚀

---

*– Madan*

## Tài Nguyên Bổ Sung

- [Tài Liệu Chính Thức Kubernetes](https://kubernetes.io/docs/)
- [Tài Liệu Chính Thức Helm](https://helm.sh/docs/)
- [Best Practices cho Spring Boot Microservices](https://spring.io/microservices)

## Chủ Đề Liên Quan

- Container Orchestration với Kubernetes
- Cấu Trúc và Quản Lý Helm Charts
- Kiến Trúc Microservices với Spring Boot
- DevOps Best Practices cho Ứng Dụng Java