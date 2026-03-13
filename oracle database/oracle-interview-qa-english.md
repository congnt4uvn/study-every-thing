# Oracle Database Interview Q&A (English)

> 100 practical interview questions with concise answers.

1. **Q: What is the difference between an Oracle *instance* and an Oracle *database*?**
   **A:** An *instance* is memory + background processes (SGA + processes). A *database* is the physical files (datafiles, control files, redo logs). One database can be opened by one instance (single-instance) or multiple instances (RAC).

2. **Q: What are the main components of the SGA?**
   **A:** Common components include Database Buffer Cache, Shared Pool (Library Cache + Data Dictionary Cache), Redo Log Buffer, Large Pool, Java Pool, and (optionally) In-Memory area.

3. **Q: What is the PGA and what does it contain?**
   **A:** PGA is per-process memory (not shared). It contains session memory, private SQL area, and work areas for sorts/hash joins (subject to PGA settings and spilling to TEMP).

4. **Q: Name key Oracle background processes and their responsibilities.**
   **A:** DBWn writes dirty buffers to datafiles; LGWR writes redo to online redo logs; CKPT signals checkpoints and updates headers; SMON does instance recovery; PMON cleans up failed sessions; ARCn archives redo (ARCHIVELOG mode).

5. **Q: What are control files and what do they store?**
   **A:** Control files store database metadata needed to start/open the DB: DB name, file names, checkpoint SCN, redo log history, and backup information. They are critical and should be multiplexed.

6. **Q: What are online redo logs vs archived redo logs?**
   **A:** Online redo logs store redo for current operations; LGWR writes to them. Archived logs are copies of filled redo log groups created by ARCn in ARCHIVELOG mode, used for media recovery and Data Guard.

7. **Q: What is a checkpoint and why is it important?**
   **A:** A checkpoint is when Oracle ensures dirty buffers are written and file headers are updated with a checkpoint SCN. It limits crash recovery time by reducing how much redo must be applied.

8. **Q: What is SCN and where is it used?**
   **A:** SCN (System Change Number) is a logical time/version counter. It’s used for read consistency, recovery, checkpointing, and Data Guard synchronization.

9. **Q: Explain read consistency (Oracle MVCC) at a high level.**
   **A:** Queries see a consistent snapshot as of the query SCN. If rows change during the query, Oracle reconstructs older versions using UNDO so the query doesn’t see partial/dirty changes.

10. **Q: What are UNDO and TEMP tablespaces used for?**
   **A:** UNDO stores before-images for read consistency and rollback. TEMP is for sort/hash work areas that overflow memory (e.g., large sorts, hash joins), and for some global temporary segment needs.

11. **Q: What is the difference between CDB/PDB in multitenant architecture?**
   **A:** A CDB (Container DB) contains the root (CDB$ROOT), seed (PDB$SEED), and one or more PDBs (pluggable databases). PDBs are isolated logical databases sharing the same Oracle instance.

12. **Q: What is a tablespace and why do we use it?**
   **A:** A tablespace is a logical storage container that maps to one or more datafiles. It helps manage allocation, backup/recovery strategy, and administrative separation of segments.

13. **Q: What are common tablespace types?**
   **A:** Permanent (for tables/indexes), Temporary (for sort/work), Undo (for undo segments). You may also see bigfile tablespaces and locally managed tablespaces (typical).

14. **Q: What is the data dictionary?**
   **A:** It’s the metadata repository (tables and views) that describes objects, users, privileges, and storage. DBAs query views like `DBA_TABLES`, `DBA_INDEXES`, `DBA_USERS`.

15. **Q: What are dynamic performance views (V$ views)?**
   **A:** Views (backed by X$ fixed tables) exposing live instance metrics and state, e.g. `V$SESSION`, `V$SQL`, `V$SYSTEM_EVENT`, `V$DATABASE`.

16. **Q: What is a bind variable and why does it matter?**
   **A:** A placeholder value in SQL (e.g., `:id`). It improves cursor reuse, reduces hard parsing, and typically improves performance and scalability.

17. **Q: What is the difference between hard parse and soft parse?**
   **A:** Hard parse creates a new cursor (parse, optimize, allocate) and is expensive. Soft parse reuses an existing cursor from the shared pool, avoiding most overhead.

18. **Q: What is cursor sharing and when can it be a problem?**
   **A:** Cursor sharing is reuse of parsed SQL. Too many literal variations cause cursor explosion; forced matching can reduce parses but may create suboptimal plans for skewed data.

