# OnChangeAirBalloonStyle

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the style of a player's air balloon effect. The value is only stored on the avatar (avatar+0x2bf4); where it is used wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | balloon style |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnChangeAirBalloonStyle(NetAvatar *a, VariantList *vl) {
    a->airBalloonStyle = vl[1].i;                                  // avatar+0x2bf4
}
```

<small>Handler: `0x12f6d8c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangeAirBalloonStyle", 1 }, pPeer->netid);
```
