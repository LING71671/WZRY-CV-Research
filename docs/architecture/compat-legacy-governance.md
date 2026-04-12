# Compatibility and Legacy Code Governance

## Overview

This document defines the governance policy for the `src/wzry_ai/compat/legacy/` directory and any transitional compatibility surfaces elsewhere in the codebase.

---

## Inventory

### Current Legacy Files

| File | Status | Purpose | Lines |
|------|--------|---------|-------|
| `src/wzry_ai/compat/legacy/hero_skill_manager.py` | **Removed** | Transitional hero skill manager retired after confirming no active callers remained | 0 |
| `src/wzry_ai/compat/legacy/master_auto_main.py` | **Removed** | Was empty deadweight at planning time; removed per Task 6 | 0 |

### Transitional Compatibility Surfaces

| Symbol | Location | Re-exported From | Status |
|--------|----------|-------------------|--------|
| _None_ | _N/A_ | _N/A_ | **Retired** |

---

## Owner

**Primary Owner**: Skills module maintainers (`src/wzry_ai/skills/`)

**Escalation Path**: Architecture decisions affecting legacy compatibility require sign-off from the module owner before implementation.

---

## Allowed Callers

### HeroSkillManager (Retired)

The `HeroSkillManager` class and its compatibility re-export have been removed from the active surface.

**Current State**:
- `from wzry_ai.skills import HeroSkillManager` now fails
- No production caller is expected to depend on the retired path
- Any future compatibility need must be treated as a new explicit migration exception

---

## Removal Trigger

### HeroSkillManager Removal Criteria

The `HeroSkillManager` transition is complete. The compatibility surface has been removed after the zero-active-import audit.

### master_auto_main.py

This file was empty at planning time and has been removed. No removal criteria needed.

---

## Follow-up Milestone

### Milestone: Legacy Skill System Cleanup

**Target**: Task 7 completion or v1.1 release (whichever comes first)

**Deliverables**:
- [x] Audit all imports of `HeroSkillManager` across the codebase
- [x] Create migration guide: `HeroSkillManager` → `HeroSkillLogicBase`
- [x] Migrate any remaining callers to v2 skill logic
- [x] Remove `HeroSkillManager` re-export from `src/wzry_ai/skills/__init__.py`
- [x] Move `hero_skill_manager.py` to `compat/legacy/removed/` or delete if confirmed unused
- [x] Update this governance document to reflect final state

**Success Criteria**:
- `grep -r "HeroSkillManager" src/` returns only governance/history references
- `from wzry_ai.skills import HeroSkillManager` raises `ImportError`
- All active heroes remain functional using v2 skill logic only

---

## Policy Notes

### Adding New Legacy Code

New legacy code should only be added to `compat/legacy/` under the following conditions:

1. The code is being superseded by a new implementation
2. A migration path exists and is documented
3. An owner is assigned for eventual removal
4. Removal criteria and target milestone are defined

### Empty Files

Empty files in `compat/legacy/` are considered deadweight and should be removed unless they serve as intentional placeholders with documented purpose. The `master_auto_main.py` file was removed because it was empty and unexplained.

---

## Changelog

| Date | Change | Task |
|------|--------|------|
| 2026-04-11 | Created governance document | Task 6 |
| 2026-04-11 | Removed empty `master_auto_main.py` | Task 6 |
| 2026-04-11 | Documented `HeroSkillManager` as transitional | Task 6 |
| 2026-04-12 | Retired `HeroSkillManager` compatibility surface and deleted legacy manager file | Task 9 |
