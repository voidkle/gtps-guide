# OnSetDungeonToken

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the player's dungeon-token count and refreshes the store header. In the 5.60 client this only works
when the server's `proto` (login settings) is 999999 or more. Below that the client stores 0 and returns, so
with any realistic `proto` dungeon tokens always show as 0.

| # | Type | Meaning |
|---|---|---|
| 1 | int | dungeon tokens (GameLogic+0x2ac) |

### Decompiled handler

```c
void OnSetDungeonToken(GameLogic *self, VariantList *args) {
    if (GetApp()->proto < 999999) { self->dungeonTokens = 0; return; }
    self->dungeonTokens = arg1.i;
    int tokens = inventory->Count(1486) + inventory->Count(6802) * 100;
    UpdateStoreHeader(self->gems, tokens, self->dungeonTokens,
                      GetApp()->proto >= 185 ? self->vouchers : 0);    // 0x1771ae8
}
```

<small>Handler: `0x136f664` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1771ae8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetDungeonToken", 1 });
```
