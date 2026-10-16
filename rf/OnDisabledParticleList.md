Replaces the lists of particle effects the client should not draw. The argument is a comma-separated list of
`V1-<id>` and `V2-<id>` entries; each id goes into one of two sets kept by the world renderer. An empty string
clears both sets. Ignored when there is no world renderer (no world loaded).

| # | Type | Meaning |
|---|---|---|
| 1 | string | `V1-<id>,V2-<id>,...`; empty = clear both lists |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

- Entries are split on `,`, then each entry on `-`. Only entries whose first part is exactly `V1` or `V2` are used;
  the second part goes through `atoi`. Anything else is skipped.
- `V1` ids go to the set at renderer+0x178, `V2` ids to renderer+0x1a0. These are probably the ids of
  [OnParticleEffect](/functions/OnParticleEffect) (V1) and [OnParticleEffectV2](/functions/OnParticleEffectV2) (V2).
- A non-empty list **adds** to the sets; it doesn't clear them first. Send an empty string to reset.

### Decompiled handler

```c
void GameLogic::OnDisabledParticleList(GameLogic *self, VariantList *vl) {
    if (!self->renderer) return;                                  // self+0xe0
    std::string list = vl[1].s;                                    // read without a type check
    if (list.empty()) {
        self->renderer->disabledV1.clear();                        // renderer+0x178
        self->renderer->disabledV2.clear();                        // renderer+0x1a0
        return;
    }
    for (std::string &entry : Split(list, ",")) {                  // 0x1e6b024
        std::vector<std::string> p = Split(entry, "-");
        if (p[0].size() != 2) continue;
        if (p[0] == "V1") self->renderer->disabledV1.insert(atoi(p[1]));   // 0x1e6d44c, 0x13889c0
        else if (p[0] == "V2") self->renderer->disabledV2.insert(atoi(p[1]));
    }
}
```

<small>Handler: `0x1372068` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e6b024`, `0x1e6d44c`, `0x13889c0`.</small>

<!-- args: string -->
