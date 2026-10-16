After an in-app purchase is validated with Ubisoft's purchase service ("houston", `iap-mob.ubi.com`), the client
reports the receipt to the game server.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `packageName`, `productId`, `purchaseTime`, `purchaseState`, `developerPayload`, `purchaseToken` | from the store receipt (Google Play JSON) |
| `currency`, `price` | the product's price |
| `houstonTransId` | the purchase service's transaction id |
| `orderId` | the store order id |
| `houstonresult` | the purchase service's result |

<small>Builder: `0x16dfbd0`; called from the purchase flow `0x16debe0`.</small>
