# Task 1 Modernization Ledger

## Scope Freeze
- Repo root: `E:\wzry_ai_v1.0_20260409`
- Canonical active code root after migration: `src/wzry_ai/`
- Canonical operator entrypoint after cutover: `scripts/master_auto.py`
- Only default root shim retained during migration: `Master_Auto.py`
- Canonical resource roots after migration:
  - `assets/templates/`
  - `assets/heroes/`
  - `models/`
  - `data/`
  - `docs/`
- Repo-specific resource assumption frozen for later tasks: `hero_skills/` maps to `assets/templates/hero_skills/`

## Canonical Layout Freeze
```text
src/wzry_ai/
├── app/
├── battle/
├── compat/
│   └── legacy/
├── config/
├── detection/
├── device/
├── game_manager/
├── movement/
├── skills/
└── utils/

scripts/
assets/
├── templates/
│   └── hero_skills/
└── heroes/
models/
data/
docs/
```

## Old → New Mapping

### Runtime and Code Boundaries
| Current path | Frozen target | Boundary type | Notes |
|---|---|---|---|
| `Master_Auto.py` | `Master_Auto.py` shim + `scripts/master_auto.py` + `src/wzry_ai/app/` | entrypoint | Current composition root. Root file becomes delegation-only after packaged app bootstrap exists. |
| `config/` | `src/wzry_ai/config/` | active package | `config/__init__.py` remains the stable compatibility surface, but under `wzry_ai.config`. |
| `device/` | `src/wzry_ai/device/` | active package | Move low-level emulator/ADB/scrcpy transport before higher-level domains. |
| `utils/` | `src/wzry_ai/utils/` | active package | Shared helpers move early so downstream imports can converge on package paths. |
| `detection/` | `src/wzry_ai/detection/` | active package | Model adapters and modal fusion move after config/device/utils. |
| `game_manager/` | `src/wzry_ai/game_manager/` | active package | UI state machine and template orchestration move after resource resolver exists. |
| `skills/` | `src/wzry_ai/skills/` | active package | Active skill system moves after detection/game-manager imports stabilize. |
| `battle/` | `src/wzry_ai/battle/` | active package | Registry and combat logic move with packaged import updates for dynamic imports. |
| `movement/` | `src/wzry_ai/movement/` | active package | Movement depends on battle outputs and detector/game state inputs, so it moves in the final domain wave. |

### Resource and Non-Code Boundaries
| Current path | Frozen target | Boundary type | Notes |
|---|---|---|---|
| `image/` | `assets/templates/` | resource | Current UI/template images normalize here. `game_manager/template_matcher.py` currently defaults to `image/`. |
| `hero_skills/` | `assets/templates/hero_skills/` | resource | Frozen repo-specific mapping used by hero-selection skill-icon verification. |
| `hero/` | `assets/heroes/` | resource | Current portrait assets normalize here. `game_manager/hero_selector.py` currently defaults to `hero/`. |
| `models/` | `models/` | top-level resource boundary | Stays top-level; access will be via shared resolver instead of direct root assumptions. |
| `data/` | `data/` | top-level resource boundary | Stays top-level; access will be via shared resolver instead of direct root assumptions. |
| `AGENTS.md` | `docs/project-knowledge/AGENTS.md` | documentation | Repo knowledge-base content belongs under docs once docs consolidation starts. |
| `使用文档.txt` | `docs/operator/使用文档.txt` | documentation | Operator-facing usage doc belongs under docs boundary. |

### New Boundaries Introduced by the Plan
| New path | Role |
|---|---|
| `src/wzry_ai/` | Only canonical active Python namespace after cutover. |
| `src/wzry_ai/app/` | Composition root and runtime bootstrap location. |
| `src/wzry_ai/compat/legacy/` | Bounded home for deprecated code required during transition. |
| `scripts/` | Thin operator entrypoints only. |
| `assets/templates/` | Canonical template and UI image root. |
| `assets/heroes/` | Canonical hero portrait root. |
| `docs/` | Canonical architecture/operator document boundary. |

## Migration Order Freeze
1. `config` + `device` + `utils`
2. `detection` + `game_manager`
3. `skills` + `battle` + `movement`
4. `app` assembly finalization and `scripts/master_auto.py` activation
5. `Master_Auto.py` reduced to root shim only

## Import and Resource Rules
- After cutover, active code uses only `wzry_ai.*` absolute imports.
- `config/__init__.py` remains the public compatibility surface inside `wzry_ai.config`.
- Resource/model/data/doc lookups go through one resolver owned by `wzry_ai.app` or `wzry_ai.utils`.
- No active domain may depend on current working directory assumptions.
- Dynamic import strings in `battle/hero_registry.py` must be updated to packaged module paths during the `skills` + `battle` wave.

## Shim and Legacy Rules
- Default root shim set: `Master_Auto.py` only.
- No extra long-lived root package shims for `battle`, `config`, `detection`, `device`, `game_manager`, `movement`, `skills`, or `utils`.
- Deprecated `skills/hero_skill_manager.py` moves under `src/wzry_ai/compat/legacy/` when the skill package relocation occurs.
- `skills/__init__.py` export compatibility is preserved inside the package namespace until legacy manager retirement is complete.

## Cutover Rules
- `scripts/master_auto.py` becomes the canonical operator entrypoint before any root shim reduction is declared complete.
- `Master_Auto.py` stops owning business orchestration once `wzry_ai.app` can assemble runtime services.
- A domain is considered cut over only when its active imports resolve from `src/wzry_ai/` and its resource access uses the shared resolver.
- Root directories stop being canonical immediately after their packaged equivalents are active.
- `compat/legacy/` remains transitional only for explicitly approved deprecated code, not for parallel active implementations.

## Repo-Specific Evidence Basis
- `Master_Auto.py` is the current composition root and wires emulator, detection, game-manager, battle, movement, and skills services.
- `config/__init__.py` is the current stable compatibility surface.
- `config/base.py` and `config/emulator.py` compute root-relative paths for `models/` and `data/` today.
- `game_manager/template_matcher.py` currently assumes `image/` as the default template root.
- `game_manager/hero_selector.py` currently assumes `hero/` and `hero_skills/` as default asset roots.
- `battle/hero_registry.py` currently uses dynamic import strings rooted at `skills.*` and `battle.*`.
- `skills/hero_skill_manager.py` is deprecated but still exported from `skills/__init__.py`, so legacy isolation is required during package migration.
