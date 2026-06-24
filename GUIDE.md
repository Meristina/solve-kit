# 📖 GUIDE — Armée de Résolution de Problèmes

> Mode d'emploi de l'armée généraliste de résolution de problèmes, **portable
> Claude + OpenAI**. Pour l'état d'avancement de la construction, voir
> `_ETAT_AVANCEMENT.md`.

---

## 1. Ce que c'est

Une **armée d'agents** qui résout n'importe quel problème (sector-agnostic) en
suivant une démarche structurée en 5 phases, avec un contrôle qualité final à droit
de veto. Deux principes non négociables :

- **Aucune info inventée.** Chaque unité a un accès internet ; tout fait est sourcé
  ou explicitement marqué `à vérifier`. L'Inspecteur vérifie en fin de boucle.
- **Miroir de la langue.** Les fichiers sont rédigés en anglais, mais chaque unité
  **répond dans la langue de l'utilisateur** (FR / AR / EN…).

---

## 2. Architecture

```
🔴 COMMANDANT  (orchestre, garde la main, livre le résultat)
   │
   ├─ 🟠 Officier 1 · Définir le problème
   ├─ 🟠 Officier 2 · Identifier les causes
   ├─ 🟠 Officier 3 · Trouver la solution      (diverge → converge)
   ├─ 🟠 Officier 4 · Lancer les actions        (plan → schedule → secure)
   ├─ 🟠 Officier 5 · Suivre l'efficacité        (measure → steer, boucle PDCA)
   │
   └─ 🛡️ INSPECTEUR (transverse, fin de boucle, DROIT DE VETO)
         sources · conformité · qualité (avocat du diable → converge)

Chaque Officier commande des 🔵/🎖️ SOLDATS (1 par méthode).
Un soldat = 1 skill (procédure) + 1 agent (Claude) + 1 port .py (OpenAI).
```

**Grades :** 🔵 standard (Sonnet / gpt-5-mini) vs 🎖️ élite (Opus / gpt-5). Le
critère d'élite est la **profondeur de raisonnement**, pas la célébrité de la
méthode.

**Délégation :** « le manager garde la main » (agents-as-tools / `.as_tool()`). Sur
Claude, les sous-agents ne descendent que d'un niveau : la délégation profonde passe
par Workflow ou par OpenAI ; sinon l'officier « enfile le casque » du soldat en
chargeant sa skill.

---

## 3. Arborescence

```
Armee_Resolution_Probleme/
├─ GUIDE.md                    ← ce fichier
├─ _ETAT_AVANCEMENT.md         ← état de construction (point d'ancrage)
├─ agents/                     ← versions CLAUDE (31 .md)
│   ├─ commander-problem-solving.md
│   ├─ inspector.md
│   ├─ officer-1..5-*.md
│   └─ soldier-*.md            (24 soldats)
├─ skills/                     ← procédures CLAUDE (24 SKILL.md)
│   └─ <methode>/SKILL.md
└─ openai/                     ← port OPENAI (31 .py)
    ├─ commander.py            ← point d'entrée
    ├─ inspector.py
    ├─ officers/officer_1..5_*.py
    └─ soldiers/soldier_*.py   (24 soldats)
```

Portabilité : chaque unité existe en 2 exemplaires — `agents/*.md` (Claude) +
`openai/**/*.py` (OpenAI). Côté Claude la procédure est une skill ; côté OpenAI elle
est intégrée dans les instructions du soldat.

---

## 4. Catalogue des méthodes (24 soldats)

| Officier | Soldats (🆕 nouveau · ♻️ partagé) |
| --- | --- |
| **O1 · Définir** | QQOQCP 🔵 · CATWOE 🔵 · 5-Pourquoi 🎖️ · Brainstorming 🔵 · Reverse-BS 🎖️ · Affinités 🔵 · CIRCEPT 🔵 · Pareto 🔵 |
| **O2 · Causes** | Ishikawa 🔵 · Diagramme des relations 🎖️ · MECE 🎖️ · ♻️ 5-Pourquoi · ♻️ Brainstorming · ♻️ QQOQCP |
| **O3 · Solution** | *Diverger* : SCAMPER 🔵 · ASIT 🔵 · Matrice de découverte 🔵 · ♻️ Brainstorming · ♻️ Reverse-BS · ♻️ CATWOE · ♻️ CIRCEPT · *Converger* : Diagramme en arbre 🔵 · Analyse de la valeur 🔵 · Matrice de décision 🎖️ · Delphes 🔵 · ♻️ MECE |
| **O4 · Actions** | Plan d'action 🔵 · PERT 🎖️ · Gantt 🔵 · Risques/RAID 🔵 · ♻️ QQOQCP |
| **O5 · Suivi** | Tableau de bord 🔵 · Feuille de relevés 🔵 · ♻️ Pareto |