19. **Q: In what logical order does Oracle evaluate a SELECT query?**
   **A:** Conceptually: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `FETCH/OFFSET` (actual execution plan may differ).

20. **Q: Explain INNER JOIN vs OUTER JOIN.**
   **A:** INNER JOIN returns only matching rows. LEFT/RIGHT/FULL OUTER JOIN returns matches plus non-matching rows from one/both sides with NULLs filled in.

21. **Q: What’s the difference between `IN` and `EXISTS`?**
   **A:** `IN` compares against a list/subquery result; `EXISTS` checks presence of at least one row. `EXISTS` often performs better for correlated checks; null semantics differ.

22. **Q: What’s a correlated subquery?**
   **A:** A subquery that references columns from the outer query, evaluated per outer row (though Oracle can transform it). Example: `WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.k=t1.k)`.

23. **Q: What are analytic (window) functions and why use them?**
   **A:** Functions like `ROW_NUMBER() OVER (...)` compute results across a window of rows without collapsing rows like `GROUP BY`, useful for ranking, running totals, top-N per group.

24. **Q: Difference between `ROW_NUMBER`, `RANK`, and `DENSE_RANK`?**
   **A:** `ROW_NUMBER` is unique sequence. `RANK` gives ties same rank and leaves gaps. `DENSE_RANK` gives ties same rank without gaps.

25. **Q: How do you do pagination in Oracle (12c+)?**
   **A:** Use `OFFSET :n ROWS FETCH NEXT :m ROWS ONLY` with a deterministic `ORDER BY`. For older versions, use `ROWNUM` in a subquery.

26. **Q: What is `MERGE` used for?**
   **A:** It performs conditional insert/update (and optionally delete) in one statement based on match conditions—often used for upsert patterns.

27. **Q: What’s the difference between `DELETE` and `TRUNCATE`?**
   **A:** `DELETE` is DML (row-by-row, generates undo/redo, can be rolled back). `TRUNCATE` is DDL (deallocates/extents, minimal logging, cannot be rolled back).

28. **Q: How do constraints differ from indexes?**
   **A:** Constraints enforce data rules (PK/UK/FK/CHECK/NOT NULL). Indexes speed access. Oracle typically creates a supporting index for PK/UK but not for FK.

29. **Q: Why is indexing foreign keys often recommended?**
   **A:** Unindexed FKs can cause locking/contention and poor performance during parent updates/deletes, and can lead to table locks during constraint enforcement.

30. **Q: What is a deferrable constraint?**
   **A:** A constraint that can be deferred to commit time (`DEFERRABLE INITIALLY DEFERRED`) enabling complex batch operations while still enforcing integrity at commit.

31. **Q: Explain B-tree vs bitmap indexes.**
   **A:** B-tree indexes are good for high-cardinality and OLTP. Bitmap indexes are good for low-cardinality and analytics but can cause locking issues with frequent DML.

32. **Q: What is a function-based index and when is it useful?**
   **A:** An index on an expression (e.g., `UPPER(email)`). Useful when queries filter on expressions; enables index access without full scans.

33. **Q: What is a composite index and what is the “leading column” rule?**
   **A:** An index on multiple columns. Oracle can efficiently use it when predicates include the leading column(s); otherwise usage may be limited (though skip-scan can help).

34. **Q: What is index clustering factor and why does it matter?**
   **A:** It measures how ordered table rows are with respect to the index. Low clustering factor favors index range scans; high factor can make table access via index expensive.

35. **Q: What’s the difference between `EXPLAIN PLAN` and seeing the actual runtime plan?**
   **A:** `EXPLAIN PLAN` shows an estimated plan without executing. Actual plan (e.g., `DBMS_XPLAN.DISPLAY_CURSOR`) includes real row counts, adaptive decisions, and runtime stats when enabled.

36. **Q: What are optimizer statistics and how do you gather them?**
   **A:** Stats describe data distribution (row counts, NDV, histograms). Gather using `DBMS_STATS.GATHER_TABLE_STATS` (or auto task). Fresh stats are crucial for good plans.

37. **Q: What are histograms and when do you need them?**
   **A:** Histograms capture skewed value distributions to improve selectivity estimates. Useful when predicates filter on non-uniform columns and plan choices depend on accurate selectivity.

38. **Q: What is the shared pool and what causes shared pool issues?**
   **A:** Shared pool caches parsed SQL/PLSQL and dictionary metadata. Excessive parsing, many unique SQLs, or large objects can cause memory pressure and errors like ORA-04031.

