Puts a player in a disguise, or takes it off.

| # | Type | Meaning |
|---|---|---|
| 1 | int | disguise id; 0 = no disguise |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

- **Non-zero:** the id is stored (avatar+0x3630), three flags are set (avatar+0x31f8, +0x2787, +0x2790), and bits
  0x14 are added to avatar+0x274c.
- **Zero** (`0x12ec654`):
  - the tile the disguise was attached to (avatar+0x3628) gets its saved background id back;
  - the id and the three flags are cleared, and bits 0x14 removed;
  - the disguise's particle effect, if any, is stopped.

### Decompiled handler

```c
void NetAvatar::OnDisguiseChanged(NetAvatar *a, VariantList *vl) {
    int id = vl[1].i;
    a->disguise = id;                                              // avatar+0x3630
    if (id) {
        a->f_31f8 = 1; a->f_2787 = 1; a->f_2790 = 1;
        a->f_274c |= 0x14;
    } else {
        a->EndDisguise();                                          // 0x12ec654
    }
}

void NetAvatar::EndDisguise(NetAvatar *a) {                        // 0x12ec654
    if (a->disguiseTile) a->disguiseTile->bg = a->savedBg;         // +0x3628, tile+0x50 ← +0x3634
    a->disguise = 0;
    sub_11b4620(sub_11b25a4(), a->disguiseTile);
    a->disguiseTile = NULL;
    a->f_31f8 = a->f_2787 = a->f_2790 = 0;
    a->f_274c &= ~0x14;
    ... release shared object at +0x3648 ...
    if (a->disguiseParticle != -1) stop particle a->disguiseParticle; // +0x3638
}
```

<small>Handler: `0x12f7e64` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x12ec654`.</small>

<!-- args: int -->
