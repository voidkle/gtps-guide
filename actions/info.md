# action|info

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|info
|itemID|{}
|count|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |
| `count` | Amount of the item. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **INFO** button of the inventory item bar, and selecting an item in the seed diary. The server answers with
the item info dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the item |
| `count` | how many you have (the inventory slot's count byte) |

- Not while trading; `audio/cant_place_tile.wav` if the item isn't in the inventory.

<small>Builders: `0x16f73e0` (item bar), `0x1d35724` (seed diary `OnItemSelect`).</small>

## Server

gurotopia: [`include/action/info.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/info.cpp).

Reply: `OnDialogRequest` with the item's description and rarity.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|info\n|itemID|2\n|count|1\n");
```

<small>Client function: `0x16f73e0` in libgrowtopia.so 5.60.</small>