39. **Q: What are common SQL performance troubleshooting steps?**
   **A:** Confirm the exact SQL + binds, check plan and row estimates, identify wait events, validate stats, review indexes/partitioning, and compare with known good baselines.

40. **Q: What are AWR and ASH used for?**
   **A:** AWR provides periodic performance snapshots and reports. ASH samples active sessions to diagnose waits and top SQL during incidents (near-real-time root cause).

41. **Q: Where do you look to find currently running SQL for a session?**
   **A:** `V$SESSION` (SQL_ID), then `V$SQL`/`V$SQLAREA` for text, and `V$SQL_PLAN`/`DBMS_XPLAN.DISPLAY_CURSOR` for the plan.

42. **Q: What is a wait event and why is it useful?**
   **A:** Wait events indicate what a session is waiting on (I/O, locks, latches, network). They help distinguish CPU-bound issues from contention or I/O bottlenecks.

43. **Q: What is an execution plan “cardinality” issue?**
   **A:** When the optimizer misestimates rows, it may choose a wrong join method/access path. Fixes include better stats, histograms, extended stats, or query rewrite.

44. **Q: What is SQL Plan Management (SPM)?**
   **A:** SPM captures and manages plan baselines to keep stable, known-good plans and prevent regressions after stats changes or upgrades.

45. **Q: What is partitioning and why do we use it?**
   **A:** Partitioning splits a table/index into smaller pieces (partitions) to improve manageability and performance (partition pruning, maintenance, lifecycle operations).

46. **Q: Name common partitioning types.**
   **A:** Range, List, Hash, and Composite (e.g., Range-Hash). Each targets different data access patterns and distribution.

47. **Q: What is partition pruning?**
   **A:** The optimizer eliminates irrelevant partitions based on predicates, reducing I/O and speeding queries—one of the key benefits of partitioning.

48. **Q: Difference between local and global indexes on partitioned tables?**
   **A:** Local indexes are partition-aligned and easier to maintain (partition operations don’t invalidate all index data). Global indexes span partitions and can be more efficient for some queries but are harder to maintain.

49. **Q: What is a materialized view and when would you use it?**
   **A:** A precomputed, stored query result used for performance (especially aggregates/joins). Can be refreshed on demand, scheduled, or fast refreshed with logs.

50. **Q: What is query rewrite with materialized views?**
   **A:** The optimizer can transparently rewrite a query to use a materialized view instead of base tables when enabled and valid, improving performance without changing SQL.

51. **Q: What are PL/SQL packages and why are they useful?**
   **A:** Packages group related procedures/functions, provide encapsulation (spec/body), shared state, and improved performance via reduced parse/load overhead.

52. **Q: How does exception handling work in PL/SQL?**
   **A:** Exceptions can be predefined or user-defined; handled in `EXCEPTION` blocks. Unhandled exceptions propagate outward. Use `RAISE`, `RAISE_APPLICATION_ERROR` for custom errors.

53. **Q: What are `BULK COLLECT` and `FORALL`?**
   **A:** Bulk processing features to reduce context switches between SQL and PL/SQL: `BULK COLLECT` fetches many rows at once; `FORALL` performs bulk DML.

54. **Q: What is dynamic SQL and how do you execute it in PL/SQL?**
   **A:** SQL constructed at runtime. Use `EXECUTE IMMEDIATE` (simple) or `DBMS_SQL` (more complex/bind by name, describe columns).

55. **Q: What is an autonomous transaction and when should you avoid it?**
   **A:** A transaction independent of the caller (separate commit/rollback). Useful for audit/log tables, but can create consistency issues—use sparingly.

56. **Q: What are database triggers and common pitfalls?**
   **A:** Triggers run on DML/DDL/system events. Pitfalls: hidden side effects, mutating table errors, performance overhead, and complex debugging; prefer constraints and declarative logic when possible.

57. **Q: Definer’s rights vs invoker’s rights in PL/SQL?**
   **A:** Definer’s rights (default) executes with owner privileges. Invoker’s rights (`AUTHID CURRENT_USER`) executes with caller privileges—useful for shared utilities with security boundaries.

58. **Q: What is `DBMS_SCHEDULER` used for?**
   **A:** It schedules jobs, programs, and chains (more advanced than `DBMS_JOB`), supports calendars, windows, job classes, and resource management integration.

59. **Q: Sequences vs identity columns—what’s the difference?**
   **A:** Identity columns (12c+) are a table feature backed by a sequence managed by Oracle. Sequences are standalone objects used explicitly in inserts.

