The favourite (star) button of the inventory item bar.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `itemID` | the selected item |

- Only when the server's `proto` allows favourites, not while trading, if the item is in the inventory, can be a
  favourite (`0x156d3d0`) and isn't one yet; the client marks it locally at once. Otherwise `audio/cant_place_tile.wav`.
- The answer is [OnFavItemUpdated](/functions/OnFavItemUpdated).

<small>Builder: `0x16f7c64`; called from `0x16f6aa0`.</small>
