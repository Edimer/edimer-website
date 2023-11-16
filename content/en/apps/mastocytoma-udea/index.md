---
date: "2023-07-01T00:00:00Z"
external_link: ""
image:
  caption: App image with Gradio in Python
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
summary: Implementation of artificial vision algorithms for classification of Mastocytoma in pets.
tags:
- Computer vision
- Fastai
- Pets
- Deep Learning
title: Mastocytoma classifier with artificial vision
url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""
---

# Project description

This project aims to implement computer vision algorithms to classify two types of mastocytoma in pets (high grade - MAG and low grade - MBG). The current version uses the [Resnet](https://en.wikipedia.org/wiki/Residual_neural_network) neural network architecture trained through [fastai](https://docs.fast.ai/). The app was built with [Gradio](https://www.gradio.app/) and deployed on [Hugging Face](https://huggingface.co/).

This project is in continuous development with the involvement of students and professors from the University of Antioquia (Colombia), evaluating new algorithms and increasing the number of samples in model training.

# App

<script
	type="module"
	src="https://gradio.s3-us-west-2.amazonaws.com/3.38.0/gradio.js"
></script>

<gradio-app src="https://sidereus-mastocitoma-udea.hf.space"></gradio-app>

