# OnFactionDataChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's faction data and bounty.

| # | Type | Meaning |
|---|---|---|
| 1 | int | stored at avatar+0x260 (probably the faction id) |
| 2 | int | stored at avatar+0x27c and +0x312c; 1–3 also pick a value from a 3-entry table on the avatar (+0x3138) into +0x3134, anything else gives -1 |
| 3 | int | stored at avatar+0x280 and +0x3130 |
| 4 | string | `key|value` lines; `bountyLevel|` and `bountyScore|` are read (`atoi`) into avatar+0x264 and +0x268 |
| 5 | int | ≠ 0 sets avatar+0x26c |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The meanings of arguments 2, 3 and 5 aren't in the client's strings. A missing bounty key reads as 0.

### Decompiled handler

```c
void NetAvatar::OnFactionDataChanged(NetAvatar *a, VariantList *vl) {
    a->f_260 = vl[1].i;
    int v = vl[2].i;
    a->f_27c = v; a->f_312c = v;
    a->f_3134 = (v >= 1 && v <= 3) ? a->table_3138[v - 1] : -1;
    a->f_280 = vl[3].i; a->f_3130 = vl[3].i;
    std::string data = vl[4].s;
    a->bountyLevel = atoi(GetValue(data, "bountyLevel|"));        // 0x157f12c, avatar+0x264
    a->bountyScore = atoi(GetValue(data, "bountyScore|"));        // avatar+0x268
    a->f_26c = vl[5].i != 0;
}
```

<small>Handler: `0x12f79f0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x157f12c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnFactionDataChanged", 1, 1, 1, "...", 1 }, pPeer->netid);
```
