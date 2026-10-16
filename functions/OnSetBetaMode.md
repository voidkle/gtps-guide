# OnSetBetaMode

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Turns beta mode on or off and **disconnects** the client: it prints a console message, sends `action|quit`, closes the pause
menu and leaves the world.

| # | Type | Meaning |
|---|---|---|
| 1 | int | non-zero = beta mode on, 0 = off |

Message: "Beta mode has been turned on.  Quit and re-logon to try it." or "Beta mode has been turned off.  Quit and re-logon
to enter the normal server."

### Decompiled handler

```c
// v[n] = argument n
void OnSetBetaMode(GameLogic *self, VariantList *v) {
    App *app = GetApp();
    app->beta = v[1].GetINT32() != 0;                                    // app+0xbe4
    ConsolePrintf(app->beta ? "Beta mode has been turned on.  Quit and re-logon to try it."
                            : "Beta mode has been turned off.  Quit and re-logon to enter the normal server.");
    Disconnect(app->client);              // 0x11424bc: sends "action|quit" (type 3), state 5, retry in 500 ms
    ClosePauseMenu(GetEntityByName(GetGUIRoot(), "PauseMenu"));          // 0x1728644
    LeaveWorld(app->gameLogic, 0);        // 0x135ccc8: closes trade, stops PvE, unloads the world
    RemoveEntity(app->gameLogic->entity, "TouchHandlerArcade...");       // 0x1dbe264
}
```

<small>Handler: `0x1370668` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1716a00`, `0x11424bc`, `0x135ccc8`.</small>

### Screen-controller listener (`0x1ba1ec8`)

This name is also registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function (`0x1be931c` connects it to GameLogic+0x28), so it runs together with the GameLogic handler, for calls with header `netID` = -1.

No arguments are read. The listener wipes the saved login (`0x1087094`, the same as [OnLogout](./OnLogout)
with argument 1 ≠ 0) and pops the current screen (`0x179c59c`), so the player is sent back to log in again.

```c
void operator()(VariantList *const &) {           // 0x1ba87f0
    ScreenFlow *self = this->owner;
    ResetSavedLogin(self->appContext);             // 0x17f9580 → 0x1087094
    PopController(self);                           // 0x179c59c
}
```

<small>Listener: `0x1ba87f0`; callees read: `0x17f9580`, `0x179c59c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetBetaMode", 1 });
```
