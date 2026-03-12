# Chiến Lược Caching với AWS ElastiCache

## Tổng Quan

Hướng dẫn này cung cấp kiến thức chuyên sâu về các chiến lược caching khác nhau cho AWS ElastiCache, bao gồm các cân nhắc triển khai và thực tiễn tốt nhất.

## Cache Có An Toàn và Hiệu Quả Không?

### Các Cân Nhắc Về An Toàn

Nhìn chung, caching là an toàn, nhưng có những điều quan trọng cần xem xét:

- **Độ Mới Của Dữ Liệu**: Dữ liệu của bạn có thể đã lỗi thời, dẫn đến tính nhất quán cuối cùng (eventual consistency)
- **Tính Phù Hợp Của Loại Dữ Liệu**: Không phải tập dữ liệu nào cũng phù hợp để cache
- Chỉ cache dữ liệu khi có thể chấp nhận được việc dữ liệu có thể cũ

### Đánh Giá Hiệu Quả

Caching hiệu quả nhất khi:

- ✅ Dữ liệu thay đổi chậm
- ✅ Một vài key được truy cập thường xuyên
- ✅ Cấu trúc key-value hoặc kết quả tổng hợp

Caching kém hiệu quả (anti-patterns):

- ❌ Dữ liệu thay đổi rất nhanh
- ❌ Bạn cần tất cả các key trong dataset thường xuyên
- ❌ Cấu trúc dữ liệu không phù hợp với mẫu truy vấn

### Các Câu Hỏi Quan Trọng

1. **Có an toàn khi cache dữ liệu này không?**
2. **Caching có hiệu quả với dữ liệu này không?**
3. **Dữ liệu đã được cấu trúc đúng cách cho caching chưa?**
4. **Mẫu thiết kế caching nào phù hợp nhất?**

## Chiến Lược Caching 1: Lazy Loading

**Còn được gọi là**: Cache-Aside, Lazy Population

### Cách Hoạt Động

1. **Cache Hit**: Ứng dụng yêu cầu dữ liệu → ElastiCache có dữ liệu → Trả về ngay lập tức
2. **Cache Miss**: Ứng dụng yêu cầu dữ liệu → ElastiCache không có → Đọc từ database (RDS) → Ghi vào cache → Trả về dữ liệu

### Luồng Kiến Trúc

```
Ứng dụng → ElastiCache (Cache Miss) 
        → Amazon RDS (Đọc) 
        → ElastiCache (Ghi) 
        → Trả về Dữ liệu
```

### Ưu Điểm

- ✅ **Hiệu Quả**: Chỉ cache dữ liệu được yêu cầu
- ✅ **Không Gây Lỗi Nghiêm Trọng**: Nếu cache bị lỗi, hệ thống vẫn hoạt động (với độ trễ tăng)
- ✅ **Tự Phục Hồi**: Cache tự động làm ấm khi có requests

### Nhược Điểm

- ❌ **Phạt Cache Miss**: Ba lượt đi về (app → cache → database → cache)
- ❌ **Trải Nghiệm Người Dùng**: Độ trễ đáng chú ý khi cache miss
- ❌ **Dữ Liệu Cũ**: Cập nhật trong RDS không tự động cập nhật cache

### Ví Dụ Pseudocode

```python
def get_user(user_id):
    # Kiểm tra cache trước
    record = cache.get(user_id)
    
    if record is None:
        # Cache miss - truy vấn database
        record = db.query("SELECT * FROM users WHERE id = ?", user_id)
        
        # Điền vào cache
        cache.set(user_id, record)
    
    return record

# Cách sử dụng
user = get_user(17)
```

## Chiến Lược Caching 2: Write Through

### Cách Hoạt Động

- Ứng dụng ghi vào database
- Đồng thời ghi vào cache
- Các lần đọc luôn trúng dữ liệu mới trong cache

### Luồng Kiến Trúc

```
Ứng dụng → Amazon RDS (Ghi) 
        → ElastiCache (Ghi)
        
Ứng dụng → ElastiCache (Đọc - Cache Hit)
```

