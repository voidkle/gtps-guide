# UpdateOwnedRespawnAnim

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client which respawn animations the player owns, as a bit mask. If the animation the player
currently uses isn't in the mask, it is reset to 0 (the default).

| # | Type | Meaning |
|---|---|---|
| 1 | int | bit mask: bit *n−1* set = animation *n* owned |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

- The mask goes into the app variable `OwnedRespawnAnim` (as int).
- The check is `mask >> ((current − 1) & 31) & 1`. With the current animation at 0 this tests bit 31, so a mask
  without bit 31 also "resets" an already-default animation (no visible change).
- On reset, the look, avatar+0x2868 and the app variable `respawnAnim` all become 0.

### Decompiled handler

```c
void NetAvatar::UpdateOwnedRespawnAnim(NetAvatar *a, VariantList *vl) {
    int owned = vl[1].i;
    GetApp()->GetVar("OwnedRespawnAnim")->SetINT(owned);
    if (((owned >> ((a->respawnAnim - 1) & 31)) & 1) == 0) {         // avatar+0x2868
        a->look.SetRespawnAnim(0);                                 // 0x14ce8f0
        a->respawnAnim = 0;
        GetApp()->GetVar("respawnAnim")->SetUINT(a->look.RespawnAnim());
    }
}
```

<small>Handler: `0x12f6b44` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce8f0`, `0x14ce844`, `0x107fe7c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "UpdateOwnedRespawnAnim", 1 }, pPeer->netid);
```
