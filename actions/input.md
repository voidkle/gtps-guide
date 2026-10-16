# action|input

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|input
|text|{}
```

## Fields

| Field | Meaning |
|---|---|
| `text` | Chat text. Starts with `/` for commands. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** the text is **not** followed by `\n`: `action|input\n|text|<text>`. When the client's own
chat filter flags the text, `\n|[FT##]|1` is appended.

Chat: sent when you press Enter in the chat box (the classic GUI and the new world UI both use this).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `text` | what you typed, unchanged (commands like `/help` too) |
| `[FT##]` | optional extra line `\|[FT##]\|1`: the local profanity filter (`0x1490f20`) matched the text |

- Nothing is sent if the box is empty or you aren't connected (app client +0xa5).
- With the "disable chat" personal setting (account flag 0x2000) only text that passes `0x1231e98` (probably commands)
  is sent; anything else shows "Chat is disabled."

```c
void SendChat(std::string text) {                             // 0x1682f84 / 0x1c2477c
    if (text.empty() || !Connected()) return;
    if (HasFlag(0x2000) && !IsAllowedWhenChatDisabled(text)) { Toast("Chat is disabled."); return; }
    std::string msg = fmt("action|input\n|text|{}", text);
    if (FilterEnabled()) { bool hit = false; Filter(text, &hit); if (hit) msg += "\n|[FT##]|1"; }
    SendText(2, msg);
}
```

<small>Builders: `0x1682f84` (classic chat box), `0x1c2477c` (world UI chat, Enter key `0x48` in `0x1c246dc`).</small>

## Server

gurotopia: [`include/action/input.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/input.cpp).

Reply: Chat: `OnTalkBubble` and `OnConsoleMessage` to everyone in the world. Commands (`/...`): handled in `include/commands/`.

## Notes

The client sometimes appends `\n|[FT##]|1`. gurotopia rate-limits 5 messages in 6 seconds.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|input\n|text|hello");
```

<small>Client function: `0x1682f84, 0x1c2477c` in libgrowtopia.so 5.60.</small>
