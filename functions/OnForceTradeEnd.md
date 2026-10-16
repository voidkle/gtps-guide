# OnForceTradeEnd

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Closes the trade window if one is open, and logs "Trade force canceled". It takes no arguments and sends nothing back.

### Decompiled handler

```c
void OnForceTradeEnd(GameLogic *self, VariantList *v) {
    if (self->trade) {                       // self+0x300
        CloseTradeMenu(GetGameLogic());      // 0x135d0a4
        LogMsg("Trade force canceled");
    }
}
```

<small>Handler: `0x13700d4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x178dc70`, `0x135d0a4`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnForceTradeEnd" });
```
