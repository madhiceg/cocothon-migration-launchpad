# Action Plan: Infrastructure & Scalability

## Foundational (Score 0-25)

### ACTION: Right-Size Warehouses and Enable Auto-Suspend
- **Effort:** Low | **Impact:** High | **Timeline:** Week 1
- Audit warehouse utilization. Set `auto_suspend` to 60s for interactive, 300s for ETL. Downsize underutilized warehouses.
- **SQL Template:** `tools/action_plan/sql/warehouse_optimization.sql`

### ACTION: Create Resource Monitors with Alerts
- **Effort:** Low | **Impact:** Medium | **Timeline:** Week 1
- Add resource monitors at account and warehouse level with 75%/90%/100% notification thresholds.

---

## Developing (Score 26-50)

### ACTION: Separate Workloads into Dedicated Warehouses
- **Effort:** Medium | **Impact:** High | **Timeline:** Week 2-3
- Create WH_ETL, WH_ANALYTICS, WH_ML with appropriate sizes. Route queries by workload type.

### ACTION: Enable Clustering and Search Optimization
- **Effort:** Medium | **Impact:** Medium | **Timeline:** Week 3-4
- Add clustering keys to large, frequently filtered tables. Enable search optimization for point lookups.

---

## Advancing (Score 51-75)

### ACTION: Implement FinOps with Cost Attribution
- **Effort:** High | **Impact:** High | **Timeline:** Week 4-8
- Tag warehouses with `cost_center`. Build chargeback reports from `METERING_DAILY_HISTORY`.
