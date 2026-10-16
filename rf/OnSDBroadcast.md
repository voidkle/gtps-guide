Shows a Super Duper Broadcast. It always prints the broadcast in the chat log. When no menu or dialog is
open, it also opens a dialog with the message and, if a world is given, a **GO!** button.

| # | Type | Meaning |
|---|---|---|
| 1 | string | five lines separated by `\n`: sender name, world name, then up to three message lines |
| 2 | int | non-zero = the broadcast comes from a world: show "(In world …)", embed the world name and offer **GO!**. Missing = 0 |

Message lines 3-5 go through the swear filter and the emoticon table. An empty line is skipped.

The chat log gets:

```
`w** `2Super Duper Broadcast`` from `$<sender>`` (in `$<world>``) ** :``
`w**** `#<line 3>``
`w**** `#<line 4>``
`w**** `#<line 5>``
```

The client skips the dialog if any of these is open: `ControllerDialog`, `GenericDialog`, `StoreContainer`,
`HelpMenuContainer`, `UbiclubMenuContainer`, `SurveyContainer`, `CommunityHubContainer`, `DailyMenuContainer`,
`PauseMenu`, `PuzzleParent` (`0x137d330`). Otherwise it runs its own [OnDialogRequest](./OnDialogRequest) with:

```
set_default_color|`o
add_label_with_icon|big|`2Broadcast from <sender>``|left|660|
add_smalltext|(In world <world>)|left|          <- only when argument 2 != 0
embed_data|worldname|<world>                    <- only when argument 2 != 0
add_spacer|small|
add_textbox|<line 3>|left|                      <- one per non-empty line
add_textbox|<line 4>|left|
add_textbox|<line 5>|left|
add_spacer|small|
end_dialog|sdbrespond|Cancel|GO!|               <- argument 2 != 0
end_dialog|sdbrespond|OK||                      <- argument 2 == 0
```

Pressing a button sends the usual `action|dialog_return` with `dialog_name|sdbrespond` and the embedded
`worldname`.

### Decompiled handler

```c
void OnSDBroadcast(GameLogic *self, VariantList *args) {
    std::string s = arg1.str;
    int inWorld = arg2.i;
    std::string sender = GetLine(s, 0), world = GetLine(s, 1);          // 0x1e732f4, split at '\n'
    std::string l1 = SwearFilter(GetLine(s, 2)), l2 = SwearFilter(GetLine(s, 3)), l3 = SwearFilter(GetLine(s, 4));  // 0x137d050
    ReplaceEmoticons(l1); ReplaceEmoticons(l2); ReplaceEmoticons(l3);   // 0x1e63e84

    AddToLog("`w** `2Super Duper Broadcast`` from `$" + sender + "`` (in `$" + world + "``) ** :``");
    if (!l1.empty()) AddToLog("`w**** `#" + l1 + "``");
    if (!l2.empty()) AddToLog("`w**** `#" + l2 + "``");
    if (!l3.empty()) AddToLog("`w**** `#" + l3 + "``");

    if (IsAnyMenuOpen()) return;                                        // 0x137d330
    std::string d = "set_default_color|`o\nadd_label_with_icon|big|`2Broadcast from " + sender
                  + "``|left|" + ToString(660) + "|\n";
    if (inWorld)
        d += "add_smalltext|(In world " + world + ")|left|\n" + "embed_data|worldname|" + world + "\n";
    d += "add_spacer|small|\n";
    if (!l1.empty()) d += "add_textbox|" + l1 + "|left|\n";
    if (!l2.empty()) d += "add_textbox|" + l2 + "|left|\n";
    if (!l3.empty()) d += "add_textbox|" + l3 + "|left|\n";
    d += "add_spacer|small|\n";
    d += inWorld ? "end_dialog|sdbrespond|Cancel|GO!|\n" : "end_dialog|sdbrespond|OK||\n";
    CallFunction(self, "OnDialogRequest", d);
}
```

<small>Handler: `0x136bdfc` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e732f4`, `0x137d050`, `0x1e63e84`, `0x1716724`, `0x137d330`, `0x137d650`.</small>

<!-- args: string,int -->
