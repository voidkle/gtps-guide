# 0x08 TILE_APPLY_DAMAGE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

A punch landed on a tile but didn't break it. The client adds the damage to the tile (which draws the cracks),
flips items that toggle when punched, and plays player `netID`'s punch animation with a hit sound.

| Field | Used as |
|---|---|
| `tileX`, `tileY` | the tile; ignored if outside the world |
| `itemID` | damage to add (gurotopia sends 6). The total is capped at the item's break hits |
| `targetNetID` | the **item id of the punching tool** (stored on the tile, +0x90); it picks how the cracks are drawn (below). Non-zero on a fresh hit also picks a random crack variant 0-2 (+0x8d) |
| `flags` | bit 27 (stored on the tile, +0x8c) lets the tool item's own effect handler draw the cracks (below) |
| `buildRange` | for dice-type items (action type 36: Dice Block, Roshambo Block), the face shown, stored in the tile extra |
| `netID` | the player who punched; -1 or a netID not in the world = no animation or sound (the damage still applies) |

### How the cracks are drawn

The tile renderer (`0x11b5118`) draws the damage with a frame chosen from the damage fraction (`0x15b244c`):
- **Bit 27 set:** the special-effect handler of item `targetNetID` (`0x11f60d8`, vtable +0x3a0) may draw its own
  cracks. If it doesn't, the client draws the normal crack sheet (Doomsday Warhammer, 9606, has its own sheet).
- **Bit 27 clear:** a few tools have built-in crack sprites, for example Staff of Deepest Winter (10406),
  Shamrock Shuriken (10676), Pharaoh's Pendant (11324), Matrix Visor (11384) and Santa's Super Sack (11458).
  Other items go to the item's handler (vtable +0x388/+0x398), and then to the normal cracks. Cactus Cannon
  (10800) and Mystic Battle Lance (10578) add a timed overlay; the Cactus Cannon's is mirrored by the crack
  variant.

So `targetNetID` = 0 (what gurotopia sends) gives the normal cracks.

### What happens

- **Damage.** If the tile's last hit is older than the item's heal time, the damage starts again from 0.
  Then `itemID` is added (Ultra Pinata (718) always counts 1), capped at the item's break hits, and the heal timer
  restarts.
- **Toggles.** Some items change state when punched by flipping tile flag 0x40: action types 12 and 122
  (Boombox, Gravity Well...; not Bullseye, and Antigravity Generator only on the first hit), 138, 31, 32, 39 and 45,
  Steam Crank (3768), and types 11, 36 and 38 once their cooldown has passed. A background of action type 23
  flips tile flag 0x100.
- **Sound and animation** (only when `netID` is a player in the world), chosen from the foreground (or the
  background when there's no foreground):
  - Starship Airlock (6398) that is on: `audio/blorb.wav` and 10 particles (id 255).
  - Action type 11 or 38 that is on: nothing more.
  - Action type 12, 23 or 122 with at most 7 damage: `audio/switch.wav`, no punch animation.
  - Anything else: punch animation, then `audio/metal_hit.wav`, `audio/rock_hit.wav`, `audio/glass_hit.wav` or
    `audio/wood_damage.wav` by the item's material.

### Decompiled handler

```c
case 0x08: // TILE_APPLY_DAMAGE
    if (!self->world) break;
    Avatar *who = pkt->netID == -1 ? NULL : GetAvatar(pkt->netID);
    if (!World_HandlePacket(self->world, pkt)) break;        // applies the damage, see below
    Tile *tile = GetTile(pkt->tileX, pkt->tileY);
    if (!who) break;
    u16 id = tile->fg ? GetFG(tile) : tile->bg;
    if (!itemTable) { PunchAnimation(who, tile); break; }    // 0x1311a24 -> 0x10d8ef8
    ItemInfo *item = items[id];

    if (item->id == 6398 /* Starship Airlock */ && (tile->flags & 0x40)) {
        PlaySound(self, TilePos(tile), "audio/blorb.wav");
        for (10 times) SpawnParticle(TilePos(tile), Random(0, 360), Random(16, 48), self->renderer, 255);
    }
    switch (item->type) {
    case 11: case 38:
        if (tile->flags & 0x40) return;                      // already on: nothing
        goto hit;
    case 12: case 23: case 122:
        if (tile->damage > 7) goto hit;
        PlaySound(self, TileCenter(tile), "audio/switch.wav");
        return;
    default:
    hit:
        PunchAnimation(who, tile);
        PlaySound(self, TileCenter(tile),
                  item->material == 3 ? "audio/metal_hit.wav" : item->material == 2 ? "audio/rock_hit.wav"
                : item->material == 1 ? "audio/glass_hit.wav" : "audio/wood_damage.wav");
    }
    break;

// World_HandlePacket (0x15dd790), type 8:
    Tile *tile = GetTile(pkt->tileX, pkt->tileY);
    if (!tile) return false;
    Tile_ApplyDamage(tile, pkt->itemID, (pkt->flags >> 27) & 1, pkt->targetNetID);   // 0x15b1f90
    if (ItemOf(tile)->type == 36 /* dice */ && tile->extra) tile->extra->value = pkt->buildRange;  // extra+0x60
    return true;

// Tile_ApplyDamage (0x15b1f90)
    tile->hitCount++;                                        // +0x98
    if (tile->fg == 718 /* Ultra Pinata */) damage = 1;
    if (GetTick() > tile->healAt) {                          // +0x84: not hit recently, start over
        tile->damage = 0; tile->hitCount = 0; tile->healAt = 0; tile->tool = -1;
    }
    tile->toolDrawsCracks = flag27;                          // +0x8c
    if (tool != 0 && tile->tool == -1) tile->crackVariant = Random(3);   // +0x8d
    tile->tool = tool;                                       // +0x90: item id of the punching tool
    ItemInfo *item = GetItem(tile->fg ? tile->fg : tile->bg);
    if (!item) return;
    tile->damage = min(tile->damage + damage, item->breakHits);   // +0x80, item byte +0x60
    tile->healAt = GetTick() + item->healSeconds * 1000;    // item int +0xac
    if (tile->fg) { ...toggle tile flag 0x40 for the item types listed above... }
    if (bg item type == 23) tile->flags ^= 0x100;
    else if (bg item type == 22 && bgItem->field_54 == 5) tile->flags &= ~0x100;
```

<small>Handler: case 0x08 of `0x1373e20` in the 5.60 arm64 client; callees read: `0x15dd790`, `0x15b1f90`, `0x1311a24`; crack drawing `0x11b5118`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `buildRange (4th type byte)` | damage/random value (dice, roshambo) |
| `netID` | who punched |
| `itemID` | 6 |
| `tileX / tileY` | the tile |

## gurotopia

`tile_apply_damage()` in `include/database/world.cpp`, sent when a punch lands but the block doesn't break yet.

## Official client

**Received:** handled at `0x1374860` in the incoming switch (`0x1373e20`).
