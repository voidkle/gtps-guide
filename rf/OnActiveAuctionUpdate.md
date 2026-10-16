Updates the auction that is running right now: the auction event button and, if it's open, the bid screen. Two
listeners on GameLogic's functions (through `0x1be9ae8`), both needing header `netID` -1, each only while its
controller is active: `EventsDataController::OnActivate` (`0x1c50d04`) and `AuctionBlockBidController::OnActivate`
(`0x1c75470`).

| # | Type | Meaning |
|---|---|---|
| 1 | string | JSON, below |

| Key | Type | Read by | Meaning |
|---|---|---|---|
| `Active` | bool | both | false: no auction is running; the button's data is cleared and its timer stopped |
| `ItemId` | int | event button | the item being auctioned |
| `HighestBidUserName` | string | both | name of the highest bidder |
| `HighestBidWlCount` | int | both | the highest bid, in World Locks |
| `AvailableLocks` | int | both | probably how many locks you can bid |
| `AlreadyPlaced` | int | both | probably how many locks you have already bid |
| `BidEndTime` | int | both | when bidding ends (probably a Unix time) |
| `BidDelay` | int | bid screen | the delay between bids; only taken while the stored value is 0 |

- Event button: with `Active` true the client starts a timer that updates the button every model+0x350 seconds
  (+ 500 ms) and copies a counter to the auction button.
- Event button: the client also looks up the world's Auction Block tile (item 15546) and stores whether you have
  access to it (`0x15b5d5c`).
- Bid screen: sets a flag when the bid value on the world's Auction Block is below `HighestBidWlCount`.

<small>Handlers: lambda `0x1c54e38` → `0x1c539c0` (loader `0x1c69054`) and lambda `0x1c75f08` → `0x1c75a7c` (loader `0x1c701b8`) in the 5.60 arm64 client.</small>

<!-- args: string -->
