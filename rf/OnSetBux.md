Sets the player's gem count. It also sets a few HUD details that travel with it. Two handlers run for a call
with header `netID == -1`: the menu-flow listener puts the gems into the login/menu screen's player info, and
GameLogic's handler updates the in-game HUD and the store header.

| # | Type | Meaning |
|---|---|---|
| 1 | int, or 64-bit (variant type 10) | gems. With the server's `proto` (login settings) at 227 or higher the client reads a **64-bit** value; below that a 32-bit int |
| 2 | int | 0 = stop the gem counter's effect (`RenderBux` +0x94 = 0); non-zero = the counter runs two of its methods, probably the "gems changed" animation. gurotopia sends 1 |
| 3 | int | non-zero = the trash button (`TEXT_TRASH`) reads `RECYCLE`, 0 = `TRASH`. Only applied when the value changes. gurotopia sends 1 |
| 4 | vec3 | optional: `x` goes to GameLogic+0x308 with the current time (+0x310) and a "set" flag (+0x30c); `y != 0` sets GameLogic+0x2e9. Meaning not traced |

Since the type of argument 1 depends on `proto`, a server that sends `proto|227` or more must send gems as a
type-10 (8-byte) variant.

After storing, the store header is refreshed with gems, growtokens (item 1486 + 100 × item 6802), dungeon
tokens and vouchers (`0x1771ae8`; see [OnStoreRequest](./OnStoreRequest)).

### Decompiled handler

```c
// GameLogic (0x135e25c)
void OnSetBux(GameLogic *self, VariantList *args) {
    if (GetApp()->proto < 227) self->gems = (int64)arg1.i;          // +0x2a0
    else                       self->gems = arg1.i64;               // variant type 10
    int effect = arg2.i, recycle = arg3.i;
    self->f_308 = (int)arg4.x;  self->f_310 = GetTick();  self->f_30c = 1;
    self->f_2e9 = (int)arg4.y != 0;
    if (self->recycle != (recycle != 0)) {                          // +0x2e8
        self->recycle = recycle != 0;
        if (Entity *t = FindEntity(GetEntityRoot(), "TEXT_TRASH"))
            SetText(t, self->recycle ? "RECYCLE" : "TRASH");        // 0x1dc99d0
    }
    if (RenderBux *b = GetBuxCounter()) {                           // 0x13c17a8: BuxEnt / RenderBux
        if (effect == 0) b->f_94 = 0;
        else { b->vfunc_0x28(); b->vfunc_0x20(); }
    }
    int tokens = inventory->Count(1486) + inventory->Count(6802) * 100;
    UpdateStoreHeader(self->gems, tokens,
                      GetApp()->proto >= 999999 ? self->dungeonTokens : 0,
                      GetApp()->proto >= 185 ? self->vouchers : 0);  // 0x1771ae8
}

// menu flow (0x1ba1ec8), lambda 0x1ba8928
void OnSetBux_menu(MenuFlow *m, VariantList *args) {
    int64 gems = GetApp()->proto > 226 ? arg1.i64 : arg1.i;
    m->screen->playerInfo.SetGems(gems);                            // 0x1924164: +0x30, refreshes "PlayerInfo"
}
```

<small>Handler: `0x136f37c` (dispatcher `0x135e25c`) and `0x1ba8928` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x13c17a8`, `0x1dc99d0`, `0x1771ae8`, `0x1924164`, `0x1e77b5c`.</small>

<!-- args: int,int,int,vec3 -->
