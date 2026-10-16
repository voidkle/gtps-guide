# OnKilled

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Plays a player's death. No arguments are read.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

- **Your own avatar:**
  - a camera/screen effect is reset (`0x165ec5c` on +0x49f8 of the object from `0x11b25a4`);
  - avatar+0x274 is cleared and the collision box recomputed;
  - a counter at avatar+0x2b8 goes down by one;
  - flags 0x904 are added to avatar+0x124.
- **Other players:**
  - the avatar snaps to its controller's position and the death animation starts;
  - if it died on or next to a Demon Crystal (5274) or Naval Mine (6994) that overlaps it, that tile's
    animation timer is set.
- For everyone: `audio/male_scream.wav` plays unless the player has a third sound set by
  [OnWepSfx](/functions/OnWepSfx) (avatar+0x230). Then the death animation is finished (`0x10d6864`).

### Decompiled handler

```c
void NetAvatar::OnKilled(NetAvatar *a, VariantList *vl) {
    if (!a->controller) {                                          // your own avatar
        ResetScreenEffect(sub_11b25a4() + 0x49f8, 0);              // 0x165ec5c
        a->f_274 = 0;
        a->RecalcCollisionBox();
        if (a->f_2b8.count > 0) a->f_2b8.count--;                  // 0x14c9024
        a->flags |= 0x904;
        a->physics->f_8e = 1;
    } else {
        a->pos = a->controller->pos;                               // controller+0x28
        a->visual.StartDeath(a, true);                             // 0x109abe4
        Tile *t = TileAtPixel(GetWorld(), a->Center());
        if (!t) return;
        if (!IsDeathTrap(t->fg))                                   // 0x156dd34: 5274, 6994
            t = first tile in the 3×3 around it that IsDeathTrap() and overlaps the avatar;
        if (t) t->animStart = GetApp()->tick;                      // tile+0x88, app+0x22c
    }
    a->f_68 = 0;
    if (a->deathSound.empty())                                     // avatar+0x230
        a->PlaySound("audio/male_scream.wav");                     // 0x1303a84
    a->visual.FinishDeath();                                       // 0x10d6864
}
```

<small>Handler: `0x12f5620` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x165ec5c`, `0x14c9024`, `0x109abe4`, `0x156dd34`, `0x156b760`, `0x1303a84`, `0x10d6864`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnKilled"` |

The game packet header's `netID` names the player this call is about.

gurotopia: `include/action/respawn.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnKilled" }, pPeer->netid);
```
