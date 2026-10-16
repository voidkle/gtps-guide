# OnChangePureBeingMode

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's "pure being" mode. Only the low byte of the value is stored (avatar+0x3300); where it is used wasn't
traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | mode (low 8 bits kept) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnChangePureBeingMode(NetAvatar *a, VariantList *vl) {
    a->pureBeingMode = (uint8_t)vl[1].u;                           // avatar+0x3300
}
```

<small>Handler: `0x12f6ddc` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangePureBeingMode", 1u }, pPeer->netid);
```
