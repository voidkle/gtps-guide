# 11 NETSTATE_RAW

<Badge type="info" text="message type" /> <Badge type="info" text="client → server" />

8 raw bytes, sent unreliable from the same world tick as type 10. The name is this site's.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Client → server**, 8 raw bytes, sent **unreliable** from the same world tick as [type 10](/messages/10-netstate-frame) (worlds
with flag 0x200 or bit 0 of the version-27 trailer int). The 8 bytes are copied from your entry in a
map at world+0x11878, keyed by your avatar's id (avatar+0xbc). They're only sent when that entry exists and
its float at +0x68 is 0 or less, probably when your character has no HP left. What the 8 bytes hold wasn't
traced. The client doesn't handle type 11 from a server ("Got unknown packet type: 11").

<small>Sender: `0x1b3ee38` (body from `0x1348c5c`), called from `0x13811d0`.</small>

## Layout

```text
[u32 11][...]
```
