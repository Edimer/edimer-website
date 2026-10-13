# edimer-website

Sitio personal de Edimer David Jaramillo (<https://edimer.netlify.app>), construido con Hugo 0.119 + Wowchemy (tema *starter-hugo-academic*) y publicado en Netlify. Es bilingüe: el contenido en español está en `content/es/` y el inglés en `content/en/`.

## Charlas

Cada charla es una carpeta (page bundle) con el mismo nombre en ambos idiomas:

```
content/es/event/<slug>/index.md   + featured.png
content/en/event/<slug>/index.md   + featured.png
```

La página queda en `/es/talk/<slug>/` y `/en/talk/<slug>/` (el `slug:` del front matter fija la URL). El inicio muestra las 6 charlas más recientes con el enlace "Ver todas las charlas"; la lista completa, agrupada por año, está en `/es/event/`.

Las charlas se construyen en `D:/Github/charlas-eventos` (Quarto + RevealJS). **Todas las diapositivas se alojan en este sitio**, en `static/slides/<slug>/`, y las fichas enlazan a `/slides/<slug>/index.html`. Así no dependen de servicios externos: Posit deja de permitir publicar en quarto.pub el 31 de diciembre de 2026 (lo ya publicado sigue en línea hasta el 31 de diciembre de 2031), y RPubs deja de publicar el 30 de junio de 2027.

### Agregar una charla nueva

1. Renderizar la charla en su carpeta de `charlas-eventos` (`quarto render`).
2. Desde la raíz de este sitio:

   ```bash
   python scripts/nueva_charla.py D:/Github/charlas-eventos/<carpeta-de-la-charla>
   ```

   El script lee título, subtítulo y fecha del `.qmd`, copia el HTML renderizado con sus librerías e imágenes a `static/slides/<slug>/` (y reduce las imágenes muy pesadas), crea los dos `index.md` y copia la portada (`images/logo.png` por defecto, o la que indiques con `--imagen`). Si la charla no está renderizada pero sí publicada en quarto.pub, descarga la versión publicada.

   Opciones útiles:
   - `--slug`
   - `--fuente`, si hay varios `.qmd`
   - `--fecha`, si el `.qmd` dice `date: today`
   - `--evento`, `--ciudad`, `--region`
   - `--externo`, para enlazar quarto.pub en vez de alojar
3. Completar en ambos `index.md`: `summary`, `abstract`, `tags`, `event_url` y la traducción al inglés (los campos pendientes dicen `TODO`).
4. Revisar con `hugo server` y hacer commit.

Sin el script: `hugo new --kind event content/es/event/<slug>` (y lo mismo con `en`) usa la plantilla `archetypes/event/index.md`.

### Respaldar una presentación ya publicada

Para traer al sitio cualquier presentación o documento publicado (quarto.pub, GitHub Pages, RPubs):

```bash
python scripts/respaldar_slides.py <url-publicada> <slug>
```

Descarga el HTML y todos los recursos que usa (librerías de reveal.js, imágenes, fuentes, remark.js de xaringan) a `static/slides/<slug>/`. Para RPubs resuelve el documento real dentro del iframe. Los PDF van en `static/uploads/charlas/` y se enlazan con `url_pdf: /uploads/charlas/<archivo>.pdf`.

### Convenciones

- Títulos en español con mayúscula solo en la primera palabra (salvo nombres propios y siglas), con dos puntos para el subtítulo.
- La versión `es` va en español y la `en` en inglés, incluidas las etiquetas (`tags`), que generan páginas por idioma.
- Si cambias el `slug` de una charla ya publicada, agrega una línea en `static/_redirects` (`/es/talk/<viejo>/  /es/talk/<nuevo>/  301`, y lo mismo para `/en/`). No uses `aliases:`: con el sitio multilingüe, Netlify no lee los `_redirects` que genera el tema dentro de `/es/` y `/en/`.
- Botones extra (tableros, ejemplos, guías) van en `links:` con `name`, `url`, `icon_pack` e `icon`.
