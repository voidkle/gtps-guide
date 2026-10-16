Checks a world name while you type it in the world-select box, so the screen can show whether it exists.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `name` | the text in the name box |

- Sent from the screen's update (`0x1c162ec`) only when the typed text changed since the last check, it isn't empty,
  no check is pending (+0x3ac) and a small delay timer (+0x3f8) has passed.
- Logs "Validing World Now %s" and sets the pending flag until the answer arrives.

```c
void WorldSelect::Validate(std::string name) {               // 0x1c163d0
    Log("Validing World Now %s", name);
    self->validating = true;                                  // +0x3ac
    SendText(3, "action|validate_world\nname|" + name + "\n");
}
```

<small>Builder: `0x1c163d0`; called from `0x1c162ec`.</small>
