# Oracle Database — Tài liệu thực hành (Tiếng Việt)

Tài liệu này là bản tổng quan thực hành theo góc nhìn phỏng vấn và vận hành (DBA/engineering) về Oracle Database.

## 1) Oracle Database là gì?
- Là hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) với SQL là ngôn ngữ truy vấn chính và PL/SQL là phần mở rộng thủ tục.
- Hỗ trợ giao dịch ACID, cơ chế đa phiên bản (MVCC/read consistency), các lựa chọn HA/DR (RAC, Data Guard) và backup/recovery chuẩn doanh nghiệp (RMAN).

## 2) Thuật ngữ cốt lõi
- **Database**: các file vật lý (datafiles, control files, online redo logs).
- **Instance**: bộ nhớ + các tiến trình nền (SGA + processes) truy cập database.
- **Schema**: không gian logic thuộc một user; chứa object (tables, views, procedures).
- **Tablespace**: lớp lưu trữ logic ánh xạ tới một/nhiều datafile.
- **Segment / Extent / Block**: đơn vị cấp phát lưu trữ (segment là vùng của object; extent là “miếng” cấp phát; block là đơn vị nhỏ nhất).

## 3) Tổng quan kiến trúc
### 3.1 Bộ nhớ
- **SGA (chia sẻ)**
  - Buffer Cache: cache data block
  - Shared Pool: library cache + dictionary cache
  - Redo Log Buffer: chứa redo trước khi ghi ra redo log
  - Tuỳ chọn: Large Pool, Java Pool, vùng In-Memory
- **PGA (theo process)**
  - Session memory, private SQL area, work areas (sort/hash)

### 3.2 Background processes (phổ biến)
- **DBWn**: ghi dirty buffer ra datafile
- **LGWR**: ghi redo vào online redo log
- **CKPT**: báo checkpoint và cập nhật header
- **SMON**: instance recovery
- **PMON**: dọn dẹp session chết
- **ARCn**: archive redo log (khi ARCHIVELOG)

## 4) Lưu trữ vật lý và các file
- **Datafiles**: chứa data block của user và dictionary.
- **Control files**: metadata quan trọng (tên file, checkpoint SCN, redo history). Nên multiplex.
- **Online redo logs**: redo hiện tại; tổ chức theo group/member.
- **Archived redo logs**: bản sao redo log đã đầy (phục vụ recovery / Data Guard).
- **Undo tablespace**: undo segment phục vụ read consistency và rollback.
- **Temp tablespace**: sort, hash và các thao tác spill.

## 5) Lưu trữ logic: tablespace và object
- **Loại tablespace**: permanent, undo, temporary.
- **Locally managed tablespaces** là chuẩn; extent được quản lý bằng bitmap.
- **Bigfile tablespace**: một datafile rất lớn (lựa chọn quản trị).

## 6) Multitenant (CDB/PDB) cơ bản
- **CDB (container database)** gồm:
  - CDB$ROOT (root)
  - PDB$SEED (template)
  - Nhiều **PDB** (pluggable database)
- Lợi ích: gom cụm, cấp phát nhanh, clone thuận tiện, kiểm soát tài nguyên theo PDB.

## 7) SQL thiết yếu (một số điểm Oracle)
### 7.1 Thực thi và tối ưu
- Oracle dùng **cost-based optimizer (CBO)**.
- Dùng **bind variables** để reuse cursor và giảm hard parse.
- Khi troubleshoot, ưu tiên xem **actual plan**:
  - `DBMS_XPLAN.DISPLAY_CURSOR` (có row count thực tế và runtime statistics khi bật)

### 7.2 Một số cấu trúc hay dùng
- **Analytic functions**: `ROW_NUMBER() OVER (...)`, `SUM(...) OVER (...)` để ranking và running total.
- Phân trang (12c+):
  ```sql
  SELECT *
  FROM   t
  ORDER  BY created_at DESC
  OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY;
  ```

## 8) Giao dịch, khoá và read consistency
- Oracle cung cấp **read consistency** dựa trên UNDO (query nhìn snapshot nhất quán).
- DML thường đặt **row-level lock**; đồng thời có TM lock để phối hợp.
- **Deadlock** được phát hiện và báo lỗi (ORA-00060); một statement bị rollback để phá vòng.
- ORA-01555 “snapshot too old” thường do áp lực undo hoặc query quá lâu.

## 9) Index và access path
- **B-tree index**: phù hợp OLTP và cột cardinality cao.
- **Bitmap index**: phù hợp phân tích/cardinality thấp; tránh với bảng DML nhiều.
- **Composite index**: thứ tự cột quan trọng; “leading columns” ảnh hưởng khả năng dùng.
- **Function-based index**: index trên biểu thức dùng trong predicate.
- Nên cân nhắc index **foreign key** để giảm locking và tăng tốc update/delete ở parent.

