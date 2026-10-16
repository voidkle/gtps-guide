Adds, changes or removes one of the event buttons on the world screen.
Registered by `EventsDataController::OnActivate` (`0x1c50d04`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the button's key |
| 2 | int | 0 removes the button with that key; anything else adds or updates it |
| 3 | string | the button as JSON (below); not read when argument 2 is 0 |

If a button with the key exists, argument 3 is parsed into it and the list is refreshed. Otherwise a new button is
made from it if the JSON parses. JSON keys (`0x14415e8`), all optional:

| Key | Type | Meaning |
|---|---|---|
| `active` | bool | shown or not |
| `name` | string | the button's name |
| `order` | int | position in the list |
| `counter`, `counterMax` | int | a counter shown on the button |
| `buttonState` | int | probably which look it uses |
| `itemIdIcon` | int | item whose icon is drawn |
| `text` | string | label |
| `rcssClass` | string | style class |
| `buttonTemplate` | string | which button template to use |
| `buttonAction` | string | what pressing it does, probably an [EventButton.OpenDialog](./EventButton.OpenDialog) screen name |
| `notification` | int | notification badge count |
| `visibilityFlag` | string or int | a flag name from the client's table (`NO_FLAG`, ...) or its number |

The same kind of data probably also comes in the `eventButtons=` part of the
[OnSuperMainStartAcceptLogon…](./OnSuperMainStartAcceptLogonHrdxs47254722215a) settings.

### Decompiled handler

```c
void OnEventButtonDataSet(EventsDataController *self, VariantList *v) {   // 0x1c5468c
    std::string key = v[1].s;
    if (v[2].GetINT32() == 0) { self->buttons.Remove(key); return; }    // 0x1c4ce70
    if (EventButton *b = self->buttons.Find(key)) {                     // 0x1c4cd2c
        b->data.FromJson(v[3].s);                                       // 0x14415e8
        self->buttons.Refresh();                                        // 0x1c4ccb8
    } else {
        EventButtonData d;
        if (d.FromJson(v[3].s)) self->buttons.Add(key, d);              // 0x1c4d704, 0x1c4cb74
    }
}
```

<small>Handler: lambda `0x1c54d28` → `0x1c5468c` (registered by `0x1c50d04`) in the 5.60 arm64 client; callees read: `0x14415e8`, `0x1c4cd2c`, `0x1c4ce70`, `0x1c4cb74`.</small>

<!-- args: string,int,string -->
