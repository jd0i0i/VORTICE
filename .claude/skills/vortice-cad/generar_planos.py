#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VORTICE 150 v3 - Generador de las tres laminas acotadas (SVG -> PNG).

Cada cota sale de PARAMETERS/master.yaml o de PARAMETERS/derivados_cad.json,
que escribe el generador del modelo 3D. NINGUNA se escribe aqui.

En la v2 este script llevaba su PROPIO desplazamiento de cinta escrito a
mano (-35,0 mm) mientras el modelo 3D calculaba -31,6: las laminas y el
STEP estaban desincronizados 3,4 mm y la lamina imprimia un recorrido de
asentamiento de 480 mm que no era el de la maquina. Ya no hay
desplazamiento y no hay numeros propios.

Las trayectorias que se dibujan son EXACTAMENTE las que verifico
verificar.py, punto por punto: vienen en derivados_cad.json.

LAMINA 1  Alzado lateral   - posiciones X, alturas, trayectorias
LAMINA 2  Planta           - anchos y posiciones transversales
LAMINA 3  Rotor y tambor   - cortes, entrehierro indexado, despiece
"""

import os
import math
import json
import datetime

import yaml


def svg_a_png(ruta_svg, ruta_png, ancho_px=2480):
    """SVG -> PNG. cairosvg necesita la DLL nativa de cairo, que no
    existe en una instalacion Windows limpia; svglib+reportlab es Python
    puro y cubre el subconjunto de SVG que genera este script."""
    try:
        import cairosvg
        cairosvg.svg2png(url=ruta_svg, write_to=ruta_png,
                         output_width=ancho_px, background_color="white")
        return
    except Exception:
        pass
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    dib = svg2rlg(ruta_svg)
    escala = ancho_px / float(dib.width)
    dib.scale(escala, escala)
    dib.width *= escala
    dib.height *= escala
    renderPM.drawToFile(dib, ruta_png, fmt="PNG", bg=0xFFFFFF)


AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
DIR_PNG = os.path.join(RAIZ, "CAD", "PLANOS")
os.makedirs(DIR_PNG, exist_ok=True)

with open(os.path.join(RAIZ, "PARAMETERS", "master.yaml"), "r", encoding="utf-8") as fh:
    P = yaml.safe_load(fh)
with open(os.path.join(RAIZ, "PARAMETERS", "derivados_cad.json"), "r", encoding="utf-8") as fh:
    D = json.load(fh)

R, TB, OP, CI, TO = P["rotor"], P["tambor"], P["operacion"], P["cinta"], P["tolva"]
TR, SA, BA, MO = P["transmision"], P["salida"], P["bastidor"], P["montaje"]
GE, EH, EL = R["geometria"], OP["entrehierro"], P["electronica"]

HOY = datetime.date.today().strftime("%d/%m/%Y")
W, H = 420.0, 297.0                      # A3 apaisado, en mm

C_LIN = "#1F2937"     # geometria
C_COT = "#B91C1C"     # cotas
C_AUX = "#9CA3AF"     # ejes y auxiliares
C_TRA = "#0F766E"     # trayectorias
C_REL = "#2563EB"     # resaltado
C_CAR = "#7C3AED"     # carcasa / tambor


class SVG(object):
    """Minimo generador de SVG tecnico. Unidades = mm de papel."""

    def __init__(self, titulo, escala, subtitulo=""):
        self.o = []
        self.titulo, self.escala, self.subtitulo = titulo, escala, subtitulo

    def line(self, x1, y1, x2, y2, c=C_LIN, w=0.35, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.o.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" '
                      'stroke="%s" stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, c, w, d))

    def rect(self, x, y, w_, h_, c=C_LIN, sw=0.35, fill="none", dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" '
                      'fill="%s" stroke="%s" stroke-width="%.2f"%s/>'
                      % (x, y, max(w_, 0), max(h_, 0), fill, c, sw, d))

    def circle(self, x, y, r, c=C_LIN, sw=0.35, fill="none", dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" '
                      'stroke="%s" stroke-width="%.2f"%s/>' % (x, y, r, fill, c, sw, d))

    def poly(self, pts, c=C_LIN, sw=0.35, fill="none", dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        s = " ".join("%.3f,%.3f" % p for p in pts)
        self.o.append('<polyline points="%s" fill="%s" stroke="%s" '
                      'stroke-width="%.2f"%s/>' % (s, fill, c, sw, d))

    def text(self, x, y, s, size=2.6, c=C_LIN, anchor="middle",
             bold=False, italic=False, rot=None):
        s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        tr = ' transform="rotate(%.2f %.3f %.3f)"' % (rot, x, y) if rot else ""
        self.o.append('<text x="%.3f" y="%.3f" font-family="Arial, Helvetica, '
                      'sans-serif" font-size="%.2f" fill="%s" text-anchor="%s"%s%s%s>%s</text>'
                      % (x, y, size, c, anchor, ' font-weight="bold"' if bold else "",
                         ' font-style="italic"' if italic else "", tr, s))

    def _flecha(self, x, y, dx, dy):
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        p = [(x, y), (x + ux * 2.0 + px * 0.6, y + uy * 2.0 + py * 0.6),
             (x + ux * 2.0 - px * 0.6, y + uy * 2.0 - py * 0.6)]
        self.o.append('<polygon points="%s" fill="%s"/>'
                      % (" ".join("%.3f,%.3f" % q for q in p), C_COT))

    def dim_h(self, x1, x2, y, etiqueta, y_obj=None, size=2.4):
        if abs(x2 - x1) < 0.05:
            return
        if y_obj is not None:
            for x in (x1, x2):
                self.line(x, y_obj, x, y + (1.5 if y > y_obj else -1.5), C_COT, 0.18)
        self.line(x1, y, x2, y, C_COT, 0.25)
        self._flecha(x1, y, 1, 0)
        self._flecha(x2, y, -1, 0)
        if abs(x2 - x1) < len(etiqueta) * size * 0.62:
            self.text(max(x1, x2) + 1.5, y - 1.1, etiqueta, size, C_COT, "start")
        else:
            self.text((x1 + x2) / 2.0, y - 1.1, etiqueta, size, C_COT)

    def dim_v(self, y1, y2, x, etiqueta, x_obj=None, size=2.4, lado="izq"):
        if abs(y2 - y1) < 0.05:
            return
        if x_obj is not None:
            for y in (y1, y2):
                self.line(x_obj, y, x + (1.5 if x > x_obj else -1.5), y, C_COT, 0.18)
        self.line(x, y1, x, y2, C_COT, 0.25)
        self._flecha(x, y1, 0, 1)
        self._flecha(x, y2, 0, -1)
        yc = (y1 + y2) / 2.0
        if abs(y2 - y1) < len(etiqueta) * size * 0.62:
            self.text(x - 1.2, min(y1, y2) - 1.2, etiqueta, size, C_COT, "end")
        else:
            self.text(x - 1.2, yc, etiqueta, size, C_COT, "middle",
                      rot=-90 if lado == "izq" else 90)

    def caratula(self, filas):
        bx, by, bw, bh = W - 96.0, H - 46.0, 88.0, 38.0
        self.rect(bx, by, bw, bh, C_LIN, 0.5, "#FFFFFF")
        self.line(bx, by + 8.5, bx + bw, by + 8.5, C_LIN, 0.5)
        self.text(bx + 3, by + 6, "VORTICE 150", 4.4, C_LIN, "start", True)
        self.text(bx + bw - 3, by + 6, self.titulo, 2.7, C_LIN, "end", True)
        y = by + 13.5
        for k, v in filas:
            self.text(bx + 3, y, k, 2.4, "#6B7280", "start")
            self.text(bx + bw - 3, y, v, 2.4, C_LIN, "end", True)
            y += 4.6

    def tabla(self, x, y, titulo, filas, ancho=74.0, size=2.35):
        alto = 8.6 + len(filas) * 4.35
        self.rect(x, y, ancho, alto, C_LIN, 0.4, "#F9FAFB")
        self.line(x, y + 6.4, x + ancho, y + 6.4, C_LIN, 0.4)
        self.text(x + 2.5, y + 4.5, titulo, 2.7, C_LIN, "start", True)
        yy = y + 10.6
        for k, v in filas:
            self.text(x + 2.5, yy, k, size, "#4B5563", "start")
            self.text(x + ancho - 2.5, yy, v, size, C_LIN, "end", True)
            yy += 4.35
        return alto

    def guardar(self, nombre):
        cab = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" '
               'height="%.1fmm" viewBox="0 0 %.1f %.1f">'
               '<rect width="%.1f" height="%.1f" fill="#FFFFFF"/>' % (W, H, W, H, W, H))
        marco = ('<rect x="6" y="6" width="%.1f" height="%.1f" fill="none" '
                 'stroke="%s" stroke-width="0.6"/>' % (W - 12, H - 12, C_LIN))
        svg = cab + marco + "".join(self.o) + "</svg>"
        ruta_svg = os.path.join(DIR_PNG, nombre + ".svg")
        with open(ruta_svg, "w", encoding="utf-8") as fh:
            fh.write(svg)
        svg_a_png(ruta_svg, os.path.join(DIR_PNG, nombre + ".png"))
        print("  -> %s.png" % nombre)


def fmt(v, dec=0):
    return (("%%.%df" % dec) % v).replace(".", ",")


# =====================================================================
# LAMINA 1 - ALZADO LATERAL
# =====================================================================
def lamina1():
    E = 1.0 / 5.0
    s = SVG("LAMINA 1 - ALZADO LATERAL", "1:5")
    OX, OZ = 56.0, 200.0

    def px(x):
        return OX + x * E

    def pz(z):
        return OZ - z * E

    xb0, xb1 = MO["x_base_ini"], MO["x_base_fin"]
    zoff = MO["z_offset_cad"]

    # --- suelo y bastidor ---------------------------------------------
    s.line(px(xb0 - 40), pz(0), px(xb1 + 40), pz(0), C_AUX, 0.4, "3,1.6")
    s.rect(px(xb0), pz(zoff), (xb1 - xb0) * E, BA["base_esp"] * E, C_LIN, 0.5)
    for xf in (xb0 + P["cad"]["pata_x_borde"], xb1 - P["cad"]["pata_x_borde"]):
        s.rect(px(xf - BA["pata_D"] / 2), pz(BA["pata_H"]),
               BA["pata_D"] * E, BA["pata_H"] * E, C_LIN, 0.4)
    s.rect(px(xb0), pz(MO["z_lateral_top_cad"]), (xb1 - xb0) * E,
           BA["lateral_H"] * E, C_LIN, 0.5)
    for xc in BA["ventanas"]["x_centros"]:
        s.rect(px(xc - BA["ventanas"]["ancho_X"] / 2),
               pz(BA["ventanas"]["z_centro"] + zoff + BA["ventanas"]["alto_Z"] / 2),
               BA["ventanas"]["ancho_X"] * E, BA["ventanas"]["alto_Z"] * E, C_AUX, 0.3)
    esc = BA["ventanas"]["escotadura_rotor"]
    s.rect(px(esc["x_ini"]), pz(MO["z_eje_tambor_cad"] + 40),
           (esc["x_fin"] - esc["x_ini"]) * E, 80 * E, C_AUX, 0.3, dash="2,1.2")

    # --- guarda --------------------------------------------------------
    g0, g1 = MO["x_guarda"]
    s.rect(px(g0), pz(MO["z_lateral_top_cad"] + BA["guarda_esp"]),
           (g1 - g0) * E, BA["guarda_esp"] * E, C_REL, 0.6, C_REL)
    s.line(px((g0 + g1) / 2), pz(MO["z_lateral_top_cad"] + BA["guarda_esp"]) - 0.5,
           px((g0 + g1) / 2), pz(MO["z_lateral_top_cad"]) - 12, C_REL, 0.3)
    s.text(px((g0 + g1) / 2), pz(MO["z_lateral_top_cad"]) - 13.5,
           "GUARDA  %s x %s x %s" % (fmt(g1 - g0), fmt(BA["guarda_Y"]),
                                     fmt(BA["guarda_esp"], 1)),
           2.4, C_REL, "middle", True)

    # --- cinta: rodillo de cola + tambor + banda que lo envuelve -------
    zr = MO["z_eje_rodillo_cola_cad"]
    zt = MO["z_eje_tambor_cad"]
    rr, rc, rm = D["r_rodillo"], D["r_carcasa"], D["r_material"]
    s.circle(px(MO["x_rodillo_cola"]), pz(zr), rr * E, C_LIN, 0.45)
    s.circle(px(MO["x_rodillo_cola"]), pz(zr), 0.5, C_AUX, 0.3)
    s.circle(px(MO["x_tambor"]), pz(zt), rc * E, C_CAR, 0.55)
    s.circle(px(MO["x_tambor"]), pz(zt), GE["D_r"] / 2 * E, C_LIN, 0.45)
    s.circle(px(MO["x_tambor"]), pz(zt), R["tubo"]["OD"] / 2 * E, C_LIN, 0.3, dash="2,1.2")
    s.line(px(MO["x_tambor"]) - 15, pz(zt), px(MO["x_tambor"]) + 15, pz(zt),
           C_AUX, 0.3, "4,1.5,1,1.5")
    s.line(px(MO["x_tambor"]), pz(zt) - 15, px(MO["x_tambor"]), pz(zt) + 15,
           C_AUX, 0.3, "4,1.5,1,1.5")
    # banda: ramal superior horizontal + envolvente del tambor + retorno
    s.line(px(MO["x_rodillo_cola"]), pz(MO["z_banda_sup_cad"]),
           px(MO["x_tambor"]), pz(MO["z_banda_sup_cad"]), C_LIN, 0.7)
    arco = [(px(MO["x_tambor"] + rm * math.sin(math.radians(a))),
             pz(zt + rm * math.cos(math.radians(a)))) for a in range(0, 181, 5)]
    s.poly(arco, C_LIN, 0.7)
    s.line(px(MO["x_tambor"]), pz(zt - rm), px(MO["x_rodillo_cola"]),
           pz(zr - rr - CI["banda_esp"]), C_LIN, 0.5)
    arco2 = [(px(MO["x_rodillo_cola"] - (rr + CI["banda_esp"]) * math.sin(math.radians(a))),
              pz(zr - (rr + CI["banda_esp"]) * math.cos(math.radians(a))))
             for a in range(0, 181, 5)]
    s.poly(arco2, C_LIN, 0.5)

    # --- tolva ---------------------------------------------------------
    xt = MO["x_tolva_centro"]
    zs = zoff + TO["z_boca"]
    zc_ = zs + TO["h_cuello"]
    ztop = zc_ + TO["h_cono"]
    sx, ux = TO["salida"][1] / 2, TO["sup"][1] / 2
    s.poly([(px(xt - sx), pz(zs)), (px(xt - sx), pz(zc_)), (px(xt - ux), pz(ztop)),
            (px(xt + ux), pz(ztop)), (px(xt + sx), pz(zc_)), (px(xt + sx), pz(zs)),
            (px(xt - sx), pz(zs))], C_LIN, 0.5)
    for sgn in (-1, 1):
        s.rect(px(xt + sgn * TO["soportes"]["ancho_X"] / 2 - 1.5),
               pz(zs - TO["soportes"]["brida_esp"]), 3.0 * E,
               (zs - TO["soportes"]["brida_esp"] - zoff) * E, C_REL, 0.45)
    s.rect(px(xt - TO["soportes"]["brida_X"] / 2), pz(zs),
           TO["soportes"]["brida_X"] * E, TO["soportes"]["brida_esp"] * E, C_REL, 0.5)
    s.text(px(xt), pz(ztop) - 3.2, "TOLVA %s L" % fmt(TO["volumen_L"], 2),
           2.5, C_LIN, "middle", True)

    # --- salida: bandejas, cuchilla, deflector -------------------------
    zp, zk = MO["z_bandeja_piso_cad"], MO["z_bandeja_canto_cad"]
    for (a, b), et in ((MO["x_bandeja_inerte"], "INERTES"),
                       (MO["x_bandeja_nofe"], "NO FERROSOS")):
        s.rect(px(a), pz(zk), (b - a) * E, (zk - MO["z_celda_top_cad"]) * E, C_LIN, 0.45)
        s.text(px((a + b) / 2), pz(zk) + 5.0, et, 2.3, C_LIN, "middle", True)
        s.rect(px((a + b) / 2 - EL["celda_L"] / 2), pz(MO["z_celda_top_cad"]),
               EL["celda_L"] * E, EL["celda_alto"] * E, C_REL, 0.45)
    s.text(px((MO["x_bandeja_inerte"][0] + MO["x_bandeja_nofe"][1]) / 2),
           pz(MO["z_celda_top_cad"]) + 8.5,
           "1 celda de %s kg por bandeja  -  2 canales" % fmt(EL["celda_FS"], 0),
           2.3, C_REL, "middle", True)
    xc = MO["x_cuchilla"]
    s.rect(px(xc - SA["cuchilla_esp"] / 2), pz(D["z_cuchilla_top"]),
           max(SA["cuchilla_esp"] * E, 0.6), SA["cuchilla_H"] * E, C_REL, 0.6, C_REL)
    s.rect(px(xc - SA["cuchilla_tejadillo"] / 2), pz(D["z_tejadillo"][1]),
           SA["cuchilla_tejadillo"] * E, SA["cuchilla_esp"] * E, C_REL, 0.4, C_REL)
    # El rotulo de la cuchilla NO se pone junto a ella: ahi pasan las
    # cuatro trayectorias. Va en la tabla, con su altura.
    s.text(px(xc), pz(D["z_cuchilla_top"]) - 2.0, "C", 2.4, C_REL, "middle", True)
    xd = MO["x_deflector_espuma"]
    s.rect(px(xd), pz(zk + 4 * SA["cuchilla_H"]), SA["deflector_espuma"] * E,
           (zk + 4 * SA["cuchilla_H"] - zp - SA["deflector_z_bot_holgura"]) * E, C_LIN, 0.5)
    s.text(px(xd + SA["deflector_espuma"] / 2), pz(zk + 4 * SA["cuchilla_H"]) - 1.6,
           "deflector", 2.2, C_LIN, "middle")

    # --- trayectorias: las mismas que verifica verificar.py ------------
    TY = D["trayectorias"]
    orden = [("inerte", "1", "2,1.4"), ("f35", "2", None),
             ("f25", "3", None), ("lata", "4", None)]
    for k, num, dash in orden:
        pts = [(px(x), pz(z)) for x, z in TY[k]["pts"]]
        s.poly(pts, C_TRA, 0.5, dash=dash)
        s.circle(pts[-1][0], pts[-1][1], 2.0, C_TRA, 0.3, "#FFFFFF")
        s.text(pts[-1][0], pts[-1][1] + 0.8, num, 2.4, C_TRA, "middle", True)

    # --- cotas horizontales (tres niveles escalonados) ------------------
    n1, n2, n3 = pz(0) + 12.0, pz(0) + 22.0, pz(0) + 32.0
    yo = pz(0) + 2
    s.dim_h(px(MO["x_rodillo_cola"]), px(MO["x_tambor"]), n1, fmt(CI["entrecentros"]), yo)
    s.dim_h(px(MO["x_tambor"]), px(xc), n1, fmt(xc - MO["x_tambor"]), yo)
    s.dim_h(px(xt), px(MO["x_tambor"]), n2,
            "asentamiento  " + fmt(MO["recorrido_asentamiento"]), yo)
    s.dim_h(px(xc), px(xd), n2, fmt(xd - xc), yo)
    s.dim_h(px(xb0), px(xb1), n3, "base  " + fmt(BA["base_L"]), yo)

    # --- cotas verticales ----------------------------------------------
    v1, v2 = px(xb0) - 9.0, px(xb0) - 19.0
    s.dim_v(pz(0), pz(zoff), v1, fmt(zoff), px(xb0))
    s.dim_v(pz(zoff), pz(MO["z_banda_sup_cad"]), v1, fmt(CI["banda_sup_altura"]), px(xb0))
    s.dim_v(pz(0), pz(ztop), v2, "altura  " + fmt(ztop), px(xb0))
    s.dim_v(pz(MO["z_banda_sup_cad"]), pz(zp), px(xb1) + 10,
            "caida  " + fmt(SA["alcances"]["h_caida"]), px(xb1) + 2, lado="der")

    # --- tablas ---------------------------------------------------------
    s.tabla(12, 244, "PARAMETROS DE OPERACION", [
        ("Velocidad de banda", fmt(OP["v_banda"], 2) + " m/s"),
        ("Velocidad del rotor", fmt(OP["N_nominal"]) + " rpm"),
        ("f = p N/60,  p = n_polos/2 = " + fmt(GE["p_pares"]), fmt(OP["f_nominal"], 1) + " Hz"),
        ("Entrehierro nominal", fmt(EH["z_nominal"], 1) + " mm"),
        ("Paso polar lambda = pi D_r/p", fmt(GE["lambda"], 2) + " mm"),
        ("Caudal nominal", fmt(P["caudal"]["caudal_kg_h"], 1) + " kg/h"),
    ], 132)
    s.text(302, 16.5, "Las trayectorias son PREDICCIONES: las cuatro", 2.3, C_TRA, "start", italic=True)
    s.text(302, 20.0, "velocidades de salida van marcadas [VERIFICAR]", 2.3, C_TRA, "start", italic=True)
    s.text(302, 23.5, "y se cierran con el pendulo (P-06).", 2.3, C_TRA, "start", italic=True)
    s.tabla(302, 27, "CAIDA PREDICHA  (x absoluto)", [
        ("1  Inerte, sin empuje", fmt(TY["inerte"]["x_fin"], 0) + " mm"),
        ("2  Fragmento 35 mm", fmt(TY["f35"]["x_fin"], 0) + " mm"),
        ("3  Fragmento 25 mm", fmt(TY["f25"]["x_fin"], 0) + " mm"),
        ("4  Media lata (la para el defl.)", fmt(TY["lata"]["x_fin"], 0) + " mm"),
        ("C  Cuchilla divisora", fmt(xc) + " mm"),
        ("    filo sobre el canto de bandeja", fmt(SA["cuchilla_H"]) + " mm"),
        ("Margen minimo a la cuchilla", fmt(SA["margen_cuchilla"], 0) + " mm"),
    ], 110)
    s.caratula([("Escala", "1:5  (A3)"), ("Cotas en", "milimetros"),
                ("Fuente", "master.yaml v%d" % P["meta"]["version_parametros"]),
                ("Fecha", HOY), ("Lamina", "1 de 3")])
    s.guardar("LAMINA1_alzado")


# =====================================================================
# LAMINA 2 - PLANTA
# =====================================================================
def lamina2():
    E = 1.0 / 5.0
    s = SVG("LAMINA 2 - PLANTA", "1:5")
    OX, OY = 56.0, 118.0

    def px(x):
        return OX + x * E

    def py(y):
        return OY - y * E

    xb0, xb1 = MO["x_base_ini"], MO["x_base_fin"]
    s.rect(px(xb0), py(BA["base_W"] / 2), (xb1 - xb0) * E, BA["base_W"] * E, C_LIN, 0.5)
    for sgn in (-1, 1):
        yi = sgn * BA["sep_laterales"] / 2
        ye = yi + sgn * BA["lateral_esp"]
        s.rect(px(xb0), py(max(yi, ye)), (xb1 - xb0) * E, BA["lateral_esp"] * E, C_LIN, 0.45)
    s.line(px(xb0 - 12), py(0), px(xb1 + 12), py(0), C_AUX, 0.3, "5,1.5,1,1.5")

    s.rect(px(MO["x_rodillo_cola"]), py(CI["banda_ancho"] / 2),
           (MO["x_tambor"] - MO["x_rodillo_cola"]) * E, CI["banda_ancho"] * E, C_LIN, 0.5)
    s.rect(px(MO["x_rodillo_cola"] - CI["rodillo_D"] / 2), py(CI["rodillo_L"] / 2),
           CI["rodillo_D"] * E, CI["rodillo_L"] * E, C_LIN, 0.4)
    xt = MO["x_tolva_centro"]
    s.rect(px(xt - TO["sup"][1] / 2), py(TO["sup"][0] / 2),
           TO["sup"][1] * E, TO["sup"][0] * E, C_LIN, 0.45)
    s.rect(px(xt - TO["salida"][1] / 2), py(TO["salida"][0] / 2),
           TO["salida"][1] * E, TO["salida"][0] * E, C_REL, 0.45, dash="2,1.2")

    # tambor: carcasa, largo activo, discos, chumaceras
    xr = MO["x_tambor"]
    s.rect(px(xr - TB["OD"] / 2), py(TB["y_ext"]), TB["OD"] * E, 2 * TB["y_ext"] * E, C_CAR, 0.55)
    s.rect(px(xr - GE["D_r"] / 2), py(R["tubo"]["largo"] / 2),
           GE["D_r"] * E, R["tubo"]["largo"] * E, C_LIN, 0.45)
    s.rect(px(xr - GE["D_r"] / 2), py(GE["largo_activo"] / 2),
           GE["D_r"] * E, GE["largo_activo"] * E, C_REL, 0.4, dash="2,1.2")
    for sgn in (-1, 1):
        yc = sgn * R["soporte"]["span_chumaceras"] / 2
        s.rect(px(xr - R["soporte"]["ucp204_L"] / 2), py(yc + R["soporte"]["ucp204_A"] / 2),
               R["soporte"]["ucp204_L"] * E, R["soporte"]["ucp204_A"] * E, C_LIN, 0.4)
    s.line(px(xr), py(R["eje"]["largo"] / 2), px(xr), py(-R["eje"]["largo"] / 2),
           C_AUX, 0.35, "5,1.5,1,1.5")
    s.text(px(xr), py(BA["base_W"] / 2) - 2.5, "TAMBOR  ·  carcasa no conductora",
           2.4, C_CAR, "middle", True)

    for (a, b), et in ((MO["x_bandeja_inerte"], "INERTES"),
                       (MO["x_bandeja_nofe"], "NO FERROSOS")):
        yb = SA["bandeja_inerte"][0] / 2 + SA["bandeja_esp"]
        s.rect(px(a), py(yb), (b - a) * E, 2 * yb * E, C_LIN, 0.45)
        s.text(px((a + b) / 2), py(0) + 1.0, et, 2.4, C_LIN, "middle", True)
    xc = MO["x_cuchilla"]
    s.line(px(xc), py(SA["cuchilla_Y"]), px(xc), py(-SA["cuchilla_Y"]), C_REL, 0.8)

    n1, n2 = py(-BA["base_W"] / 2) + 11.0, py(-BA["base_W"] / 2) + 21.0
    yo = py(-BA["base_W"] / 2) + 2
    s.dim_h(px(xt), px(xr), n1, fmt(xr - xt), yo)
    s.dim_h(px(xr), px(xc), n1, fmt(xc - xr), yo)
    s.dim_h(px(MO["x_bandeja_nofe"][0]), px(MO["x_bandeja_nofe"][1]), n2,
            "bandeja no ferrosos  " + fmt(MO["x_bandeja_nofe"][1] - MO["x_bandeja_nofe"][0]), yo)

    vx = px(xb0) - 8.0
    s.dim_v(py(BA["sep_laterales"] / 2), py(-BA["sep_laterales"] / 2), vx,
            "entre laterales  " + fmt(BA["sep_laterales"]), px(xb0))
    s.dim_v(py(R["soporte"]["span_chumaceras"] / 2), py(-R["soporte"]["span_chumaceras"] / 2),
            vx - 10, "span chumaceras  " + fmt(R["soporte"]["span_chumaceras"]), px(xb0))
    s.dim_v(py(BA["base_W"] / 2), py(-BA["base_W"] / 2), vx - 20,
            "base  " + fmt(BA["base_W"]), px(xb0))
    s.dim_v(py(CI["banda_ancho"] / 2), py(-CI["banda_ancho"] / 2),
            px(MO["x_rodillo_cola"]) + (MO["x_tambor"] - MO["x_rodillo_cola"]) * E * 0.45,
            "banda  " + fmt(CI["banda_ancho"]), None)

    s.tabla(12, 206, "ANCHOS CLAVE", [
        ("Base", fmt(BA["base_W"]) + " mm"),
        ("Entre laterales (interior)", fmt(BA["sep_laterales"]) + " mm"),
        ("Banda", fmt(CI["banda_ancho"]) + " mm"),
        ("Carcasa del tambor (largo)", fmt(2 * TB["y_ext"]) + " mm"),
        ("Largo activo del rotor", fmt(GE["largo_activo"]) + " mm"),
        ("Bandejas (interior)", fmt(SA["bandeja_inerte"][0]) + " mm"),
        ("Salida de tolva  (banda - 2x%s)" % fmt(TO["margen_a_banda"]),
         fmt(TO["salida"][0]) + " mm"),
    ], 118)
    s.caratula([("Escala", "1:5  (A3)"), ("Cotas en", "milimetros"),
                ("Fuente", "master.yaml v%d" % P["meta"]["version_parametros"]),
                ("Fecha", HOY), ("Lamina", "2 de 3")])
    s.guardar("LAMINA2_planta")


# =====================================================================
# LAMINA 3 - ROTOR Y TAMBOR
# =====================================================================
def lamina3():
    s = SVG("LAMINA 3 - ROTOR Y TAMBOR", "1:1 / 1:2")
    CX, CY = 92.0, 108.0
    rt, ri = R["tubo"]["OD"] / 2, GE["D_r"] / 2
    IM = R["iman"]

    s.text(CX, 26.0, "CORTE TRANSVERSAL   1:1", 3.2, C_LIN, "middle", True)
    # capas del entrehierro, de dentro afuera
    s.circle(CX, CY, R["tubo"]["ID"] / 2, C_LIN, 0.5)
    s.circle(CX, CY, rt, C_LIN, 0.5)
    s.circle(CX, CY, R["eje"]["D"] / 2, C_LIN, 0.4)
    s.circle(CX, CY, ri, C_AUX, 0.3, dash="2,1.5")
    s.circle(CX, CY, ri + R["retencion"]["z_zuncho"], C_AUX, 0.3, dash="1,1")
    s.circle(CX, CY, TB["ID"] / 2, C_CAR, 0.4, dash="3,1.5")
    s.circle(CX, CY, TB["OD"] / 2, C_CAR, 0.6)
    s.circle(CX, CY, TB["OD"] / 2 + CI["banda_esp"], C_LIN, 0.55)
    s.line(CX - ri - 12, CY, CX + ri + 12, CY, C_AUX, 0.3, "6,2,1,2")
    s.line(CX, CY - ri - 12, CX, CY + ri + 12, C_AUX, 0.3, "6,2,1,2")

    paso = 360.0 / IM["n_polos"]
    for k in range(IM["n_polos"]):
        th = math.radians(k * paso)
        col = "#C0392B" if k % 2 == 0 else "#2563EB"
        for j in range(IM["k_piezas"]):
            off = (j - (IM["k_piezas"] - 1) / 2.0) * IM["W"]
            ux, uy = math.cos(th), -math.sin(th)
            tx, ty = -math.sin(th), -math.cos(th)
            pts = []
            for (a, b) in ((-IM["W"] / 2, 0), (IM["W"] / 2, 0),
                           (IM["W"] / 2, IM["T"]), (-IM["W"] / 2, IM["T"])):
                d, rr = off + a, rt + b
                pts.append((CX + ux * rr + tx * d, CY + uy * rr + ty * d))
            pts.append(pts[0])
            s.poly(pts, col, 0.3, col)
        th2 = math.radians(k * paso + paso / 2.0)
        ux, uy = math.cos(th2), -math.sin(th2)
        tx, ty = -math.sin(th2), -math.cos(th2)
        pts = []
        for (a, b) in ((-R["retencion"]["tira_ancho"] / 2, 0),
                       (R["retencion"]["tira_ancho"] / 2, 0),
                       (R["retencion"]["tira_ancho"] / 2, R["retencion"]["tira_alto"]),
                       (-R["retencion"]["tira_ancho"] / 2, R["retencion"]["tira_alto"])):
            pts.append((CX + ux * (rt + b) + tx * a, CY + uy * (rt + b) + ty * a))
        pts.append(pts[0])
        s.poly(pts, "#8B5CF6", 0.25, "#8B5CF6")
        etq = "N" if k % 2 == 0 else "S"
        s.text(CX + math.cos(th) * (ri + 4.0), CY - math.sin(th) * (ri + 4.0) + 1.0,
               etq, 3.0, col, "middle", True)

    s.dim_v(CY - ri, CY + ri, CX - ri - 16, "D_r  " + fmt(GE["D_r"], 1), None)
    s.dim_v(CY - rt, CY + rt, CX - ri - 26, "OD  " + fmt(R["tubo"]["OD"], 1), None)
    s.dim_v(CY - TB["OD"] / 2, CY + TB["OD"] / 2, CX + ri + 13,
            "carcasa  " + fmt(TB["OD"], 1), None, lado="der")
    s.text(CX, CY + ri + 14, "%d polos alternados - paso %s mm"
           % (IM["n_polos"], fmt(GE["paso_circ"], 2)), 2.4, C_LIN, "middle")
    s.text(CX, CY + ri + 18.5, "hueco entre polos %s mm (tira PETG)"
           % fmt(GE["hueco_polos"], 2), 2.3, "#8B5CF6", "middle")
    s.text(CX, CY + ri + 23.0, "la banda envuelve la carcasa: el material va a R=%s"
           % fmt(TB["OD"] / 2 + CI["banda_esp"], 1), 2.3, C_CAR, "middle", True)

    # --- corte longitudinal 1:2 -----------------------------------------
    E2, LX, LY = 0.5, 236.0, 96.0
    s.text(LX + 55, 26.0, "CORTE LONGITUDINAL   1:2", 3.2, C_LIN, "middle", True)
    L = R["tubo"]["largo"]
    s.rect(LX, LY - rt * E2, L * E2, 2 * rt * E2, C_LIN, 0.5)
    s.rect(LX, LY - R["tubo"]["ID"] / 2 * E2, L * E2, R["tubo"]["ID"] * E2, C_LIN, 0.35, dash="3,1.5")
    s.line(LX - 14, LY, LX + L * E2 + 14, LY, C_AUX, 0.3, "6,2,1,2")
    s.rect(LX - (R["eje"]["largo"] - L) / 2 * E2, LY - R["eje"]["D"] / 2 * E2,
           R["eje"]["largo"] * E2, R["eje"]["D"] * E2, C_LIN, 0.4)
    # carcasa y discos
    yc0 = (L - 2 * TB["y_ext"]) / 2
    s.rect(LX + yc0 * E2, LY - TB["OD"] / 2 * E2, 2 * TB["y_ext"] * E2, TB["OD"] * E2, C_CAR, 0.55)
    for sgn in (0, 1):
        yd = (L / 2 - TB["y_disco_int"] - TB["disco_esp"]) if sgn == 0 else (L / 2 + TB["y_disco_int"])
        s.rect(LX + yd * E2, LY - TB["ID"] / 2 * E2, TB["disco_esp"] * E2, TB["ID"] * E2, C_CAR, 0.4)
    s.text(LX + L * E2 / 2, LY - TB["OD"] / 2 * E2 - 2.0,
           "carcasa %s  +  2 discos con 6004-2RS" % TB["material"].split()[0], 2.3, C_CAR)

    for i in range(IM["n_filas"]):
        y0 = (L - GE["largo_activo"]) / 2 + i * IM["L"]
        for sgn, col in ((-1, "#C0392B"), (1, "#2563EB")):
            s.rect(LX + y0 * E2, LY + sgn * rt * E2 - (IM["T"] * E2 if sgn < 0 else 0),
                   IM["L"] * E2, IM["T"] * E2, col, 0.3, col)
    s.text(LX - 4, LY - rt * E2 - IM["T"] * E2 - 1.5, "N", 3.0, "#C0392B", "end", True)
    s.text(LX - 4, LY + rt * E2 + IM["T"] * E2 + 3.5, "S", 3.0, "#2563EB", "end", True)
    for sgn in (-1, 1):
        yc = (L - R["cubo"]["largo"]) / 2 if sgn > 0 else 0
        s.rect(LX + yc * E2, LY - R["cubo"]["OD"] / 2 * E2,
               R["cubo"]["largo"] * E2, R["cubo"]["OD"] * E2, C_AUX, 0.35)
    s.dim_h(LX, LX + L * E2, LY + TB["OD"] / 2 * E2 + 12, "tubo  " + fmt(L),
            LY + TB["OD"] / 2 * E2 + 2)
    s.dim_h(LX + (L - GE["largo_activo"]) / 2 * E2, LX + (L + GE["largo_activo"]) / 2 * E2,
            LY + TB["OD"] / 2 * E2 + 22, "activo  " + fmt(GE["largo_activo"]),
            LY + TB["OD"] / 2 * E2 + 2)

    # --- entrehierro indexado --------------------------------------------
    s.tabla(236, 148, "ENTREHIERRO INDEXADO  (H1)",
            [("manguito %s mm  ->  z = %s mm" % (fmt(p_, 1), fmt(z_, 1)),
              "F/F0 = " + fmt(f_, 3))
             for p_, z_, f_ in zip(TB["manguitos"]["pared"], EH["z_index"], EH["F_relativa"])]
            + [("galga bajo la subplaca", "%s mm" % fmt(EH["galga_max"], 1))], 122)
    s.text(238, 195, "z = %s zuncho + %s holgura + %s carcasa + %s banda"
           % (fmt(EH["z_zuncho"], 1), fmt(EH["z_holgura"], 1),
              fmt(EH["z_carcasa"], 1), fmt(EH["z_banda"], 1)), 2.3, C_LIN, "start")
    s.text(238, 199, "La razon (lambda/2pi)/(lambda/4pi) vale 2 POR ALGEBRA.",
           2.3, C_COT, "start", italic=True)
    s.text(238, 203, "H1 se comprueba MIDIENDO F(z) con la bobina de prueba.",
           2.3, C_COT, "start", italic=True)

    s.tabla(12, 190, "ROTOR", [
        ("Tubo", R["tubo"]["designacion"]),
        ("Pared / minimo por saturacion",
         fmt(R["tubo"]["pared"], 2) + " / " + fmt(R["tubo"]["pared_min_N52"], 2)),
        ("Imanes", "%d x N52 %sx%sx%s" % (R["iman"]["n_total"], fmt(IM["L"]),
                                          fmt(IM["W"]), fmt(IM["T"]))),
        ("Paso polar  lambda = pi D_r/p", fmt(GE["lambda"], 2) + " mm"),
        ("Decaim. del CAMPO  lambda/2pi", fmt(GE["lam_2pi"], 2) + " mm"),
        ("Decaim. de la FUERZA  lambda/4pi", fmt(GE["lam_4pi"], 2) + " mm"),
        ("Sagita: pieza de %s / POLO de %s" % (fmt(IM["W"]), fmt(GE["ancho_polo"])),
         fmt(GE["sagita_pieza"], 3) + " / " + fmt(GE["sagita_polo"], 3) + " mm"),
        ("Masa del rotor / del tambor",
         fmt(P["masas"]["m_rotor"], 2) + " / " + fmt(P["masas"]["m_tambor"], 2) + " kg"),
        ("Velocidad critica", fmt(P["mecanica"]["N_critica"], 0) + " rpm"),
    ], 122)

    # --- despiece del iman: en la COLUMNA IZQUIERDA, bajo la tabla, para
    # no invadir la caratula (que ocupa 324..412 x 251..289).
    BX, BY = 12.0, 239.0
    s.rect(BX, BY, 122.0, 50.0, C_LIN, 0.45, "#F9FAFB")
    s.text(BX + 4, BY + 6.5, "DESPIECE DEL IMAN", 2.9, C_LIN, "start", True)
    ex, ey, ke = BX + 16, BY + 17, 0.72
    s.rect(ex, ey, IM["L"] * ke, IM["W"] * ke, C_LIN, 0.5)
    s.dim_h(ex, ex + IM["L"] * ke, ey + IM["W"] * ke + 7, fmt(IM["L"]), ey + IM["W"] * ke + 1)
    s.dim_v(ey, ey + IM["W"] * ke, ex - 6, fmt(IM["W"]), ex)
    sx2 = ex + IM["L"] * ke + 26
    s.rect(sx2, ey, IM["T"] * ke * 2.6, IM["W"] * ke, C_LIN, 0.5)
    s.line(sx2 + IM["T"] * ke * 1.3, ey - 3.5, sx2 + IM["T"] * ke * 1.3,
           ey + IM["W"] * ke + 3.5, "#C0392B", 0.6)
    s._flecha(sx2 + IM["T"] * ke * 1.3, ey - 3.5, 0, -1)
    s.text(sx2 + IM["T"] * ke * 1.3, ey - 5.5, "N", 2.8, "#C0392B", "middle", True)
    s.text(sx2 + IM["T"] * ke * 1.3, ey + IM["W"] * ke + 7.5, "S", 2.8, "#2563EB", "middle", True)
    s.text(sx2 + IM["T"] * ke * 2.6 + 4, ey + IM["W"] * ke - 1,
           "espesor " + fmt(IM["T"]), 2.3, C_COT, "start")
    s.text(BX + 4, BY + 45, "MAGNETIZACION A TRAVES DE LOS %s mm" % fmt(IM["T"]),
           2.4, "#C0392B", "start", True)

    s.caratula([("Escala", "1:1 y 1:2  (A3)"), ("Cotas en", "milimetros"),
                ("Fuente", "master.yaml v%d" % P["meta"]["version_parametros"]),
                ("Fecha", HOY), ("Lamina", "3 de 3")])
    s.guardar("LAMINA3_rotor")


if __name__ == "__main__":
    print("VORTICE 150 v3 - laminas acotadas")
    lamina1()
    lamina2()
    lamina3()
    print("Listo.")
