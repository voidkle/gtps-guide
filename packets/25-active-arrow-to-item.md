# 0x25 ACTIVE_ARROW_TO_ITEM

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374d1c`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows or hides the world renderer's guide arrow, the one that points the player at something. When `netID` isn't
0, the client stores it as the arrow's target id, stores `objectType` as the mode, and shows the arrow for its
fixed duration. A `netID` of 0 hides it. Nothing happens when no world is loaded.

The renderer (`0x11b9c1c`) shows what the target and mode mean:
- **Mode 0**: point at the tile the renderer tracks, using the stored id for some tiles.
- **Mode 1**: point at a dropped object. It first tries the tracked object and checks that its item id equals
  the stored id. Otherwise it points at the nearest dropped object of that item.
- **Mode 2**: point at the tracked tile.

So `netID` is really an **item id**.

| Field | Used as |
|---|---|
| `netID` | item id the arrow points at; 0 = hide the arrow |
| `objectType` | mode: 0, 1 (nearest dropped item with that id) or 2 |

### Decompiled handler

```c
case 0x25: // ACTIVE_ARROW_TO_ITEM
    if (!self->world) break;
    WorldRenderer *r = self->renderer;             // self+0xe0
    if (pkt->netID != 0) {
        r->arrowItem = pkt->netID;                 // renderer+0x4a04
        r->arrowMode = pkt->objectType;            // renderer+0x4a08
    }
    // FUN_0165ec5c: timed visibility
    r->arrow.visible = pkt->netID != 0;            // renderer+0x49f8+10
    r->arrow.f_18 = 0; r->arrow.f_20 = 0; r->arrow.f_24 = 0;
    r->arrow.hideAt = GetTick() + r->arrow.duration;
    r->f_4a0c = r->f_4a00;
    break;
```

<small>Handler: inline in the switch at `0x1374d1c`; callees read: `0x165ec5c`; the arrow is drawn in `0x11b9c1c`, which reads the mode and target.</small>

## Official client

**Received:** handled at `0x1374d1c` in the incoming switch (`0x1373e20`).
