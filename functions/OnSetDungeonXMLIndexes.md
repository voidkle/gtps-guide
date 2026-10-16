# OnSetDungeonXMLIndexes

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sends three name lists used by dungeons, so the client can turn numbers into names. Probably the NPC,
dungeon and room (or item) definition names; the code that looks them up wasn't traced.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | list → table `0x29c4570`: the same table as [OnSetNpcXMLIndexes](./OnSetNpcXMLIndexes), so this replaces the NPC list |
| 2 | string | list → table `0x29c4470` |
| 3 | string | list → table `0x29c44f0` |

Each list is a `|`-separated list of names. The client numbers them from 1 in order and keeps both directions: name → number and number → name (`0x1ba3e90`). The previous list is replaced.

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                       // 0x1ba8ac4
    SetIndexList(&g_xmlIndexes.npc,  vl->GetString(0));          // 0x29c4570
    SetIndexList(&g_xmlIndexes.list0, vl->GetString(1));         // 0x29c4470
    SetIndexList(&g_xmlIndexes.list1, vl->GetString(2));         // 0x29c44f0
}
```

<small>Handler: `0x1ba8ac4` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1ba3e90`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetDungeonXMLIndexes", "...", "...", "..." });
```
