Stores one number on a player (the CALL_FUNCTION header's `netID`), at avatar+0x274. By the name, probably
a setting for the client's spike/hazard death check; the code that reads it wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | stored at avatar+0x274 |

### Decompiled handler

```c
void NetAvatar::OnSetSpikeCheck(VariantList *args) {   // 0x12f8e14
    this->spikeCheck = args->GetInt(0);                // avatar+0x274
}
```

<small>Handler: `0x12f8e14` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
