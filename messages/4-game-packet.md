# 4 GAME_PACKET

<Badge type="info" text="message type" /> <Badge type="tip" text="both" />

Binary game packets: the 56-byte header plus optional extra data. See [Game packet header](/guide/game-packet) and the Game packets section.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Binary game packets. Before handing one to the game packet switch (`0x1373e20`), the client checks the size
(`0x157eff0`):

- the message must be at least 60 bytes (u32 type + the 56-byte header), else it logs "Got bad tank packet"
  and drops it;
- if the header's flags have `S_EXTENDED` (0x08), the message must hold `60 + extraDataLength` bytes, else it
  logs "Packet too small for extended packet to be valid" and drops it;
- without `S_EXTENDED`, `extraDataLength` is set to 0 and any extra bytes are ignored.

```c
GameHeader *GetGamePacket(ENetPacket *p) {                        // 0x157eff0
    if (p->dataLength < 0x3c) return NULL;
    GameHeader *h = (GameHeader *)(p->data + 4);
    if (!(h->flags & 0x08)) { h->extraDataLength = 0; return h; }
    if (p->dataLength < h->extraDataLength + 0x3c) {
        Log("Packet too small for extended packet to be valid"); return NULL;
    }
    return h;
}
```

<small>Case 4 of the dispatcher `0x114276c`.</small>

## Layout

```text
[u32 4][56-byte header][extraDataLength bytes]
```

gurotopia: `include/eventType/receive.cpp`.
