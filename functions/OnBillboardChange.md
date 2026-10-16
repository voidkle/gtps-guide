# OnBillboardChange

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the trade billboard shown above a player: the item, whether it's shown, and whether the player is buying
or selling it, at what price.

The player comes from argument 1, not from the header: the client looks up that netID and logs
"Unable to find netObj %d" if it isn't in the world. (It's registered as a NetAvatar function, so the
header's `netID` must also name a player in the world for the call to arrive at all.)

| # | Type | Meaning |
|---|---|---|
| 1 | uint | netID of the player whose billboard changes |
| 2 | int | item id; stored only if > 0 (so 0 keeps the previous item) |
| 3 | string or int | `proto` ≥ 167: the string `"show,isBuying"`, two numbers. `proto` &lt; 167: an int, the show flag (isBuying is then always on) |
| 4 | int | price |
| 5 | int | 1 = the price is per item (non-zero = on) |

`proto` is the value from the login settings (`OnSuperMainStartAcceptLogonHrdxs47254722215a`, app+0xc08).
With `proto` ≥ 167 and a string with fewer than two comma-separated parts, the client falls back to reading
argument 3 as an int, which is 0 for a string, so the billboard is hidden.

### Decompiled handler

```c
void NetAvatar::OnBillboardChange(VariantList *args) {         // 0x12f8454
    int netID = args->GetUInt(0);
    NetAvatar *p = GetAvatar(netID);                           // 0x1342f40
    if (!p) { LogMsg("Unable to find netObj %d", netID); return; }
    int item = args->GetInt(1);
    bool show, buying;
    if (GetApp()->proto >= 167) {                              // 0x117e8cc
        std::vector<std::string> parts = Split(args->GetString(2), ",");   // 0x1e6b024
        if (parts.size() < 2) { show = args->GetInt(2) != 0; buying = true; }
        else { show = atoi(parts[0]) != 0; buying = atoi(parts[1]) != 0; }
    } else {
        show = args->GetInt(2) != 0; buying = true;
    }
    int price   = args->GetInt(3);
    int perItem = args->GetInt(4);
    if (item > 0) p->billboard.item = item;                    // avatar+0x334
    p->billboard.buying  = buying;                             // +0x33c
    p->billboard.price   = price;                              // +0x338
    p->billboard.perItem = perItem != 0;                       // +0x33d
    p->billboard.show    = show;                               // +0x330
}
```

<small>Handler: `0x12f8454` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1342f40`, `0x117e8cc`, `0x1e6b024`, `0x1e6e470`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnBillboardChange"` |
| 1 | int | netID |
| 2 | int | item id |
| 3 | string | "show,isBuying" as 0/1 |
| 4 | int | price |
| 5 | int | 1 = price per item |

gurotopia: `include/onVariant/BillboardChange.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnBillboardChange", 1u, 1, "...", 1, 1 }, pPeer->netid);
```
