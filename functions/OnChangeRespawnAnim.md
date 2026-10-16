# OnChangeRespawnAnim

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets which respawn animation a player uses. The value is stored twice: in the avatar's look (avatar+0x2f8) and at
avatar+0x2868.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | respawn animation id; 0 = default |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variable `respawnAnim` is set as well, for whichever player it's sent for.
[UpdateOwnedRespawnAnim](/functions/UpdateOwnedRespawnAnim) resets it to 0 if the player doesn't own that animation.

### Decompiled handler

```c
void NetAvatar::OnChangeRespawnAnim(NetAvatar *a, VariantList *vl) {
    a->look.SetRespawnAnim(vl[1].u);                               // 0x14ce8f0 (avatar+0x2f8)
    a->respawnAnim = vl[1].u;                                        // avatar+0x2868
    GetApp()->GetVar("respawnAnim")->SetUINT(a->look.RespawnAnim()); // 0x14ce844
}
```

<small>Handler: `0x12f68c4` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce8f0`, `0x14ce844`, `0x107fe7c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangeRespawnAnim", 1u }, pPeer->netid);
```
