"""Crea (o aloja) una charla en el sitio a partir de una carpeta de D:/Github/charlas-eventos.

Uso típico (desde la raíz del sitio):

    python scripts/nueva_charla.py D:/Github/charlas-eventos/charla-unal-palmira-mayo-2026

Qué hace:
  1. Lee el YAML del .qmd/.Rmd principal (title, subtitle, date) y la URL de
     quarto.pub desde _publish.yml.
  2. Crea content/es/event/<slug>/index.md y content/en/event/<slug>/index.md
     con el mismo formato del resto de charlas (campos en inglés marcados con TODO).
  3. Copia una imagen de portada como featured.<ext> en ambos bundles.
  4. Con --alojar, copia el HTML renderizado y sus recursos locales a
     static/slides/<slug>/ y usa esa ruta como url_slides (útil cuando la charla
     no está publicada en quarto.pub).

Opciones:
  --slug SLUG          slug de la URL (/talk/SLUG/). Por defecto, el nombre de la carpeta
                       sin el prefijo "charla-".
  --fuente ARCHIVO     .qmd/.Rmd principal si la carpeta tiene varios.
  --imagen RUTA        imagen de portada (png/jpg/webp). Si no se da, se intenta
                       images/logo.png o img/logo*.png.
  --evento TEXTO       nombre del evento/institución (por defecto el footer del .qmd).
  --fecha AAAA-MM-DD   fecha de la charla (por defecto la del YAML; si es "today",
                       se estima desde el HTML renderizado y se avisa).
  --ciudad TEXTO / --region TEXTO
  --alojar             copiar las slides renderizadas a static/slides/<slug>/.
  --solo-alojar        solo copiar las slides (no crea ni toca los index.md).
  --forzar             sobrescribir index.md existentes.

Requiere PyYAML (pip install pyyaml). Pillow es opcional (convierte webp a png y
reduce imágenes grandes).
"""

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Falta PyYAML: pip install pyyaml")

SITIO = Path(__file__).resolve().parent.parent
MAX_LADO_IMAGEN = 1600


def leer_yaml_frontmatter(ruta):
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def elegir_fuente(carpeta, fuente):
    if fuente:
        return Path(fuente)
    candidatos = [
        p for p in list(carpeta.glob("*.qmd")) + list(carpeta.glob("*.Rmd"))
        if "borrador" not in p.name
    ]
    if not candidatos:
        candidatos = list(carpeta.glob("slides/*.qmd")) + list(carpeta.glob("diapositivas/*.Rmd"))
    if len(candidatos) != 1:
        nombres = ", ".join(p.name for p in candidatos) or "ninguno"
        sys.exit(f"No pude decidir el archivo principal ({nombres}). Usa --fuente.")
    return candidatos[0]


def url_quarto_pub(carpeta, fuente):
    publish = carpeta / "_publish.yml"
    if not publish.exists():
        publish = fuente.parent / "_publish.yml"
    if not publish.exists():
        return ""
    for entrada in yaml.safe_load(publish.read_text(encoding="utf-8")) or []:
        if entrada.get("source") == fuente.name:
            sitios = entrada.get("quarto-pub") or []
            if sitios:
                return sitios[0]["url"].rstrip("/") + "/"
    return ""


def fecha_charla(meta, fuente):
    """Devuelve (fecha, exacta). Usa la fecha del YAML; si es 'today', la estima desde el HTML renderizado."""
    fecha = str(meta.get("date", "")).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        return fecha, True
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", fecha):  # formato DD-MM-AAAA de xaringan
        d, m, a = fecha.split("-")
        return f"{a}-{m}-{d}", True
    html = fuente.with_suffix(".html")
    if html.exists():
        m = re.search(r'<p class="date">(\d{4}-\d{2}-\d{2})', html.read_text(encoding="utf-8", errors="ignore"))
        if m:
            return m.group(1), False
        return dt.date.fromtimestamp(html.stat().st_mtime).isoformat(), False
    return dt.date.today().isoformat(), False


def copiar_imagen(origen, destinos):
    origen = Path(origen)
    try:
        from PIL import Image

        im = Image.open(origen)
        im.thumbnail((MAX_LADO_IMAGEN, MAX_LADO_IMAGEN))
        ext = ".jpg" if origen.suffix.lower() in (".jpg", ".jpeg") else ".png"
        for d in destinos:
            salida = d / f"featured{ext}"
            (im.convert("RGB") if ext == ".jpg" else im).save(salida)
    except ImportError:
        for d in destinos:
            shutil.copy2(origen, d / f"featured{origen.suffix.lower()}")


REF_LOCAL = re.compile(
    r"""(?:src|href|data-background-image|data-src)\s*=\s*["']([^"'#?]+)["']"""
    r"""|url\(\s*["']?([^)"'#?]+)["']?\s*\)"""
    r"""|!\[[^\]]*\]\(([^)\s]+)\)"""
)


