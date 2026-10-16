# action|validate_world

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|validate_world
name|{}
```

## Fields

| Field | Meaning |
|---|---|
| `name` | World name. Letters and digits only, at most 24 characters. gurotopia uppercases it. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

Sent while typing a world name in the world menu.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|validate_world\nname|START\n");
```

<small>Client function: `0x1c163d0` in libgrowtopia.so 5.60.</small>
