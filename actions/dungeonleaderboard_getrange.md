# action|dungeonleaderboard_getrange

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|dungeonleaderboard_getrange
startIndex|{}
endIndex|{}
relative|{}
```

## Fields

| Field | Meaning |
|---|---|
| `startIndex` | First row. |
| `endIndex` | Last row. |
| `relative` | Rows relative to you. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The dungeon leaderboard asks for a range of entries.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `startIndex` | first entry |
| `endIndex` | last entry; must be greater than `startIndex` or nothing is sent |
| `relative` | probably 1 for a range around your own rank |

- The client waits up to 5 s for the answer.

<small>Builder: `0x1cc00c4`; called from `0x1cbf6b4`, `0x1cc045c`, `0x1cc0590`, `0x1cc347c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|dungeonleaderboard_getrange\nstartIndex|0\nendIndex|0\nrelative|0\n");
```

<small>Client function: `0x1cc00c4` in libgrowtopia.so 5.60.</small>
