Sets the look of a player's Infinity Weapon (the player in the CALL_FUNCTION header's `netID`), stored in the
weapon's settings (avatar+0x2db0). The client only stores the values; their visual meaning wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = on (settings+0x24) |
| 2 | string | two numbers `a,b`: a → settings+0x28 (0 becomes 1), b → settings+0x8 |
| 3 | string | three numbers `,`-separated → settings+0xc, +0x14, +0x1c; probably colors (`strtoul(…, 0)`) |
| 4 | string | three numbers → settings+0x10, +0x18, +0x20; probably colors |
| 5 | string | two numbers → settings+0, +4 |

The strings must have the listed number of parts; the client doesn't check the count. A "has settings" flag
(settings+0x2c) is set.

### Decompiled handler

```c
void NetAvatar::OnInfinityWeapon(VariantList *args) {  // 0x12f9268
    InfinityWeapon_Set(&this->infinityWeapon, args);    // avatar+0x2db0, 0x12081f0
}

void InfinityWeapon_Set(Weapon *s, VariantList *args) {     // 0x12081f0
    s->on = args->GetUInt(0) != 0;                      // +0x24
    auto p = Split(args->GetString(1), ',');
    s->v28 = strtoul(p[0]); s->v08 = strtoul(p[1]);
    if (s->v28 == 0) s->v28 = 1;
    auto a = Split(args->GetString(2), ',');  s->c[0] = strtoul(a[0]); s->c[2] = strtoul(a[1]); s->c[4] = strtoul(a[2]);
    auto b = Split(args->GetString(3), ',');  s->c[1] = strtoul(b[0]); s->c[3] = strtoul(b[1]); s->c[5] = strtoul(b[2]);
    auto c = Split(args->GetString(4), ',');  s->v00 = atoi(c[0]); s->v04 = atoi(c[1]);   // 0x1e6d44c
    s->set = true;                                      // +0x2c
}
```

<small>Handler: `0x12f9268` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x12081f0`, `0x1e6d860`, `0x1e6d44c`.</small>

<!-- args: uint,string,string,string,string -->
