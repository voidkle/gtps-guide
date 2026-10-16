# OnFashionShowUpdate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Send it (server side)

```cpp
send_varlist(peer, { "OnFashionShowUpdate", 1 }, pPeer->netid);
```
