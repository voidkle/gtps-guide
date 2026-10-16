Sets the look of a player's Infinity Aura (the player in the CALL_FUNCTION header's `netID`), stored in the
aura's settings (avatar+0x2d78). The client only stores the values; their visual meaning wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | option bits: bit n (n = 0…13) → settings+n, bit 14 → settings+0x28 |
| 2 | uint | a number, at least 1 (0 and 1 both become 1) → settings+0x2c |
| 3 | string | three numbers separated by `,` → settings+0x10, +0x18, +0x20; probably colors (`strtoul(…, 0)`, hex with `0x` works) |
| 4 | string | three numbers separated by `,` → settings+0x14, +0x1c, +0x24; probably colors |

Each string must have three parts; the client reads parts 0–2 without checking the count.
A "has settings" flag (settings+0x30) is set.

### Decompiled handler

```c
void NetAvatar::OnInfinityAura(VariantList *args) {    // 0x12f925c
    InfinityAura_Set(&this->infinityAura, args);        // avatar+0x2d78, 0x12036ec
}

void InfinityAura_Set(Aura *s, VariantList *args) {    // 0x12036ec
    uint f = args->GetUInt(0);
    s->flag14 = f >> 14 & 1;                            // +0x28
    uint n = args->GetUInt(1);  s->value = n < 2 ? 1 : n;   // +0x2c
    auto a = Split(args->GetString(2), ',');
    s->c[0] = strtoul(a[0]); s->c[2] = strtoul(a[1]); s->c[4] = strtoul(a[2]);   // +0x10, +0x18, +0x20
    auto b = Split(args->GetString(3), ',');
    s->c[1] = strtoul(b[0]); s->c[3] = strtoul(b[1]); s->c[5] = strtoul(b[2]);   // +0x14, +0x1c, +0x24
    for (int i = 0; i < 14; i++) s->b[i] = f >> i & 1;  // +0 .. +0xd
    s->set = true;                                      // +0x30
}
```

<small>Handler: `0x12f925c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x12036ec`, `0x1e6d860`.</small>

<!-- args: uint,uint,string,string -->
