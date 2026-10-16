Adds a named tutorial arrow (`interface/tutorial/tut_arrow.rttex`) that points at something in the world or
the HUD. An arrow with the same name is removed first. Remove arrows with
[OnClearTutorialArrow](./OnClearTutorialArrow) or [OnClearAllTutorialArrows](./OnClearAllTutorialArrows).

| # | Type | Meaning |
|---|---|---|
| 1 | string | the arrow's name (used to replace or clear it) |
| 2 | int | stored with the arrow (+0x98); the value 270 sets an extra flag (+0x89). Probably the arrow's angle in degrees |
| 3 | uint | non-zero sets a flag on the arrow (+0x9c); meaning not traced |
| 4 | uint | what the arrow points at, see below |
| 5 | any | the target: an int or a string depending on argument 4 (the whole variant is copied) |
| 6 | string | kept by the arrow's target object; meaning not traced |

The handler also reads a 7th argument as a vec2 offset, but a CALL_FUNCTION list only holds 6 arguments, so
it is always the default `(1, 0)`.

Argument 4 picks the target class (`0x11542cc`):

| Value | Class | Argument 5 |
|---|---|---|
| 0 | `HudIndicatorTileTarget` | int |
| 1 | `HudIndicatorEntityTarget` | string (a GUI entity name) |
| 2 | `HudIndicatorItemTarget` | int (item id) |
| 3 | `HudIndicatorTileItemTarget` | int |
| 4 | `HudIndicatorFloatingItemTarget` | int |
| 5 | `HudIndicatorEmptyTile` | int |
| 6 | `HudIndicatorSpliceTreeTarget` | int |
| 7 | `HudIndicatorNetAvatarWrenchTarget` | int (only `!= 0` is kept) |
| 8 | `HudIndicatorSurgeryButttonTarget` | string |
| 9 | `HudIndicatorEditableTileItemTarget` | int |
| 10 | `HudIndicatorEventButtonTarget` | string |
| 11 | `HudIndicatorItemTypeTarget` | int (converted by `0x1158dbc`, probably item id → item type) |
| other | none, no arrow | |

### Decompiled handler

```c
void OnTutorialArrow(GameLogic *self, VariantList *args) {
    TutorialArrow a = {};
    a.name     = arg1.str;
    a.angle    = arg2.i;          // +0x98
    a.flag     = arg3.u != 0;     // +0x9c
    a.kind     = arg4.u;          // +0x18
    a.target   = arg5;            // +0x20, Variant copy
    a.text     = arg6.str;        // +0x68
    if (args[6].type) a.offset = args[6].vec2;   // never present
    self->tutorial->Add(&a);      // 0x11505ac, self+0x1e8
}

void Tutorial::Add(TutorialArrow *a) {           // 0x11505ac
    Texture *t = GetTexture("interface/tutorial/tut_arrow.rttex");
    if (!t) { this->texture = NULL; return; }
    a->texture = t;
    Remove(a->name);                              // 0x1150764
    a->scale = {0, 1.0f};
    a->is270 = (a->angle == 270);                 // +0x89
    arrows.push_back(*a);                         // builds the HudIndicator* target (0x11542cc)
}
```

<small>Handler: `0x136d814` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x11505ac`, `0x1150764`, `0x115414c`, `0x11542cc`.</small>

<!-- args: string,int,uint,uint,int,string -->
