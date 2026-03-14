# Dọn Dẹp AWS và Quản Lý Chi Phí

## Tổng Quan
Hướng dẫn này giúp bạn xóa các tài nguyên AWS để quản lý và kiểm soát chi phí hiệu quả sau khi hoàn thành khóa học hoặc dự án.

## Các Tài Nguyên Cần Dọn Dẹp

### 1. Elastic Beanstalk (Tốn Kém Nhất)
Elastic Beanstalk thường là tài nguyên tốn kém nhất, vì vậy việc xóa nó khi không còn cần thiết là rất quan trọng.

**Các bước xóa:**
1. Truy cập vào bảng điều khiển Elastic Beanstalk
2. Điều hướng đến các môi trường (environments) của bạn
3. Nhấp vào ứng dụng (application) bạn muốn xóa
4. Chọn "Delete" để xóa ứng dụng
5. Điều này sẽ tự động xóa tất cả các môi trường liên quan

**Quan trọng:** Hãy đảm bảo xóa Elastic Beanstalk trước vì đây là tài nguyên tốn chi phí nhất.

### 2. CodePipeline
CodePipeline có thể được xóa để giảm chi phí khi bạn không triển khai tích cực.

**Các bước xóa:**
1. Truy cập vào bảng điều khiển CodePipeline
2. Nhấp vào pipeline của bạn
3. Chọn "Edit" nếu cần
4. Nhấp "Delete" để xóa pipeline

### 3. CodeDeploy
Tương tự như CodePipeline, CodeDeploy có thể được xóa khi không sử dụng.

**Các bước xóa:**
1. Điều hướng đến bảng điều khiển CodeDeploy
2. Chọn cấu hình triển khai hoặc ứng dụng
3. Xóa các tài nguyên theo nhu cầu

## Thực Hành Tốt Nhất Để Kiểm Soát Chi Phí

- **Ưu tiên dọn dẹp:** Luôn xóa Elastic Beanstalk trước do chi phí cao
- **Xem xét định kỳ:** Kiểm tra định kỳ các tài nguyên không sử dụng
- **Dọn dẹp hoàn toàn:** Xóa tất cả tài nguyên được tạo trong quá trình học tập hoặc thử nghiệm
- **Theo dõi hóa đơn:** Để mắt đến bảng điều khiển thanh toán AWS của bạn

## Những Điểm Chính Cần Nhớ

✅ Elastic Beanstalk là tài nguyên tốn kém nhất - xóa nó trước tiên  
✅ CodePipeline và CodeDeploy có thể xóa an toàn khi không sử dụng  
✅ Xóa ứng dụng trong Elastic Beanstalk sẽ xóa tất cả các môi trường  
✅ Dọn dẹp thường xuyên giúp duy trì kiểm soát chi phí
