# Cập Nhật Luân Phiên ECS Service (Rolling Updates)

## Tổng Quan

Khi cập nhật một ECS service từ phiên bản 1 lên phiên bản 2, bạn có thể kiểm soát số lượng task sẽ được khởi động và dừng tại một thời điểm cũng như thứ tự thực hiện thông qua rolling updates (cập nhật luân phiên).

## Các Tham Số Cấu Hình Cập Nhật

Khi bạn cập nhật một ECS service bằng cách chọn một task definition mới, bạn sẽ có hai cài đặt quan trọng:

- **Minimum Healthy Percent** - Phần trăm tối thiểu (mặc định: 100)
- **Maximum Percent** - Phần trăm tối đa (mặc định: 200)

### Cách Hoạt Động

ECS service của bạn đang chạy các task đại diện cho công suất thực tế đang chạy là 100%.

- **Minimum Healthy Percent**: Nếu được đặt dưới 100%, điều này cho phép bạn terminate (dừng) các task, miễn là bạn có đủ task để duy trì phần trăm trên mức tối thiểu.

- **Maximum Percent**: Cho biết bạn có thể tạo bao nhiêu task mới của phiên bản 2 để triển khai cập nhật cho service của mình.

Hai cài đặt này kiểm soát cách thực hiện cập nhật bằng cách tạo task mới, terminate task cũ, và đảm bảo tất cả task của bạn được cập nhật lên phiên bản mới hơn.

## Kịch Bản 1: Min 50% / Max 100%

Bắt đầu với **4 task**:

1. **Terminate 2 task** → Chạy ở 50% công suất
2. **Tạo 2 task mới** → Trở lại 100% công suất
3. **Terminate 2 task cũ** → Trở lại 50% công suất
4. **Tạo 2 task mới** → Trở lại 100% công suất

✅ Hoàn thành cập nhật luân phiên!

Trong kịch bản này, các task bị terminate trước vì minimum được đặt ở 50% và maximum ở 100%.

## Kịch Bản 2: Min 100% / Max 150%

Bắt đầu với **4 task**:

1. **Không thể terminate task** (minimum là 100%)
2. **Tạo 2 task mới** → Công suất ở 150%
3. **Terminate 2 task cũ** → Trở lại 100% công suất
4. **Tạo 2 task mới** → Công suất ở 150%
5. **Terminate 2 task cũ** → Trở lại 100% công suất

✅ Hoàn thành cập nhật luân phiên!

Trong kịch bản này, task mới được tạo trước khi terminate task cũ, duy trì ít nhất 100% công suất trong suốt quá trình cập nhật.

## Điểm Chính Cần Nhớ

- Rolling updates cho phép bạn kiểm soát quá trình cập nhật ECS service
- **Minimum Healthy Percent** xác định công suất thấp nhất trong quá trình cập nhật
- **Maximum Percent** xác định số lượng task bổ sung có thể chạy trong quá trình cập nhật
- Các kết hợp khác nhau của những cài đặt này cung cấp các chiến lược cập nhật khác nhau dựa trên yêu cầu về tính khả dụng của bạn

---

*Đây là một khái niệm quan trọng có thể xuất hiện trong các kỳ thi chứng chỉ AWS.*