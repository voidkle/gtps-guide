# 0x07 TILE_ACTIVATE_REQUEST

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="confirmed" />

## What the client sends

<Badge type="tip" text="decompiled from the 5.60 client" />

The client never handles this type; it **sends** it. It asks the server to activate a tile: enter a door or
portal, touch a checkpoint, a race flag, a pickup and so on. Every send goes through `0x1381730`:

| Field | Value |
|---|---|
| `type` | 0x07 |
| `tileX`, `tileY` | the tile (tile+0x54, +0x55) |
| everything else | 0 (no `netID`, no position) |

Sent reliable, no extra data.

### When it's sent

- **Entering a door** (`0x13035e4`): by walking into a tile of action type 26 (portals: Orange Portal, Blue Portal,
  Hellgate, Time-Space Rupture...), or of action type 43 (Sungate) when a value at `0x11b25a4`+0x260 is above 6;
  by tapping the door you stand on with the Fist; or with the punch key while on it. Before sending, the client:
  - refuses with "You must complete the tutorial first!" (at most every 1.5 s) when feature 6 isn't unlocked
    (`0x1444c80(6)`);
  - refuses the Main Door (6) while avatar+0x175 bit 7 is set, and the Rune Carved Door (9358) unless you wear
    Magic Stones (9356);
  - zooms the camera, freezes you until the server answers (avatar+0x128), closes open dialogs, and for doors
    other than the Main Door shows "Entering world".
- **Walking into a tile** (`0x13002b4`, every frame), once per tile until you step on another one
  (avatar+0x254 holds the last tile index; `OnSetPos` resets it):
  - Challenge End Flag (3808), Blarney Stone (1508), Great Legendary Orb (1792), Great Wolf Totem (2994),
    Finale Claim 1-9 (8776-8792), Icy Heart Pickup (3212);
  - Race Start Flag (428) when you aren't racing, Race End Flag (430) when you are (avatar+0x68);
  - tiles of action type 94 (Valhowla Treasure...) that aren't already "on" (tile flag 0x40);
  - Steam Stomper (3270) when its state allows it (`0x15b241c` false, `0x15b244c` ≥ 1) and you fall onto it
    faster than ¾ of a physics constant; Steam Revolver (3496) under the same state checks while you move;
  - adventure tiles: The Adventure Begins (4722), Tomb Robber (4742), Adventure's End (4740, only after an
    adventure flag at avatar+0x2eb is set), the Adventure Brazier (4704) while you carry the Adventure Item - Torch
    (1702), and the Adventure Pedestal (4708) while you carry the Golden Idol (1698). Brazier and Pedestal are
    skipped while a flag at avatar+0x2e8 / +0x2e9 is set (probably "already done");
  - team games, while you're on a team (avatar+0x26d ≤ 4): a Game Flag (1622) or Game Egg (5992) of another
    team (its tile extra's team byte, +0x60), and a Game Goal (1658) or Game Goal Egg Basket (5998) of your team;
  - a checkpoint (action type 27) that isn't your current one (avatar+0x25c).
- **Landing on a powered Steam Launcher** (3498, tile flag 0x40, `0x131092c`): the client launches you, clears
  the flag and sends 0x07.
- **Tapping with the Fist** (`0x13a70f8`) an Angry Adventure Gorilla (4712) that is "on" while you carry the
  Adventure Item - Banana (1700), or item 7962 while you carry item 7960.
- **A moving world object reaching a checkpoint** (`0x12c5640`, world objects updated by `0x12b5c18`): when the
  object enters a new tile of action type 27 (Checkpoint, Flower Checkpoint...). Probably an object you control;
  which items use it wasn't traced.

<small>Sender: `0x1381730`; callers `0x13035e4`, `0x13002b4`, `0x1303a18`, `0x131092c`, `0x13a70f8`, `0x12c5640`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `tileX / tileY` | the tile you activated (door, portal, ...) |

## gurotopia

`include/gamePacket/tile_activate.cpp`: doors and portals warp you.

## Official client

**Received:** ignored (falls to the switch's default).

**Sent:** `0x1381790` sets the type to 7.
