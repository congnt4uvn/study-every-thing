# Hướng Dẫn AWS CloudFormation Stack Policies

## Giới Thiệu

CloudFormation Stack policies là một tính năng bảo mật quan trọng cho phép bạn kiểm soát những tài nguyên nào trong stack có thể được cập nhật và những tài nguyên nào cần được bảo vệ khỏi các thay đổi.

## Hành Vi Mặc Định

Khi bạn thực hiện cập nhật CloudFormation Stack, theo mặc định, mọi hành động đều được phép trên tất cả các tài nguyên. Điều này có nghĩa là bạn có thể thay đổi stack của mình tùy ý mà không có hạn chế.

## Stack Policies Là Gì?

Stack policies là các tài liệu JSON định nghĩa những hành động cập nhật nào được phép trên các tài nguyên cụ thể trong quá trình cập nhật Stack. Chúng giúp bạn bảo vệ stack của mình, hoặc các phần cụ thể của stack, khỏi các cập nhật không mong muốn.

### Tính Năng Chính

- **Bảo Vệ Có Chọn Lọc**: Bạn có thể bảo vệ các tài nguyên cụ thể trong khi vẫn cho phép cập nhật các tài nguyên khác
- **Định Dạng JSON**: Stack policies được viết dưới dạng tài liệu JSON
- **Kiểm Soát Cập Nhật**: Định nghĩa chính xác những hành động cập nhật nào được phép trên mỗi tài nguyên

## Ví Dụ Stack Policy

Đây là một ví dụ thực tế về Stack policy:

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "ProductionDatabase"
    }
  ]
}
```

### Giải Thích Ví Dụ

1. **Statement Thứ Nhất**: `"Allow update*"` trên mọi thứ
   - Điều này cho phép tất cả các tài nguyên trong CloudFormation Stack của bạn được cập nhật theo mặc định

2. **Statement Thứ Hai**: `"Deny update*"` trên Resource "ProductionDatabase"
   - Bất kỳ tài nguyên nào được đặt tên là "ProductionDatabase" trong CloudFormation Stack của bạn sẽ được bảo vệ khỏi mọi loại cập nhật
   - Cơ sở dữ liệu production của bạn được giữ an toàn khỏi các thay đổi vô tình

## Cách Stack Policies Hoạt Động

### Bảo Vệ Mặc Định

Khi bạn thiết lập một Stack policy, **theo mặc định, tất cả các tài nguyên đều được bảo vệ**. Đây là một tính năng bảo mật quan trọng.

### Yêu Cầu Explicit Allow

Để cho phép cập nhật các tài nguyên cụ thể, bạn cần bao gồm một statement **"allow" rõ ràng** cho những tài nguyên đó trong policy của bạn.

## Mục Đích và Lợi Ích

Các mục tiêu chính của Stack policies là:

- **Ngăn Chặn Cập Nhật Không Mong Muốn**: Bảo vệ các tài nguyên quan trọng khỏi các thay đổi vô tình
- **An Toàn Production**: Giữ cho cơ sở dữ liệu production và các hạ tầng quan trọng khác được an toàn
- **Kiểm Soát Chi Tiết**: Định nghĩa chính xác những tài nguyên nào có thể được sửa đổi và những tài nguyên nào không thể

## Những Điểm Chính Cần Nhớ

- Stack policies sử dụng định dạng JSON để định nghĩa quyền cập nhật
- Theo mặc định, khi một policy được thiết lập, tất cả các tài nguyên đều được bảo vệ
- Bạn phải cho phép rõ ràng việc cập nhật cho các tài nguyên mà bạn muốn sửa đổi
- Các tài nguyên quan trọng như cơ sở dữ liệu production có thể được bảo vệ vĩnh viễn khỏi các cập nhật

## Mẹo Thi Chứng Chỉ

Hiểu về Stack policies rất quan trọng cho các kỳ thi chứng chỉ AWS. Các điểm chính cần nhớ:

- Stack policies kiểm soát những gì có thể được cập nhật trong CloudFormation stack
- Hành vi mặc định không có policies: mọi thứ đều có thể được cập nhật
- Hành vi mặc định với policies: mọi thứ đều được bảo vệ trừ khi được cho phép rõ ràng
- Hữu ích cho việc bảo vệ các tài nguyên production quan trọng

---

*Hướng dẫn này bao gồm các khái niệm thiết yếu về CloudFormation Stack policies mà bạn cần biết để làm việc với hạ tầng AWS dưới dạng code.*