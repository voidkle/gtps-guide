Shows a short message in the middle of the screen, with a box behind it. It fades in, and probably fades out
again after about 2 seconds.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the text (color codes work) |

The text is centered horizontally on the screen and kept inside the screen edges. Its font scale is 24.0,
and a box is drawn behind it (`0x1dc7c24`). The label also gets `0x1dc8e08(e, 0xb4)`; what that sets wasn't traced. The two fades are `0x1dc4cdc(1.0, e, 1, 300, …)`, a
300 ms fade-in, and `0x1dc7178(e, 0, 500, 2000, …)`, probably a 500 ms fade-out that starts after 2000 ms.
Nothing goes into the chat log.

### Decompiled handler

```c
void OnTextOverlay(GameLogic *self, VariantList *args) {
    vec2 center = GetScreenCenter();                    // 0x1e713a4
    ShowTextOverlay(&center, arg1.str);                 // 0x17176f0
}

void ShowTextOverlay(vec2 *pos, std::string text) {     // 0x17176f0
    GetFontAndScale(24.0f, &font, &scale);              // 0x1dc9108
    vec2 size = MeasureText(font, text);                // 0x174bd38
    float x = clamp(pos->x - size.x * 0.5f, 0, ScreenWidth() - size.x);
    float y = pos->y - (size.y + ScaleY(30.0f));
    Entity *e = CreateTextLabel(x, y, root, text);      // 0x1dc3c5c
    sub_1dc8e08(e, 0xb4);
    FadeIn(e, 300);  FadeOutLater(e, 500, 2000);        // also kills the entity
    AddBackgroundBox(e, ScaleY(10.0f));                 // 0x1dc7c24, same fades
}
```

<small>Handler: `0x136d140` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e713a4`, `0x17176f0`.</small>

<!-- args: string -->
