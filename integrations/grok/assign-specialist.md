# assign-specialist

Invariant : chaque agent / subagent a un specialist `agency-agents`. Pas de helper générique.  
Canal : `prompt` (`spawn_subagent` n’a pas de champ `persona`). `load-specialist.py`.

## Pick

Matching = jugement parent. Slug `agency` interdit. Catalog hors enfant.

```
candidates := slugs pertinents pour TASK
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

## Happy path

1. Candidates  
2. `load-specialist.py` sur le ou les deux meilleurs  
3. ASK / CLOSEST ; annonce dès le gagnant  
4. PROMPT = stdout gagnant + TASK ; `description`  
5. `spawn_subagent`  
6. overlay  

## Enveloppes

**parallel / workflow.agent :** pour chaque item, le path ci-dessus. `ITEM_EXCLUDED` (ASK / `LOC_*`) nommé, n’abort pas les autres. `LOC_PLUGIN_MISSING` abort tout. `parallel()` = simultané.

**Parent-as-role :** 1–4 puis exécuter TASK (pas de spawn, pas de `description`). Outils = session parent ; METHOD Agency. ASK pending : ne pas s’attribuer le rôle.

CLOSEST n’est pas un abort.
