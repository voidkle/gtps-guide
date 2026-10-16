The **INFO** button of the inventory item bar, and selecting an item in the seed diary. The server answers with
the item info dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the item |
| `count` | how many you have (the inventory slot's count byte) |

- Not while trading; `audio/cant_place_tile.wav` if the item isn't in the inventory.

<small>Builders: `0x16f73e0` (item bar), `0x1d35724` (seed diary `OnItemSelect`).</small>
