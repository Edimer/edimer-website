"""Descarga una presentación publicada (quarto.pub, GitHub Pages, RPubs...) a static/slides/<slug>/.

Uso (desde la raíz del sitio):

    python scripts/respaldar_slides.py https://edimer.quarto.pub/productos-de-datos-2025/ productos-de-datos-unal-palmira-2025

Descarga el HTML como index.html y, recursivamente, todo recurso local que referencie:
src/href/data-src/data-background-image, url(...) de CSS, imágenes markdown de
xaringan (![](...)) y los archivos que los plugins de reveal.js cargan en tiempo de
ejecución. Los scripts de remark.js (xaringan) se guardan localmente para no depender
de remarkjs.com. Las páginas de RPubs se resuelven al documento real (el iframe).

Al final reduce las imágenes muy grandes (máximo 1920 px, JPEG calidad 85), conservando
nombre y formato para no romper las referencias, e imprime los recursos que no se
pudieron descargar. Para optimizar una carpeta ya existente:

    python scripts/respaldar_slides.py --optimizar static/slides/<slug>
"""

import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path

SITIO = Path(__file__).resolve().parent.parent
AGENTE = {"User-Agent": "Mozilla/5.0 (respaldo de slides de edimer.netlify.app)"}

REF_HTML = re.compile(
    r"""(?:src|href|data-src|data-background-image|data-background-video|poster)\s*=\s*["']([^"']+)["']"""
    r"""|url\(\s*["']?([^)"']+)["']?\s*\)"""
    r"""|!\[[^\]]*\]\(\s*([^)\s]+)"""
)
REF_CSS = re.compile(r"""url\(\s*["']?([^)"']+)["']?\s*\)|@import\s*["']([^"']+)["']""")
# Rutas que los plugins (chalkboard, menu, notes...) arman en tiempo de ejecución.
REF_JS = re.compile(
    r"""["']([\w./-]+\.(?:png|svg|cur|gif|jpg|css|html|woff2?|ttf))["']"""
    r"""|((?:img|images|fonts?)/[\w.-]+\.(?:png|svg|cur|gif|jpg))"""
)
EXTERNO = re.compile(r"^(?:[a-z]+:|//|#)", re.I)
REMARK = "https://remarkjs.com/downloads/remark-latest.min.js"
# polyfill.io fue comprometido en 2024; lo quitamos de las copias.
POLYFILL = re.compile(r'<script[^>]+src="https?://(?:cdn\.)?polyfill\.io/[^"]*"[^>]*>\s*</script>\s*')


def localizar_externos(texto, destino):
    """Guarda remark.js junto a las slides y quita scripts externos riesgosos. Devuelve el HTML ajustado."""
    if REMARK in texto:
        (Path(destino) / "remark-latest.min.js").write_bytes(bajar(REMARK)[0])
        texto = texto.replace(REMARK, "remark-latest.min.js")
    return POLYFILL.sub("", texto)


def guardar_html(texto, archivo):
    """Escribe sin traducir saltos de línea (write_text en Windows duplicaría los retornos de carro)."""
    Path(archivo).write_bytes(texto.encode("utf-8"))


def bajar(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE), timeout=60) as r:
        return r.read(), r.geturl()


def resolver_rpubs(url):
    """rpubs.com/<usuario>/<id> envuelve el documento en un iframe; devolvemos el documento real."""
    html, _ = bajar(url)
    m = re.search(r'<iframe[^>]+src="([^"]+)"', html.decode("utf-8", "ignore"))
    if not m:
        sys.exit("No encontré el iframe del documento en RPubs.")
    return urllib.parse.urljoin(url, m.group(1).replace("&amp;", "&"))


def limpiar(ref):
    return ref.split("#")[0].split("?")[0].strip()


