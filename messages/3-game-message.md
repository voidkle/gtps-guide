# 3 GAME_MESSAGE

<Badge type="info" text="message type" /> <Badge type="tip" text="both" />

Text actions. The client sends a few actions as type 3 (`join_request`, `quit`, ...); the server sends commands such as `action|log` and `action|play_sfx`, listed on [Text commands from the server](/guide/server-text).

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Text actions in both directions. Every `action|...` page on this site is one the client sends. From the
server, the client needs `action|` as the first key; otherwise it logs "bad net game message". What it
does with each action is on [Text commands from the server](/guide/server-text).

The client reads text from the server (types 3, 5 and 6) with `0x157f908`, which **overwrites the last
byte** of the message with a NUL. So the server must add one extra byte (a `\0`) after the text, or the
last character is lost.

<small>Case 3 of the dispatcher `0x114276c` → `0x1372d28`.</small>

## Layout

```text
[u32 3][key|value\n ... ][\0]
```

The trailing NUL is required by gurotopia, which drops the last byte (`receive.cpp`).

gurotopia: `include/eventType/receive.cpp`.
