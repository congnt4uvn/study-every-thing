# Tổng Quan về Amazon ElastiCache

## Giới Thiệu

Amazon ElastiCache là dịch vụ caching được quản lý giúp bạn triển khai Redis hoặc Memcached một cách dễ dàng. Tương tự như Amazon RDS cung cấp các cơ sở dữ liệu quan hệ được quản lý, ElastiCache cung cấp các công nghệ cache được quản lý.

## Cache là gì?

Cache là **cơ sở dữ liệu trong bộ nhớ (in-memory databases)** với các đặc điểm sau:
- **Hiệu suất cao**
- **Độ trễ thấp**
- Giảm tải cho cơ sở dữ liệu đối với các workload đọc dữ liệu nhiều

### Lợi Ích của ElastiCache

1. **Giảm Tải Cơ Sở Dữ Liệu**: Các truy vấn phổ biến được lưu trong cache, giảm số lần truy vấn trực tiếp vào database
2. **Ứng Dụng Stateless**: Lưu trữ trạng thái ứng dụng trong ElastiCache để làm cho ứng dụng không có trạng thái
3. **Dịch Vụ Được Quản Lý**: AWS xử lý:
   - Bảo trì hệ điều hành
   - Vá lỗi (Patching)
   - Tối ưu hóa
   - Thiết lập và cấu hình
   - Giám sát
   - Khôi phục khi lỗi
   - Sao lưu

### Lưu Ý Quan Trọng

⚠️ **Triển khai yêu cầu thay đổi mã nguồn ứng dụng đáng kể**. Đây không phải là tính năng "bật lên và chạy" đơn giản. Ứng dụng của bạn phải được sửa đổi để truy vấn cache trước hoặc sau khi truy vấn cơ sở dữ liệu.

## Các Kiến Trúc ElastiCache

### 1. Mô Hình Cache-Aside (Lazy Loading)

```
Ứng Dụng → ElastiCache → Cơ Sở Dữ Liệu RDS
```

**Cách hoạt động:**

1. Ứng dụng truy vấn ElastiCache trước
2. **Cache Hit**: Dữ liệu có trong ElastiCache → Trả về dữ liệu ngay lập tức (tiết kiệm một lần truy vấn database)
3. **Cache Miss**: Dữ liệu không có trong cache → Lấy từ cơ sở dữ liệu RDS
4. Ghi dữ liệu đã lấy vào cache cho các truy vấn trong tương lai
5. Giảm tải cho cơ sở dữ liệu RDS

**Lưu Ý Quan Trọng**: Cần có chiến lược invalidation (vô hiệu hóa) cache để đảm bảo chỉ dữ liệu hiện tại được lưu trong cache. Đây là một trong những thách thức chính khi sử dụng công nghệ caching.

### 2. Mô Hình Session Store

**Mục đích**: Làm cho ứng dụng không có trạng thái (stateless)

**Cách hoạt động:**

1. Người dùng đăng nhập vào ứng dụng
2. Ứng dụng ghi dữ liệu session vào ElastiCache
3. Người dùng được chuyển hướng đến instance ứng dụng khác
4. Instance mới lấy dữ liệu session từ ElastiCache
5. Người dùng vẫn đăng nhập mà không cần xác thực lại

Mô hình này cho phép mở rộng theo chiều ngang trong khi vẫn duy trì session người dùng trên nhiều instance ứng dụng.

## So Sánh Redis và Memcached

### Tính Năng của Redis

- ✅ **Multi-Availability Zone** với tự động chuyển đổi dự phòng (auto-failover)
- ✅ **Read Replicas** để mở rộng khả năng đọc và tính sẵn sàng cao
- ✅ **Bền Vững Dữ Liệu** sử dụng AOF (Append-Only File) persistence
- ✅ **Sao Lưu và Khôi Phục**
- ✅ **Cấu Trúc Dữ Liệu Nâng Cao**: Hỗ trợ sets và sorted sets (tuyệt vời cho leaderboards)
- **Kiến Trúc**: Các node Redis sao chép sang các node khác để đảm bảo dự phòng

### Tính Năng của Memcached

- ❌ **Không có High Availability** (phiên bản truyền thống)
- ❌ **Không có Replication** (phiên bản truyền thống)
- ⚠️ **Nguy Cơ Mất Dữ Liệu**: Nếu một node gặp sự cố, dữ liệu cache có thể bị mất
- ✅ **Kiến Trúc Đa Luồng**: Hiệu suất tốt hơn cho một số loại workload
- ⚠️ **Sao Lưu Hạn Chế**: Sao lưu và khôi phục chỉ có trong phiên bản serverless
- **Kiến Trúc**: Nhiều node với sharding/phân vùng dữ liệu

## Điểm Chính Cần Nhớ

- ElastiCache cung cấp dịch vụ Redis và Memcached được quản lý
- Yêu cầu thay đổi mã nguồn ứng dụng để triển khai
- Hai mô hình chính: Cache-Aside và Session Store
- Redis cung cấp nhiều tính năng hơn (HA, replication, persistence)
- Memcached cung cấp kiến trúc sharding đa luồng đơn giản hơn
- Lựa chọn dựa trên trường hợp sử dụng cụ thể và yêu cầu của bạn

## Mẹo Cho Kỳ Thi

Kỳ thi có thể không kiểm tra sâu về so sánh Redis vs Memcached, nhưng hiểu biết về sự khác biệt cơ bản và các trường hợp sử dụng là rất có giá trị cho các tình huống thực tế.