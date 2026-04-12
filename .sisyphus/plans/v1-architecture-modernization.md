# v1.0 Architecture Modernization Plan

## TL;DR
> **Summary**: Preserve v1.0's stronger domain architecture (`battle`, `movement`, `game_manager`, `detection`) while restoring v0.5's engineering discipline through a single package namespace, thin entrypoints, explicit resource boundaries, and isolated legacy code.
> **Deliverables**:
> - Canonical code package under `src/wzry_ai/`
> - Thin bootstrap entrypoints replacing heavy root orchestration
> - Unified resource/path resolver for assets/models/data
> - Explicit `compat/legacy/` boundary for old systems
> - Characterization + smoke validation harness for safe migration
> **Effort**: XL
> **Parallel**: YES - 4 waves
> **Critical Path**: 1 → 2 → 3 → 4/5/6 → 7/8 → 9

## Context
### Original Request
- Analyze v1.0 weaknesses versus v0.5 and give an update plan.
- Then refine it into the ideal architecture for future development.

### Interview Summary
- User prefers **safe migration** over a pure high-risk rewrite.
- User prefers **isolate legacy first, then retire it**, not long-term dual active systems.
- The final architecture should optimize for future hero additions, detection evolution, and ongoing maintainability.

### Metis Review (gaps addressed)
- Do not mix structural migration with battle-logic rewrites, ROI retuning, or hero behavior changes.
- Validation must combine static/import/path checks with emulator-backed smoke tests when available.
- The plan must define ownership boundaries for legacy code and a removal trigger, otherwise temporary coexistence becomes permanent debt.
- Entrypoint slimming must extract a composition root before moving package locations, otherwise boot logic becomes fragile.

## Work Objectives
### Core Objective
- Move `E:\wzry_ai_v1.0_20260409` to a future-proof architecture that keeps v1.0's domain split but standardizes code packaging, resource boundaries, entrypoints, and compatibility policy.

### Deliverables
- New canonical directory layout:
  - `src/wzry_ai/app/`
  - `src/wzry_ai/config/`
  - `src/wzry_ai/game_manager/`
  - `src/wzry_ai/battle/`
  - `src/wzry_ai/movement/`
  - `src/wzry_ai/detection/`
  - `src/wzry_ai/device/`
  - `src/wzry_ai/skills/`
  - `src/wzry_ai/utils/`
  - `src/wzry_ai/compat/legacy/`
  - `scripts/`
  - `assets/templates/`
  - `assets/heroes/`
  - `models/`
  - `data/`
  - `docs/`
- Thin runtime entrypoints:
  - `scripts/master_auto.py`
  - root `Master_Auto.py` kept only as temporary compatibility shim during migration
- Single resource resolver for templates, hero assets, model weights, and runtime data
- Explicit legacy isolation strategy for `skills/hero_skill_manager.py` and any residual旧路径
- Validation harness for imports, package loading, path resolution, and emulator smoke flows

### Definition of Done (verifiable conditions with commands)
- All active Python code loads from `src/wzry_ai/`; root business packages are no longer the canonical implementation path.
- Root `Master_Auto.py` contains only compatibility bootstrap logic and delegates to packaged `main()`.
- Runtime resources are resolved through a single path layer; code does not assume current working directory.
- Legacy code lives only under `src/wzry_ai/compat/legacy/` and has documented removal criteria.
- Static verification succeeds:
  - `python -m compileall src`
  - `$env:PYTHONPATH='src'; python -c "import importlib; mods=['wzry_ai','wzry_ai.app','wzry_ai.config','wzry_ai.game_manager','wzry_ai.battle','wzry_ai.movement','wzry_ai.detection','wzry_ai.device','wzry_ai.skills','wzry_ai.utils','wzry_ai.compat.legacy']; [importlib.import_module(m) for m in mods]"`
  - `$env:PYTHONPATH='src'; python scripts/master_auto.py --help`
- Emulator smoke verification succeeds when hardware/runtime is available:
  - startup boot
  - frame acquisition
  - state detection enters lobby/menu path
  - hero-selection flow loads without import/path failures

