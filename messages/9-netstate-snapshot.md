# 9 NETSTATE_SNAPSHOT

<Badge type="info" text="message type" /> <Badge type="info" text="server → client" />

A binary state snapshot for the client's "NetState" system, used only in some worlds (probably PvE / dungeon). The name is this site's; the client has none.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Server → client**, a binary state snapshot for the client's "NetState" system (its logs use that name).
It goes with the [type 10 and 11](/messages/10-netstate-frame) messages the client sends in worlds that use this system (worlds with
flag 0x200 in world+0x1a0, or bit 0 of the version-27 trailer int, see [World data](/guide/world-data));
probably the PvE / dungeon worlds. Neither gurotopia nor GrowServer uses it.

Layout after the `u32 9`:

| Bytes | Field | Meaning |
|---|---|---|
| u32 | tick | the snapshot's time |
| u8 n | count | at most 100 |
| n × 8 bytes | entries A | keyed by their first byte (an id); merged into the snapshot with the same tick. Meaning not traced |
| u8 m | count | at most 100 |
| m × 24 bytes | player states | keyed by their first byte (a netID), see below |

Player state (24 bytes), as the client applies it to **your own** avatar (`0x1b3bfac`):

| Offset | Size | Meaning |
|---|---|---|
| 0 | u8 | netID |
| 3 | u8 | a value used as a 0–1 fraction (/255) |
| 4 | u32 | the last input number the server processed. The client drops inputs up to it and replays the later ones, so this is probably server reconciliation of client-side prediction |
| 8 | u32 | not traced |
| 14, 16 | u16, u16 | position (unsigned) |
| 18, 20 | i16, i16 | velocity |
| 22 | u8 | a second 0–1 fraction (/255) |
| 23 | u8 | not traced |

What the client does:

- An older tick than the newest buffered one is skipped ("Skip snapshot. Snapshot time: {}, comparisonTime {}").
- The same tick is merged into that snapshot (entries with the same key are replaced).
- A newer tick is added to a ring buffer, and the client sets its clock to `tick − 250`.
- More than 100 entries throws "Snapshot target array capacity exceeded".
- Only the entry with your own netID is applied, and only while you're in a world.

<small>Case 9 of the dispatcher `0x114276c` → `0x1b3c7bc`; parser `0x1348d64`; merge `0x1b3caa8`, `0x1b3ccf0`; apply `0x1b3bed4` → `0x1b3bfac`.</small>

## Layout

```text
[u32 9][...]
```
