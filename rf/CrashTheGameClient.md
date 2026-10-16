Crashes the client on purpose: it calls `raise()` with the signal number from argument 1, or 11 (SIGSEGV)
when the argument is missing or not positive. Nothing else happens; there's no check of who sent it.

| # | Type | Meaning |
|---|---|---|
| 1 | int | signal number to raise; ≤ 0 or missing = 11 (SIGSEGV) |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

### Decompiled handler

```c
void GameLogic::CrashTheGameClient(GameLogic *self, VariantList *vl) {
    int sig = 11;
    if (vl[1].i > 0) sig = vl[1].i;
    raise(sig);
}
```

<small>Handler: `0x1372740` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
