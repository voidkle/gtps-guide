# 2 GENERIC_TEXT

<Badge type="info" text="message type" /> <Badge type="info" text="client → server" />

Text from the client: the two login messages and most `action|...` messages (each action page says which type it uses). See the two login pages.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The client only **sends** this type (its login text). If a server sends it, the client logs
"Got unknown packet type: 2" and drops it.

How the client sends text (`0x157f060`, used for types 2 and 3):

```text
u32 type | the text bytes | 1 byte the client doesn't write
```

The ENet packet is one byte longer than the text, and the client doesn't write that last byte, so a
server should drop it (gurotopia does). Sent reliable.

<small>Sender: `0x157f060` (125 callers send type 2, 10 send type 3).</small>

## Layout

```text
[u32 2][key|value\n ... ][\0]
```

The trailing NUL is required by gurotopia, which drops the last byte (`receive.cpp`).

gurotopia: `include/eventType/receive.cpp`.
