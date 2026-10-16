# action|mod_trade

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|mod_trade
itemID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Offers an item in the trade window: the trade window's add button with an item selected in the inventory.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected inventory item (GameLogic+0x298) |

- With nothing selected the client shows "Select one of your items first!" and sends nothing.
- The amount is not part of this message; the server is expected to ask (a dialog) and then send
  [OnTradeStatus](/functions/OnTradeStatus).

```c
void TradeMenu::ModItem(int item) {                           // 0x178e3b4
    if (item == 0) {                                          // "add" button
        if (!self->selected) { Toast("Select one of your items first!"); return; }
        SendText(2, "action|mod_trade\nitemID|" + to_string(self->selected) + "\n");
    } else SendText(2, "action|rem_trade\nitemID|" + to_string(item) + "\n");
}
```

<small>Builder: `0x178e3b4`; called from `0x13ead80` (trade slot tap).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn't implement trading yet.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|mod_trade\nitemID|2\n");
```

<small>Client function: `0x178e3b4` in libgrowtopia.so 5.60.</small>
