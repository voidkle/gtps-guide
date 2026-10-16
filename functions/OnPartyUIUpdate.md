# OnPartyUIUpdate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the three party slots shown in the in-world menu (`WorldSpecificGUI` → `GameMenu`), each drawn with
`interface/large/guild_button.rttex`, then refreshes them.

| # | Type | Meaning |
|---|---|---|
| 1 | int | slot 0 value; a negative value hides the slot |
| 2 | int | slot 1 value; negative hides it |
| 3 | int | slot 2 value; negative hides it |
| 4 | string | slot 0 text |
| 5 | string | slot 1 text |
| 6 | string | slot 2 text |

Apart from the sign, the client doesn't use the values in this path. Each slot also has a progress bar whose two values
(slot +0x20 / +0x24) this call doesn't set; something else fills them.

### Decompiled handler

```c
// v[n] = argument n
void OnPartyUIUpdate(GameLogic *self, VariantList *v) {
    int a = v[1].GetINT32(), b = v[2].GetINT32(), c = v[3].GetINT32();
    PartySlots *p = &GetGameLogic()->party;                  // GameLogic+0x440, 3 slots of 0x28 bytes
    p->slot[0] = { a, v[4].s };
    p->slot[1] = { b, v[5].s };
    p->slot[2] = { c, v[6].s };                              // 0x14cf238
    RefreshPartyUI();                                        // 0x17219c8 → 0x17218b8 per slot
}
```

<small>Handler: `0x1370318` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x14cf238`, `0x17219c8`, `0x17218b8`, `0x1720e3c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPartyUIUpdate", 1, 1, 1, "...", "...", "..." });
```
