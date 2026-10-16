**Format correction:** after `status|`, the client appends one `item|<id>|<count>\n` line for each filled slot of
one side of the trade (the four slots at trade+0xf0; which side wasn't traced, probably the other player's offer, so
the server can check that you accepted what you saw).

The **AcceptTrade** button.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `status` | `1` if you haven't accepted yet (trade+300 == 0), else `0` (toggle) |
| `item` lines | `item\|<item id>\|<count>` per filled slot |

- With a new enough `proto` (feature 10) it does nothing while another menu is open.
- Logs "Trade accepted" and updates the button state locally (`0x178b970`).

```c
SendText(2, "action|trade_accept\nstatus|" + to_string(!trade->accepted) + "\n" + TradeItems(trade));  // 0x178b618
```

<small>Builder: `0x178aeec`; item list `0x178b618`.</small>
