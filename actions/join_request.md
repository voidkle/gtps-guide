# action|join_request

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|join_request
name|{}
invitedWorld|{}
```

## Fields

| Field | Meaning |
|---|---|
| `name` | World name. Letters and digits only, at most 24 characters. gurotopia uppercases it. |
| `invitedWorld` | `1` if joining from an invite, otherwise `0`. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia: [`include/action/join_request.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/join_request.cpp).

Reply: `SEND_MAP_DATA` (0x04), `OnEmoticonDataChanged`, `OnSpawn` for every player (yours has `type|local`), `OnSetPos`, `OnConsoleMessage`, `OnSetClothing`, `OnCountryState`. On a bad name: `OnFailedToEnterWorld`.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|join_request\nname|START\ninvitedWorld|0\n");
```

<small>Client function: `0x1383e28, 0x1c1653c` in libgrowtopia.so 5.60.</small>
