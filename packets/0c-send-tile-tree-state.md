# 0x0c SEND_TILE_TREE_STATE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x13740d0`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Updates the tree on a tile: its fruit count and growth timer, or removes it when it was harvested. Only works on a
tile that already has tree data (tile extra type 4).

| Field | Used as |
|---|---|
| `tileX`, `tileY` | the tree's tile |
| `targetNetID` | -1: the tree was harvested. Otherwise the tree's **age in seconds** (extra+0x5c): the tile-extra clock (`0x15d0b24`) keeps adding the elapsed seconds to it, and the renderer and splice code read it back through `0x15d1a64`. 1 also plays `audio/wood_damage.wav` |
| `netID` | with `targetNetID` -1: the player who harvested (plays `audio/tree_harvest.wav` and their animation) |
| `itemID` | the fruit count (stored as a byte) |
| `jumpCount` | 1 sets tile flag 0x08 (`TILE_FLAG_WILL_SPAWN_SEEDS_TOO`), anything else clears it |
| `buildRange` | 1 sets tile flag 0x10 (`TILE_FLAG_IS_SEEDLING`), anything else clears it |

Flag names come from the client's own flag-name table (`0x14dbe04`, values 1, 2, 4, 8, 0x10, ...).

If the tile has no tree data the client logs `Error handling tree state change`.

### Decompiled handler

```c
case 0x0c: // SEND_TILE_TREE_STATE
    if (!self->world) break;
    Tile *tile = GetTile(pkt->tileX, pkt->tileY);
    if (pkt->targetNetID == -1) {
        Avatar *who = GetAvatar(pkt->netID);
        if (who) {                                           // 0x1311d90
            AvatarPlaySound(who, "audio/tree_harvest.wav");
            sub_10db78c(&who->anim, tile);                   // harvest animation
        }
    } else if (pkt->targetNetID == 1) {
        PlaySound(self, TileCenter(tile), "audio/wood_damage.wav");
    }
    if (!World_HandlePacket(self->world, pkt))
        LogError("Error handling tree state change");
    break;

// World_HandlePacket (0x15dd790), type 0x0c:
    Tile *tile = GetTile(pkt->tileX, pkt->tileY);
    if (!tile || !tile->extra || tile->extra->type != 4 /* tree */) return false;
    if (pkt->targetNetID == -1) {                            // harvested
        ClearFlag(tile, 0xe000);                             // paint
        SetForeground(tile, 0, 0, world, 0);
        RefreshTile(world, pkt->tileX, pkt->tileY);
        return true;
    }
    tile->extra->fruit = (u8)pkt->itemID;                    // extra+0x60
    pkt->jumpCount  == 1 ? SetFlag(tile, 0x08) : ClearFlag(tile, 0x08);
    pkt->buildRange == 1 ? SetFlag(tile, 0x10) : ClearFlag(tile, 0x10);
    TileExtra_UpdateClock(tile->extra, 0);                   // 0x15d0b24: bring the age up to now
    tile->extra->ageSeconds = pkt->targetNetID;              // +0x5c
    return true;
```

<small>Handler: case 0x0c of `0x1373e20` in the 5.60 arm64 client; callees read: `0x15dd790`, `0x15d1b54`, `0x1311d90`.</small>

## Official client

**Received:** handled at `0x13740d0` in the incoming switch (`0x1373e20`).
