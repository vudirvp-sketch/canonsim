## 36. AI AGENT = PRIVILEGED RUNTIME

AI coding agent не считать «текстовым помощником». Современные agentic coding tools могут читать проект, запускать команды, устанавливать пакеты, редактировать файлы, работать с сетью и изменять build/CI/deployment поверхности. Поэтому capability model относится к агенту так же, как к любому privileged runtime.

### 36.1 Agent Capability Model

```text
agent identity
→ task scope
→ tool capability
→ resource scope
→ operation scope
→ data classification
→ approval gate
→ audit trail
→ revocation
```

По умолчанию:

```text
least privilege
read-only where possible
sandboxed runtime
restricted filesystem
restricted network egress
ephemeral credentials
bounded CPU/memory/processes
tool allowlist
explicit high-impact approval
```

Практика OWASP для agentic coding включает sandboxing, tool allowlists, egress controls, ephemeral credentials и защиту чувствительных файлов/секретов.

### 36.2 Untrusted context

Repository text, issue bodies, PR descriptions, comments, logs, fetched pages и tool descriptions могут быть **instruction-bearing input**, а не trusted policy. Поэтому:

```text
DATA ≠ INSTRUCTION
OBSERVATION ≠ AUTHORITY
TOOL DESCRIPTION ≠ POLICY
REPOSITORY FILE ≠ TRUSTED AGENT RULE
```

### 36.3 High-impact surfaces

Повышенный gate для AI-изменений:

```text
CI/CD
build scripts
package scripts
Dockerfiles
deployment config
permissions/auth
secrets
schema migrations
lockfiles/dependency resolution
agent rules / tool configuration
```

**Правило:**

> Агенту запрещено одновременно быть генератором, единственным verifier'ом и владельцем irreversible action.

---


## 36.4 Context sufficiency

Context window/retrieval budget — security/reliability resource. Для material action проверить:

```text
required context
∩ effective context
```

Если отсутствует critical invariant, authority boundary, risk, forbidden action или verification plan:

```text
BLOCK | RETRIEVE | ESCALATE
```

Context truncation не является permission to guess.

## 36.5 Tool/provider supply-chain

Любой внешний tool server считать `untrusted-by-default` до проверки:

```text
identity + version + provenance + capability manifest + network/data scope + audit + revocation
```

`tool description ≠ policy`; declaration ≠ grant.

## 36.6 Agent claim provenance

Material claim:

```text
claim → epistemic type → source → transformation → verifier → observation boundary → expiry
```

Failure taxonomy: `fabrication | stale-belief | overgeneralization | unsupported-attribution`.

Generated rationale не является evidence причины поведения.
