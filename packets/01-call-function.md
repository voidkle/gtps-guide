# 0x01 CALL_FUNCTION

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Runs a named client function (`OnConsoleMessage`, `OnSpawn`, `OnDialogRequest`, ...). The extra data is a
variant list; variant 0 is the function name and variants 1–6 are its arguments. `netID` picks who runs it
and `itemID` is a delay in milliseconds.

| Field | Used as |
|---|---|
| `netID` | `-1`: a global function, run by the game's GUI root. Anything else: run on that player's entity (dropped if the player isn't in the world) |
| `itemID` | delay in ms before the function runs. With `netID == -1`, `-1` means "run now, synchronously"; otherwise the value is added to the current time, so `0` and `-1` both run on the next update |
| `extraDataLength` | passed to the variant-list parser, which doesn't use it (no bounds check) |

### Extra data

A variant list, read by `VariantList::SerializeFromMem` (`0x1e78650`):

```
u8 count
count × { u8 index, u8 type, value }
   type 1 float     4 bytes
   type 2 string    u32 length + bytes
   type 3 vec2      2 × float
   type 4 vec3      3 × float
   type 5 uint      4 bytes
   type 8 rect      4 × float
   type 9 int       4 bytes
   type 10          8 bytes
```

`index` is the slot (0–6), so the variants don't have to be in order. Any other type logs "unknown var type"
and stops; the packet is then dropped with "Error reading function packet, ignoring".

### Decompiled handler

```c
case 0x01: {
    VariantList v;                                       // 7 slots
    if (!v.SerializeFromMem(extra, pkt->extraDataLength, NULL)) {
        LogError("Error reading function packet, ignoring");
        break;
    }
    std::string name = v[0].string;
    VariantList args; v.CopyFrom(args, 1);               // slots 1..6 become args 0..5

    if (pkt->netID == -1) {
        FunctionHooks()->Notify(name, args);             // 0x13770e0 / 0x1b29490: global listeners
        if (pkt->itemID == -1)
            self->functions.Find(name)->Call(args);      // self+0x28, runs now
        else
            CallFunctionLater(GetApp()->guiRoot, pkt->itemID, name, args);   // app+0xfd8
    } else {
        NetAvatar *p = GetAvatar(pkt->netID);
        if (p)
            CallFunctionLater(p->entity, pkt->itemID, name, args);           // avatar+0x48
    }
}
```

`CallFunctionLater` is `0x1e443fc`: it schedules the call at `now + delay`.

<small>Handler: `0x137445c` (switch case) in the 5.60 arm64 client; callees read: `0x1e78650`, `0x1e78944`, `0x1b29490`, `0x1e443fc`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `netID` | the player the call is about, or -1 |
| `flags` | `S_EXTENDED` (0x08) |
| `itemID` | delay in milliseconds before the client runs it |
| `extraDataLength` | size of the variant list |

## Extra data

A variant list. Variant 0 is the function name. See [Variant lists](/guide/variant-list) and the Server functions section.

## gurotopia

Built by `send_varlist()` in `include/proton/Variant.cpp`.

## Official client

**Received:** handled at `0x137445c` in the incoming switch (`0x1373e20`).
