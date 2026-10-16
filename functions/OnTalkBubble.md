# OnTalkBubble

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows a speech bubble over a player. The text gets the same prefix handling as
[OnConsoleMessage](./OnConsoleMessage) (`CP:`, `PL:`, `OID:`), plus emoticons, chat tags and the swear
filter. A smiley in the text also changes the speaker's face for a moment. The bubble does **not** go into the
chat log.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | netID of the speaker; if nobody has that netID the client logs "Unable to find netObj %d" |
| 2 | string | the text |
| 3 | uint | optional line style, stored with the line. With 2 the bubble uses different colors (`0x0f851eff` / `0x5fe69aff` instead of `0x9f7d27ff` / `0xfbe3a5ff`). Missing = 0 |
| 4 | uint | optional; non-zero **replaces** the bubble's text, 0 **adds** a line (a bubble keeps at most 4 lines). Missing = 0 |
| 5 | int | overwritten by the client with the `PL:` prefix value (−1 if none); not read afterwards |
| 6 | int | overwritten with the `CP:` value (1 if none); not read afterwards |

How long a line stays: 90 ms per character, not counting color codes (`0x1e74058`), but at least 4 seconds.

A face change happens if the text contains one of these smileys: `:)` `=)` `:-)` `;)` `;-)` `>:(` `:D` `lol` `LOL`
`:*` `:(` `:P` `:p` `:O` `:o` `:O.O` `:~(` `:'(` `:,(` `:|` `:/` `:,` `0-0` `-_-`. Each sets a face id on the
avatar (avatar+0x100) together with the value 3.0, probably the face's duration in seconds (`0x1312e8c`). The
smileys are then removed from the bubble text (`0x1580360`), so a bubble that was only a smiley shows nothing.

The bubble is only drawn when the world renderer exists (GameLogic+0xe0) and the final text isn't empty.

### Decompiled handler

```c
void OnTalkBubble(GameLogic *self, VariantList *args) {
    self->f_2ec = 0;
    if (self->pendingChaching && self->world) { sub_1083db8(); self->pendingChaching = 0; }
    std::string text = arg2.str;
    int cp = StripPrefixCP(&text), pl = StripPrefixPL(&text);
    std::string oid; StripPrefixOID(&oid, &text);
    arg2.Set(text); arg5.SetInt(pl); arg6.SetInt(cp);
    ShowTalkBubble(self, args);                                   // 0x137d9a4
}

void ShowTalkBubble(GameLogic *self, VariantList *args) {         // 0x137d9a4
    std::string text = arg2.str;
    int netID = arg1.u, style = arg3.u, replace = arg4.u;
    NetAvatar *a = NetObjects()->Get(netID);
    if (!a) { Log("Unable to find netObj %d", netID); return; }
    a->SetFaceFromText(text);                                     // 0x1312e8c
    text = ReplaceEmoticons(text);
    ChatTag tag = ParseChatTag(text);                             // 0x1588540
    if (!HasField(text, "player_chat=")) {
        RemoveSmileys(&text);                                     // 0x1580360
        SwearFilter(&text, tag.tab != 0x40);                      // 0x137ce9c
    } else {
        ... the same on the player_chat= value, then "player_chat=" + value
    }
    if (!text.empty() && self->worldRenderer)                     // +0xe0
        self->bubbles.Say(netID, text, style, replace != 0);      // 0x1182458, self+0x1b0
}
```

<small>Handler: `0x136cf9c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x137d9a4`, `0x1312e8c`, `0x1182458`, `0x1189da8`, `0x1189f04`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnTalkBubble"` |
| 1 | int | netID of the speaker |
| 2 | string | text |
| 3 | uint | optional: 1 = also in console |
| 4 | uint | optional |

gurotopia: `include/action/input.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnTalkBubble", 1u, "...", 1u, 1u });
```
