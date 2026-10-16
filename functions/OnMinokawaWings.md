# OnMinokawaWings

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the style of a player's Minokawa Wings (the player in the CALL_FUNCTION header's `netID`), stored in its settings (avatar+0x2d40). The client only stores the number; what each value shows wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored at settings+4; probably the style |

A "has settings" flag (settings+0) is set.

### Decompiled handler

```c
void NetAvatar::OnMinokawaWings(VariantList *args) {     // 0x12f9298
    this->minokawaWings.value = args->GetUInt(0);         // avatar+0x2d44, setter 0x120980c
    this->minokawaWings.set = true;                       // avatar+0x2d40
}
```

<small>Handler: `0x12f9298` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x120980c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnMinokawaWings", 1u }, pPeer->netid);
```
