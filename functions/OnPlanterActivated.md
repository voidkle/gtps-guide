# OnPlanterActivated

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client what the planter (items with action type 112) holds and where it is. The values are stored on the game
logic (+0xa4, +0xa8, +0xac) and used later:

- The inventory icon of a type-112 item draws the stored item on top of it.
- When you place a type-112 item, the client checks the tile at (#2, #3). If its extra data is of kind `G` or `>` with a
  non-empty list, the "item flies" animation shows the stored item instead of the planter.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | item id the planter holds (0 = none) |
| 2 | uint | the planter's tile x |
| 3 | uint | the planter's tile y |

### Decompiled handler

```c
// v[n] = argument n
void OnPlanterActivated(GameLogic *self, VariantList *v) {
    self->planterItem = v[1].GetUINT();      // +0xa4
    self->planterX    = v[2].GetUINT();      // +0xa8
    self->planterY    = v[3].GetUINT();      // +0xac
}
```

<small>Handler: `0x1370c78` (dispatcher `0x135e25c`) in the 5.60 arm64 client; readers: `0x10d6488` (place animation), `0x11668c0` (inventory icon).</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPlanterActivated", 1u, 1u, 1u });
```