60. **Q: What is the difference between a view and a materialized view?**
   **A:** A view stores only the query definition (computed on access). A materialized view stores the result set (computed on refresh), trading storage/refresh cost for query speed.

61. **Q: What happens when a transaction updates a row—what locks are taken?**
   **A:** Oracle takes row-level locks on modified rows and a table-level TM lock in a mode that allows concurrent DML but coordinates DDL and referential checks.

62. **Q: How does Oracle detect and handle deadlocks?**
   **A:** Oracle detects deadlocks (e.g., ORA-00060), aborts one statement to break the cycle, and records details in a trace file; the session remains connected.

63. **Q: What isolation levels does Oracle support?**
   **A:** `READ COMMITTED` (default) and `SERIALIZABLE` (plus `READ ONLY` transactions). Oracle provides statement-level read consistency in read committed.

64. **Q: What is ORA-01555 “snapshot too old” and common causes?**
   **A:** It occurs when needed undo is overwritten before a query can use it for consistent reads. Causes: long queries, insufficient undo retention/size, high DML; fix via undo sizing/retention and query tuning.

65. **Q: What is memory management (AMM/ASMM) in Oracle?**
   **A:** ASMM uses `SGA_TARGET` to auto-tune SGA components; AMM uses `MEMORY_TARGET` to manage both SGA and PGA. Many DBAs prefer ASMM + manual PGA target for predictability.

66. **Q: What is PGA spill to TEMP and how do you reduce it?**
   **A:** Large sorts/hash joins exceed PGA and use TEMP, slowing queries. Reduce by tuning SQL, adding indexes, increasing PGA, or using better join methods/partitioning.

67. **Q: What is parallel query and when can it hurt?**
   **A:** It uses multiple processes to scan/join faster on large workloads. It can hurt due to CPU, I/O, and interconnect contention, or skewed distribution; use selectively with proper DOP.

68. **Q: What is direct-path insert?**
   **A:** Inserts that bypass buffer cache and write data above the high-water mark (e.g., `INSERT /*+ APPEND */`). It can be faster for bulk loads but increases redo/space patterns and impacts concurrency.

69. **Q: What is Flashback Query and how is it used?**
   **A:** It lets you query data “as of” a past SCN/timestamp using undo, e.g., `SELECT ... AS OF TIMESTAMP ...`. Useful for investigation and recovery from user errors.

70. **Q: What is Flashback Database?**
   **A:** It rewinds the whole database to a prior time using flashback logs (requires FRA and flashback enabled), often faster than restore/recover for many logical corruptions.

71. **Q: What is the recycle bin in Oracle?**
   **A:** Dropped tables are moved to a recycle bin for easy undrop (unless `PURGE`), helping recover from accidental drops (space permitting).

72. **Q: What is RMAN and why use it instead of OS copies?**
   **A:** RMAN is Oracle’s backup/recovery tool that understands block structure, supports incremental backups, compression, encryption, validation, and integrates with catalogs and media managers.

73. **Q: Explain RMAN incremental level 0 vs level 1.**
   **A:** Level 0 is a base backup (like full for incremental strategy). Level 1 backs up blocks changed since the last level 0/1 (differential) or since last level 0 (cumulative).

74. **Q: What’s the difference between RESTORE and RECOVER?**
   **A:** RESTORE copies backup pieces/datafiles back to disk. RECOVER applies redo/archived logs to bring restored files to a consistent point in time.

75. **Q: What is point-in-time recovery (PITR)?**
   **A:** Recovering the database (or a tablespace, or a PDB) to a specific time/SCN before an error, then opening with RESETLOGS (for DB PITR).

76. **Q: What is the RMAN recovery catalog and is it required?**
   **A:** A separate schema/database that stores RMAN metadata history beyond the control file record. Not required, but helpful for long history, reporting, and complex environments.

77. **Q: What is control file autobackup?**
   **A:** An RMAN feature that automatically backs up the control file and SPFILE after backup jobs, improving recoverability when control files are lost.

78. **Q: What is block media recovery?**
   **A:** Recovery of specific corrupted blocks rather than entire datafiles, using RMAN and backups/redo—useful for localized corruption.

79. **Q: What is Oracle Data Guard?**
   **A:** A high availability/disaster recovery solution maintaining one or more standby databases (physical/logical) synchronized via redo transport and apply.

