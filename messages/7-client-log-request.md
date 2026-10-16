# 7 CLIENT_LOG_REQUEST

<Badge type="info" text="message type" /> <Badge type="info" text="server → client" />

The client only logs the name. Not used by either server.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The client only logs the text "NET_MESSAGE_CLIENT_LOG_REQUEST" and does nothing else. It doesn't answer with
type 8.

<small>Case 7 of the dispatcher `0x114276c`.</small>

## Layout

```text
[u32 7][...]
```
