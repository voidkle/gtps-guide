# action|buy

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|buy
item|{}
```

## Fields

| Field | Meaning |
|---|---|
| `item` | Store item or category id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Buys or opens a store entry.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `item` | the store entry's name |

When it is sent:

- Tapping a store entry whose name ends in `_menu`: `item` is the name without `_menu` (opens that sub-store).
- Confirming a purchase in the store's confirmation pop-up (prices from the entry's `gemCost`, `vCost`,
  `voucherCost`, `pveCost` values) and in the purchase confirmation dialog (`0x176791c`, which checks vouchers / GrowID).
- With an old `proto` (&lt; 88), the Back button sends `buy` for the previous tab instead of [storenavigate](./storenavigate).
- `mafwall`, `tapjoy` and the `video_tapjoy*` entries open offer walls / ads instead.

<small>Builders: `0x175dcdc` (store click handler), `0x176791c` (purchase confirmation).</small>

## Server

gurotopia: [`include/action/buy.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/buy.cpp).

Reply: `OnStorePurchaseResult` and an updated `OnStoreRequest`.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|buy\nitem|main\n");
```

<small>Client function: `0x175dcdc, 0x176791c` in libgrowtopia.so 5.60.</small>
