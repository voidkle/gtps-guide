A bomb went off at a tile. Only your own player reacts (the call must name your netID in the CALL_FUNCTION
header; for other players it does nothing). If the bomb's tile is within one tile of the tile under your
player's center, you die: the client runs its own [OnKilled](./OnKilled) handler and sends
`action|respawn_spike` to the server. The explosion sound plays either way.

| # | Type | Meaning |
|---|---|---|
| 1 | int | tile x of the bomb |
| 2 | int | tile y of the bomb |

What the client does:

1. Finds the tile under your player's center. If the bomb is at most 1 tile away in both x and y:
   - If you're already dead (avatar+0x128 ≠ 0), nothing more happens there.
   - If the tile under you is item 6398 (Starship Airlock), an effect plays first (`0x10d7b98`).
   - Marks you dead (avatar+0x128 = 2), runs the `OnKilled` handler (`0x12f5620`), then sends a
     [message type 2](/messages/2-generic-text):
     ```text
     action|respawn_spike
     tileX|<x of the tile under you>
     tileY|<y of the tile under you>
     ```
     If there's no tile under you, only `action|respawn_spike\n` is sent.
2. Plays `audio/explode.wav` at the bomb's tile, if that tile is inside the world.

### Decompiled handler

```c
void NetAvatar::BombDetonated(VariantList *args) {            // 0x12f8e64
    if (this->controller) return;                              // avatar+0x110: remote players
    int x = args->GetInt(0), y = args->GetInt(1);
    if (GetWorldTiles()) {
        Rect r = GetCollisionRect(this);                       // 0x133c89c
        Tile *under = GetTileAtPixel(GetWorldTiles(), r.center());   // 0x1621f28
        if (under && abs(x - under->x) < 2 && abs(y - under->y) < 2)
            DieOnSpike(this, under);                           // 0x12f9a18
    }
    if (Tile *t = GetTile(GetWorldTiles(), x, y))              // 0x162092c
        PlaySound(GameLogic(), TilePixelPos(t), "audio/explode.wav");
}

void DieOnSpike(NetAvatar *a, Tile *t) {                       // 0x12f9a18
    if (a->dead) return;                                       // avatar+0x128
    if (t && t->fg == 6398) PlayTileEffect(&a->renderer, 1, TilePixelPos(t));   // 0x10d7b98
    a->dead = 2;
    a->OnKilled();                                             // 0x12f5620
    if (t) SendText(2, "action|respawn_spike\ntileX|" + to_string(t->x) + "\ntileY|" + to_string(t->y) + "\n");
    else   SendText(2, "action|respawn_spike\n");
    GameLogic()->sub_137c33c();
}
```

<small>Handler: `0x12f8e64` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x12f9a18`, `0x12f5620`, `0x1621f28`, `0x162092c`, `0x157f060`.</small>

<!-- args: int,int -->
