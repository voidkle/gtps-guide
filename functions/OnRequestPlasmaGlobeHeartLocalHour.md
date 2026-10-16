# OnRequestPlasmaGlobeHeartLocalHour

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Asks the client for its local hour of the day. It answers at once with a text message (message type 2):

```text
action|PlasmaGlobeHeartLocalHour
localHour|<0-23>
```

No arguments are read. The hour is `tm_hour` from `localtime(time())` on the device. It's registered as a
player function, but the answer doesn't depend on the player.

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` must be a player in the world
(any player), or the call is dropped.

### Decompiled handler

```c
void NetAvatar::OnRequestPlasmaGlobeHeartLocalHour(NetAvatar *a, VariantList *vl) {
    SendPlasmaGlobeHeartLocalHour(GetGameLogic());                 // 0x1382228
}

void SendPlasmaGlobeHeartLocalHour(GameLogic *self) {
    int mon, day, year, hour, min, sec;
    GetLocalDateTime(&mon, &day, &year, &hour, &min, &sec);        // 0x14224b8: localtime()
    std::string s = "action|PlasmaGlobeHeartLocalHour\nlocalHour|" + std::to_string(hour) + "\n";
    SendText(2, s, GetApp()->client->peer);                        // 0x157f060
}
```

<small>Handler: `0x12f6d78` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1382228`, `0x14224b8`, `0x157f060`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRequestPlasmaGlobeHeartLocalHour" }, pPeer->netid);
```
