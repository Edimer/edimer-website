---
# Plantilla para una charla nueva. Uso (crear el mismo slug en ambos idiomas):
#   hugo new --kind event content/es/event/<slug>
#   hugo new --kind event content/en/event/<slug>
# O, más rápido, desde una carpeta de D:/Github/charlas-eventos:
#   python scripts/nueva_charla.py D:/Github/charlas-eventos/<carpeta>
# Agrega la portada como featured.png (o .jpg) dentro de cada carpeta.

title: "{{ replace .Name "-" " " | humanize }}"
# La URL queda fija en /talk/<slug>/ aunque cambie el título.
slug: {{ .Name }}
event: ""
event_url: ""
location: ""
address:
  street: ""
  city: ""
  region: ""
  postcode: ""
  country: Colombia
summary: ""
abstract: ""
date: "{{ now.Format "2006-01-02" }}T08:00:00Z"
date_end: "{{ now.Format "2006-01-02" }}T12:00:00Z"
all_day: true
publishDate: "{{ now.Format "2006-01-02" }}T12:00:00Z"
authors: []
tags: []
featured: false
image:
  caption: ""
  focal_point: Center
  preview_only: false
# Botones extra, p.ej. tableros o ejemplos:
# links:
#   - name: "Tablero"
#     url: "https://..."
#     icon_pack: fas
#     icon: chart-bar
links: []
# URL de quarto.pub, o /slides/<slug>/index.html si las slides se alojan en static/slides/.
url_slides: ""
url_code: ""
# PDFs: guardarlos en static/uploads/charlas/ y usar /uploads/charlas/<archivo>.pdf
url_pdf: ""
url_video: ""
slides: ""
projects: []
---
