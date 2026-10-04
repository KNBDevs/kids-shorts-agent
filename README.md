# kids-shorts-agent

Pipeline 100 % autónomo y a coste 0 para YouTube Shorts infantiles en 3D.

- `scene.py` — escena Blender procedural (personaje, animación, loop), render Cycles CPU.
- `audio.py` — música en bucle, SFX y voz (Piper TTS) sincronizados a frames.
- `compose.sh` — montaje 1080×1920, -14 LUFS.
- `.github/workflows/render.yml` — render repartido en 16 jobs paralelos + audio + montaje.

Fase actual: **piloto** (vídeo "Aprende los colores con Pip").
