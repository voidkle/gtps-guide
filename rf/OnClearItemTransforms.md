Switches off the "transformed" look of every item a player wears (the player in the CALL_FUNCTION header's
`netID`). No arguments.

For each of the nine clothing slots (avatar+0x29e … +0x2ae, u16 item ids), the client looks up the item's
behaviour and tells it to un-transform.

### Decompiled handler

```c
void NetAvatar::OnClearItemTransforms() {                  // 0x12f9694
    for (int i = 0; i < 9; i++) {
        ItemInfo *it = GetItem(this->clothes[i]);          // avatar+0x29e + 2*i, 0x1564a48
        if (!it) continue;
        if (ItemBehaviour *b = ItemBehaviours()->Find(it->id))
            b->SetTransform(&this->renderer, false);       // vtable +0x2f8
    }
}
```

<small>Handler: `0x12f9694` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1564a48`, `0x11f60d8`.</small>

<!-- args: -->
