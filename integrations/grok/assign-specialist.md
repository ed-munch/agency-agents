# assign-specialist

Sous `/algorithm`, ce protocole est **hors happy path**.

Happy path : `/algorithm` → un agent de porte (`agents/agency-*.md`) → **au plus un** skill si la porte l’a nommé (`tool: /slug`). Gates 1–2 peuvent finir à zéro specialist.

Ce fichier s’applique quand un spawn a encore besoin d’un slug nommé (slash `/slug`, ou une porte qui a déjà annoncé `tool: /slug`). Pas pour ouvrir une session. Pas de helper générique.

Invariant : chaque agent / subagent hors algo a un specialist `agency-agents`.  
Canal : `prompt` (`spawn_subagent` n’a pas de champ `persona`). `load-specialist.py`.

## Pick

Matching = jugement parent. Slug `agency` interdit (c’est le routeur). Catalog hors enfant — ne pas coller `references/roster.md` dans le prompt.

Sous `/algorithm`, les candidats **doivent** être autorisés sur la porte en cours (`GROK.md`). `/ai-engineer` et `/devops-automator` interdits en portes 1–3.

```
candidates := slugs pertinents pour TASK (et pour la porte, si algo)
|c|==0 → pick 1 + "closest: /slug (no clean match)"
|c|==1 → that slug
|c|>=2 → un `load-specialist.py` plein par candidat ; jobs différents ET les deux ont ## Method
         → ASK (wait user, pas de spawn) ; sinon CLOSEST
```

Sans `## Method` (vu dans le stdout) → CLOSEST. ASK pending → pas de spawn.

## Load specialist

`python3 integrations/grok/load-specialist.py <slug>` from the plugin root — un appel par slug, stdout = IDENTITY+METHOD.  
Exit 2 `LOC_PLUGIN_MISSING` · 3 `LOC_SLUG_UNKNOWN` · 4 `LOC_SKILL_UNREADABLE`.  
`LOC_ASK` : 3–5 slugs **déjà** dossiers `skills/<slug>/` ; wait user ; pas de spawn.

## Prompt + label

```
PROMPT := stdout de load-specialist.py (gagnant) + TASK
description := "[" slug "]" SP rest     # rest = tâche courte, sans le slug
annonce    := "persona: /" slug
```

Les trois slugs identiques. Interdit : `slug: rest`, bullets à la place de la METHOD, IDENTITY sans METHOD.

## Overlay

Outils : `subagent_type` gagne (`explore` ne gagne pas d’écriture).  
Méthode : Agency gagne vs persona bundlée (`[writer]`, …). Une METHOD. Pas d’enfant sans slug.

## Path (quand on est déjà hors happy path)

1. Candidates (filtrés par porte si `/algorithm`)
2. `load-specialist.py` sur le ou les deux meilleurs
3. ASK / CLOSEST ; annonce dès le gagnant
4. PROMPT = stdout gagnant + TASK ; `description`
5. `spawn_subagent`
6. overlay

## Enveloppes

**parallel / workflow.agent :** pour chaque item, le path ci-dessus. `ITEM_EXCLUDED` (ASK / `LOC_*`) nommé, n’abort pas les autres. `LOC_PLUGIN_MISSING` abort tout. `parallel()` = simultané.

**Parent-as-role :** 1–4 puis exécuter TASK (pas de spawn, pas de `description`). Outils = session parent ; METHOD Agency. ASK pending : ne pas s’attribuer le rôle.

CLOSEST n’est pas un abort.
