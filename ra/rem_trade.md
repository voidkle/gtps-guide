Takes an item back out of the trade: tapping one of **your own** filled slots in the trade window.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the item in that slot |

- Tapping an empty slot plays `audio/cant_place_tile.wav`; tapping the other player's slot shows its item info.

<small>Builder: `0x178e3b4` (see [mod_trade](./mod_trade)); called from `0x13ead80`.</small>
