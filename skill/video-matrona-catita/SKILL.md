---
name: "video-matrona-catita"
description: "Guion y edición de videos cortos de Matrona Catita (Instagram/TikTok). Usar cuando Cata o Tomás pidan temas, un guion o suban una toma cruda para editar."
---

# Video Matrona Catita: temas, guion y edición

Tres modos: **A** temas, **B** guion, **C** edición de la toma cruda. Los scripts, el cierre animado con el logo y las medidas exactas viajan en `kit_matrona_catita.zip`: pedirlo adjunto al iniciar un chat de edición (esta skill solo guarda las instrucciones). Si el kit trae `LEEME.md` y `formato_medido.json`, mandan sobre este texto.

## Contexto fijo
- Catalina Carrasco (Cata), matrona en Chile. Cuentas Matrona Catita: Instagram ~12,4 mil, TikTok ~33,9 mil seguidores.
- Público: embarazadas y mamás recientes, mujeres 25-44 años, sobre todo chilenas. Objetivo: 2 videos por semana (martes y jueves 20:00) y que seguidoras chilenas agenden consulta.
- Tomás organiza el sistema; Cata habla en su voz. Cata valida todo lo clínico y lo legal antes de grabar y antes de publicar textos en pantalla. Nunca inventar contenido clínico.
- Respuestas breves y en viñetas; Cata no lee textos largos.
- Español chileno cercano ("guagua", "hoy día").

## Modo A: temas
1. Proponer 15 temas en viñetas: tema, palabra que la gente busca, fuente que prueba el interés y un gancho. Buscar en la web; no inventar interés.
2. Priorizar lo que mejor rinde en las estadísticas: procedimientos educativos (epidural, Leopold, vía venosa) traen alcance y seguidores; las bienvenidas de bebés rinden poco (van a historias). En TikTok el 71,7 % del tráfico es búsqueda: la palabra buscada va en la primera frase, en pantalla y en la descripción.
3. Mezcla mensual de 8 videos: 4 de procedimientos o "qué pasa en…", 2 de dudas de recién nacido con trend, 2 de temas chilenos (postnatal, beneficios, controles).
4. Cata elige 1 o 2 y se pasa al Modo B.

## Modo B: guion (formato teleprompter con códigos)
Cada línea que se dice lleva un código L y cada apoyo visual un código de tipo; Cata sube el material con ese código como nombre (`B1.mp4`, `F1.jpg`, `T1.mov`) y el editor lo ubica solo.

```
TÍTULO: tema
PALABRA CLAVE: lo que la gente escribe en el buscador
DURACIÓN META: 45-60 s   TOMA CRUDA: ~2 min

L1 [GANCHO] máximo 12 palabras, con la palabra clave
   T1: grabación de pantalla del trend o búsqueda, entra en "palabra"
L2 [PROMESA] Así que hoy día te voy a contar …
L3 [CUERPO] una idea por frase
   B1: qué muestra el clip, entra en "palabra", hasta el fin de L4
…
L9 [TRANQUILIDAD] frase que calma (sin apoyo visual)
L10 [CIERRE] qué hacer o qué esperar
   F1: foto con permiso, entra en "palabra"
L11 [CHAO] ¡Chao!  (saludo con la mano, 2 s quieta)

MATERIAL: código · tipo · quién lo consigue (Cata / Tomás / Claude lo genera)
PARA PUBLICAR: descripción con palabra clave + 3 a 5 hashtags; fuentes con enlace
```

Tipos de apoyo: **T** trend o pantalla original en grande (solo gancho); **B** clip ancho sin borde para el cuerpo, seguidos y sin huecos; **F** foto con borde blanco y etiqueta; **D** tarjeta de datos generada por código con la paleta de marca (temas no anatómicos como postnatal; máximo 6 palabras por línea).

Reglas: 9 a 12 líneas, frases cortas, término clínico correcto más su explicación simple, una línea de tranquilidad sin apoyo, sin subtítulos en L1, L2 ni en el "Chao". Cada dato clínico o legal lleva fuente oficial citada. Indicaciones de grabación que van con el guion: vertical, celular fijo, luz de frente, sin música; cara en el tercio superior y hombros libres; una línea a la vez con 1 s de silencio entre líneas; si se equivoca repite la LÍNEA COMPLETA desde el inicio; todo en una toma, al final "¡Chao!", saludo y 2 s quieta.

