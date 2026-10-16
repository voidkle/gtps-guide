# 5 ERROR

<Badge type="info" text="message type" /> <Badge type="info" text="server → client" />

Error text. The client passes it to a signal nothing listens to. Not used by gurotopia or GrowServer.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Text from the server, like type 3, but not parsed as `key|value`. The client wraps it in a variant list
`{ uint 0, string text }` and fires a signal of the network client (netclient+0x20) with it. No listener of
that signal was found in 5.60, so the message probably has no visible effect.

```c
case 5: {
    VariantList v(Variant(0u), Variant(std::string(TextOf(msg))));   // 0x1142d58
    net->signal_20(v);                                                // 0x108d11c
}
```

<small>Case 5 of the dispatcher `0x114276c`.</small>

## Layout

```text
[u32 5][...]
```
