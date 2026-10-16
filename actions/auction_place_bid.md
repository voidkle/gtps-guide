# action|auction_place_bid

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|auction_place_bid
bidAmount|{}
```

## Fields

| Field | Meaning |
|---|---|
| `bidAmount` | Bid in World Locks. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Places a bid on the auction screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `bidAmount` | the bid (the clicked element's `bid_amount`/`bid_value` attribute, an int) |

- Only when the bid is valid for the item (`0x1c68c34`) and no bid is pending; a timer of (item duration × 1000 + 500) ms
  then blocks the next bid. The second builder sends a bid that was confirmed in a pop-up.

<small>Builders: `0x1c518fc` (bid button), `0x1c7587c` (confirm, via `0x1c75d50`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|auction_place_bid\nbidAmount|0\n");
```

<small>Client function: `0x1c518fc` in libgrowtopia.so 5.60.</small>
