Closes the trade window if one is open, and logs "Trade force canceled". It takes no arguments and sends nothing back.

### Decompiled handler

```c
void OnForceTradeEnd(GameLogic *self, VariantList *v) {
    if (self->trade) {                       // self+0x300
        CloseTradeMenu(GetGameLogic());      // 0x135d0a4
        LogMsg("Trade force canceled");
    }
}
```

<small>Handler: `0x13700d4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x178dc70`, `0x135d0a4`.</small>

<!-- args: -->
