# OnRiftWings

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the look of a player's Rift Wings (the player in the CALL_FUNCTION header's `netID`), stored in the
wings' settings (avatar+0x2ce4). The client only stores the values; what each bit shows wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | option bits, see below |
| 2 | uint | color 1 (settings+0x18), probably RGBA |
| 3 | uint | color 2 (settings+0x1c) |
| 4 | uint | color 3 (settings+0x20) |
| 5 | uint | color 4 (settings+0x24) |
| 6 | uint | a number (settings+0x2c); probably a time or speed |

Argument 1 bits:

| Bits | Stored as |
|---|---|
| 2, 3, 0 | flags at settings+0, +1, +2 |
| 1, 4, 5, 6 | flags at settings+3, +4, +5, +6 |
| 7 | flag at settings+7 |
| 8–9, 10–11, 12–13, 14–15 | four choices (settings+8, +0xc, +0x10, +0x14): 1 → 0, 2 → 1, 3 → 2, 0 → none (−1) |
| 16 | flag at settings+0x28 |

A "has settings" flag (settings+0x30) is set.

### Decompiled handler

```c
void NetAvatar::OnRiftWings(VariantList *args) {      // 0x12f9244
    RiftWingsSettings_Set(&this->riftWings, args);     // avatar+0x2ce4, 0x1212ce4
}

void RiftWingsSettings_Set(RiftWings *s, VariantList *args) {  // 0x1212ce4
    uint f = args->GetUInt(0);
    s->b[0] = f >> 2 & 1;  s->b[1] = f >> 3 & 1;  s->b[2] = f & 1;
    s->b[3] = f >> 1 & 1;  s->b[4] = f >> 4 & 1;  s->b[5] = f >> 5 & 1;  s->b[6] = f >> 6 & 1;
    s->b[7] = f >> 7 & 1;
    s->choice[0] = Choice(f >> 8 & 3);  s->choice[1] = Choice(f >> 10 & 3);
    s->choice[2] = Choice(f >> 12 & 3); s->choice[3] = Choice(f >> 14 & 3);
    s->flag16 = f >> 16 & 1;                                       // +0x28
    for (int i = 0; i < 4; i++) s->color[i] = args->GetUInt(1 + i);   // +0x18..+0x24
    s->value = args->GetUInt(5);                                   // +0x2c
    s->set = true;                                                 // +0x30
}
```

<small>Handler: `0x12f9244` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1212ce4`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRiftWings", 1u, 1u, 1u, 1u, 1u, 1u }, pPeer->netid);
```
