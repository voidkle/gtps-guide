# 0x0e ITEM_CHANGE_OBJECT

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Creates, changes or removes a dropped object (an item lying in the world), and handles picking one up.
`netID` selects the operation.

| Field | Used as |
|---|---|
| `netID` | the operation: `-1` new drop, `-3` change an existing drop, `-2` remove a drop, a player's netID = that player picked it up |
| `targetNetID` | for `-3`: the object's uid. For other values: a player the item flies from (`-1` = none) |
| `itemID` | for `-1`/`-3`: the item id. For a pickup or `-2`: the object's uid |
| `float_var` | the amount (truncated to an int) |
| `posX`, `posY` | where the object lies |
| `objectType` (byte 1) | object flags, stored with the object |

### Sub-commands

| `netID` | Effect | Fields used |
|---|---|---|
| -1 | Adds a new object. Its uid is the world's drop counter + 1 (`0x161827c`: `uid = ++objects->lastUid`), so the server must number drops the same way. The counter starts at the world data's `last_drop_uid` (`0x16188d0`; when that loader is asked to renumber, the drops become 1..n instead and the counter is n). Plays `audio/object_spawn2.wav` at `pos`, at most once every 150 ms | `itemID`, `float_var`, `pos`, `objectType` |
| -3 | Finds the object whose uid is `targetNetID` and updates its item, amount, position and flags. Also plays the spawn sound | `targetNetID`, `itemID`, `float_var`, `pos`, `objectType` |
| -2 | Removes the object whose uid is `itemID` (nobody picks it up) | `itemID` |
| your netID | You picked up object `itemID`: an item-to-inventory animation plays and the item goes into your inventory. Gems (112) add to the gem counter instead, and item 12250 to another counter. The item is put into a free quick slot | `itemID` |
| another player | That player picked up object `itemID`: a pickup animation plays toward them | `itemID` |

If `itemID` names no existing object for a pickup or `-2`, the client logs "Bad object change request: %d" and stops.
When `targetNetID` isn't -1 (and `netID` isn't -3), the item also animates from that player to `pos`, which is how a drop
by a player looks.

### Decompiled handler

```c
case 0x0e: {
    if (!self->world) break;
    WorldObject *obj = NULL;
    if (pkt->netID >= 0 || pkt->netID == -2) {
        obj = world->objects.Find(pkt->itemID);                       // 0x1618da8, by uid
        if (!obj) { LogError("Bad object change request: %d", pkt->itemID); return; }
    }
    bool refresh = false;
    if (self->localPlayer && pkt->netID == self->localPlayer->netID) {
        PickupAnimation(obj->itemID, obj->amount, &obj->pos);         // 0x1148bb8
        if (obj->itemID == 12250)      GetApp()->state->counter_2a8 += obj->amount;
        else if (obj->itemID == 112) { GetApp()->state->gems += obj->amount; GetApp()->state->gemsTotal += obj->amount; UpdateGemsUI(obj->amount); }
        else if (!(GetApp()->flag_cca && obj->itemID == 9186)) {
            int had = inventory->Count(obj->itemID);
            inventory->AddItem(obj->itemID, obj->amount, NULL);
            if (had == 0) { inventory->Sort(); refresh = true; }
        }
        inventory->PutInFreeQuickSlot(obj->itemID);                    // 0x15954f4
    } else {
        NetAvatar *p = GetAvatar(pkt->netID);
        if (p) OtherPlayerPickupAnimation(obj->itemID, obj->amount, &obj->pos, p);   // 0x1148df0
    }
    if (pkt->netID == -1 || pkt->netID == -3) {
        if (GetTick() > nextSpawnSound) {
            PlaySound(self, &pkt->pos, "audio/object_spawn2.wav");
            nextSpawnSound = GetTick() + 150;
        }
    }
    if (pkt->targetNetID != -1 && pkt->netID != -3)
        FlyItemFromPlayer(pkt->itemID, (int)pkt->float_var, pkt->targetNetID, &pkt->pos);   // 0x1148fa4
    world->HandlePacket(pkt);                                          // 0x15dd790 → objects.HandlePacket
    if (refresh) RefreshInventoryUI();
}

bool WorldObjects::HandlePacket(packet *pkt)                           // 0x1618b80
{
    if (pkt->netID == -3) {
        WorldObject *o = Find(pkt->targetNetID);
        if (o) {
            if (o->itemID != pkt->itemID) ChangeItem(o, pkt->itemID);
            o->amount = (int)pkt->float_var;
            MoveTo(o, &pkt->pos);
            o->flags = pkt->objectType;
        }
    } else if (pkt->netID == -1) {
        Add(pkt->itemID, &pkt->pos, (int)pkt->float_var, pkt->objectType);   // 0x161827c
    } else {
        Remove(pkt->itemID);                                           // 0x161845c, by uid
    }
    return true;
}
```

<small>Handler: `0x13741a0` (switch case) in the 5.60 arm64 client; callees read: `0x1618da8`, `0x1618b80`, `0x1148bb8`, `0x1148df0`, `0x1148fa4`, `0x1595c80`, `0x15954f4`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `netID` | -1 new drop, -3 count changed, otherwise the player who picked it up |
| `targetNetID` | object uid, or -1 when picked up |
| `itemID` | item id, or the object uid when picked up |
| `float_var` | count |
| `pos` | where it lies |

## gurotopia

`add_object()`, `merge_object()` and `remove_object()` in `include/database/world.cpp`.

## Official client

**Received:** handled at `0x13741a0` in the incoming switch (`0x1373e20`).
