# FTUESetBeginingState

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a global tutorial flag (0x29c4f24), probably "the player is at the beginning of the tutorial". The
spelling *Begining* is the client's. [OnLogout](./OnLogout) resets the flag.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = set. Missing = 0 |

### Decompiled handler

```c
void FTUESetBeginingState(GameLogic *self, VariantList *args) {
    g_ftueBeginning = arg1.u != 0;           // 0x29c4f24
}
```

<small>Handler: `0x135d280` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "FTUESetBeginingState", 1u });
```
