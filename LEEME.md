# Edición de videos Matrona Catita

- `.claude/skills/video-matrona-catita/SKILL.md`: la skill. Se carga sola en cualquier sesión de Claude Code abierta sobre este repositorio.
- `editor/`: transcripción, render y rastreo de manchas.
- `proyectos/<tema>/`: plan de edición, tarjetas y retoques de cada video.
- `assets/`: logo animado para el cierre y fuente Poppins Bold.
- `entregas/`: videos finales, con y sin subtítulos.

Render: `python3 editor/render.py proyectos/<tema>/plan.json toma.mp4 assets/logo_animado.mov entregas -vN`
(agregar `--hoja` para ver la hoja de fotogramas antes del render).
