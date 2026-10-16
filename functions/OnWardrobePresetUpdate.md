# OnWardrobePresetUpdate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Fills the wardrobe save/load screen with your saved outfits.
Registered by `WardrobeSaveLoadUiController::OnActivate` (`0x1d683d8`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

The format depends on `proto` (app+0xc08, `0x117e8cc`):

| `proto` | # | Type | Meaning |
|---|---|---|---|
| &lt; 226 | 1 | string | preset 1 |
| &lt; 226 | 2 | string | preset 2 |
| ≥ 226 | 1 | string | JSON `{"PresetCount": n, "Presets": ["...", ...]}`; presets after the first `n` are shown locked. An empty string does nothing |

A preset is 10 comma-separated item ids, one per clothing slot (`0x1d67860`); a preset with another number of
fields is ignored. 0 is an empty slot (blue border); items get an orange border, and the client notes when one of
them isn't in your inventory. A JSON error logs "New wardrobe save load ui data Parse Error!!!".

<small>Handler: lambda `0x1d68af4` → `0x1d673cc` in the 5.60 arm64 client; callees read: `0x1d67860`, `0x1d5e370`, `0x1d5e778`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnWardrobePresetUpdate", "...", "..." });
```
