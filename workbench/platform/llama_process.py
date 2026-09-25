"""The llama-server process mechanics (wb-8, the app spec §11.1's
MANAGED half + §2's "process mechanics | platform/process" row).

The law this module closes: **the operator's «llama.cpp тоже
запускаться при загрузке модели» call** — the workbench may OWN the
llama-server process (MANAGED), not merely observe it (wb-6's
ATTACHED form). Per §11.1 the ownership splits exactly two ways:

```text
application/runtime (the composition root, scripts/workbench_app.py)
        owns LIFECYCLE POLICY — when to spawn, what to load, when to
        stop, the replacement decision (prepare new → validate →
        ready → swap → retire old)
THIS module (platform/process)
        owns OS MECHANICS — spawn, the command line, handle/stdio
        ownership, exit observation, the bounded graceful stop
        (TERM → wait → kill), the readiness wait driven by an
        injected probe
```

The seam discipline (INV-4's spirit, §4.1): this module holds NO
network imports and NO HTTP — readiness is observed by calling a
PROBE the composition root injects (the engine adapter's own
`health()`, cli/engine.py — the one sanctioned outbound surface).
`workbench/` stays engine-agnostic otherwise: nothing here knows the
wire protocol, the model semantics, or the gateway.

The default flag set (the owner's «настройки подтягиваться и самые
нужные флаги» call — the RTX 3080 Ti + 32 GB RAM station's honest
defaults, re-verified 2026-09-25 against the current llama.cpp
server surface):

```text
-m <model path>     the file to load (the discovered GGUF)
--host 127.0.0.1    loopback only (the exposure law, app §4)
--port <port>       the backend port (the composition root's own)
-a <alias>          the model alias (= the logical_name — /props and
                    the API surface name the model by it)
-ngl 999            all layers on the GPU (the 12 GB VRAM station's
                    Q4_K_M-class budget; overridable per launch)
-c 8192             the context window (a chat-honest default;
                    overridable)
-fa on              flash attention (the current builds' on/off/auto
                    form; the CUDA default, pinned explicitly)
--jinja             the model's own chat template (the Gemma-class
                    requirement — without it the server's generic
                    template mangles the turns)
--no-webui          no browser UI on the loopback port (the Redot
                    shell is the only intended client)
```

The sampler default flags (wb-9, the owner's «сэмплеры всякие» call —
the app spec §19's 2026-09-23 research surface's stable core, each
emitted EXPLICITLY, never assumed from the build's own defaults —
the same pinning law `-fa on` uses):

```text
--temp 0.8          the temperature (the chat surface's own default
                    rides every request that omits one — §19.1)
--top-k 40          top-k truncation
--top-p 0.95        nucleus truncation
--min-p 0.05        the min-p floor (the current builds' default)
--repeat-penalty 1.1  the repetition penalty
```

Build-sensitive like every llama.cpp surface (app §20's law): the
defaults are the CONSERVATIVE admitted set; `extra_args` carries the
operator's own flags verbatim (the honest override — later rows
promote validated knobs into typed config as they earn consumers).
"""

from __future__ import annotations

import subprocess
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "DEFAULT_CONTEXT",
    "DEFAULT_FLASH_ATTENTION",
    "DEFAULT_GPU_LAYERS",
    "DEFAULT_HOST",
    "DEFAULT_MIN_P",
    "DEFAULT_REPEAT_PENALTY",
    "DEFAULT_TEMPERATURE",
    "DEFAULT_TOP_K",
    "DEFAULT_TOP_P",
    "LlamaProcessError",
    "LlamaServerProcess",
    "SEMANTIC_FLAG_TABLE",
    "build_server_command",
    "build_semantic_command",
    "semantic_flag_tokens",
]

#: The default GPU layer count — all layers (the single-GPU station's
#: Q4_K_M-class budget; a CPU-fallback station overrides it).
DEFAULT_GPU_LAYERS = 999

#: The default context window — a chat-honest mid size (KV budget on
#: the 12 GB station stays comfortable beside a Q4_K_M body).
DEFAULT_CONTEXT = 8192

#: The default flash-attention form — the current builds' explicit
#: "on" (the CUDA default made explicit, never an assumed "auto").
DEFAULT_FLASH_ATTENTION = "on"

#: The sampler default family (wb-9 — §19's stable core, the current
#: llama.cpp server builds' own defaults pinned explicitly; the
#: settings store's UI surface rides these as its defaults).
DEFAULT_TEMPERATURE = 0.8
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.95
DEFAULT_MIN_P = 0.05
DEFAULT_REPEAT_PENALTY = 1.1