## Modo C: edición de la toma cruda

### Formato objetivo (video final aprobado, "cabecita alargada", medido sobre 1080x1920)
- Salida 1080x1920, 30 fps, H.264 CRF 17 (preset veryfast, yuv420p, bt709), audio AAC 192k a -14 LUFS con pico -1,5 dBTP; 45-60 s. No entregar en 4K; si la toma llega en 4K, bajar a 1080x1920 antes de trabajar.
- Entregables: `Matrona_<tema>_vN.mp4` y `Matrona_<tema>_vN_sin_subtitulos.mp4` (para CapCut).
- Ritmo: cero silencios; pausa objetivo 0,10-0,13 s, nunca más de 0,25 s. Sin "okay", "eh", arranques en falso ni repeticiones; de cada línea repetida queda la mejor dicha gramaticalmente. Nunca cortar un término clínico. Piezas de 2 a 4 s con zoom alternado 1,00 / 1,09 y deriva 1,8 %, anclado en la cara (555, 640) para disimular cortes.
- Orden: gancho (Cata sola, ~1 s) → trend en grande → promesa (Cata sola) → cuerpo con subtítulos y clips seguidos → fotos → tranquilidad sin apoyo → cierre del tema → "¡Chao!" sin subtítulo → cierre animado de 3 s en silencio.
- **Trend (T):** grabación de pantalla ORIGINAL con su interfaz, en grande: rect [104, 247, 976, 1672] (872x1425), tapa la cara mientras dura (~4,4 s). Entra con desenfoque y fundido de 0,25 s; ~1 s después un acercamiento a la foto sin mover el marco; sale con corte seco a Cata. Sin subtítulos.
- **Clip de apoyo (B):** rect [52, 1216, 1029, 1716] (977x500), sin borde ni esquinas; clips seguidos de 2,5 a 7 s; cada uno entra en la palabra que nombra lo que muestra.
- **Foto (F):** rect [220, 1224, 860, 1696] (640x472), borde blanco 7 px, esquinas 34 px, sombra suave, entrada 0,32 s; etiqueta píldora blanca abajo-izquierda (punto de color + texto en negrita + texto gris, ej. "Al nacer  cabecita alargada" → "Días después  recupera su forma"); crédito pequeño abajo-izquierda ("vía TikTok · Matti").
- **Datos (D):** tarjeta generada por código con la paleta de marca, en el rect de B o de F; Cata valida el texto. Entrada animada de 0,45 s: sube desde abajo, crece de 72 % a 100 % con rebote y funde. Tarjetas seguidas: la nueva entra encima de la anterior. Una tarjeta puede quedar hasta que entra la siguiente (D6 duró 14 s y fue aprobada).
- **Sin apoyo** en frases de tranquilidad ("pero tranquilos…") ni en el "Chao". Lo que Cata agrega en CapCut se respeta tal cual.
- **Subtítulos:** Poppins Bold 64 px (baja hasta 48 si no cabe en 880 px), 1-4 palabras por grupo, blanco `#FFFFFF` con la palabra activa en amarillo `#FFD640`, centrados en x 540, y 1170, **sin borde**: doble sombra suave (blur 13 px al 78 % + blur 3 px al 85 %), entrada 0,11 s. Parten recién después de la promesa (en la referencia, a los 8,0 s) y no hay en gancho, trend, promesa ni "Chao". Verificar legibilidad sobre fondos claros.
- **Cierre:** 3 s en silencio después del "Chao", generado desde `assets/logo_animado.mov` (grabación 828x1170 del logo): ajustado al ancho de 1080 con el fondo extendido y difuminado arriba y abajo, velocidad 1,6x para que el logo termine de dibujarse antes de 1,5 s, aparición progresiva de 0,5 s y fundido a negro de 0,6 s.
- **Retoques:** manchas pequeñas en la ropa se borran rastreándolas cuadro a cuadro (`editor/rastrear_mancha.py` + clave `mancha` del plan); verificar que no quede resto en ningún cuadro.
- **Paleta de marca:** #F7EBE9, #F3D8CA, #EEC0A5, #D8A088, #271D1B; acento de subtítulos #FFD640.

