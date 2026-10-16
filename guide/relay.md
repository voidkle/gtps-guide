# Relay (watching the official client)

On your own server you don't need to intercept anything to see packets:

- **Server side:** `receive()` in `include/eventType/receive.cpp` sees every packet a client sends (it
  already prints text packets), and `send_data()` / `send_varlist()` see everything the server sends.
- **Client side:** [hello.cpp](/guide/talk-to-server) prints every packet it receives.

To see what the **official app** sends, put a relay between it and your server:

```text
Growtopia app ──▶ relay :17092 ──▶ gurotopia :17091
              ◀──              ◀──
```

1. Run an ENet **server** on 17092 with `usingNewPacketForServer`, CRC32 and the range coder, and an ENet
   **client** that connects to 17091 with `usingNewPacket`, CRC32 and the range coder
   ([Transport](/guide/transport)).
2. Point the app at the relay: `port|17092` in `server_data.php`.
3. When the app connects, open a connection to the real server for it. Forward every packet in both
   directions unchanged, and log or edit what you want. Read the first 4 bytes for the
   [message type](/guide/message-types), and for type 4 the [header](/guide/game-packet).
4. Rewrite [OnSendToServer](/functions/OnSendToServer) on its way to the app so its ip and port point at
   the relay again. Otherwise the app reconnects straight to the real server and leaves the relay.

A relay only sees traffic after the HTTPS `server_data.php` step, so it doesn't help an app that rejects
your certificate ([Login](/guide/login)). Use it with clients that reach your server, such as the
Windows app with your certificate installed.

Only run a relay against servers you operate.
