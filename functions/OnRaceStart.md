# OnRaceStart

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Starts a race timer for a player: the current app tick is stored as the race start time (avatar+0x68). No
arguments are read. [OnRaceEnd](/functions/OnRaceEnd) clears it.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

[OnKilled](/functions/OnKilled) also clears the start time.

### Decompiled handler

```c
void NetAvatar::OnRaceStart(NetAvatar *a, VariantList *vl) {
    a->raceStart = GetApp()->tick;                                 // avatar+0x68, app+0x22c
}
```

<small>Handler: `0x12f76dc` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRaceStart" }, pPeer->netid);
```
