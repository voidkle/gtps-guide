# action|giveupdungeonchallenge

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|giveupdungeonchallenge
|chalid|{}
```

## Fields

| Field | Meaning |
|---|---|
| `chalid` | Challenge id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

A challenge button on the dungeon start screen (`DungeonStartUi.OnChallengeButtonClicked`). One handler sends
`activatedungeonchallenge`, `giveupdungeonchallenge` or `claimdungeonchallengerewards` depending on the
challenge's state; this one is sent when the challenge is active and can be given up (challenge+0x45) (state 1).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `chalid` | the challenge id, from the clicked element's id attribute |


- The screen closes after a claim.

```c
Challenge *c = Find(atoi(el->GetAttribute("id")), el->GetAttribute("is_optional") == "1");   // 0x1cca984
switch (c->state) {
case 0: Send(fmt("action|activatedungeonchallenge\n|chalid|{}\n", c->id)); break;
case 1: if (c->canGiveUp) Send(fmt("action|giveupdungeonchallenge\n|chalid|{}\n", c->id)); break;
case 2: if (!c->claimed) { Send(fmt("action|claimdungeonchallengerewards\n|questid|{}\n|isChal|{}\n", c->id, optional)); Close(); } break;
}
```

<small>Builder: `0x1cd416c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|giveupdungeonchallenge\n|chalid|0\n");
```

<small>Client function: `0x1cd416c` in libgrowtopia.so 5.60.</small>