### Antes de editar: material y preguntas
- Una sesión en la nube (Claude Code web) NO ve los chats de Cowork ni los documentos del proyecto: el guion se pega en el chat o se sube al repositorio `matronacatita/Edici-n-video`.
- Los adjuntos del chat aceptan hasta ~30 MB. Si la toma pesa más: exportarla en 1080x1920 con buena calidad (ideal 8-12 Mbps), o partirla en trozos de menos de 30 MB (mejor calidad: se conserva el 4K original; el orden se detecta solo por el audio y hay que quitar el cuadro repetido que queda en las uniones), o abrir el chat en la app de escritorio sobre la carpeta del video. No usar 4K.
- Revisar qué es cada archivo antes de asumir: el `RPReplay` del 2026-11-14 era la animación del logo (sirve de cierre), no un trend.
- Preguntar si la toma viene **cruda** o **ya editada de corrido**. Si ya viene editada: NO cortar pausas ni aplicar zoom alternado; solo tarjetas, subtítulos, retoques, audio y cierre.
- Si falta el guion, ubicar cada tarjeta por su texto y entregar la tabla "tarjeta → palabra de entrada" para que Cata la confirme.

### Procedimiento
1. **Inventario:** ffprobe de cada archivo; trabajar sobre una copia 1080x1920. Extraer wav 16 kHz mono (ASR) y 48 kHz (audio final).
2. **Transcribir:** Parakeet (`sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8`) con tiempos por palabra; verificar con Whisper turbo en palabras dudosas. Si ambos modelos discrepan con lo que ella dijo, mandan los dos sobre una ventana corta.
3. **Alinear con el guion:** emparejar lo dicho con las líneas L; por cada línea elegir la última toma completa que mejor coincide; marcar para revisión las líneas con parecido menor a 0,85 o con texto distinto al guion.
4. **Islas de voz:** envolvente de 10 ms, umbral +14 dB sobre el piso; cerrar huecos menores a 150 ms; margen 0,05 s antes del onset y 0,06 s después del offset, redondeado a cuadros.
5. **Plan de edición** (un archivo de configuración por video): cortes por línea, grupos de subtítulos y cada apoyo con archivo, tipo y palabra de entrada y salida. No reescribir código por video.
6. **Hoja de fotogramas** en cada corte y en cada entrada y salida de apoyo (máximo 6 imágenes por revisión) antes de renderizar.
7. **Audio:** cortar con fades de 8 ms, highpass 70, compresor suave, loudnorm en dos pasadas (I=-14, TP=-1,5, LRA=11). Si parte del audio viene de la edición de CapCut de Cata o Tomás, concatenarlo sin re-normalizar.
8. **Render** en una pasada, con y sin subtítulos, cierre pegado.
9. **Verificar antes de entregar:** (a) re-transcribir el resultado: texto corrido, sin palabras cortadas ni repetidas, igual al guion; (b) ninguna pausa mayor a 0,25 s dentro del habla; (c) sin clics en los cortes (salto máximo entre muestras menor a 0,01); (d) nada tapa la cara salvo el trend y los subtítulos se leen; (e) -14 LUFS ±0,5 y pico ≤ -1,5 dB; (f) sin subtítulos en gancho, trend, promesa y "Chao"; cierre completo.
10. **Entregar** con 1-2 líneas de contexto y avisar riesgos: clips con marca de agua ("SAMPLE USE ONLY · Nucleus Medical Media"), contenido de terceros marcado como IA en el trend, fotos de personas sin permiso; recordar que Cata valide los textos clínicos en pantalla.

### Código y plan (repositorio `matronacatita/Edici-n-video`)
- `editor/transcribir.py` (Parakeet con tiempos por palabra), `editor/render.py` (render con y sin subtítulos desde un `plan.json`; `--hoja` genera la hoja de fotogramas; `-vN` fija la versión), `editor/rastrear_mancha.py`.
- Un plan por video en `proyectos/<tema>/plan.json`: `segments` (tramos de la toma que se conservan; un solo tramo = sin cortes), `words`, `cards` (archivo, rect, entra, sale), `subs`, `cierre`, `mancha`, `zoom`, `drift`. Para una versión nueva se edita el plan, no el código.
- Entregas en `entregas/`. Con la toma original en mejor calidad basta volver a correr `render.py` con el mismo plan.

