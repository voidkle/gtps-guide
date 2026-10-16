# action|auction_getpage

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|auction_getpage
pageIndex|{}
sortType|{}
searchItem|{}
```

## Fields

| Field | Meaning |
|---|---|
| `pageIndex` | Page number. |
| `sortType` | Sort order. |
| `searchItem` | Search text. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The auction house asks for a page (open, next page, sort, item search).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1) |
| `sortType` | the chosen sort (`Auction.ApplySort`) |
| `searchItem` | the searched item id (`Auction.OpenItemSearch`), probably 0 when cleared |

- Ignored while a request is already pending; the client waits up to 30 s for `OnRequestAuctionPage`.

<small>Builder: `0x1c90084`; called from `0x1c8fb40`, `0x1c90e28`, `0x1c91ba4`, `0x1c92408`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|auction_getpage\npageIndex|0\nsortType|0\nsearchItem|0\n");
```

<small>Client function: `0x1c90084` in libgrowtopia.so 5.60.</small>
