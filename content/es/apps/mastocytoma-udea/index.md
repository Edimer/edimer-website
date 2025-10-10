---
date: "2023-07-01T00:00:00Z"
external_link: ""
image:
  caption: Imagen de la app con Gradio en Python
  focal_point: Smart
links:
- icon: code
  icon_pack: fa
  name: Code
  url: https://huggingface.co/spaces/Sidereus/mastocitoma_udea/tree/main
- icon: tablet-screen-button
  icon_pack: fa
  name: App Hugging Face
  url: https://huggingface.co/spaces/Sidereus/mastocitoma_udea
summary: Implementación de algoritmos de visión artificial para clasificación de Mastocitoma en mascotas.
tags:
- Computer vision
- Fastai
- Pets
- Deep Learning
- Python
title: Clasificador de Mastocitoma con visión artificial
url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""
---

# Descripción del proyecto

Este proyecto tiene como objetivo implementar algoritmos de visión artificial para clasificar dos tipos de mastocitoma en mascotas (alto grado - MAG y bajo grado - MBG). La versión actual utiliza la arquitectura de red neuronal [Resnet](https://en.wikipedia.org/wiki/Residual_neural_network) entrenada mediante [fastai](https://docs.fast.ai/). La aplicación fue construida con [Gradio](https://www.gradio.app/) y desplegada en [Hugging Face](https://huggingface.co/).

Este proyecto está en desarrollo continuo con la participación de estudiantes y profesores de la Universidad de Antioquia (Colombia), evaluando nuevos algoritmos y aumentando el número de muestras en el entrenamiento del modelo.

# Aplicación

<script
	type="module"
	src="https://gradio.s3-us-west-2.amazonaws.com/3.38.0/gradio.js"
></script>

<gradio-app src="https://sidereus-mastocitoma-udea.hf.space"></gradio-app>

