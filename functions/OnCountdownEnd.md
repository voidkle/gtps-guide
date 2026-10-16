# OnCountdownEnd

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Stops a player's countdown and forgets the two challenge tiles set by [OnChallengeFlags](/functions/OnChallengeFlags).
No arguments are read.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnCountdownEnd(NetAvatar *a, VariantList *vl) {
    a->countdown = 0;                                              // avatar+0x70
    a->challengeTile1 = NULL;                                      // avatar+0x3598
    a->challengeTile2 = NULL;                                      // avatar+0x35a0
}
```

<small>Handler: `0x12f7794` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnCountdownEnd" }, pPeer->netid);
```
