Shows a notification with a picture, a text and an optional sound.

| # | Type | Meaning |
|---|---|---|
| 1 | string | image file, e.g. `interface/atomic_button.rttex` |
| 2 | string | the message text |
| 3 | string | sound file to play, e.g. `audio/hub_open.wav`; empty = no sound |
| 4 | int | 0 (or missing): a small notification that slides in (`Notification` / `NotificationPic`). Non-zero: a centred pop-up from `NotificationPopup.xml` with `interface/tutorial/taptocontinue.rttex`, plays `audio/swoosh.wav` and closes on tap |

Arguments 1-3 are read without a type check, so they must really be strings. The sound plays 800 ms after the
notification appears.

### Decompiled handler

```c
// v[n] = argument n
void OnAddNotification(GameLogic *self, VariantList *v) {
    bool popup = v[4].type != 0 && v[4].i != 0;
    AddNotification(v[1].s /*image*/, v[2].s /*text*/, v[3].s /*sound*/, popup);   // 0x171cf58
    // popup ? ShowNotificationPopup (0x171c28c) : ShowNotification (0x171b8c4)
}
```

<small>Handler: `0x136fdb0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x171cf58`, `0x171b8c4`, `0x171c28c`.</small>

<!-- args: string,string,string,int -->
