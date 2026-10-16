# GrowIDChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Updates the saved GrowID name after a rename. It works like [SetHasGrowID](./SetHasGrowID) without the
password.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = has a GrowID (GameLogic+0x29c). With 0 the name isn't saved |
| 2 | string | the new name, saved as `tankid_name` |

### Decompiled handler

```c
void GrowIDChanged(GameLogic *self, VariantList *args) {
    self->hasGrowID = arg1.u != 0;
    if (arg1.u) GetApp()->GetVar("tankid_name")->Set(arg2.str);
}
```

<small>Handler: `0x136f124` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "GrowIDChanged", 1u, "..." });
```
