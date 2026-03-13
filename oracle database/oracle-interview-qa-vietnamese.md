# Câu hỏi & Trả lời phỏng vấn Oracle Database (Tiếng Việt)

> 100 câu hỏi phỏng vấn thực tế kèm trả lời ngắn gọn.

1. **Hỏi: Khác nhau giữa *instance* và *database* trong Oracle là gì?**
   **Đáp:** *Instance* là bộ nhớ + các tiến trình nền (SGA + processes). *Database* là các file vật lý (datafiles, control files, redo logs). Một database có thể được mở bởi một instance (single-instance) hoặc nhiều instance (RAC).

2. **Hỏi: Các thành phần chính của SGA gồm những gì?**
   **Đáp:** Thường gồm Database Buffer Cache, Shared Pool (Library Cache + Data Dictionary Cache), Redo Log Buffer, Large Pool, Java Pool và (tuỳ chọn) vùng In-Memory.

3. **Hỏi: PGA là gì và chứa những gì?**
   **Đáp:** PGA là bộ nhớ theo từng process (không chia sẻ). Chứa session memory, private SQL area và work areas cho sort/hash join (phụ thuộc cấu hình PGA; có thể spill ra TEMP).

4. **Hỏi: Kể tên các background process quan trọng và nhiệm vụ của chúng.**
   **Đáp:** DBWn ghi dirty buffer ra datafiles; LGWR ghi redo vào online redo logs; CKPT báo checkpoint và cập nhật header; SMON recovery instance; PMON dọn dẹp session chết; ARCn archive redo (khi ARCHIVELOG).

5. **Hỏi: Control file là gì và lưu thông tin gì?**
   **Đáp:** Control file lưu metadata quan trọng để startup/open DB: tên DB, danh sách file, checkpoint SCN, lịch sử redo, thông tin backup. Rất quan trọng và nên nhân bản (multiplex).

6. **Hỏi: Online redo log khác archived redo log thế nào?**
   **Đáp:** Online redo log chứa redo của hoạt động hiện tại; LGWR ghi vào đây. Archived log là bản sao của redo log group đã đầy do ARCn tạo ra trong ARCHIVELOG, dùng cho media recovery và Data Guard.

7. **Hỏi: Checkpoint là gì và vì sao quan trọng?**
   **Đáp:** Checkpoint là lúc Oracle đảm bảo dirty buffer được ghi ra đĩa và header file được cập nhật checkpoint SCN. Nó giảm thời gian crash recovery vì phải apply ít redo hơn.

8. **Hỏi: SCN là gì và được dùng ở đâu?**
   **Đáp:** SCN (System Change Number) là “mốc thời gian” logic. Dùng cho read consistency, recovery, checkpoint và đồng bộ Data Guard.

9. **Hỏi: Giải thích read consistency (Oracle MVCC) ở mức khái quát.**
   **Đáp:** Mỗi câu query thấy một “snapshot” nhất quán theo SCN. Nếu dữ liệu bị thay đổi trong lúc query chạy, Oracle dùng UNDO để dựng lại phiên bản cũ, tránh đọc dữ liệu dở dang.

10. **Hỏi: UNDO và TEMP tablespace dùng để làm gì?**
   **Đáp:** UNDO lưu before-image phục vụ read consistency và rollback. TEMP dùng cho sort/hash work area khi vượt bộ nhớ (sort lớn, hash join), và một số nhu cầu temporary segment khác.

11. **Hỏi: CDB/PDB trong kiến trúc multitenant khác nhau thế nào?**
   **Đáp:** CDB (Container DB) gồm root (CDB$ROOT), seed (PDB$SEED) và nhiều PDB. PDB là “DB logic” tách biệt tương đối nhưng cùng chia sẻ một Oracle instance.

12. **Hỏi: Tablespace là gì và vì sao dùng tablespace?**
   **Đáp:** Tablespace là lớp lưu trữ logic ánh xạ đến một hoặc nhiều datafile. Giúp quản trị phân bổ, backup/recovery và tách biệt quản trị theo nhóm dữ liệu.

13. **Hỏi: Các loại tablespace phổ biến là gì?**
   **Đáp:** Permanent (table/index), Temporary (sort/work), Undo (undo segments). Thường là locally managed; có thể gặp bigfile tablespace.

