# OnDaylightDragon

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the state of a player's Daylight Dragon (the player in the CALL_FUNCTION header's `netID`). By the
field use it's a state number with an optional animated change; what each state number looks like wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the new state. If it equals the current one (avatar+0x2b48), nothing happens |
| 2 | int | 1 = set it even if a state is already set |
| 3 | int | 1 = change with an animation, using arguments 4–6 |
| 4 | uint | only with arg 3 = 1: a value stored as float (renderer+0x2820); probably the animation start or progress |
| 5 | uint | only with arg 3 = 1: a value stored as float (renderer+0x2824); probably the animation length |
| 6 | int | only with arg 3 = 1: the state to animate from when no state is set yet |

Without arg 3 = 1, arguments 4–6 aren't read.

### Decompiled handler

```c
void NetAvatar::OnDaylightDragon(VariantList *args) {          // 0x12f90b4
    int state = args->GetInt(0), force = args->GetInt(1), animate = args->GetInt(2);
    uint a = 0, b = 0; int from = -1;
    if (animate == 1) { a = args->GetUInt(3); b = args->GetUInt(4); from = args->GetInt(5); }
    if (this->dragon.current == state) return;                  // avatar+0x2b48
    SetDragonState(&this->renderer, state, force == 1, animate == 1, a, b, from);   // 0x10d7d04
}

void SetDragonState(Renderer *r, int state, bool force, bool animate, uint a, uint b, int from) {
    if (animate) {
        r->dragon.a = (float)a; r->dragon.b = (float)b;         // +0x2820, +0x2824
        if (r->dragon.current == -1) r->dragon.current = from;
        r->dragon.next = state;                                 // +0x281c
        return;
    }
    if (!force && r->dragon.current != -1) return;
    r->dragon.current = state; r->dragon.next = -1; r->dragon.a = r->dragon.b = 0;
}
```

<small>Handler: `0x12f90b4` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x10d7d04`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDaylightDragon", 1, 1, 1, 1u, 1u, 1 }, pPeer->netid);
```
