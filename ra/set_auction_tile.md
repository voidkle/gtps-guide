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
