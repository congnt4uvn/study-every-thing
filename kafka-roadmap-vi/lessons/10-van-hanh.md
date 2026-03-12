# Bài 10 — Vận hành: sizing, cấu hình, rebalancing, upgrade

## Mục tiêu
- Hiểu bề mặt vận hành của Kafka
- Nắm các nhóm cấu hình quan trọng nhất
- Hiểu rebalancing và cách lên kế hoạch upgrade ở mức tổng quan

## Sizing (mức tổng quan)
Capacity planning phụ thuộc:
- Throughput (MB/s vào/ra)
- Số partitions và replication factor
- Retention (theo thời gian/dung lượng)
- Kỳ vọng về consumer lag

Cách tiếp cận thực tế:
- Bắt đầu từ ước lượng peak throughput
- Chọn partition count đủ song song
- Kiểm tra ngân sách disk và network

## Các vùng cấu hình quan trọng
Broker-side (ví dụ):
- Log retention và segment
- Replication và ISR
- Network threads và IO threads

Topic-side:
- Partitions và replication factor
- Retention và cleanup policy

Client-side:
- Producer acks/idempotence, batching
- Consumer max poll, commit strategy

## Rebalancing
Rebalance xảy ra khi:
- Consumer join/leave
- Partitions thay đổi
- Sự kiện coordinator

Gợi ý vận hành:
- Giữ consumer ổn định (tránh restart không cần)
- Dùng cooperative rebalancing nếu client hỗ trợ

## Upgrades
Hãy upgrade như hệ production:
- Đọc ghi chú compatibility
- Upgrade theo từng bước
- Monitor controller và replication health

## Lab (local)
Trong lab local, luyện restart an toàn:
1. Start consumer group `demo-group`.
2. Restart consumer và quan sát continuity.
3. Restart Kafka container và quan sát recovery.

## Checklist
- Tôi liệt kê được các yếu tố chính ảnh hưởng sizing
- Tôi hiểu vì sao rebalance xảy ra và vì sao quan trọng
- Tôi mô tả được mindset upgrade thận trọng

## Lỗi hay gặp
- Coi Kafka là “cứ chạy là xong” mà không monitor/backup/plan upgrade
- Over-partition mà không đo tác động