### Ưu Điểm

- ✅ **Không Bao Giờ Cũ**: Dữ liệu trong cache luôn cập nhật
- ✅ **Kỳ Vọng Người Dùng**: Người dùng mong đợi ghi chậm hơn đọc
- ✅ **Hiệu Suất Đọc**: Tất cả các lần đọc đều nhanh (cache hits)

### Nhược Điểm

- ❌ **Phạt Ghi**: Hai lần gọi mỗi lần ghi (database + cache)
- ❌ **Thiếu Dữ Liệu**: Cache không có dữ liệu cho đến khi nó được ghi vào database
- ❌ **Cache Churn**: Có thể cache dữ liệu không bao giờ được đọc (lãng phí không gian)

### Ví Dụ Pseudocode

```python
def save_user(user_id, values):
    # Lưu vào database trước
    record = db.query("UPDATE users ... ", user_id, values)
    
    # Cập nhật cache
    cache.set(user_id, record)
    
    return record
```

### Thực Tiễn Tốt Nhất: Kết Hợp Các Chiến Lược

Kết hợp Write Through với Lazy Loading để xử lý các trường hợp dữ liệu bị thiếu.

## Cache Eviction và Time-to-Live (TTL)

### Các Trigger Xóa Cache

1. **Xóa Rõ Ràng**: Xóa items thủ công
2. **Bộ Nhớ Đầy**: Các items Ít Được Sử Dụng Gần Đây nhất (LRU) bị xóa
3. **Hết Hạn TTL**: Items hết hạn sau thời gian đặt

### Chiến Lược TTL

- Hiệu quả cho: Bảng xếp hạng, Bình luận, Luồng hoạt động
- Phạm vi: Vài giây đến hàng giờ hoặc ngày
- Ngay cả TTL ngắn (vài giây) cũng có thể rất hiệu quả cho dữ liệu được truy cập thường xuyên

### Khi Nào Cần Scale

Nếu bạn gặp quá nhiều evictions:
- Scale up: Tăng kích thước node
- Scale out: Thêm nhiều nodes hơn

## Thực Tiễn Tốt Nhất và Khuyến Nghị

### 1. Bắt Đầu Với Lazy Loading
- Dễ triển khai
- Hoạt động như một nền tảng vững chắc
- Cải thiện hiệu suất đọc trong hầu hết các tình huống

### 2. Thêm Write Through Như Một Tối Ưu Hóa
- Triển khai sau Lazy Loading
- Sử dụng để giảm tính cũ của cache
- Thường không phải là chiến lược độc lập

### 3. Triển Khai TTL Một Cách Khôn Ngoan
- Sử dụng TTL trong hầu hết các trường hợp (trừ Write Through thuần túy)
- Đặt giá trị hợp lý cho ứng dụng của bạn
- Cân bằng giữa độ mới và hiệu suất

### 4. Cache Có Chọn Lọc
- ✅ Ứng viên tốt: Hồ sơ người dùng, blogs, danh mục sản phẩm
- ❌ Ứng viên kém: Dữ liệu giá cả, số dư tài khoản ngân hàng, dữ liệu thời gian thực quan trọng

## Suy Nghĩ Cuối Cùng

> "Có hai điều khó khăn trong Khoa học Máy tính: vô hiệu hóa cache và đặt tên cho mọi thứ."

Caching rất phức tạp và đầy thách thức. Hướng dẫn này bao gồm các kiến thức cơ bản cần thiết cho các kỳ thi chứng chỉ AWS, nhưng caching là cả một lĩnh vực của Khoa học Máy tính.

### Trọng Tâm Kỳ Thi

Đối với các kỳ thi AWS, cần hiểu:
- Các chiến lược caching khác nhau (Lazy Loading, Write Through)
- Các mẫu pseudocode
- Đánh đổi và ý nghĩa của từng phương pháp

---

**Điểm Chính**: Chọn chiến lược caching dựa trên trường hợp sử dụng cụ thể, đặc điểm dữ liệu và yêu cầu hiệu suất của bạn.