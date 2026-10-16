Stops a player's race timer by clearing the start time set by [OnRaceStart](/functions/OnRaceStart). No
arguments are read.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnRaceEnd(NetAvatar *a, VariantList *vl) {
    a->raceStart = 0;                                              // avatar+0x68
}
```

<small>Handler: `0x12f7704` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: -->
