# OnRiftCape

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the look of a player's Rift Cape (the player in the CALL_FUNCTION header's `netID`). The values are
stored in the cape's settings (avatar+0x2ca0) and used when drawing it. The client only stores the bits;
what each one shows wasn't traced. The "probably" names below follow the options of the Rift Cape's
settings dialog in the official game.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | option bits, see below |
| 2 | uint | color 1 (settings+0x10); probably cape color 1, RGBA |
| 3 | uint | color 2 (settings+0x14); probably collar color 1 |
| 4 | uint | color 3 (settings+0x18); probably cape color 2 |
| 5 | uint | color 4 (settings+0x1c); probably collar color 2 |
| 6 | uint | stored as a float (settings+0x24); probably the time-cycle length |

Argument 1 bits:

| Bits | Stored as |
|---|---|
| 0–7 | eight on/off flags, settings+0 … +7 (bit n → byte n) |
| 8–9 | a choice (settings+8): 1 → 0, 2 → 1, 3 → 2, 0 → none (−1); probably the first aura style |
| 10–11 | a choice (settings+0xc), same coding; probably the second aura style |
| 12 | a flag (settings+0x20); probably "time dilation" |

### Decompiled handler

```c
void NetAvatar::OnRiftCape(VariantList *args) {      // 0x12f9238
    RiftCapeSettings_Set(&this->riftCape, args);      // avatar+0x2ca0, 0x120fa50
}

void RiftCapeSettings_Set(RiftCape *s, VariantList *args) {    // 0x120fa50
    uint f = args->GetUInt(0);
    for (int i = 0; i < 8; i++) s->flag[i] = (f >> i) & 1;
    s->choiceA = Choice((f >> 8) & 3);                 // 1→0, 2→1, 3→2, 0→-1
    s->choiceB = Choice((f >> 10) & 3);
    s->flag12  = (f >> 12) & 1;                        // +0x20
    s->color[0] = args->GetUInt(1);  s->color[1] = args->GetUInt(2);
    s->color[2] = args->GetUInt(3);  s->color[3] = args->GetUInt(4);
    s->time = (float)args->GetUInt(5);                 // +0x24
}
```

<small>Handler: `0x12f9238` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x120fa50`. Drawing code that reads the settings: `0x1537b04`, `0x189e518`, `0x18ac91c` (not traced).</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRiftCape", 1u, 1u, 1u, 1u, 1u, 1u }, pPeer->netid);
```
