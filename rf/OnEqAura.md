Sets the style of a player's Eq Aura (the player in the CALL_FUNCTION header's `netID`), stored in its settings (avatar+0x2d24). The client only stores the number; what each value shows wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored at settings+0; probably the style |

A "has settings" flag (settings+4) is set.

### Decompiled handler

```c
void NetAvatar::OnEqAura(VariantList *args) {            // 0x12f9280
    this->eqAura.value = args->GetUInt(0);                // avatar+0x2d24, setter 0x1200614
    this->eqAura.set = true;                              // +4
}
```

<small>Handler: `0x12f9280` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1200614`.</small>

<!-- args: uint -->
