# OnResetInventoryPosRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Moves the inventory panel back to its default height. The panel is the `ItemsParent` GUI entity, and it slides
there over 200 ms. The client then saves the resulting height in the `defaultInventoryHeight` option.

No arguments are read.

### Decompiled handler

```c
void OnResetInventoryPosRequest(GameLogic *self) {          // 0x135d12c: tail call to 0x16f656c
    Entity *items = FindEntity(GetEntityRoot(), "ItemsParent");
    if (!items) return;
    vec2 pos = GetPos(items);
    MoveTo(items, pos /* y from the default slot 0x29dc16c */, 200, 1, 0);   // 0x1dc5668
    g_inventoryY = <new y>;                                   // 0x29dc1b4
    GetApp()->GetVar("defaultInventoryHeight")->SetFloat(g_inventoryY);
}
```

<small>Handler: `0x135d12c` → `0x16f656c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1dc5668`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnResetInventoryPosRequest" });
```
