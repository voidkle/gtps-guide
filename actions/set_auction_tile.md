# action|set_auction_tile

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|set_auction_tile
item|{}|price|{}|duration|{}|state|{}
```

## Fields

| Field | Meaning |
|---|---|
| `item` | Store item or category id. |
| `price` | Price. |
| `duration` | Auction length. |
| `state` | Auction tile state. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** the fields are on **one** line, with no trailing `\n`:
`action|set_auction_tile\nitem|{}|price|{}|duration|{}|state|{}`.

Saving the settings of an auction tile (a placed auction block).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `item` | the item for sale |
| `price` | the starting price (from the price text box) |
| `duration` | the auction length |
| `state` | the tile's on/off state |

- Only if the auction tile at the screen's position still exists and a value changed; otherwise logs "{}: nothing to do".

<small>Builder: `0x1c80b20`; called from `0x1c81694`, `0x1c81744`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

Unusually, the fields share one line.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|set_auction_tile\nitem|main|price|0|duration|0|state|0");
```

<small>Client function: `0x1c80b20` in libgrowtopia.so 5.60.</small>
