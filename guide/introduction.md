# Introduction

This site documents every packet that the Growtopia client and a private server exchange, so you can
build a server that behaves like the real one, or write your own client and **speak to a server
directly**.

Everything here comes from three sources, and each page says which one it relies on:

- **gurotopia**: the C++ server in this repository. What it sends and accepts is confirmed by its code,
  and by running it.
- **GrowServer 4.0.0**: a TypeScript server. It speaks the same protocol, so it's used to cross-check
  field names.
- **The official Growtopia 5.60 Android client** (`libgrowtopia.so`), read with static analysis. This is
  where the full list of client actions, the login fields and the function names come from. Nothing
  from it was confirmed with live traffic yet, so those pages carry `inferred` or `unknown` badges where
  the meaning isn't certain.

## How a connection works

```text
client                                     server
  │  HTTPS POST /growtopia/server_data.php   │   (server address, port, loginurl)
  │ ───────────────────────────────────────▶ │
  │                                          │
  │  ENet connect (UDP 17091)                │
  │ ───────────────────────────────────────▶ │
  │              1 SERVER_HELLO              │
  │ ◀─────────────────────────────────────── │
  │  2 GENERIC_TEXT  protocol|..ltoken|..    │
  │ ───────────────────────────────────────▶ │
  │  4 GAME_PACKET   OnSendToServer, ...     │
  │ ◀─────────────────────────────────────── │
  │  3 GAME_MESSAGE  action|enter_game ...   │
  │ ───────────────────────────────────────▶ │
```

After the HTTPS step, everything is ENet. Every ENet packet starts with a 4-byte
[message type](/guide/message-types):

- **Text** (types 2 and 3) is `key|value` lines. Every `action|...` is one of these. See **Actions**.
- **Game packets** (type 4) are a 56-byte binary header plus optional extra data. See
  [Game packet header](/guide/game-packet) and **Game packets**.
- **Server function calls** are game packets of type `0x01` carrying a [variant list](/guide/variant-list).
  See **Server functions**.

## Where to start

- To talk to your server from your own code, read [Talk to the server](/guide/talk-to-server). It
  walks through a 130-line client that logs in, joins a world and chats.
- To watch the official client's traffic, see [Relay](/guide/relay).
- To implement a missing feature (trading, for example), open its action pages and the server
  functions the client expects back.
