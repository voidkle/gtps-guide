# HidePearlCurrency

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Hides the pearl counter in the UI. No arguments. It sets the "show pearls" flag of the `PlayerInfo`
data model (+0x3c) to 0 and notifies its listeners. The amount is set with [OnSetPearl](./OnSetPearl).

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

### Decompiled handler

```c
void operator()(VariantList *const &) {                         // 0x1ba8c48
    SetShowPearls(&this->owner->appContext->playerInfo, 0);     // owner+0x60 → +0x38, 0x19239a8
}
```

<small>Handler: `0x1ba8c48` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x19239a8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "HidePearlCurrency" });
```
