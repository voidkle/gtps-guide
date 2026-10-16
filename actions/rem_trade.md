# action|rem_trade

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|rem_trade
itemID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Takes an item back out of the trade: tapping one of **your own** filled slots in the trade window.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the item in that slot |

- Tapping an empty slot plays `audio/cant_place_tile.wav`; tapping the other player's slot shows its item info.

<small>Builder: `0x178e3b4` (see [mod_trade](./mod_trade)); called from `0x13ead80`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn't implement trading yet.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|rem_trade\nitemID|2\n");
```

<small>Client function: `0x178e3b4` in libgrowtopia.so 5.60.</small>
