# OnTileBePaintballed

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows a paintball flying from the player (the CALL_FUNCTION header's `netID`) to a tile. Only the effect is drawn; the tile itself isn't changed (that's [OnPaintTile](./OnPaintTile)).

| # | Type | Meaning |
|---|---|---|
| 1 | int | paint bucket item id, picks the paint color (3478 Red, 3480 Yellow, 3482 Green, 3484 Aqua, 3486 Blue, 3488 Purple, 3490 Charcoal, 3492 Varnish) |
| 2 | int | tile index, `x + y × width`; ignored if outside the world |

- Plays `audio/thwoop.wav` at the player, at most once every 150 ms per player.
- Spawns particle effect 209 at the player's center, with the target set to the tile's pixel position. The
  item id goes into the effect's parameter slot; the effect turns it into a color with
  `GetPaintballColor` (`0x1903a44`), which logs "un-defined color" for any other id.
- If the player's avatar field +0x27ec is 115 (probably an aiming state), the avatar's arm turns to face the tile.

### Decompiled handler

```c
void NetAvatar::OnTileBePaintballed(VariantList *args) {      // 0x12f8100
    int   paintItem = args->GetInt(0);                         // arg 1
    Tile *tile = GetWorldTiles()->GetTileByIndex(args->GetInt(1));   // 0x1625b8c: index < width*height
    if (!tile) return;
    if (this->nextThwoopMS < GetTick()) {                      // avatar+0x168
        this->nextThwoopMS = GetTick() + 150;
        PlaySoundAt(this, "audio/thwoop.wav");                 // 0x1303a84
    }
    vec2 from = this->pos + this->size * 0.5f;                 // avatar+8, +0x10
    vec2 to   = TilePixelPos(tile);                            // 0x15b1c78
    int fx = AddEffect(renderer->particles, 209, from, 0, /*param=*/(float)paintItem);   // 0x1912570
    if (Effect *e = GetEffect(renderer->particles, fx)) e->target = to;                  // +0xb8
    if (this->f_27ec == 115) AimArmAt(&this->renderer, to, from);                        // 0x10df9fc
}
```

<small>Handler: `0x12f8100` (dispatcher `0x12ecb2c`, NetAvatar functions) in the 5.60 arm64 client; callees read: `0x1625b8c`, `0x1303a84`, `0x1912570`, `0x1888e08`, `0x1903a44`, `0x10df9fc`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnTileBePaintballed", 1, 1 }, pPeer->netid);
```
