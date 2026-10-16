# OnWepSfx

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's custom sound effects (for example, from a weapon they hold). Three strings are stored on the
avatar. An empty string means "use the default".

| # | Type | Meaning |
|---|---|---|
| 1 | string | stored at avatar+0x200; where it is used wasn't traced |
| 2 | string | punch sound; empty = `audio/punch.wav` (read at `0x10d7864`) |
| 3 | string | stored at avatar+0x230; while it's set, [OnKilled](/functions/OnKilled) skips `audio/male_scream.wav` (probably the death sound) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The strings are copied without a type check.

### Decompiled handler

```c
void NetAvatar::OnWepSfx(NetAvatar *a, VariantList *vl) {
    a->sfx1       = vl[1].s;                                       // avatar+0x200
    a->punchSfx   = vl[2].s;                                       // avatar+0x218
    a->deathSfx   = vl[3].s;                                       // avatar+0x230
}
```

<small>Handler: `0x12f769c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; readers: `0x10d7810` (punch), `0x12f5620` (OnKilled).</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnWepSfx", "...", "...", "..." }, pPeer->netid);
```
