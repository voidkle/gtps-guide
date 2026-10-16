Stores a number on a player's Pineapple Pizza Paddle (the player in the CALL_FUNCTION header's `netID`).
The client logs `pineappleindex %d` with it, so it's an index, probably which pizza or style the paddle shows.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the index, stored at avatar+0x3544 |

### Decompiled handler

```c
void NetAvatar::OnPineapplePizzaPaddleUpdate(VariantList *args) {   // 0x12f930c
    LogMsg("pineappleindex %d", args->GetInt(0));
    this->pineappleIndex = args->GetInt(0);                          // avatar+0x3544
}
```

<small>Handler: `0x12f930c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
