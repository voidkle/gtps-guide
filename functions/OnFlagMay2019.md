# OnFlagMay2019

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Send it (server side)

```cpp
send_varlist(peer, { "OnFlagMay2019", 1u }, pPeer->netid);
```
