# Hướng Dẫn Về CloudFormation Capabilities (Khả Năng)

## Tổng Quan

CloudFormation capabilities (khả năng) là các tính năng bảo mật quan trọng mà bạn cần hiểu khi làm việc với các template AWS CloudFormation. Các khả năng này đảm bảo rằng bạn xác nhận rõ ràng các hành động mà CloudFormation sẽ thực hiện thay mặt bạn, đặc biệt khi xử lý các tài nguyên IAM.

## Các Loại CloudFormation Capabilities

### 1. CAPABILITY_IAM và CAPABILITY_NAMED_IAM

Các khả năng này được yêu cầu bất cứ khi nào template CloudFormation của bạn sẽ tạo hoặc cập nhật các tài nguyên IAM, chẳng hạn như:

- IAM users (người dùng IAM)
- IAM roles (vai trò IAM)
- IAM groups (nhóm IAM)
- IAM policies (chính sách IAM)

**Khi nào sử dụng:**
- Sử dụng `CAPABILITY_NAMED_IAM` nếu các tài nguyên IAM có tên tùy chỉnh được chỉ định trong template
- Sử dụng `CAPABILITY_IAM` nếu các tài nguyên không có tên tùy chỉnh (AWS tự động tạo tên)

**Tại sao cần thiết:**
Yêu cầu khả năng này đảm bảo rằng bạn xác nhận rõ ràng việc CloudFormation sẽ tạo các tài nguyên IAM trong tài khoản của bạn. Đây là một biện pháp bảo mật quan trọng vì các tài nguyên IAM kiểm soát quyền truy cập vào môi trường AWS của bạn.

### 2. CAPABILITY_AUTO_EXPAND

Khả năng này được yêu cầu khi template CloudFormation của bạn bao gồm:
- Macros (macro)
- Nested stacks (các stack lồng nhau - stack trong stack)

Các tính năng này thực hiện các chuyển đổi động trên template của bạn. Bằng cách chỉ định khả năng này, bạn xác nhận rằng template có thể thay đổi trước khi được triển khai.

## Xử Lý InsufficientCapabilitiesException

Nếu bạn gặp phải `InsufficientCapabilitiesException` khi khởi chạy một template, điều đó có nghĩa là:

1. Template CloudFormation yêu cầu các khả năng cụ thể
2. Bạn chưa xác nhận các khả năng này

**Giải pháp:**
Là một biện pháp bảo mật, bạn cần:
1. Xem xét các yêu cầu của template
2. Gửi lại template với các khả năng phù hợp được xác nhận
3. Điều này có thể được thực hiện bằng cách thêm một tham số bổ sung trong API call hoặc đánh dấu vào checkbox trên AWS Console

## Ví Dụ Thực Tế

### Template CloudFormation Mẫu (3_capabilities.yaml)

Đây là ví dụ về template CloudFormation tạo một IAM role:

```yaml
Resources:
  MyIAMRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: MyCustomRoleName
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEC2FullAccess
```

### Các Bước Triển Khai

1. Truy cập CloudFormation console
2. Nhấp vào "Create Stack"
3. Tải lên file template (`3_capabilities.yaml`)
4. Đặt tên cho stack (ví dụ: "DemoIAM")
5. Tiếp tục qua các bước cấu hình
6. **Quan trọng:** Ở trang xem xét cuối cùng, bạn phải xác nhận khả năng

### Xác Nhận Trên AWS Console

Ở bước xem xét cuối cùng, bạn sẽ thấy một checkbox xác nhận ghi:

> "Tôi xác nhận rằng CloudFormation có thể tạo các tài nguyên IAM với tên tùy chỉnh."

**Điểm chính:**
- ✅ **Có xác nhận:** CloudFormation sẽ tạo IAM role thành công
- ❌ **Không có xác nhận:** Việc gửi stack sẽ thất bại

Xác nhận này đảm bảo bạn hiểu các tác động bảo mật của việc tạo các tài nguyên IAM thông qua CloudFormation.

## Thực Hành Tốt Nhất

1. **Luôn xem xét quyền IAM** trước khi xác nhận các khả năng
2. **Sử dụng CAPABILITY_NAMED_IAM** khi bạn có tên tài nguyên tùy chỉnh để kiểm soát tốt hơn
3. **Hiểu rõ rủi ro** của các tài nguyên IAM đang được tạo
4. **Ghi chép các yêu cầu khả năng** trong quy trình triển khai của bạn
5. **Sử dụng các thực hành tốt nhất về Infrastructure as Code (IaC)** khi định nghĩa các tài nguyên IAM

## Tóm Tắt

CloudFormation capabilities là một tính năng bảo mật quan trọng yêu cầu xác nhận rõ ràng khi:
- Tạo hoặc cập nhật các tài nguyên IAM
- Sử dụng macro hoặc nested stacks

Bằng cách yêu cầu các khả năng này, AWS đảm bảo rằng bạn biết về các tài nguyên và chuyển đổi mà CloudFormation sẽ thực hiện trong tài khoản của bạn, giúp ngăn chặn các thay đổi ngẫu nhiên hoặc trái phép đối với tư thế bảo mật của bạn.