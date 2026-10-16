# OnTeaSoakedUpdate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a "tea soaked" flag on a player (avatar+0x29f9). No arguments are read. The handler never clears the flag,
and where it is used wasn't traced.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnTeaSoakedUpdate(NetAvatar *a, VariantList *vl) {
    a->teaSoaked = 1;                                              // avatar+0x29f9
}
```

<small>Handler: `0x12f7e04` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnTeaSoakedUpdate" }, pPeer->netid);
```
