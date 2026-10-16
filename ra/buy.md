Buys or opens a store entry.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `item` | the store entry's name |

When it is sent:

- Tapping a store entry whose name ends in `_menu`: `item` is the name without `_menu` (opens that sub-store).
- Confirming a purchase in the store's confirmation pop-up (prices from the entry's `gemCost`, `vCost`,
  `voucherCost`, `pveCost` values) and in the purchase confirmation dialog (`0x176791c`, which checks vouchers / GrowID).
- With an old `proto` (< 88), the Back button sends `buy` for the previous tab instead of [storenavigate](./storenavigate).
- `mafwall`, `tapjoy` and the `video_tapjoy*` entries open offer walls / ads instead.

<small>Builders: `0x175dcdc` (store click handler), `0x176791c` (purchase confirmation).</small>
