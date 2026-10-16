Asks to enter a world. Sent when you pick a world on the world-select screen (typed name, world button,
`OPENWORLD` dialog links, the auction "go to world" and world-lock storage "visit" buttons).

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `name` | the world name as given (the client also saves it, probably upper-cased, as the `lastworld` setting) |
| `invitedWorld` | always `0` from these builders |

- If you hold the Fist (item 18) in your inventory it is re-selected first, and an open trade is closed.
- After sending, the client shows its "Entering world" loading message and waits for
  [SEND_MAP_DATA (0x04)](/packets/04-send-map-data) or `OnFailedToEnterWorld`.

```c
void JoinWorld(GameLogic *self, std::string name) {          // 0x1383e28 (also 0x1c1653c on the world screen)
    if (HasItem(self->inventory, 18)) { self->selected = 18; CloseTrade(); ... }
    SetSetting("lastworld", ToUpper(name));                   // 0x1e6e8f8, probably upper-case
    SendText(3, "action|join_request\nname|" + name + "\ninvitedWorld|" + to_string(0) + "\n");
    ShowLoading("Entering world");
}
```

<small>Builder: `0x1383e28` (wrapper `0x13843a4`, 9 callers) and `0x1c1653c` (world-select screen); called from `0x1c16adc`, `0x1693460`, `0x1c91218`, `0x1d7d680`.</small>
