Switches the app's screen mode. Argument 1 equal to 1 selects mode 1, anything else mode 0. The mode is kept
at app+0xbd8. When it changes, the client runs its own `ApplyScreenMode` function, which probably hides or
shows the menus and HUD.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | 1 = hide (mode 1), anything else = normal (mode 0). Missing = 0 |

### Decompiled handler

```c
void OnHideMenusRequest(GameLogic *self, VariantList *args) {
    App *app = GetApp();
    int mode = (arg1.u == 1);
    if (app->screenMode != mode) {                      // app+0xbd8, 0x10843b0
        app->screenMode = mode;
        CallFunction(GameLogic(), "ApplyScreenMode");
    }
}
```

<small>Handler: `0x135d0e4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x10843b0`.</small>

<!-- args: uint -->
