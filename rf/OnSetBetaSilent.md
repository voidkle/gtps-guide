Sets one of the beta-server flags without a message, but only while all three are off. Then it marks the settings as
changed (app+0x9a8 = 1, probably so they get saved).

| # | Type | Meaning |
|---|---|---|
| 1 | int | non-zero = on |
| 2 | int | which flag: 0 = Beta, 1 = Beta2, 2 = Beta3; anything else does nothing |

### Decompiled handler

```c
// v[n] = argument n
void OnSetBetaSilent(GameLogic *self, VariantList *v) {
    int which = v[2].GetINT32();
    App *app = GetApp();
    if (app->beta || app->beta2 || app->beta3) return;          // +0xbe4, +0xbe6, +0xbe7
    if      (which == 0) app->beta  = v[1].GetINT32() != 0;
    else if (which == 1) app->beta2 = v[1].GetINT32() != 0;
    else if (which == 2) app->beta3 = v[1].GetINT32() != 0;
    else return;
    app->f_9a8 = 1;
}
```

<small>Handler: `0x13707d8` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: int,int -->
