Adds a player to the current world. The single argument is a text block of `key|value` lines. If no world is
loaded the client logs "World doesn't exit, not spawning" and does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the spawn description, `key|value` lines separated by `\n` |

Keys the client reads (a missing **required** key means no player is added):

| Key | Required | Used as |
|---|---|---|
| `spawn` | | must be `avatar`, or nothing is added |
| `type` | | `local` = this is you; anything else = another player |
| `netID` | yes | the player's netID |
| `userID` | | stored at avatar+0x12c; [OnRemove](./OnRemove) can check it |
| `posXY` | | `x|y`, the position in **pixels** |
| `colrect` | yes | `left|top|right|bottom`; the collision box is `right-left` × `bottom-top` (gurotopia: `0|0|20|30`) |
| `name` | | display name (avatar+0x28), may contain color codes |
| `eid`, `ip` | | passed together to an app service (app+0xcb0, vtable+0x38); probably crash/analytics user info |
| `titleIcon` | | a title icon name; looked up in the title table (`0x131114c`) |
| `country` | | `code|flag|flag...`, see below |
| `invis` | yes | non-zero = invisible (avatar+0x160) |
| `mstate` | yes | non-zero = moderator state (avatar+0x161) |
| `smstate` | yes | non-zero = super-moderator state (avatar+0x162) |
| `onlineID` | | stored on the avatar |
| `battle` | | team number (avatar+0x26d); when absent the team and flag bytes are 0xff |
| `bflag` | | carried-flag byte (avatar+0x26e), 0xff when absent; only read when `battle` is present |
| `bscore` | | team-battle score (avatar+0x270); the top-3 list is recomputed |

`country` is split at `|`. The first part is the country code. The words after it set flags on the avatar:
`donor`, `master`, `doctor`, `ccBadge`, `ttBadge`, `euphoriaTitle`, `showGuild`, `maxLevel`. Some of them
(and the code `lg`, and a name ending in ` of Legend``) replace the shown flag with a badge.

With `type|local`:

- if the saved variable `seed_diary_hash_dirty` is ≥ 1 the client sends `action|get_seed_diary_data\n` (message type 2);
- the avatar gets the local-player controller and becomes `self->localPlayer` (GameLogic+0x1a8);
- the client fires its own `OnLocalPlayerSpawned` function and sets 9 `Slot_N` entries from a list kept on the avatar (avatar+0x2f8, probably the quick-bar);
- the tile under `posXY` is looked up and stored on the avatar (avatar+0x254).

Other players get a remote controller (`0x12dccb0`), which is what [0x00 STATE](/packets/00-state) packets move.

### Decompiled handler

```c
void OnSpawn(GameLogic *self, VariantList *args) {
    if (!self->world) { Log("World doesn't exit, not spawning"); return; }
    const char *s = arg1.str;
    GetField(s, "spawn|", &spawn);  GetField(s, "type|", &type);
    GetVec2(s, "posXY|", &pos);
    if (!GetInt(s, "netID|", &netID)) return;
    GetInt(s, "userID|", &userID);  GetField(s, "name|", &name);
    GetField(s, "eid|", &eid);  GetField(s, "ip|", &ip);
    GetApp()->service->SetUser(eid, ip);                       // app+0xcb0, vtable+0x38
    GetField(s, "titleIcon|", &titleIcon);  GetField(s, "country|", &country);
    int invis = 0, mstate = 0, smstate = 0;
    if (!GetInt(s, "invis|", &invis) || !GetInt(s, "mstate|", &mstate) || !GetInt(s, "smstate|", &smstate)) return;
    if (!GetRect(s, "colrect|", &rect)) return;
    GetField(s, "onlineID|", &onlineID);
    if (spawn == "avatar") {
        LogMsg("Add new avatar.");
        NetAvatar *a = new NetAvatar();                        // 0x36c0 bytes
        if (invis) a->invisible = 1;                           // +0x160
        a->mod = mstate != 0; a->superMod = smstate != 0;      // +0x161, +0x162
        a->RegisterFunctions();                                // 0x12ecb2c, the NetAvatar dispatcher
        a->SetNetID(netID);
        a->name = name;
        a->SetCountry(country);                                // 0x131123c
        a->userID = userID;                                    // +0x12c
        a->SetOnlineID(onlineID);
        a->SetTitleIcon(titleIcon);                            // 0x131114c
        if (GetInt(s, "battle|", &v)) {
            a->team = v;                                       // +0x26d
            a->flag = GetInt(s, "bflag|", &v) ? v : 0xff;      // +0x26e
            GetInt(s, "bscore|", &v); a->SetBattleScore(v);    // +0x270, 0x1313674
        } else a->team = a->flag = 0xff;
        if (type != "local") {
            a->SetController(new RemoteController());          // 0x12dccb0
        } else {
            if (GetApp()->GetVar("seed_diary_hash_dirty")->i >= 1)
                SendText(2, "action|get_seed_diary_data\n");
            self->f_2f4 = 0;
            a->SetLocalController(...);                        // 0x130db78, 0x130e678
            self->localPlayer = a;                             // +0x1a8
            CallFunction(self, "OnLocalPlayerSpawned");
            for (i = 0; i < 9; i++) SetSlot("Slot_" + i, a->slots[i]);      // u16 list from avatar+0x2f8
            if (Tile *t = GetTileAtPixel(self->world, pos)) a->f_254 = t->f_56;
            ...                                                // app+0xe38: registers userID → eid
        }
        NetObjects()->Add(a);
        a->SetSize(rect.right - rect.left, rect.bottom - rect.top);   // 0x133c158
        a->pos = pos;                                          // +8
        a->UpdateTile();  a->EnterWorld(self->world);
        LogMsg("Add new avatar done.");
    }
    ...                                                        // refreshes the player list UI (0x115046c, 0x13c88b4)
}
```

<small>Handler: `0x136accc` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x157f12c` (get field), `0x157f420` (get vec2), `0x157f82c` (get int), `0x157f568` (get rect), `0x131123c`, `0x131114c`, `0x1311a10`, `0x12ec798`, `0x1313674`.</small>

<!-- args: string -->
