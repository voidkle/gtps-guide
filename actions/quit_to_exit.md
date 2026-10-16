# action|quit_to_exit

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|quit_to_exit
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** the client sends `action|quit_to_exit` with **no** trailing `\n`.

Leaving a world. The world-select screen sends it every time it opens (its activate method, vtable slot of
`WorldSelectScreen`), so it follows the Quit/Exit button in the pause menu.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| text | `action\|quit_to_exit` |

- Before sending, the screen starts listening for `OnFailedToEnterWorld` and `GameTextMessage`.
- Afterwards it shows the world menu UI; the server is expected to answer with
  [OnRequestWorldSelectMenu](/functions/OnRequestWorldSelectMenu).

```c
void WorldSelectScreen::OnActivate() {                        // 0x1c10eb8
    Listen("GameTextMessage", ...); Listen("OnFailedToEnterWorld", ...);
    SendText(3, "action|quit_to_exit");
    ShowWorldMenu();                                          // 0x1dd34a4, 0x1716d88, 0x16fc630
}
```

<small>Builder: `0x1c10eb8` (`WorldSelectScreen` vtable slot `0x29247c0`).</small>

## Server

gurotopia: [`include/action/quit_to_exit.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/quit_to_exit.cpp).

Reply: `OnRemove` to the others in the world, then the world menu.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|quit_to_exit");
```

<small>Client function: `0x1c10eb8` in libgrowtopia.so 5.60.</small>