#: The managed server's bind host — loopback only (app §4's exposure
#: law: MANAGED is still never an implicit LAN surface).
DEFAULT_HOST = "127.0.0.1"

# inf-1 — the typed surface's own runtime-form vocabularies (the
# reviewed --help snapshot's literal values; the application's
# semantic overlay carries its own copy and the claim packet pins the
# two EQUAL — the settings.py precedent: each layer validates its own
# boundary, an import edge would couple the layers for a tuple).
KV_CACHE_TYPES = (
    "f32",
    "f16",
    "bf16",
    "q8_0",
    "q4_0",
    "q4_1",
    "iq4_nl",
    "q5_0",
    "q5_1",
)

_STOP_POLL_S = 0.05


# --------------------------------------------- inf-2: the semantic flag table


@dataclass(frozen=True)
class SemanticFlag:
    """One profile field's FLAG LAW (the inf-2 compile seam): the
    application's `compile_semantic` hands over field-keyed VALUES;
    THIS table owns the flag syntax — the form, the emission kind,
    the off-form, and the guard's reserved token aliases. The
    application owns the MEANING (ranges, relations, defaults);
    the platform owns the SYNTAX (app §2's seam law, verbatim).

    The emission kinds:

    ```text
    int / float     [flag, value] (floats via repr — the --temp law)
    enum            [flag, value]; `not_emitted` skips the flag
    text            [flag, value]; the empty string skips the flag
    bool_pair       on -> [flag]; off -> [off_flag] (both explicit)
    bool_flag       on -> [flag]; off -> NOTHING (no off-flag exists)
    samplers        [flag, ";".join(members)] (the ordered chain)
    gpu             -ngl's own 'auto' | 'all' | int literal forms
    chat_template   MODEL DEFAULT -> --jinja; GENERIC -> --no-jinja;
                    CUSTOM -> --jinja --chat-template <text>
    template_text   the custom template text (only with CUSTOM mode)
    ```

    Every form below is the reviewed --help snapshot's own literal
    (pinned 2026-09-25); the maintenance protocol (the LAW §19)
    re-diffs this table against the installed binary at every
    upgrade — an unknown field refuses LOUD, never a silent skip."""

    field: str
    flag: str
    kind: str
    off_flag: str = ""
    not_emitted: object = None
    forms: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()  # the guard's reserved tokens