### Entorno
- Probado el 2026-11-14 en sesión nube: `pip install sherpa-onnx soundfile shapely scipy opencv-python-headless` funciona y el modelo Parakeet baja desde GitHub (487 MB). Whisper NO se puede bajar (Hugging Face bloqueado): verificar palabras dudosas re-transcribiendo ventanas cortas (2-4 s) con Parakeet. Parakeet puede saltarse tramos largos en una sola pasada: transcribir en ventanas de ~25 s.
- Poppins Bold: `npm pack @fontsource/poppins` (el .woff carga en PIL); ya está en `assets/fonts/`.
- Con voz suave o ruido de fondo, el umbral de islas de +14 dB corta sílabas: usar piso +6,5 dB y revisar el final de cada frase ("explico", "solas", "postnatal" quedaron cortas en el primer intento).
Falta por defecto `sherpa-onnx`, `soundfile`, `shapely` y los modelos de GitHub `k2-fsa/sherpa-onnx` (tag `asr-models`). Si la instalación de paquetes está bloqueada en la cuenta, detenerse, decirlo en una línea y pedir que se active en los ajustes de red y abrir un chat nuevo; no improvisar una edición sin transcripción.

## Cómo pide Cata los cambios
Suele mandar un audio o video comentando mientras ve el corte: parte es lectura del video y parte son instrucciones. Separarlas antes de actuar; si una instrucción es ambigua, una sola pregunta con opciones concretas. Cada corrección que sea regla nueva se anota en el historial con fecha.

## Estadísticas y marketing
Cada video se mide a 7 días contra la mediana de los 8 anteriores. Se anota: vistas, tiempo promedio visto, % que lo ve completo, guardados, compartidos, comentarios, seguidores nuevos, fuente principal (búsqueda / Para ti), toques en el enlace. Sobre la mediana en vistas y en guardados + compartidos → se vuelve serie; bajo la mediana dos veces el mismo tipo → se descarta o cambia el gancho. Cata graba la pantalla de estadísticas cada 2 semanas y se actualiza la planilla.

## Historial de decisiones de Cata
- 2026-11-05 "cabecita alargada": trend como grabación de pantalla original; sin cuadro en "pero tranquilos"; imágenes reales (fotos, pelvis ósea), no dibujos animados; subtítulos sin borde y sin subtítulo en el "Chao"; sin subtítulos mientras dura el inicio con el trend; cierre con el logo a pantalla completa; conversación fluida sin silencios.
- 2026-11-09: entrega en 1080x1920 (4K no es necesario); 2 videos por semana; planes en viñetas breves; primer tema postnatal 12 vs 18 semanas. El video final aprobado (export de CapCut) manda sobre la skill anterior: trend directo en grande, clips anchos sin borde en el cuerpo, subtítulos desde el cuerpo, cierre animado de 3 s.- 2026-11-14 "postnatal 12 vs 18": la toma llegó ya editada de corrido → sin cortes adicionales ni zoom. Tarjetas D1-D7 aprobadas en estas palabras: D1 "Después del parto", D2 "Opción 1", D3 "Opción 2", D4 "Si eliges las 18", D5 "Al menos 30 días", D6 "En las dos opciones", D7 "él también debe avisar". Tarjetas con animación de entrada. Quitar manchas de la ropa. Sin trend cuando no hay grabación del trend: parte directo Cata. Cierre con el logo animado, aparición y desvanecimiento progresivo.

## Registro de iteraciones (para afinar la edición)
| Fecha | Video | Versión | Qué se hizo | Resultado |
|---|---|---|---|---|
| 2026-11-14 | postnatal 12 vs 18 | v1 | 17 cortes de pausas, zoom alternado, tarjetas D1-D7 con fundido, subtítulos, cierre con logo; 51 s | Tarjetas y resto bien; rechazados los cortes (la toma ya venía editada) |
| 2026-11-14 | postnatal 12 vs 18 | v2 | Sin cortes ni zoom, tarjetas con entrada animada, mancha blanca de la polera borrada; 55 s | Aprobado ("Perfecto") |
| 2026-11-14 | postnatal 12 vs 18 | v3 | Misma edición que v2 desde la toma 4K original subida en 3 partes (<30 MB c/u), unidas en orden y bajadas a 1080x1920 | Algo más nítida que v2 (pestañas, piel, pelo); diferencia moderada, se nota al ampliar |

Límites conocidos: la calidad final no supera la de la toma recibida (la versión liviana venía a 3,7 Mbps; subir la resolución por software no recupera detalle); sin Whisper como segunda verificación; el audio con ruido de fondo solo se limpia de forma suave.
