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
