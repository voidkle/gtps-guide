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
