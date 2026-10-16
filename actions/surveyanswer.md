# action|surveyanswer

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|surveyanswer
answer|{}
```

## Fields

| Field | Meaning |
|---|---|
| `answer` | Survey answer. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** one `answer|<n>` line per question, not just one.

The **submitButton** of the survey screen ([OnSurveyRequest](/functions/OnSurveyRequest)).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `answer` | repeated, one line per question in order: the index of the chosen option (`-1` if none) |

- The submit button is only enabled when every question has an answer. `button_quick_exit` closes without sending.

```c
std::string s = "action|surveyanswer\n";
for (Question *q : self->questions) s += "answer|" + to_string(q->chosen) + "\n";
SendText(2, s);
```

<small>Builder: `0x1782600`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|surveyanswer\nanswer|0\n");
```

<small>Client function: `0x1782600` in libgrowtopia.so 5.60.</small>