Arsenal partagé : une méthode = **un** soldat, réutilisé par plusieurs officiers
(pas de duplication). Partages actuels : 5-Pourquoi (O1+O2), Brainstorming (O1+O2+O3),
QQOQCP (O1+O2+O4), CATWOE (O1+O3), CIRCEPT (O1+O3), Reverse-BS (O1+O3), MECE (O2+O3),
Pareto (O1+O5) · Tableau de bord (O1+O5) · Feuille de relevés (O1+O5). Les deux
derniers servent au **baseline** en O1 (mesurer l'état actuel) et au **suivi** en O5.

---

## 5. Lancer une mission — côté CLAUDE

### Installation
Copier les agents et les skills dans la config Claude de l'utilisateur :

```bash
cd Armee_Resolution_Probleme
mkdir -p ~/.claude/agents ~/.claude/skills
cp agents/*.md           ~/.claude/agents/
cp -R skills/*           ~/.claude/skills/
```

(Les skills gardent leur dossier : `~/.claude/skills/<methode>/SKILL.md`.)

### Utilisation
Dans Claude Code, s'adresser au **commandant** et décrire le problème. Il applique
la doctrine en 5 étapes, choisit le sous-ensemble MINIMAL de phases/méthodes
nécessaires (MECE), délègue aux officiers, puis fait passer le résultat à
l'Inspecteur avant de livrer.

> Rappel runtime : sur Claude la délégation ne descend que d'un niveau. Pour une
> chaîne profonde commandant→officier→soldat, soit on utilise Workflow, soit
> l'officier charge directement la skill du soldat (« enfile le casque »).

---

## 6. Lancer une mission — côté OPENAI

### Installation
```bash
pip install openai-agents
export OPENAI_API_KEY=sk-...
```

### Exécution
Les imports sont relatifs au dossier `openai/` (`officers.*`, `soldiers.*`,
`inspector`). Lancer **depuis `openai/`** (ou ajouter ce dossier au `PYTHONPATH`) :

```bash
cd openai
python commander.py
```

`commander.py` instancie le commandant (modèle `gpt-5`), lui branche les 5 officiers
+ l'Inspecteur via `.as_tool()`, et lance `Runner.run_sync(commander, "<le
problème>")`. Remplacer la chaîne d'exemple en bas de `commander.py` par le vrai
problème, ou importer `commander` depuis ton propre script.

Chaque unité dispose du `WebSearchTool` hébergé : l'accès internet est garanti
partout, donc aucune unité n'invente de faits.

---

## 7. Ajouter un soldat (patron répétable)

1. `mkdir skills/<methode>/`
2. Écrire `agents/soldier-<methode>.md` (frontmatter `name`/`description`/`model`/
   `color` + corps : rôle, manuel = skill, règles dures, ce qu'il rend).
3. Écrire `skills/<methode>/SKILL.md` (procédure + template + format de sortie).
4. Écrire `openai/soldiers/soldier_<methode>.py` (Agent + WebSearchTool + modèle).
5. **Câbler chez l'officier OpenAI** : décommenter l'`import` + la ligne `.as_tool()`.
   (Côté Claude, l'officier liste déjà le soldat dans son tableau d'arsenal.)
6. Mettre à jour `_ETAT_AVANCEMENT.md`.

**Contrôle qualité** à chaque ajout : `python3 -m py_compile openai/**/*.py` ;
vérifier `name` == nom de fichier, skill `name` == dossier, grade md↔py cohérent
(🔵 sonnet↔gpt-5-mini, 🎖️ opus↔gpt-5), et câblage actif chez l'officier.

---

## 8. Garde-fous transverses

- **Sourcing obligatoire.** Tout fait cite une source internet réelle, ou est marqué
  `à vérifier`. Les scores de jugement sont étiquetés comme estimations.
- **Inspecteur, 2 modes.** GATE rapide aux charnières P1→P2 et P3→P4 (definition-of-
  done + sourcing → GATE-PASS/FAIL, évite qu'une phase faible contamine l'aval) ;
  FINAL complet avant livraison (sources + conformité + qualité → PASS/PASS-WITH-FIXES/
  VETO). Un fait non sourcé, un risque de conformité matériel ou une faille logique
  fatale bloquent la livraison jusqu'à correction, puis ré-inspection.
- **Checkpoint HITL avant la Phase 4.** Une approbation humaine **GO / NO-GO /
  REVISE** est requise avant d'engager des ressources (Phase 4). Distinct de
  l'Inspecteur (qualité, pas autorité de dépense). Côté OpenAI, le runner
  `mission.py` fait une vraie pause via `approval_fn` (console par défaut ;
  injectable, ex. `auto_approve` pour les runs non interactifs).
- **Lanes nettes.** Chaque soldat « reste dans sa voie » et renvoie vers les autres
  (ex. : l'analyse de la valeur ne choisit pas — c'est la matrice de décision ; le
  plan d'action ne suit pas l'exécution — c'est l'Officier 5).
- **Miroir de la langue** partout, dans la sortie utilisateur.
```
