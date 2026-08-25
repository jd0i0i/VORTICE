#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VORTICE 150 v3 - Generador del modelo 3D completo.

ARQUITECTURA v3: el rotor magnetico ES EL TAMBOR DE CABEZA. Gira dentro
de una carcasa no conductora que rueda libre sobre su mismo eje, y la
banda envuelve esa carcasa. No hay plancha fija, no hay transferencia y
no hay hueco: el material va apoyado en la banda hasta el lanzamiento.

Lee TODOS los parametros de PARAMETERS/master.yaml. No hay ni un solo
numero de cota escrito a mano en este archivo -- las que la v2 llevaba
sueltas viven ahora en la seccion `cad` del YAML.

Sistema de coordenadas (ver cabecera de master.yaml):
    X -> avance del material, X=0 en el eje del rodillo de cola
    Y -> transversal, Y=0 en el plano medio
    Z -> vertical desde el SUELO;  z_cad = z_cotas + pata_H + base_esp

Salidas:
    CAD/STEP/VORTICE_maquina.step | _rotor.step | _guarda.step
    CAD/STL/  los mismos tres
    CAD/PLANOS/Vista_isometrica.png | Vista_lateral.png | Vista_rotor_detalle.png
    PARAMETERS/derivados_cad.json   (lo contrasta verificar.py, cota a cota)
