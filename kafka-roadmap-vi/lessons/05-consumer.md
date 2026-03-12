# Bài 05 — Consumer: group, offset, delivery semantics

## Mục tiêu
- Hiểu consumer group và song song
- Hiểu offset và commit
- Hiểu at-most-once vs at-least-once vs effectively-once

## Consumer groups
**Consumer group** là tập consumer cùng chia việc đọc một topic.

Quy tắc:
- Song song tối đa cho một topic = số partitions
- Mỗi partition chỉ do tối đa một consumer trong cùng group đọc tại một thời điểm

## Offsets
**Offset** là vị trí record trong một partition.

Consumer theo dõi tiến độ bằng cách commit offsets.

2 kiểu commit phổ biến:
- Auto-commit (đơn giản, rủi ro cho correctness)
- Manual commit sau khi xử lý (kiểm soát tốt hơn)

## Delivery semantics (thực tế)
### At-most-once
Commit trước khi xử lý.
- Nhanh
- Có thể mất message khi lỗi

### At-least-once
Xử lý rồi mới commit.
- Không mất (giả sử retry)
- Có thể duplicate (cần idempotency ở downstream)

### Effectively-once (ở mức ứng dụng)
Với idempotent writes / dedupe keys / transactional patterns, bạn có thể đạt kết quả “gần như đúng một lần”.

## Rebalancing
Khi thành viên group thay đổi (consumer join/leave), Kafka phân bổ lại partitions.

Triệu chứng:
- Tạm dừng xử lý
- Có thể xử lý trùng nếu commit sai

## Lab thực hành
1. Consume từ đầu:
```powershell
docker exec -it $(docker ps -q --filter "name=kafka") bash -lc "kafka-console-consumer --bootstrap-server kafka:29092 --topic demo.orders --from-beginning --group demo-group"
```

2. Ở terminal khác, produce thêm vài message.

3. Stop consumer và start lại cùng group.
   - Quan sát: nó tiếp tục từ offsets đã commit.

## Checklist
- Tôi giải thích được consumer group và partition assignment
- Tôi hiểu offset và commit
- Tôi chọn at-most-once vs at-least-once có chủ đích

## Lỗi hay gặp
- Nghĩ duplicate là “không thể” (thực tế có)
- Nghĩ rebalances hiếm (môi trường động sẽ gặp thường)
