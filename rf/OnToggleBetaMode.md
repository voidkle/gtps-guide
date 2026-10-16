Switches which beta server the client will use next time it logs on, and prints a message in the console. It doesn't
reconnect.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 2 = "Beta3", 1 = "Beta2", anything else = "Beta" |

All three flags are cleared first and then one is set, so this always turns a beta mode **on**.

| Value | Message |
|---|---|
| 2 | Beta3 mode has been turned on.  Quit and re-logon to try it. |
| 1 | Beta2 mode has been turned on.  Quit and re-logon to try it. |
| other | Beta mode has been turned on.  Quit and re-logon to try it. |

### Decompiled handler

```c
// v[n] = argument n
void OnToggleBetaMode(GameLogic *self, VariantList *v) {
    int which = v[1].GetINT32();
    App *app = GetApp();
    app->beta = app->beta2 = app->beta3 = false;                 // app+0xbe4, +0xbe6, +0xbe7
    if (which == 2) app->beta3 = true; else if (which == 1) app->beta2 = true; else app->beta = true;
    if (app->beta)       ConsolePrintf("Beta mode has been turned on.  Quit and re-logon to try it.");
    else if (app->beta2) ConsolePrintf("Beta2 mode has been turned on.  Quit and re-logon to try it.");
    else ConsolePrintf(app->beta3 ? "Beta3 mode has been turned on.  Quit and re-logon to try it."
                                  : "Beta mode has been turned off.  Quit and re-logon to enter the normal server.");
}
```

`ConsolePrintf` is `0x1716a00` (printf into the console log).

<small>Handler: `0x137057c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1716a00`.</small>

### Screen-controller listener (`0x1ba1ec8`)

This name is also registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function (`0x1be931c` connects it to GameLogic+0x28), so it runs together with the GameLogic handler, for calls with header `netID` = -1.

No arguments are read. The listener wipes the saved login (`0x1087094`, the same as [OnLogout](./OnLogout)
with argument 1 ≠ 0) and pops the current screen (`0x179c59c`), so the player is sent back to log in again.

```c
void operator()(VariantList *const &) {           // 0x1ba86b8
    ScreenFlow *self = this->owner;
    ResetSavedLogin(self->appContext);             // 0x17f9580 → 0x1087094
    PopController(self);                           // 0x179c59c
}
```

<small>Listener: `0x1ba86b8`; callees read: `0x17f9580`, `0x179c59c`.</small>

<!-- args: int -->
