Sets the style of a player's Plasma Globe Heart effect.

| # | Type | Meaning |
|---|---|---|
| 1 | int | style |
| 2 | int | 0 = apply now; ≠ 0 = only store it (avatar+0x2c50) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

"Apply now" writes the style into two fields of the avatar's visuals and sets a "changed" flag there
(`0x10dedf4`). Where the stored value is used wasn't traced.

### Decompiled handler

```c
void NetAvatar::OnChangePlasmaGlobeHeartStyle(NetAvatar *a, VariantList *vl) {
    int style = vl[1].i;
    if (vl[2].i != 0) a->plasmaHeartStyle = style;                 // avatar+0x2c50
    else a->visual.SetPlasmaHeartStyle(style);                     // 0x10dedf4
}
```

<small>Handler: `0x12f6ce8` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x10dedf4`.</small>

<!-- args: int,int -->