14. **Hỏi: Data dictionary là gì?**
   **Đáp:** Kho metadata mô tả object, user, privilege, storage. DBA thường truy vấn các view như `DBA_TABLES`, `DBA_INDEXES`, `DBA_USERS`.

15. **Hỏi: Dynamic performance views (V$ views) là gì?**
   **Đáp:** Các view (dựa trên fixed tables X$) cung cấp thông tin runtime của instance, ví dụ `V$SESSION`, `V$SQL`, `V$SYSTEM_EVENT`, `V$DATABASE`.

16. **Hỏi: Bind variable là gì và tại sao quan trọng?**
   **Đáp:** Là placeholder trong SQL (ví dụ `:id`). Giúp reuse cursor, giảm hard parse, tăng hiệu năng và khả năng mở rộng.

17. **Hỏi: Hard parse khác soft parse như thế nào?**
   **Đáp:** Hard parse tạo cursor mới (parse/optimize/allocate) tốn kém. Soft parse tái sử dụng cursor sẵn có trong shared pool nên nhẹ hơn nhiều.

18. **Hỏi: Cursor sharing là gì và khi nào gây vấn đề?**
   **Đáp:** Là cơ chế tái sử dụng SQL đã parse. Nếu SQL dùng literal đa dạng sẽ nổ số lượng cursor; ép chia sẻ (forced matching) có thể giảm parse nhưng đôi khi tạo plan không tối ưu khi dữ liệu bị skew.

19. **Hỏi: Theo logic, Oracle xử lý SELECT theo thứ tự nào?**
   **Đáp:** Về mặt khái niệm: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `FETCH/OFFSET` (kế hoạch thực thi thực tế có thể khác).

20. **Hỏi: INNER JOIN khác OUTER JOIN thế nào?**
   **Đáp:** INNER JOIN chỉ trả về dòng khớp. LEFT/RIGHT/FULL OUTER JOIN trả về cả dòng không khớp từ một/hai phía (cột phía kia sẽ là NULL).

21. **Hỏi: `IN` khác `EXISTS` như thế nào?**
   **Đáp:** `IN` so với danh sách/kết quả subquery; `EXISTS` chỉ kiểm tra có ít nhất một dòng. `EXISTS` thường tốt cho kiểm tra tương quan; semantics với NULL cũng khác.

22. **Hỏi: Correlated subquery là gì?**
   **Đáp:** Subquery tham chiếu cột của outer query và (về logic) được đánh giá theo từng dòng outer, ví dụ `WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.k=t1.k)`.

23. **Hỏi: Analytic (window) functions là gì và vì sao dùng?**
   **Đáp:** Ví dụ `ROW_NUMBER() OVER (...)` tính toán trên “cửa sổ” dòng mà không gom dòng như `GROUP BY`. Rất hữu ích cho ranking, running total, top-N theo nhóm.

24. **Hỏi: Khác nhau giữa `ROW_NUMBER`, `RANK`, `DENSE_RANK`?**
   **Đáp:** `ROW_NUMBER` đánh số duy nhất. `RANK` cho các dòng hoà (tie) cùng hạng và để khoảng trống. `DENSE_RANK` cũng cho tie cùng hạng nhưng không tạo khoảng trống.

25. **Hỏi: Phân trang (pagination) trong Oracle (12c+) làm thế nào?**
   **Đáp:** Dùng `OFFSET :n ROWS FETCH NEXT :m ROWS ONLY` kèm `ORDER BY` có tính xác định. Phiên bản cũ dùng `ROWNUM` trong subquery.

26. **Hỏi: `MERGE` dùng để làm gì?**
   **Đáp:** Thực hiện insert/update (và tuỳ chọn delete) theo điều kiện match trong một câu lệnh—hay dùng cho upsert.

27. **Hỏi: `DELETE` khác `TRUNCATE` thế nào?**
   **Đáp:** `DELETE` là DML (ghi undo/redo, có thể rollback). `TRUNCATE` là DDL (thu hồi extent, logging tối thiểu, không rollback).

