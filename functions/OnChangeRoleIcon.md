# OnChangeRoleIcon

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's role icon. Same as the second argument of [OnSetRoleSkinsAndIcons](/functions/OnSetRoleSkinsAndIcons).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | role icon id |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variable `roleIcon` is set too, for whichever player it's sent for.

### Decompiled handler

```c
void NetAvatar::OnChangeRoleIcon(NetAvatar *a, VariantList *vl) {
    a->roleIcon = vl[1].u;                                         // avatar+0x3624
    GetApp()->GetVar("roleIcon")->SetUINT(vl[1].u);
}
```

<small>Handler: `0x12f6f38` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangeRoleIcon", 1u }, pPeer->netid);
```