def _table() -> tuple[SemanticFlag, ...]:
    """The field → flag table in CANONICAL EMISSION ORDER (the
    compiled command's own deterministic sequence — model, device,
    memory, loading, MoE, CPU, sampling, chat, structured, server,
    observability, speculative, rope, special, LoRA)."""
    return (
        # ------------------------------------------------- model / runtime
        SemanticFlag("context", "-c", "int", aliases=("--ctx-size",)),
        SemanticFlag("n_predict", "-n", "int", aliases=("--predict", "--n-predict")),
        SemanticFlag("keep", "--keep", "int"),
        SemanticFlag("threads", "-t", "int", aliases=("--threads",)),
        SemanticFlag("threads_batch", "-tb", "int", aliases=("--threads-batch",)),
        SemanticFlag("batch_size", "-b", "int", aliases=("--batch-size",)),
        SemanticFlag("ubatch_size", "-ub", "int", aliases=("--ubatch-size",)),
        # ------------------------------------------------------ device / GPU
        SemanticFlag(
            "gpu_layers", "-ngl", "gpu",
            aliases=("--gpu-layers", "--n-gpu-layers"),
        ),
        SemanticFlag(
            "flash_attention", "-fa", "enum",
            forms=("auto", "on", "off"), aliases=("--flash-attn",),
        ),
        SemanticFlag("fit", "--fit", "enum", forms=("on", "off")),
        SemanticFlag("main_gpu", "-mg", "int", aliases=("--main-gpu",)),
        SemanticFlag("tensor_split", "-ts", "text", aliases=("--tensor-split",)),
        SemanticFlag(
            "split_mode", "-sm", "enum",
            forms=("none", "layer", "row", "tensor"),
            aliases=("--split-mode",),
        ),
        # ------------------------------------------------------ memory / KV
        SemanticFlag(
            "cache_type_k", "--cache-type-k", "enum", forms=KV_CACHE_TYPES,
            aliases=("-ctk",),
        ),
        SemanticFlag(
            "cache_type_v", "--cache-type-v", "enum", forms=KV_CACHE_TYPES,
            aliases=("-ctv",),
        ),
        SemanticFlag(
            "kv_offload", "--kv-offload", "bool_pair",
            off_flag="--no-kv-offload", aliases=("-kvo", "-nkvo"),
        ),
        SemanticFlag(
            "kv_unified", "--kv-unified", "bool_pair",
            off_flag="--no-kv-unified", aliases=("-kvu", "-no-kvu"),
        ),
        SemanticFlag("cache_ram", "--cache-ram", "int", aliases=("-cram",)),
        SemanticFlag("cache_reuse", "--cache-reuse", "int"),
        SemanticFlag("swa_full", "--swa-full", "bool_flag"),
        # ---------------------------------------------------------- loading
        SemanticFlag(
            "load_mode", "--load-mode", "enum",
            forms=("auto", "none", "mmap", "mlock", "mmap+mlock", "dio"),
            aliases=("-lm",),
        ),
        SemanticFlag("warmup", "--warmup", "bool_pair", off_flag="--no-warmup"),
        SemanticFlag("check_tensors", "--check-tensors", "bool_flag"),
        SemanticFlag(
            "repack", "--repack", "bool_pair", off_flag="--no-repack",
            aliases=("-nr",),
        ),
        # --------------------------------------------------------------- MoE
        SemanticFlag("cpu_moe", "--cpu-moe", "bool_flag", aliases=("-cmoe",)),
        SemanticFlag(
            "n_cpu_moe", "--n-cpu-moe", "int", aliases=("-ncmoe",),
        ),
        SemanticFlag(
            "n_cpu_ffn", "--n-cpu-ffn", "int", aliases=("-ncffn",),
        ),
        SemanticFlag(
            "override_tensor", "--override-tensor", "text", aliases=("-ot",),
        ),
        # ---------------------------------------------------------- CPU / NUMA
        SemanticFlag(
            "numa", "--numa", "enum", not_emitted="off",
            forms=("off", "distribute", "isolate", "numactl"),
        ),
        # ------------------------------------------------------------ sampling
        SemanticFlag("temperature", "--temp", "float", aliases=("--temperature",)),
        SemanticFlag("top_k", "--top-k", "int"),
        SemanticFlag("top_p", "--top-p", "float"),
        SemanticFlag("min_p", "--min-p", "float"),
        SemanticFlag("typical", "--typical", "float", aliases=("--typical-p",)),
        SemanticFlag("top_n_sigma", "--top-nsigma", "float", aliases=("--top-n-sigma",)),
        SemanticFlag("repeat_penalty", "--repeat-penalty", "float"),
        SemanticFlag("repeat_last_n", "--repeat-last-n", "int"),
        SemanticFlag("presence_penalty", "--presence-penalty", "float"),
        SemanticFlag("frequency_penalty", "--frequency-penalty", "float"),
        SemanticFlag("dry_multiplier", "--dry-multiplier", "float"),
        SemanticFlag("dry_base", "--dry-base", "float"),
        SemanticFlag("dry_allowed_length", "--dry-allowed-length", "int"),
        SemanticFlag("dry_penalty_last_n", "--dry-penalty-last-n", "int"),
        SemanticFlag(
            "dry_sequence_breaker", "--dry-sequence-breaker", "text"
        ),
        SemanticFlag("xtc_probability", "--xtc-probability", "float"),
        SemanticFlag("xtc_threshold", "--xtc-threshold", "float"),
        SemanticFlag("mirostat", "--mirostat", "int"),
        SemanticFlag("mirostat_lr", "--mirostat-lr", "float"),
        SemanticFlag("mirostat_ent", "--mirostat-ent", "float"),
        SemanticFlag("dynatemp_range", "--dynatemp-range", "float"),
        SemanticFlag("dynatemp_exp", "--dynatemp-exp", "float"),
        SemanticFlag("adaptive_target", "--adaptive-target", "float"),
        SemanticFlag("adaptive_decay", "--adaptive-decay", "float"),
        SemanticFlag("ignore_eos", "--ignore-eos", "bool_flag"),
        SemanticFlag("logit_bias", "--logit-bias", "text", aliases=("-l",)),
        SemanticFlag("seed", "-s", "int", aliases=("--seed",)),
        SemanticFlag("samplers", "--samplers", "samplers"),
        # --------------------------------------------- chat / template / reasoning
        SemanticFlag(
            "chat_template", "--jinja", "chat_template",
            forms=("model_default", "generic", "custom"),
        ),
        SemanticFlag(
            "chat_template_custom", "--chat-template", "template_text"
        ),
        SemanticFlag(
            "reasoning", "-rea", "enum",
            forms=("auto", "on", "off"), aliases=("--reasoning",),
        ),
        SemanticFlag(
            "reasoning_format", "--reasoning-format", "enum",
            forms=("auto", "none", "deepseek", "deepseek-legacy"),
        ),
        SemanticFlag(
            "reasoning_effort", "--reasoning-effort", "enum",
            forms=("default", "minimal", "low", "medium", "high", "xhigh", "max"),
        ),
        SemanticFlag("reasoning_budget", "--reasoning-budget", "int"),
        SemanticFlag(
            "prefill_assistant", "--prefill-assistant", "bool_pair",
            off_flag="--no-prefill-assistant",
        ),
        # --------------------------------------------------- structured output
        SemanticFlag("grammar", "--grammar", "text"),
        SemanticFlag(
            "json_schema", "--json-schema", "text",
            aliases=("-j", "--json-schema-file", "-jf"),
        ),
        # ------------------------------------------------ server / concurrency
        SemanticFlag("parallel", "-np", "int", aliases=("--parallel",)),
        SemanticFlag(
            "cont_batching", "-cb", "bool_pair",
            off_flag="--no-cont-batching", aliases=("--cont-batching", "-nocb"),
        ),
        SemanticFlag(
            "context_shift", "--context-shift", "bool_pair",
            off_flag="--no-context-shift",
        ),
        SemanticFlag(
            "cache_prompt", "--cache-prompt", "bool_pair",
            off_flag="--no-cache-prompt",
        ),
        # ----------------------------------------------------- observability
        SemanticFlag("metrics", "--metrics", "bool_flag"),
        SemanticFlag(
            "log_jsonl", "--log-jsonl", "bool_pair", off_flag="--no-log-jsonl"
        ),
        SemanticFlag("perf", "--perf", "bool_pair", off_flag="--no-perf"),
        # -------------------------------------------------- speculative decoding
        SemanticFlag(
            "spec_type", "--spec-type", "enum", not_emitted="none",
            forms=(
                "none", "draft-simple", "draft-eagle3", "draft-mtp",
                "draft-dflash", "draft-dspark", "ngram-simple",
                "ngram-map-k", "ngram-map-k4v", "ngram-mod", "ngram-cache",
            ),
        ),
        SemanticFlag(
            "spec_draft_model", "--spec-draft-model", "text",
            aliases=("-md", "--model-draft"),
        ),
        # ------------------------------------------------------ RoPE / YaRN
        SemanticFlag(
            "rope_scaling", "--rope-scaling", "enum", not_emitted="model",
            forms=("model", "none", "linear", "yarn"),
        ),
        SemanticFlag("rope_freq_base", "--rope-freq-base", "float"),
        SemanticFlag("rope_freq_scale", "--rope-freq-scale", "float"),
        SemanticFlag("yarn_orig_ctx", "--yarn-orig-ctx", "int"),
        SemanticFlag("yarn_ext_factor", "--yarn-ext-factor", "float"),
        SemanticFlag("yarn_attn_factor", "--yarn-attn-factor", "float"),
        SemanticFlag("yarn_beta_fast", "--yarn-beta-fast", "float"),
        SemanticFlag("yarn_beta_slow", "--yarn-beta-slow", "float"),
        # ------------------------------------------------------ special modes
        SemanticFlag("embedding", "--embedding", "bool_flag", aliases=("--embeddings",)),
        SemanticFlag("mmproj", "--mmproj", "text", aliases=("-mm",)),
        # --------------------------------------------------------------- LoRA
        SemanticFlag("lora", "--lora", "text"),
    )


