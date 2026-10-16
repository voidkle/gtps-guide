Moves a player to a new position, in pixels. Ignored when no world is loaded.

| # | Type | Meaning |
|---|---|---|
| 1 | vec2 | the new position in pixels (top-left of the player's box); missing = (0, 0) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

- The collision box is recomputed, and the index of the tile under the player's centre is stored
  (avatar+0x254; -2 if there's no tile).
- Some movement state is reset (avatar+0xd1, +0x121, and +0x2858 = 3).
- For **your own** avatar, the client also checks a set of physics constants against a value kept in the app
  (app+0xd04). If they differ by more than 0.2 it sends an [APP_INTEGRITY_FAIL (0x19)](/packets/19-app-integrity-fail)
  packet with `itemID` 25, at most once per cooldown.

### Decompiled handler

```c
void NetAvatar::OnSetPos(NetAvatar *a, VariantList *vl) {
    if (!GetGameLogic()->world) return;                            // +0xd8
    a->pos = vl[1].v2;                                             // avatar+0x8 / +0xc
    a->RecalcCollisionBox();                                       // +0xd8..+0xf4
    Tile *t = GetWorld() ? TileAtPixel(GetWorld(), a->Center()) : NULL;   // 0x1621f28
    a->tileIndexUnder = t ? t->index : -2;                         // avatar+0x254, tile+0x56
    a->f_d1 = 0; a->f_121 = 0; a->f_2858 = 3;
    if (a->physics) a->physics->dirty = 1;                         // avatar+0x118, +0x8c
    if (!a->controller) {                                          // your own avatar
        if (fabs(SumOfPhysicsConstants() - GetApp()->physicsCheck) > 0.2f) {   // app+0xd04
            a->integrityReason = 25;                               // avatar+0x258
            if (a->nextIntegrityReport <= GetTick()) {             // avatar+0xfc
                a->nextIntegrityReport = GetTick() + cooldown;
                SendIntegrityFail(GetGameLogic(), ..., 25, 0);     // 0x137c374: type 0x19, itemID 25
            }
        }
        a->lastPosTiles = a->pos / 32;                             // 0x1333c78, avatar+0x18
    }
}
```

<small>Handler: `0x12f5158` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1621f28`, `0x137c374`, `0x1333c78`.</small>

<!-- args: vec2 -->
