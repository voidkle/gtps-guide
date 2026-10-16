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