#: The field → flag table (canonical emission order).
SEMANTIC_FLAG_TABLE: tuple[SemanticFlag, ...] = _table()

_TABLE_INDEX: dict[str, SemanticFlag] = {
    row.field: row for row in SEMANTIC_FLAG_TABLE
}


def semantic_flag_tokens() -> frozenset[str]:
    """Every flag token the semantic layer OWNS (the primary flag,
    the off-form and every documented alias): the raw extra_args
    hatch's duplicate-ownership guard consumes this set — a hatch
    token that collides with ANY owned flag refuses LOUD at the
    compile step (the law's §13), never an ambiguous precedence."""
    tokens: set[str] = set()
    for row in SEMANTIC_FLAG_TABLE:
        tokens.add(row.flag)
        if row.off_flag:
            tokens.add(row.off_flag)
        tokens.update(row.aliases)
    return frozenset(tokens)

#: The per-pipe drain ring (bytes kept for the honest failure note):
#: enough for llama-server's verbose startup + the last requests' —
#: stderr lines, bounded everywhere (§26's spirit at the process row).
_PIPE_TAIL_BYTES = 64 * 1024


class _PipeDrain:
    """One captured pipe's reader thread (wb-11 — the Windows pipe
    wedge + the honest tail): a spawned llama-server writes its logs
    into PIPEs nobody drained — the OS pipe buffer (~4KB-class on
    Windows) fills, the server BLOCKS mid-write, never answers /health,
    and the readiness walk burns its whole budget (the observed
    «транспорт результ 13» chain's trigger). One daemon thread per
    pipe reads continuously into a bounded tail ring: the pipe never
    fills, and the tail is readable cross-platform (the old
    `os.set_blocking` dance raised on Windows pipes — the failure
    note's cause showed '(empty)')."""

    def __init__(self, stream, name: str) -> None:
        self._stream = stream
        self._name = name
        self._lock = threading.Lock()
        self._buffer = bytearray()

    def start(self) -> None:
        thread = threading.Thread(
            target=self._drain,
            name=f"canonsim-llama-{self._name}",
            daemon=True,
        )
        thread.start()

    def _drain(self) -> None:
        try:
            while True:
                # read1: whatever arrived, never a wait-for-the-whole-n
                # (a live process's last line lands in the ring now,
                # not at EOF).
                chunk = self._stream.read1(4096)
                if not chunk:
                    break  # EOF — the process closed its end
                with self._lock:
                    self._buffer.extend(chunk)
                    excess = len(self._buffer) - _PIPE_TAIL_BYTES
                    if excess > 0:
                        del self._buffer[:excess]
        except (OSError, ValueError):
            return  # the pipe died under us — the ring keeps its tail

    def tail_text(self, limit: int) -> str:
        """The drained tail as text (the honest failure note's cause —
        works on every platform: it reads OUR ring, never the pipe
        fd; a live process's recent output is already in the ring)."""
        with self._lock:
            text = bytes(self._buffer).decode("utf-8", errors="replace")
        text = text.strip()
        return text[-limit:] if text else ""


