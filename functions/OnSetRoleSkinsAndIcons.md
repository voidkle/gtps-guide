# OnSetRoleSkinsAndIcons

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's role skin and role icon (the role system: farmer, builder, …). The skin is applied
to the avatar at once.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | role skin id |
| 2 | uint | role icon id |
| 3 | int | ≠ 0: redraw the avatar's clothes now |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variables `roleSkin` and `roleIcon` are also set to these values. This happens for every player it is
sent for, not only you. The two single-value versions are [OnChangeRoleSkin](/functions/OnChangeRoleSkin) and
[OnChangeRoleIcon](/functions/OnChangeRoleIcon).

### Decompiled handler

```c
void NetAvatar::OnSetRoleSkinsAndIcons(NetAvatar *a, VariantList *vl) {
    a->look.SetRoleSkin(vl[1].u);                                  // 0x14ce854 (avatar+0x2f8)
    a->visual.ApplyRoleSkin(a->look.RoleSkin());                   // 0x109b6cc (avatar+0x330)
    a->roleIcon = vl[2].u;                                         // avatar+0x3624
    if (vl[3].i) a->visual.RefreshClothes(a);                      // 0x1098f88
    GetApp()->GetVar("roleSkin")->SetUINT(a->look.RoleSkin());
    GetApp()->GetVar("roleIcon")->SetUINT(vl[2].u);
}
```

<small>Handler: `0x12f6334` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce854`, `0x14ce84c`, `0x109b6cc`, `0x1098f88`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetRoleSkinsAndIcons", 1u, 1u, 1 }, pPeer->netid);
```
