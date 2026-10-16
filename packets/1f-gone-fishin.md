# 0x1f GONE_FISHIN

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1373fd8`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Player `netID` starts or stops fishing. `buildRange` 0 starts it. The avatar plays the fishing animation (state 23)
with the bobber at tile `tileX`, `tileY`, facing left when the bobber is left of the tile the avatar stands on.
`buildRange` 2 stops it, but only if the avatar is still fishing. Other values are ignored.

| Field | Used as |
|---|---|
| `netID` | the player; ignored if not in the world (or no world is loaded) |
| `buildRange` | 0 = start fishing, 2 = stop fishing |
| `tileX`, `tileY` | start only: the tile the line is cast to (stored as floats for the bobber) |

### Sub-commands

`buildRange` selects what happens:

| Value | Effect | Fields used |
|---|---|---|
| 0 | start the fishing animation, bobber at the tile, face toward it | `netID`, `tileX`, `tileY` |
| 2 | stop fishing (animation state 23 → 0) | `netID` |

### Decompiled handler

```c
case 0x1f: // GONE_FISHIN
    if (!self->world) break;
    NetAvatar *avatar = GetAvatar(&self->netObjects /* +0x148 */, pkt->netID);
    if (!avatar) break;
    bool start;
    if (pkt->buildRange == 0)      start = true;
    else if (pkt->buildRange == 2) start = false;
    else break;
    Fishing(&avatar->anim /* avatar+0x330 */, start, pkt->tileX, pkt->tileY);   // FUN_010d8090

void Fishing(AvatarAnim *a, bool start, int tileX, int tileY)
{
    LogMsg("tileX == %d, tileY == %d", tileX, tileY);
    if (!start) {
        if (a->state == 23) a->state = 0;            // 23 = fishing
        return;
    }
    bool faceLeft = false;
    Tile *under = GetTileAtPixel(world, center_of(a->owner));   // FUN_01621f28
    if (under) faceLeft = tileX < under->x;
    // unless one of the avatar's attached objects handles it (vtable +0x310), place the rod
    // and line start: faceLeft ? +14 : 0 pixels across, -12 up, from the avatar's position
    a->faceLeft = faceLeft;
    a->state = 23;
    a->bobberTarget = vec2{ (float)tileX, (float)tileY };
    a->f_25ac = 135.0f;  a->f_259c = a->f_25a4 = 1.0f;  a->f_2580 = 0;   // animation values, meaning not traced
}
```

<small>Handler: the switch at `0x1373fd8`, tail-calls `0x10d8090`; callees read: `0x1626f30`, `0x1621f28`.</small>

## Official client

**Received:** handled at `0x1373fd8` in the incoming switch (`0x1373e20`).
