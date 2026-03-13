# Oracle Database — Practical Documentation (English)

This document is a practical, interview-and-operations oriented overview of Oracle Database concepts and day-to-day DBA/engineering topics.

## 1) What Oracle Database is
- A relational database management system (RDBMS) with SQL as the primary query language and PL/SQL as the procedural extension.
- Provides ACID transactions, multi-version concurrency control (MVCC), rich availability options (RAC, Data Guard), and enterprise backup/recovery (RMAN).

## 2) Core terminology
- **Database**: physical files (datafiles, control files, online redo logs).
- **Instance**: memory + background processes (SGA + processes) that access the database.
- **Schema**: logical container owned by a user; holds objects (tables, views, procedures).
- **Tablespace**: logical storage mapping to one/more datafiles.
- **Segment / Extent / Block**: storage allocation units (segment is object storage; extents are allocated chunks; blocks are smallest units).

## 3) Architecture overview
### 3.1 Memory
- **SGA (shared)**
  - Buffer Cache: cached data blocks
  - Shared Pool: library cache + dictionary cache
  - Redo Log Buffer: redo before writing to redo logs
  - Optional: Large Pool, Java Pool, In-Memory area
- **PGA (per-process)**
  - Session memory, private SQL area, work areas (sort/hash)

### 3.2 Background processes (common)
- **DBWn**: writes dirty buffers to datafiles
- **LGWR**: writes redo entries to online redo logs
- **CKPT**: checkpoint signaling and header updates
- **SMON**: instance recovery
- **PMON**: cleans up failed sessions
- **ARCn**: archives redo logs (ARCHIVELOG)

## 4) Physical storage and files
- **Datafiles**: hold user and dictionary data blocks.
- **Control files**: critical metadata (file names, checkpoint SCN, redo history). Multiplex them.
- **Online redo logs**: current redo; organized into groups/members.
- **Archived redo logs**: copies of filled redo logs (for recovery / Data Guard).
- **Undo tablespace**: undo segments for read consistency and rollback.
- **Temp tablespace**: sorting, hashing, and spill operations.

## 5) Logical storage: tablespaces and objects
- **Tablespace types**: permanent, undo, temporary.
- **Locally managed tablespaces** are standard; extents tracked by bitmaps.
- **Bigfile tablespaces**: single large datafile (management choice).

## 6) Multitenant (CDB/PDB) basics
- **CDB (container database)** contains:
  - CDB$ROOT (root container)
  - PDB$SEED (template)
  - One or more **PDBs** (pluggable databases)
- Benefits: consolidation, easier provisioning/cloning, resource control per PDB.

## 7) SQL essentials (Oracle-specific notes)
### 7.1 Execution and optimization
- Oracle uses a **cost-based optimizer (CBO)**.
- Use **bind variables** for cursor reuse and reduced hard parsing.
- Prefer checking the **actual plan** when troubleshooting:
  - `DBMS_XPLAN.DISPLAY_CURSOR` (actual plan with runtime statistics when enabled)

### 7.2 Common constructs
- **Analytic functions**: `ROW_NUMBER() OVER (...)`, `SUM(...) OVER (...)` for ranking and running totals.
- Pagination (12c+):
  ```sql
  SELECT *
  FROM   t
  ORDER  BY created_at DESC
  OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY;
  ```

## 8) Transactions, locking, and read consistency
- Oracle provides **read consistency** using UNDO (queries see a consistent snapshot).
- DML typically takes **row-level locks**; Oracle also uses TM locks for coordination.
- **Deadlocks** are detected and reported (ORA-00060); one statement is rolled back to break the cycle.
- ORA-01555 “snapshot too old” often indicates undo pressure or long-running queries.

## 9) Indexing and access paths
- **B-tree index**: best for OLTP and high-cardinality columns.
- **Bitmap index**: good for analytics/low-cardinality; avoid on heavy-DML tables.
- **Composite indexes**: order matters; leading columns guide usability.
- **Function-based indexes**: index expressions used in predicates.
- Consider indexing **foreign keys** to reduce locking and improve parent updates/deletes.

