# 0x20 STEAM

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374204`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Steam (steampunk) block events. `buildRange` says what happened at the tile: a steam pulse, a valve, vent or door
changing state, a pipe being pointed somewhere, or a Spirit Storage Unit filling up or exploding. The client
changes the tile's flags, starts its animation timer, and plays the sound and particles.

| Field | Used as |
|---|---|
| `tileX`, `tileY` | the steam block's tile; ignored if outside the world |
| `buildRange` | the event (below) |

Most events check the tile's foreground and do nothing if it isn't the expected item. "Item sound" is the sound
file of the tile's item in items.dat; "timer" is the tile's animation timer (`0x15b23e8`), in ms.

### Sub-commands

`buildRange` selects what happens:

| Value | Needs foreground | Effect |
|---|---|---|
| 0, 16, 18, 19 | any | Timer = the item's own duration (item+0x13c), item sound, steam effect at the tile (kind 1, 3, 0, 2 for 0, 16, 18, 19). On a Steam Engine (3558), particle 162 pointing at 270° |
| 1, 2 | Steam Valve (3280) | Item sound; 1 clears tile flag 0x20, 2 sets it; sets 0x40; timer 3000 |
| 3 | Steam Vent (3284) | Timer = item duration, sets 0x40, item sound, particle 162 at 180° if the tile is flipped (0x20), else 0° |
| 4, 5 | Steam Door (3286) | 4 sets tile flag 0x40 (open), 5 clears it; particle 162; item sound |
| 6, 7, 8, 9 | any | Clears flags 0x220, then sets 0x40, plus 0x20 for 8 and 9, plus 0x200 for 7 and 9 (no sound) |
| 10, 11, 12, 13 | any | Same flags as 6-9 (10 like 6, 11 like 7...), and plays the item sound |
| 14 | Steam Launcher (3498) | Sets 0x40, timer 1000 |
| 15 | Steam Launcher (3498) | Clears 0x40, item sound, particle 162 at 90° |
| 17 | any | Sets tile flag 0x04 |
| 20, 21 | Spirit Storage Unit (3724) | Timer 1000, `audio/spell1.wav`, 10 particles 154 in random directions |
| 22 | Spirit Storage Unit (3724) | Becomes Destroyed Spirit Storage Unit (3726), `audio/bigboom.wav`, particle 97 |
| 23 | Steam Lamp (3770) | Sets 0x40, timer 10000 |
| 24 | Steam Spikes (3772) | Sets 0x40, timer 500, `audio/hiss3.wav` |
| 25 | Steam Spikes (3772) | Clears 0x40, timer 500, `audio/hiss4.wav` |

Other values do nothing. Tile flag 0x40 is the usual "on" flag and 0x20 "flipped"; 0x200 and 0x04 are only named
by what sets them here.

### Decompiled handler

```c
case 0x20: // STEAM -> 0x137a910
    if (!self->world) return;
    u8 cmd = pkt->buildRange;
    Tile *tile = GetTile(pkt->tileX, pkt->tileY);
    if (!tile) return;
    ItemInfo *it = ItemOf(tile);                             // item->sound is the string at +0x120
    u16 fg = GetFG(tile);

    if (cmd == 0 || cmd == 16 || cmd == 18 || cmd == 19) {
        StartTimer(tile, it->duration);                      // item int +0x13c
        PlaySound(self, TilePos(tile), it->sound);
        SteamEffect_Add(&self->renderer->steam, tile->x, tile->y,
                        cmd == 0 ? 1 : cmd == 16 ? 3 : cmd == 18 ? 0 : 2);   // 0x15a7594
        if (fg == 3558) SpawnParticle(TilePos(tile), 270.0f, 0, self->renderer, 162);
    }
    else if (cmd == 1 || cmd == 2) {
        if (fg != 3280) return;
        PlaySound(self, TilePos(tile), it->sound);
        cmd == 1 ? ClearFlag(tile, 0x20) : SetFlag(tile, 0x20);
        SetFlag(tile, 0x40);
        StartTimer(tile, 3000);
    }
    else if (cmd == 3) {
        if (fg != 3284) return;
        StartTimer(tile, it->duration);
        SetFlag(tile, 0x40);
        PlaySound(self, TilePos(tile), it->sound);
        SpawnParticle(TilePos(tile), (tile->flags & 0x20) ? 180.0f : 0.0f, 0, self->renderer, 162);
    }
    else if (cmd == 4 || cmd == 5) {
        if (fg != 3286) return;
        cmd == 4 ? SetFlag(tile, 0x40) : ClearFlag(tile, 0x40);
        SpawnParticle(TilePos(tile), 0, 1.0f, self->renderer, 162);
        PlaySound(self, TilePos(tile), it->sound);
    }
    else if (cmd == 17) SetFlag(tile, 0x04);                 // 0x15a7640
    else if (cmd >= 6 && cmd <= 13) {
        ClearFlag(tile, 0x220);
        SetFlag(tile, 0x40 | ((cmd & 0xe) == 8 || (cmd & 0xe) == 12 ? 0x20 : 0) | (cmd & 1 ? 0x200 : 0));
        if (cmd >= 10) PlaySound(self, TilePos(tile), it->sound);
    }
    else if (cmd == 22 && fg == 3724) {
        SetForeground(tile, 3726, 0, self->world, 0);
        PlaySound(self, TilePos(tile), "audio/bigboom.wav");
        SpawnParticle(TilePos(tile), 0, 3724.0f, self->renderer, 97);
    }
    else if (cmd == 15 && fg == 3498) {
        ClearFlag(tile, 0x40);
        PlaySound(self, TilePos(tile), it->sound);
        SpawnParticle(TilePos(tile), 90.0f, 0, self->renderer, 162);
    }
    else if (cmd == 14 && fg == 3498) { SetFlag(tile, 0x40); StartTimer(tile, 1000); }
    else if ((cmd == 20 || cmd == 21) && fg == 3724) {
        StartTimer(tile, 1000);
        PlaySound(self, TilePos(tile), "audio/spell1.wav");
        for (10 times) SpawnParticle(TilePos(tile), Random(0, 360), Random(16, 48), self->renderer, 154);
    }
    else if (cmd == 25 && fg == 3772) { ClearFlag(tile, 0x40); StartTimer(tile, 500); PlaySound(self, TilePos(tile), "audio/hiss4.wav"); }
    else if (cmd == 24 && fg == 3772) { SetFlag(tile, 0x40);   StartTimer(tile, 500); PlaySound(self, TilePos(tile), "audio/hiss3.wav"); }
    else if (cmd == 23 && fg == 3770) { SetFlag(tile, 0x40);   StartTimer(tile, 10000); }
```

<small>Handler: `0x137a910` (case 0x20 of `0x1373e20`) in the 5.60 arm64 client; callees read: `0x15a7594`, `0x15a7640`, `0x15b23e8`, `0x15b1a88`.</small>

## Official client

**Received:** handled at `0x1374204` in the incoming switch (`0x1373e20`).
