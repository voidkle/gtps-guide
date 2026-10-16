Tapping the **Remove Favorites** entry (item 13720) in the inventory, when the server's `proto` allows favourites.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|inventoryfavuitrigger\n` |

- The same tap handler sends `action|storenavigate\nitem|locks\nselection|upgrade_backpack\n` for the
  **Increase Backpack** entry (item 9412).

<small>Builder: `0x13940cc` (inventory touch handler, set up in `0x13925b8`).</small>
