# Oddwick — vídeo de MUESTRA del nuevo estilo de la casa (2026-11-20)

**No publicado ni programado en ningún sitio. No añadido a TOPICS.md.**

- Vídeo: `samples/oddwick_style_sample.mp4` (1080x1920, 30 fps, H.264 + AAC, **87,7 s**, 31 MB)
- Hoja de contactos: `samples/oddwick_style_sample_sheet.jpg` (un fotograma por plano, 51 planos)
- Guion (JSON): `samples/oddwick_style_sample_episode.json`
- Título propuesto: **I Have 3 Days to Pay for a Window** (≤ 45 caracteres)

## Premisa (original)
Un niño de 11 años rompe de un pelotazo la ventana del ayuntamiento en pleno discurso del alcalde. En este pueblo "si lo rompes, lo pagas": **1.000 $ antes del sábado o limpia la torre del reloj para siempre**. Tiene 3 días y 4 $. Limonada (Benny pide reembolso), pasear 6 perros (le arrastran por la pastelería: ahora debe 1.060 $), vender galletas de la abuela (se las come ella). Clímax: el **Concurso del Pueblo** de noche con pantallas de neón, el alcalde de presentador y la campeona invicta Mrs. Pickles. Última pregunta: "¿Cuántas ventanas tiene el ayuntamiento?". Ella dice 40; él dice **39, porque sabe exactamente cuál falta**. Gana, le da todo al alcalde... que lanza su sombrero de alegría **a través de la ventana 38**. Giro final (callback de la primera frase): "In this town, if you break it, you pay for it. So now the Mayor owes me a thousand dollars." + pregunta A/B.

## Guion (inglés, 300 palabras)
  - In this town, if you break it, you pay for it. And I just broke the town hall window.
  - With a baseball. During the Mayor's big speech.
  - The Mayor said: one thousand dollars by Saturday. Or you clean the clock tower. Forever.
  - I had three days. And four dollars.
  - Forever is a long time. I'm eleven.
  - Day one. I opened a lemonade stand. Fifty cents a cup.
  - My friend Benny bought one cup. Then he asked for a refund.
  - Day two. I started walking dogs. Six of them.
  - Actually, the dogs walked me. Straight through the bakery.
  - The baker made me pay for six cakes. Now I owed one thousand and sixty dollars.
  - So I sold my grandma's cookies door to door. Grandma ate the whole box first.
  - Day three. Still four dollars. Actually, three. Benny got his refund.
  - Then I saw the poster. Saturday night. The Town Game Show. First prize, one thousand dollars.
  - The whole town showed up. Neon lights. Cameras. And the host was the Mayor.
  - Round one, the baker. Out. Round two, Benny. Out. He asked for a refund.
  - Then it was just me and the champion. Mrs. Pickles. Undefeated for forty years.
  - Last question. For one thousand dollars. The whole town held its breath.
  - How many windows does the town hall have?
  - Mrs. Pickles hit the buzzer. Forty! The crowd went wild.
  - Wrong.
  - I said thirty-nine. Because I know exactly which one is missing.
  - Correct! Confetti. Fireworks. Benny cried.
  - I walked up and handed every dollar straight back to the Mayor. For the window.
  - The Mayor was so happy, he threw his top hat in the air.
  - Right through window number thirty-eight.
  - In this town, if you break it, you pay for it. So now the Mayor owes me a thousand dollars.
  - A or B?

Pregunta A/B final (dos velas Oddwick): **A: MAYOR CLEANS THE TOWER** / **B: DOUBLE OR NOTHING**.

## Voz (un solo narrador joven)
Kokoro, mezcla `am_puck 0.6 + am_echo 0.25 + af_heart 0.15`, **speed 1.22**, sintetizada frase a frase (timing exacto para subtítulos sin Whisper — HuggingFace está bloqueado desde la nube), y luego efecto "chico": `asetrate=26400,aresample=24000,atempo=0.90909,rubberband=pitch=1.25:formant=preserved` (+10 % formantes, tono total ×1,375).
Código reutilizable: `engine/blocktown/kidvoice.py`.

| Mezcla probada (mismo guion, speed 1.22) | wpm | F0 mediana sin efecto | con efecto ×1,375 |
|---|---|---|---|
| am_puck (referencia) | 225 | 117 Hz | — |
| A: am_puck .55 + am_liam .45 | 224 | 121 Hz | ~166 Hz |
| **B: am_puck .6 + am_echo .25 + af_heart .15 (elegida)** | 219 | 126 Hz | **186 Hz** |
| C: am_liam .5 + am_puck .3 + af_nicole .2 | 211 | 126 Hz | ~173 Hz |

Medido en la pista final: **206 wpm sobre toda la pista (220 wpm hablando)**, **F0 mediana 186 Hz** (objetivo 170-230 ✓). Sin Kokoro "pura" no llega a >170 Hz: el pitch-shift es necesario. No he podido escucharla: confirma tú que no suena "ardilla".

