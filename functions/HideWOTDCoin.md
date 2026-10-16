# HideWOTDCoin

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Hides the World of the Day coin: it sets a flag on the game logic (+0x4d1 = 0) that the world renderer checks (in `0x11a9ee4`).
No arguments.

### Decompiled handler

```c
void HideWOTDCoin(GameLogic *self, VariantList *v) {
    self->showWOTDCoin = 0;      // +0x4d1
}
```

<small>Handler: `0x1372054` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "HideWOTDCoin" });
```
