Stores one number on a player (the CALL_FUNCTION header's `netID`). Probably which flag the May 2019
event flag item shows; the code that reads it wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored at avatar+0x178 |

### Decompiled handler

```c
void NetAvatar::OnFlagMay2019(VariantList *args) {     // 0x12f8dc4
    this->flagMay2019 = args->GetUInt(0);              // avatar+0x178
}
```

<small>Handler: `0x12f8dc4` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: uint -->
