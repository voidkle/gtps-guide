Sets the look of a player's Infinity Crown (the player in the CALL_FUNCTION header's `netID`), stored in the
crown's settings (avatar+0x2d48). The client only stores the values; their visual meaning wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | option bits, see below |
| 2 | uint | a number (settings+0x24) |
| 3 | string | three numbers separated by `,` → settings+0x8, +0x10, +0x18; probably colors (parsed with `strtoul(…, 0)`, so `0x…` hex works) |
| 4 | string | three numbers separated by `,` → settings+0xc, +0x14, +0x1c; probably colors |

Each string must have three parts; the client reads parts 0–2 without checking the count.

Argument 1 bits: bit 2 → settings+0, bit 3 → +1, bit 4 → +2, bit 5 → +3, bit 0 → +4, bit 1 → +5,
bit 6 → +6, bit 7 → +7, bit 8 → +0x20. A "has settings" flag (settings+0x28) is set.

### Decompiled handler

```c
void NetAvatar::OnInfinityCrown(VariantList *args) {   // 0x12f9250
    InfinityCrown_Set(&this->infinityCrown, args);      // avatar+0x2d48, 0x1204cd0
}

void InfinityCrown_Set(Crown *s, VariantList *args) {  // 0x1204cd0
    uint f = args->GetUInt(0);
    s->flag8 = f >> 8 & 1;                              // +0x20
    s->value = args->GetUInt(1);                        // +0x24
    auto a = Split(args->GetString(2), ',');            // 0x1e6d860
    s->c[0] = strtoul(a[0], 0, 0); s->c[2] = strtoul(a[1], 0, 0); s->c[4] = strtoul(a[2], 0, 0);   // +8, +0x10, +0x18
    auto b = Split(args->GetString(3), ',');
    s->c[1] = strtoul(b[0], 0, 0); s->c[3] = strtoul(b[1], 0, 0); s->c[5] = strtoul(b[2], 0, 0);   // +0xc, +0x14, +0x1c
    s->b[0] = f >> 2 & 1; s->b[1] = f >> 3 & 1; s->b[2] = f >> 4 & 1; s->b[3] = f >> 5 & 1;
    s->b[4] = f & 1;      s->b[5] = f >> 1 & 1; s->b[6] = f >> 6 & 1; s->b[7] = f >> 7 & 1;
    s->set = true;                                      // +0x28
}
```

<small>Handler: `0x12f9250` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1204cd0`, `0x1e6d860`.</small>

<!-- args: uint,uint,string,string -->
