Finishes the client's item picker with a chosen item, as if the player had picked it.
Registered by `ItemPickerScreen::OnActivate` (`0x1b8cdc0`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the item id; missing reads as 0 |

- Calls the picker's result callback (ItemPickerScreen+0x380) with the id, then closes the picker (`0x179c59c`,
  which logs `[Controllers] PopController: ...`). With no callback set it only closes it.
- The callback belongs to whatever opened the picker, for example a dialog's `add_item_picker`
  (see [Dialog elements](/guide/dialog-elements)).

### Decompiled handler

```c
void OnItemPicker_Selected(ItemPickerScreen *self, VariantList *v) {   // lambda 0x1b8d32c
    if (self->callback) { int id = v[1].GetINT32(); self->callback->Invoke(&id); }   // +0x380, vtable +0x30
    PopController(self);                                                // 0x179c59c
}
```

<small>Handler: lambda `0x1b8d32c` (registered by `0x1b8cdc0`) in the 5.60 arm64 client; callees read: `0x179c59c`.</small>

<!-- args: int -->
