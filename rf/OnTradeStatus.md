Updates one side of the open trade window: its label, the items offered and the "accepted" state. Send it once for each
side. If no trade window is open, the client logs "Ignoring trade data, trade window not on" and drops it.

| # | Type | Meaning |
|---|---|---|
| 1 | int | netID of the side to update: your own netID, or the other player's (the one from [OnStartTrade](./OnStartTrade)) |
| 2 | string | new label for **your** side (used when #1 is you; empty = keep the label) |
| 3 | string | new label for the **other** side (used when #1 is the other player; empty = keep), e.g. `` `oPlayer's offer.`` `` |
| 4 | string | the side's offer, lines separated by `\n`, fields by `\|` (see below) |

If #1 is neither player, the other side's label becomes "Error occured.  Just cancel." Without a local player the client logs
"Ignoring trade data, no local player".

Lines of argument 4:

| Line | Effect |
|---|---|
| `add_slot\|<itemID>\|<count>` | fills the next of the four slots (the slots are emptied first, in order of the lines) |
| `accepted\|0/1` | the side's accept state: highlights its `AcceptTrade` label |
| `reset_locks\|<anything>` | clears the accept state (and, for your side, the stored "you accepted" flag) |
| `locked\|0/1` | parsed but not used by 5.60 |

Example for the other side:

```text
OnTradeStatus, 7, "", "`oBob's offer.``", "locked|0\nreset_locks|1\naccepted|0\nadd_slot|242|1"
```

### Decompiled handler

```c
// v[n] = argument n
void OnTradeStatus(GameLogic *self, VariantList *v) {
    TradeMenu *t = self->trade;                                     // self+0x300
    if (!t) { LogMsg("Ignoring trade data, trade window not on"); return; }
    t->SetStatus(v[1].GetINT32(), v[2].s, v[3].s, v[4].s);          // 0x178dca0
}

// 0x178dca0
void TradeMenu::SetStatus(int netID, string myLabel, string otherLabel, string data) {
    if (!LocalPlayer()) { LogMsg("Ignoring trade data, no local player"); return; }
    bool reset = false, accepted = false, locked;
    if (netID == LocalPlayer()->netID) {                            // avatar+0x40
        if (!myLabel.empty()) SetText(this->myLabel, myLabel);      // +0x60
        locked = this->f_12d;
        ParseSide(&this->mine /*+0x58*/, data, &reset, &accepted, &locked);   // 0x178df8c
        if (reset) { SetAccepted(this, 0, 1); this->otherAccepted = 0; }    // 0x178b970, +0x12e
        else { this->iAccepted = accepted; SetAccepted(this, accepted, 0); } // +0x12c
    } else if (netID == this->otherNetID) {                         // +0x110
        if (!otherLabel.empty()) SetText(this->otherLabel, otherLabel);   // +0xc0
        ParseSide(&this->theirs /*+0xb8*/, data, &reset, &accepted, &locked);
        this->otherAccepted = accepted;                             // +0x12e
        if (reset) SetAccepted(this, 0, 1);
    } else
        SetText(this->otherLabel, "Error occured.  Just cancel.");
}

// 0x178df8c
void ParseSide(Side *s, string data, bool *reset, bool *accepted, bool *locked) {
    for (int i = 0; i < 4; i++) ClearSlot(s->slot[i]);              // 0x13eb050(slot, 0, 0)
    int n = 0;
    for (line in Split(data, '\n')) {
        auto f = Split(line, '|');
        if (f[0] == "add_slot")    { if (s->slot[n]) SetSlot(s->slot[n], atoi(f[1]), atoi(f[2])); n++; }
        if (f[0] == "locked")      *locked = atoi(f[1]) != 0;
        if (f[0] == "reset_locks") *reset = true;
        if (f[0] == "accepted")    *accepted = atoi(f[1]) != 0;
    }
}
```

<small>Handler: `0x13700e4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x178dca0`, `0x178df8c`, `0x178b970`.</small>

<!-- args: int,string,string,string -->
