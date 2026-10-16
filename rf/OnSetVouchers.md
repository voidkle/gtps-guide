Sets the player's voucher count and refreshes the store header. It needs the server's `proto` (login settings)
to be 185 or more; below that the client stores 0 and returns.

| # | Type | Meaning |
|---|---|---|
| 1 | int | vouchers (GameLogic+0x2b0) |

### Decompiled handler

```c
void OnSetVouchers(GameLogic *self, VariantList *args) {
    if (GetApp()->proto < 185) { self->vouchers = 0; return; }
    self->vouchers = arg1.i;
    int tokens = inventory->Count(1486) + inventory->Count(6802) * 100;
    UpdateStoreHeader(self->gems, tokens,
                      GetApp()->proto >= 999999 ? self->dungeonTokens : 0, self->vouchers);   // 0x1771ae8
}
```

<small>Handler: `0x136f728` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1771ae8`.</small>

<!-- args: int -->
