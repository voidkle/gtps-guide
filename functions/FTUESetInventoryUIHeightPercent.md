# FTUESetInventoryUIHeightPercent

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets how high the inventory panel sits during the tutorial, as a fraction of the screen. The client stores
the value (0x29c4f2c) and works out the panel's y position from it (0x29dc1b4). The panel moves on the next
layout; this handler doesn't move it.

| # | Type | Meaning |
|---|---|---|
| 1 | float | the fraction, probably 0–1. Missing = 0 |

### Decompiled handler

```c
void FTUESetInventoryUIHeightPercent(GameLogic *self, VariantList *args) {
    g_ftueInvHeight = arg1.f;                                  // 0x29c4f2c
    vec2 p = GetInventoryOrigin();                             // 0x16f8ed4
    float span = ScreenHeight() - p.y;                         // 0x1e7149c
    g_inventoryY = ScreenHeight() - g_ftueInvHeight * span;    // 0x29dc1b4
}
```

<small>Handler: `0x135d308` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x16f8ed4`, `0x1e7149c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "FTUESetInventoryUIHeightPercent", 1.0f });
```
