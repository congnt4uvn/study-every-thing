# Tối Ưu Hóa Hiệu Suất Amazon S3

## Hiệu Suất Cơ Bản của S3

Amazon S3 tự động mở rộng để xử lý số lượng yêu cầu rất cao với các đặc tính hiệu suất vượt trội:

### Chỉ Số Hiệu Suất

- **Độ trễ**: 100-200 milliseconds để lấy byte đầu tiên từ S3
- **Giới hạn yêu cầu trên mỗi Prefix**:
  - 3,500 yêu cầu PUT/COPY/POST/DELETE mỗi giây
  - 5,500 yêu cầu GET/HEAD mỗi giây
- **Không giới hạn** số lượng prefix trong bucket của bạn

### Hiểu về Prefix

Prefix là đường dẫn giữa tên bucket và tên object. Dưới đây là một số ví dụ:

| Đường dẫn Object | Prefix |
|-----------------|--------|
| `bucket/folder1/sub1/file` | `/folder1/sub1` |
| `bucket/folder1/sub2/file` | `/folder1/sub2` |
| `bucket/folder2/sub1/file` | `/folder2/sub1` |
| `bucket/folder2/sub2/file` | `/folder2/sub2` |

**Ví dụ**: Nếu bạn phân tán các yêu cầu đọc đều trên bốn prefix khác nhau, bạn có thể đạt được **22,000 yêu cầu mỗi giây** cho các thao tác GET/HEAD.

## Các Kỹ Thuật Tối Ưu Hóa Hiệu Suất S3

### 1. Multi-Part Upload (Tải lên Đa phần)

Multi-part upload cho phép bạn tải lên các file lớn thành nhiều phần song song, tối đa hóa việc sử dụng băng thông.

**Khi nào nên sử dụng**:
- **Khuyến nghị** cho các file trên 100 MB
- **Bắt buộc** cho các file trên 5 GB

**Cách hoạt động**:
1. Chia file lớn thành các phần nhỏ hơn
2. Tải lên từng phần song song lên Amazon S3
3. S3 tự động ghép các phần lại thành file hoàn chỉnh

**Lợi ích**:
- Tải lên song song
- Tốc độ truyền tải nhanh hơn
- Tận dụng băng thông tốt hơn

### 2. S3 Transfer Acceleration (Tăng tốc truyền tải S3)

Transfer Acceleration tăng tốc độ truyền file bằng cách định tuyến dữ liệu qua các edge location của AWS.

**Tính năng chính**:
- Hoạt động cho cả tải lên và tải xuống
- Sử dụng mạng riêng của AWS để truyền tải nhanh hơn
- Tương thích với multi-part upload
- Hơn 200 edge location trên toàn thế giới

**Cách hoạt động**:

```
USA (File) → Edge Location (USA) → [Mạng riêng AWS] → S3 Bucket (Úc)
     ↑                                                        ↑
  Tải lên nhanh                                      Truyền tải nhanh
 (Internet công cộng)                                 (Mạng riêng)
```

**Lợi ích**:
- Giảm thiểu sử dụng internet công cộng
- Tối đa hóa sử dụng mạng riêng AWS
- Nhanh hơn đáng kể cho các truyền tải khoảng cách xa

### 3. S3 Byte-Range Fetches (Lấy dữ liệu theo phạm vi Byte)

Byte-Range Fetches cho phép bạn tải xuống các phạm vi byte cụ thể của file một cách song song.

**Trường hợp sử dụng**:

#### Tăng tốc tải xuống
- Yêu cầu các phạm vi byte khác nhau song song
- Song song hóa các yêu cầu GET để tải xuống nhanh hơn
- Khả năng phục hồi tốt hơn: chỉ thử lại các phạm vi byte bị lỗi

**Ví dụ**:
```
File lớn trong S3
├── Phần 1 (bytes 0-1000) ──┐
├── Phần 2 (bytes 1001-2000) ├──→ Tải xuống song song
└── Phần 3 (bytes 2001-3000) ┘
```

#### Lấy dữ liệu một phần
- Chỉ yêu cầu dữ liệu bạn cần
- Ví dụ: Chỉ lấy phần header của file (50 bytes đầu tiên)
- Thời gian phản hồi nhanh hơn cho các truy vấn metadata

## Tóm tắt

Amazon S3 cung cấp nhiều kỹ thuật tối ưu hóa:

1. **Multi-Part Upload**: Song song hóa việc tải lên cho các file lớn
2. **Transfer Acceleration**: Sử dụng edge location để truyền tải toàn cầu nhanh hơn
3. **Byte-Range Fetches**: Song song hóa tải xuống và lấy dữ liệu một phần

Các kỹ thuật này giúp bạn tối đa hóa hiệu suất S3 cho cả tải lên và tải xuống trong khi vẫn tuân thủ các giới hạn hiệu suất.

---

**Lưu ý**: Hãy chắc chắn bạn hiểu các khái niệm này cho các kỳ thi chứng chỉ AWS.