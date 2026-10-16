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

<!-- args: string -->
