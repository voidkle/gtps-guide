The tutorial task button. Without the tutorial flag (`0x1444df4` false) and with no menu open, the client sends this;
with it, it opens the questline screen itself (`OnDialogRequestRML("show_questline_ui")`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|tutorialTaskQuestClicked\n` |

<small>Builder: `0x1c5ad7c` (`ServerAuthPacketBuilder` table, set up in `0x1864840`).</small>
