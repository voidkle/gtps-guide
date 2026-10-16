# OnStoreRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the store, or refreshes it if it's already open. The client has two store UIs:

- **The tabbed store** (`0x1773fdc`) is used when the server's `proto` (login settings) is above 91 **and** the
  text contains `enable_tabs|1`.
- **The old single-page store** (`0x1768970`) is used otherwise.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the store description, built by the store builder (gurotopia: `action/store.cpp`). If it contains `enable_tabs`, the client remembers whether it was `enable_tabs|1` |

If the store isn't open yet and another menu or dialog is open, the client logs "Ignoring dialog request" and
does nothing. The tabbed store makes an exception for the pause menu: it still opens over `PauseMenu`.

The tabbed store's header shows the player's currencies, taken from what the server sent earlier:

| Shown | Value | Source |
|---|---|---|
| gems | GameLogic+0x2a0 | [OnSetBux](./OnSetBux) |
| growtokens | count of item 1486 + 100 × count of item 6802 (Mega Growtoken) in the inventory | inventory |
| dungeon tokens | GameLogic+0x2ac, but only if `proto` ≥ 999999, so in practice always 0 | [OnSetDungeonToken](./OnSetDungeonToken) |
| vouchers | GameLogic+0x2b0 if `proto` ≥ 185, else 0 | [OnSetVouchers](./OnSetVouchers) |

The last argument of `0x1773fdc` is 1 when the store opens fresh and 0 when it refreshes an open one.

### Decompiled handler

```c
void OnStoreRequest(GameLogic *self, VariantList *args) {
    std::string text = arg1.str;
    if (text.find("enable_tabs") != npos)
        g_storeTabs = text.find("enable_tabs|1") != npos;               // 0x1769a78, 0x299b564
    bool tabbed = GetApp()->proto > 91 && g_storeTabs;                  // 0x175a68c
    bool open = FindEntity(GetEntityRoot(), "StoreMenu") != NULL;
    Entity *gui = FindEntity(GetEntityRoot(), "WorldSpecificGUI");
    if (!tabbed) {
        if (!open && IsAnyMenuOpen()) { Log("Ignoring dialog request"); return; }
        BuildOldStore(gui, text);                                       // 0x1768970
    } else {
        if (!open && IsAnyMenuOpen() && !FindEntity(GetEntityRoot(), "PauseMenu")) {
            Log("Ignoring dialog request"); return;
        }
        int tokens = inventory->Count(1486) + inventory->Count(6802) * 100;   // 0x1595c80
        int dungeon = GetApp()->proto >= 999999 ? self->dungeonTokens : 0;
        int vouchers = GetApp()->proto >= 185 ? self->vouchers : 0;
        BuildStore(gui, text, self->gems, tokens, dungeon, vouchers, !open);  // 0x1773fdc
    }
}
```

<small>Handler: `0x136e1ac` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x175a68c`, `0x1769a78`, `0x137d330`, `0x1768970`, `0x1773fdc`, `0x1595c80`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnStoreRequest"` |
| 1 | string | store page |

gurotopia: `include/action/store.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnStoreRequest", "..." });
```