## 10) Partitioning (performance + manageability)
- Common types: **range**, **list**, **hash**, and **composite**.
- Key benefit: **partition pruning** (scan only relevant partitions).
- Indexes can be **local** (aligned with partitions) or **global** (spanning partitions).

## 11) Performance diagnostics (what to look at)
### 11.1 Common data sources
- **AWR/ASH**: historical and sampled active session insights.
- Dynamic views:
  - `V$SESSION`, `V$SQL`, `V$SQLAREA`, `V$SYSTEM_EVENT`, `V$ACTIVE_SESSION_HISTORY` (licensed features may apply)

### 11.2 Practical troubleshooting workflow
1. Identify the exact SQL and bind values.
2. Check plan (estimated vs actual) and row misestimates.
3. Check waits (I/O, locks, CPU, network).
4. Validate optimizer stats (stale/missing/skew).
5. Review indexing/partitioning and SQL shape.
6. Use plan stability tools if regressions occur (e.g., SPM).

## 12) Backup and recovery (RMAN)
- **RMAN** is Oracle’s native backup/recovery tool (incrementals, validation, encryption).
- Concepts:
  - **RESTORE**: bring back files from backup
  - **RECOVER**: apply redo to reach target time/SCN
  - Incrementals: level 0 (base) and level 1 (differential/cumulative)
- Recommended:
  - Enable **CONTROLFILE AUTOBACKUP**
  - Periodically **VALIDATE** backups
  - Keep backup + archive log retention aligned with recovery objectives

## 13) High availability and disaster recovery
- **Data Guard**: primary + standby using redo transport and apply
  - Physical standby (redo apply) vs logical standby (SQL apply)
  - Switchover (planned) vs failover (unplanned)
- **RAC**: multiple instances on shared storage for instance-level HA and scaling
- **Flashback** features:
  - Flashback Query (AS OF)
  - Flashback Database (rewind the DB when enabled)

## 14) Security basics
- Privileges:
  - **System privileges** (e.g., create objects)
  - **Object privileges** (e.g., select on a table)
  - **Roles** group privileges
- Policies:
  - **Profiles** for password and resource limits
  - **Auditing** (Unified Auditing)
  - **TDE** for encryption at rest
  - **VPD/FGAC** for row-level security

## 15) Connectivity and services
- **Listener** accepts connection requests and routes to server processes.
- Use **services** to represent workloads (especially in RAC), enabling load balancing and failover.
- Prefer **connection pooling** in applications.

## 16) Routine maintenance checklist
- Monitor tablespace usage, FRA (if used), and archive log generation.
- Keep statistics fresh (auto stats tasks; targeted `DBMS_STATS` as needed).
- Review alert log and trace for recurring errors.
- Validate backups and recovery drills.
- Patch planning: test in lower environments; watch for optimizer changes.

## 17) Common errors (high-level hints)
- **ORA-01555**: undo overwritten; tune query and/or increase undo retention/size.
- **ORA-04031**: shared pool allocation; reduce hard parses, size/tune shared pool.
- **ORA-00060**: deadlock; enforce consistent locking order, index FKs.
- **ORA-12514**: listener doesn’t know service; check service registration and connect descriptor.

## 18) Quick reference: useful queries
> These are examples; adapt for your version and privileges.

- Current sessions (high level):
  ```sql
  SELECT sid, serial#, username, status, sql_id, event
  FROM   v$session
  WHERE  type = 'USER';
  ```

- Top SQL by elapsed time (basic idea):
  ```sql
  SELECT sql_id, elapsed_time/1e6 AS elapsed_s, executions
  FROM   v$sql
  ORDER  BY elapsed_time DESC
  FETCH FIRST 20 ROWS ONLY;
  ```

- Tablespace usage (simple):
  ```sql
  SELECT tablespace_name,
         ROUND(SUM(bytes)/1024/1024) AS mb
  FROM   dba_data_files
  GROUP  BY tablespace_name;
  ```

## 19) Notes on editions and licensing
Some diagnostics/features (AWR/ASH, partitioning, RAC, certain security options) may require specific licenses/editions. Always confirm what’s allowed in your environment.
