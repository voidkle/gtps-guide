Shows the result of a store purchase in the purchase pop-up. If the purchase pop-up (`PurchaseMenu`) is
gone, the client logs "Ignoring purchase result, they must have canceled" and drops the message.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the result text (color codes work) |

With the old store (see [OnStoreRequest](./OnStoreRequest)), the text simply fills the pop-up (`0x173ed84`).
With the tabbed store, the client also picks the pop-up title from the text:

| Text contains | Title |
|---|---|
| `You can't afford`, `You already have too many of those`, `slots free to buy that!` or `You don't have enough space` | `Purchase Unsuccessful.` |
| anything else | `Thank you for your purchase!` (and an internal "purchase made" flag is set on the UbiServices adapter) |

So a server reporting a failure should use one of those phrases. A gurotopia-style message such as
`` `4You can't afford that! `` gets the right title.

### Decompiled handler

```c
void OnStorePurchaseResult(GameLogic *self, VariantList *args) {
    ShowPurchaseResult(arg1.str);                         // 0x174873c
}

void ShowPurchaseResult(std::string text) {               // 0x174873c
    Entity *m = FindEntity(GetEntityRoot(), "PurchaseMenu");
    if (!m) { Log("Ignoring purchase result, they must have canceled"); return; }
    if (!TabbedStore()) { FillPopUp(m, text, ...); return; }          // 0x173ed84
    std::string title;
    if (text.find("You can't afford") != npos || text.find("You already have too many of those") != npos
        || text.find("slots free to buy that!") != npos || text.find("You don't have enough space") != npos)
        title = "Purchase Unsuccessful.";
    else {
        title = "Thank you for your purchase!";
        UbiServicesAdapter()->purchased = 1;
    }
    FillPopUp(m, title, text, ...);
}
```

<small>Handler: `0x136e7c0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x174873c`, `0x175a68c`, `0x173ed84`.</small>

<!-- args: string -->
