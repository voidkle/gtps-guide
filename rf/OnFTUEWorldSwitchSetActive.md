Sets a tutorial flag on GameLogic (+0x3a4), probably whether the tutorial's world-switch step is active.
Nothing else happens in the handler.

| # | Type | Meaning |
|---|---|---|
| 1 | int | non-zero = active. Missing = 0 |

### Decompiled handler

```c
void OnFTUEWorldSwitchSetActive(GameLogic *self, VariantList *args) {
    self->ftueWorldSwitch = arg1.i != 0;     // +0x3a4
}
```

<small>Handler: `0x136e168` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