28. **Hỏi: Constraint khác index như thế nào?**
   **Đáp:** Constraint đảm bảo quy tắc dữ liệu (PK/UK/FK/CHECK/NOT NULL). Index chủ yếu để tăng tốc truy vấn. Oracle thường tạo index hỗ trợ cho PK/UK nhưng không tự tạo cho FK.

29. **Hỏi: Vì sao thường khuyến nghị index cho foreign key?**
   **Đáp:** FK không có index dễ gây locking/contention và chậm khi update/delete ở parent, đôi khi dẫn đến table lock khi kiểm tra ràng buộc.

30. **Hỏi: Deferrable constraint là gì?**
   **Đáp:** Constraint có thể trì hoãn kiểm tra đến lúc COMMIT (`DEFERRABLE INITIALLY DEFERRED`), giúp làm batch phức tạp nhưng vẫn đảm bảo toàn vẹn tại thời điểm commit.

31. **Hỏi: B-tree index khác bitmap index thế nào?**
   **Đáp:** B-tree phù hợp cardinality cao và OLTP. Bitmap phù hợp cardinality thấp và workload phân tích, nhưng dễ gây locking vấn đề nếu DML nhiều.

32. **Hỏi: Function-based index là gì và khi nào hữu ích?**
   **Đáp:** Index trên biểu thức (ví dụ `UPPER(email)`). Hữu ích khi query filter theo biểu thức, giúp dùng index thay vì full scan.

33. **Hỏi: Composite index là gì và quy tắc “leading column” là gì?**
   **Đáp:** Index nhiều cột. Oracle dùng hiệu quả khi predicate có chứa cột đầu (leading columns); nếu thiếu có thể bị hạn chế (dù skip-scan đôi khi hỗ trợ).

34. **Hỏi: Clustering factor của index là gì và vì sao quan trọng?**
   **Đáp:** Đo mức độ “cùng thứ tự” giữa index và bảng. Clustering factor thấp giúp index range scan hiệu quả; cao khiến truy cập bảng qua index tốn I/O.

35. **Hỏi: `EXPLAIN PLAN` khác xem actual runtime plan thế nào?**
   **Đáp:** `EXPLAIN PLAN` chỉ là ước lượng và không chạy câu lệnh. Actual plan (ví dụ `DBMS_XPLAN.DISPLAY_CURSOR`) có row count thực tế, quyết định adaptive và thống kê runtime (khi bật).

36. **Hỏi: Optimizer statistics là gì và thu thập thế nào?**
   **Đáp:** Stats mô tả phân phối dữ liệu (row count, NDV, histogram). Thu thập bằng `DBMS_STATS.GATHER_TABLE_STATS` (hoặc auto task). Stats mới giúp chọn plan tốt.

37. **Hỏi: Histogram là gì và khi nào cần?**
   **Đáp:** Histogram mô tả phân phối skew để ước lượng selectivity chính xác hơn. Hữu ích khi cột lọc không phân bố đều và plan phụ thuộc mạnh vào selectivity.

38. **Hỏi: Shared pool là gì và nguyên nhân phổ biến gây vấn đề shared pool?**
   **Đáp:** Shared pool cache SQL/PLSQL đã parse và metadata dictionary. Parse quá nhiều, SQL duy nhất quá nhiều, hoặc object lớn gây áp lực bộ nhớ, có thể dẫn đến ORA-04031.

39. **Hỏi: Các bước cơ bản để xử lý SQL chậm là gì?**
   **Đáp:** Xác định đúng SQL + bind, kiểm tra plan và ước lượng, xác định wait events, xác minh stats, xem index/partitioning, và so sánh với baseline tốt trước đó.

40. **Hỏi: AWR và ASH dùng để làm gì?**
   **Đáp:** AWR cung cấp snapshot định kỳ và báo cáo. ASH lấy mẫu session đang active để phân tích wait/top SQL trong sự cố (gần realtime).

41. **Hỏi: Tìm SQL đang chạy của một session ở đâu?**
   **Đáp:** Xem `V$SESSION` (SQL_ID), sau đó `V$SQL`/`V$SQLAREA` để lấy text, và `V$SQL_PLAN`/`DBMS_XPLAN.DISPLAY_CURSOR` để xem plan.