def optimizar_imagenes(carpeta, lado_max=1920, umbral=300_000):
    """Recomprime JPG/PNG pesados sin cambiar su nombre ni formato. Requiere Pillow."""
    try:
        from PIL import Image
    except ImportError:
        print("  (Pillow no está instalado: no se optimizan imágenes)")
        return
    ahorro = 0
    for f in Path(carpeta).rglob("*"):
        ext = f.suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png") or f.stat().st_size < umbral:
            continue
        antes = f.stat().st_size
        im = Image.open(f)
        im.load()
        if max(im.size) > lado_max:
            im.thumbnail((lado_max, lado_max))
        tmp = f.with_name(f.name + ".tmp")
        if ext == ".png":
            im.save(tmp, format="PNG", optimize=True)
        else:
            im.convert("RGB").save(tmp, format="JPEG", quality=85, optimize=True, progressive=True)
        if tmp.stat().st_size < antes:
            tmp.replace(f)
            ahorro += antes - f.stat().st_size
        else:
            tmp.unlink()
    print(f"  imágenes optimizadas: {ahorro / 1e6:.1f} MB menos")


def respaldar(url, slug):
    if "rpubs.com/" in url:
        url = resolver_rpubs(url)
    if not urllib.parse.urlparse(url).path.rsplit("/", 1)[-1].count("."):
        url = url.rstrip("/") + "/"
    destino = SITIO / "static" / "slides" / slug
    destino.mkdir(parents=True, exist_ok=True)

    html, url_final = bajar(url)
    base = url_final if url_final.endswith("/") else url_final.rsplit("/", 1)[0] + "/"
    texto = html.decode("utf-8", "ignore")
    texto = localizar_externos(texto, destino)
    guardar_html(texto, destino / "index.html")

    pendientes = deque((limpiar(next(g for g in m.groups() if g)), base) for m in REF_HTML.finditer(texto))
    vistos, fallidos, opcionales = set(), [], set()
    while pendientes:
        ref, desde = pendientes.popleft()
        if not ref or EXTERNO.match(ref) or ref.startswith("/"):
            continue
        abs_url = urllib.parse.urljoin(desde, urllib.parse.quote(urllib.parse.unquote(ref), safe="/.-_~%"))
        if not abs_url.startswith(base) or abs_url in vistos:
            continue
        vistos.add(abs_url)
        relativo = urllib.parse.unquote(abs_url[len(base):])
        if not relativo or relativo.endswith("/"):
            continue
        try:
            datos, _ = bajar(abs_url)
        except urllib.error.HTTPError as e:
            if abs_url not in opcionales:
                fallidos.append(f"{e.code} {relativo}")
            continue
        archivo = destino / relativo
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_bytes(datos)
        carpeta = abs_url.rsplit("/", 1)[0] + "/"
        if relativo.endswith(".css"):
            for m in REF_CSS.finditer(datos.decode("utf-8", "ignore")):
                pendientes.append((limpiar(m.group(1) or m.group(2)), carpeta))
        elif relativo.endswith(".js") and "/plugin/" in relativo:
            # Probamos cada ruta relativa al archivo y a su carpeta padre; las que no existan se ignoran.
            for m in REF_JS.finditer(datos.decode("utf-8", "ignore")):
                ref = m.group(1) or m.group(2)
                for raiz in (carpeta, carpeta.rsplit("/", 2)[0] + "/"):
                    opcionales.add(urllib.parse.urljoin(raiz, ref))
                    pendientes.append((ref, raiz))
    optimizar_imagenes(destino)
    tam = sum(f.stat().st_size for f in destino.rglob("*") if f.is_file()) / 1e6
    print(f"{slug}: {len(vistos)} recursos revisados, {tam:.1f} MB en static/slides/{slug}/")
    for f in fallidos:
        print("  no descargado:", f)
    return f"/slides/{slug}/index.html"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 3 and sys.argv[1] == "--optimizar":
        optimizar_imagenes(sys.argv[2])
    elif len(sys.argv) == 3:
        print(respaldar(sys.argv[1], sys.argv[2]))
    else:
        sys.exit(__doc__)
