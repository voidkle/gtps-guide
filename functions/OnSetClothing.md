# OnSetClothing

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the clothes a player wears and their skin colour. Item ids are sent as floats inside three vec3s.

| # | Type | Meaning |
|---|---|---|
| 1 | vec3 | hair, shirt, pants (legs) |
| 2 | vec3 | feet, face, hand |
| 3 | vec3 | back, mask (head), necklace (charm) |
| 4 | uint | skin colour (stored as-is; gurotopia sends `-140` as uint for ghosts) |
| 5 | vec3 | x = ances item; y ≠ 0 plays `audio/change_clothes.wav`; z unused |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world. Gurotopia follows it with a
[SET_CHARACTER_STATE (0x14)](/packets/14-set-character-state).

- **Slots.** The nine ids are stored as u16 at avatar+0x29e. A visible copy at avatar+0x28c goes through the
  avatar's item-replacement map (avatar+0x3668), so transformed items can show something else.
- **Log.** The client logs `{}Player items: {}`, with the prefix `Local ` for your own avatar.
- **Your own avatar:**
  - each slot is recorded as a Crashlytics key `Slot_<name>`;
  - the inventory marks the worn items (`0x15968e8`);
  - GameLogic+0xa0 is set to the ances id.
- **Skin colour.** It goes to avatar+0x2f8+8 and to the app variable `skinColor`. That happens for every player
  whose clothes change, not only you. The colour used for drawing (avatar+0x88) is taken from the items.dat
  record of item *pants + 1* (item+0xb8) when that item exists and pants ≠ 0; otherwise it is the skin colour.
- **Hand item.** The punch-range box (avatar+0x35f8…) is placed at a random offset (0 to 999999) when the hand
  item is Rayman's Fist (5480), and at -1000 otherwise. The client then re-checks that box. If it doesn't match, it logs `Punch hack detected!` and sends
  [APP_INTEGRITY_FAIL (0x19)](/packets/19-app-integrity-fail) with `itemID` 28, at most once per cooldown.
- **Last steps.** The collision box is recomputed and the clothes are redrawn (`0x1098f88`). avatar+0x2b4
  becomes the number of entries the local inventory reports (`0x1596b34`), plus 1 if an ances is set.
  `Player cloth loaded` is logged.

### Decompiled handler

```c
void NetAvatar::OnSetClothing(NetAvatar *a, VariantList *vl) {
    a->cloth[0..2] = (u16)vl[1].v3.{x,y,z};    // hair, shirt, pants      avatar+0x29e..
    a->cloth[3..5] = (u16)vl[2].v3.{x,y,z};    // feet, face, hand
    a->cloth[6..8] = (u16)vl[3].v3.{x,y,z};    // back, mask, necklace
    ApplyItemReplacements(a->cloth, &a->replaceMap, a->shownCloth);       // 0x1311af8, +0x3668 → +0x28c
    a->ances = (int)vl[5].v3.x;                                            // avatar+0x2b0
    a->look.SetCloth(a->cloth);                                            // 0x14ce8f8 (avatar+0x2f8)
    Log(format("{}Player items: {}", a->controller ? "" : "Local ", ClothToString(a->cloth)));
    if (!a->controller)
        for (int i = 0; i < 9; i++) Crashlytics()->SetCustomKey("Slot_" + slotName[i], a->cloth[i]);
    a->look.skinColor = vl[4].u;                                           // 0x14ce8e0
    GetApp()->GetVar("skinColor")->SetUINT(a->look.skinColor);             // 0x107fe7c
    ItemInfo *it = GetItem(a->shownCloth[2] + 1);                          // pants + 1
    a->drawColor = (it && a->shownCloth[2]) ? it->f_b8 : a->look.skinColor;  // avatar+0x88
    if (vl[5].v3.y != 0) a->PlaySound("audio/change_clothes.wav");
    if (!a->controller) {
        Inventory::MarkWorn(&GetGameLogic()->inventory, a->cloth);         // 0x15968e8
        GetGameLogic()->localAnces = a->ances;                             // +0xa0
    }
    ... hand-item effects (0x11f60d8, 0x156c838 on hand/feet) ...
    float base = (a->cloth[5] == 5480) ? RandomFloat(0, 999999.0f) : -1000.0f;   // Rayman's Fist
    a->punchBox = box built from base;
    if (punch box doesn't add up) {
        Log("Punch hack detected!");
        a->integrityReason = 28;
        if (a->nextIntegrityReport <= GetTick()) SendIntegrityFail(..., 28, 0);   // 0x137c374
    }
    a->RecalcCollisionBox();
    a->visual.RefreshClothes(a);                                           // 0x1098f88
    a->wornCount = Inventory::Equipped(&GetGameLogic()->inventory).size() + (a->ances ? 1 : 0);  // +0x2b4
    Log("Player cloth loaded");
}
```

<small>Handler: `0x12f59cc` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1311af8`, `0x14ce8f8`, `0x14ce8e0`, `0x107fe7c`, `0x15968e8`, `0x137c374`, `0x1098f88`, `0x1596b34`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnSetClothing"` |
| 1 | vec3 | hair, shirt, legs |
| 2 | vec3 | feet, face, hand |
| 3 | vec3 | back, head, charm |
| 4 | int/uint | skin color (-140 for ghost) |
| 5 | vec3 | ances, 0, 0 |

The game packet header's `netID` names the player this call is about.

Followed by a SET_CHARACTER_STATE (0x14) game packet.

gurotopia: `include/onVariant/SetClothing.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetClothing", CL_Vec3f{a, b, c}, CL_Vec3f{a, b, c}, CL_Vec3f{a, b, c}, 1u, CL_Vec3f{a, b, c} }, pPeer->netid);
```
