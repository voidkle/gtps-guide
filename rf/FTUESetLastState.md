Sets a global tutorial flag (0x29c4f28), probably "the tutorial is at its last step".
[OnLogout](./OnLogout) resets it.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = set. Missing = 0 |

### Decompiled handler

```c
void FTUESetLastState(GameLogic *self, VariantList *args) {
    g_ftueLast = arg1.u != 0;                // 0x29c4f28
}
```

<small>Handler: `0x135d2c4` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: uint -->
