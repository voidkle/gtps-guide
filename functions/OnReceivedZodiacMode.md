# OnReceivedZodiacMode

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Stores a zodiac mode number on the game logic (+0x140). No reader was found with a direct search, so its effect wasn't
traced; it is probably which zodiac sign or event is active.

| # | Type | Meaning |
|---|---|---|
| 1 | int | zodiac mode |

### Decompiled handler

```c
// v[n] = argument n
void OnReceivedZodiacMode(GameLogic *self, VariantList *v) {
    self->zodiacMode = v[1].GetINT32();     // +0x140
}
```

<small>Handler: `0x1371b60` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnReceivedZodiacMode", 1 });
```
