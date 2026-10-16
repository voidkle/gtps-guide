# action|trade_accept

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|trade_accept
status|{}
```

## Fields

| Field | Meaning |
|---|---|
| `status` | `1` to set, `0` to undo. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** after `status|`, the client appends one `item|<id>|<count>\n` line for each filled slot of
one side of the trade (the four slots at trade+0xf0; which side wasn't traced, probably the other player's offer, so
the server can check that you accepted what you saw).

The **AcceptTrade** button.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `status` | `1` if you haven't accepted yet (trade+300 == 0), else `0` (toggle) |
| `item` lines | `item\|<item id>\|<count>` per filled slot |

- With a new enough `proto` (feature 10) it does nothing while another menu is open.
- Logs "Trade accepted" and updates the button state locally (`0x178b970`).

```c
SendText(2, "action|trade_accept\nstatus|" + to_string(!trade->accepted) + "\n" + TradeItems(trade));  // 0x178b618
```

<small>Builder: `0x178aeec`; item list `0x178b618`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn't implement trading yet.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|trade_accept\nstatus|1\n");
```

<small>Client function: `0x178aeec` in libgrowtopia.so 5.60.</small>