class LlamaProcessError(RuntimeError):
    """A process-mechanics contract violation (LOUD — a spawn on a
    missing executable, a stop of nothing; never a silent no-op)."""


def _positive_int(value: object, name: str, *, maximum: int) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 0 <= value <= maximum
    ):
        raise LlamaProcessError(
            f"{name} {value!r} must be an int in [0, {maximum}]"
        )
    return value


def _unit_float(value: object, name: str, *, maximum: float) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0.0 <= float(value) <= maximum
    ):
        raise LlamaProcessError(
            f"{name} {value!r} must be a number in [0, {maximum}]"
        )
    return float(value)


def build_server_command(
    exe: str | Path | Sequence[str],
    model_path: str | Path,
    *,
    host: str = DEFAULT_HOST,
    port: int,
    alias: str | None = None,
    context: int = DEFAULT_CONTEXT,
    gpu_layers: int | str = DEFAULT_GPU_LAYERS,
    flash_attention: str = DEFAULT_FLASH_ATTENTION,
    jinja: bool = True,
    no_webui: bool = True,
    temperature: float = DEFAULT_TEMPERATURE,
    top_k: int = DEFAULT_TOP_K,
    top_p: float = DEFAULT_TOP_P,
    min_p: float = DEFAULT_MIN_P,
    repeat_penalty: float = DEFAULT_REPEAT_PENALTY,
    samplers: Sequence[str] | None = None,
    seed: int | None = None,
    fit: str | None = None,
    cache_type_k: str | None = None,
    cache_type_v: str | None = None,
    extra_args: Sequence[str] = (),
) -> list[str]:
    """The honest default command line (§22: the launcher selects
    runtime paths; the flags stay the platform's typed surface). The
    alias rides `-a` so the served model's API identity IS the
    workbench logical_name (§9: one name, one identity). The sampler
    defaults ride their five flags EXPLICITLY (wb-9 — the §19 research
    surface's stable core, never assumed from the build's defaults).

    `exe` is the command LEAD: one token (the executable path — the
    launcher's CLI form) or a short prefix (an interpreter + script —
    the contract tests' stand-in form; never a shell string)."""
    lead: list[str]
    if isinstance(exe, (str, Path)):
        lead = [str(exe)]
    else:
        lead = [str(part) for part in exe]
        if not lead or not lead[0].strip():
            raise LlamaProcessError(
                "the command lead is empty — the executable path is required"
            )
    if not str(model_path).strip():
        raise LlamaProcessError("the model path is empty")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise LlamaProcessError(f"port {port!r} must be an int in [1, 65535]")
    if not isinstance(context, int) or context <= 0:
        raise LlamaProcessError(f"context {context!r} must be a positive int")
    if isinstance(gpu_layers, str):
        # inf-1 — the runtime's own literal forms ('auto'/'all', the
        # reviewed --help's own words): AUTO is a real form, never
        # 'unset' (the law's §10).
        if gpu_layers not in ("auto", "all"):
            raise LlamaProcessError(
                f"gpu_layers {gpu_layers!r} must be 'auto' | 'all' or a "
                "non-negative int"
            )
    elif not isinstance(gpu_layers, int) or isinstance(gpu_layers, bool) or gpu_layers < 0:
        raise LlamaProcessError(
            f"gpu_layers {gpu_layers!r} must be 'auto' | 'all' or a "
            "non-negative int"
        )
    if flash_attention not in ("on", "off", "auto"):
        raise LlamaProcessError(
            f"flash_attention {flash_attention!r} must be one of "
            "['auto', 'off', 'on']"
        )
    temperature = _unit_float(temperature, "temperature", maximum=2.0)
    top_k = _positive_int(top_k, "top_k", maximum=10_000)
    top_p = _unit_float(top_p, "top_p", maximum=1.0)
    min_p = _unit_float(min_p, "min_p", maximum=1.0)
    repeat_penalty = _unit_float(repeat_penalty, "repeat_penalty", maximum=4.0)
    # inf-1 — the semantic layer's compiled surface (each form the
    # reviewed --help's own literal: ';' separators, the KV enum, the
    # fit on/off pair, the -1 random sentinel). None = NOT EMITTED
    # (the legacy caller's command stays byte-stable).
    if samplers is not None:
        if (
            not isinstance(samplers, Sequence)
            or isinstance(samplers, (str, bytes))
            or not samplers
            or any(not isinstance(item, str) or not item for item in samplers)
        ):
            raise LlamaProcessError(
                "samplers must be a non-empty sequence of sampler ids "
                "(the ordered enabled chain)"
            )
    if seed is not None and (
        isinstance(seed, bool) or not isinstance(seed, int) or seed < -1
    ):
        raise LlamaProcessError(
            f"seed {seed!r} must be an int >= -1 (-1 = the random form)"
        )
    if fit is not None and fit not in ("on", "off"):
        raise LlamaProcessError(f"fit {fit!r} must be 'on' or 'off'")
    for name, value in (
        ("cache_type_k", cache_type_k),
        ("cache_type_v", cache_type_v),
    ):
        if value is not None and value not in KV_CACHE_TYPES:
            raise LlamaProcessError(
                f"{name} {value!r} must be one of {list(KV_CACHE_TYPES)}"
            )
    command: list[str] = [
        *lead,
        "-m", str(model_path),
        "--host", str(host),
        "--port", str(port),
        "-ngl", str(gpu_layers),
        "-c", str(context),
        "-fa", str(flash_attention),
        "--temp", repr(temperature),
        "--top-k", str(top_k),
        "--top-p", repr(top_p),
        "--min-p", repr(min_p),
        "--repeat-penalty", repr(repeat_penalty),
    ]
    if fit is not None:
        command += ["--fit", str(fit)]
    if samplers is not None:
        command += ["--samplers", ";".join(samplers)]
    if seed is not None:
        command += ["--seed", str(seed)]
    if cache_type_k is not None:
        command += ["--cache-type-k", str(cache_type_k)]
    if cache_type_v is not None:
        command += ["--cache-type-v", str(cache_type_v)]
    if alias is not None and alias.strip():
        command += ["-a", alias.strip()]
    if jinja:
        command.append("--jinja")
    if no_webui:
        command.append("--no-webui")
    command += [str(arg) for arg in extra_args]
    return command


