---
cursor:
  subagentId: "bc-2740e3da-bc74-51e5-880c-131d56e6ddb8"
---

# Spot check: four c7i.12xlarge in us-east-1

Checked 2026-10-05 16:53 UTC on account `023894314260`. Read-only calls only. No instance was launched, started, or stopped.

**Yes.** Four Spot `c7i.12xlarge` at once are likely in `us-east-1` when the four can land in more than one Availability Zone. They are unlikely all in one zone.

The placement score for a request that names only `c7i.12xlarge` is **3** in the region and **1** in every zone. Amazon EC2 returns a low score when a request names fewer than three instance types, so that 3 is the documented floor, not a reading of the pool. A request for 4 instances of `c7i.12xlarge`, `c6i.12xlarge`, and `c6in.12xlarge` scores **9** in the region. The same shape with `c6i.12xlarge`, `c6in.12xlarge`, and `c5.12xlarge` scores **3**. Adding `c7i.12xlarge` is what moves the score from 3 to 9. Every zone for the high-scoring set is still 1, so the 9 is for capacity spread across zones. A score is a recommendation, not a reservation.

`c7i.12xlarge` is 48 vCPU and 96 GiB. Four of them are 192 vCPU. The fleet in the mass-tokenization plan does not pin a single zone: each machine claims its own parquet key.

## Placement scores

Target capacity is 4 instances. Scores are 1–10. Ten means highly likely to succeed. One means unlikely. The score matches a later Spot request only when that request uses the same types, the same target, and the capacity-optimized strategy.

| Request | Region | us-east-1a | us-east-1b | us-east-1c | us-east-1d | us-east-1f |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `c7i.12xlarge` alone | 3 | 1 | 1 | 1 | 1 | 1 |
| `c7i.12xlarge`, `c6i.12xlarge`, `c6in.12xlarge` | 9 | 1 | 1 | 1 | 1 | 1 |
| `c6i.12xlarge`, `c6in.12xlarge`, `c5.12xlarge` | 3 | 3 | 3 | 3 | 3 | 1 |
| `c7i.12xlarge`, `c7i.8xlarge`, `c7i.16xlarge` | 9 | 6 | 8 | 3 | 8 | 1 |
| `c7i.8xlarge`, `c7i.16xlarge`, `m7i.8xlarge` | 9 | — | — | — | — | — |
| Those three c7i sizes, 192 vCPU | 9 | 5 | 8 | 2 | 8 | 1 |

Zone ids: `use1-az1` is `us-east-1a`, `use1-az2` is `us-east-1b`, `use1-az4` is `us-east-1c`, `use1-az6` is `us-east-1d`, `use1-az5` is `us-east-1f`. `us-east-1e` (`use1-az3`) does not offer `c7i.12xlarge`.

A target of one `c7i.12xlarge` alone still scores 3 in the region, and the best zone for that single machine is `us-east-1a` at 3. A target of two scores 3 in the region and 1 in every zone. Same one-type floor as the four-instance call.

Close types, each queried alone for 4 instances, also sit on that floor: `c7i.8xlarge` region 3 (zone scores 1 to 3), `c7i.16xlarge` region 3 (every zone 1), `m7i.8xlarge` region 1 (every zone 1). Read as a set, they do have a real score. Four instances drawn from `c7i.8xlarge`, `c7i.16xlarge`, and `m7i.8xlarge` score 9 in the region. Four drawn from `c7i.12xlarge`, `c7i.8xlarge`, and `c7i.16xlarge` score 9 in the region and 8 in `us-east-1b` and `us-east-1d`. Adding `m7i.8xlarge` to those three c7i sizes scores 9 in the region and 9 in `us-east-1b` and `us-east-1d`. If all four must share one zone, a mix of the c7i sizes is the request that scores well. The dash row above is region-only.

## Spot price and on-demand

Spot history is Linux/UNIX, the last day, ending at the check. Prices below are USD per instance-hour.

| Zone | Latest | At | Day range |
| --- | ---: | --- | --- |
| us-east-1a | 1.0898 | 2026-10-05 14:00 UTC | 1.0781–1.0898 |
| us-east-1b | 1.1298 | 2026-10-05 14:00 UTC | 1.1298–1.1471 |
| us-east-1c | 1.1926 | 2026-10-05 12:00 UTC | 1.1926–1.2062 |
| us-east-1d | 0.8260 | 2026-10-05 13:00 UTC | 0.8260–0.8315 |
| us-east-1f | 1.6010 | 2026-10-05 14:00 UTC | 1.6010–1.6390 |

On-demand Linux, shared tenancy, is **$2.142 per hour**. `pricing:GetProducts` is denied for this user. The $2.142 figure is the public EC2 price-list row `$2.142 per On Demand Linux c7i.12xlarge Instance Hour`.

Latest Spot is 39% of on-demand in `us-east-1d` ($0.826) and 75% in `us-east-1f` ($1.601). Four boxes are $3.30 per hour at the `us-east-1d` price and $6.40 per hour at the `us-east-1f` price. Four on-demand are $8.57 per hour.

## Quota

| Quota | Code | Value | Four c7i.12xlarge |
| --- | --- | ---: | --- |
| All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests | L-34B43A08 | 256 vCPU | Fits. 192 vCPU, 64 vCPU left. A fifth 12xlarge also fits (240). A sixth does not (288). |
| Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances | L-1216C47A | 64 vCPU | Does not fit. One 12xlarge is 48 vCPU. A second needs 96. |

Both quotas are adjustable. No pending increase is on file. Nothing in `us-east-1` is running or pending, and there is no open Spot request. CloudWatch `AWS/Usage` `ResourceCount` for Standard/Spot and Standard/OnDemand vCPU returned no points in the six hours before the check. Stopped instances were left stopped; a stopped instance does not consume the running vCPU quota.

`c7i.16xlarge` is 64 vCPU, so four of them are 256 vCPU and sit on the Spot cap. `c7i.8xlarge` and `m7i.8xlarge` are 32 vCPU, so four of either are 128 vCPU.
