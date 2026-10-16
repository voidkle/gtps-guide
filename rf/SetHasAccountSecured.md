Sets the client's "account secured" flag (GameLogic+0x29d), probably whether the account has extra
protection such as two-factor or an email. No other effect in the handler.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = secured. Missing = 0 |

### Decompiled handler

```c
void SetHasAccountSecured(GameLogic *self, VariantList *args) {
    self->accountSecured = arg1.u != 0;      // +0x29d
}
```

<small>Handler: `0x136f0e0` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: uint -->
