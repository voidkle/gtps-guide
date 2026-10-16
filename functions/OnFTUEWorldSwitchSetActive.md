# OnFTUEWorldSwitchSetActive

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a tutorial flag on GameLogic (+0x3a4), probably whether the tutorial's world-switch step is active.
Nothing else happens in the handler.

| # | Type | Meaning |
|---|---|---|
| 1 | int | non-zero = active. Missing = 0 |

### Decompiled handler

```c
void OnFTUEWorldSwitchSetActive(GameLogic *self, VariantList *args) {
    self->ftueWorldSwitch = arg1.i != 0;     // +0x3a4
}
```

<small>Handler: `0x136e168` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnFTUEWorldSwitchSetActive", 1 });
```
