# OnPaw2018SkinColor1Changed

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Unlocks (or locks) extra skin colour 1 from the 2018 "Paw" promotion (the name comes from the function; what Paw was isn't in the code). The flag (GameLogic+0x3b0) is read by the skin colour picker
("Select a skin color:").

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 = unlocked; any other value = locked |

### Decompiled handler

```c
// v[n] = argument n
void OnPaw2018SkinColor1Changed(GameLogic *self, VariantList *v) {
    self->pawSkinColor1 = v[1].GetINT32() == 1;      // +0x3b0, read by 0x1bc580c
}
```

<small>Handler: `0x1370fd0` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPaw2018SkinColor1Changed", 1 });
```