42. **Hỏi: Wait event là gì và vì sao hữu ích?**
   **Đáp:** Wait event cho biết session đang chờ gì (I/O, lock, latch, network). Giúp phân biệt vấn đề CPU-bound với contention hoặc bottleneck I/O.

43. **Hỏi: “Cardinality issue” trong execution plan là gì?**
   **Đáp:** Khi optimizer ước lượng sai số dòng, nó có thể chọn join/access path sai. Cách khắc phục: stats tốt hơn, histogram, extended stats, hoặc rewrite query.

44. **Hỏi: SQL Plan Management (SPM) là gì?**
   **Đáp:** SPM quản lý plan baseline để giữ plan ổn định (đã biết tốt) và tránh regression khi thay đổi stats hoặc nâng cấp.

45. **Hỏi: Partitioning là gì và vì sao dùng?**
   **Đáp:** Chia table/index thành nhiều phần (partition) để dễ quản trị và tăng hiệu năng (partition pruning, bảo trì theo vòng đời dữ liệu).

46. **Hỏi: Các kiểu partition phổ biến là gì?**
   **Đáp:** Range, List, Hash và Composite (ví dụ Range-Hash). Mỗi kiểu phù hợp pattern truy cập và phân bố khác nhau.

47. **Hỏi: Partition pruning là gì?**
   **Đáp:** Optimizer loại bỏ các partition không liên quan dựa trên predicate, giảm I/O và tăng tốc query—đây là lợi ích lớn của partitioning.

48. **Hỏi: Local index khác global index trên bảng partitioned thế nào?**
   **Đáp:** Local index “căn theo” partition nên dễ bảo trì (operation trên partition ít ảnh hưởng). Global index trải trên nhiều partition, có thể tốt cho một số query nhưng khó bảo trì hơn.

49. **Hỏi: Materialized view là gì và khi nào nên dùng?**
   **Đáp:** Là kết quả query được lưu sẵn để tăng tốc (đặc biệt join/aggregate). Có thể refresh theo lịch, theo nhu cầu, hoặc fast refresh nếu có MV log.

50. **Hỏi: Query rewrite với materialized view là gì?**
   **Đáp:** Optimizer có thể tự động rewrite query để dùng materialized view thay vì bảng gốc (khi bật và hợp lệ), cải thiện hiệu năng mà không cần sửa SQL.

51. **Hỏi: PL/SQL package là gì và lợi ích?**
   **Đáp:** Gom nhóm procedure/function liên quan, có encapsulation (spec/body), có thể giữ state, và thường giảm overhead parse/load.

52. **Hỏi: Exception handling trong PL/SQL hoạt động thế nào?**
   **Đáp:** Exception có sẵn hoặc tự định nghĩa; xử lý trong khối `EXCEPTION`. Exception chưa xử lý sẽ propagate ra ngoài. Dùng `RAISE`/`RAISE_APPLICATION_ERROR` để báo lỗi tuỳ chỉnh.

53. **Hỏi: `BULK COLLECT` và `FORALL` là gì?**
   **Đáp:** Cơ chế xử lý bulk giảm context switch giữa SQL và PL/SQL: `BULK COLLECT` fetch nhiều dòng/lần; `FORALL` thực hiện DML hàng loạt.

54. **Hỏi: Dynamic SQL là gì và chạy trong PL/SQL như thế nào?**
   **Đáp:** SQL được dựng lúc runtime. Dùng `EXECUTE IMMEDIATE` (đơn giản) hoặc `DBMS_SQL` (phức tạp hơn, bind theo tên, describe cột).

55. **Hỏi: Autonomous transaction là gì và khi nào nên tránh?**
   **Đáp:** Là transaction độc lập với caller (commit/rollback riêng). Hữu ích cho audit/log, nhưng có thể gây vấn đề nhất quán—nên dùng hạn chế.

56. **Hỏi: Trigger trong Oracle là gì và các “bẫy” thường gặp?**
   **Đáp:** Trigger chạy khi DML/DDL/system events. Pitfalls: side effect ẩn, lỗi mutating table, giảm hiệu năng, khó debug; ưu tiên constraint và logic khai báo khi có thể.

