The auction house asks for a page (open, next page, sort, item search).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1) |
| `sortType` | the chosen sort (`Auction.ApplySort`) |
| `searchItem` | the searched item id (`Auction.OpenItemSearch`), probably 0 when cleared |

- Ignored while a request is already pending; the client waits up to 30 s for `OnRequestAuctionPage`.

<small>Builder: `0x1c90084`; called from `0x1c8fb40`, `0x1c90e28`, `0x1c91ba4`, `0x1c92408`.</small>
