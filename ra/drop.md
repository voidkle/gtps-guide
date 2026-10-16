The **DROP** button of the inventory item bar, for the selected item. The server answers with a drop dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected inventory item (GameLogic+0x298) |

- Not while trading (GameLogic+0xc0) or when the item isn't in the inventory (plays `audio/cant_place_tile.wav`).
- An untradeable item (`0x156ecec`) plays the same sound instead, unless a certain avatar field is negative (not traced).

<small>Builder: `0x16f6ed4`; called from `0x16f6aa0` (item bar buttons `DROP`, `TRASH`, `INFO`, `STORE`, `DAILYREWARD`).</small>
