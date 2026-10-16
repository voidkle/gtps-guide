# OnLogout

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Logs the player out. Two handlers run for a call with header `netID == -1`. The menu-flow listener runs first:
if argument 1 is non-zero it wipes the saved login, then it leaves the current screen. GameLogic's own
handler then clears the client's game data and shows the pause menu.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | optional; non-zero also forgets the saved account (`tankid_name`, `tankid_password`, age/legal flags, console layout, …). Missing = 0 |

### Decompiled handler

```c
// menu flow (0x1ba1ec8), lambda 0x1ba8414 -> 0x1ba39b0
void OnLogout_menu(MenuFlow *m, VariantList *args) {
    if (arg1.u != 0)
        GetAppContext(m->app)->ResetAccount();     // 0x17f9580 -> 0x1087094: LoginAccountType, tankid_name,
                                                   // tankid_password, AgeRequested, LegalShown, IsFirstLogin, ...
    m->PopController();                            // 0x179c59c, "[Controllers] {}: {}" "PopController"
}

// GameLogic (0x135e25c), arguments not read
void OnLogout(GameLogic *self) {
    LogMsg("OnLogout: Clear data");
    sub_11424bc(GetApp()->client);                 // app+0x9a0
    sub_e7e360(); sub_19e5e38(); sub_f1ef6c(); sub_1a01690(); sub_137decc();
    sub_19fa1bc(); sub_137dff4(); sub_19ecf38(); sub_137e11c(); sub_1a08b7c();   // reset game subsystems
    g_29c4f24 = g_29c4f28 = g_29c4f2c = 0;  g_29c4f30 = "";
    CloseMenu(FindEntity(GetEntityRoot(), "PauseMenu"));
    sub_135ccc8(self, 0);
    RemoveEntity(self->entity, "TouchHandlerArcade");
    LogMsg("OnLogout: Clear data done");
}
```

<small>Handler: `0x136b858` (dispatcher `0x135e25c`) and `0x1ba8414` → `0x1ba39b0` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x17f9580`, `0x1087094`, `0x179c59c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnLogout", 1u });
```
