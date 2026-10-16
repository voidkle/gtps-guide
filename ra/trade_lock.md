The **LockTrade** button.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `status` | `1` if you aren't locked yet (trade+0x12d == 0), else `0` (toggle) |

- Logs "Trade lock attempt"; the lock shows only after the server's [OnTradeStatus](/functions/OnTradeStatus).

<small>Builder: `0x178aeec` (trade window click handler).</small>
