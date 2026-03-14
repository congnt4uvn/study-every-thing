# AWS X-Ray (in CloudWatch) — Study Notes

## What this lab demonstrates
- Where to find **X-Ray** in the **CloudWatch** console (new experience)
- How to generate trace data using a **CloudFormation** demo stack
- How to read the **Service map**, investigate **errors**, and analyze **traces**
- Why you should **delete the stack** afterwards to avoid ongoing cost

## Key ideas to remember
- **X-Ray is integrated into CloudWatch**: you can view **Service map** and **Traces** under the CloudWatch navigation.
- **Service map** shows dependencies between AWS components (microservices and downstream calls).
- When something is unhealthy, X-Ray highlights it (e.g., orange/red nodes) and you can drill into **latency**, **request count**, and **faults**.
- **Traces** let you:
  - run queries (including starting with an empty query to see everything)
  - filter to specific services/resources
  - open an individual trace to see a **timeline breakdown** (segments/subsegments)

## Hands-on walkthrough (from the transcript)
### 1) Find X-Ray in CloudWatch
1. Open **CloudWatch console**.
2. In the left navigation, locate X-Ray features such as **Service map**.
3. Expect no data initially.

### 2) Deploy a demo app (CloudFormation)
Goal: create traffic that emits traces into X-Ray.

1. Open **CloudFormation** → **Create stack**.
2. Choose **Upload a template file**.
3. Select the template mentioned in the transcript (simplified “Scorekeep” X-Ray template).
4. Set a stack name, e.g. **Scorekeep X-Ray**.
5. Keep defaults except these network settings:
   - **Subnet 1**: pick the first subnet
   - **Subnet 2**: pick the second subnet
   - **VPC ID**: pick your target VPC
6. Continue **Next** → **Next** → acknowledge capabilities → **Submit**.

Notes on what gets deployed (high level):
- An **ECS**-based app (front-end + back-end) instrumented for X-Ray
- Supporting resources such as **DynamoDB tables**, and **SNS** (as observed in the service map)

### 3) Use the app to generate traces
1. In the stack, open **Outputs**.
2. Find the **Load Balancer** URL and open it.
3. Use the UI to create and play a sample game (the transcript uses **Tic Tac Toe**).
4. As you interact, the app generates X-Ray traces.

### 4) Investigate in X-Ray
#### Service map
- Open **Service map** and identify nodes such as:
  - ECS service/container
  - DynamoDB tables
  - SNS topic
- If a node shows errors (example: **SNS error 100%**), click it to view:
  - latency over time
  - request count
  - faults
  - response time distribution

#### Traces
1. Click **View traces**.
2. Run a query (starting with empty query is fine).
3. Narrow results by adding a service/resource to the query.
4. Use the latency distribution chart to find slow outliers.
5. Open a specific trace to see:
   - the trace map for that request
   - detailed timing of calls (e.g., DynamoDB `GetItem` / other operations)
   - segment details, annotations, metadata, and errors

## Console differences (new vs old)
- The **new X-Ray experience** in CloudWatch may focus on **Service map** and **Traces**.
- The **older X-Ray console** still exposes settings like **sampling**, **encryption**, and **groups**.

## Cleanup (important)
- Delete the CloudFormation stack (e.g., **Scorekeep X-Ray**) when finished.

## Quick self-check (questions)
1. Where do you find X-Ray’s Service map in the console now?
2. What does the Service map represent?
3. How do you go from “SNS shows errors” to identifying the failing requests?
4. What’s the value of opening a single trace vs looking at the aggregate charts?
5. What must you do at the end of this lab to prevent unwanted charges?
