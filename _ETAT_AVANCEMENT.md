# 📍 ÉTAT D'AVANCEMENT — Armée de Résolution de Problèmes

> **But de ce fichier :** point d'ancrage durable. Quand l'utilisateur demande
> « où es-tu ? », Claude LIT ce fichier (ne devine pas). Mis à jour à chaque
> soldat/officier terminé. Dernière maj : 🎉 SOLVE-KIT COMPLET — Stage A (paquet `solve_kit/`) + Stage B (commandes `/solve.*` + CLI `solve`), 17 tests OK, vérif e2e Meristina réussie. Repo `Meristina/solve-kit`, branche `claude/solve-kit-packaging` (PR #1).

---

## 🎯 LE PROJET EN 5 LIGNES
Construire, **fichier par fichier**, une armée généraliste de résolution de
problèmes, **portable Claude + OpenAI**. Hiérarchie : **Commandant → Officiers
(1 par phase) → Soldats (1 par méthode) → Skills (procédures)** + un **Inspecteur**
transverse. Tout est sector-agnostic. **Aucune info inventée** : accès internet
partout + sourcing obligatoire + Inspecteur en fin de boucle (sources/conformité/
qualité, droit de veto).

## 🧱 DÉCISIONS DE DESIGN (verrouillées)
1. **Portabilité** : chaque unité existe en 2 exemplaires → `agents/*.md` (Claude)
   + `solve_kit/**/*.py` (OpenAI). Les skills (`skills/*/SKILL.md`) sont côté Claude ;
   côté OpenAI la procédure est intégrée dans les instructions du soldat.
2. **Arsenal partagé** : une méthode = UNE skill + UN soldat, réutilisé par
   plusieurs officiers (pas de duplication).
3. **Grades** : 🔵 standard (Sonnet / gpt-5-mini) vs 🎖️ élite (Opus / gpt-5).
   Critère élite = **profondeur de raisonnement**, PAS la célébrité/fréquence.
4. **Langue** : fichiers rédigés en **anglais** ; comportement = **miroir** de la
   langue de l'utilisateur (FR/AR/EN).
5. **Délégation** : « manager garde la main » (agents-as-tools / `.as_tool()`),
   handoff réservé aux cas mono-spécialiste.
6. **Runtime** : sur Claude les sous-agents ne descendent qu'd'1 niveau → la
   délégation profonde se fait via Workflow ou via OpenAI ; sinon le commandant/
   officier « enfile le casque » du soldat en chargeant sa skill.

## 🔧 PATRON RÉPÉTABLE (pour créer un soldat)
1. `mkdir skills/<methode>/`
2. Écrire `agents/soldier-<methode>.md` (frontmatter name/description/model/color
   + corps : rôle, manuel=skill, règles dures, ce qu'il rend).
3. Écrire `skills/<methode>/SKILL.md` (procédure + template + format de sortie).
4. Écrire `solve_kit/soldiers/soldier_<methode>.py` (Agent + WebSearchTool + modèle).
5. **Câbler chez l'officier OpenAI** : décommenter l'`import` + la ligne `.as_tool()`.
   (Côté Claude : l'officier liste déjà le soldat dans son tableau d'arsenal.)
6. Mettre à jour CE fichier.

## 🪖 CÂBLAGE COMMANDANT (solve_kit/commander.py)
- ✅ Officier 1, 2, 3, 4, 5 **et Inspecteur** branchés (import + as_tool). Chaîne complète.

---

## 📊 PROGRESSION DÉTAILLÉE

### 🔴 Commandant — ✅ COMPLET
`agents/commander-problem-solving.md` + `solve_kit/commander.py` (Opus / model fort).

### 🟠 Officier 1 · Définir le problème — ✅ COMPLET (8/8 + 2 partagés baseline)
`officer-1-define-problem.md` + `solve_kit/officers/officer_1_define_problem.py`
Mandat étendu (Bloc #2) : **définir ET quantifier** l'état actuel (baseline).
| Soldat | Grade | Partage |
|---|---|---|
| QQOQCP | 🔵 | O1+O2+O4 |
| CATWOE | 🔵 | O1+O3 |
| 5-Pourquoi | 🎖️ | O1+O2 |
| Brainstorming | 🔵 | O1+O2+O3 |
| Reverse-BS | 🎖️ | O1+O3 |
| Affinités | 🔵 | O1 |
| CIRCEPT | 🔵 | O1+O3 |
| Pareto | 🔵 | O1+O5 |
| ♻️ Feuille de relevés | 🔵 | O1+O5 (baseline) |
| ♻️ Tableau de bord | 🔵 | O1+O5 (baseline) |

### 🟠 Officier 2 · Identifier les causes — ✅ COMPLET (6/6)
`officer-2-root-cause.md` + `solve_kit/officers/officer_2_root_cause.py`
- ♻️ hérités : 5-Pourquoi, Brainstorming, QQOQCP
- 🆕 Ishikawa 🔵 · Relations 🎖️ · MECE 🎖️ (partagé O2+O3)

### 🟠 Officier 3 · Trouver la solution — ✅ COMPLET (12/12)
`officer-3-solution.md` + `solve_kit/officers/officer_3_solution.py` (12 outils soldats actifs : 7 nouveaux + 5 partagés)
- ♻️ hérités CÂBLÉS : Brainstorming, Reverse-BS, CATWOE, CIRCEPT, MECE
- 🆕 DIVERGER : **SCAMPER** 🔵 · **ASIT** 🔵 · **Matrice de découverte** 🔵
- 🆕 CONVERGER : **Diagramme en arbre** 🔵 · **Analyse de la valeur** 🔵 · **Matrice de décision** 🎖️ · **Delphes** 🔵

### 🟠 Officier 4 · Lancer les actions — ✅ COMPLET (4 nouveaux + 1 partagé)
`officer-4-launch-actions.md` + `solve_kit/officers/officer_4_launch_actions.py` (🎖️ opus/gpt-5)
Mouvements : **PLAN → SCHEDULE → SECURE**.
- 🆕 PLAN : **Plan d'action** 🔵 (actions owned/testables ; **sans champ statut** → suivi = O5)
- ♻️ PLAN : **QQOQCP** 🔵 (partagé O1+O2+O4 — deep-frame d'UNE action complexe)
- 🆕 SCHEDULE : **PERT** 🎖️ (chemin critique, marges, durée) · **Gantt** 🔵 (timeline calendaire)
- 🆕 SECURE : **Risques/RAID** 🔵 (registre proba×impact + mitigation/owner + log RAID)
- 🔧 Révision périmètre (validée) : statut retiré (→O5) · QQOQCP recâblé · frontière O3-tree clarifiée · soldat Risques ajouté.

### 🟠 Officier 5 · Suivre l'efficacité — ✅ COMPLET (2 nouveaux + 1 partagé)
`officer-5-monitor.md` + `solve_kit/officers/officer_5_monitor.py` (🎖️ opus/gpt-5) — câblé au commandant.
Mouvements : **MEASURE → STEER** (boucle Check/Act du PDCA).
- 🆕 MEASURE : **Tableau de bord** 🔵 · **Feuille de relevés** 🔵 — désormais **partagés O1+O5** (baseline en O1, suivi solution en O5)
- ♻️ STEER : **Pareto** 🔵 (partagé O1+O5 — déviations vital-few)

### 🛡️ Inspecteur (transverse, fin de boucle) — ✅ COMPLET
`agents/inspector.md` + `solve_kit/inspector.py` (🎖️ opus/gpt-5, color purple) — câblé au commandant (`inspect`).
Vérifie : (a) sources internet (rien d'inventé) · (b) conformité secteur · (c) qualité
(avocat du diable → converge). Verdict PASS / PASS-WITH-FIXES / VETO + ré-inspection.
Audit only (ne refait pas le travail des officiers).

### 📘 Divers restants — ✅ FAIT
- ✅ `GUIDE.md` (présentation, architecture, catalogue 24 méthodes, install Claude +
  OpenAI, patron répétable, garde-fous).
- ✅ Câbler O4, O5, Inspecteur dans `commander.py`.

---

## 🔁 UPGRADES PIPELINE (post-MVP, 3 blocs — cadence : bloc par bloc avec validation)
- ✅ **Bloc #1 — Dossier de Mission + boucle de contrôle** (code-driven).
  Livré : `skills/mission-dossier/SKILL.md` · maj `commander.md` (sections « Mission
  Dossier » + « Control loop ») · **nouveau `solve_kit/mission.py`** (runner déterministe :
  dossier-dict, boucle commandant→inspecteur, ré-entrée sur VETO, `MAX_ITERS=3`) ·
  note d'entrée dans `commander.py`. Parser de verdict testé (VETO > PASS).
- ✅ **Bloc #2 — Mesure baseline** : `commander.md` Phase 1 = définir + quantifier ·
  Officier 1 `.md`/`.py` (mandat baseline + câblage partagé `check_sheet` + `dashboard`) ·
  soldats dashboard + check-sheet **généralisés en partagés O1+O5** (md/skill/py) ·
  partages maj (GUIDE + état). **Aucun nouveau soldat (réutilisation pure).**
- ✅ **Bloc #3 — Gates qualité entre phases** : `inspector.md`/`.py` à **2 modes**
  (GATE rapide = definition-of-done + sourcing ; FINAL complet = 3 contrôles + veto) ·
  `commander.md` invoque le gate après P1 et P3 · `mission.py` précise MODE: FINAL au
  gate de référence. Gates internes à la passe du commandant.

- ✅ **Bloc #4 — Checkpoint HITL avant Phase 4** : `commander.md` (section « 🚦 HITL
  CHECKPOINT » GO/NO-GO/REVISE entre P3 et P4) · `mission.py` **refondu en 2 stages**
  (DECIDE 0-3 → pause humaine `approval_fn` → EXECUTE 4-5) avec `console_approval` +
  `auto_approve` injectables · champ `hitl` au Dossier · GUIDE maj.

## 🧰 SOLVE-KIT — transformation en toolkit façon spec-kit (plan validé)
- ✅ **STAGE A — packager le moteur** : `git mv openai/ → solve_kit/` (paquet pip,
  imports relatifs, `__init__.py`, `main()`), `pyproject.toml` + `requirements.txt`,
  `tests/` (structure + harness e2e stub-SDK, **12 tests OK**), `README.md`, GUIDE/ÉTAT
  maj. Corrige le shadowing `openai/`. Branche `claude/solve-kit-packaging`.
- ✅ **STAGE B Phase 1 — COMPLET** : `.solve/memory/constitution.md` (10 articles) ·
  **7 templates** (dossier, problem, causes, solution, decision-package, actions,
  monitor) · **2 scripts** (`new-mission.sh` testé · `install-claude.sh` testé sur
  scratch : 9 cmds + 31 agents + 25 skills) · **9 commandes** `.solve/commands/`
  (mission, frame, define, causes, design, act [refuse sans GO], monitor, gate,
  inspect). `missions/` gitignoré. Installeur → `/solve.<name>` dans `~/.claude`.
- ✅ **STAGE B Phase 2 — CLI COMPLÈTE** : paquet `solve_cli/` (cli/scaffolder/
  integrations/runner_bridge) · console-script **`solve`** (init/run/check/version) ·
  `solve init --agent claude|cursor|copilot|gemini|opencode` scaffolde `.solve/` + commandes + (claude)
  agents/skills · `solve run --auto-approve` → `runner_bridge` appelle
  `solve_kit.mission.run_mission(..., auto_approve)` **inchangé** et sérialise le
  dossier en `missions/<NNN>/{dossier,deliverable}.md`. **Tests : 17 OK** (5 CLI).
  Smoke-test live OK (version/check/init).
- ✅ **Vérif toolkit e2e** : mission Meristina passée par les commandes → 7 artefacts
  fichiers, 2 GATE PASS, HITL GO respecté, Inspecteur FINAL = PASS WITH FIXES (a
  attrapé la conformité loi 09-08/CNDP). `missions/` gitignoré.

- ✅ **CI** : `.github/workflows/ci.yml` (compile + pytest, Python 3.10 & 3.12) — verte. Mergée dans `main` (PR #1).
- ✅ **Bundling PyPI** (branche `claude/solve-kit-bundling`) : payload mirroré sous
  `solve_cli/payload/` (généré par `solve sync`), `pyproject` package-data +
  `include-package-data` + `MANIFEST.in`, résolution dev-vs-bundled dans `scaffolder`,
  **test anti-drift** (Art. IV). Wheel vérifié (75 fichiers payload embarqués) ;
  `solve init` validé en mode **bundled** hors-repo. **20 tests OK.**

- ✅ **Adaptateurs multi-agents** (branche `claude/solve-kit-adapters`, PR #3) :
  `integrations.py` transcode le pack de commandes (source unique `.solve/commands/`)
  en formats natifs vérifiés — **claude** (.claude/commands, `solve.<n>.md`), **cursor**
  (.cursor/commands, MD sans frontmatter), **copilot** (.github/prompts, `*.prompt.md`
  mode:agent), **gemini** (.gemini/commands/solve/`*.toml`, args `{{args}}`), **opencode**
  (.opencode/commands). **21 tests OK** (init + transcodage vérifiés pour les 5).

## ▶️ PROCHAINE ACTION
🎉 **SOLVE-KIT COMPLET, distribuable, multi-agents** (Stage A + B + CI + bundling +
5 adaptateurs). PR #1 & #2 mergées dans `main`. PR #3 (adaptateurs) ouverte → à merger.
Plus de piste obligatoire ; le toolkit est livré.