def alojar_slides(html, slug):
    """Copia el HTML renderizado y los recursos locales que referencia a static/slides/<slug>/."""
    html = Path(html)
    destino = SITIO / "static" / "slides" / slug
    destino.mkdir(parents=True, exist_ok=True)
    shutil.copy2(html, destino / "index.html")
    texto = html.read_text(encoding="utf-8", errors="ignore")
    copiados = set()
    for m in REF_LOCAL.finditer(texto):
        ref = next(g for g in m.groups() if g)
        if re.match(r"^(https?:|data:|mailto:|//|#)", ref):
            continue
        partes = Path(ref).parts
        # Las carpetas de librerías (index_files/, libs/, *_files/) se copian completas.
        if partes and (partes[0] in ("libs",) or partes[0].endswith("_files")):
            raiz = html.parent / partes[0]
            if partes[0] not in copiados and raiz.is_dir():
                shutil.copytree(raiz, destino / partes[0], dirs_exist_ok=True)
                copiados.add(partes[0])
            continue
        archivo = html.parent / ref
        if archivo.is_file():
            (destino / ref).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archivo, destino / ref)
    # Hojas de estilo locales que xaringan referencia sin ruta (p.ej. mtheme_max.css).
    for css in html.parent.glob("*.css"):
        if css.name in texto:
            shutil.copy2(css, destino / css.name)
    return f"/slides/{slug}/index.html"


PLANTILLA = """---
title: {title}
slug: {slug}
event: {event}
event_url: {event_url}
location: {location}
address:
  street: ""
  city: {city}
  region: {region}
  postcode: ""
  country: Colombia
summary: {summary}
abstract: {abstract}
date: "{date}T08:00:00Z"
date_end: "{date}T12:00:00Z"
all_day: true
publishDate: "{date}T12:00:00Z"
authors: []
tags: {tags}
featured: false
image:
  caption: ""
  focal_point: Center
  preview_only: false
links: []
url_slides: {url_slides}
url_code: ""
url_pdf: ""
url_video: ""
slides: ""
projects: []
---
"""


def q(texto):
    """Cadena YAML entre comillas dobles."""
    return '"' + str(texto).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("carpeta")
    p.add_argument("--slug")
    p.add_argument("--fuente")
    p.add_argument("--imagen")
    p.add_argument("--evento", default="")
    p.add_argument("--ciudad", default="")
    p.add_argument("--region", default="")
    p.add_argument("--fecha")
    p.add_argument("--alojar", action="store_true")
    p.add_argument("--solo-alojar", action="store_true")
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()

    carpeta = Path(a.carpeta)
    fuente = elegir_fuente(carpeta, a.fuente)
    slug = a.slug or re.sub(r"^charla-", "", carpeta.name).lower()

    if a.solo_alojar:
        print(alojar_slides(fuente.with_suffix(".html"), slug))
        return

    meta = leer_yaml_frontmatter(fuente)
    titulo = str(meta.get("title", "")).strip().rstrip(":")
    subtitulo = str(meta.get("subtitle") or "").strip()
    if subtitulo and ":" not in titulo:
        titulo = f"{titulo}: {subtitulo[0].lower()}{subtitulo[1:]}"
    if a.fecha:
        fecha, exacta = a.fecha, True
    else:
        fecha, exacta = fecha_charla(meta, fuente)
    if not exacta:
        print(f"Aviso: el .qmd no tiene fecha fija; estimé {fecha} desde el HTML renderizado. Corrígela con --fecha si no es la del evento.")
    footer = str(((meta.get("format") or {}).get("revealjs") or {}).get("footer", ""))
    # Algunos footers solo traen el nombre del autor (con enlace); esos no sirven como evento.
    if "[" in footer or "Edimer" in footer:
        footer = ""
    evento = a.evento or re.sub(r"\s*[|·].*$", "", footer) or "TODO evento"

    url_slides = url_quarto_pub(carpeta, fuente)
    if re.search(r"[()\s]", url_slides):
        print("Aviso: la URL de las slides tiene paréntesis o espacios; Hugo los codifica y quarto.pub "
              "puede responder 404. Agrega una redirección /go/<nombre> en static/_redirects y úsala en url_slides.")
    if a.alojar or not url_slides:
        if fuente.with_suffix(".html").exists():
            url_slides = alojar_slides(fuente.with_suffix(".html"), slug)
        else:
            print("Aviso: no hay quarto.pub ni HTML renderizado; url_slides queda vacío.")

    bundles = []
    for idioma in ("es", "en"):
        bundle = SITIO / "content" / idioma / "event" / slug
        indice = bundle / "index.md"
        if indice.exists() and not a.forzar:
            sys.exit(f"Ya existe {indice}. Usa --forzar para sobrescribir.")
        bundle.mkdir(parents=True, exist_ok=True)
        es = idioma == "es"
        indice.write_text(PLANTILLA.format(
            title=q(titulo if es else f"TODO (EN): {titulo}"),
            slug=slug,
            event=q(evento),
            event_url=q(""),
            location=q(evento),
            city=q(a.ciudad),
            region=q(a.region),
            summary=q("TODO: resumen de una oración" if es else "TODO: one-sentence summary"),
            abstract=q("TODO: resumen de 2-4 oraciones" if es else "TODO: 2-4 sentence abstract"),
            date=fecha,
            tags="[]",
            url_slides=q(url_slides),
        ), encoding="utf-8")
        bundles.append(bundle)

    imagen = a.imagen
    if not imagen:
        for patron in ("images/logo.png", "img/logo*.png", "slides/images/png-converted/logo.png"):
            encontrados = sorted(carpeta.glob(patron))
            if encontrados:
                imagen = encontrados[0]
                break
    if imagen:
        copiar_imagen(imagen, bundles)
    else:
        print("Aviso: no encontré imagen de portada; agrega featured.png a ambos bundles.")

    print(f"Charla creada: content/{{es,en}}/event/{slug}/  (fecha {fecha}, slides {url_slides or '—'})")
    print("Siguiente paso: completa summary, abstract, tags y la versión en inglés; luego revisa con `hugo server`.")


if __name__ == "__main__":
    main()
