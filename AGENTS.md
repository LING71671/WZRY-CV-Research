# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-10
**Git:** unavailable (not a git repo)

## OVERVIEW
Windows-only 王者荣耀 automation project for MuMu emulator. Core stack: Python, OpenCV, scrcpy/ADB, Ultralytics YOLO, OCR, template matching.

## STRUCTURE
```text
./
├── Master_Auto.py      # runtime entrypoint, thread wiring, main loop
├── config/             # all runtime constants, ROI, emulator, hero metadata
├── game_manager/       # UI state machine, template matching, clicks, hero pick
├── detection/          # model1/2/3 detectors + modal fusion
├── device/             # emulator discovery, ADB, scrcpy transport
├── utils/              # logging, frame sharing, OCR, keyboard, thread supervision
├── skills/             # hero skill logic and shared skill base
├── battle/             # combat FSM, decision makers, threat/target logic
├── movement/           # follow / stuck / minimap movement logic
├── models/             # YOLO weights
├── image/              # template assets used by state detection
├── hero/               # hero portrait assets
└── data/               # MuMu config, class names, map grid
```

## WHERE TO LOOK
| Task | Location | Notes |
|---|---|---|
| Start the app | `Master_Auto.py` | `main()` bootstraps emulator, windows, queues, detectors, threads |
| Adjust runtime constants | `config/base.py` | FPS, ADB path, model paths, movement + battle thresholds |
| Adjust UI template detection | `config/templates.py` | ROI and confidence thresholds assume fixed layout |
| Change supported heroes / lane mappings | `config/heroes/` | Name mapping, support config, hero state configs |
| Understand menu/game flow | `game_manager/state_definitions.py`, `state_transitions.py`, `state_detector.py` | Core UI state machine |
| Change click/tap behavior | `game_manager/click_executor.py` | ADB-backed action executor |
| Handle popups / hero pick | `game_manager/popup_handler.py`, `hero_selector.py` | UI remediation + hero lock-in |
| Emulator / ADB issues | `device/emulator_manager.py`, `device/ADBTool.py`, `device/ScrcpyTool.py` | MuMu-specific window + stream plumbing |
| Frame / OCR / logging utilities | `utils/` | Shared infrastructure used by many modules |
| Combat decision logic | `battle/` | FSM + decision makers + world state |
| Skill behavior | `skills/` | Hero-specific skill loops on shared base |
| Movement behavior | `movement/` | Unified movement + stuck detection |

## CODE MAP
| Symbol / module | Role | Location |
|---|---|---|
| `main` | top-level runtime orchestrator | `Master_Auto.py` |
| `GameStateDetector` | UI state detection + orchestration glue | `game_manager/state_detector.py` |
| `GameState` / `STATE_SIGNATURES` | state catalog + detection metadata | `game_manager/state_definitions.py` |
| `STATE_TRANSITION_RULES` | allowed state transitions | `game_manager/state_transitions.py` |
| `TemplateMatcher` | template matching engine | `game_manager/template_matcher.py` |
| `ClickExecutor` | click/swipe/keyevent backend | `game_manager/click_executor.py` |
| `HeroSelector` | pick / verify hero | `game_manager/hero_selector.py` |
| `PopupHandler` | dismiss/handle popup states | `game_manager/popup_handler.py` |
| `SharedFrameManager` / `FrameManager` | frame fan-out and caching | `utils/frame_manager.py` |
| `ThreadSupervisor` | worker restart watchdog | `utils/thread_supervisor.py` |
| `BattleFSM` | combat-mode state machine | `battle/battle_fsm.py` |
| `fuse_modal_data` | model1+model2 merge point | `detection/modal_fusion.py` |

## CONVENTIONS
- Project is package-at-root, not `src/` based.
- Chinese hero names are canonical runtime identifiers; pinyin mapping lives in `config/heroes/mapping.py`.
- `config/__init__.py` is the stable import surface; most modules use `from config import ...`.
- State detection is template-first and resolution-specific.
- Runtime coordination prefers queues, module-level helpers, and long-lived threads over dependency injection.

## ANTI-PATTERNS (THIS PROJECT)
- Do not assume portability: repo is tuned for **MuMu + Windows + near-1080p**.
- Do not change ROI / threshold constants casually; template matching is tightly coupled to current UI layout.
- Do not add new config constants directly into random modules; wire them through `config/`.
- Do not treat `hero_skill_manager.py` as the primary path; file itself is marked old/legacy, v2 logic lives in `*_skill_logic_v2.py` and `hero_skill_logic_base.py`.
- Do not ignore emulator discovery branches; ADB path and window matching have multiple fallbacks.

## UNIQUE STYLES
- Heavy inline Chinese comments explain intent at line level.
- Distinct domain split: `game_manager` for UI state, `battle` for combat decisions, `skills` for hero actions, `movement` for locomotion.
- Shared helpers are centralized under `utils/`, especially logging/frame/OCR/input.
- Assets are first-class runtime dependencies, not just docs/media.

## COMMANDS
```bash
pip install -r requirements.txt
python Master_Auto.py
```

## NOTES
- `使用文档.txt` says MuMu only; current project also persists MuMu window/device info in `data/mumu_config.json`.
- No test suite or CI config found; validation is manual emulator-backed runtime testing.
- Existing Python diagnostics contain many pre-existing issues unrelated to this documentation work.
- If adding nested docs elsewhere, prioritize directories with clear logic boundaries; leave `image/`, `hero/`, `models/`, `data/` under parent coverage unless process/docs there become complex.