def _semantic_number(value: object, row: SemanticFlag) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LlamaProcessError(
            f"{row.field} {value!r} must be an int/float for {row.flag}"
        )
    return float(value)


def build_semantic_command(
    exe: str | Path | Sequence[str],
    model_path: str | Path,
    *,
    host: str = DEFAULT_HOST,
    port: int,
    alias: str | None = None,
    no_webui: bool = True,
    semantic: Mapping[str, object],
    extra_args: Sequence[str] = (),
) -> list[str]:
    """The inference-compiled command (inf-2 — the law's §13 compile
    seam): the application's `compile_semantic` document (field-keyed
    values) translated onto the actual flag surface. THIS function
    owns the FLAG SYNTAX ONLY (app §2's seam law): every emission
    form is the table's own — the application owns the meaning
    (ranges, relations, defaults; validated at the store boundary).

    Validation law: an UNKNOWN field refuses LOUD (never a silent
    skip — the honest failure mode); the per-kind TYPE checks and
    the closed ENUM sets are the platform's own boundary (the
    settings.py precedent — each layer validates its own boundary,
    the claim packet pins the vocabularies EQUAL). A CUSTOM chat
    template with an empty custom text refuses LOUD (a half-config
    never reaches the runtime).

    `exe` is the command LEAD (one token or an interpreter prefix —
    the same law as `build_server_command`)."""
    lead: list[str]
    if isinstance(exe, (str, Path)):
        lead = [str(exe)]
    else:
        lead = [str(part) for part in exe]
        if not lead or not lead[0].strip():
            raise LlamaProcessError(
                "the command lead is empty — the executable path is required"
            )
    if not str(model_path).strip():
        raise LlamaProcessError("the model path is empty")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise LlamaProcessError(f"port {port!r} must be an int in [1, 65535]")
    if not isinstance(semantic, Mapping):
        raise LlamaProcessError(
            "the semantic document must be a mapping (field -> value)"
        )
    unknown = sorted(set(semantic) - set(_TABLE_INDEX))
    if unknown:
        raise LlamaProcessError(
            f"the semantic document carries unknown field(s) {unknown} — "
            "the platform's flag table is the closed compile surface "
            "(the application's compile_semantic owns the field set)"
        )
    command: list[str] = [*lead, "-m", str(model_path), "--host", str(host), "--port", str(port)]
    for row in SEMANTIC_FLAG_TABLE:
        if row.field not in semantic:
            continue  # an absent field emits nothing (the closed doc's own choice)
        value = semantic[row.field]
        kind = row.kind
        if kind == "int":
            if isinstance(value, bool) or not isinstance(value, int):
                raise LlamaProcessError(
                    f"{row.field} {value!r} must be an int for {row.flag}"
                )
            command += [row.flag, str(value)]
        elif kind == "float":
            number = _semantic_number(value, row)
            command += [row.flag, repr(number)]
        elif kind == "enum":
            if value not in row.forms:
                raise LlamaProcessError(
                    f"{row.field} {value!r} must be one of {list(row.forms)}"
                )
            if value != row.not_emitted:
                command += [row.flag, str(value)]
        elif kind == "text":
            if not isinstance(value, str):
                raise LlamaProcessError(
                    f"{row.field} {value!r} must be a str for {row.flag}"
                )
            if value != "":
                command += [row.flag, value]
        elif kind == "bool_pair":
            if not isinstance(value, bool):
                raise LlamaProcessError(
                    f"{row.field} {value!r} must be a bool for {row.flag}"
                )
            command += [row.flag if value else row.off_flag]
        elif kind == "bool_flag":
            if not isinstance(value, bool):
                raise LlamaProcessError(
                    f"{row.field} {value!r} must be a bool for {row.flag}"
                )
            if value:
                command += [row.flag]
        elif kind == "samplers":
            if (
                not isinstance(value, Sequence)
                or isinstance(value, (str, bytes))
                or not value
                or any(
                    not isinstance(item, str) or not item for item in value
                )
            ):
                raise LlamaProcessError(
                    "samplers must be a non-empty sequence of sampler ids "
                    "(the ordered enabled chain)"
                )
            command += [row.flag, ";".join(value)]
        elif kind == "gpu":
            if isinstance(value, str):
                if value not in ("auto", "all"):
                    raise LlamaProcessError(
                        f"gpu_layers {value!r} must be 'auto' | 'all' or a "
                        "non-negative int"
                    )
            elif (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value < 0
            ):
                raise LlamaProcessError(
                    f"gpu_layers {value!r} must be 'auto' | 'all' or a "
                    "non-negative int"
                )
            command += [row.flag, str(value)]
        elif kind == "chat_template":
            if value not in ("model_default", "generic", "custom"):
                raise LlamaProcessError(
                    f"chat_template {value!r} must be one of "
                    "['model_default', 'generic', 'custom']"
                )
            if value == "model_default":
                command += ["--jinja"]
            elif value == "generic":
                command += ["--no-jinja"]
            else:
                custom = semantic.get("chat_template_custom", "")
                if not isinstance(custom, str) or not custom.strip():
                    raise LlamaProcessError(
                        "chat_template 'custom' requires a non-empty "
                        "chat_template_custom text — a half-config never "
                        "reaches the runtime"
                    )
                command += ["--jinja"]
        elif kind == "template_text":
            # emitted by the chat_template row's own logic? No — the
            # TEXT rides this row, but only in CUSTOM mode.
            mode = semantic.get("chat_template", "model_default")
            if mode == "custom":
                if not isinstance(value, str) or not value.strip():
                    raise LlamaProcessError(
                        "chat_template_custom must be a non-empty str when "
                        "chat_template is 'custom'"
                    )
                command += [row.flag, value]
    if alias is not None and alias.strip():
        command += ["-a", alias.strip()]
    if no_webui:
        command.append("--no-webui")
    command += [str(arg) for arg in extra_args]
    return command


