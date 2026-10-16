# OnPaintTile

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

A player (the CALL_FUNCTION header's `netID`) paints a tile with a paint tool. The client passes the tile
and the paint color to the matching item effect on that player, which draws the painting.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id of the painting tool; only the player's active item effect with this id (low 16 bits) reacts |
| 2 | int | paint bucket item id, picks the color (3478 Red … 3492 Varnish, as in [OnTileBePaintballed](./OnTileBePaintballed)) |
| 3 | int | tile index, `x + y × width`; ignored if outside the world |

Plays `audio/thwoop.wav` at the player, at most once every 150 ms. The color is `GetPaintballColor(arg 2)`
(`0x1903a44`). The tile's own paint state isn't set here; it comes with the tile data.

### Decompiled handler

```c
void NetAvatar::OnPaintTile(VariantList *args) {               // 0x12f82d0
    int toolItem  = args->GetInt(0);
    int paintItem = args->GetInt(1);
    Tile *tile = GetWorldTiles()->GetTileByIndex(args->GetInt(2));
    if (!tile) return;
    if (this->nextThwoopMS < GetTick()) {
        this->nextThwoopMS = GetTick() + 150;
        PlaySoundAt(this, "audio/thwoop.wav");
    }
    uint32_t color = GetPaintballColor(paintItem, true);      // 0x1903a44
    for (ItemEffect *fx : this->itemEffects)                   // avatar+0x3148 .. +0x3150
        if (fx && fx->itemID == (toolItem & 0xffff))           // fx+0x24
            fx->OnPaint(&this->renderer, color, tile);         // vtable +0x150
}
```

<small>Handler: `0x12f82d0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1625b8c`, `0x1303a84`, `0x1903a44`, `0x10d55a0`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPaintTile", 1, 1, 1 }, pPeer->netid);
```
