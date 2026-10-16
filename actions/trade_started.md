# action|trade_started

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|trade_started
netid|{}
```

## Fields

| Field | Meaning |
|---|---|
| `netid` | The player's `netID` in the current world (from their `OnSpawn`). |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent when the trade window has opened after [OnStartTrade](/functions/OnStartTrade) found the other player.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `netid` | the other player's netID (OnStartTrade argument 2) |

- Not sent if the in-world GUI or the other avatar is missing ("other player doesn't exist!").

<small>Builder: `0x178cd48` (TradeMenu::Open); called from `0x136ffa8` (OnStartTrade).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn't implement trading yet.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|trade_started\nnetid|2\n");
```

<small>Client function: `0x178cd48` in libgrowtopia.so 5.60.</small>
