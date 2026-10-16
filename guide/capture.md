# Capturing and decoding the game's traffic

`gtps/tools/gtcap` reads a Wireshark (or tcpdump) capture of Growtopia's ENet traffic and prints every message in
the same form as the rest of this site. Use it to see what a real server sends for an action and compare it with
your own server.

## Capture

1. Install Wireshark (on Windows with **Npcap**) and start capturing on the network adapter the game uses.
2. Optional capture filter: `udp`. The game's UDP traffic is the ENet connection; the web login is HTTPS and
   stays encrypted, which is fine.
3. Play. Keep a note of what you did and roughly when.
4. Stop and save as `.pcapng` or `.pcap`.

## Decode

```sh
cd gtps && make tools/gtcap.out
./tools/gtcap.out game.pcapng                # every message, in order
./tools/gtcap.out game.pcapng --port 17091   # only UDP to or from one port
./tools/gtcap.out game.pcapng --stats        # how often each packet and function occurs
./tools/gtcap.out game.pcapng --only server  # one direction (client or server)
./tools/gtcap.out game.pcapng --hex          # also dump the extra data of packets it can't summarize
```

```text
    0.504 C->S TEXT "protocol|227|ltoken|<redacted>|platformID|0"
    0.504 S->C CALL netID=-1 delay=0  OnSendToServer(17095, 1338781234, 1, "127.0.0.2|0|e450e99e3b1d68a9", 1, "alice70423")
    2.544 S->C 0x04 SEND_MAP_DATA flags=0x8 tile=(7522083,0) extra=48078B [world v27 flags 0 "TEST70423" 100x60]
   26.849 C->S 0x03 TILE_CHANGE_REQUEST itemID=2 posY=736 tile=(1,23)
```

Passwords, tokens and device ids in the login messages are replaced by `<redacted>`; `--raw-secrets` keeps them.
Retransmitted packets are shown once. Datagrams that don't decode print as `undecodable`.

## How a datagram is laid out

What the decoder relies on (found by recording this repo's own client and server):

| Bytes | Field |
|---|---|
| 6 | **integrity**, client → server only. It depends on the server's UDP port, so a proxy on a different port than the server breaks the connection |
| 2 | peer ID in the low 12 bits; `0x4000` = body is range-coded, `0x8000` = a sent time follows |
| 2 | sent time (if flagged) |
| 4 | CRC32 |
| rest | the commands, range-coded when flagged (ENet's own range coder, `enet_range_coder_decompress`) |

All ENet fields are big-endian. Commands are ENet's (`CONNECT`, `SEND_RELIABLE`, `SEND_FRAGMENT`, ...); big messages
such as the world map arrive as fragments, which the tool reassembles. The message inside is
[the usual message type](/guide/message-types) and, for type 4, the [game packet](/guide/game-packet).

## Testing without root

`gtps/tools/udpcap.py` is a small UDP forwarder that records into a pcap, so the decoder can be tried on this
repo's own traffic. Because of the integrity field it must listen on the **same port** as the server, on a different
loopback address (`127.0.0.2`) with the server bound to `127.0.0.1` (`bind_ip` in `gtps.conf`). The end-to-end test
accepts that address as its fourth argument.
