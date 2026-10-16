Places a bid on the auction screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `bidAmount` | the bid (the clicked element's `bid_amount`/`bid_value` attribute, an int) |

- Only when the bid is valid for the item (`0x1c68c34`) and no bid is pending; a timer of (item duration × 1000 + 500) ms
  then blocks the next bid. The second builder sends a bid that was confirmed in a pop-up.

<small>Builders: `0x1c518fc` (bid button), `0x1c7587c` (confirm, via `0x1c75d50`).</small>
