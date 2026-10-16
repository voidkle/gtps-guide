# 0x23 SPECIAL

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374024`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Adventure mode (worlds built with Adventure Items and the Tomb Robber). It updates the local player's adventure state (an object at local avatar+0x2b8): which adventure items they carry (up to five), the torch, the gong, your lives, the Tomb Robber tile and a door sound. `buildRange` is the sub-command. Nothing happens when you're not in a world or have no avatar.

| Field | Used as |
|---|---|
| `buildRange` | the sub-command (below) |
| `netID` | -1 = clear everything, otherwise the slot (0-4) the item goes into (sub-command 0) |
| `tileX`, `tileY` | a tile (0, 4), an on/off switch in `tileX` (1, 2, 5: 1 = on), or the lives count in `tileX` (3) |
| `posX`, `posY` | where the torch/gong effect plays (1, 2) |

Adventure items are the tiles 1694-1702 with even ids (Rope, Key, Golden Idol, Banana, Torch), 4716 (Pineapple) and 4738 (Crystal Goblet). Tile flag 0x40 hides the item on its tile while someone carries it.

### Sub-commands
`buildRange` selects what happens:

| Value | Effect | Fields used |
|---|---|---|
| 0 | `netID` -1: drop all carried items (their tiles show them again), clear the state and the Tomb Robber mark. Otherwise: take the adventure item on tile (`tileX`, `tileY`) into slot `netID`. The tile hides its item, particle 0x2c plays, the item flies to you, and the item that was in that slot reappears on its tile. A tile that isn't an adventure item does nothing; a tile outside the world empties the slot. | `netID`, `tileX`, `tileY` |
| 1 | Torch on (`tileX` 1) or off. Turning it on plays `audio/flame_go.wav` and particle 0x14 at `pos`. | `tileX`, `pos` |
| 2 | Gong state: when it changes, `audio/gong.wav` and ten particles 0x12 around `pos`. | `tileX`, `pos` |
| 3 | **Lives.** `tileX` is your number of lives (state +0x38 = avatar+0x2f0) and turns the display on (+0x33). Your name tag (`0x12fbeec`) then gets " `4(last life!)``" at 1 or " (*n* lives)``" above 1. `tileY` is stored at +0x34, but nothing in 5.60 reads it back. | `tileX`, `tileY` |
| 4 | Marks the Tomb Robber (4742) on tile (`tileX`, `tileY`): the previously marked one is unmarked; each change plays particle 1. | `tileX`, `tileY` |
| 5 | Door: `audio/door_open.wav` if `tileX` is 1, else `audio/door_shut.wav` (played on your avatar). | `tileX` |

### Decompiled handler

```c
void Adventure(GameLogic *self, packet *pkt)                  // 0x137bfcc
{
    World *w = self->world;
    if (!w) return;
    NetAvatar *me = self->localPlayer;
    AdventureState *a = me ? &me->adventure : NULL;           // avatar+0x2b8
    vec2 pos = pkt->pos;
    switch (pkt->buildRange) {
    case 0:
        if (!me) return;
        if (pkt->netID == -1) Adventure_Clear(a, true);       // sub_14c836c
        else Adventure_Take(a, pkt->netID, GetTile(w, pkt->tileX, pkt->tileY));   // sub_14c86b8
        break;
    case 1: if (me) Adventure_Torch(a, pkt->tileX == 1, &pos); break;   // sub_14c89e0
    case 2: if (me) Adventure_Gong (a, pkt->tileX == 1, &pos); break;   // sub_14c8aec
    case 3: if (me) { a->lives = pkt->tileX; a->value34 = pkt->tileY; a->showLives = 1; } break;  // sub_14c9014
    case 4: if (me) Adventure_MarkRobber(a, GetTile(w, pkt->tileX, pkt->tileY)); break;   // sub_14c8574
    case 5: if (me) {                                           // sub_14c8efc
                a->door = pkt->tileX == 1;
                AvatarSound(me, pkt->tileX == 1 ? "audio/door_open.wav" : "audio/door_shut.wav");
            }
            break;
    }
}

void Adventure_Take(AdventureState *a, int slot, Tile *t)    // sub_14c86b8
{
    if (t && !IsAdventureItem(GetFG(t))) return;
    if (!LocalAvatar()) return;
    if (a->slot[slot] && IsAdventureItem(GetFG(a->slot[slot])))
        ClearFlag(a->slot[slot], 0x40);                        // shows the old item again
    if (t) {
        SetFlag(t, 0x40);                                      // hides the item on its tile
        SpawnParticles(TilePos(t), 0x2c);
        ItemFliesTo(GetFG(t), 1, TilePos(t), LocalAvatar()->netID);   // sub_11493c4
    }
    a->slot[slot] = t;
}

void Adventure_Torch(AdventureState *a, bool on, vec2 *pos)  // sub_14c89e0
{
    if (!a->torch && on && LocalAvatar()) {
        AvatarSound(LocalAvatar(), "audio/flame_go.wav");
        SpawnParticles(pos->x, pos->y, 270.0f, .., 0x14);
    }
    a->torch = on;                                             // state +0x30
}

void Adventure_Gong(AdventureState *a, bool on, vec2 *pos)   // sub_14c8aec
{
    if (a->gong != on && LocalAvatar()) {
        AvatarSound(LocalAvatar(), "audio/gong.wav");
        for (int i = 0; i < 10; i++) SpawnParticles(pos->x ± 32, pos->y ± 32, 0x12);
    }
    a->gong = on;                                              // state +0x31
}
// IsAdventureItem(id): (id - 1694 < 9 && id is even) || id == 4716 || id == 4738
```

<small>Handler: `0x137bfcc` (called from the switch at `0x1374024`) in the 5.60 arm64 client; callees read: `0x14c836c`, `0x14c86b8`, `0x14c89e0`, `0x14c8aec`, `0x14c9014`, `0x14c8574`, `0x14c8efc`.</small>

## Official client

**Received:** handled at `0x1374024` in the incoming switch (`0x1373e20`).
