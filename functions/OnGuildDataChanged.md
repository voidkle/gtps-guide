# OnGuildDataChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's guild data: four numbers stored on the avatar. When the call is for your own avatar, the screen
in mode 0x29 is rebuilt if it's open (probably the guild screen).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | avatar+0x8c (probably the guild id) |
| 2 | uint | avatar+0x90 |
| 3 | uint | avatar+0x94 |
| 4 | uint | avatar+0x98 |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

"Your own avatar" means its avatar+0x12c equals the local avatar's.

### Decompiled handler

```c
void NetAvatar::OnGuildDataChanged(NetAvatar *a, VariantList *vl) {
    a->guild[0] = vl[1].u;                                         // avatar+0x8c
    a->guild[1] = vl[2].u;                                         // +0x90
    a->guild[2] = vl[3].u;                                         // +0x94
    a->guild[3] = vl[4].u;                                         // +0x98
    NetAvatar *me = GetGameLogic()->GetLocalAvatar();              // 0x1373e18
    if (me && a->f_12c == me->f_12c) {
        Menu *m = sub_11b25a4();
        if (m->mode == 0x29) m->Rebuild(0x29);                     // 0x11a3bd8 → 0x11a2fb0
    }
}
```

<small>Handler: `0x12f7ca4` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x11a3bd8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnGuildDataChanged", 1u, 1u, 1u, 1u }, pPeer->netid);
```