## 10) Partitioning (hiệu năng + quản trị)
- Các kiểu phổ biến: **range**, **list**, **hash**, và **composite**.
- Lợi ích chính: **partition pruning** (chỉ đọc partition liên quan).
- Index có thể là **local** (theo partition) hoặc **global** (trải nhiều partition).

## 11) Chẩn đoán hiệu năng (xem gì?)
### 11.1 Nguồn dữ liệu thường dùng
- **AWR/ASH**: báo cáo lịch sử và lấy mẫu session active.
- Dynamic views:
  - `V$SESSION`, `V$SQL`, `V$SQLAREA`, `V$SYSTEM_EVENT`, `V$ACTIVE_SESSION_HISTORY` (một số tính năng có thể liên quan license)

### 11.2 Quy trình troubleshoot thực tế
1. Xác định đúng SQL và giá trị bind.
2. Kiểm tra plan (estimated vs actual), chú ý sai lệch cardinality.
3. Kiểm tra waits (I/O, locks, CPU, network).
4. Xác minh optimizer stats (stale/missing/skew).
5. Rà soát index/partitioning và cách viết SQL.
6. Nếu có regression, cân nhắc công cụ ổn định plan (ví dụ SPM).

## 12) Backup và recovery (RMAN)
- **RMAN** là công cụ backup/recovery chuẩn của Oracle (incremental, validation, encryption).
- Khái niệm:
  - **RESTORE**: khôi phục file từ backup về disk
  - **RECOVER**: apply redo để đạt mục tiêu time/SCN
  - Incremental: level 0 (base) và level 1 (differential/cumulative)
- Khuyến nghị:
  - Bật **CONTROLFILE AUTOBACKUP**
  - Định kỳ **VALIDATE** backup
  - Đồng bộ retention của backup + archive logs theo mục tiêu RPO/RTO

## 13) High availability và disaster recovery
- **Data Guard**: primary + standby dùng redo transport/apply
  - Physical standby (redo apply) vs logical standby (SQL apply)
  - Switchover (có kế hoạch) vs failover (sự cố)
- **RAC**: nhiều instance trên shared storage để HA ở mức instance và mở rộng
- **Flashback**:
  - Flashback Query (AS OF)
  - Flashback Database (rewind DB khi đã bật)

## 14) Bảo mật cơ bản
- Quyền:
  - **System privileges** (ví dụ tạo object)
  - **Object privileges** (ví dụ select trên table)
  - **Roles** gom nhóm quyền
- Chính sách:
  - **Profiles** cho mật khẩu và giới hạn tài nguyên
  - **Auditing** (Unified Auditing)
  - **TDE** mã hoá dữ liệu at rest
  - **VPD/FGAC** bảo mật theo dòng

## 15) Kết nối và services
- **Listener** nhận request kết nối và chuyển tới server process.
- Dùng **services** để biểu diễn workload (đặc biệt RAC), hỗ trợ load balancing/failover.
- Ứng dụng nên dùng **connection pooling**.

## 16) Checklist bảo trì định kỳ
- Theo dõi tablespace usage, FRA (nếu dùng), và tốc độ sinh archive log.
- Giữ statistics mới (auto stats task; `DBMS_STATS` khi cần).
- Xem alert log/trace để phát hiện lỗi lặp.
- Kiểm tra backup và diễn tập recovery.
- Lập kế hoạch patch: test ở môi trường thấp; theo dõi thay đổi optimizer.

## 17) Một số lỗi thường gặp (gợi ý mức cao)
- **ORA-01555**: undo bị ghi đè; tune query và/hoặc tăng undo retention/size.
- **ORA-04031**: thiếu shared pool; giảm hard parse, tune/size shared pool.
- **ORA-00060**: deadlock; thống nhất thứ tự locking, index FK.
- **ORA-12514**: listener không biết service; kiểm tra service registration và connect descriptor.

## 18) Tham khảo nhanh: một số query hữu ích
> Đây là ví dụ; cần điều chỉnh theo version và quyền.

- Danh sách session (mức cơ bản):
  ```sql
  SELECT sid, serial#, username, status, sql_id, event
  FROM   v$session
  WHERE  type = 'USER';
  ```

- Top SQL theo elapsed time (ý tưởng cơ bản):
  ```sql
  SELECT sql_id, elapsed_time/1e6 AS elapsed_s, executions
  FROM   v$sql
  ORDER  BY elapsed_time DESC
  FETCH FIRST 20 ROWS ONLY;
  ```

- Dung lượng datafile theo tablespace (đơn giản):
  ```sql
  SELECT tablespace_name,
         ROUND(SUM(bytes)/1024/1024) AS mb
  FROM   dba_data_files
  GROUP  BY tablespace_name;
  ```

## 19) Lưu ý về edition và licensing
Một số tính năng/chẩn đoán (AWR/ASH, partitioning, RAC, một số security options) có thể cần license/edition riêng. Luôn xác nhận phạm vi được phép trong môi trường của bạn.
