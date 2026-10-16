# OnClashEventIsActiveChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Turns the "Clash event is active" flag on or off. The flag (GameLogic+0x39c) is cleared when the game logic resets; no reader
of it was found with a direct search, so what it changes in the UI wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 = active; any other value = inactive |

### Decompiled handler

```c
// v[n] = argument n
void OnClashEventIsActiveChanged(GameLogic *self, VariantList *v) {
    self->clashEventActive = v[1].GetINT32() == 1;      // +0x39c
}
```

<small>Handler: `0x13716e8` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnClashEventIsActiveChanged", 1 });
```
