Sends the list of NPC definition names, so the client can turn NPC numbers into names. Probably the names of
the NPC XML files the server's NPC packets refer to by number.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | NPC names, `name1\|name2\|...`; name1 = 1 |

Each list is a `|`-separated list of names. The client numbers them from 1 in order and keeps both directions: name → number and number → name (`0x1ba3e90`). The previous list is replaced. The table is the global at `0x29c4570`, the same one [OnSetDungeonXMLIndexes](./OnSetDungeonXMLIndexes)
argument 1 fills.

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                 // 0x1ba8a30
    SetIndexList(&g_xmlIndexes.npc, vl->GetString(0));     // 0x29c4570, 0x1ba3e90
}

void SetIndexList(IndexList *t, const std::string &s) {   // 0x1ba3e90
    t->names = Split(s, "|");                             // t+0x50
    int i = 1;
    for (auto &n : t->names) { t->byName[n] = i; t->byIndex[i] = n; i++; }   // t+0, t+0x28
}
```

<small>Handler: `0x1ba8a30` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1ba3e90`.</small>

<!-- args: string -->
