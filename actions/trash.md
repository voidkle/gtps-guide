# action|trash

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|trash
|itemID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `itemID` | Item id from items.dat. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **TRASH** button of the inventory item bar. The server answers with a confirmation dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected inventory item |

- Not while trading; `audio/cant_place_tile.wav` if the item isn't in the inventory.

<small>Builder: `0x16f71a8`; called from `0x16f6aa0`.</small>

## Server

gurotopia: [`include/action/trash.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/trash.cpp).

Reply: `OnDialogRequest` asking how many to destroy (dialog `trash_item`).

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|trash\n|itemID|2\n");
```

<small>Client function: `0x16f71a8` in libgrowtopia.so 5.60.</small>
