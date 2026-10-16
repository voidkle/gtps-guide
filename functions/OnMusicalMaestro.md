# OnMusicalMaestro

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the style of a player's Musical Maestro item (the player in the CALL_FUNCTION header's `netID`), stored in its settings (avatar+0x2d2c). The client only stores the number; what each value does wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored at settings+0; probably the selected style or instrument |

A "has settings" flag (settings+4) is set.

### Decompiled handler

```c
void NetAvatar::OnMusicalMaestro(VariantList *args) {    // 0x12f928c
    this->musicalMaestro.value = args->GetUInt(0);        // avatar+0x2d2c, setter 0x120c8bc
    this->musicalMaestro.set = true;                      // +4
}
```

<small>Handler: `0x12f928c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x120c8bc`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnMusicalMaestro", 1u }, pPeer->netid);
```
