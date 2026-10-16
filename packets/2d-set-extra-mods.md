# 0x2d SET_EXTRA_MODS

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374068`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets three movement modifiers on a player from the first byte of the extra data ("extra mods"). The bits are
stored on the avatar and read by the movement and jump code.

| Field | Used as |
|---|---|
| `netID` | the player; ignored if they aren't in the world |
| `extraDataLength` | must be non-zero, otherwise the packet is ignored |

### Extra data

One byte:

| Bit | Stored at | Read by |
|---|---|---|
| 0 | avatar+0x191 | **charged jump.** While you stand on the ground holding jump, the movement code (`0x130429c`) charges avatar+0xb8 up to 1.0 over one second. The jump code (`0x13045d4`) then scales the jump by charge × 1.25 instead of 1 |
| 1 | avatar+0x192 | a half-second timer in the movement helper `0x13040dc`, keyed by a value its caller (`0x1303b64`) passes; without the bit the helper resets it. The gameplay effect wasn't identified |
| 2 | avatar+0x198 | **air jump.** On every landing (`0x12f9fd0`) the avatar gets one jump in the air (avatar+0x199); the jump code uses it up |

The whole byte is also kept at avatar+0x190. A [0x14](./14-set-character-state) for the same player clears all of them.

### Decompiled handler

```c
case 0x2d: {
    NetAvatar *p = GetAvatar(pkt->netID);
    if (!p || pkt->extraDataLength == 0) break;
    u8 b = extra[0];
    p->moveFlags = b;                 // avatar+0x190
    p->moveFlag0 = b & 1;             // avatar+0x191
    p->moveFlag1 = (b >> 1) & 1;      // avatar+0x192
    p->moveFlag2 = (b >> 2) & 1;      // avatar+0x198
}
```

<small>Handler: `0x1374068` (switch case) → `0x13131d4` in the 5.60 arm64 client.</small>

## Official client

**Received:** handled at `0x1374068` in the incoming switch (`0x1373e20`).