## Música y SFX
Música real de **Kevin MacLeod (incompetech.com), licencia CC BY 4.0** — incompetech está bloqueado desde la nube, así que se descargó del espejo github.com/dinglegames/dingle-radio. Cortada a la historia y con low-pass 5,5 kHz (para que no asomen platos/hi-hats):
- 0–15 s *Sergio's Magic Dustbin* (curioso) → 15–39 s *Club Seamus* (saltarín, montaje de trabajos) → 39–57 s *Le Grand Chase* (energía del concurso) → 57–66,5 s *Goblin Tinker Soldier Spy* (tensión) → **golpe orquestal + silencio en "Wrong."** → 70–79 s *Hillbilly Swing* (celebración) → **0,6 s de silencio total antes del giro** → golpe de cristal → *Cloud Dancer* (final brillante).

**Créditos para la descripción:** "Sergio's Magic Dustbin", "Club Seamus", "Le Grand Chase", "Goblin Tinker Soldier Spy", "Hillbilly Swing", "Cloud Dancer" — Kevin MacLeod (incompetech.com), Licensed under Creative Commons: By Attribution 4.0 — http://creativecommons.org/licenses/by/4.0/

SFX (~90 eventos, uno por acción en pantalla): CC0 de github.com/wyzowl/sfx-kit y github.com/facebookincubator/Meta-open-sound (ventana rompiéndose, ladridos, puerta, golpes, monedas, billetes, confeti, fuegos artificiales, eructo de la abuela, estingers orquestales de victoria/derrota, whooshes). Público (vítores, risas, "ooh", aplausos): sintetizado superponiendo 12 voces Kokoro + palmadas CC0 (`engine/blocktown/crowd_sfx.py`), porque OpenGameArt/Freesound están bloqueados. Sin ticks, relojes, hi-hats, pitidos, dings ni arpegios.

Niveles medidos: **mezcla final −14,0 LUFS integrado**, voz ≈ −14,6 LUFS, **cama musical ≈ −22,5 LUFS**, SFX ≈ −22,4 LUFS, LRA 1,6 LU.

## Imagen
Kit Blocktown (Blender 5.0 headless, Cycles 432x768, 10 muestras + denoise, 15 fps → 30 fps, escalado a 1080x1920 + sharpen). Novedad reutilizable en `engine/blocktown/lib.py`: `Char(..., cartoon=True, blush=True)` = ojos grandes blancos con pupila y brillo, cejas gruesas, mejillas rosas. Pueblo soleado (calle, puesto de limonada, pastelería, casa de la abuela, ayuntamiento con torre del reloj y ventanas que se rompen) + escenario de concurso nocturno en la plaza (pantallas de neón, atriles con pulsador, cámaras de TV, confeti, fuegos artificiales). Reparto fijo: héroe (sudadera amarilla), Benny, panadero, abuela, **el alcalde con banda y chistera**, Mrs. Pickles (nueva). Subtítulos: **una palabra cada vez, todas las palabras, Fredoka Bold amarillo #F5F542 con contorno negro grueso al 70 % de la altura**; contador de dinero/días arriba. Vela Oddwick real (`brand/oddwick_avatar.png`) se enciende en el primer segundo y las dos velas A/B se apagan (humo) en el último fotograma. Scripts: `engine/blocktown/window_shots.py`, `window_post.py`.

## Control de calidad
| Prueba | Resultado |
|---|---|
| Duración > 60 s (75-100) | 87,7 s ✓ |
| Gancho sin sonido en 1 s | ✓ texto arriba "I BROKE IT. NOW I OWE $1,000" desde el fotograma 0 + pelota rompiendo la ventana a 0,8 s |
| Plano nuevo cada 1-2 s | 51 planos, **media 1,72 s**; 8 planos de 2,3-3,4 s (todos con cámara en movimiento) — ~ok |
| Giro en los últimos 5 s | ✓ ventana 38 a 80,3 s, "the Mayor owes me a thousand dollars" ~85-86 s, A/B al final |
| wpm / tono | 206 wpm (220 hablando) ✓ / 186 Hz ✓ |
| Sonoridad | −14,0 LUFS integrado ✓, cama −22,5 LUFS ✓ |
| shot-qc | **score 80, pass** (sin congelados ni negros; flags: "cuts" = por diseño, "clipping" = neón/cielo/subtítulos con blanco puro). La versión sin sharpen daba 70 con flag "soft"; corregido. |

## Qué mejoraría
1. **Escuchar la voz**: el pitch-shift puede sonar algo artificial; si es así, bajar a ×1,3 (≈170 Hz) o probar Chatterbox con una voz de referencia joven en Colab.
2. Más reacciones en primer plano y bocas sincronizadas con las sílabas (ahora abren/cierran a ritmo fijo).
3. Partir los 8 planos de >2,2 s en dos (p. ej. perros, cartel, final).
4. Bajar un poco las luces del escenario de neón (flag de clipping) y renderizar a 540x960 si hay tiempo (render actual ≈ 85 min).
5. Público real: grabaciones CC0 de vítores/risas (OpenGameArt está bloqueado desde la nube; el sintetizado funciona pero es mejorable).
6. Animar las cuerdas de los 6 perros y los pasteles volando con más detalle.
