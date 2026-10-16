Starts a store purchase sync: the client sets a flag (app+0xe10 = 1) and asks the store library to restore purchases,
showing "Syncing purchases...". No arguments.

### Decompiled handler

```c
void OnRestorePurchases(GameLogic *self, VariantList *v) {
    GetApp()->f_e10 = 1;
    RestorePurchases(&GetApp()->iap);          // 0x1d935d8, app+0xd10: "Syncing purchases..."
}
```

<small>Handler: `0x1370c54` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1d935d8`.</small>

<!-- args: -->
