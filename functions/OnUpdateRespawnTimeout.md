# OnUpdateRespawnTimeout

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets one flag on the game: on when the argument is greater than 0. The only reader traced is the
Turkey Fight Entrance tile (item 12982), which picks its animation frame from it (frame +1 while the flag
is off). Other readers weren't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | > 0 sets the flag, anything else (or missing) clears it |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

### Decompiled handler

```c
void GameLogic::OnUpdateRespawnTimeout(GameLogic *self, VariantList *vl) {
    self->respawnTimeoutFlag = vl[1].i > 0;                        // self+0x4e0, getter 0x1381e7c
}
```

<small>Handler: `0x1372408` (dispatcher `0x135e25c`) in the 5.60 arm64 client; reader: `0x11a6a9c` (tile frame, item 12982).</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnUpdateRespawnTimeout", 1 });
```
