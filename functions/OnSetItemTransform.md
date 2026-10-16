# OnSetItemTransform

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Switches an item's "transformed" look on for a player (the player in the CALL_FUNCTION header's `netID`).
All transforms are cleared first, exactly like [OnClearItemTransforms](./OnClearItemTransforms), then the
item's behaviour is told to transform.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id; ignored if the item has no behaviour object |

### Decompiled handler

```c
void NetAvatar::OnSetItemTransform(VariantList *args) {     // 0x12f9618
    this->OnClearItemTransforms(args);                      // 0x12f9694
    if (ItemBehaviour *b = ItemBehaviours()->Find(args->GetInt(0)))   // 0x11f60d8
        b->SetTransform(&this->renderer, true);             // vtable +0x2f8
}
```

<small>Handler: `0x12f9618` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x12f9694`, `0x11f60d8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetItemTransform", 1 }, pPeer->netid);
```