### Must Have
- Single canonical package namespace: `src/wzry_ai/`
- Preserve v1.0 domain boundaries: `battle`, `movement`, `game_manager`, `detection`, `device`, `skills`, `utils`, `config`
- Keep `config` as the stable import surface, but inside the canonical package
- Introduce `app/` as the composition root and runtime bootstrap location
- Introduce `compat/legacy/` for old systems with an explicit removal window
- Unify assets under `assets/templates/` and `assets/heroes/`
- Keep `models/` and `data/` as explicit top-level non-code boundaries

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Do not rewrite battle heuristics, threat thresholds, hero behavior, or ROI constants as part of the migration
- Do not leave multiple active canonical import paths after cutover
- Do not solve package migration with long-term `sys.path` hacks
- Do not keep root directories as active business packages after `src/wzry_ai/` is introduced
- Do not leave legacy and active implementations mixed inside the same package boundary
- Do not move assets casually without first centralizing resource resolution

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: **tests-after**. A project-level automated test suite is now established and green (pytest: 138 passed, 1 skipped); use characterization checks, import smoke, path smoke, and emulator-backed smoke scenarios.
- QA policy: Every task includes agent-executed scenarios.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`
- Default applied: emulator-backed smoke is required in final validation when runtime is available; static checks remain mandatory regardless.

## Target End-State Architecture
### Canonical Repository Shape
```text
./
├── src/
│   └── wzry_ai/
│       ├── app/                 # composition root, startup policy, service wiring
│       ├── config/              # canonical runtime config surface
│       ├── game_manager/        # UI state machine, template matching, click orchestration
│       ├── battle/              # world state, threat analysis, battle FSM, hero decisions
│       ├── movement/            # follow, minimap, stuck recovery, path execution
│       ├── detection/           # model inference, modal fusion, detector adapters
│       ├── device/              # emulator discovery, ADB, scrcpy transport
│       ├── skills/              # active skill system and hero-specific v2 logic
│       ├── utils/               # cross-domain shared utilities only
│       └── compat/
│           └── legacy/          # isolated deprecated code paths with explicit sunset policy
├── scripts/                     # canonical operator entrypoints
├── assets/
│   ├── templates/               # former image/ templates and UI assets
│   └── heroes/                  # former hero/ portrait assets
├── models/                      # YOLO weights and related model artifacts
├── data/                        # runtime data, maps, emulator config, class names
└── docs/                        # operator docs, migration docs, architecture docs
```

### Architectural Principles
- **Single code root**: all active Python code lives under `src/wzry_ai/`.
- **Domain-preserving migration**: v1.0's domain split is retained, not flattened.
- **Thin entrypoints**: `scripts/` and temporary root shims only delegate into `wzry_ai.app`.
- **Central path policy**: assets/models/data/docs are resolved through one path layer.
- **Explicit compatibility**: anything transitional is named `compat`, anything deprecated is named `legacy`.
- **One active path rule**: each runtime capability has exactly one canonical implementation path.

### Domain Ownership Boundaries
- `app/`
  - Owns startup sequence, dependency assembly, service lifecycle, top-level runtime modes.
  - Must not contain battle heuristics, UI detection rules, or hero-specific behavior.
- `config/`
  - Owns stable import surface for runtime constants and structured config modules.
  - Must not accumulate business logic, path hacks, or runtime orchestration.
- `game_manager/`
  - Owns UI state detection, template state transitions, popup handling, click flow coordination.
  - Must not embed battle policy or emulator bootstrap logic.
- `battle/`
  - Owns semantic combat understanding: world model, threat evaluation, tactical state, decision makers.
  - Must not own raw transport, UI templates, or resource lookup policy.
- `movement/`
  - Owns path/follow/minimap movement execution and stuck recovery.
  - Must not own hero skill behavior or menu-state logic.
- `detection/`
  - Owns detector interfaces, inference scheduling, modal fusion, model adapters.
  - Must not own battle decisions or UI click flows.
- `device/`
  - Owns emulator discovery, ADB/scrcpy transport, low-level device/session connection.
  - Must not own high-level game-state or hero logic.
- `skills/`
  - Owns active skill abstractions, hero-specific v2 logic, registry-linked behavior execution.
  - Must not retain deprecated paths in the active surface.
- `utils/`
  - Owns only truly cross-domain utilities with low business meaning.
  - Must not become a dumping ground for uncategorized domain code.
- `compat/legacy/`
  - Owns deprecated code required for bounded transition only.
  - Must not be imported by new code except through approved shims.

### Allowed Dependency Rules
- `app` may depend on any active domain package.
- `config` may be imported by any active domain package.
- `game_manager` may depend on `config`, `utils`, `device`, and narrow `detection` interfaces.
- `battle` may depend on `config`, `utils`, `skills` interfaces, and normalized outputs from `detection`.
- `movement` may depend on `config`, `utils`, and `battle` outputs needed for movement decisions.
- `detection` may depend on `config`, `utils`, `device`, and model/data access helpers.
- `skills` may depend on `config`, `utils`, and battle-facing interfaces needed for skill execution.
- `device` may depend on `config` and `utils` only.
- `utils` should not depend on business domains.
- `compat/legacy` may depend inward on active code when necessary for delegation; active code must not depend outward on `compat/legacy` except documented shims.

### Forbidden Dependency Rules
- `battle` must not import `game_manager` state-machine internals.
- `device` must not import `battle`, `movement`, or `skills`.
- `config` must not import runtime domains.
- `utils` must not import `battle`, `movement`, `game_manager`, or `skills` business logic.
- No active domain may bypass the resource resolver with direct deprecated root-path assumptions.

### Extension Model for Future Development
- **Adding a new hero**:
  - Add hero metadata/config under `config/heroes/`.
  - Add hero skill logic under `skills/`.
  - Register active behavior through a registry (`battle/hero_registry.py` or its packaged equivalent).
  - Do not modify entrypoint or unrelated battle infrastructure.
- **Adding a new detector/model**:
  - Add detector adapter/scheduler/fusion integration under `detection/`.
  - Expose normalized outputs to `battle`/`game_manager`; do not leak model-specific details across domains.
- **Adding a new runtime mode**:
  - Wire mode selection in `app/`; keep feature behavior inside the owning domain package.
  - Do not expand `Master_Auto.py` or add new root scripts unless operator UX requires it.

### Composition Root Contract
- `wzry_ai.app` is the only place allowed to:
  - create top-level services
  - wire queues/threads/shared managers
  - choose runtime mode
  - assemble device + detection + state + battle + movement + skill subsystems
- All other packages expose reusable units; they do not self-bootstrap the application.

### Composition Root Lifecycle
- Boot order is canonicalized to:
  1. process/logging/runtime safeguards
  2. config load and resource resolver initialization
  3. emulator/device discovery
  4. frame transport and shared frame services
  5. detector construction and model loading
  6. UI state services and menu/runtime mode services
  7. battle, movement, and skills activation
  8. supervisor/health monitoring
  9. bounded shutdown in reverse dependency order
- No domain package may bypass this lifecycle by self-starting threads, self-loading models at random integration points, or self-owning global process startup.

### Inter-Domain Contract Types
- The packaged architecture must converge on stable cross-domain DTOs/interfaces for at least:
  - `FrameSnapshot` - frame payload + metadata for downstream consumers
  - `DetectorResult` - normalized detector output contract
  - `UIStateResult` - state detector output consumed outside `game_manager`
  - `WorldState` - semantic combat world model consumed by `battle` and `movement`
  - `SkillInput` - normalized skill-execution input from battle/runtime state
  - `RuntimeModeSpec` - runtime mode registration/config contract
- New cross-domain features must prefer extending these contracts over introducing new ad hoc dict payloads.
- Detector/model-specific raw payloads must be normalized inside `detection/` before leaving the package boundary.

### Hero Extension Contract
- Canonical runtime hero identity remains the existing Chinese runtime key used by selection/state systems.
- Pinyin aliases may exist only as mapping/config helpers; they must not replace the canonical runtime key at the registry boundary.
- A new active hero integration must define, at minimum:
  - hero config/metadata entry under `config/heroes/`
  - active skill logic under `skills/`
  - registry entry in the canonical hero registry boundary
  - decision-maker mapping or explicit fallback policy
- Optional hero-specific assets/state detectors may be added only through the owning package and resolver-backed asset declarations.
- Fallback behavior must be explicit:
  - missing skill logic -> approved generic skill fallback
  - missing decision logic -> approved generic decision fallback
  - missing config -> registration must fail fast rather than silently half-register

### Detector Extension Contract
- `detection/` owns the canonical detector plugin boundary.
- Every detector integration must declare:
  - stable detector id/key
  - initialization/loading phase
  - expected input source(s)
  - normalized output schema
  - error/failure isolation behavior
  - whether model loading is eager or lazy
- Detector implementations may differ internally, but external callers may consume only normalized `DetectorResult` contracts.
- New detectors must not leak model-specific result shapes into `battle/`, `game_manager/`, or `movement/`.

### Runtime Mode Extension Contract
- A runtime mode is treated as an application-composition profile, not a root-script fork.
- New runtime modes must declare:
  - activation conditions
  - required detectors/services
  - required UI flow/state handlers
  - supported heroes or hero constraints if relevant
  - mode-specific config surface
- Runtime modes are wired by `app/`; mode-specific UI logic may live in `game_manager/` only if it remains behind a declared mode contract.
- Adding a new mode must not require expanding root entrypoints or hardcoding unrelated mode behavior into generic startup flow.

### Public API vs Internal Module Policy
- Each package may expose a narrow stable surface via `__init__.py` or a dedicated public module.
- Direct imports into deep implementation modules are allowed only inside the owning package unless explicitly documented as public.
- `compat/legacy` symbols must not be re-exported from active package public surfaces.
- Public API promises should be minimal; internal module layout may evolve as long as package-level contracts remain stable.

## Governance and Migration Policy
### Migration Milestones
- **M1: Architecture Freeze**
  - Canonical tree, dependency rules, shim policy, and resource policy are frozen.
- **M2: Namespace Establishment**
  - `src/wzry_ai/` exists and package skeleton is valid.
- **M3: Path Stabilization**
  - Resource resolver is active and deprecated path assumptions are contained.
- **M4: Entrypoint Slimming**
  - `app/` composition root exists; root `Master_Auto.py` delegates only.
- **M5: Active Domain Relocation**
  - All active domain packages run from `src/wzry_ai/`.
- **M6: Compatibility Containment**
  - Temporary shims and `compat/legacy/` boundaries are explicit and documented.
- **M7: Canonical Cutover**
  - `src/wzry_ai/` is the sole active authority.
- **M8: Post-Cutover Verification**
  - Final review wave passes and residual legacy debt is scheduled for removal.

### Legacy Retirement Policy
- A legacy module may remain only if all conditions are true:
  - an active caller still depends on it indirectly through an approved shim
  - removal would break startup/runtime verification today
  - the module is listed in the legacy registry with owner, reason, and target removal milestone
- A legacy module must be removed when all conditions are true:
  - no approved shim requires it
  - active code no longer imports it
  - packaged runtime smoke passes without it
- Every legacy item must record:
  - original path
  - new canonical replacement
  - last allowed caller
  - removal trigger
  - target removal wave/commit

### Compatibility Shim Policy
- Approved shim categories only:
  - root entrypoint bootstrap shim
  - import-path compatibility shim
  - resource-location compatibility shim inside the central resolver
- Every shim must declare:
  - owner
  - allowed callers
  - delegated canonical target
  - removal trigger
- Shims must not:
  - hold business logic
  - become new extension points
  - survive beyond documented sunset criteria

### Verification Matrix
| Layer | What is Verified | Minimum Evidence |
|---|---|---|
| Structure | canonical package tree and resource boundaries | inventory report + path checks |
| Imports | `wzry_ai.*` canonical imports and no root authority | import smoke + regression scan |
| Entrypoints | packaged entry works and root shim delegates | startup logs |
| Resources | templates/heroes/models/data resolve canonically | resolver smoke evidence |
| Legacy | deprecated code isolated and not used by active paths | dependency scan |
| Scope | migration stayed structural | scope-fidelity audit |
| Runtime | startup and bounded emulator smoke | runtime smoke logs |

### Risk Register
- **Import-cycle exposure after packaging**
  - Mitigation: stabilize dependency rules before relocation; fail fast on package-import smoke.
- **Root-relative path breakage**
  - Mitigation: central resolver before any asset/data move.
- **Entrypoint regression**
  - Mitigation: extract `app` composition root before cutover.
- **Legacy becoming permanent**
  - Mitigation: mandatory registry + removal trigger for every legacy item.
- **Behavior drift during structural work**
  - Mitigation: scope-fidelity audit and no mixed structural/behavioral commits.

### Rollback Strategy
- **Rollback principle**: each migration task must leave the repo in a runnable or at least statically importable state.
- **Rollback units**:
  - Task 2 rollback: remove incomplete package skeleton additions only if they are unused.
  - Task 3 rollback: revert resolver adoption as one unit if canonical path coverage is incomplete.
  - Task 4 rollback: restore previous root bootstrap only if packaged `app` startup smoke fails.
  - Tasks 5-6 rollback: revert one migrated domain or shim batch at a time; do not partially revert imports without restoring the previous authoritative path.
  - Tasks 7-8 rollback: revert legacy or asset moves only together with their caller/path updates.
  - Task 9 rollback: if full cutover smoke fails, restore last known good dual-path transitional state rather than forcing partial canonicalization.
- **Rollback triggers**:
  - package import smoke fails for any active domain
  - packaged startup path fails while previous bootstrap path was green
  - resolver cannot resolve representative template/hero/model/data paths
  - duplicate-authority scan cannot be made green without breaking runtime startup

### Architecture Decision Log
- **ADR-001**: Canonical code root is `src/wzry_ai/`.
  - Reason: restores engineering discipline from v0.5 while keeping packaging explicit.
- **ADR-002**: Preserve v1.0's domain split instead of flattening into generic layers.
  - Reason: battle/movement/game_manager/detection decomposition is a real architectural gain and improves future feature growth.
- **ADR-003**: `Master_Auto.py` becomes a temporary compatibility launcher, not the composition root.
  - Reason: entrypoint obesity is a known structural weakness.
- **ADR-004**: All resource lookup flows through a single resolver.
  - Reason: path breakage is one of the highest migration risks.
- **ADR-005**: Deprecated systems must live under `compat/legacy/` with explicit sunset criteria.
  - Reason: implicit coexistence is how dual-track maintenance becomes permanent debt.

### Anti-Patterns to Eliminate
- Root-level active business packages remaining authoritative after `src/wzry_ai/` cutover.
- New code importing deprecated root paths or `compat/legacy/` directly.
- `utils/` absorbing domain behavior because the correct owner is unclear.
- Resource paths hardcoded in feature modules instead of going through the resolver.
- Entry logic expanding back into `Master_Auto.py` after `app/` is introduced.
- Compatibility shims accumulating business logic or becoming long-term extension points.
- Structural migration commits that also change battle heuristics, hero behavior, ROI constants, or model semantics.

### Package Stewardship Model
- `app/`: startup/runtime stewardship
- `config/`: configuration contract stewardship
- `game_manager/`: UI flow and state-machine stewardship
- `battle/`: combat semantics and decision stewardship
- `movement/`: locomotion/path execution stewardship
- `detection/`: detector/fusion stewardship
- `device/`: emulator transport stewardship
- `skills/`: active skill framework stewardship
- `compat/legacy/`: deprecation stewardship only; no new feature ownership allowed

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. <3 per wave (except final) = under-splitting.

Wave 1: 1 architecture freeze, 2 package skeleton + namespace contract, 3 resource/path contract

Wave 2: 4 extract composition root from `Master_Auto.py`, 5 migrate domain packages into `src/wzry_ai/`, 6 introduce compatibility shims

Wave 3: 7 isolate legacy systems, 8 consolidate assets/docs/scripts and update loaders

Wave 4: 9 cut over canonical imports and remove temporary root-package authority

### Dependency Matrix (full, all tasks)
- 1 blocks: 2, 3, 4, 5, 6, 7, 8, 9
- 2 blocks: 4, 5, 6, 7, 8, 9
- 3 blocks: 4, 5, 8, 9
- 4 blocks: 9
- 5 blocks: 7, 8, 9
- 6 blocks: 7, 8, 9
- 7 blocks: 9
- 8 blocks: 9
- 9 blocks: Final Verification Wave

### Agent Dispatch Summary (wave → task count → categories)
- Wave 1 → 3 tasks → `deep`, `quick`
- Wave 2 → 3 tasks → `deep`, `unspecified-high`
- Wave 3 → 2 tasks → `deep`, `unspecified-high`
- Wave 4 → 1 task → `deep`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [ ] 1. Freeze canonical target architecture and migration contracts

  **What to do**:
  - Produce a complete old→new mapping for all active code, assets, models, data, scripts, and docs.
  - Lock the canonical target layout to:
    - `src/wzry_ai/app/`
    - `src/wzry_ai/config/`
    - `src/wzry_ai/game_manager/`
    - `src/wzry_ai/battle/`
    - `src/wzry_ai/movement/`
    - `src/wzry_ai/detection/`
    - `src/wzry_ai/device/`
    - `src/wzry_ai/skills/`
    - `src/wzry_ai/utils/`
    - `src/wzry_ai/compat/legacy/`
    - `scripts/`, `assets/templates/`, `assets/heroes/`, `models/`, `data/`, `docs/`
  - Freeze import policy: only `wzry_ai.*` absolute imports inside active code after cutover.
  - Freeze resource policy: all path access must go through a single resolver module under `wzry_ai.app` or `wzry_ai.utils`.

  **Must NOT do**:
  - Do not move files yet.
  - Do not rewrite business logic.
  - Do not leave any target path as “to be decided later”.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: requires full-project mapping and zero-ambiguity migration contracts.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - this is architecture freezing, not implementation.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: [2,3,4,5,6,7,8,9] | Blocked By: []

  **References**:
  - Pattern: `Master_Auto.py` - current heavy root entrypoint to be reduced to compatibility bootstrap
  - Pattern: `config/__init__.py` - current stable import surface that must survive inside package namespace
  - Pattern: `battle/`, `movement/`, `game_manager/`, `detection/`, `device/`, `skills/`, `utils/` - preserve as domain boundaries
  - Pattern: `image/`, `hero/`, `models/`, `data/` - current resource boundaries to normalize
  - Pattern: `E:\wzry_ai_v0.5_20260408\src\wzry_ai\` - structural discipline reference to restore

  **Acceptance Criteria**:
  - [ ] A complete path mapping exists for every active code and resource path.
  - [ ] The canonical package layout and import/path policy are documented with no unresolved placeholders.
  - [ ] Legacy isolation target (`src/wzry_ai/compat/legacy/`) is explicitly declared.

  **QA Scenarios**:
  ```
  Scenario: Mapping completeness audit
    Tool: Bash
    Steps: Run a script that inventories all top-level active directories/files and verifies each appears in the migration map.
    Expected: No unmapped active path remains; evidence lists every mapped source path.
    Evidence: .sisyphus/evidence/task-1-architecture-map.json

  Scenario: Contract ambiguity failure check
    Tool: Bash
    Steps: Run a script that scans the frozen contract document for TODO/TBD/placeholder markers.
    Expected: Zero unresolved placeholders; otherwise task fails with exact lines.
    Evidence: .sisyphus/evidence/task-1-architecture-map-error.txt
  ```

  **Commit**: YES | Message: `chore(architecture): freeze v1 modernization target` | Files: planning/evidence artifacts only

- [ ] 2. Create canonical package skeleton and namespace boundary

  **What to do**:
  - Create `src/wzry_ai/` and all package subdirectories declared in Task 1.
  - Add required `__init__.py` files.
  - Create explicit namespace boundaries for `app`, `compat`, and active domains.
  - Ensure no second active top-level package name is introduced.

  **Must NOT do**:
  - Do not migrate business files in this task.
  - Do not add shim logic yet.
  - Do not create package aliases that imply multiple canonical roots.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: structure creation after decisions are frozen.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - no code rewriting needed yet.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [4,5,6,7,8,9] | Blocked By: [1]

  **References**:
  - Pattern: `E:\wzry_ai_v0.5_20260408\src\wzry_ai\__init__.py` - reference for disciplined package root
  - Pattern: `config/`, `game_manager/`, `battle/`, `movement/`, `detection/`, `device/`, `skills/`, `utils/` - active domain packages to mirror

  **Acceptance Criteria**:
  - [ ] `src/wzry_ai/` exists with all planned subpackages.
  - [ ] Every package directory that should be importable contains `__init__.py`.
  - [ ] A smoke script confirms the skeleton exists exactly as frozen in Task 1.

  **QA Scenarios**:
  ```
  Scenario: Skeleton existence check
    Tool: Bash
    Steps: Run a script that checks existence of all required `src/wzry_ai/*` package paths and expected top-level support directories.
    Expected: All required paths exist and are reported true.
    Evidence: .sisyphus/evidence/task-2-skeleton.json

  Scenario: Missing init failure check
    Tool: Bash
    Steps: Run a script that scans `src/wzry_ai` for importable package directories lacking `__init__.py`.
    Expected: No missing package init files; otherwise task fails with exact paths.
    Evidence: .sisyphus/evidence/task-2-skeleton-error.txt
  ```

  **Commit**: YES | Message: `chore(structure): add canonical wzry_ai package skeleton` | Files: `src/`, support directories

- [ ] 3. Centralize resource and path resolution before relocation

  **What to do**:
  - Create a single path resolver module for assets, hero portraits, model weights, and runtime data.
  - Replace direct path assumptions in active code with the resolver abstraction.
  - Freeze canonical resource destinations:
    - `assets/templates/`
    - `assets/heroes/`
    - `models/`
    - `data/`
    - `docs/`
  - Preserve temporary backward-compatible lookups during transition, but only inside the resolver.

  **Must NOT do**:
  - Do not move assets before the resolver exists.
  - Do not leave path logic duplicated across domains.
  - Do not rely on current working directory.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: path breakage is one of the highest migration risks.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - avoid broad rewrites outside path handling.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: [4,5,8,9] | Blocked By: [1]

  **References**:
  - Pattern: `config/base.py` - model/data path constants currently bound to root layout
  - Pattern: `image/`, `hero/`, `models/`, `data/` - current resource locations
  - Pattern: `E:\wzry_ai_v0.5_20260408\assets\images\` - stronger historical resource separation to emulate

  **Acceptance Criteria**:
  - [ ] There is one canonical resolver API for all runtime resource lookups.
  - [ ] No active module resolves root resource paths by hardcoded relative path after this task.
  - [ ] Resource smoke checks pass for templates, heroes, models, and data.

  **QA Scenarios**:
  ```
  Scenario: Resource resolver smoke
    Tool: Bash
    Steps: Run a Python script that imports the resolver and resolves a representative template path, hero asset path, model path, and data path.
    Expected: All returned paths exist and point to the intended canonical or transitional location.
    Evidence: .sisyphus/evidence/task-3-resource-resolver.json

  Scenario: Hardcoded path regression scan
    Tool: Bash
    Steps: Run a code scan for direct references to known root resource directories outside the resolver module.
    Expected: No disallowed hardcoded path references remain; otherwise exact files/lines are reported.
    Evidence: .sisyphus/evidence/task-3-resource-resolver-error.txt
  ```

  **Commit**: YES | Message: `refactor(paths): centralize runtime resource resolution` | Files: resolver + migrated callers

- [ ] 4. Extract composition root from `Master_Auto.py` and thin the entrypoint

  **What to do**:
  - Move runtime composition, service wiring, thread orchestration, and startup policy into `src/wzry_ai/app/`.
  - Introduce a packaged `main()`/bootstrap path.
  - Reduce root `Master_Auto.py` to a compatibility launcher that delegates to the packaged entry.
  - Add `scripts/master_auto.py` as the canonical script entrypoint.

  **Must NOT do**:
  - Do not keep business decisions in the root entrypoint.
  - Do not split code arbitrarily; extract only stable orchestration seams.
  - Do not remove root compatibility entry before cutover validation passes.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: entrypoint slimming must preserve runtime behavior while reducing coupling.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - avoid unrelated refactors while extracting the composition root.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [9] | Blocked By: [1,2,3]

  **References**:
  - Pattern: `Master_Auto.py` - current heavy runtime entrypoint
  - Pattern: `E:\wzry_ai_v0.5_20260408\scripts\master_auto.py` - disciplined script-entry reference
  - Pattern: `utils/frame_manager.py`, `device/`, `game_manager/state_detector.py` - likely collaborators currently wired from root

  **Acceptance Criteria**:
  - [ ] Root `Master_Auto.py` only bootstraps and delegates; no active orchestration remains there.
  - [ ] `scripts/master_auto.py` launches the packaged application path.
  - [ ] Startup smoke passes via both compatibility entry and canonical script entry.

  **QA Scenarios**:
  ```
  Scenario: Canonical entry smoke
    Tool: Bash
    Steps: Run `$env:PYTHONPATH='src'; python scripts/master_auto.py --help` and a dry-start command that initializes without entering gameplay.
    Expected: The packaged entry loads without import errors and logs the expected startup path.
    Evidence: .sisyphus/evidence/task-4-entrypoint-smoke.log

  Scenario: Root compatibility entry failure check
    Tool: Bash
    Steps: Run the root `Master_Auto.py` compatibility path under the same smoke conditions.
    Expected: It delegates successfully and does not duplicate orchestration behavior; failure logs exact stack trace if imports or bootstrap are wrong.
    Evidence: .sisyphus/evidence/task-4-entrypoint-error.log
  ```

  **Commit**: YES | Message: `refactor(app): extract composition root from master entry` | Files: `Master_Auto.py`, `scripts/`, `src/wzry_ai/app/`

- [ ] 5. Migrate active domain packages into `src/wzry_ai/`

  **What to do**:
  - Move active business domains into the canonical package while preserving domain names and internal boundaries:
    - `config`
    - `game_manager`
    - `battle`
    - `movement`
    - `detection`
    - `device`
    - `skills`
    - `utils`
  - Convert active imports to `wzry_ai.*` absolute imports.
  - Keep behavior unchanged.

  **Must NOT do**:
  - Do not rename domain concepts.
  - Do not rewrite logic while moving files.
  - Do not preserve root directories as second canonical implementations.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: large-scale package relocation with broad import updates.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - avoid opportunistic redesign during migration.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [7,8,9] | Blocked By: [1,2,3]

  **References**:
  - Pattern: `config/__init__.py` - preserve stable config surface semantics inside package namespace
  - Pattern: `battle/world_state.py`, `battle/threat_analyzer.py`, `battle/battle_fsm.py` - preserve v1.0 architectural gains
  - Pattern: `game_manager/state_detector.py`, `game_manager/template_matcher.py` - preserve UI domain boundaries
  - Pattern: `movement/unified_movement.py`, `device/`, `utils/frame_manager.py` - preserve runtime integration boundaries

  **Acceptance Criteria**:
  - [ ] All active domain modules import from `wzry_ai.*` only.
  - [ ] No root-level business package remains the authoritative implementation path.
  - [ ] Package import smoke passes for every migrated domain.

  **QA Scenarios**:
  ```
  Scenario: Package import smoke
    Tool: Bash
    Steps: Run `$env:PYTHONPATH='src'; python -c "import importlib; mods=['wzry_ai.config','wzry_ai.game_manager','wzry_ai.battle','wzry_ai.movement','wzry_ai.detection','wzry_ai.device','wzry_ai.skills','wzry_ai.utils']; [importlib.import_module(m) for m in mods]"`
    Expected: All modules import successfully without root-path hacks.
    Evidence: .sisyphus/evidence/task-5-package-imports.log

  Scenario: Root import regression check
    Tool: Bash
    Steps: Run a scan for active code importing bare root domain packages instead of `wzry_ai.*`.
    Expected: No disallowed active imports remain; otherwise output exact files.
    Evidence: .sisyphus/evidence/task-5-package-imports-error.txt
  ```

  **Commit**: YES | Message: `refactor(package): move active domains into wzry_ai namespace` | Files: active domain packages

- [ ] 6. Introduce temporary compatibility shims with explicit sunset rules

  **What to do**:
  - Add short-lived compatibility wrappers only where required to keep startup paths or transitional imports functional.
  - Document allowed shim locations and allowed callers.
  - Add removal criteria and deadline conditions to the compatibility layer.

  **Must NOT do**:
  - Do not treat compatibility wrappers as permanent architecture.
  - Do not create shims for convenience where callers can be updated directly.
  - Do not hide ownership of compatibility code.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: needs discipline to reduce migration risk without creating permanent debt.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - shim policy must stay narrow and intentional.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: [7,8,9] | Blocked By: [1,2]

  **References**:
  - Pattern: root `Master_Auto.py` compatibility path
  - Pattern: current root-level imports using `config` and sibling packages
  - Pattern: `E:\wzry_ai_v0.5_20260408\src\wzry_ai\config\runtime.py` - example of compatibility export surface

  **Acceptance Criteria**:
  - [ ] Every compatibility shim has an owner, purpose, and removal trigger.
  - [ ] No shim introduces a second permanent canonical path.
  - [ ] Compatibility smoke tests cover all declared shim entrypoints.

  **QA Scenarios**:
  ```
  Scenario: Shim coverage smoke
    Tool: Bash
    Steps: Run import and startup smoke for every declared shim entrypoint and compatibility wrapper.
    Expected: All shims delegate successfully to canonical packaged implementations.
    Evidence: .sisyphus/evidence/task-6-compat-shims.log

  Scenario: Undocumented shim failure check
    Tool: Bash
    Steps: Run a scan comparing shim files against the documented shim registry.
    Expected: Zero undocumented shims; otherwise fail with file list.
    Evidence: .sisyphus/evidence/task-6-compat-shims-error.txt
  ```

  **Commit**: YES | Message: `chore(compat): add temporary migration shims with sunset rules` | Files: shim files + shim registry/docs

- [ ] 7. Isolate legacy systems into `src/wzry_ai/compat/legacy/`

  **What to do**:
  - Move deprecated or superseded code paths into `compat/legacy/`.
  - Start with old skill-management flow centered on `skills/hero_skill_manager.py` and any directly related residual legacy helpers.
  - Keep only one active recommended path: `hero_skill_logic_base.py` + `*_skill_logic_v2.py` + registry-driven dispatch.
  - Document legacy removal conditions and caller restrictions.

  **Must NOT do**:
  - Do not leave legacy modules mixed into active domain paths without labels.
  - Do not delete legacy code before compatibility and smoke coverage exist.
  - Do not let new code depend on `compat/legacy/`.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: requires careful boundary definition and dependency control.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - avoid changing skill behavior while relocating legacy code.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [9] | Blocked By: [1,5,6]

  **References**:
  - Pattern: `skills/hero_skill_manager.py` - explicitly marked as old/legacy system
  - Pattern: `skills/hero_skill_logic_base.py` - active base path
  - Pattern: `skills/*_skill_logic_v2.py` - active hero-specific skill logic path
  - Pattern: `battle/hero_registry.py` - active registry-driven dispatch path

  **Acceptance Criteria**:
  - [ ] Deprecated systems are physically isolated under `wzry_ai.compat.legacy`.
  - [ ] Active code does not import from legacy paths except declared shims.
  - [ ] Legacy registry/removal policy is documented.

  **QA Scenarios**:
  ```
  Scenario: Active-vs-legacy dependency scan
    Tool: Bash
    Steps: Run a scan to detect imports from active code into `wzry_ai.compat.legacy` outside approved compatibility wrappers.
    Expected: Zero disallowed imports; otherwise fail with exact files.
    Evidence: .sisyphus/evidence/task-7-legacy-boundary.log

  Scenario: Legacy isolation smoke
    Tool: Bash
    Steps: Import the active skill path and the isolated legacy path separately to confirm both load and remain distinct.
    Expected: Active path remains default; legacy path loads only through compatibility boundary.
    Evidence: .sisyphus/evidence/task-7-legacy-boundary-error.txt
  ```

  **Commit**: YES | Message: `refactor(legacy): isolate deprecated skill system` | Files: legacy modules + policy docs

- [ ] 8. Consolidate assets, scripts, and docs into explicit non-code boundaries

  **What to do**:
  - Normalize templates into `assets/templates/`.
  - Normalize hero portraits into `assets/heroes/`.
  - Keep runtime data in `data/`, model weights in `models/`, and documentation in `docs/`.
  - Update loader/resolver references to canonical locations.
  - Keep temporary compatibility aliases only inside the resolver until final cutover.

  **Must NOT do**:
  - Do not scatter new assets back into code packages.
  - Do not retain both `image/` and `assets/templates/` as permanent canonical locations.
  - Do not hardcode old asset paths in active modules.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: large surface area, low algorithmic complexity, high path integrity risk.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - no logic redesign needed.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: [9] | Blocked By: [1,3,5,6]

  **References**:
  - Pattern: `image/`, `hero/`, `models/`, `data/`
  - Pattern: `E:\wzry_ai_v0.5_20260408\assets\images\` - desired engineering discipline reference
  - Pattern: resolver module from Task 3 - only allowed translation layer

  **Acceptance Criteria**:
  - [ ] Canonical non-code boundaries match the frozen architecture.
  - [ ] Resolver successfully resolves all representative assets from canonical locations.
  - [ ] Active code contains no hardcoded references to deprecated asset locations.

  **QA Scenarios**:
  ```
  Scenario: Canonical asset resolution smoke
    Tool: Bash
    Steps: Resolve representative template, hero portrait, model, and runtime data files via the canonical resolver after consolidation.
    Expected: All files resolve from canonical locations and exist.
    Evidence: .sisyphus/evidence/task-8-asset-boundary.json

  Scenario: Deprecated asset path regression scan
    Tool: Bash
    Steps: Scan active code for deprecated asset directory references like `image/` or `hero/` outside compatibility code.
    Expected: Zero active references remain; otherwise fail with exact files.
    Evidence: .sisyphus/evidence/task-8-asset-boundary-error.txt
  ```

  **Commit**: YES | Message: `chore(resources): normalize assets data and docs boundaries` | Files: assets/data/docs/scripts as applicable

- [ ] 9. Cut over canonical authority to `src/wzry_ai/` and retire transitional root-package authority

  **What to do**:
  - Make `src/wzry_ai/` the only authoritative implementation path.
  - Remove or demote root-level business package authority after all imports, resolver paths, and compatibility shims are verified.
  - Keep only the documented temporary compatibility surfaces that remain within the sunset window.
  - Update docs and operator commands to canonical packaged entrypoints.

  **Must NOT do**:
  - Do not retain duplicate active code trees.
  - Do not cut over before import, path, and startup smoke are green.
  - Do not leave undocumented residual root authority.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: final cutover is high leverage and highest regression risk.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/refactor']` - cutover only, no opportunistic improvements.

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: [Final Verification Wave] | Blocked By: [1,2,3,4,5,6,7,8]

  **References**:
  - Pattern: `src/wzry_ai/` package tree from Tasks 2 and 5
  - Pattern: `Master_Auto.py` compatibility shim from Task 4
  - Pattern: `compat/legacy/` and shim registry from Tasks 6 and 7
  - Pattern: canonical assets/models/data/docs boundaries from Task 8

  **Acceptance Criteria**:
  - [ ] `src/wzry_ai/` is the sole authoritative active code location.
  - [ ] Canonical startup path is documented and operational.
  - [ ] Transitional root authority is removed or explicitly limited to approved shims only.

  **QA Scenarios**:
  ```
  Scenario: Full package cutover smoke
    Tool: Bash
    Steps: Run compile/import/startup smoke through the canonical packaged entrypoint with `$env:PYTHONPATH='src'`.
    Expected: Startup succeeds without relying on old root package paths.
    Evidence: .sisyphus/evidence/task-9-cutover.log

  Scenario: Duplicate authority failure check
    Tool: Bash
    Steps: Run a scan for duplicate active modules existing both at root and under `src/wzry_ai/` after cutover.
    Expected: No duplicate active authority remains; otherwise fail with exact path pairs.
    Evidence: .sisyphus/evidence/task-9-cutover-error.txt
  ```

  **Commit**: YES | Message: `refactor(cutover): make wzry_ai package canonical` | Files: active package tree, startup paths, docs

## Final Verification Wave (MANDATORY — after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [ ] F1. Plan Compliance Audit — oracle

  **What to do**:
  - Compare implemented structure against every mandatory requirement in this plan.
  - Verify canonical code root, entrypoint strategy, legacy boundary, resource boundary, and compatibility policy were all implemented exactly as specified.
  - Produce a pass/fail checklist with one row per major requirement.

  **Must NOT do**:
  - Do not review only the latest commit; inspect the final workspace state.
  - Do not accept partial compliance.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: requires strict plan-to-result conformance review.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/review-work']` - final verification is already explicitly defined here.

  **Parallelization**: Can Parallel: YES | Final Wave | Blocks: [Completion] | Blocked By: [9]

  **Acceptance Criteria**:
  - [ ] Every must-have item is marked pass/fail with evidence.
  - [ ] Any deviation from planned architecture is explicitly listed.
  - [ ] Review output includes a final verdict: APPROVE / REJECT.

  **QA Scenarios**:
  ```
  Scenario: Plan compliance checklist audit
    Tool: Bash
    Steps: Run a verification script that checks canonical paths, package imports, compatibility shim registry, legacy directory location, and canonical asset/data/model/docs locations against the plan.
    Expected: All required checks pass and a structured checklist is written.
    Evidence: .sisyphus/evidence/f1-plan-compliance.md

  Scenario: Non-compliance detection
    Tool: Bash
    Steps: Run the same checklist with failure-on-mismatch enabled.
    Expected: Any missing canonical path, duplicate active root authority, or undocumented shim causes a non-zero result and a detailed failure report.
    Evidence: .sisyphus/evidence/f1-plan-compliance-error.txt
  ```

- [ ] F2. Code Quality Review — unspecified-high

  **What to do**:
  - Review the migrated code for structural cleanliness, import discipline, dead shim buildup, and packaging anti-patterns.
  - Check for accidental business-logic changes made during structural migration.
  - Verify no new AI-slop patterns were introduced (duplicate wrappers, vague helper layers, path hacks, dead abstractions).

  **Must NOT do**:
  - Do not restrict review to syntax/build success only.
  - Do not ignore maintainability regressions caused by migration scaffolding.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: hands-on structural/code quality inspection.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/review-work']` - this task has a narrower architecture-specific review scope.

  **Parallelization**: Can Parallel: YES | Final Wave | Blocks: [Completion] | Blocked By: [9]

  **Acceptance Criteria**:
  - [ ] No root-path hacks remain in active code.
  - [ ] No duplicate active module authorities remain.
  - [ ] No accidental behavior-changing edits are identified without documentation.

  **QA Scenarios**:
  ```
  Scenario: Structural quality scan
    Tool: Bash
    Steps: Run static scans for `sys.path` hacks, deprecated root imports, duplicate active module locations, and compatibility wrappers outside the approved shim registry.
    Expected: Zero disallowed findings; results are summarized in a review report.
    Evidence: .sisyphus/evidence/f2-code-quality.md

  Scenario: Migration anti-pattern detection
    Tool: Bash
    Steps: Run targeted scans for duplicate wrappers, dead compatibility layers, and direct resource-path handling outside the resolver.
    Expected: Any anti-pattern is reported with exact file paths and categorized as must-fix or advisory.
    Evidence: .sisyphus/evidence/f2-code-quality-error.txt
  ```

- [ ] F3. Agent-Executed Runtime QA — unspecified-high (+ emulator-backed smoke if available)

  **What to do**:
  - Execute runtime smoke validation through the canonical packaged entrypoint.
  - Validate import path, startup path, frame acquisition path, and state-detection startup path.
  - When emulator/runtime is available, run startup-to-menu smoke and hero-select-path smoke using agent-executed steps only.

  **Must NOT do**:
  - Do not require a human to click through or verify output manually.
  - Do not skip static startup smoke just because emulator-backed smoke is unavailable.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: requires hands-on execution and artifact capture.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/playwright']` - browser tooling is irrelevant; runtime validation is shell/emulator-based.

  **Parallelization**: Can Parallel: YES | Final Wave | Blocks: [Completion] | Blocked By: [9]

  **Acceptance Criteria**:
  - [ ] Canonical entrypoint startup smoke succeeds.
  - [ ] Import/path failures do not occur during startup sequence.
  - [ ] If emulator is available, runtime reaches menu/lobby detection path without structural regressions.

  **QA Scenarios**:
  ```
  Scenario: Canonical startup smoke
    Tool: Bash
    Steps: Run `$env:PYTHONPATH='src'; python scripts/master_auto.py --help` and a non-destructive startup smoke command that initializes packaged services without entering a full match loop.
    Expected: Startup completes without import/path errors and logs packaged bootstrap usage.
    Evidence: .sisyphus/evidence/f3-runtime-smoke.log

  Scenario: Emulator-backed flow smoke
    Tool: Bash
    Steps: If emulator/runtime is available, run a bounded smoke script that boots the app, confirms frame acquisition, and verifies state detection reaches menu/lobby or hero-select initialization without crashing.
    Expected: Smoke completes successfully and records runtime milestones; if unavailable, the script records SKIPPED-EMULATOR with reason while static startup smoke remains required.
    Evidence: .sisyphus/evidence/f3-runtime-smoke-emulator.log
  ```

- [ ] F4. Scope Fidelity Check — deep

  **What to do**:
  - Verify the migration stayed within scope: structural modernization only.
  - Check that battle logic, threat heuristics, ROI thresholds, hero behavior, and model semantics were not changed unless explicitly justified and documented.
  - Audit changed files against the plan's scope boundaries.

  **Must NOT do**:
  - Do not approve if opportunistic architecture cleanup introduced behavioral drift.
  - Do not treat undocumented logic changes as acceptable collateral.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: requires change-intent analysis against scope boundaries.
  - Skills: `[]` - no extra skills required.
  - Omitted: `['/review-work']` - this is a narrower scope-fidelity audit.

  **Parallelization**: Can Parallel: YES | Final Wave | Blocks: [Completion] | Blocked By: [9]

  **Acceptance Criteria**:
  - [ ] No out-of-scope business logic changes are present.
  - [ ] Any unavoidable non-structural change is explicitly documented and justified.
  - [ ] Final review issues a pass/fail verdict on scope fidelity.

  **QA Scenarios**:
  ```
  Scenario: Scope-boundary audit
    Tool: Bash
    Steps: Compare changed files and diffs against the allowed-scope list; classify each change as structural, compatibility, resource-boundary, or out-of-scope.
    Expected: All changes are in allowed categories or explicitly justified; audit report is written.
    Evidence: .sisyphus/evidence/f4-scope-fidelity.md

  Scenario: Out-of-scope regression detection
    Tool: Bash
    Steps: Scan diffs and changed files for modifications to battle heuristics, threat thresholds, ROI/template constants, hero behavior logic, or model semantics.
    Expected: No undocumented out-of-scope logic changes remain; any detection causes task failure with exact files.
    Evidence: .sisyphus/evidence/f4-scope-fidelity-error.txt
  ```

## Commit Strategy
- Use small migration commits aligned to tasks.
- Do not mix structural relocation with behavioral changes in the same commit.
- Prefer one commit per completed task or tightly coupled task pair.
- Compatibility shim introduction and shim removal must be separate commits.
- Legacy isolation and legacy deletion must be separate commits.

## Success Criteria
- The project has one canonical code root: `src/wzry_ai/`.
- v1.0's battle-centric architecture is preserved and clearer than before.
- Entry startup is thinner, testable, and no longer an oversized orchestration script.
- Resource boundaries are explicit and future additions do not require ad hoc path logic.
- Legacy systems are isolated, named, and on a path to removal instead of silently coexisting.
- Future additions (new heroes, new detectors, new runtime modes) can be implemented inside stable domain boundaries without growing root-level sprawl.
