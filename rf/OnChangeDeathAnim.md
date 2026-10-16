Sets which death animation a player uses. The value is stored twice: in the avatar's look (avatar+0x2f8) and at
avatar+0x2864.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | death animation id; 0 = default |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variable `deathAnim` is set as well, for whichever player it's sent for.
[UpdateOwnedDeathAnim](/functions/UpdateOwnedDeathAnim) resets it to 0 if the player doesn't own that animation.

### Decompiled handler

```c
void NetAvatar::OnChangeDeathAnim(NetAvatar *a, VariantList *vl) {
    a->look.SetDeathAnim(vl[1].u);                               // 0x14ce8e8 (avatar+0x2f8)
    a->deathAnim = vl[1].u;                                        // avatar+0x2864
    GetApp()->GetVar("deathAnim")->SetUINT(a->look.DeathAnim()); // 0x14ce83c
}
```

<small>Handler: `0x12f67a0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce8e8`, `0x14ce83c`, `0x107fe7c`.</small>

<!-- args: uint -->
