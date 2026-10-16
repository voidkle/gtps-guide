# OnStartTrade

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the trade window with another player in the world and tells the server it opened.

| # | Type | Meaning |
|---|---|---|
| 1 | string | read but not used (probably the other player's name; the window takes the name from the avatar instead) |
| 2 | int | netID of the other player |

What happens:

- Any trade window that is already open is closed first.
- Nothing more happens without the in-world GUI (`WorldSpecificGUI`) or a local player.
- If no avatar has netID #2, "other player doesn't exist!" is logged and the window stays empty.
- Otherwise the window shows your four item slots, "`` `oSelect an item from the inventory.``", "Waiting for &lt;name>" for the
  other side, `CancelTrade` and `AcceptTrade` buttons, and a `Check Prices` button when the server's `proto` is high enough
  for that feature.
- The client then sends `action|trade_started\nnetid|<#2>\n` (message type 2).

Fill the window with [OnTradeStatus](./OnTradeStatus) and close it with [OnForceTradeEnd](./OnForceTradeEnd).

### Decompiled handler

```c
// v[n] = argument n
void OnStartTrade(GameLogic *self, VariantList *v) {
    if (self->trade) { self->trade->Close(); delete self->trade; }          // self+0x300, 0x178c008
    self->trade = new TradeMenu();                                           // 0x178be44
    std::string name = v[1].s;                                               // unused below
    self->trade->Open(name, v[2].GetINT32());                                // 0x178cd48
}

// 0x178cd48, shortened
void TradeMenu::Open(std::string /*unused*/, int netID) {
    ... build the window under "WorldSpecificGUI" ...
    NetAvatar *other = GetAvatar(netID);
    if (!other) { LogMsg("other player doesn't exist!"); return; }
    this->otherNetID = netID;                                                // +0x110
    SetText(this->myLabel, "`oSelect an item from the inventory.");
    SetText(this->otherLabel, "Waiting for " + other->name);
    ... CancelTrade / AcceptTrade / Check Prices buttons ...
    SendTextPacket(2, "action|trade_started\nnetid|" + std::to_string(netID) + "\n");
}
```

<small>Handler: `0x136ffa8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x178be44`, `0x178c008`, `0x178cd48`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnStartTrade", "...", 1 });
```
