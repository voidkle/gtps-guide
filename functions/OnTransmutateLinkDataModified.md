# OnTransmutateLinkDataModified

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Replaces a player's transmutation links: which item looks like which other item (the Transmutabooth),
probably. Runs on the player in the CALL_FUNCTION header's `netID`.

| # | Type | Meaning |
|---|---|---|
| 1–5 | string | five pieces of one text; the client joins them in order, so long data can be split across them |

The joined text:

```text
key:value,key:value,...;key:value,key:value,...|N
└─ section 0 ─────────┘ └─ section 1 ──────────┘
```

- Sections are separated by `;`, pairs by `,`, key and value by `:`. Keys and values are integers
  (probably item ids: the real item → the item it looks like).
- Section 0 becomes the player's link map (avatar+0x3668).
- Section 1, before the `|`, is a second map (avatar+0x3680); its pairs are also written into the first map,
  overwriting the same keys. The number after `|` is parsed and then not used.
- Pairs without a `:` are skipped. A missing section gives an empty map.

### Decompiled handler

```c
void NetAvatar::OnTransmutateLinkDataModified(VariantList *args) {   // 0x12f870c
    std::string s = args->GetString(0) + args->GetString(1) + args->GetString(2)
                  + args->GetString(3) + args->GetString(4);
    std::map<int,int> links, extra; int unused;
    ParseLinks(&links, s, ',', ':', ';', '|', &extra, &unused);        // 0x14ce90c
    this->transmuteLinks = links;                                       // avatar+0x3668
    this->transmuteExtra = extra;                                       // avatar+0x3680
    for (auto &[k, v] : extra) this->transmuteLinks[k] = v;
}

// 0x14ce90c
void ParseLinks(map *out, string s, char pair, char kv, char section, char bar, map *out2, int *n) {
    auto sec = Split(s, section);                                       // 0x1e6d860
    for (auto &p : Split(sec[0], pair)) { auto f = Split(p, kv); if (f.size() > 1) (*out)[atoi(f[0])] = atoi(f[1]); }
    out2->clear(); *n = 0;
    if (sec.size() > 1) {
        auto b = Split(sec[1], bar);
        if (b.size() > 1) *n = atoi(b[1]);
        for (auto &p : Split(b[0], pair)) { auto f = Split(p, kv); if (f.size() > 1) (*out2)[atoi(f[0])] = atoi(f[1]); }
    }
}
```

<small>Handler: `0x12f870c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce90c`, `0x1e6d860`, `0x1e6d44c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnTransmutateLinkDataModified", "...", "...", "...", "...", "..." }, pPeer->netid);
```
