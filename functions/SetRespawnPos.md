# SetRespawnPos

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's respawn tile, usually a checkpoint. The argument is a tile index (`x + y × width`); -1 means none.
Ignored when no world is loaded, or when the index is already the current one.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | tile index of the new respawn point |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

For **your own** avatar, the tile flag 0x40 (the "active checkpoint" look, probably) is moved:

- it's cleared on the old respawn tile, if that tile passes `0x15b1d98`;
- it's set on the new one;
- the new tile's item sound plays (the items.dat sound field, item+0x120), if the item has one.

For other players only the index is stored. It's at avatar+0x25c, where the respawn effects of
[OnSetFreezeState](/functions/OnSetFreezeState) read it.

### Decompiled handler

```c
void NetAvatar::SetRespawnPos(NetAvatar *a, VariantList *vl) {
    if (!GetWorldTiles()) return;                                  // 0x1626f30
    int idx = vl[1].u;
    if (idx == a->respawnTile) return;                             // avatar+0x25c
    if (!a->controller) {                                          // your own avatar
        if (a->respawnTile != -1) {
            Tile *old = GetTileByIndex(GetWorldTiles(), a->respawnTile);
            if (old && sub_15b1d98(old)) ClearTileFlag(old, 0x40); // 0x15b015c
        }
        Tile *t = GetTileByIndex(GetWorldTiles(), idx);            // 0x1625b8c
        if (t) {
            SetTileFlag(t, 0x40);                                  // 0x15b0188
            ItemInfo *it = TileItem(t);                            // 0x15b1a88
            if (!it->soundFile.empty()) a->PlaySound(it->soundFile);   // item+0x120
        }
    }
    a->respawnTile = idx;
}
```

<small>Handler: `0x12f77a8` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1625b8c`, `0x15b015c`, `0x15b0188`, `0x15b1a88`, `0x1303a84`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "SetRespawnPos", 1u }, pPeer->netid);
```
