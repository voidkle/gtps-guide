# OnChangeRoleSkin

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's role skin and applies it to the avatar at once. Same as the first argument of
[OnSetRoleSkinsAndIcons](/functions/OnSetRoleSkinsAndIcons).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | role skin id |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variable `roleSkin` is set too, for whichever player it's sent for.

### Decompiled handler

```c
void NetAvatar::OnChangeRoleSkin(NetAvatar *a, VariantList *vl) {
    a->look.SetRoleSkin(vl[1].u);                                  // 0x14ce854
    a->visual.ApplyRoleSkin(a->look.RoleSkin());                   // 0x109b6cc
    GetApp()->GetVar("roleSkin")->SetUINT(a->look.RoleSkin());
}
```

<small>Handler: `0x12f6e34` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce854`, `0x14ce84c`, `0x109b6cc`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangeRoleSkin", 1u }, pPeer->netid);
```