80. **Q: Physical vs logical standby—what’s the difference?**
   **A:** Physical standby applies redo at block level (Redo Apply) and stays byte-for-byte similar. Logical standby applies SQL (SQL Apply) and can allow some structural differences.

81. **Q: Switchover vs failover in Data Guard?**
   **A:** Switchover is planned role reversal with minimal/no data loss. Failover is unplanned promotion of standby to primary; may involve data loss depending on protection mode.

82. **Q: What is Fast-Start Failover (FSFO)?**
   **A:** A Data Guard Broker feature enabling automatic failover based on health conditions, with configurable thresholds and observers.

83. **Q: What is Oracle RAC and what problem does it solve?**
   **A:** Real Application Clusters allows multiple instances to open the same database on shared storage, providing scalability and high availability at the instance level.

84. **Q: What is cache fusion in RAC?**
   **A:** RAC uses the interconnect to ship data blocks between instances (via Global Cache) instead of writing to disk, reducing I/O and enabling coordinated buffer cache coherency.

85. **Q: What are services in Oracle and why are they important (especially in RAC)?**
   **A:** Services represent workloads and can be managed for preferred instances, failover, and load balancing. They provide a stable connection name independent of specific instances.

86. **Q: What is ASM and why use it?**
   **A:** Automatic Storage Management is Oracle’s volume manager for database files, offering striping/mirroring, simplified management, and integration with RAC.

87. **Q: Explain ASM redundancy levels.**
   **A:** External (storage provides redundancy), Normal (two-way mirroring), High (three-way mirroring). Redundancy affects usable capacity and fault tolerance.

88. **Q: What is the Oracle Listener?**
   **A:** A network service that accepts client connection requests and hands them off to server processes. It uses service registration (dynamic/static) and listens on configured ports.

89. **Q: Dedicated server vs shared server?**
   **A:** Dedicated uses one server process per session (common for OLTP). Shared server uses dispatchers/shared processes to multiplex sessions, beneficial for many idle sessions but not ideal for heavy per-session work.

90. **Q: What is connection pooling and why is it recommended?**
   **A:** Pooling reuses a small number of DB sessions for many app requests, reducing logon overhead and resource usage; essential for scalable web applications.

91. **Q: Explain roles vs system privileges vs object privileges.**
   **A:** System privileges allow actions across the DB (e.g., `CREATE TABLE`). Object privileges allow actions on specific objects (e.g., `SELECT` on a table). Roles group privileges for easier management.

92. **Q: What is a profile in Oracle security?**
   **A:** A set of limits and password policies (password lifetime, failed login attempts, resource limits) assigned to users to enforce security and governance.

93. **Q: What is auditing (Unified Auditing) used for?**
   **A:** It records security-relevant actions (logons, privilege use, object access) for compliance and forensics. Unified Auditing centralizes audit configuration and storage.

94. **Q: What is TDE (Transparent Data Encryption)?**
   **A:** Oracle feature encrypting data at rest (tablespaces/columns) using a wallet/keystore, helping protect backups and datafiles from offline theft.

95. **Q: What is VPD/FGAC?**
   **A:** Virtual Private Database / Fine-Grained Access Control adds security policies that transparently append predicates to queries, enforcing row-level security.

96. **Q: What are best practices for least-privilege database access for applications?**
   **A:** Separate schemas, grant only needed object privileges (avoid broad system privileges), use roles carefully (definer/invoker contexts), rotate credentials, and audit critical actions.

97. **Q: How would you approach troubleshooting ORA-00060 (deadlock detected)?**
   **A:** Identify the deadlock trace, find involved sessions/objects, review transaction order, ensure consistent locking order in code, index foreign keys where needed, and reduce long-running transactions.

98. **Q: How would you troubleshoot ORA-12514 (listener does not currently know of service requested)?**
   **A:** Verify service name, listener status, dynamic registration (`LOCAL_LISTENER`), database is open and registered, and `tnsnames.ora`/connect descriptor matches the DB service.

99. **Q: How would you troubleshoot ORA-04031 (unable to allocate shared memory)?**
   **A:** Check shared pool usage and fragmentation, find large allocations, reduce hard parsing (bind variables), flush only as last resort, and size `SGA`/shared pool appropriately.

100. **Q: What are key considerations when upgrading or migrating an Oracle database?**
   **A:** Compatibility parameters, NLS settings, feature usage (deprecated), backup/rollback plan, stats gathering after upgrade, performance testing, and migration method (Data Pump, transportable tablespaces, RMAN duplicate, PDB unplug/plug).
