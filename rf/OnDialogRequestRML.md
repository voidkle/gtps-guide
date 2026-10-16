Opens one of the client's built-in (RML) screens by name. Despite the name, no RML text is sent: argument 1
picks a screen the client already has. The world screen (`0x1bff3ec`) registers this function as a listener on
GameLogic's functions, so the header `netID` must be -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the screen's name, from the list below |
| 2 | string | passed to the screen's open function. The screens checked (`show_mailbox_ui` and the next three) don't read it |

If a menu is already open (`0x137d330`), the client logs `Dialog already opened. Ignore dialog {}.` and stops.
Otherwise it looks the name up in the world screen's table (WorldScreen+0x3b8, filled by the constructor
`0x1bfe46c`):

- **Found:** the client logs `Open dialog: {}` and calls the screen's function with argument 2. Each function
  builds a view model and pushes it onto the UI stack (`0x179c1b4`).
- **Not found:** the client sends `action|<argument 1>\n` to the server as a text message (type 2), so the
  server can answer with its own dialog.

The names the 5.60 client knows:

| Name |
|---|
| `show_mailbox_ui` |
| `show_auction_ui` |
| `show_auction_block_ui_setup` |
| `show_auction_block_ui_bid` |
| `show_world_lock_storage` |
| `show_world_lock_storage_from_panel` |
| `show_fashion_show_bouncer_popup` |
| `show_fashion_show_voting_popup` |
| `show_seed_diary_ui` |
| `show_hint_ui` |
| `show_questline_ui` |
| `show_concert_lights_ui` |
| `show_adult_verification_required` |
| `show_dungeon_start_ui` |
| `show_cheats_result_ui` |
| `show_wardrobe_main_ui` |

### Decompiled handler

```c
// lambda 0x1c082b0 -> 0x1c00ab0; v[1] = argument 1, v[2] = argument 2
void OnDialogRequestRML(WorldScreen *self, Variant *v) {
    std::string name = v[1].s;
    GetGameLogic();
    if (IsAnyMenuOpen()) {                                         // 0x137d330
        LogError(fmt("Dialog already opened. Ignore dialog {}.", name));
        return;
    }
    auto *entry = self->rmlScreens.find(name);                     // +0x3b8, 0x1c08a00
    if (!entry) {
        SendTextMessage(2, "action|" + name + "\n", GetApp()->client->peer);   // 0x157f060
        return;
    }
    LogError(fmt("Open dialog: {}", name));
    entry->open(self->uiStack /* +0x38 */, v[2].s);               // std::function, vtable +0x30
}
```

<small>Handler: `0x1c082b0` → `0x1c00ab0`, registered by the world screen (`0x1bff3ec`, through `0x1be9ae8`) in the 5.60 arm64 client; callees read: `0x137d330`, `0x1c08a00`, `0x1bfe46c`, `0x1c01054`, `0x1c015fc`, `0x1c01ba4`, `0x1c0214c`.</small>

<!-- args: string,string -->
