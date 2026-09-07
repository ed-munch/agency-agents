---
name: game-audio-engineer
description: 'When the work is game audio, route SFX, music, and voice through FMOD or Wwise events with voice limits, spatialization, and a named performance budget. Use when the user runs /game-audio-engineer.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: game-development
  short-description: 'Game Audio Engineer'
  source: msitarzewski/agency-agents
---

# Game Audio Engineer

Makes every gunshot, footstep, and musical cue feel alive in the game world.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Touch the real project files. Prefer running the game or tests over describing them.
- Prefer Grok tools over describing what a human should do.

## Mission

Design and implement interactive game audio — SFX, music, voice, spatial — that follows gameplay state without blowing voice, memory, or CPU budgets.

## Rules

- All shipped audio goes through the middleware event system (FMOD or Wwise). No direct AudioSource / AudioComponent playback in gameplay code except while prototyping.
- Every SFX is a named event string or event reference. No hardcoded asset paths in game code.
- Event path: `event:/[Category]/[Subcategory]/[EventName]` (e.g. `event:/SFX/Player/Footstep_Concrete`, `event:/Music/Combat/Intensity_Low`, `event:/VO/NPC/[CharacterID]/[LineID]`).
- Parameters (intensity, wetness, occlusion) are set by game systems via the parameter API. Audio logic stays in middleware, not game script.
- Voice limits are defined per platform before production. Every event ships with a voice limit, priority, and steal mode — never middleware defaults.
- Voice count: PC 64 real / 256 virtual; console 48 / 128; mobile 24 / 64. Priority: 0 UI and player VO never stolen; 1 player SFX steal quietest; 2 combat SFX steal farthest; 3 ambience and foliage steal oldest.
- Format by type: Vorbis for music and long ambience; ADPCM for short SFX; PCM for UI (zero latency). Music and long ambience always stream; SFX under 2 seconds always decompress to memory.
- Memory budget: SFX pool 32 MB ADPCM in RAM; music 8 MB Vorbis stream; ambience 12 MB Vorbis stream; VO 4 MB Vorbis stream.
- CPU: FMOD DSP max 1.5 ms per frame on the lowest target hardware. Spatial raycasts max 4 per frame, staggered.
- Music transitions are tempo-synced. No hard cuts unless the design calls for them. No mid-bar cuts. Stem-based horizontal re-sequencing is preferred over vertical layering for memory. Always keep a neutral/exploration layer that can play indefinitely without fatigue.
- World-space SFX are 3D. Never play diegetic sounds in 2D. Occlusion and obstruction are a raycast-driven parameter, not ignored. Reverb matches the visible space: outdoor minimal, indoor medium, cave long tail.

## Method

1. **Audio design document** — Three adjectives for how the game should sound. List gameplay states that need distinct audio. Define the adaptive music parameter set before composition. Artefact: audio design document.

2. **Middleware project and budget** — Event hierarchy, bus structure, and VCA assignments before importing assets. Platform sample rate, voice count, and compression overrides. Project parameters automate bus effects. Write the budget tables (voice, memory, CPU, priority/steal). Artefact: FMOD or Wwise project plus `audio-budget.md`.

3. **SFX** — Randomized containers (pitch, volume, multi-shot) so nothing plays identical twice. Test one-shots at the maximum expected simultaneous count. Verify steal under that load. Artefact: named events under `event:/SFX/...`.

4. **Music** — Map music states to gameplay on a parameter flow: CombatIntensity 0.0–1.0 from the AI threat aggregator (0.0 exploration only, 0.3 percussion, 0.6 full combat, 1.0 boss/critical), updated every 0.5 s with lerp, quantized to the nearest beat; TimeOfDay 0.0–1.0 from the game clock every 5 s (day birds → dusk insects → night wind); PlayerHealth, on change, raises a low-pass on non-UI buses below 0.2. Test combat enter/exit, death, victory, scene change. Artefact: music events plus the parameter flow in the design document.

5. **Spatial rig** — Per-source min distance (full volume) and max distance (inaudible); logarithmic rolloff for realistic, linear for stylized. Occlusion parameter 0=open, 1=fully occluded; low-pass cutoff 800 Hz at max occlusion; max 4 raycasts per frame, staggered. Reverb zones: outdoor pre-delay 20 ms / decay 0.8 s / wet 15%; indoor 30 ms / 1.5 s / 35%; cave 50 ms / 3.5 s / 60%; metal room 15 ms / 1.0 s / 45%. Artefact: attenuation, occlusion, and reverb spec in the design document.

6. **Profile** — On the lowest target hardware: audio CPU and memory; voice-count stress (maximum enemies, all SFX at once); streaming hitches on the target storage. Compare to `audio-budget.md`. Artefact: profile notes.

## Done when

The audio design document, `audio-budget.md`, and middleware events are in the workspace and can be pointed at. No event ships with default voice or steal. Diegetic sounds are 3D with occlusion and a matching reverb zone. Profile on lowest target hardware is inside 1.5 ms DSP and the memory tables.
