# Lesson 12 — Performance troubleshooting

## Goal

Develop a repeatable approach to diagnosing Redis slowness and memory problems.

## Key concepts

- Most Redis “slow” incidents are caused by:
  - big keys or heavy commands (`KEYS`, large `SORT`, large `ZRANGE` without bounds)
  - CPU saturation (too much work per command)
  - memory pressure leading to eviction or swapping (don’t swap Redis)
  - network latency or client connection storms

## Triage checklist (do in order)

1) Is Redis up?

- `PING`
- `INFO server`

2) Is latency high?

- `LATENCY DOCTOR`
- `SLOWLOG GET 20`

3) Is memory pressured?

- `INFO memory`
- Look at evictions: `INFO stats` (`evicted_keys`)

4) Are there big keys?

- Use `SCAN` + `MEMORY USAGE` sampling (build your own script in your language).

## Hands-on

- `SLOWLOG RESET` (in a non-prod environment)
- Generate some load, then `SLOWLOG GET 10`

## Checklist

- You can name 3 commands to avoid in production patterns.
- You can use `SLOWLOG` and `LATENCY DOCTOR`.

## Next

Capstone: put it all together into a cache layer design.
