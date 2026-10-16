# action|drop

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|drop
|itemID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **DROP** button of the inventory item bar, for the selected item. The server answers with a drop dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected inventory item (GameLogic+0x298) |

- Not while trading (GameLogic+0xc0) or when the item isn't in the inventory (plays `audio/cant_place_tile.wav`).
- An untradeable item (`0x156ecec`) plays the same sound instead, unless a certain avatar field is negative (not traced).

<small>Builder: `0x16f6ed4`; called from `0x16f6aa0` (item bar buttons `DROP`, `TRASH`, `INFO`, `STORE`, `DAILYREWARD`).</small>

## Server

gurotopia: [`include/action/drop.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/drop.cpp).

Reply: `OnDialogRequest` asking how many (dialog `drop_item`), or `OnTextOverlay` "You can't drop that."

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|drop\n|itemID|2\n");
```

<small>Client function: `0x16f6ed4` in libgrowtopia.so 5.60.</small>
