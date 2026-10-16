# OnAvatarBePaintBalled

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

A player is hit by paint shot by another player. A paint particle flies from the shooter to the target, and the
target stays painted for 60 seconds.

| # | Type | Meaning |
|---|---|---|
| 1 | int | paint bucket item id: 3478 Red, 3480 Yellow, 3482 Green, 3484 Aqua, 3486 Blue, 3488 Purple, 3490 Charcoal, 3492 Varnish |
| 2 | int | the shooter's netID |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` is the player who gets
painted; the call is dropped if that player isn't in the world.

- If the shooter isn't in the world, the client logs `NetAvatar::OnAvatarBePaintBalled sourceNetID is invalid=%d`
  and does nothing.
- The colour comes from `GetPaintballColor` (`0x1903a44`). Other ids log
  `ParticleEmitter::GetPaintballColor() un-defined color` and give 0.
- `audio/thwoop.wav` plays at most once every 150 ms per target. Particle 209 starts at the shooter's centre and
  heads for the target's centre.
- If the shooter's avatar+0x27ec is 115, the shooter also turns to aim at the target (`0x10df9fc`).
- The paint colour is stored at avatar+0x321c and stays until now + 60000 ms (avatar+0x3220).

### Decompiled handler

```c
void NetAvatar::OnAvatarBePaintBalled(NetAvatar *a, VariantList *vl) {
    int item = vl[1].i, src = vl[2].i;
    NetAvatar *s = dynamic_cast<NetAvatar*>(GetAvatar(src));      // 0x1342f40
    if (!s) { Log("NetAvatar::OnAvatarBePaintBalled sourceNetID is invalid=%d", src); return; }
    a->paintColor = GetPaintballColor(item, false);                // 0x1903a44, avatar+0x321c
    CL_Vec2f from = s->Center(), to = a->Center();
    if (a->nextThwoop < GetTick()) {                               // avatar+0x168
        a->nextThwoop = GetTick() + 150;
        a->PlaySound("audio/thwoop.wav");
    }
    int p = SpawnParticle((float)item, renderer + 0x178, 209, &from, 0);   // 0x1912570
    Particle *pp = FindParticle(renderer + 0x178, p);              // 0x190cedc
    if (pp) pp->target = to;                                       // +0xb8
    if (s->f_27ec == 115) s->visual.AimAt(&from, &to);             // 0x10df9fc
    a->paintUntil = GetTick() + 60000;                             // avatar+0x3220
}
```

<small>Handler: `0x12f7ee8` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1903a44`, `0x1912570`, `0x190cedc`, `0x10df9fc`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnAvatarBePaintBalled", 1, 1 }, pPeer->netid);
```
