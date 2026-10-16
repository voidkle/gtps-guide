# OnConsoleMessage

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Adds a line to the chat log (the console). Before it shows the text, the client takes some optional prefixes
off the front, replaces emoticon codes, applies the swear filter, and picks a chat tab.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the text, with `` `x `` color codes and the optional prefixes below |

The handler overwrites arguments 1, 5 and 6 with the stripped text and the parsed prefix values. It then
passes the list on to the console code (`0x137c83c`), which reads only argument 1.

### Text prefixes

They're checked in this order, and each one is removed from the text when found:

| Prefix | Example | Effect |
|---|---|---|
| `CP:<n>_` | `CP:0_hello` | Removes everything up to and including the `_` after `CP:` (the tag can appear anywhere in the text). `n` goes into argument 6; without the prefix that's 1. The console doesn't use it. |
| `PL:<n>_` | `PL:12_hi` | Only at the very start, and `n` must be all digits. `n` goes into argument 5 (−1 without it). The console doesn't use it; for [OnTalkBubble](./OnTalkBubble) it's passed on. |
| `OID:<id>_` | `OID:abc_hi` | Removed, and the value is thrown away. |

### Chat tabs

After the prefixes, the text may contain a channel tag `CT:[XX]`. The tag picks the tab the line goes to
and the label shown in front of it. The label only appears when a client option (app+0xca0) is set:

| Tag | Tab bit | Label |
|---|---|---|
| none | 0x40 | |
| `S` | 0x40 | `` `7[S] `` |
| `BC`, `CB`, `SB` | 0x01 | `` `p[BC] ``, `` `#[CB] ``, `` `5[SB] `` |
| `W` | 0x04 | `` `6[W] `` |
| `MSG` | 0x10 | `` `c[MSG] `` |
| `FC` | 0x20 | `` `3[FC] `` |
| `GC` | 0x80 | `` `2[GC] `` |

A part in `<…>` (up to the first `>`) is treated as the sender. With the `chatTimestamp` option on, the
client puts a `[hh:mm] ` time in front of the line.

### Other processing

- **Emoticons.** Codes from the table set by [OnEmoticonDataChanged](./OnEmoticonDataChanged) are replaced
  in the text (`0x1e63e84`).
- **`player_chat=`.** If the text contains `player_chat=`, the part before the first `>` is rebuilt without
  that marker, probably so the client can recognise player chat for blocking.
- **Swear filter.** It runs when the `swearFilter` option is on (`0x137ce9c`).
- **Blocking.** The client has a branch that shows `Blocked | <text>` instead, but in this build its check
  (`0x15876e0`) always returns false.

### Decompiled handler

```c
void OnConsoleMessage(GameLogic *self, VariantList *args) {
    std::string text = arg1.str;
    int cp = StripPrefixCP(&text);         // 0x1588078: "CP:<n>_", default 1
    int pl = StripPrefixPL(&text);         // 0x15876e8: "PL:<n>_", default -1
    std::string oid; StripPrefixOID(&oid, &text);   // 0x1587b10: "OID:<x>_" (unused)
    arg1.Set(text);
    arg5.SetInt(pl);
    arg6.SetInt(cp);
    AddConsoleMessage(args);               // 0x137c83c
}

void AddConsoleMessage(VariantList *args) {   // 0x137c83c
    std::string text = arg1.str;
    if (IsBlocked(text)) {                 // 0x15876e0: always false
        AddToLog("Blocked | " + text);
        return;
    }
    text = ReplaceEmoticons(text);         // 0x1e63e84
    if (HasField(text, "player_chat=")) ...   // strip the marker before the first '>'
    ChatTag tag = ParseChatTag(text);      // 0x1588540: CT:[..], <sender>, chatTimestamp
    SwearFilter(&text, tag.tab != 0x40);   // 0x137ce9c, "swearFilter"
    AddToLog(text);                        // 0x1716724: LogDisplayEntity / TabComponent
}
```

<small>Handler: `0x136bc70` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1588078`, `0x15876e8`, `0x1587b10`, `0x137c83c`, `0x1588540`, `0x1e63e84`, `0x137ce9c`, `0x1716724`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnConsoleMessage"` |
| 1 | string | text with `` `x `` color codes |

gurotopia: `include/onVariant/ConsoleMessage.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnConsoleMessage", "..." });
```
