Fills the auction list screen with a page of auctions.
Registered by `AuctionController::OnActivate` (`0x1c8fb40`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 0: nothing to show; the list stays empty |
| 2 | int | stored on the list (model+0x70), probably the page number |
| 3 | int | stored on the list (model+0x30), probably the number of pages |
| 4 | string | JSON `{"Items": [ ... ]}`, one object per auction |

Each item object has `id`, `bid` and `endTime` (numbers), `world` (string), and one more number whose key wasn't
recovered. The list is cleared first. The call is ignored while the screen is in its search mode (model+0x59). A
100 ms timer then refreshes the screen.

<small>Handler: lambda `0x1c91658` → `0x1c905ac` (registered by `0x1c8fb40`) in the 5.60 arm64 client.</small>

<!-- args: int,int,int,string -->
