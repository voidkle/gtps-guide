# OnItemEffect

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows an item (with a count) flying from one place to another, the animation used when items are picked up, given or
moved. The flying icon lives 2.5 s. Seeds are drawn at full size, other items at half size. It needs a loaded world.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | mode, see below |
| 2 | int | item id (mode 2: the dropped object's id) |
| 3 | int | count shown on the icon |
| 4 | vec2 | point P in pixels (the start point in modes 0, 1, 6 and 7) |
| 5 | vec2 or string | point Q in pixels. In mode 7 it is a string instead: the name of a GUI entity, and Q is that entity's screen position |
| 6 | int | a player's netID, or -1 |

### Modes

| Mode | What flies | Uses |
|---|---|---|
| 2 | Looks up dropped object #2 in the world (gives up if it's gone), **moves the object to Q**, then animates the object's own item and count like the default mode | 2, 4, 5, 6 |
| 3 | From player #6 to the player whose netID is Q.x (the x of argument 5, converted to int). The icon follows the target. "Well, one of them is gone, forget it" is logged if either player is missing | 2, 3, 5, 6 |
| 4 | From player #6 (centre of the avatar) to Q; nothing if that player isn't in the world | 2, 3, 5, 6 |
| 5 | From Q to player #6; the icon follows the player | 2, 3, 5, 6 |
| 6 | From P to Q | 2, 3, 4, 5 |
| 7 | From P (converted from world to screen coordinates) to the GUI entity named by argument 5, for example an inventory button | 2, 3, 4, 5 |
| other | From P to Q if #6 is -1, otherwise from player #6 to Q (same as mode 4) | 2-6 |

Modes 3 and 5 log "Unknown item error" for an item id the item database doesn't have.

### Decompiled handler

```c
// v[n] = argument n
void OnItemEffect(GameLogic *self, VariantList *v) {
    if (!self->world) return;
    uint mode = v[1].GetUINT();
    int  item = v[2].GetINT32(), count = v[3].GetINT32();
    vec2 P = v[4].GetVector2(), Q = {0, 0};
    if (mode == 7) {
        Entity *e = GetEntityByName(GetGUIRoot(), v[5].GetString());
        if (!e) return;
        Q = GetScreenPos(e);                                        // 0x1dbc92c
    } else Q = v[5].GetVector2();
    int netID = v[6].GetINT32();
    ItemFx *fx = &GetGameLogic()->itemFx;                           // GameLogic+0x2c8
    switch (mode) {
    case 2: {
        DroppedObject *o = self->world->objects.Find(item);         // world+0xa0
        if (!o) return;
        MoveObject(&self->world->objects, o, &Q);                   // 0x16191bc
        item = o->itemID; count = o->count;
        goto dflt;
    }
    case 3: FlyBetweenPlayers(fx, item, count, netID, (int)Q.x); break;   // 0x114921c
    case 4: FlyFromPlayer(fx, item, count, netID, &Q); break;             // 0x1148fa4
    case 5: FlyToPlayer(fx, item, count, &Q, netID); break;               // 0x11493c4
    case 6: Fly(fx, item, count, &P, &Q); break;                          // 0x1149048
    case 7: { vec2 s = WorldToScreen(GetCamera(), &P);                    // 0x1199994
              FlyToGUI(fx, item, count, &s, &Q); break; }                 // 0x1149144
    default: dflt:
        if (netID == -1) Fly(fx, item, count, &P, &Q);
        else FlyFromPlayer(fx, item, count, netID, &Q);
    }
}
```

<small>Handler: `0x136fa4c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1148fa4`, `0x1149048`, `0x1149144`, `0x114921c`, `0x11493c4`, `0x16191bc`, `0x1617ff0`, `0x1199994`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnItemEffect", 1u, 1, 1, CL_Vec2f{x, y}, CL_Vec2f{x, y}, 1 });
```
