# OnWorldMenuFTUEMessageRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Stores a tutorial message in a global string (0x29c4f30), probably for the world-select menu to show. The
handler only stores it. [OnLogout](./OnLogout) clears it, and
[CloseWorldMenuFTUEMessage](./CloseWorldMenuFTUEMessage) doesn't.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the message |

### Decompiled handler

```c
void OnWorldMenuFTUEMessageRequest(GameLogic *self, VariantList *args) {
    g_worldMenuFTUEMessage = arg1.str;       // 0x29c4f30
}
```

<small>Handler: `0x135d3c0` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnWorldMenuFTUEMessageRequest", "..." });
```