57. **Hỏi: Definer’s rights và invoker’s rights trong PL/SQL khác nhau ra sao?**
   **Đáp:** Definer’s rights (mặc định) chạy với quyền của owner. Invoker’s rights (`AUTHID CURRENT_USER`) chạy với quyền người gọi—hữu ích cho utility dùng chung có ranh giới bảo mật.

58. **Hỏi: `DBMS_SCHEDULER` dùng để làm gì?**
   **Đáp:** Lập lịch job/program/chain (mạnh hơn `DBMS_JOB`), hỗ trợ calendar, window, job class, và tích hợp resource management.

59. **Hỏi: Sequence khác identity column thế nào?**
   **Đáp:** Identity column (12c+) là tính năng của table và được Oracle quản lý thông qua sequence “ẩn”. Sequence là object độc lập và thường phải gọi tường minh khi insert.

60. **Hỏi: View khác materialized view thế nào?**
   **Đáp:** View chỉ lưu định nghĩa query (tính toán khi truy cập). Materialized view lưu kết quả (tính toán khi refresh), đổi storage/refresh cost lấy tốc độ.

61. **Hỏi: Khi update một dòng, Oracle đặt những loại lock nào?**
   **Đáp:** Oracle đặt row-level lock trên dòng bị sửa và lock TM ở mức table để phối hợp DDL và kiểm tra ràng buộc, nhưng vẫn cho phép DML đồng thời hợp lệ.

62. **Hỏi: Oracle phát hiện và xử lý deadlock thế nào?**
   **Đáp:** Oracle phát hiện deadlock (ORA-00060), huỷ một statement để phá vòng lặp và ghi chi tiết vào trace; session vẫn còn kết nối.

63. **Hỏi: Oracle hỗ trợ những isolation level nào?**
   **Đáp:** `READ COMMITTED` (mặc định) và `SERIALIZABLE` (cộng thêm transaction `READ ONLY`). Oracle cung cấp statement-level read consistency ở read committed.

64. **Hỏi: ORA-01555 “snapshot too old” là gì và nguyên nhân thường gặp?**
   **Đáp:** Xảy ra khi UNDO cần cho consistent read bị ghi đè trước khi query dùng. Nguyên nhân: query chạy lâu, undo nhỏ/retention thấp, DML cao; khắc phục bằng sizing undo/retention và tuning query.

65. **Hỏi: AMM/ASMM trong quản lý bộ nhớ Oracle là gì?**
   **Đáp:** ASMM dùng `SGA_TARGET` để auto-tune SGA; AMM dùng `MEMORY_TARGET` quản lý cả SGA và PGA. Nhiều DBA thích ASMM + cấu hình PGA riêng để dễ dự đoán.

66. **Hỏi: PGA spill ra TEMP là gì và giảm như thế nào?**
   **Đáp:** Sort/hash join lớn vượt PGA sẽ dùng TEMP làm chậm. Giảm bằng tuning SQL, thêm index, tăng PGA, hoặc chọn join method/partitioning phù hợp.

67. **Hỏi: Parallel query là gì và khi nào có hại?**
   **Đáp:** Dùng nhiều process để scan/join nhanh cho workload lớn. Có thể gây hại vì tranh chấp CPU/I/O/interconnect hoặc data skew; nên dùng có kiểm soát với DOP hợp lý.

68. **Hỏi: Direct-path insert là gì?**
   **Đáp:** Insert bỏ qua buffer cache và ghi phía trên high-water mark (ví dụ `INSERT /*+ APPEND */`). Nhanh cho bulk load nhưng ảnh hưởng redo/space và concurrency.

69. **Hỏi: Flashback Query là gì và dùng thế nào?**
   **Đáp:** Cho phép query “tại thời điểm quá khứ” theo SCN/timestamp bằng undo, ví dụ `SELECT ... AS OF TIMESTAMP ...`. Hữu ích điều tra và phục hồi lỗi người dùng.

70. **Hỏi: Flashback Database là gì?**
   **Đáp:** “Quay ngược” toàn bộ database về thời điểm trước bằng flashback logs (cần FRA và bật flashback), thường nhanh hơn restore/recover cho nhiều lỗi logic.

