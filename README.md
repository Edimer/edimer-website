# edimer-website

Sitio personal de Edimer David Jaramillo (<https://edimer.netlify.app>), construido con Hugo 0.119 + Wowchemy (tema *starter-hugo-academic*) y publicado en Netlify. Es bilingüe: el contenido en español está en `content/es/` y el inglés en `content/en/`.

## Charlas

Cada charla es una carpeta (page bundle) con el mismo nombre en ambos idiomas:

```
content/es/event/<slug>/index.md   + featured.png
content/en/event/<slug>/index.md   + featured.png
```

La página queda en `/es/talk/<slug>/` y `/en/talk/<slug>/` (el `slug:` del front matter fija la URL). El inicio muestra las 6 charlas más recientes con el enlace "Ver todas las charlas"; la lista completa, agrupada por año, está en `/es/event/`.

Las charlas se construyen en `D:/Github/charlas-eventos` (Quarto + RevealJS) y se publican en <https://edimer.quarto.pub/>.

### Agregar una charla nueva

1. Publicar las slides desde su carpeta en `charlas-eventos` (`quarto publish quarto-pub`), lo que deja la URL en `_publish.yml`.
2. Desde la raíz de este sitio:

   ```bash
   python scripts/nueva_charla.py D:/Github/charlas-eventos/<carpeta-de-la-charla>
   ```

   El script lee título, subtítulo y fecha del `.qmd`, toma la URL de `_publish.yml`, crea los dos `index.md` y copia la portada (`images/logo.png` por defecto, o la que indiques con `--imagen`). Opciones útiles: `--slug`, `--fuente` (si hay varios `.qmd`), `--fecha` (si el `.qmd` dice `date: today`), `--evento`, `--ciudad`, `--region`.
3. Completar en ambos `index.md`: `summary`, `abstract`, `tags`, `event_url` y la traducción al inglés (los campos pendientes dicen `TODO`).
4. Revisar con `hugo server` y hacer commit.

Sin el script: `hugo new --kind event content/es/event/<slug>` (y lo mismo con `en`) usa la plantilla `archetypes/event/index.md`.

### Charlas sin publicación en quarto.pub

Si una charla no está publicada, sus slides renderizadas se pueden alojar en el propio sitio:

```bash
python scripts/nueva_charla.py D:/Github/charlas-eventos/<carpeta> --alojar
```

Esto copia el HTML y los recursos que usa a `static/slides/<slug>/` y deja `url_slides: /slides/<slug>/index.html`. Los PDF van en `static/uploads/charlas/` y se enlazan con `url_pdf: /uploads/charlas/<archivo>.pdf`.

### Convenciones

- Títulos en español con mayúscula solo en la primera palabra (salvo nombres propios y siglas), con dos puntos para el subtítulo.
- La versión `es` va en español y la `en` en inglés, incluidas las etiquetas (`tags`), que generan páginas por idioma.
- Si cambias el `slug` de una charla ya publicada, agrega una línea en `static/_redirects` (`/es/talk/<viejo>/  /es/talk/<nuevo>/  301`, y lo mismo para `/en/`). No uses `aliases:`: con el sitio multilingüe, Netlify no lee los `_redirects` que genera el tema dentro de `/es/` y `/en/`.
- Botones extra (tableros, ejemplos, guías) van en `links:` con `name`, `url`, `icon_pack` e `icon`.
