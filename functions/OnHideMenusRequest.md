# OnHideMenusRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Send it (server side)

```cpp
send_varlist(peer, { "OnHideMenusRequest", 1u });
```
