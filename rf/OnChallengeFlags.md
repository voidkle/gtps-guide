Points a player at two tiles, probably the start and finish flags of a challenge or race. Each argument is a
tile index (`x + y × width`), turned into a pointer to that tile of the current world. An index outside the world
gives no tile.

| # | Type | Meaning |
|---|---|---|
| 1 | int | tile index of the first flag (avatar+0x3598) |
| 2 | int | tile index of the second flag (avatar+0x35a0) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

[OnCountdownEnd](/functions/OnCountdownEnd) clears them. The code that reads them wasn't traced.

### Decompiled handler

```c
void NetAvatar::OnChallengeFlags(NetAvatar *a, VariantList *vl) {
    a->challengeTile1 = GetTileByIndex(GetWorldTiles(), vl[1].i);  // 0x1625b8c, avatar+0x3598
    a->challengeTile2 = GetTileByIndex(GetWorldTiles(), vl[2].i);  // avatar+0x35a0
}
```

<small>Handler: `0x12f7924` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1626f30`, `0x1625b8c`.</small>

<!-- args: int,int -->
