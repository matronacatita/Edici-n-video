"""Render de video Matrona Catita a partir de un plan.json.

Uso: python3 render.py plan.json toma.mp4 logo.mov salida_dir [--hoja]
Genera Matrona_<tema>_vN.mp4 (con subtítulos) y ..._sin_subtitulos.mp4.
"""
import json, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

plan_path, toma, logo, outdir = sys.argv[1:5]
HOJA = '--hoja' in sys.argv
VERSION = next((a[2:] for a in sys.argv if re.fullmatch(r'-v\d+', a)), '1')
P = json.load(open(plan_path))
base = os.path.dirname(os.path.abspath(plan_path))
repo = os.path.dirname(os.path.dirname(base))
FPS = P['fps']; W, H = P['size']
os.makedirs(outdir, exist_ok=True)
tmp = os.path.join(outdir, '_tmp'); os.makedirs(tmp, exist_ok=True)

# ---------- línea de tiempo ----------
segs = [(round(a * FPS), round(b * FPS)) for a, b in P['segments']]
starts = np.cumsum([0] + [b - a for a, b in segs])  # en cuadros de salida
NBODY = int(starts[-1])


def s2o(t):
    """tiempo de la toma -> tiempo de salida (s)."""
    f = t * FPS
    for (a, b), o in zip(segs, starts):
        if f < a: return o / FPS
        if f < b: return (o + f - a) / FPS
    return NBODY / FPS


# ---------- audio ----------
def build_audio():
    raw = os.path.join(tmp, 'raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', toma, '-ac', '1', '-ar', '48000', raw], check=True)
    a, sr = sf.read(raw, dtype='float32')
    fade = int(0.008 * sr); ramp = np.linspace(0, 1, fade, dtype='float32')
    parts = []
    for fa, fb in segs:
        x = a[int(fa * sr / FPS):int(fb * sr / FPS)].copy()
        n = (fb - fa) * sr // FPS
        x = np.pad(x, (0, max(0, n - len(x))))[:n]
        x[:fade] *= ramp; x[-fade:] *= ramp[::-1]
        parts.append(x)
    cut = os.path.join(tmp, 'cut.wav'); sf.write(cut, np.concatenate(parts), sr)
    pre = 'highpass=f=70,afftdn=nr=6:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1'
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', cut, '-af', pre + ',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    out = os.path.join(tmp, 'final.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cut, '-af',
                    f"{pre},{ln},apad=pad_dur={P['cierre']['dur']}", '-ar', '48000', out], check=True)
    return out


# ---------- subtítulos ----------
S = P['subs']
font_path = os.path.join(repo, S['font'])


