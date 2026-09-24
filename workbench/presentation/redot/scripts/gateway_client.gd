# CanonSim Workbench — the gateway client (wb-7, the live chat
# circuit's frontend half).
#
# What this script is: the ONE typed HTTP client the Redot shell uses
# to reach the Workbench gateway (wb-4's loopback binding, POST /op —
# the app spec §8's single dispatch entry). It is presentation-layer
# plumbing ONLY: it serializes request envelopes, delivers them, parses
# the response document, and reports. It holds NO canonical state, NO
# chat semantics, NO backend knowledge — the shell owns the surface
# logic; the gateway owns the operation semantics (frontend §47's G8:
# the frontend cannot bypass the application boundary — this client
# dials the GATEWAY, never llama.cpp).
#
# Version admission (the reference index §8): the API surface used —
# HTTPRequest.request(url, headers, method, data), the `timeout`
# property, the request_completed(result, code, headers, body) signal,
# JSON.stringify/parse_string — verified against redot-26.2-stable
# (scene/main/http_request.h/.cpp, 2026-09-24).
#
# Delivery model (§13's bounded minimal form): a SEQUENTIAL queue over
# one HTTPRequest node — one request in flight at a time, later calls
# wait their turn. The shell's operations are short dispatches
# (chat.send returns the execution identity immediately; run.get is a
# read), so a queue is honest and bounded. A request that cannot be
# delivered reports transport_failed and the queue moves on — the
# caller decides what that means (the honest "gateway unreachable"
# note, never a silent drop).
#
# Per-call timeout (wb-8): a caller may name its own budget on the
# ONE request that legitimately outruns the dispatch default —
# model.load, whose managed spawn + weight load is minutes-class
# (§11.1's STARTING→PROBING→READY walk). The property write rides
# the Redot 26.2 `timeout` member (verified with the rest of the
# surface); the DEFAULT_TIMEOUT_S stays the queue's honest floor.
extends Node

signal operation_answered(tag: String, document: Dictionary)
signal transport_failed(tag: String, error: String)

const DEFAULT_TIMEOUT_S := 10.0

var _base_url := ""
var _http: HTTPRequest
var _queue: Array[Dictionary] = []
var _in_flight: Dictionary = {}


func _ready() -> void:
        _http = HTTPRequest.new()
        _http.timeout = DEFAULT_TIMEOUT_S
        _http.request_completed.connect(_on_request_completed)
        add_child(_http)


func configure(base_url: String) -> void:
        # The gateway root (no endpoint lives in this file — the shell
        # configures it; POST /op rides it).
        _base_url = base_url.rstrip("/")


func busy() -> bool:
        return not _in_flight.is_empty() or not _queue.is_empty()


func call_operation(
        tag: String,
        operation: String,
        arguments: Dictionary,
        session_id: String = "",
        client_request_id: String = "",
        timeout_s: float = DEFAULT_TIMEOUT_S,
) -> void:
        # One dispatch envelope (§8): operation + arguments; the session id
        # on session-scoped calls; the idempotency key on mutations (G4 —
        # REQUIRED server-side; the shell passes a stable per-action key);
        # the caller's own timeout budget when the call legitimately
        # outruns the dispatch default (model.load's managed spawn).
        var document := {"operation": operation, "arguments": arguments}
        if session_id != "":
                document["session_id"] = session_id
        if client_request_id != "":
                document["client_request_id"] = client_request_id
        _queue.append({
                "tag": tag,
                "body": JSON.stringify(document),
                "timeout_s": timeout_s,
        })
        _pump()


func _pump() -> void:
        if _in_flight.is_empty() and not _queue.is_empty():
                var next: Dictionary = _queue.pop_front()
                _http.timeout = float(next.get("timeout_s", DEFAULT_TIMEOUT_S))
                var err := _http.request(
                        _base_url + "/op",
                        PackedStringArray(["Content-Type: application/json"]),
                        HTTPClient.METHOD_POST,
                        String(next["body"]),
                )
                if err != OK:
                        transport_failed.emit(String(next["tag"]), "request_refused_%d" % err)
                        _pump()  # the queue moves on (bounded, never wedged)
                else:
                        _in_flight = next


func _on_request_completed(
        result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray
) -> void:
        if _in_flight.is_empty():
                return  # a late completion with nothing in flight (defensive)
        var tag := String(_in_flight["tag"])
        _in_flight = {}
        if result != HTTPRequest.RESULT_SUCCESS:
                transport_failed.emit(tag, "transport_result_%d" % result)
        elif response_code != 200:
                # Transport-level failures answer 4xx JSON errors (wb-4's wire
                # contract); ANY non-200 is a transport failure at this layer —
                # semantic rejections ride HTTP 200 documents.
                var note := "http_%d" % response_code
                var text := body.get_string_from_utf8()
                var parsed = JSON.parse_string(text)
                if parsed is Dictionary and parsed.has("error"):
                        note = "http_%d_%s" % [response_code, str(parsed["error"])]
                transport_failed.emit(tag, note)
        else:
                var parsed = JSON.parse_string(body.get_string_from_utf8())
                if parsed is Dictionary:
                        operation_answered.emit(tag, parsed)
                else:
                        transport_failed.emit(tag, "response_not_json")
        _pump()
