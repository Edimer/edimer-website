# edimer-website

Código fuente del sitio web personal de **Edimer David Jaramillo**, científico de datos y profesor: <https://edimer.netlify.app>

El sitio es bilingüe (español e inglés) y reúne mi perfil, experiencia, publicaciones, aplicaciones y las charlas que he presentado en universidades, centros de investigación y eventos académicos.

## Tecnologías

- [Hugo](https://gohugo.io/) 0.119 (versión *extended*)
- [Wowchemy](https://wowchemy.com/), tema *starter-hugo-academic*
- [Netlify](https://www.netlify.com/) para el despliegue
- Presentaciones hechas con [Quarto](https://quarto.org/) + reveal.js y R Markdown (xaringan)

## Estructura

```
content/es/, content/en/   Contenido en español e inglés
  event/<charla>/          Una carpeta por charla (ficha + imagen de portada)
  publication/             Publicaciones
  apps/                    Aplicaciones
static/slides/<charla>/    Diapositivas de cada charla, servidas desde el propio sitio
static/uploads/            PDF y otros archivos descargables
scripts/                   Utilidades en Python para agregar charlas y respaldar presentaciones
layouts/, assets/scss/     Ajustes propios sobre la plantilla del tema
```

Las diapositivas de todas las charlas se alojan en el propio sitio, de modo que siguen disponibles sin depender de servicios externos de publicación.

## Ejecutarlo localmente

Con Hugo *extended* 0.119 instalado:

```bash
git clone https://github.com/Edimer/edimer-website.git
cd edimer-website
hugo server
```

El sitio queda disponible en <http://localhost:1313/>.

## Licencia

El código de este repositorio está bajo la licencia MIT (ver [LICENSE](LICENSE)).
