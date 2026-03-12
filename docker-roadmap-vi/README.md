# Lộ trình Docker Từ Số 0 → Thành Thạo

Một kế hoạch học thực hành để nắm Docker từ nền tảng đến quy trình dùng thực tế.

## Dành cho ai
- Lập trình viên muốn môi trường dev local nhất quán
- Người mới DevOps/SRE cần kiến thức container để dùng trong pipeline triển khai
- Bất kỳ ai muốn *hiểu* Docker đang làm gì (không chỉ copy/paste lệnh)

## Cách học theo lộ trình
- Học theo thứ tự bài.
- Mỗi bài gồm:
  - **Mục tiêu** (làm được gì)
  - **Khái niệm** (hiểu được gì)
  - **Lab thực hành** (lệnh + kết quả mong đợi)
  - **Checklist** (tự kiểm tra nhanh)
- Ghi lại lỗi bạn gặp và cách sửa; kỹ năng Docker lên nhanh nhất khi bạn debug.

## Điều kiện trước
- Biết dùng terminal cơ bản (PowerShell hoặc Bash)
- Biết căn bản một ngôn ngữ/app bất kỳ (Node/Python/.NET/Java...)

## Lịch học gợi ý
- **Nhanh (1 tuần):** 1–2 bài/ngày + capstone cuối tuần
- **Đều (2–3 tuần):** 3–5 bài/tuần + lặp lại lab tới khi “thuộc tay”

## Danh sách bài học
1. [Bài 01 — Docker là gì + cài đặt + container đầu tiên](lessons/01-docker-la-gi.md)
2. [Bài 02 — Khái niệm lõi: image, container, layer, registry](lessons/02-khai-niem-loi.md)
3. [Bài 03 — Vòng đời container + CLI thiết yếu](lessons/03-cli-va-vong-doi.md)
4. [Bài 04 — Thực hành image: pull, tag, inspect, push](lessons/04-thuc-hanh-image.md)
5. [Bài 05 — Nền tảng Dockerfile](lessons/05-dockerfile-co-ban.md)
6. [Bài 06 — Build tốt hơn: cache, .dockerignore, multi-stage](lessons/06-build-tot-hon.md)
7. [Bài 07 — Dữ liệu: volume, bind mount, quyền truy cập](lessons/07-volume-va-mount.md)
8. [Bài 08 — Networking: ports, DNS, bridge network](lessons/08-networking-co-ban.md)
9. [Bài 09 — Docker Compose căn bản](lessons/09-compose-can-ban.md)
10. [Bài 10 — Mẫu Compose: dev/prod, env, healthcheck](lessons/10-compose-pattern.md)
11. [Bài 11 — Debug & troubleshooting](lessons/11-debug.md)
12. [Bài 12 — Bảo mật cơ bản: least privilege, secrets, scanning](lessons/12-bao-mat-co-ban.md)
13. [Bài 13 — Capstone: containerize app + publish image](lessons/13-capstone.md)

## “Thành thạo” nghĩa là gì
Bạn được xem là dùng Docker tốt khi có thể:
- Viết Dockerfile build nhanh, image nhỏ
- Dùng Compose chạy hệ nhiều service local
- Debug lỗi thường gặp (port, mount, DNS, permission)
- Push image có version lên registry và giải thích được nó chứa gì

## Bước tiếp theo (tuỳ chọn)
- Tìm hiểu OCI và mối liên hệ giữa Docker và containerd
- Học Kubernetes cơ bản (deployments, services, ingress)
- Đi sâu security supply-chain (SBOM, signing, SLSA)
