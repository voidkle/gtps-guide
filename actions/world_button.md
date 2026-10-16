# action|world_button

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|world_button
name|{}
```

## Fields

| Field | Meaning |
|---|---|
| `name` | World name. Letters and digits only, at most 24 characters. gurotopia uppercases it. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

A button on the world-select screen whose entity name contains `_` (category tabs and world tiles of the
server-built menu). The button's name is sent as is.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `name` | the clicked button's entity name |

- Unless the name is `_catselect_`, it is also saved as the `last_Category` setting.
- Other buttons on the same screen don't send this: `Start` joins the world named in its data, `Back`
  disconnects ([quit](./quit)), and the name box joins the typed world ([join_request](./join_request)).

```c
void WorldSelect::OnButton(Entity *b) {                      // 0x1c16adc
    std::string n = b->name;
    if (n == "Start" && ...) return JoinWorld(...);
    if (n == "Back") { Disconnect(); return; }
    if (n.find('_') != npos) {
        SendText(3, "action|world_button\nname|" + n + "\n");
        if (n != "_catselect_") SetSetting("last_Category", n);
        return;
    }
    JoinWorld(nameBox.text);                                  // 0x1c1653c
}
```

<small>Builder: `0x1c16adc`; called from `0x1c181e4`, `0x1c18294`, `0x1c183cc`, `0x1c1847c`, `0x1c1852c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

A category button in the world menu.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|world_button\nname|START\n");
```

<small>Client function: `0x1c16adc` in libgrowtopia.so 5.60.</small>