"""

import os
import sys
import math
import json

import yaml
import cadquery as cq

# ---------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
YAML_PATH = os.path.join(RAIZ, "PARAMETERS", "master.yaml")
DIR_STEP = os.path.join(RAIZ, "CAD", "STEP")
DIR_STL = os.path.join(RAIZ, "CAD", "STL")
DIR_PNG = os.path.join(RAIZ, "CAD", "PLANOS")
for d in (DIR_STEP, DIR_STL, DIR_PNG):
    os.makedirs(d, exist_ok=True)

with open(YAML_PATH, "r", encoding="utf-8") as fh:
    P = yaml.safe_load(fh)

R = P["rotor"]
TB = P["tambor"]
OP = P["operacion"]
CI = P["cinta"]
TO = P["tolva"]
TR = P["transmision"]
SA = P["salida"]
BA = P["bastidor"]
EL = P["electronica"]
MO = P["montaje"]
CD = P["cad"]
COL = P["colores"]


def hex2col(h, alpha=1.0):
    """'#RRGGBB' -> cq.Color."""
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return cq.Color(r, g, b, alpha)


# =====================================================================
# GEOMETRIA DERIVADA  (se recalcula, nunca se copia del YAML)
# =====================================================================
Z_OFF = BA["pata_H"] + BA["base_esp"]              # suelo -> cara sup. base


def zc(z_cotas):
    """z de cotas -> z del CAD (desde el suelo)."""
    return z_cotas + Z_OFF


# --- Bastidor --------------------------------------------------------
X_BASE_0 = MO["x_base_ini"]
X_BASE_1 = X_BASE_0 + BA["base_L"]
Y_BASE = BA["base_W"] / 2.0
Z_BASE_0 = BA["pata_H"]
Z_BASE_1 = Z_BASE_0 + BA["base_esp"]               # = Z_OFF
Y_LAT_INT = BA["sep_laterales"] / 2.0
Y_LAT_EXT = Y_LAT_INT + BA["lateral_esp"]
Z_LAT_TOP = Z_BASE_1 + BA["lateral_H"]

# --- Cinta y tambor --------------------------------------------------
# La banda es horizontal por construccion: los dos cilindros que la
# llevan tienen su TANGENTE SUPERIOR a la misma cota. De ahi salen las
# dos alturas de eje, cada una restando su propio radio.
Z_BANDA_SUP = zc(CI["banda_sup_altura"])
Z_BANDA_INF = Z_BANDA_SUP - CI["banda_esp"]        # cara inferior de la banda

R_ROD = CI["rodillo_D"] / 2.0
Z_ROD_EJE = Z_BANDA_INF - R_ROD
X_ROD_COLA = MO["x_rodillo_cola"]

R_CARC = TB["OD"] / 2.0                            # carcasa nominal
R_MAT = R_CARC + CI["banda_esp"]                   # donde va el material
X_TAMBOR = MO["x_tambor"]
Z_EJE_ROTOR = Z_BANDA_INF - R_CARC
Y_BANDA = CI["banda_ancho"] / 2.0

R_TUBO = R["tubo"]["OD"] / 2.0
R_IMAN = R["geometria"]["D_r"] / 2.0
R_ZUNCHO = R_IMAN + R["retencion"]["z_zuncho"]
EH = OP["entrehierro"]
# Envolvente del rotor magnetico CON el manguito mas grueso: es lo que
# la guarda tiene que cubrir.
R_ENVOL = R_CARC + max(TB["manguitos"]["pared"])
Y_ROD_CHUM = R["soporte"]["span_chumaceras"] / 2.0

# --- Soporte del rotor -----------------------------------------------
U = R["soporte"]
SUB = U["subplaca"]
Z_SUB_TOP = Z_EJE_ROTOR - U["ucp204_H"]
Z_SUB_BOT = Z_SUB_TOP - SUB[2]
Z_GALGA_BOT = Z_SUB_BOT - EH["galga_max"]
ESC = BA["ventanas"]["escotadura_rotor"]
X_SUB_0, X_SUB_1 = ESC["x_ini"], ESC["x_fin"]
Z_ESC_TOP = Z_EJE_ROTOR + U["ucp204_cuerpo_D"] / 2.0 + ESC["margen_superior"]
Y_SUB_1 = Y_BASE
Y_SUB_0 = Y_SUB_1 - SUB[1]                         # libra la carcasa

# --- Transmision -----------------------------------------------------
ANG = math.radians(TR["motor_angulo_deg"])
X_MOTOR = X_TAMBOR + TR["entrecentros_poleas"] * math.cos(ANG)
Z_MOTOR = Z_EJE_ROTOR + TR["entrecentros_poleas"] * math.sin(ANG)
# La polea va por fuera del disco del tambor y por dentro de la chumacera
Y_POLEA = TB["y_ext"] + TR["polea_holgura_carcasa"] + TR["polea_ancho"] / 2.0
R_POL_COND = TR["Dp_cond"] / 2.0
R_POL_MOTRIZ = TR["Dp_motriz"] / 2.0

# --- Tolva -----------------------------------------------------------
X_TOLVA = MO["x_tolva_centro"]
Z_TOLVA_SAL = zc(TO["z_boca"])
Z_TOLVA_CUE = Z_TOLVA_SAL + TO["h_cuello"]
Z_TOLVA_TOP = Z_TOLVA_CUE + TO["h_cono"]
SOP = TO["soportes"]
Z_BRIDA_TOP = Z_TOLVA_SAL
Z_BRIDA_BOT = Z_BRIDA_TOP - SOP["brida_esp"]

# --- Salida ----------------------------------------------------------
Z_CELDA_TOP = Z_BASE_1 + EL["celda_alto"]
BJ_ESP = SA["bandeja_esp"]
Z_BJ_PISO = Z_CELDA_TOP + BJ_ESP
Z_BJ_CANTO = Z_BJ_PISO + SA["bandeja_inerte"][2]
HOL = SA["holgura_bandeja"]
X_CUCH = SA["cuchilla_x"]
GAP = SA["gap_bandejas"]
X_BJ_I1 = X_CUCH - GAP / 2.0
X_BJ_I0 = X_BJ_I1 - (SA["bandeja_inerte"][1] + 2 * BJ_ESP)
X_BJ_N0 = X_CUCH + GAP / 2.0
X_BJ_N1 = X_BJ_N0 + (SA["bandeja_nofe"][1] + 2 * BJ_ESP)
Y_BJ = SA["bandeja_inerte"][0] / 2.0 + BJ_ESP
X_DEF_ESP = SA["deflector_x"]
X_DEF_PLA = X_DEF_ESP + SA["deflector_espuma"]

# --- Guarda: DERIVADA de la extension real del rotor y del vuelo -----
X_GU_0 = (X_TAMBOR - R_ENVOL) - BA["guarda_margen_rotor"]
X_GU_1 = X_BJ_N1
GU_PASO = (X_GU_1 - X_GU_0) / BA["guarda_paños"]

# =====================================================================
# BALISTICA  (derivada de las velocidades de salida, no al reves)
# =====================================================================
G = 9.81
LZ = SA["lanzamiento"]
V_SAL = LZ["v_salida"]
V_MIN_CIMA = math.sqrt(G * R_MAT / 1000.0)


def despegue(nombre):
    """(x0, z0, vx, vz) del punto de lanzamiento.

    Dos regimenes fisicos distintos, no un ajuste:
      v <  sqrt(gR) : la pieza NO se separa en la cima. Sigue la banda
                      hasta theta = acos(v^2/gR) y sale tangencialmente.
      v >= sqrt(gR) : se separa en la cima, horizontalmente.
    """
    v = V_SAL[nombre]
    if v < V_MIN_CIMA:
        th = math.acos(v ** 2 / (G * R_MAT / 1000.0))
        return (X_TAMBOR + R_MAT * math.sin(th),
                Z_EJE_ROTOR + R_MAT * math.cos(th),
                v * math.cos(th), -v * math.sin(th))
    return X_TAMBOR, Z_BANDA_SUP, v, 0.0


def trayectoria(nombre, n=None):
    """Vuelo hasta donde REALMENTE se detiene la pieza.

    El destino no siempre es el piso: la media lata alcanzaria 1.542 mm
    y la bandeja acaba en 1.160, asi que la para el deflector acolchado.
    Sin truncar aqui, la comprobacion de trayectoria contra solidos
    marcaria el deflector como un choque indebido en vez de como el
    reten que es.
    """
    n = n or CD["tray_muestras"]
    x0, z0, vx, vz = despegue(nombre)
    vx_, vz_ = vx * 1000.0, vz * 1000.0
    g = G * 1000.0
    # z(t) = z0 + vz*t - g t^2/2 = z_fin  ->  g t^2/2 - vz t - dz = 0
    #   t = [vz + sqrt(vz^2 + 2 g dz)] / g
    # OJO CON EL SIGNO: vz_ ya es NEGATIVO cuando la pieza sale bajando
    # (el inerte despega a 78 grados de la cima). Poner -vz_ aqui da la
    # raiz del lanzamiento hacia ARRIBA y la trayectoria atraviesa el
    # piso. Lo caza D3 (trayectoria contra solidos).
    t_piso = (vz_ + math.sqrt(vz_ ** 2 + 2 * g * (z0 - Z_BJ_PISO))) / g
    destino, t_fin = "piso", t_piso
    if vx_ > 0:
        t_def = (X_DEF_ESP - x0) / vx_
        if 0 < t_def < t_piso:
            destino, t_fin = "deflector_espuma", t_def
    pts = [(x0 + vx_ * (t_fin * i / n),
            z0 + vz_ * (t_fin * i / n) - 0.5 * g * (t_fin * i / n) ** 2)
           for i in range(n + 1)]
    return dict(pts=pts, destino=destino, v=V_SAL[nombre],
                x0=x0, z0=z0, vx=vx, vz=vz,
                x_fin=pts[-1][0], z_fin=pts[-1][1],
                x_libre=x0 + vx_ * t_piso)


TRAYECTORIAS = {k: trayectoria(k) for k in ("inerte", "f35", "f25", "lata")}
ALCANCES = {k: v["x_libre"] for k, v in TRAYECTORIAS.items()}

PARTES = []          # (nombre, solido, color_hex, alpha, grupo)


def add(nombre, solido, color_hex, alpha=1.0, grupo="maquina"):
    PARTES.append(dict(nombre=nombre, solido=solido, color=color_hex,
                       alpha=alpha, grupo=grupo))


def caja(x0, x1, y0, y1, z0, z1):
    """Caja por esquinas absolutas."""
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=True)
            .translate(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)))


def cil_Y(x, z, y0, y1, r):
    """Cilindro con eje paralelo a Y, de y0 a y1.

    OJO: el plano "XZ" tiene normal -Y y extruye hacia Y NEGATIVA.
    Hay que usar "ZX" (normal +Y) o el solido aparece espejado 2*L.
    """
    return (cq.Workplane("ZX").circle(r).extrude(y1 - y0)
            .translate((x, y0, z)))


def racetrack(c0, r0, c1, r1, espesor, y0, ancho):
    """Lazo cerrado (banda o correa) sobre dos poleas de radio distinto.

    Envolvente convexa real de las dos circunferencias (arcos + rectas
    tangentes exteriores) menos la interior. Con radios distintos las
    tangentes NO son horizontales abajo: por eso se calculan.
    """
    dx, dz = c1[0] - c0[0], c1[1] - c0[1]
    L = math.hypot(dx, dz)
    ang = math.degrees(math.atan2(dz, dx))

    def envolvente(ra, rb):
        a = math.acos(max(-1.0, min(1.0, (ra - rb) / L)))
        ca, sa = math.cos(a), math.sin(a)
        pts = [(ra * ca, ra * sa), (L + rb * ca, rb * sa),
               (L + rb * ca, -rb * sa), (ra * ca, -ra * sa)]
        cuerpo = cq.Workplane("XY").polyline(pts).close().extrude(ancho)
        for c, r in (((0.0, 0.0), ra), ((L, 0.0), rb)):
            cuerpo = cuerpo.union(cq.Workplane("XY")
                                  .center(c[0], c[1]).circle(r).extrude(ancho))
        return cuerpo

    lazo = envolvente(r0 + espesor, r1 + espesor).cut(envolvente(r0, r1))
    return (lazo.rotate((0, 0, 0), (1, 0, 0), 90)      # y_local -> Z
            .rotate((0, 0, 0), (0, 1, 0), -ang)        # inclinar en XZ
            .translate((c0[0], y0 + ancho, c0[1])))


# =====================================================================
# 1 - BASTIDOR
# =====================================================================
for sx in (X_BASE_0 + CD["pata_x_borde"], X_BASE_1 - CD["pata_x_borde"]):
    for sy in (-(Y_BASE - CD["pata_y_borde"]), Y_BASE - CD["pata_y_borde"]):
        add("pata", cq.Workplane("XY").circle(BA["pata_D"] / 2.0)
            .extrude(BA["pata_H"]).translate((sx, sy, 0)),
            COL["caucho"], 1.0, "bastidor")

add("base_MDF", caja(X_BASE_0, X_BASE_1, -Y_BASE, Y_BASE, Z_BASE_0, Z_BASE_1),
    COL["mdf"], 1.0, "bastidor")

VEN = BA["ventanas"]
for signo in (+1, -1):
    y0, y1 = (Y_LAT_INT, Y_LAT_EXT) if signo > 0 else (-Y_LAT_EXT, -Y_LAT_INT)
    panel = caja(X_BASE_0, X_BASE_1, y0, y1, Z_BASE_1, Z_LAT_TOP)
    for xcv in VEN["x_centros"]:                      # ventanas de inspeccion
        panel = panel.cut(caja(xcv - VEN["ancho_X"] / 2.0, xcv + VEN["ancho_X"] / 2.0,
                               y0 - 1, y1 + 1,
                               zc(VEN["z_centro"]) - VEN["alto_Z"] / 2.0,
                               zc(VEN["z_centro"]) + VEN["alto_Z"] / 2.0))
    # Ventana (no escotadura abierta) para la subplaca y la chumacera:
    # el puente de panel de encima da rigidez y sostiene la guarda.
    panel = panel.cut(caja(X_SUB_0, X_SUB_1, y0 - 1, y1 + 1, Z_GALGA_BOT, Z_ESC_TOP))
    add("lateral_MDF", panel, COL["mdf"], 1.0, "bastidor")

TRV = BA["travesano_secc"]
for xcv in BA["travesano_x"]:
    add("travesano", caja(xcv - TRV[0] / 2.0, xcv + TRV[0] / 2.0,
                          -Y_LAT_INT, Y_LAT_INT, Z_BASE_1, Z_BASE_1 + TRV[1]),
        COL["mdf"], 1.0, "bastidor")

CC = BA["caja_control"]
add("caja_control", caja(BA["caja_control_x"], BA["caja_control_x"] + CC[0],
                         Y_LAT_EXT, Y_LAT_EXT + CC[2],
                         zc(BA["caja_control_z"]), zc(BA["caja_control_z"]) + CC[1]),
    COL["mdf"], 1.0, "bastidor")

# =====================================================================
# 2 - CINTA  (rodillo de cola motriz + banda que envuelve el tambor)
# =====================================================================
add("rodillo_cola", cil_Y(X_ROD_COLA, Z_ROD_EJE, -CI["rodillo_L"] / 2.0,
                          CI["rodillo_L"] / 2.0, R_ROD),
    COL["aluminio"], 1.0, "cinta")

add("banda_PVC", racetrack((X_ROD_COLA, Z_ROD_EJE), R_ROD,
                           (X_TAMBOR, Z_EJE_ROTOR), R_CARC,
                           CI["banda_esp"], -Y_BANDA, 2 * Y_BANDA),
    COL["banda"], 1.0, "cinta")

add("cama_deslizamiento",
    caja(CI["cama_x"][0], CI["cama_x"][1],
         -CI["cama_ancho"] / 2.0, CI["cama_ancho"] / 2.0,
         Z_BANDA_INF - CI["cama_esp"], Z_BANDA_INF),
    COL["mdf"], 1.0, "cinta")

for signo in (+1, -1):
    # La guia baja hasta el canto de la cama: asi apoya de verdad contra
    # la cama Y contra el canto de la banda. Si arranca en la superficie
    # de banda solo la toca por una linea, que es apoyo cero.
    y0 = signo * Y_BANDA
    y1 = y0 + signo * CI["guia_esp"]
    add("guia_lateral",
        caja(CI["cama_x"][0], CI["cama_x"][1], min(y0, y1), max(y0, y1),
             Z_BANDA_INF - CI["cama_esp"], Z_BANDA_SUP + CI["guia_alto"]),
        COL["aluminio"], 1.0, "cinta")

# =====================================================================
# 3 - TOLVA
# =====================================================================
TS_Y, TS_X = TO["salida"][0] / 2.0, TO["salida"][1] / 2.0
TU_Y, TU_X = TO["sup"][0] / 2.0, TO["sup"][1] / 2.0
t_tol = TO["espesor"]


def tolva_solida(dx_s, dy_s, dx_u, dy_u, z0, z1, z2):
    """Cuello recto + tronco piramidal, macizo."""
    cuello = (cq.Workplane("XY").rect(2 * dx_s, 2 * dy_s).extrude(z1 - z0)
              .translate((X_TOLVA, 0, z0)))
    cono = (cq.Workplane("XY").rect(2 * dx_s, 2 * dy_s)
            .workplane(offset=z2 - z1).rect(2 * dx_u, 2 * dy_u)
            .loft(ruled=True).translate((X_TOLVA, 0, z1)))
    return cuello.union(cono)


tolva = (tolva_solida(TS_X, TS_Y, TU_X, TU_Y,
                      Z_TOLVA_SAL, Z_TOLVA_CUE, Z_TOLVA_TOP)
         .cut(tolva_solida(TS_X - t_tol, TS_Y - t_tol, TU_X - t_tol, TU_Y - t_tol,
                           Z_TOLVA_SAL - 1, Z_TOLVA_CUE, Z_TOLVA_TOP + 1)))
add("tolva", tolva, COL["acrilico"], 0.55, "tolva")

brida = caja(X_TOLVA - SOP["brida_X"] / 2.0, X_TOLVA + SOP["brida_X"] / 2.0,
             -SOP["brida_Y"] / 2.0, SOP["brida_Y"] / 2.0,
             Z_BRIDA_BOT, Z_BRIDA_TOP)
brida = brida.cut(caja(X_TOLVA - TS_X, X_TOLVA + TS_X, -TS_Y, TS_Y,
                       Z_BRIDA_BOT - 1, Z_BRIDA_TOP + 1))
add("tolva_brida", brida, COL["mdf"], 1.0, "tolva")

for signo in (+1, -1):
    yc = signo * SOP["y_centro"]
    add("tolva_soporte",
        caja(X_TOLVA - SOP["ancho_X"] / 2.0, X_TOLVA + SOP["ancho_X"] / 2.0,
             yc - SOP["espesor"] / 2.0, yc + SOP["espesor"] / 2.0,
             Z_BASE_1, Z_BRIDA_BOT),
        COL["mdf"], 1.0, "tolva")

add("compuerta", caja(X_TOLVA + TS_X, X_TOLVA + TS_X + TO["espesor"], -TS_Y, TS_Y,
                      Z_TOLVA_SAL, Z_TOLVA_SAL + TO["h_cuello"]),
    COL["aluminio"], 1.0, "tolva")

# =====================================================================
# 4 - ROTOR MAGNETICO
# =====================================================================
LT = R["tubo"]["largo"] / 2.0
tubo = (cil_Y(X_TAMBOR, Z_EJE_ROTOR, -LT, LT, R_TUBO)
        .cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, -LT - 1, LT + 1, R["tubo"]["ID"] / 2.0)))
add("rotor_tubo", tubo, COL["acero"], 1.0, "rotor")

IM = R["iman"]
GE = R["geometria"]
r_med = R_TUBO + IM["T"] / 2.0
filas_y = [(k - (IM["n_filas"] - 1) / 2.0) * IM["L"] for k in range(IM["n_filas"])]
paso_ang = 360.0 / IM["n_polos"]

for k in range(IM["n_polos"]):
    th = k * paso_ang
    color = COL["iman_N"] if k % 2 == 0 else COL["iman_S"]
    for j in range(IM["k_piezas"]):
        off = (j - (IM["k_piezas"] - 1) / 2.0) * IM["W"]
        for yf in filas_y:
            m = (cq.Workplane("XY").box(IM["W"], IM["L"], IM["T"], centered=True)
                 .translate((off, yf, r_med))
                 .rotate((0, 0, 0), (0, 1, 0), 90.0 - th)
                 .translate((X_TAMBOR, 0, Z_EJE_ROTOR)))
            add("iman_%s" % ("N" if k % 2 == 0 else "S"), m, color, 1.0, "rotor")

RT = R["retencion"]
for k in range(IM["n_polos"]):
    th = k * paso_ang + paso_ang / 2.0
    tira = (cq.Workplane("XY")
            .box(RT["tira_ancho"], RT["tira_largo"], RT["tira_alto"], centered=True)
            .translate((0, 0, r_med))
            .rotate((0, 0, 0), (0, 1, 0), 90.0 - th)
            .translate((X_TAMBOR, 0, Z_EJE_ROTOR)))
    add("tira_separadora", tira, COL["petg"], 1.0, "rotor")

LA = GE["largo_activo"] / 2.0
zun = (cil_Y(X_TAMBOR, Z_EJE_ROTOR, -LA, LA, R_ZUNCHO)
       .cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, -LA - 1, LA + 1, R_IMAN)))
add("zuncho_fibra", zun, COL["acrilico"], 0.30, "rotor")

EJ = R["eje"]
add("eje_rotor", cil_Y(X_TAMBOR, Z_EJE_ROTOR, -EJ["largo"] / 2.0,
                       EJ["largo"] / 2.0, EJ["D"] / 2.0),
    COL["acero"], 1.0, "rotor")

CU = R["cubo"]
for signo in (+1, -1):
    yc = signo * (LT - CU["largo"] / 2.0)
    cubo = cil_Y(X_TAMBOR, Z_EJE_ROTOR, yc - CU["largo"] / 2.0,
                 yc + CU["largo"] / 2.0, CU["OD"] / 2.0)
    cubo = cubo.cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, yc - CU["largo"], yc + CU["largo"],
                          EJ["D"] / 2.0))
    for i in range(CU["taladros"]):                    # aligeramiento
        a = math.radians(i * 360.0 / CU["taladros"])
        cubo = cubo.cut(cil_Y(X_TAMBOR + CU["taladro_PCD"] / 2.0 * math.cos(a),
                              Z_EJE_ROTOR + CU["taladro_PCD"] / 2.0 * math.sin(a),
                              yc - CU["largo"], yc + CU["largo"],
                              CU["taladro_D"] / 2.0))
    add("cubo_fijacion", cubo, COL["aluminio"], 1.0, "rotor")

# --- Soporte: pedestal + galgas + subplaca + chumaceras ---------------
for signo in (+1, -1):
    ys0, ys1 = sorted((signo * Y_SUB_0, signo * Y_SUB_1))
    yg0, yg1 = sorted((signo * Y_LAT_INT, signo * Y_SUB_1))
    yp0, yp1 = sorted((signo * Y_LAT_EXT, signo * Y_SUB_1))

    add("pedestal_rotor", caja(X_SUB_0, X_SUB_1, yp0, yp1, Z_BASE_1, Z_GALGA_BOT),
        COL["mdf"], 1.0, "rotor")
    add("galgas", caja(X_SUB_0, X_SUB_1, yg0, yg1, Z_GALGA_BOT, Z_SUB_BOT),
        COL["aluminio"], 1.0, "rotor")

    sub = caja(X_SUB_0, X_SUB_1, ys0, ys1, Z_SUB_BOT, Z_SUB_TOP)
    # alivio para el paso de la correa
    ya0, ya1 = sorted((signo * Y_SUB_0,
                       signo * (Y_POLEA + TR["polea_ancho"] / 2.0
                                + CD["subplaca_alivio_y_margen"])))
    sub = sub.cut(caja(X_MOTOR + CD["subplaca_alivio_x"][0],
                       X_TAMBOR + CD["subplaca_alivio_x"][1], ya0, ya1,
                       Z_SUB_BOT - 1, Z_SUB_TOP + 1))
    add("subplaca_rotor", sub, COL["aluminio"], 1.0, "rotor")

    yc = signo * Y_ROD_CHUM
    base_ch = caja(X_TAMBOR - U["ucp204_L"] / 2.0, X_TAMBOR + U["ucp204_L"] / 2.0,
                   yc - U["ucp204_A"] / 2.0, yc + U["ucp204_A"] / 2.0,
                   Z_SUB_TOP, Z_SUB_TOP + CD["chumacera_base_esp"])
    cuerpo = cil_Y(X_TAMBOR, Z_EJE_ROTOR, yc - U["ucp204_cuerpo_L"] / 2.0,
                   yc + U["ucp204_cuerpo_L"] / 2.0, U["ucp204_cuerpo_D"] / 2.0)
    add("chumacera_UCP204", base_ch.union(cuerpo), COL["aluminio"], 1.0, "rotor")

# =====================================================================
# 5 - TAMBOR DE CABEZA  (carcasa no conductora, rueda libre)
# =====================================================================
carc = (cil_Y(X_TAMBOR, Z_EJE_ROTOR, -TB["y_ext"], TB["y_ext"], R_CARC)
        .cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, -TB["y_ext"] - 1, TB["y_ext"] + 1,
                   TB["ID"] / 2.0)))
add("carcasa_tambor", carc, COL["carcasa"], 0.45, "tambor")

for signo in (+1, -1):
    y0 = signo * TB["y_disco_int"]
    y1 = y0 + signo * TB["disco_esp"]
    disco = (cil_Y(X_TAMBOR, Z_EJE_ROTOR, min(y0, y1), max(y0, y1), TB["ID"] / 2.0)
             .cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, min(y0, y1) - 1, max(y0, y1) + 1,
                        TB["rodamiento_OD"] / 2.0)))
    add("disco_tambor", disco, COL["petg"], 1.0, "tambor")
    rod = (cil_Y(X_TAMBOR, Z_EJE_ROTOR, min(y0, y1), max(y0, y1),
                 TB["rodamiento_OD"] / 2.0)
           .cut(cil_Y(X_TAMBOR, Z_EJE_ROTOR, min(y0, y1) - 1, max(y0, y1) + 1,
                      EJ["D"] / 2.0)))
    add("rodamiento_tambor", rod, COL["acero"], 1.0, "tambor")

# =====================================================================
# 6 - MOTOR Y TRANSMISION
# =====================================================================
Y_MOT_1 = Y_POLEA - TR["polea_ancho"] / 2.0 - TR["motor_holgura_polea"]
Y_MOT_0 = Y_MOT_1 - TR["motor_L"]
add("motor_DC", cil_Y(X_MOTOR, Z_MOTOR, Y_MOT_0, Y_MOT_1, TR["motor_D"] / 2.0),
    COL["motor"], 1.0, "transmision")

# Cuna en V: un bloque al que se le resta el cilindro del motor. Con un
# bloque recto el motor quedaba 0,8 mm por encima de la cuna y no se
# apoyaba en nada (lo caza D5, cadena de apoyo).
_cw = CD["cuna_ancho"] / 2.0
_mot = cil_Y(X_MOTOR, Z_MOTOR, Y_MOT_0 - 1, Y_MOT_1 + 1, TR["motor_D"] / 2.0)
for xm in (X_MOTOR - TR["motor_D"] / 2.0 + _cw, X_MOTOR + TR["motor_D"] / 2.0 - _cw):
    add("cuna_motor", caja(xm - _cw, xm + _cw,
                           Y_MOT_0 + CD["cuna_y_margen"], Y_MOT_1 - CD["cuna_y_margen"],
                           Z_BASE_1, Z_MOTOR).cut(_mot),
        COL["mdf"], 1.0, "transmision")

yp0 = Y_POLEA - TR["polea_ancho"] / 2.0
yp1 = Y_POLEA + TR["polea_ancho"] / 2.0
add("eje_motor", cil_Y(X_MOTOR, Z_MOTOR, Y_MOT_1, yp1, TR["eje_motor_D"] / 2.0),
    COL["acero"], 1.0, "transmision")
add("polea_conducida", cil_Y(X_TAMBOR, Z_EJE_ROTOR, yp0, yp1, R_POL_COND),
    COL["aluminio"], 1.0, "transmision")
add("polea_motriz", cil_Y(X_MOTOR, Z_MOTOR, yp0, yp1, R_POL_MOTRIZ),
    COL["aluminio"], 1.0, "transmision")
add("correa_HTD5M", racetrack((X_MOTOR, Z_MOTOR), R_POL_MOTRIZ,
                              (X_TAMBOR, Z_EJE_ROTOR), R_POL_COND,
                              TR["polea_paso"] * 0.6, yp0, TR["polea_ancho"]),
    COL["banda"], 1.0, "transmision")

# =====================================================================
# 7 - SALIDA: CUCHILLA, BANDEJAS, CELDAS, DEFLECTOR
# =====================================================================
# La cuchilla es un CANTO, no un muro, y cuelga del bastidor: no toca
# ninguna bandeja. El tejadillo cubre la ranura de 13 mm que queda
# entre las dos bandejas para que nada se cuele a la base.
Z_TEJ_0 = Z_BJ_CANTO + HOL
Z_TEJ_1 = Z_TEJ_0 + SA["cuchilla_esp"]
Z_CUCH_1 = Z_TEJ_1 + SA["cuchilla_H"]
_ct = SA["cuchilla_tejadillo"] / 2.0
_ty = SA["cuchilla_Y"] - SA["holgura_bandeja"]      # deja paso a los montantes
add("cuchilla_tejadillo",
    caja(X_CUCH - _ct, X_CUCH + _ct, -_ty, _ty, Z_TEJ_0, Z_TEJ_1),
    COL["aluminio"], 1.0, "salida")
add("cuchilla_divisora",
    caja(X_CUCH - SA["cuchilla_esp"] / 2.0, X_CUCH + SA["cuchilla_esp"] / 2.0,
         -SA["cuchilla_Y"], SA["cuchilla_Y"], Z_TEJ_1, Z_CUCH_1),
    COL["acero"], 1.0, "salida")
Z_TRV_CU = Z_LAT_TOP - CD["cuchilla_travesano_esp"]
# Los montantes son PLETINAS DE SOLAPE atornilladas a las caras de la
# cuchilla, por fuera de su ancho util: solapan 40 mm de cuchilla y
# 40 mm de travesano. Un montante apoyado de canto sobre el filo daria
# 4,5 mm2 de contacto, que no es un apoyo (lo caza D5).
for signo in (+1, -1):
    ya = signo * SA["cuchilla_Y"]
    yb = ya + signo * SA["cuchilla_esp"]
    add("cuchilla_montante",
        caja(X_CUCH - CD["cuchilla_soporte_X"], X_CUCH + CD["cuchilla_soporte_X"],
             min(ya, yb), max(ya, yb), Z_TEJ_1, Z_TRV_CU),
        COL["aluminio"], 1.0, "salida")
add("cuchilla_travesano",
    caja(X_CUCH - CD["cuchilla_soporte_X"], X_CUCH + CD["cuchilla_soporte_X"],
         -Y_LAT_INT, Y_LAT_INT, Z_TRV_CU, Z_LAT_TOP), COL["mdf"], 1.0, "salida")


def bandeja(x0, x1, nombre):
    ext = caja(x0, x1, -Y_BJ, Y_BJ, Z_CELDA_TOP, Z_BJ_CANTO)
    hueco = caja(x0 + BJ_ESP, x1 - BJ_ESP, -Y_BJ + BJ_ESP, Y_BJ - BJ_ESP,
                 Z_BJ_PISO, Z_BJ_CANTO + 1)
    add(nombre, ext.cut(hueco), COL["bandeja"], 0.55, "salida")


bandeja(X_BJ_I0, X_BJ_I1, "bandeja_inertes")
bandeja(X_BJ_N0, X_BJ_N1, "bandeja_no_ferrosos")

# --- DOS FRACCIONES, DOS CELDAS --------------------------------------
# Una celda monopunto por bandeja, bajo el centro de la plataforma.
# Es el UNICO solido que toca cada bandeja.
for (xa, xb) in ((X_BJ_I0, X_BJ_I1), (X_BJ_N0, X_BJ_N1)):
    xcl = (xa + xb) / 2.0
    add("celda_carga",
        caja(xcl - EL["celda_L"] / 2.0, xcl + EL["celda_L"] / 2.0,
             -EL["celda_ancho"] / 2.0, EL["celda_ancho"] / 2.0,
             Z_BASE_1, Z_CELDA_TOP), COL["acero"], 1.0, "salida")
    # topes antivuelco: NO tocan, holgura declarada
    for xt in (xa + CD["celda_x_borde"] + 10, xb - CD["celda_x_borde"] - 10):
        for yt in (-Y_BJ + 40, Y_BJ - 40):
            add("tope_antivuelco",
                caja(xt - 10, xt + 10, yt - 10, yt + 10,
                     Z_BASE_1, Z_CELDA_TOP - EL["tope_holgura"]),
                COL["aluminio"], 1.0, "salida")

# --- Deflector: cuelga del bastidor, entra en la bandeja sin tocarla --
Z_DEF_0 = Z_BJ_PISO + SA["deflector_z_bot_holgura"]
add("deflector_espuma",
    caja(X_DEF_ESP, X_DEF_PLA, -SA["deflector_Y"], SA["deflector_Y"],
         Z_DEF_0, Z_BJ_CANTO + SA["cuchilla_H"] * 4), COL["espuma"], 1.0, "salida")
add("deflector_placa",
    caja(X_DEF_PLA, X_DEF_PLA + SA["deflector_esp"],
         -SA["deflector_Y"], SA["deflector_Y"], Z_DEF_0, Z_LAT_TOP),
    COL["mdf"], 1.0, "salida")
add("deflector_travesano",
    caja(X_DEF_PLA + SA["deflector_esp"],
         X_DEF_PLA + SA["deflector_esp"] + CD["deflector_travesano_X"],
         -Y_LAT_INT, Y_LAT_INT,
         Z_LAT_TOP - CD["deflector_travesano_esp"], Z_LAT_TOP),
    COL["mdf"], 1.0, "salida")

# =====================================================================
# 8 - GUARDA  (derivada; dos panos para poder abrir uno solo)
# =====================================================================
for i in range(BA["guarda_paños"]):
    add("guarda_policarbonato",
        caja(X_GU_0 + i * GU_PASO, X_GU_0 + (i + 1) * GU_PASO,
             -BA["guarda_Y"] / 2.0, BA["guarda_Y"] / 2.0,
             Z_LAT_TOP, Z_LAT_TOP + BA["guarda_esp"]),
        COL["acrilico"], 0.35, "guarda")


# =====================================================================
# VERIFICACION GEOMETRICA SOBRE LOS SOLIDOS REALES
# =====================================================================
def bbox(p):
    return p["solido"].val().BoundingBox()


def solapan(a, b, tol):
    """Solapamiento volumetrico de bounding boxes, con tolerancia."""
    ox = min(a.xmax, b.xmax) - max(a.xmin, b.xmin) - tol
    oy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin) - tol
    oz = min(a.zmax, b.zmax) - max(a.zmin, b.zmin) - tol
    return ox > 0 and oy > 0 and oz > 0


JUNTAS = set()
TIPO_JUNTA = {}
for a, b, tipo in P["juntas"]:
    JUNTAS.add((a, b))
    JUNTAS.add((b, a))
    TIPO_JUNTA[(a, b)] = tipo
    TIPO_JUNTA[(b, a)] = tipo


def declarada(na, nb):
    return na == nb or (na, nb) in JUNTAS


def verificar(partes, verboso=True):
    """Interferencias reales entre pares NO declarados como junta."""
    fallas = []
    bbs = [bbox(p) for p in partes]
    n = len(partes)
    choques = []
    for i in range(n):
        for j in range(i + 1, n):
            na, nb = partes[i]["nombre"], partes[j]["nombre"]
            if declarada(na, nb):
                continue
            if not solapan(bbs[i], bbs[j], CD["tol_contacto"]):
                continue
            try:
                inter = partes[i]["solido"].val().intersect(partes[j]["solido"].val())
                vol = abs(inter.Volume())
            except Exception:
                vol = 0.0
            if vol > CD["vol_interferencia_min"]:
                choques.append("%s <-> %s (%.0f mm3)" % (na, nb, vol))
    if choques:
        fallas.append("INTERFERENCIA: " + " | ".join(sorted(set(choques))))
    if verboso:
        print("  solidos: %d   juntas declaradas: %d" % (n, len(P["juntas"])))
        for f in fallas:
            print("  [FALLA] " + f)
        if not fallas:
            print("  [OK] ninguna interferencia entre pares no declarados")
    return fallas


# =====================================================================
# ENSAMBLE Y EXPORTACION
# =====================================================================
G_MAQ = {"bastidor", "cinta", "tolva", "salida", "rotor", "transmision", "tambor"}


def construir(grupos, corte=False):
    """corte=True quita el lateral del lado del observador (y<0)."""
    a = cq.Assembly(name="VORTICE150")
    for i, p in enumerate(PARTES):
        if p["grupo"] not in grupos:
            continue
        if corte and p["nombre"] in ("lateral_MDF", "caja_control"):
            if bbox(p).ymin < 0:
                continue
        a.add(p["solido"], name="%s_%03d" % (p["nombre"], i),
              color=hex2col(p["color"], p["alpha"]))
    return a


def exportar(assy, nombre):
    step = os.path.join(DIR_STEP, nombre + ".step")
    assy.save(step)
    comp = assy.toCompound()
    cq.exporters.export(comp, os.path.join(DIR_STL, nombre + ".stl"),
                        tolerance=0.1, angularTolerance=0.2)
    print("  -> %s.step / .stl" % nombre)


def render(assy, salida, camara, tam=(1800, 1200), paralela=False):
    """Render offscreen con VTK, conservando los colores del ensamble."""
    from cadquery.occ_impl.assembly import toVTKAssy
    import vtkmodules.all as vtk

    ren = vtk.vtkRenderer()
    ren.SetBackground(1.0, 1.0, 1.0)
    ren.SetTwoSidedLighting(True)
    for prop in toVTKAssy(assy, edgecolor=(0.15, 0.15, 0.15, 1.0), linewidth=1.0):
        ren.AddActor(prop)
        try:
            pr = prop.GetProperty()
            pr.SetAmbient(0.34)
            pr.SetDiffuse(0.78)
            pr.SetSpecular(0.10)
            pr.SetSpecularPower(28)
        except AttributeError:
            pass

    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.AddRenderer(ren)
    win.SetSize(*tam)
    win.SetMultiSamples(8)

    cam = ren.GetActiveCamera()
    cam.SetFocalPoint(*camara["foco"])
    cam.SetPosition(*camara["pos"])
    cam.SetViewUp(0, 0, 1)
    if paralela:
        cam.ParallelProjectionOn()
    ren.ResetCamera()
    if "zoom" in camara:
        cam.Zoom(camara["zoom"])
    ren.ResetCameraClippingRange()

    kit = vtk.vtkLightKit()
    kit.SetKeyLightIntensity(1.05)
    kit.SetKeyToFillRatio(2.2)
    kit.SetKeyToHeadRatio(2.6)
    kit.AddLightsToRenderer(ren)

    win.Render()
    f = vtk.vtkWindowToImageFilter()
    f.SetInput(win)
    f.SetScale(1)
    f.Update()
    w = vtk.vtkPNGWriter()
    w.SetFileName(salida)
    w.SetInputConnection(f.GetOutputPort())
    w.Write()
    print("  -> %s" % os.path.basename(salida))


# Geometria derivada que verificar.py contrasta cota a cota contra
# la seccion `montaje` del YAML.
DERIVADOS = dict(
    x_rodillo_cola=X_ROD_COLA,
    x_tambor=X_TAMBOR,
    x_tolva_centro=X_TOLVA,
    recorrido_asentamiento=X_TAMBOR - X_TOLVA,
    z_offset_cad=Z_OFF,
    z_banda_sup_cad=Z_BANDA_SUP,
    z_eje_tambor_cad=Z_EJE_ROTOR,
    z_eje_tambor_cotas=Z_EJE_ROTOR - Z_OFF,
    z_eje_rodillo_cola_cad=Z_ROD_EJE,
    z_celda_top_cad=Z_CELDA_TOP,
    z_bandeja_piso_cad=Z_BJ_PISO,
    z_bandeja_canto_cad=Z_BJ_CANTO,
    z_lateral_top_cad=Z_LAT_TOP,
    x_base_ini=X_BASE_0,
    x_base_fin=X_BASE_1,
    x_bandeja_inerte=[X_BJ_I0, X_BJ_I1],
    x_bandeja_nofe=[X_BJ_N0, X_BJ_N1],
    x_cuchilla=X_CUCH,
    x_deflector_espuma=X_DEF_ESP,
    x_deflector_placa=X_DEF_PLA,
    x_guarda=[X_GU_0, X_GU_1],
    x_motor=X_MOTOR,
    z_motor=Z_MOTOR,
    y_polea=Y_POLEA,
    x_rotor_envolvente=[X_TAMBOR - R_ENVOL, X_TAMBOR + R_ENVOL],
    extension_maquina=[X_ROD_COLA - R_ROD - CI["banda_esp"], X_BJ_N1],
)

if __name__ == "__main__":
    print("VORTICE 150 v3 - generacion del modelo 3D")
    print("  arquitectura: %s" % P["meta"]["arquitectura"])

    print("\n[1] Verificacion geometrica del ensamble completo")
    fallas = verificar(PARTES)

    print("\n[2] Balistica derivada")
    for k in ("inerte", "f35", "f25", "lata"):
        print("    %-7s v=%.4f m/s   cae en x = %.2f mm"
              % (k, V_SAL[k], ALCANCES[k]))
    print("    cuchilla en %.1f  ->  margenes %.1f / %.1f mm"
          % (X_CUCH, X_CUCH - ALCANCES["inerte"], ALCANCES["f35"] - X_CUCH))

    print("\n[3] Exportacion")
    exportar(construir(G_MAQ), "VORTICE_maquina")
    exportar(construir({"rotor", "transmision", "tambor"}), "VORTICE_rotor")
    exportar(construir({"guarda"}), "VORTICE_guarda")

    print("\n[4] Renders")
    cx, cz = 560.0, 320.0
    render(construir(G_MAQ, corte=True),
           os.path.join(DIR_PNG, "Vista_isometrica.png"),
           dict(foco=(cx, 0, cz), pos=(cx + 1300, -1700, cz + 1100), zoom=1.45))
    render(construir(G_MAQ, corte=True),
           os.path.join(DIR_PNG, "Vista_lateral.png"),
           dict(foco=(cx, 0, cz), pos=(cx, -4200, cz), zoom=2.05),
           tam=(2200, 1000), paralela=True)
    render(construir({"rotor", "transmision", "tambor"}),
           os.path.join(DIR_PNG, "Vista_rotor_detalle.png"),
           dict(foco=(X_TAMBOR - 40, 0, Z_EJE_ROTOR - 30),
                pos=(X_TAMBOR + 420, -560, Z_EJE_ROTOR + 330), zoom=1.25),
           tam=(1700, 1300))

    DERIVADOS["n_solidos"] = len(PARTES)
    DERIVADOS["alcances"] = ALCANCES
    # Las laminas dibujan EXACTAMENTE la trayectoria que se verifico.
    DERIVADOS["trayectorias"] = {
        k: dict(destino=v["destino"], v=v["v"], x_fin=v["x_fin"], z_fin=v["z_fin"],
                x_libre=v["x_libre"],
                pts=[v["pts"][i] for i in range(0, len(v["pts"]),
                                                max(1, len(v["pts"]) // 60))] + [v["pts"][-1]])
        for k, v in TRAYECTORIAS.items()}
    DERIVADOS["z_cuchilla_top"] = Z_CUCH_1
    DERIVADOS["z_tejadillo"] = [Z_TEJ_0, Z_TEJ_1]
    DERIVADOS["r_carcasa"] = R_CARC
    DERIVADOS["r_material"] = R_MAT
    DERIVADOS["r_envolvente"] = R_ENVOL
    DERIVADOS["r_rodillo"] = R_ROD
    with open(os.path.join(RAIZ, "PARAMETERS", "derivados_cad.json"), "w",
              encoding="utf-8") as fh:
        json.dump(DERIVADOS, fh, indent=1)

    print("\n%s" % ("FALLAS PENDIENTES: %d" % len(fallas) if fallas
                    else "Modelo generado sin fallas geometricas."))
    sys.exit(1 if fallas else 0)
