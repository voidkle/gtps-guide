Sets the state of a player's Balloon Bunny item effect. The value is only stored on the avatar (avatar+0x27a4); where
it is used wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | effect state |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnBalloonBunnyUpdate(NetAvatar *a, VariantList *vl) {
    a->balloonBunny = vl[1].i;                                             // avatar+0x27a4
}
```

<small>Handler: `0x12f7e14` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
