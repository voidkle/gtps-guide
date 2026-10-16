# Transport (ENet)

Growtopia runs on [ENet](http://enet.bespin.org/) over UDP, port `17091` by default (whatever
`server_data.php` returns in `port|`).

Both servers use ENet with **three Growtopia-specific changes**. A client or server must enable all three,
or the other side silently drops every packet:

| Change | Client | Server |
|---|---|---|
| Newer packet header | `host->usingNewPacket = 1` | `host->usingNewPacketForServer = 1` |
| CRC32 checksums | `host->checksum = enet_crc32` | same |
| Range coder compression | `enet_host_compress_with_range_coder(host)` | same |

- **Library:** gurotopia ships a patched ENet (ZTzTopia's fork) as `include/enet/` and
  `include/enet/lib/libenet.a`. GrowServer uses `growtopia.wasm`, a WebAssembly build of the same thing.
- **Channels:** 2. Everything is sent on channel 0 with `ENET_PACKET_FLAG_RELIABLE`.
- **Byte order:** every integer and float is little-endian.

## Client setup

```cpp
enet_initialize();
ENetHost *host = enet_host_create(ENET_ADDRESS_TYPE_IPV4, nullptr, 1, 2, 0, 0);
host->usingNewPacket = 1;
host->checksum = enet_crc32;
enet_host_compress_with_range_coder(host);

ENetAddress address{ .type = ENET_ADDRESS_TYPE_IPV4, .port = 17091 };
enet_address_set_host_ip(&address, "127.0.0.1");
ENetPeer *server = enet_host_connect(host, &address, 2, 0);
```

## Server setup

From gurotopia's `main.cpp`:

```cpp
ENetAddress address{ .type = ENET_ADDRESS_TYPE_IPV4, .port = 17091 };
host = enet_host_create(ENET_ADDRESS_TYPE_IPV4, &address, 50 /* peers */, 2, 0, 0);
host->usingNewPacketForServer = true;
host->checksum = enet_crc32;
enet_host_compress_with_range_coder(host);
```
