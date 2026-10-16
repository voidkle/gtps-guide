# 0x15 PING_REPLY

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="confirmed" />

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `netID` | your state bits |
| `targetNetID` | hash of the request's `itemID` (the challenge) |
| `itemID` | client tick in ms |
| `pos` | reach with the Fist (x) and with other items (y), in pixels |
| `speed` | physics values from the last 0x14 |
| `...` | full layout on [0x16 PING_REQUEST](/packets/16-ping-request#the-reply-the-client-builds) |

## gurotopia

`include/gamePacket/ping_reply.cpp` only logs it.

## Official client

**Received:** ignored (falls to the switch's default).

**Sent:** Sent from inside the client's server-packet handler.
