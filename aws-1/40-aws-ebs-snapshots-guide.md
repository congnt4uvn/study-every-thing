# Hướng Dẫn AWS EBS Snapshots

## Giới Thiệu

EBS Snapshots là một tính năng quan trọng để sao lưu và quản lý các EBS volumes của bạn trong AWS. Hướng dẫn này bao gồm các khái niệm và tính năng chính của EBS Snapshots.

## EBS Snapshots là gì?

**EBS Snapshot** là bản sao lưu của EBS volume tại bất kỳ thời điểm nào. Mặc dù không bắt buộc phải tách EBS volume khỏi EC2 instance để tạo snapshot, nhưng điều này được khuyến nghị để đảm bảo tính nhất quán của dữ liệu.

## Lợi Ích Chính

### Chuyển Đổi Giữa Các Region và AZ

EBS Snapshots có thể được sao chép qua:
- Các Availability Zones (AZs) khác nhau
- Các AWS Regions khác nhau

### Ví Dụ Chuyển Đổi

Xem xét kịch bản sau:
- **EC2 Instance A** với EBS volume trong **US-EAST-1A**
- **EC2 Instance B** trong **US-EAST-1B**

Bạn có thể:
1. Tạo snapshot của EBS volume từ US-EAST-1A
2. Khôi phục snapshot đó trong US-EAST-1B

Đây là phương pháp chính để chuyển EBS volume từ AZ này sang AZ khác.

## Các Tính Năng của EBS Snapshot

### 1. EBS Snapshot Archive (Lưu Trữ Snapshot)

**EBS Snapshot Archive** cho phép bạn chuyển snapshots sang "archive tier" để tiết kiệm chi phí.

**Lợi ích:**
- Tiết kiệm đến **75%** chi phí lưu trữ

**Lưu ý:**
- Thời gian khôi phục mất từ **24 đến 72 giờ**
- Không phù hợp cho các yêu cầu truy cập ngay lập tức

### 2. Recycle Bin cho EBS Snapshots (Thùng Rác)

Tính năng **Recycle Bin** bảo vệ chống lại việc xóa snapshots một cách vô tình.

**Cách hoạt động:**
- Các snapshots bị xóa được chuyển vào Recycle Bin thay vì bị xóa vĩnh viễn
- Cho phép khôi phục từ các lần xóa nhầm
- Thời gian lưu trữ có thể cấu hình: **1 ngày đến 1 năm**

### 3. Fast Snapshot Restore (FSR - Khôi Phục Snapshot Nhanh)

**Fast Snapshot Restore** buộc khởi tạo đầy đủ snapshot của bạn để loại bỏ độ trễ khi sử dụng lần đầu.

**Trường hợp sử dụng:**
- Các snapshots lớn cần khởi tạo nhanh
- Khi bạn cần tạo EBS volumes hoặc instances ngay lập tức
- Các workloads quan trọng về thời gian

**Lưu ý quan trọng:**
⚠️ Tính năng này **rất tốn kém** - hãy sử dụng cẩn thận và chỉ khi cần thiết.

## Thực Hành Tốt Nhất

1. **Sao Lưu Định Kỳ**: Tạo snapshots thường xuyên để đảm bảo bảo vệ dữ liệu
2. **Lưu Trữ Snapshots Cũ**: Chuyển các snapshots ít truy cập sang archive tier để tiết kiệm chi phí
3. **Bật Recycle Bin**: Bảo vệ chống lại việc xóa nhầm
4. **Lên Kế Hoạch Sử Dụng FSR**: Chỉ bật Fast Snapshot Restore cho các workloads quan trọng do chi phí cao

## Tóm Tắt

EBS Snapshots cung cấp khả năng sao lưu và chuyển đổi dữ liệu linh hoạt trên hạ tầng AWS. Hiểu rõ các tính năng khác nhau—Archive, Recycle Bin và Fast Snapshot Restore—cho phép bạn tối ưu hóa cả chi phí và hiệu suất dựa trên yêu cầu cụ thể của mình.