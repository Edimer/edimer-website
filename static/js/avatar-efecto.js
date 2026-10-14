/* Efecto abstracto alrededor del avatar: figuras geométricas de trazo fino que caen
   lentamente, giran y se conectan formando una red emergente cuando están cerca. */
(function () {
  "use strict";

  var canvas = document.querySelector(".avatar-efecto-canvas");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var contenedor = canvas.parentNode;

  var reducido = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  var N = 30;              // pocas partículas: bajo consumo de CPU
  var DIST = 115;          // distancia máxima para tender un enlace (px CSS)
  var ancho = 0, alto = 0, dpr = 1;
  var figuras = [];
  var visible = true, rafId = 0, ultimo = 0, tono0 = Math.random() * 360;

  function oscuro() {
    return document.body.classList.contains("dark");
  }

  function nueva(enCualquierAltura) {
    var lados = [0, 3, 4, 6][Math.floor(Math.random() * 4)]; // 0 = círculo
    return {
      x: Math.random() * ancho,
      y: enCualquierAltura ? Math.random() * alto : -20 - Math.random() * 40,
      r: 5 + Math.random() * 8,
      lados: lados,
      ang: Math.random() * Math.PI * 2,
      giro: (Math.random() - 0.5) * 0.6,       // rad/s
      vy: 8 + Math.random() * 14,              // px/s, caída lenta
      vx: (Math.random() - 0.5) * 6,
      fase: Math.random() * Math.PI * 2,
      dtono: Math.random() * 90
    };
  }

  function medir() {
    var rect = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    ancho = Math.max(1, rect.width);
    alto = Math.max(1, rect.height);
    canvas.width = Math.round(ancho * dpr);
    canvas.height = Math.round(alto * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function iniciar() {
    figuras = [];
    for (var i = 0; i < N; i++) figuras.push(nueva(true));
  }

  function poligono(f) {
    ctx.beginPath();
    if (f.lados === 0) {
      ctx.arc(f.x, f.y, f.r * 0.8, 0, Math.PI * 2);
    } else {
      for (var k = 0; k < f.lados; k++) {
        var a = f.ang + (k / f.lados) * Math.PI * 2;
        var px = f.x + Math.cos(a) * f.r, py = f.y + Math.sin(a) * f.r;
        if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
    }
    ctx.stroke();
  }

  function dibujar(t) {
    var dark = oscuro();
    var luz = dark ? 70 : 45, sat = dark ? 75 : 65;
    var alfa = dark ? 0.8 : 0.85;
    var tono = (tono0 + t * 0.012) % 360; // el color cicla lentamente
    ctx.clearRect(0, 0, ancho, alto);
    ctx.lineWidth = 1;

    // Red emergente: enlaces tenues entre figuras cercanas
    for (var i = 0; i < figuras.length; i++) {
      for (var j = i + 1; j < figuras.length; j++) {
        var a = figuras[i], b = figuras[j];
        var dx = a.x - b.x, dy = a.y - b.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < DIST) {
          ctx.strokeStyle = "hsla(" + ((tono + a.dtono) % 360) + "," + sat + "%," + luz + "%," + (alfa * 0.5 * (1 - d / DIST)).toFixed(3) + ")";
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    // Figuras
    for (var m = 0; m < figuras.length; m++) {
      var f = figuras[m];
      ctx.strokeStyle = "hsla(" + ((tono + f.dtono) % 360) + "," + sat + "%," + luz + "%," + alfa + ")";
      poligono(f);
    }
  }

  function paso(ahora) {
    rafId = 0;
    if (!visible || document.hidden) return;
    var dt = ultimo ? Math.min((ahora - ultimo) / 1000, 0.05) : 0;
    ultimo = ahora;
    for (var i = 0; i < figuras.length; i++) {
      var f = figuras[i];
      f.y += f.vy * dt;
      f.x += (f.vx + Math.sin(ahora / 1500 + f.fase) * 4) * dt;
      f.ang += f.giro * dt;
      if (f.y - f.r > alto || f.x < -30 || f.x > ancho + 30) figuras[i] = nueva(false);
    }
    dibujar(ahora);
    rafId = requestAnimationFrame(paso);
  }

  function arrancar() {
    if (reducido && reducido.matches) { dibujar(0); return; } // estado estático
    if (!rafId && visible && !document.hidden) {
      ultimo = 0;
      rafId = requestAnimationFrame(paso);
    }
  }

  function detener() {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = 0;
  }

  medir();
  iniciar();
  arrancar();

  // Redimensionado (con un pequeño retardo)
  var tRes;
  window.addEventListener("resize", function () {
    clearTimeout(tRes);
    tRes = setTimeout(function () { medir(); iniciar(); if (!rafId) dibujar(ultimo || 0); }, 150);
  });

  // Pausa cuando la sección no está a la vista o la pestaña está oculta
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entradas) {
      visible = entradas[0].isIntersecting;
      if (visible) arrancar(); else detener();
    }).observe(contenedor);
  }
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) detener(); else arrancar();
  });

  // Cambios de preferencia de movimiento y de tema claro/oscuro
  if (reducido) {
    var alCambiar = function () { detener(); arrancar(); };
    if (reducido.addEventListener) reducido.addEventListener("change", alCambiar);
    else if (reducido.addListener) reducido.addListener(alCambiar);
  }
  if ("MutationObserver" in window) {
    new MutationObserver(function () { if (!rafId) dibujar(ultimo || 0); })
      .observe(document.body, { attributes: true, attributeFilter: ["class"] });
  }
})();
