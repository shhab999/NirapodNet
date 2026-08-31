# NirapodNet — Phase 1 Test Log

**Date:** 2026-08-31
**Phase:** Phase 1
**Environment:** Windows + Python virtual environment

## Test 1 — User Idempotency

**Test:** POST the same username twice.

**Expected:**

* The first request creates the user.
* The second request returns the existing user.
* No duplicate username is created.

**Result:** TODO

**Notes:**

## Test 2 — Message History

**Test:** Create multiple messages and call `GET /messages`.

**Expected:**

* Messages are returned oldest-first.
* Each message contains:

  * `id`
  * `client_id`
  * `sender_id`
  * `sender`
  * `content`
  * `timestamp`

**Result:** TODO

**Notes:**

## Test 3 — WebSocket Round Trip

**Test:** Connect two clients using `/ws/{user_id}`. Send a message from Client A.

**Expected:**

* Client A receives an ACK.
* Client B receives the message.
* Client A is excluded from the broadcast.
* The message is not duplicated.

**Result:** TODO

**Notes:**

## Test 4 — LAN Test

**Test:** Run the server with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open NirapodNet from another device on the same LAN.

**Expected:**

* The page loads.
* WebSocket connects.
* Messages can be exchanged.

**Result:** TODO

**Notes:**

## Test 5 — Internet Disconnected

**Test:** Disconnect Internet access while keeping the local LAN available.

**Expected:**

* NirapodNet continues to load.
* Local messaging continues to work.

**Result:** TODO

**Notes:**

## Phase 1 Final Status

**Status:** NOT COMPLETE

Phase 1 is complete only after the required tests are executed and the observed results are recorded here.
