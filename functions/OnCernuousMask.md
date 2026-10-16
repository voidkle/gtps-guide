# OnCernuousMask

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the look of a player's Cernuous Mask (the player in the CALL_FUNCTION header's `netID`), stored in its settings (avatar+0x2de4).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | a style number 0–4 → settings+0 |
| 2 | uint | a second number 0–4 → settings+4 |

If either value is 5 or more, settings+0 becomes 2 instead of argument 1. Argument 2 is stored as sent
either way. What the values show wasn't traced.

### Decompiled handler

```c
void NetAvatar::OnCernuousMask(VariantList *args) {      // 0x12f92b0
    uint a = args->GetUInt(0), b = args->GetUInt(1);      // setter 0x11ff330
    this->cernuousMask.a = (a < 5 && b < 5) ? a : 2;      // avatar+0x2de4
    this->cernuousMask.b = b;                             // avatar+0x2de8
}
```

<small>Handler: `0x12f92b0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x11ff330`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnCernuousMask", 1u, 1u }, pPeer->netid);
```
