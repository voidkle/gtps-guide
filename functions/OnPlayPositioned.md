# OnPlayPositioned

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Plays a sound file at the player's position, so it is quieter the farther away that player is.

| # | Type | Meaning |
|---|---|---|
| 1 | string | sound file, e.g. `audio/punch_locked.wav` |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player (and so the
position); the call is dropped if that player isn't in the world.

The string is read without a type check, so a non-string argument plays an empty name.

### Decompiled handler

```c
void NetAvatar::OnPlayPositioned(NetAvatar *a, VariantList *vl) {
    CL_Vec2f pos = a->pos;                                         // avatar+0x8
    PlaySoundAt(GetGameLogic(), &pos, vl[1].s);                    // 0x1376d18
}
```

<small>Handler: `0x12f5548` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1376d18`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPlayPositioned", "..." }, pPeer->netid);
```
