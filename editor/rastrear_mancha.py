"""Rastrea una mancha clara pequeña sobre la ropa y guarda su posición por cuadro.
Uso: python3 rastrear_mancha.py toma.mp4 x0 y0 x1 y1 salida.json   (ventana de búsqueda)
"""
import sys, subprocess, json, numpy as np, cv2
toma = sys.argv[1]; X0, Y0, X1, Y1 = map(int, sys.argv[2:6]); out = sys.argv[6]
w, h = X1 - X0, Y1 - Y0


def frames():
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', toma, '-vf', f'fps=30,crop={w}:{h}:{X0}:{Y0}', '-f', 'rawvideo',
                          '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(w * h * 3)
        if len(b) < w * h * 3: return
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def contrast(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.medianBlur(im, 31); bgg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY).astype(np.float32)
    d = cv2.GaussianBlur(g - bgg, (0, 0), 1.5)
    hsv = cv2.cvtColor(bg, cv2.COLOR_BGR2HSV)
    d[~((hsv[..., 1] < 70) & (bgg > 60) & (bgg < 150))] = 0   # solo sobre tela gris
    return d


D = [contrast(f) for f in frames()]
N = len(D)
det = np.full((N, 2), np.nan)
for i, d in enumerate(D):
    y, x = np.unravel_index(np.argmax(d), d.shape)
    if d[y, x] > 20: det[i] = (x, y)
# trayectoria suave: mediana global -> mediana móvil de detecciones cercanas
med = np.nanmedian(det, 0)
ok = np.abs(det - med).max(1) < 45
det[~ok] = np.nan
traj = np.zeros((N, 2))
for i in range(N):
    a = det[max(0, i - 45):i + 46]; a = a[~np.isnan(a[:, 0])]
    traj[i] = np.median(a, 0) if len(a) >= 5 else med
res = []
for i, d in enumerate(D):
    x, y = traj[i].astype(int); r = 14
    sub = d[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1]
    yy, xx = np.unravel_index(np.argmax(sub), sub.shape)
    if sub[yy, xx] > 10: res.append([int(max(0, x - r) + xx + X0), int(max(0, y - r) + yy + Y0)])
    else: res.append(None)
json.dump(res, open(out, 'w'))
print(N, 'cuadros; mancha visible en', sum(r is not None for r in res))
