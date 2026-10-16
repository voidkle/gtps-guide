Turns a player's Super Supporter state on or off. It is stored as bit 24 of a flags word on the avatar
(avatar+0x170).

| # | Type | Meaning |
|---|---|---|
| 1 | int | ≠ 0 = Super Supporter |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

### Decompiled handler

```c
void NetAvatar::OnSuperSupportState(NetAvatar *a, VariantList *vl) {
    a->flags170 = (a->flags170 & ~(1u << 24)) | ((vl[1].i != 0) << 24);   // avatar+0x170
}
```

<small>Handler: `0x12f7650` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
