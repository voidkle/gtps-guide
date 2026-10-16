Turns a player's fashion-show mode on or off (the player in the CALL_FUNCTION header's `netID`). The flag
is stored; what it changes wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | non-zero = on (avatar+0x369b) |

### Decompiled handler

```c
void NetAvatar::OnFashionShowUpdate(VariantList *args) {   // 0x12f98b0
    this->fashionShow = args->GetInt(0) != 0;              // avatar+0x369b
}
```

<small>Handler: `0x12f98b0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