def groups():
    ws = [(w, t) for w, t in P['words'] if S['desde'] <= t < S['hasta']]
    phrases, cur = [], []
    for i, (w, t) in enumerate(ws):
        cur.append(i)
        if w[-1] in '.,:;?!' or i == len(ws) - 1:
            phrases.append(cur); cur = []
    out = []
    for ph in phrases:
        k = -(-len(ph) // 3)
        for c in np.array_split(ph, k):
            out.append([int(i) for i in c])
    res = []
    for gi, g in enumerate(out):
        t0 = s2o(ws[g[0]][1])
        nxt = s2o(ws[out[gi + 1][0]][1]) if gi + 1 < len(out) else None
        last = s2o(ws[g[-1]][1])
        t1 = min(nxt, last + 0.9) if nxt is not None else last + 0.7
        res.append(dict(words=[ws[i][0] for i in g], t=[s2o(ws[i][1]) for i in g], t0=t0, t1=t1))
    return res


_cache = {}


def sub_layer(words, active):
    key = (tuple(words), active)
    if key in _cache: return _cache[key]
    size = S['size']
    while True:
        f = ImageFont.truetype(font_path, size)
        sp = f.getlength(' ')
        widths = [f.getlength(w) for w in words]
        tw = sum(widths) + sp * (len(words) - 1)
        if tw <= S['max_w'] or size <= S['min_size']: break
        size -= 2
    pad = 60; hh = int(size * 1.5) + 2 * pad
    mask = Image.new('L', (W, hh), 0); col = Image.new('RGBA', (W, hh), (0, 0, 0, 0))
    dm, dc = ImageDraw.Draw(mask), ImageDraw.Draw(col)
    x = S['x'] - tw / 2
    for i, w in enumerate(words):
        dm.text((x, hh // 2), w, font=f, fill=255, anchor='lm')
        dc.text((x, hh // 2), w, font=f, fill=S['activo'] if i == active else S['color'], anchor='lm')
        x += widths[i] + sp
    lay = Image.new('RGBA', (W, hh), (0, 0, 0, 0))
    for blur, op in ((13, 0.78), (3, 0.85)):
        sh = mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, int(v * 1.6 * op)))
        lay = Image.alpha_composite(lay, Image.merge('RGBA', [Image.new('L', (W, hh), 0)] * 3 + [sh]))
    lay = Image.alpha_composite(lay, col)
    _cache[key] = (lay, S['y'] - hh // 2)
    return _cache[key]


G = groups()


def draw_subs(img, t):
    for g in G:
        if g['t0'] <= t < g['t1']:
            act = max(i for i, x in enumerate(g['t']) if x <= t + 1e-6)
            lay, y = sub_layer(g['words'], act)
            a = min(1.0, (t - g['t0'] + 1 / FPS) / 0.11)
            if a < 1:
                lay = lay.copy(); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
            img.paste(lay, (0, y), lay)
            return


# ---------- tarjetas ----------
cards = []
for c in P['cards']:
    x0, y0, x1, y1 = c['rect']
    im = Image.open(os.path.join(base, c['file'])).convert('RGBA').resize((x1 - x0, y1 - y0), Image.LANCZOS)
    cards.append(dict(im=im, x=x0, y=y0, t0=s2o(c['entra']), t1=s2o(c['sale'])))
for a, b in zip(cards, cards[1:]):
    if 0 <= b['t0'] - a['t1'] < 0.2: a['t1'] = b['t0'] + 0.45  # seguidas: la siguiente funde encima


def draw_cards(img, t):
    """Entrada dinámica: sube desde abajo, crece con rebote y funde (0,45 s)."""
    for c in cards:
        if c['t0'] <= t < c['t1']:
            p = min(1.0, (t - c['t0'] + 1 / FPS) / 0.45)
            im = c['im']
            if p < 1:
                k = 1.70158 * 1.4; q = p - 1
                e = 1 + (k + 1) * q ** 3 + k * q ** 2          # easeOutBack (rebote)
                sc = 0.72 + 0.28 * e
                w, h = im.size; nw, nh = int(w * sc), int(h * sc)
                im = im.resize((nw, nh), Image.BILINEAR)
                im.putalpha(int(255 * min(1.0, p * 2.5)))
                img.paste(im, (c['x'] + (w - nw) // 2, c['y'] + (h - nh) // 2 + int(140 * (1 - e))), im)
            else:
                img.paste(im, (c['x'], c['y']), im)


# ---------- retoques ----------
MANCHA = None
if P.get('mancha'):
    import cv2
    tr = json.load(open(os.path.join(base, P['mancha'])))
    idx = [i for i, v in enumerate(tr) if v]
    MANCHA = np.stack([np.interp(range(len(tr)), idx, [tr[i][k] for i in idx]) for k in (0, 1)], 1).astype(int)


def quitar_mancha(buf, n):
    """Borra los pixeles claros cerca de la posición rastreada (inpaint local)."""
    arr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    x, y = MANCHA[min(n, len(MANCHA) - 1)]; r = 44
    y0, y1, x0, x1 = max(0, y - r), min(H, y + r), max(0, x - r), min(W, x + r)
    roi = arr[y0:y1, x0:x1]
    g = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY).astype(np.float32)
    d = cv2.GaussianBlur(g, (0, 0), 1.2) - cv2.medianBlur(cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY), 31).astype(np.float32)
    m = (d > 4).astype(np.uint8)
    yy, xx = np.ogrid[:y1 - y0, :x1 - x0]
    m[(yy - (y - y0)) ** 2 + (xx - (x - x0)) ** 2 > 18 ** 2] = 0
    if m.any():
        m = cv2.dilate(m, np.ones((7, 7), np.uint8))
        arr[y0:y1, x0:x1] = cv2.inpaint(roi, m, 4, cv2.INPAINT_TELEA)
    return arr.tobytes()


# ---------- cuerpo ----------
ax, ay = P['face']


def zoomed(frame, si, k):
    a, b = segs[si]
    z = P['zoom'][si % 2] * (1 + P['drift'] * k / max(1, b - a - 1))
    if z == 1: return frame
    w, h = W / z, H / z
    x0, y0 = ax * (1 - 1 / z), ay * (1 - 1 / z)
    return frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))


def body_frames():
    """Genera (n_salida, PIL frame con zoom) leyendo la toma en orden."""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', toma, '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = 0; si = 0; out = 0; last = None
    while si < len(segs):
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:  # fin de la toma: repetir último cuadro
            if out >= NBODY: break
            buf = last
        if MANCHA is not None and len(buf) == W * H * 3 and buf is not last: buf = quitar_mancha(buf, n)
        last = buf
        a, b = segs[si]
        if n >= a:
            yield out, zoomed(Image.frombuffer('RGB', (W, H), buf), si, n - a)
            out += 1
        n += 1
        if n >= b: si += 1
    p.kill()


# ---------- cierre ----------
def cierre_frames():
    C = P['cierre']; n = round(C['dur'] * FPS)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(C['src_inicio']), '-i', logo, '-vf', f"setpts=PTS/{C.get('velocidad', 1)},fps={FPS}",
                        '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                         '-of', 'csv=p=0', logo], capture_output=True, text=True)
    sw, sh = map(int, pr.stdout.strip().split(','))
    fh = round(W * sh / sw); y0 = (H - fh) // 2
    feather = 140
    m = np.ones(fh, dtype='float32'); r = np.linspace(0, 1, feather) ** 2 * (3 - 2 * np.linspace(0, 1, feather))
    r = np.linspace(0, 1, feather); r = r * r * (3 - 2 * r)
    m[:feather] = r; m[-feather:] = r[::-1]
    mask = Image.fromarray((np.repeat(m[:, None], W, 1) * 255).astype('uint8'))
    for i in range(n):
        f = Image.frombuffer('RGB', (sw, sh), p.stdout[i * sw * sh * 3:(i + 1) * sw * sh * 3])
        cw = round(H * sw / sh)
        bg = f.resize((cw // 8, H // 8)).filter(ImageFilter.GaussianBlur(10)).resize((cw, H), Image.BICUBIC)
        bg = bg.crop(((cw - W) // 2, 0, (cw - W) // 2 + W, H))
        bg.paste(f.resize((W, fh), Image.LANCZOS), (0, y0), mask)
        t = i / FPS
        a = min(1.0, (t + 1 / FPS) / C['fade_in'], max(0.0, (C['dur'] - t - 1 / FPS) / C['fade_out']))
        a = a * a * (3 - 2 * a)
        if a < 1: bg = Image.blend(Image.new('RGB', (W, H), 0), bg, a)
        yield bg


# ---------- salida ----------
def encoder(path, audio):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                             '-i', '-', '-i', audio, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p',
                             '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-colorspace', 'bt709', '-color_primaries', 'bt709',
                             '-color_trc', 'bt709', '-color_range', 'tv', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                             '-movflags', '+faststart', path], stdin=subprocess.PIPE)


if HOJA:
    # hoja de fotogramas: primer cuadro tras cada corte y entradas/salidas de tarjetas
    want = {}
    for i, o in enumerate(starts[:-1]): want[int(o)] = f'corte {i}'
    for i, c in enumerate(cards):
        want[int(round(c['t0'] * FPS)) + 8] = f'D{i + 1} entra'
        want[max(0, int(round(c['t1'] * FPS)) - 2)] = f'D{i + 1} sale'
    shots = []
    for o, fr in body_frames():
        if o in want:
            fr = fr.copy(); draw_cards(fr, o / FPS); draw_subs(fr, o / FPS)
            th = fr.resize((270, 480)); ImageDraw.Draw(th).text((6, 6), f'{want[o]} {o / FPS:.2f}s', fill='yellow')
            shots.append(th)
    cf = list(cierre_frames())
    for i in (3, 10, 45, 80, 86):
        th = cf[i].resize((270, 480)); ImageDraw.Draw(th).text((6, 6), f'cierre {i / FPS:.2f}s', fill='yellow'); shots.append(th)
    per = 8
    for k in range(0, len(shots), per):
        sheet = Image.new('RGB', (270 * per, 480))
        for j, th in enumerate(shots[k:k + per]): sheet.paste(th, (270 * j, 0))
        sheet.save(os.path.join(outdir, f'hoja_{k // per + 1}.jpg'), quality=85)
    print('hojas:', -(-len(shots) // per)); sys.exit()

audio = build_audio()
name = f"Matrona_{P['tema']}_v{VERSION}"
e1 = encoder(os.path.join(outdir, name + '.mp4'), audio)
e2 = encoder(os.path.join(outdir, name + '_sin_subtitulos.mp4'), audio)
for o, fr in body_frames():
    t = o / FPS
    draw_cards(fr, t)
    e2.stdin.write(fr.tobytes())
    draw_subs(fr, t)
    e1.stdin.write(fr.tobytes())
for fr in cierre_frames():
    b = fr.tobytes(); e1.stdin.write(b); e2.stdin.write(b)
for e in (e1, e2): e.stdin.close(); e.wait()
json.dump(dict(grupos=G, cuerpo_s=NBODY / FPS), open(os.path.join(tmp, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print('ok', name, 'cuerpo', NBODY / FPS, 's')