71. **Hỏi: Recycle bin trong Oracle là gì?**
   **Đáp:** Table bị drop có thể vào recycle bin để undrop (trừ khi `PURGE`), giúp khôi phục do xoá nhầm (nếu còn đủ dung lượng).

72. **Hỏi: RMAN là gì và vì sao nên dùng thay vì copy file hệ điều hành?**
   **Đáp:** RMAN hiểu cấu trúc block Oracle, hỗ trợ incremental, nén, mã hoá, validate, và tích hợp catalog/media manager—độ tin cậy cho recovery cao hơn.

73. **Hỏi: RMAN incremental level 0 và level 1 khác nhau?**
   **Đáp:** Level 0 là nền (base) cho chiến lược incremental. Level 1 backup các block thay đổi từ level 0/1 gần nhất (differential) hoặc từ level 0 gần nhất (cumulative).

74. **Hỏi: Khác nhau giữa RESTORE và RECOVER?**
   **Đáp:** RESTORE chép datafile/backup piece từ backup về disk. RECOVER apply redo/archived logs để đưa file về trạng thái nhất quán theo thời điểm.

75. **Hỏi: Point-in-time recovery (PITR) là gì?**
   **Đáp:** Khôi phục DB (hoặc tablespace, hoặc PDB) về một thời điểm/SCN trước khi xảy ra lỗi, rồi mở với RESETLOGS (đối với DB PITR).

76. **Hỏi: RMAN recovery catalog là gì và có bắt buộc không?**
   **Đáp:** Là schema/DB riêng lưu lịch sử metadata RMAN lâu hơn control file. Không bắt buộc nhưng hữu ích cho lịch sử dài, báo cáo và môi trường phức tạp.

77. **Hỏi: Control file autobackup là gì?**
   **Đáp:** Tính năng RMAN tự động backup control file và SPFILE sau khi chạy job backup, giúp tăng khả năng phục hồi khi mất control file.

78. **Hỏi: Block media recovery là gì?**
   **Đáp:** Khôi phục một số block bị hỏng thay vì cả datafile, dùng RMAN + backup/redo—hữu ích khi lỗi cục bộ.

79. **Hỏi: Oracle Data Guard là gì?**
   **Đáp:** Giải pháp HA/DR duy trì một hoặc nhiều standby DB (physical/logical) đồng bộ thông qua redo transport và apply.

80. **Hỏi: Physical standby khác logical standby thế nào?**
   **Đáp:** Physical standby apply redo ở mức block (Redo Apply) và gần như giống byte-for-byte. Logical standby apply bằng SQL (SQL Apply) và có thể cho phép khác biệt cấu trúc nhất định.

81. **Hỏi: Switchover khác failover trong Data Guard?**
   **Đáp:** Switchover là chuyển vai trò có kế hoạch, thường không mất dữ liệu. Failover là chuyển vai trò khi sự cố, có thể mất dữ liệu tuỳ chế độ bảo vệ.

82. **Hỏi: Fast-Start Failover (FSFO) là gì?**
   **Đáp:** Tính năng của Data Guard Broker cho phép failover tự động dựa trên điều kiện sức khoẻ, có observer và ngưỡng cấu hình.

83. **Hỏi: Oracle RAC là gì và giải quyết vấn đề gì?**
   **Đáp:** RAC cho phép nhiều instance mở cùng một database trên shared storage, tăng HA ở mức instance và có thể tăng khả năng mở rộng.

84. **Hỏi: Cache fusion trong RAC là gì?**
   **Đáp:** RAC dùng interconnect để chuyển block dữ liệu giữa các instance (Global Cache) thay vì ghi/đọc disk, giúp giảm I/O và giữ nhất quán buffer cache.

85. **Hỏi: Service trong Oracle là gì và vì sao quan trọng (đặc biệt trong RAC)?**
   **Đáp:** Service đại diện workload, cấu hình preferred instance, failover và load balancing. Nó tạo tên kết nối ổn định không phụ thuộc instance cụ thể.

86. **Hỏi: ASM là gì và vì sao dùng ASM?**
   **Đáp:** Automatic Storage Management là volume manager cho file DB, cung cấp striping/mirroring, quản trị đơn giản và tích hợp tốt với RAC.

