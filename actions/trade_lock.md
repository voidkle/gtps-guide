# action|trade_lock

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|trade_lock
status|{}
```

## Fields

| Field | Meaning |
|---|---|
| `status` | `1` to set, `0` to undo. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **LockTrade** button.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `status` | `1` if you aren't locked yet (trade+0x12d == 0), else `0` (toggle) |

- Logs "Trade lock attempt"; the lock shows only after the server's [OnTradeStatus](/functions/OnTradeStatus).

<small>Builder: `0x178aeec` (trade window click handler).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn't implement trading yet.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|trade_lock\nstatus|1\n");
```

<small>Client function: `0x178aeec` in libgrowtopia.so 5.60.</small>
