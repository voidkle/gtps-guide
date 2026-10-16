# action|itemfavourite

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|itemfavourite
|itemID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The favourite (star) button of the inventory item bar.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected item |

- Only when the server's `proto` allows favourites, not while trading, if the item is in the inventory, can be a
  favourite (`0x156d3d0`) and isn't one yet; the client marks it locally at once. Otherwise `audio/cant_place_tile.wav`.
- The answer is [OnFavItemUpdated](/functions/OnFavItemUpdated).

<small>Builder: `0x16f7c64`; called from `0x16f6aa0`.</small>

## Server

gurotopia: [`include/action/itemfavourite.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/itemfavourite.cpp).

Reply: `OnFavItemUpdated`. At most 20 favourites.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|itemfavourite\n|itemID|2\n");
```

<small>Client function: `0x16f7c64` in libgrowtopia.so 5.60.</small>
