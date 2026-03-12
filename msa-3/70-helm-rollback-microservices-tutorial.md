# Hướng Dẫn Helm Rollback cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách quay lại (rollback) phiên bản hoạt động trước đó của microservices deployment bằng cách sử dụng Helm. Khác với Kubectl, yêu cầu rollback từng thành phần một, Helm cho phép rollback toàn bộ các thành phần Kubernetes cluster về trạng thái mong muốn trước đó chỉ với một lệnh duy nhất.

## Lợi Ích Chính của Helm Rollback

- **Rollback Bằng Một Lệnh Duy Nhất**: Quay lại toàn bộ các thành phần Kubernetes cluster chỉ với một lệnh
- **Hỗ Trợ Đa Dịch Vụ**: Bất kể bạn đã thay đổi bao nhiêu microservices, rollback vẫn được thực hiện chỉ với một lệnh duy nhất
- **Theo Dõi Lịch Sử Phiên Bản**: Duy trì lịch sử rõ ràng về tất cả các deployments và upgrades

## Lệnh Helm History

Trước khi thực hiện rollback, bạn có thể xem lịch sử deployment bằng lệnh Helm History.

### Cú Pháp
```bash
helm history <tên-release>
```

### Ví Dụ
```bash
helm history easybank
```

Lệnh này hiển thị tất cả các cài đặt và nâng cấp đã xảy ra cho một Helm chart cụ thể, bao gồm:
- Số revision
- Trạng thái cài đặt/deployment
- Các thay đổi được thực hiện trong mỗi revision

### Cấu Trúc Output Mẫu
- **Revision 1**: Cài đặt ban đầu hoàn tất
- **Revision 2**: Deploy với tag name s12 (có lỗi)
- **Revision 3**: Cập nhật với tag name s11, trạng thái hiện tại đang deployed

## Thực Hiện Rollback

### Cú Pháp Lệnh
```bash
helm rollback <tên-release> <số-revision>
```

### Ví Dụ: Rollback về Revision 1
```bash
helm rollback easybank 1
```

Lệnh này sẽ:
1. Rollback về revision được chỉ định (revision 1 trong ví dụ này)
2. Thực thi rollback chỉ với một lệnh duy nhất
3. Trả về thông báo thành công khi hoàn tất

## Xác Minh Rollback

### Sử Dụng Kubernetes Dashboard

1. Điều hướng đến Kubernetes dashboard
2. Vào phần **Pods**
3. Mở pod mới được tạo
4. Kiểm tra tab **Events** để xem:
   - Docker image mới đang được deploy (ví dụ: s14)
   - Tiến trình deployment

### Kiểm Tra Application Logs

Giám sát logs để xác minh ứng dụng đã khởi động thành công:
- Gateway server application nên khởi động không có lỗi
- Tất cả services nên đang chạy bình thường

### Kiểm Tra Bằng API Calls

Xác thực rollback bằng cách test các API của bạn:
- Trong ví dụ này, thử gọi API nên trả về **lỗi 401** (như mong đợi với bảo mật thích hợp)
- Điều này xác nhận gateway server hiện đã được bảo mật đúng cách

## Lịch Sử Sau Rollback

Sau khi hoàn thành rollback, chạy lại lệnh history sẽ hiển thị:

```bash
helm history easybank
```

Bạn sẽ thấy một revision mới (ví dụ: Revision 4) với comment chỉ ra "rollback to 1". Điều này cung cấp tài liệu rõ ràng cho:
- Các thao tác rollback trong tương lai
- Hiểu lịch sử deployment
- Theo dõi các thay đổi cho một release cụ thể

## Best Practices (Thực Hành Tốt Nhất)

1. **Luôn Kiểm Tra History Trước**: Xem lại lịch sử revision trước khi thực hiện rollback
2. **Ghi Chép Các Thay Đổi**: Duy trì tài liệu rõ ràng về những thay đổi được thực hiện trong mỗi revision
3. **Kiểm Tra Sau Rollback**: Luôn xác minh rollback thành công thông qua logs và API testing
4. **Cập Nhật File Cấu Hình**: Sau rollback, cập nhật file values.yaml để phản ánh trạng thái hiện tại trước khi check-in vào version control (ví dụ: GitHub)

## Kết Luận

Helm rollback là một tính năng mạnh mẽ giúp đơn giản hóa quy trình quay lại các phiên bản hoạt động trước đó của microservices deployment. Chỉ với một lệnh duy nhất, bạn có thể đảm bảo toàn bộ Kubernetes cluster của mình quay trở lại trạng thái ổn định, mong muốn, khiến nó trở thành công cụ thiết yếu để quản lý microservices trong môi trường production.

---

**Lưu Ý**: Hướng dẫn này là một phần của series toàn diện về microservices bao gồm Spring Boot, Kubernetes và Helm.