87. **Hỏi: Các mức redundancy trong ASM là gì?**
   **Đáp:** External (storage lo), Normal (mirror 2 bản), High (mirror 3 bản). Redundancy ảnh hưởng dung lượng sử dụng và khả năng chịu lỗi.

88. **Hỏi: Oracle Listener là gì?**
   **Đáp:** Dịch vụ mạng nhận yêu cầu kết nối từ client và chuyển cho server process. Dựa trên đăng ký service (dynamic/static) và lắng nghe trên port cấu hình.

89. **Hỏi: Dedicated server khác shared server thế nào?**
   **Đáp:** Dedicated: mỗi session một server process (phổ biến OLTP). Shared server: nhiều session dùng chung pool dispatcher/shared processes, hợp cho nhiều session nhàn rỗi nhưng không tối ưu cho workload nặng.

90. **Hỏi: Connection pooling là gì và vì sao nên dùng?**
   **Đáp:** Pooling tái sử dụng số ít session DB cho nhiều request ứng dụng, giảm logon overhead và tài nguyên—rất quan trọng cho ứng dụng web quy mô lớn.

91. **Hỏi: Role khác system privilege và object privilege như thế nào?**
   **Đáp:** System privilege cho phép hành động ở phạm vi DB (ví dụ `CREATE TABLE`). Object privilege cho phép trên object cụ thể (ví dụ `SELECT` trên table). Role gom nhiều quyền để quản trị dễ.

92. **Hỏi: Profile trong bảo mật Oracle là gì?**
   **Đáp:** Tập các giới hạn và chính sách mật khẩu (thời hạn mật khẩu, số lần sai, giới hạn tài nguyên) gán cho user để đáp ứng security/governance.

93. **Hỏi: Auditing (Unified Auditing) dùng để làm gì?**
   **Đáp:** Ghi lại hành động liên quan bảo mật (logon, dùng privilege, truy cập object) phục vụ tuân thủ và điều tra. Unified Auditing tập trung hoá cấu hình và lưu trữ audit.

94. **Hỏi: TDE (Transparent Data Encryption) là gì?**
   **Đáp:** Mã hoá dữ liệu “at rest” (tablespace/cột) bằng wallet/keystore, giúp bảo vệ datafile và backup khỏi bị lấy cắp offline.

95. **Hỏi: VPD/FGAC là gì?**
   **Đáp:** Virtual Private Database / Fine-Grained Access Control áp policy để tự động thêm predicate vào query, thực thi bảo mật theo dòng (row-level security).

96. **Hỏi: Best practice least-privilege cho tài khoản ứng dụng là gì?**
   **Đáp:** Tách schema, chỉ grant object privilege cần thiết (tránh system privilege rộng), dùng role đúng cách (đặc biệt với PL/SQL definer/invoker), xoay vòng credential và audit hành động quan trọng.

97. **Hỏi: Cách tiếp cận xử lý ORA-00060 (deadlock detected) thế nào?**
   **Đáp:** Xem deadlock trace, xác định session/object liên quan, kiểm tra thứ tự lock trong code, đảm bảo thứ tự locking nhất quán, index FK khi cần, và giảm transaction kéo dài.

98. **Hỏi: Cách xử lý ORA-12514 (listener không biết service) thế nào?**
   **Đáp:** Kiểm tra service name, trạng thái listener, dynamic registration (`LOCAL_LISTENER`), DB đang open và đã register, và `tnsnames.ora`/connect descriptor khớp service của DB.

99. **Hỏi: Cách xử lý ORA-04031 (không cấp phát được shared memory) thế nào?**
   **Đáp:** Kiểm tra shared pool usage/fragmentation, tìm allocation lớn, giảm hard parsing (dùng bind), hạn chế flush (chỉ khi bất đắc dĩ), và sizing `SGA`/shared pool phù hợp.

100. **Hỏi: Các điểm cần chú ý khi upgrade hoặc migrate Oracle database là gì?**
   **Đáp:** Tham số compatibility, NLS settings, tính năng đã dùng (deprecated), kế hoạch backup/rollback, gather stats sau nâng cấp, test hiệu năng, và chọn phương pháp migrate (Data Pump, transportable tablespaces, RMAN duplicate, PDB unplug/plug).
