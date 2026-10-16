Tells the client to reconnect. Two handlers run (see below). The in-game one closes the pause menu and
hides the first-time-tutorial popups. The menu-flow one pushes a new connection state (`0x1b6fbc0`, code 7)
unless that state is already showing; it probably reconnects to the server the client already knows.

No arguments are read.

Both handlers are registered, and a call with header `netID == -1` reaches both. `0x1ba1ec8` (menu-flow
listeners) is notified first, then GameLogic's own function runs.

### Decompiled handler

```c
// GameLogic (0x135e25c)
void OnReconnect(GameLogic *self, VariantList *args) {
    CloseMenu(FindEntity(GetEntityRoot(), "PauseMenu"));       // 0x1728644
    self->f_2ec = 0;
    if (self->pendingChaching && self->world) {                // self+0x2fc
        sub_1083db8();          // may send "action|chaching\r\n" + data (message type 3)
        self->pendingChaching = 0;
    }
    HideFTUEPopups(0);          // 0x1682cac: FTUEStartPopup, ConsoleInputBG, ToolSelectMenu
}

// menu flow (0x1ba1ec8), lambda 0x1ba8390 -> 0x1ba3858
void OnReconnect_menu(MenuFlow *m) {
    State s = MakeConnectState(0, 7);                          // 0x1b6fbc0 ("growid", "connectionstate", "serverconnection")
    if (!(m->current && dynamic_cast<ReconnectState *>(m->current)))
        m->Push(MakeReconnect(s, m->server));                  // 0x1ba9a3c, 0x1b72ee4; m+0x60
}
```

<small>Handler: `0x136abf8` (dispatcher `0x135e25c`) and `0x1ba8390` → `0x1ba3858` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1728644`, `0x1083db8`, `0x1682cac`, `0x1b6fbc0`.</small>

<!-- args: -->