class LlamaServerProcess:
    """One managed llama-server's OS mechanics: spawn (stdout/stderr
    captured for the honest failure note), exit observation, and the
    §11.1 bounded graceful stop — TERM, the grace deadline, then
    kill; the ACTUAL outcome is reported, never assumed.

    The process object holds no policy: it does not decide when to
    start or what to load, and it never probes the network (the
    composition root injects the readiness probe — the engine
    adapter's health(), keeping INV-4's single outbound surface).
    """

    def __init__(
        self, command: Sequence[str], *, cwd: Path | None = None
    ) -> None:
        if not command or not str(command[0]).strip():
            raise LlamaProcessError(
                "the command must lead with the executable path"
            )
        self._command = [str(part) for part in command]
        self._cwd = cwd
        self._process: subprocess.Popen[bytes] | None = None
        self._stdout_drain: _PipeDrain | None = None
        self._stderr_drain: _PipeDrain | None = None

    @property
    def command(self) -> list[str]:
        """The exact command line (the honest evidence line — the
        launcher prints it; the flags are never a hidden default)."""
        return list(self._command)

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self) -> None:
        """Spawn (§11.1 STARTING): a loud error on a missing/failed
        executable — the captured stderr tail rides the message, the
        honest cause, never 'it did not work'."""
        if self._process is not None:
            raise LlamaProcessError(
                "the process is already spawned (one process per object — "
                "the replacement path constructs a fresh one, §11.1)"
            )
        try:
            self._process = subprocess.Popen(
                self._command,
                cwd=str(self._cwd) if self._cwd is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise LlamaProcessError(
                f"cannot spawn {self._command[0]!r}: {exc} — pass "
                "--llama-server-exe with the actual path (the owner's "
                "station: D:\\llama.cpp\\llama-server.exe)"
            ) from exc
        # wb-11: the drains — one daemon reader per captured pipe (the
        # Windows pipe-buffer wedge pinned dead; the tail ring feeds
        # stderr_tail on every platform).
        assert self._process.stdout is not None
        assert self._process.stderr is not None
        self._stdout_drain = _PipeDrain(self._process.stdout, "stdout")
        self._stderr_drain = _PipeDrain(self._process.stderr, "stderr")
        self._stdout_drain.start()
        self._stderr_drain.start()

    def wait_ready(
        self,
        probe: Callable[[], bool],
        *,
        timeout_s: float,
        poll_s: float = 0.25,
    ) -> bool:
        """§11.1 PROBING → READY: poll the injected probe until it
        answers True or the deadline passes. A dead process fails the
        wait immediately (the exit code is the honest evidence); a
        timeout returns False — the caller decides the failure's
        vocabulary, this side never fabricates readiness."""
        deadline = time.monotonic() + timeout_s
        while True:
            if not self.running:
                return False
            if probe():
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(poll_s)

    def stop(self, *, grace_s: float = 10.0) -> int | None:
        """§11.1's bounded graceful stop: TERM → the grace deadline →
        kill; the returned value is the OBSERVED exit code (None when
        the process was never spawned or already reaped by the OS —
        the truth, never a guessed 0)."""
        process = self._process
        if process is None:
            return None
        if process.poll() is not None:
            return process.returncode
        process.terminate()
        try:
            return process.wait(timeout=max(0.0, grace_s))
        except subprocess.TimeoutExpired:
            process.kill()
            return process.wait()

    def exit_code(self) -> int | None:
        """The observed exit code (None while running — §11.1's exit
        observation half; never a blocking wait)."""
        process = self._process
        if process is None:
            return None
        return process.returncode

    def stderr_tail(self, limit: int = 400) -> str:
        """The captured stderr tail for the honest failure note (the
        spawn/ready failure's observed cause — bounded, never the
        whole log). wb-11: the answer comes from the drain ring (the
        reader thread's bounded buffer) — cross-platform, current
        while the process lives, complete once it dies."""
        drain = self._stderr_drain
        if drain is None:
            return ""
        return drain.tail_text(limit)
