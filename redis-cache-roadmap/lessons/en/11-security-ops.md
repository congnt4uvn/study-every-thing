# Lesson 11 — Security and operations

## Goal

Run Redis as an operational component: secure access, monitor health, and avoid common “production footguns”.

## Key concepts

- Never expose Redis directly to the public internet.
- Use authentication and ACLs.
- Prefer TLS where supported/required.
- Monitor latency, memory, eviction, and persistence status.

## Hands-on

### Inspect clients and slow operations

- `CLIENT LIST`
- `SLOWLOG GET 10`
- `LATENCY DOCTOR`

### Keyspace stats

- `INFO stats`
- `INFO keyspace`

### ACL basics (conceptual unless enabled)

- Create a user with limited commands and key patterns.
- Principle: least privilege.

## Checklist

- You can list 3 must-monitor metrics (latency, memory, evictions).
- You know why public exposure is dangerous.

## Next

Performance troubleshooting: find slow commands, big keys, and hot keys.
