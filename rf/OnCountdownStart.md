Starts a countdown on a player. Every frame the avatar update lowers the value by the elapsed time, until it
reaches 0 (`0x1306014`).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | countdown length, probably in seconds (stored as a float at avatar+0x70) |
| 2 | int | stored at avatar+0x6c; where it is used wasn't traced |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

[OnCountdownEnd](/functions/OnCountdownEnd) stops it. [OnChallengeFlags](/functions/OnChallengeFlags) sets the
two tiles that OnCountdownEnd clears.

### Decompiled handler

```c
void NetAvatar::OnCountdownStart(NetAvatar *a, VariantList *vl) {
    a->countdown = (float)vl[1].u;                                 // avatar+0x70
    a->countdownArg = vl[2].i;                                     // avatar+0x6c
}
```

<small>Handler: `0x12f770c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; reader: `0x1306014` (per-frame update).</small>

<!-- args: uint,int -->
