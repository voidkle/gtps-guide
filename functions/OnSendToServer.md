# OnSendToServer

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client to leave the current server and connect to another one (or the same one again), for
example to enter a world on a sub-server.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | int | port |
| 2 | int | token; -1 = keep the token of the current connection |
| 3 | int | user id (also stored at GameLogic+0xb4 and in the client's analytics) |
| 4 | string | `ip\|doorID\|uuid`, split on `\|`. The new login sends `doorID` as `doorID\|` and `uuid` as `UUIDToken\|` (`0x18009d0`). If `uuid` is exactly `-1`, the current connection's UUID token is kept |
| 5 | int | logon mode, stored at app+0x9a0 → +0xc0. It decides what the client sends after connecting, see [OnSuperMainStartAcceptLogonHrdxs47254722215a](./OnSuperMainStartAcceptLogonHrdxs47254722215a) |
| 6 | string | GrowID; saved as the `tankid_name` setting |

What the client does, in order:

1. Logs `Go to gameserver: server: {ip}, port: {port}, doorID: {doorID}`.
2. Sends a [DISCONNECT (0x1a)](/packets/1a-disconnect) game packet (all other header fields 0) to the
   current server and closes the connection (`0x11430e4`).
3. Stores the logon mode, builds the login info (a `ServerAuthPacketBuilder`: user id, token, UUID token, door id, and a value
   from the app context, `0x17f9a00`) and connects to `ip:port` (`0x1142610`).
4. On debug builds (app flags +0xbe4/+0xbe6/+0xbe7) shows `Logon mode is: <n>`.

The new connection's login then carries the token, user id, door id and uuid (see [Login](/guide/login)).

### Decompiled handler

```c
void operator()(VariantList *const &vl) { ScreenFlow_OnSendToServer(this->owner, vl); }   // 0x1ba849c

void ScreenFlow_OnSendToServer(ScreenFlow *self, VariantList *args) {   // 0x1ba408c
    int port = args->GetInt(0), token = args->GetInt(1), userID = args->GetInt(2);
    std::string addr = args->GetString(3), growid = args->GetString(5);
    Analytics()->SetUserID(to_string(userID));                         // 0x1f1bb5c / 0x1f1bb3c
    GameLogic()->userID = userID;                                      // +0xb4
    GetApp()->Var("tankid_name")->Set(growid);
    auto f = Split(addr, "|");                                         // ip, doorID, uuid
    std::string ip = f[0], door = f[1], uuid = f.size() > 2 ? f[2] : "";
    Log("Go to gameserver: server: {}, port: {}, doorID: {}", ip, port, door);
    GameHeader h = {}; h.type = 0x1a;                                  // DISCONNECT
    SendGamePacket(4, &h, 0x38, NULL, GetApp()->client->peer, 1);
    Disconnect(GetApp()->client);                                      // 0x11430e4
    GetApp()->client->logonMode = args->GetInt(4);                     // +0xc0
    NetClient *nc = GetNetClient();                                    // 0x1143450
    nc->f_a4 = 0;
    if (auto *cur = dynamic_cast<ServerInfo *>(nc->current)) {         // nc+200
        if (token == -1) token = cur->token;                           // +0x14
        if (uuid == "-1") uuid = cur->uuidToken;                       // +0x18
    }
    ServerAuthPacketBuilder *ci = new ServerAuthPacketBuilder{userID, token, /*+0x18*/uuid, /*+0x30*/door, AppContextValue()};
    Connect(nc, ip, port, ci);                                         // 0x1142610
    if (GetApp()->debugA || GetApp()->debugB || GetApp()->debugC)
        ShowText("Logon mode is: " + to_string(GetApp()->client->logonMode));
}
```

<small>Handler: `0x1ba849c` → `0x1ba408c` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x157ee8c`, `0x11430e4`, `0x1142610`, `0x1e6b024`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnSendToServer"` |
| 1 | int | port |
| 2 | int | token |
| 3 | int | user id |
| 4 | string | "ip|0|0" (gurotopia) or "ip|doorID|uuid" |
| 5 | int | logon mode (1 = welcome) |
| 6 | string | growid |

Tells the client which server to (re)connect to. gurotopia lets the client continue on the same connection.

gurotopia: `include/action/protocol.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnSendToServer", 1, 1, 1, "...", 1, "..." });
```
