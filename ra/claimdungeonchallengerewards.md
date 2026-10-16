A challenge button on the dungeon start screen (`DungeonStartUi.OnChallengeButtonClicked`). One handler sends
`activatedungeonchallenge`, `giveupdungeonchallenge` or `claimdungeonchallengerewards` depending on the
challenge's state; this one is sent when the challenge is completed and its reward not claimed yet (state 2).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `questid` | the challenge id, from the clicked element's id attribute |
| `isChal` | `1` if the element has `is_optional` = `1`, else `0` (probably "optional challenge" vs main quest) |

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
