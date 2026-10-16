Closes the client's item picker without a choice. The picker's callback isn't called.
Registered by `ItemPickerScreen::OnActivate` (`0x1b8cdc0`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments are read.

```c
void OnItemPicker_Cancelled(ItemPickerScreen *self) {   // lambda 0x1b8d45c
    PopController(self);                                 // 0x179c59c
}
```

<small>Handler: lambda `0x1b8d45c` (registered by `0x1b8cdc0`) in the 5.60 arm64 client.</small>

<!-- args: -->
