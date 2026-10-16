Sets what a player's Piano Wings play (the player in the CALL_FUNCTION header's `netID`). Probably the tune:
the string is stored as is and read elsewhere (`0x1095a44` and nearby), which wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | string | stored at avatar+0x27b0; probably the notes to play |
| 2 | int | stored at avatar+0x27ac |
| 3 | int | 1 = on (avatar+0x27cc); anything else = off |

The playback position (avatar+0x27c8) is reset to 0.

### Decompiled handler

```c
void NetAvatar::OnPianoWingsUpdate(VariantList *args) {   // 0x12f9020
    this->piano.tune  = args->GetString(0);               // avatar+0x27b0
    this->piano.pos   = 0;                                 // avatar+0x27c8
    this->piano.value = args->GetInt(1);                   // avatar+0x27ac
    this->piano.on    = args->GetInt(2) == 1;              // avatar+0x27cc
}
```

<small>Handler: `0x12f9020` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: string,int,int -->
