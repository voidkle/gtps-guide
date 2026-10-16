# action|houston_validation_done

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|houston_validation_done
packageName|{}
productId|{}
purchaseTime|{}
purchaseState|{}
developerPayload|{}
purchaseToken|{}
currency|{}
price|{}
houstonTransId|{}
orderId|{}
houstonresult|{}
```

## Fields

| Field | Meaning |
|---|---|
| `packageName` |  |
| `productId` |  |
| `purchaseTime` |  |
| `purchaseState` |  |
| `developerPayload` |  |
| `purchaseToken` |  |
| `currency` |  |
| `price` | Price. |
| `houstonTransId` |  |
| `orderId` |  |
| `houstonresult` |  |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The receipt of a real-money purchase. A private server has no reason to accept these.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|houston_validation_done\npackageName|0\nproductId|0\npurchaseTime|0\npurchaseState|0\ndeveloperPayload|0\npurchaseToken|0\ncurrency|0\nprice|0\nhoustonTransId|0\norderId|0\nhoustonresult|0\n");
```

<small>Client function: `0x16dfbd0` in libgrowtopia.so 5.60.</small>
