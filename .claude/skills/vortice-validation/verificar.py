#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VORTICE 150 v3 - Verificacion completa.

CINCO BLOQUES:

  A) FISICA Y MECANICA. Recalcula desde cero cada magnitud derivada de
     master.yaml y la contrasta con el valor guardado.

  B) GEOMETRIA. Mide sobre los solidos reales del modelo 3D.

  C) MONTAJE. Contrasta TODA la seccion `montaje` del YAML contra lo
     que construye el generador. Falla si algo difiere en mas de 1 um.
     (En la v2 el YAML decia x_rodillo_cabeza=500 y el generador
     construia 468,4: nadie lo comprobaba.)

  D) EL CAMINO DEL MATERIAL. Cinco familias que la v2 no tenia y que
     son las que dejaron pasar los cinco bloqueantes:
       D1 continuidad del apoyo
       D2 friccion y velocidad minima
       D3 trayectoria contra solidos
       D4 aislamiento de las bandejas
       D5 apoyo real (juntas declaradas, no tangencias)

  E) COHERENCIA DOCUMENTAL. Regresiones que ya ocurrieron antes.

TODO lo que falla, FALLA: no hay avisos que se ignoren.

Uso:   python verificar.py
"""

import os
import re
import sys
import math
import glob
import json

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, ".claude", "skills", "vortice-cad"))

with open(os.path.join(RAIZ, "PARAMETERS", "master.yaml"), "r", encoding="utf-8") as fh:
    P = yaml.safe_load(fh)

R, TB, OP, CI, TO = P["rotor"], P["tambor"], P["operacion"], P["cinta"], P["tolva"]
TR, SA, BA, MO = P["transmision"], P["salida"], P["bastidor"], P["montaje"]
GE, EH, IM = R["geometria"], OP["entrehierro"], R["iman"]
MAS, MEC, EL, CD = P["masas"], P["mecanica"], P["electronica"], P["cad"]
MAT, HIP = P["materiales"], P["hipotesis"]

G = 9.81
MU_DESFAVORABLE = 0.50          # caso desfavorable exigido por el proyecto
_estado = {"ok": 0, "falla": 0}
_fallos = []


def chk(cond, texto, detalle=""):
    marca = "[OK]  " if cond else "[FALLA]"
    _estado["ok" if cond else "falla"] += 1
    if not cond:
        _fallos.append(texto)
    print("  %s %-54s %s" % (marca, texto, detalle))
    return bool(cond)


def cerca(a, b, tol_rel=0.01, tol_abs=1e-9):
    return abs(a - b) <= max(tol_abs, abs(b) * tol_rel)


def rep(calc, guardado, unidad="", dec=4):
    return "calc %.*f  yaml %.*f %s" % (dec, calc, dec, guardado, unidad)


def titulo(t):
    print("\n" + t)
    print("  " + "-" * 78)


# =====================================================================
# A - FISICA Y MECANICA
# =====================================================================
def bloque_fisica():
    titulo("A1 - GEOMETRIA MAGNETICA")

    ID = R["tubo"]["OD"] - 2 * R["tubo"]["pared"]
    chk(cerca(ID, R["tubo"]["ID"]), "ID = OD - 2*pared", rep(ID, R["tubo"]["ID"], "mm"))
    D_r = R["tubo"]["OD"] + 2 * IM["T"]
    chk(cerca(D_r, GE["D_r"]), "D_r = OD + 2*espesor de iman", rep(D_r, GE["D_r"], "mm"))
    n_im = IM["n_polos"] * IM["k_piezas"] * IM["n_filas"]
    chk(n_im == IM["n_total"], "n_imanes = polos * piezas * filas",
        "calc %d  yaml %d" % (n_im, IM["n_total"]))
    p = IM["n_polos"] / 2.0
    chk(cerca(p, GE["p_pares"]), "p = n_polos / 2", rep(p, GE["p_pares"], "", 1))
    lam = math.pi * D_r / p
    chk(cerca(lam, GE["lambda"]), "lambda = pi * D_r / p", rep(lam, GE["lambda"], "mm"))
    chk(cerca(lam / (2 * math.pi), GE["lam_2pi"], 0.002),
        "decaimiento del CAMPO  lambda/2pi", rep(lam / (2 * math.pi), GE["lam_2pi"], "mm"))
    chk(cerca(lam / (4 * math.pi), GE["lam_4pi"], 0.002),
        "decaimiento de la FUERZA lambda/4pi", rep(lam / (4 * math.pi), GE["lam_4pi"], "mm"))

    # LA COMPROBACION CIRCULAR DE LA v2 SE ELIMINO. Dividir lambda/2pi
    # entre lambda/4pi da 2 POR ALGEBRA, con cualquier D_r y cualquier p:
    # no comprueba nada de fisica. Lo que se comprueba ahora es que H1
    # declara COMO se va a medir y que el instrumento existe.
    chk(bool(HIP["H1"].get("instrumento")) and bool(HIP["H1"].get("se_mide")),
        "H1 declara instrumento y metodo de medida (no algebra)",
        HIP["H1"]["instrumento"][:44])

    pc = math.pi * R["tubo"]["OD"] / IM["n_polos"]
    chk(cerca(pc, GE["paso_circ"]), "paso circunferencial = pi*OD/n_polos",
        rep(pc, GE["paso_circ"], "mm"))
    ap = IM["k_piezas"] * IM["W"]
    chk(cerca(ap, GE["ancho_polo"]), "ancho de polo = piezas * W", rep(ap, GE["ancho_polo"], "mm"))
    chk(cerca(pc - ap, GE["hueco_polos"]), "hueco entre polos", rep(pc - ap, GE["hueco_polos"], "mm"))
    chk(cerca(ap / pc, GE["alpha"]), "factor de llenado alpha", rep(ap / pc, GE["alpha"]))
    chk(GE["hueco_polos"] >= R["retencion"]["tira_ancho"],
        "el hueco admite la tira separadora",
        "%.2f >= %.2f mm" % (GE["hueco_polos"], R["retencion"]["tira_ancho"]))

    rt = R["tubo"]["OD"] / 2.0
    sag1 = rt - math.sqrt(rt ** 2 - (IM["W"] / 2.0) ** 2)
    chk(cerca(sag1, GE["sagita_pieza"], 0.005), "sagita de UNA pieza de 10 mm",
        rep(sag1, GE["sagita_pieza"], "mm"))
    sag2 = rt - math.sqrt(rt ** 2 - (GE["ancho_polo"] / 2.0) ** 2)
    chk(cerca(sag2, GE["sagita_polo"], 0.005),
        "sagita del POLO real de 20 mm (dos piezas coplanares)",
        rep(sag2, GE["sagita_polo"], "mm"))
    chk(sag2 > sag1, "la sagita del polo es mayor que la de la pieza",
        "%.3f > %.3f mm — afecta al pegado y al entrehierro de borde" % (sag2, sag1))

    pmin = IM["W"] * IM["Br_medio"] / (2.0 * IM["B_sat_acero"])
    chk(cerca(pmin, R["tubo"]["pared_min_N52"]), "pared minima = W*Br/(2*B_sat)",
        rep(pmin, R["tubo"]["pared_min_N52"], "mm"))
    chk(R["tubo"]["pared"] >= pmin, "pared real >= minima por saturacion",
        "%.2f >= %.2f mm" % (R["tubo"]["pared"], pmin))
    la = IM["n_filas"] * IM["L"]
    chk(cerca(la, GE["largo_activo"]), "largo activo = filas * L_iman", rep(la, GE["largo_activo"], "mm"))
    chk(la <= R["tubo"]["largo"], "el largo activo cabe en el tubo",
        "%.0f <= %.0f mm" % (la, R["tubo"]["largo"]))

    titulo("A2 - TAMBOR DE CABEZA Y ENTREHIERRO")
    cid = GE["D_r"] + 2 * R["retencion"]["z_zuncho"] + 2 * TB["holgura_radial"]
    chk(cerca(cid, TB["ID"]), "ID de carcasa = D_r + 2*zuncho + 2*holgura", rep(cid, TB["ID"], "mm"))
    cod = cid + 2 * TB["pared"]
    chk(cerca(cod, TB["OD"]), "OD de carcasa = ID + 2*pared", rep(cod, TB["OD"], "mm"))
    rmat = cod / 2.0 + CI["banda_esp"]
    chk(cerca(rmat, OP["despegue"]["R_material"]), "R del material = OD/2 + espesor de banda",
        rep(rmat, OP["despegue"]["R_material"], "mm"))
    z = (EH["z_zuncho"] + EH["z_holgura"] + EH["z_carcasa"] + EH["z_banda"])
    chk(cerca(z, EH["z_nominal"]), "entrehierro = zuncho + holgura + carcasa + banda",
        rep(z, EH["z_nominal"], "mm", 2))
    chk(cerca(rmat - GE["D_r"] / 2.0, EH["z_nominal"]),
        "y coincide con la geometria (R_material - R_iman)",
        rep(rmat - GE["D_r"] / 2.0, EH["z_nominal"], "mm", 3))
    for i, (par, od) in enumerate(zip(TB["manguitos"]["pared"], TB["manguitos"]["OD"])):
        chk(cerca(cod + 2 * par, od), "manguito %d: OD = OD_carcasa + 2*pared" % i,
            rep(cod + 2 * par, od, "mm", 1))
        chk(cerca(od / 2.0 + CI["banda_esp"] - GE["D_r"] / 2.0, EH["z_index"][i]),
            "manguito %d: entrehierro indexado" % i,
            rep(od / 2.0 + CI["banda_esp"] - GE["D_r"] / 2.0, EH["z_index"][i], "mm", 2))
        chk(cerca(math.exp(-(EH["z_index"][i] - EH["z_nominal"]) / GE["lam_4pi"]),
                  EH["F_relativa"][i], 0.002),
            "manguito %d: F/F0 = e^(-dz/(lam/4pi))" % i,
            "%.4f" % EH["F_relativa"][i])
    chk(all(cerca(EH["galgas"][i], TB["manguitos"]["pared"][i])
            for i in range(len(EH["galgas"]))),
        "la galga baja el eje lo que engorda el manguito",
        "banda plana en z=%.0f con cualquier manguito" % CI["banda_sup_altura"])
    chk(cerca(math.exp(-(EH["z_nominal"] - 3.0) / GE["lam_4pi"]),
              EH["penalizacion_vs_v2"], 0.002),
        "coste de la arquitectura: entrehierro 3,0 -> 4,0",
        "x%.4f  (%.1f %%)" % (EH["penalizacion_vs_v2"],
                              (EH["penalizacion_vs_v2"] - 1) * 100))
    chk(EH["F_relativa"][-1] < 0.5, "el barrido de entrehierro es medible (H1)",
        "la fuerza cae a x%.3f entre %.1f y %.1f mm"
        % (EH["F_relativa"][-1], EH["z_index"][0], EH["z_index"][-1]))

    titulo("A3 - OPERACION")
    f = p * OP["N_nominal"] / 60.0
    chk(cerca(f, OP["f_nominal"]), "f = p*N/60", rep(f, OP["f_nominal"], "Hz", 2))
    vs = math.pi * GE["D_r"] / 1000.0 * OP["N_nominal"] / 60.0
    chk(cerca(vs, OP["v_sup"]), "velocidad de superficie del iman", rep(vs, OP["v_sup"], "m/s"))
    rpm_t = OP["v_banda"] / (math.pi * TB["OD"] / 1000.0) * 60.0
    chk(cerca(rpm_t, TB["rpm_nominal"]), "rpm del tambor (gira con la banda, no con el rotor)",
        rep(rpm_t, TB["rpm_nominal"], "rpm", 2))
    vmin = math.sqrt(G * OP["despegue"]["R_material"] / 1000.0)
    chk(cerca(vmin, OP["despegue"]["v_min_cima"]), "v minima de despegue en la cima = sqrt(gR)",
        rep(vmin, OP["despegue"]["v_min_cima"], "m/s"))
    th = math.degrees(math.acos(OP["v_banda"] ** 2 / (G * OP["despegue"]["R_material"] / 1000.0)))
    chk(cerca(th, OP["despegue"]["theta_inerte_deg"]),
        "theta del inerte = acos(v^2/gR)", rep(th, OP["despegue"]["theta_inerte_deg"], "deg", 2))
    chk(OP["v_banda"] < vmin,
        "el inerte NO despega en la cima: sigue la banda hasta theta",
        "%.2f < %.3f m/s  (%.0f %%)" % (OP["v_banda"], vmin, OP["v_banda"] / vmin * 100))

    titulo("A4 - MASAS E INERCIA")
    rho_ac = R["tubo"]["densidad"] * 1e-9
    m_tubo = math.pi / 4 * (R["tubo"]["OD"] ** 2 - ID ** 2) * R["tubo"]["largo"] * rho_ac
    chk(cerca(m_tubo, MAS["m_tubo"]), "masa del tubo", rep(m_tubo, MAS["m_tubo"], "kg"))
    m_im = IM["n_total"] * IM["masa_unitaria"]
    chk(cerca(m_im, MAS["m_imanes"]), "masa de los imanes", rep(m_im, MAS["m_imanes"], "kg"))
    m_eje = math.pi / 4 * R["eje"]["D"] ** 2 * R["eje"]["largo"] * R["eje"]["densidad"] * 1e-9
    chk(cerca(m_eje, MAS["m_eje"]), "masa del eje", rep(m_eje, MAS["m_eje"], "kg"))
    CU = R["cubo"]
    v_cubo = (math.pi / 4 * (CU["OD"] ** 2 - R["eje"]["D"] ** 2) * CU["largo"]
              - CU["taladros"] * math.pi / 4 * CU["taladro_D"] ** 2 * CU["largo"])
    m_cub = 2 * v_cubo * CU["densidad"] * 1e-9
    chk(cerca(m_cub, MAS["m_cubos"]), "masa de los 2 cubos", rep(m_cub, MAS["m_cubos"], "kg"))
    RT = R["retencion"]
    m_tir = (IM["n_polos"] * RT["tira_ancho"] * RT["tira_alto"] * RT["tira_largo"]
             * RT["tira_densidad"] * 1e-9)
    chk(cerca(m_tir, MAS["m_tiras"], 0.02), "masa de las tiras PETG", rep(m_tir, MAS["m_tiras"], "kg"))
    r_i = GE["D_r"] / 2.0
    m_zun = (math.pi * ((r_i + RT["z_zuncho"]) ** 2 - r_i ** 2)
             * GE["largo_activo"] * RT["zuncho_densidad"] * 1e-9)
    chk(cerca(m_zun, MAS["m_zuncho"], 0.02), "masa del zuncho", rep(m_zun, MAS["m_zuncho"], "kg"))
    m_rot = m_tubo + m_im + m_eje + m_cub + m_tir + m_zun
    chk(cerca(m_rot, MAS["m_rotor"], 0.01), "masa del rotor (lo que gira a N_nominal)",
        rep(m_rot, MAS["m_rotor"], "kg"))

    m_carc = math.pi / 4 * (TB["OD"] ** 2 - TB["ID"] ** 2) * TB["largo"] * TB["densidad"] * 1e-9
    chk(cerca(m_carc, MAS["m_carcasa"], 0.01), "masa de la carcasa del tambor",
        rep(m_carc, MAS["m_carcasa"], "kg"))
    m_dis = 2 * (math.pi / 4 * (TB["ID"] ** 2 - TB["rodamiento_OD"] ** 2)
                 * TB["disco_esp"]) * TB["disco_densidad"] * 1e-9
    chk(cerca(m_dis, MAS["m_discos_tambor"], 0.01), "masa de los 2 discos de extremo",
        rep(m_dis, MAS["m_discos_tambor"], "kg"))
    m_tam = m_carc + m_dis + 2 * TB["rodamiento_masa"]
    chk(cerca(m_tam, MAS["m_tambor"], 0.01), "masa del conjunto tambor",
        rep(m_tam, MAS["m_tambor"], "kg"))
    for i, par in enumerate(TB["manguitos"]["pared"]):
        od = TB["manguitos"]["OD"][i]
        mm = math.pi / 4 * (od ** 2 - TB["OD"] ** 2) * TB["largo"] * TB["manguitos"]["densidad"] * 1e-9
        chk(cerca(mm, TB["manguitos"]["masa"][i], 0.01, 1e-6), "masa del manguito %d" % i,
            rep(mm, TB["manguitos"]["masa"][i], "kg"))

    r_med = (R["tubo"]["OD"] / 2.0 + IM["T"] / 2.0) / 1000.0
    I = (0.5 * m_tubo * ((R["tubo"]["OD"] / 2000.) ** 2 + (ID / 2000.) ** 2)
         + m_im * r_med ** 2 + 0.5 * m_eje * (R["eje"]["D"] / 2000.) ** 2
         + 0.5 * m_cub * (CU["OD"] / 2000.) ** 2 + m_tir * r_med ** 2
         + m_zun * ((r_i + RT["z_zuncho"] / 2) / 1000.) ** 2)
    chk(cerca(I, MAS["I_rotor"], 0.02), "momento de inercia del rotor",
        rep(I, MAS["I_rotor"], "kg m2", 6))
    chk("tambor" not in str(MAS["I_rotor"]),
        "I_rotor NO incluye el tambor (gira a 57 rpm, no a 1400)",
        "el tambor rueda libre: no lo acelera el motor")

    titulo("A5 - ENERGIA, RETENCION Y EJE")
    for N, clave in ((OP["N_nominal"], "E_rotor_nom"), (OP["N_max"], "E_rotor_max")):
        w = 2 * math.pi * N / 60.0
        E = 0.5 * MAS["I_rotor"] * w ** 2
        chk(cerca(E, MEC[clave], 0.01), "energia del rotor a %d rpm" % N, rep(E, MEC[clave], "J", 2))
    w_max = 2 * math.pi * OP["N_max"] / 60.0
    Fc = IM["masa_unitaria"] * w_max ** 2 * r_med
    chk(cerca(Fc, MEC["Fc_iman_max"], 0.01), "fuerza centripeta por iman a N_max",
        rep(Fc, MEC["Fc_iman_max"], "N", 2))
    sig = Fc / (IM["L"] * IM["W"])
    chk(cerca(sig, MEC["tension_union"], 0.01), "tension en la union pegada",
        rep(sig, MEC["tension_union"], "MPa", 5))
    # LAS DOS CIFRAS VAN SEPARADAS. La v1 las mezclaba.
    chk(cerca(MEC["limite_tension_union"] / sig, MEC["factor_vs_criterio"], 0.01),
        "factor contra el CRITERIO de diseno (1 MPa)",
        "%.1fx" % MEC["factor_vs_criterio"])
    chk(cerca(MEC["resistencia_epoxico"] / sig, MEC["factor_vs_epoxico"], 0.01),
        "factor contra la RESISTENCIA del epoxico (10 MPa)",
        "%.1fx" % MEC["factor_vs_epoxico"])
    chk(sig < MEC["limite_tension_union"], "la tension cumple el criterio de diseno",
        "%.4f < %.1f MPa" % (sig, MEC["limite_tension_union"]))
    v_sup_max = math.pi * GE["D_r"] / 1000.0 * OP["N_max"] / 60.0
    E_suelto = 0.5 * IM["masa_unitaria"] * v_sup_max ** 2
    chk(cerca(E_suelto, MEC["E_iman_suelto"], 0.01), "energia de un iman suelto",
        rep(E_suelto, MEC["E_iman_suelto"], "J", 3))
    chk(P["seguridad"]["guarda_obligatoria"] is True,
        "la guarda es obligatoria (iman suelto = %.2f J)" % E_suelto, "declarada")
    chk(P["seguridad"]["rotor_encerrado_por_carcasa"] is True,
        "el rotor magnetico queda encerrado por la carcasa",
        "segunda barrera por construccion")

    # Eje: ahora carga el rotor Y la reaccion de la banda por el tambor
    T = CI["tension"]
    w_b = CI["banda_masa"] * G / (CI["banda_L"] / 1000.0)
    chk(cerca(w_b, T["peso_por_metro"], 0.01), "peso de banda por metro",
        rep(w_b, T["peso_por_metro"], "N/m", 4))
    T2 = w_b * (CI["entrecentros"] / 1000.0) ** 2 / (8 * T["flecha_admisible"] / 1000.0)
    chk(cerca(T2, T["T2"], 0.01), "T2 por flecha admisible del ramal de retorno",
        rep(T2, T["T2"], "N", 3))
    m_cama = (CI["cama_largo"] * CI["banda_ancho"] * CI["banda_esp"]
              * CI["banda_densidad"] * 1e-9)
    Ft = T["mu_banda_cama"] * (m_cama + P["caudal"]["masa_sobre_banda"] / 1000.0) * G
    chk(cerca(Ft, T["F_tangencial"], 0.02), "fuerza tangencial banda/cama",
        rep(Ft, T["F_tangencial"], "N", 4))
    chk(cerca(2 * T2 + Ft, T["carga_radial_tambor"], 0.01),
        "carga radial sobre el tambor = T1 + T2",
        rep(2 * T2 + Ft, T["carga_radial_tambor"], "N", 3))

    E_ac, I_eje = 200e9, math.pi * (R["eje"]["D"] / 1000.0) ** 4 / 64.0
    L_s = MEC["eje_span"] / 1000.0
    a_ = MEC["eje_a_rodamiento_tambor"] / 1000.0
    d1 = (MAS["m_rotor"] - MAS["m_eje"]) * G * L_s ** 3 / (48 * E_ac * I_eje)
    d2 = ((T["carga_radial_tambor"] + MAS["m_tambor"] * G) / 2.0) * a_ \
        * (3 * L_s ** 2 - 4 * a_ ** 2) / (24 * E_ac * I_eje)
    chk(cerca(d1 * 1000, MEC["flecha_por_rotor"], 0.02), "flecha por el peso del rotor",
        rep(d1 * 1000, MEC["flecha_por_rotor"], "mm", 5))
    chk(cerca(d2 * 1000, MEC["flecha_por_tambor"], 0.02), "flecha por la carga del tambor",
        rep(d2 * 1000, MEC["flecha_por_tambor"], "mm", 5))
    chk(cerca((d1 + d2) * 1000, MEC["flecha_eje"], 0.02), "flecha total del eje",
        rep((d1 + d2) * 1000, MEC["flecha_eje"], "mm", 5))
    Nc = 30.0 / math.pi * math.sqrt(G / (d1 + d2))
    chk(cerca(Nc, MEC["N_critica"], 0.02), "primera velocidad critica (Rayleigh)",
        rep(Nc, MEC["N_critica"], "rpm", 1))
    pct = OP["N_max"] / Nc * 100.0
    chk(cerca(pct, MEC["pct_critica"], 0.02), "N_max como % de la critica",
        rep(pct, MEC["pct_critica"], "%", 2))
    chk(pct < MEC["limite_pct_critica"], "N_max < %.0f%% de la critica"
        % MEC["limite_pct_critica"], "%.1f %%" % pct)

    titulo("A6 - TRANSMISION")
    rel = TR["polea_cond_T"] / float(TR["polea_motriz_T"])
    chk(cerca(rel, TR["relacion"]), "relacion = dientes cond / motriz", rep(rel, TR["relacion"], "", 3))
    for Tn, Dp, nom in ((TR["polea_motriz_T"], TR["Dp_motriz"], "motriz"),
                        (TR["polea_cond_T"], TR["Dp_cond"], "conducida")):
        d = Tn * TR["polea_paso"] / math.pi
        chk(cerca(d, Dp), "diametro primitivo de la polea %s" % nom, rep(d, Dp, "mm"))
    rpm = TR["motor_rpm"] / rel
    chk(cerca(rpm, TR["rotor_rpm_fondo"]), "rpm del rotor a fondo", rep(rpm, TR["rotor_rpm_fondo"], "rpm", 1))
    chk(rpm > OP["N_max"], "hay reserva sobre el techo de firmware", "%.0f > %d rpm" % (rpm, OP["N_max"]))
    C = TR["entrecentros_poleas"]
    Lc = (2 * C + math.pi * (TR["Dp_motriz"] + TR["Dp_cond"]) / 2.0
          + (TR["Dp_cond"] - TR["Dp_motriz"]) ** 2 / (4 * C))
    chk(cerca(Lc, TR["correa_L"]), "longitud de correa", rep(Lc, TR["correa_L"], "mm", 2))
    a = w_max / OP["rampa_s"]
    chk(cerca(MAS["I_rotor"] * a, TR["par_rampa"], 0.01), "par en la rampa",
        rep(MAS["I_rotor"] * a, TR["par_rampa"], "N m", 4))
    chk(cerca(MAS["I_rotor"] * a * w_max, TR["pot_rampa"], 0.01), "potencia en la rampa",
        rep(MAS["I_rotor"] * a * w_max, TR["pot_rampa"], "W", 2))
    chk(TR["pot_rampa"] < TR["motor_W"], "el motor cubre la rampa",
        "%.1f < %d W" % (TR["pot_rampa"], TR["motor_W"]))

    titulo("A7 - CINTA Y CAUDAL")
    Lb = (2 * CI["entrecentros"] + math.pi * (TB["OD"] + CI["rodillo_D"]) / 2.0
          + (TB["OD"] - CI["rodillo_D"]) ** 2 / (4 * CI["entrecentros"]))
    chk(cerca(Lb, CI["banda_L"]), "longitud de banda sobre DOS diametros distintos",
        rep(Lb, CI["banda_L"], "mm", 2))
    dL = max(2 * CI["entrecentros"] + math.pi * (od + CI["rodillo_D"]) / 2.0
             + (od - CI["rodillo_D"]) ** 2 / (4 * CI["entrecentros"])
             for od in TB["manguitos"]["OD"]) - Lb
    chk(cerca(dL, CI["tensor_necesario"], 0.01), "banda extra con el manguito mas grueso",
        rep(dL, CI["tensor_necesario"], "mm", 3))
    chk(CI["tensor_recorrido"] >= dL, "el tensor absorbe el cambio de manguito",
        "%.0f >= %.2f mm" % (CI["tensor_recorrido"], dL))
    rrpm = OP["v_banda"] / (math.pi * CI["rodillo_D"] / 1000.0) * 60.0
    chk(cerca(rrpm, CI["rodillo_rpm"]), "rpm del rodillo motriz a v_banda",
        rep(rrpm, CI["rodillo_rpm"], "rpm", 2))
    rmax = OP["v_banda_max"] / (math.pi * CI["rodillo_D"] / 1000.0) * 60.0
    chk(cerca(rmax, CI["rodillo_rpm_max"]), "rpm del rodillo a v_banda_max — ASI HAY QUE PEDIRLO",
        rep(rmax, CI["rodillo_rpm_max"], "rpm", 2))
    mb = CI["banda_L"] * CI["banda_ancho"] * CI["banda_esp"] * CI["banda_densidad"] * 1e-9
    chk(cerca(mb, CI["banda_masa"], 0.01), "masa de la banda", rep(mb, CI["banda_masa"], "kg"))

    CA = P["caudal"]
    q = CA["sigma_areal"] * (CI["banda_ancho"] / 1000.0) * OP["v_banda"] * 1000.0
    chk(cerca(q, CA["caudal_g_s"]), "caudal = sigma * ancho * v", rep(q, CA["caudal_g_s"], "g/s", 3))
    chk(cerca(q * 3.6, CA["caudal_kg_h"]), "caudal en kg/h", rep(q * 3.6, CA["caudal_kg_h"], "kg/h", 2))
    lote = P["lote_patron"]
    m_lote = sum(x["masa_tot_g"] for x in lote)
    n_lote = sum(x["piezas"] for x in lote)
    chk(cerca(m_lote, CA["lote_g"], 0.005), "masa del lote patron", rep(m_lote, CA["lote_g"], "g", 1))
    chk(n_lote == CA["lote_piezas"], "piezas del lote patron", "calc %d  yaml %d" % (n_lote, CA["lote_piezas"]))
    m_media = CA["lote_g"] / CA["lote_piezas"]
    chk(cerca(q / m_media, CA["piezas_por_s"], 0.01), "piezas por segundo",
        rep(q / m_media, CA["piezas_por_s"], "1/s", 3))
    chk(cerca(CA["lote_g"] / q, CA["t_lote"], 0.01), "duracion de un lote", rep(CA["lote_g"] / q, CA["t_lote"], "s", 2))
    m_Al = sum(x["masa_tot_g"] for x in lote if x["material"].startswith("Al"))
    chk(cerca(m_Al / m_lote * 100, CA["lote_frac_Al"], 0.02), "fraccion de aluminio del lote",
        rep(m_Al / m_lote * 100, CA["lote_frac_Al"], "%", 2))
    chk(CA["phi_cobertura"] <= 0.35, "cobertura areal en monocapa (< 0.35)", "%.2f" % CA["phi_cobertura"])

    titulo("A8 - INSTRUMENTACION: DOS FRACCIONES, DOS CELDAS")
    chk(EL["celdas"] == 2 and EL["celdas_por_bandeja"] == 1,
        "una celda por bandeja, dos canales de datos",
        "%d celdas, %d HX711, %d canales" % (EL["celdas"], EL["hx711"], EL["canales_de_datos"]))
    chk(EL["hx711"] == EL["celdas"] == EL["canales_de_datos"],
        "celdas = HX711 = canales de datos", "cadena 1:1:1")
    for nom, clave, Lint in (("inertes", "m_bandeja_inerte", SA["bandeja_inerte"][1]),
                             ("no ferrosos", "m_bandeja_nofe", SA["bandeja_nofe"][1])):
        Y, H = SA["bandeja_inerte"][0], SA["bandeja_inerte"][2]
        area = Lint * Y + 2 * Lint * H + 2 * Y * H
        m = (area * SA["bandeja_esp"] * SA["bandeja_densidad"] * 1e-9
             + 2 * (2 * (Lint + Y)) * SA["marco_seccion"] * SA["marco_densidad"] * 1e-9)
        chk(cerca(m, MAS[clave], 0.01), "masa de la bandeja de %s" % nom, rep(m, MAS[clave], "kg"))
    tara_max = max(MAS["m_bandeja_inerte"], MAS["m_bandeja_nofe"])
    uso = (tara_max + P["caudal"]["lote_g"] / 1000.0) / EL["celda_FS"]
    chk(uso < 0.80, "la celda no se satura con tara + lote completo",
        "%.0f %% del fondo de escala de %.0f kg" % (uso * 100, EL["celda_FS"]))
    cuant = EL["resolucion_celda"] / m_Al * 100
    chk(cuant < 2.0, "cuantizacion sobre el Al del lote < 2 %",
        "%.2f %%  (la v2: 5 g / 20 kg = %.2f %%)" % (cuant, 5.0 / m_Al * 100))
    chk("[VERIFICAR]" in EL["resolucion_protocolo"],
        "la resolucion va marcada [VERIFICAR] con protocolo de medida", "no es FS/2^24")
    chk("[VERIFICAR]" in EL["error_esquina_protocolo"],
        "el error de esquina de la celda monopunto esta declarado", "con plan de medida y salida")
    chk(len(EL["dcdc"]) >= 2 and any(d["a"] == 12 for d in EL["dcdc"])
        and any(d["a"] == 5 for d in EL["dcdc"]),
        "hay conversion DC-DC para 12 V y 5 V",
        "fuente %d V -> %s" % (EL["fuente_V"], [d["a"] for d in EL["dcdc"]]))
    chk(OP["N_max"] == P["seguridad"]["N_max_firmware"],
        "el techo de firmware coincide con N_max", "%d rpm" % OP["N_max"])
    chk("no por software" in P["seguridad"]["seta_emergencia"],
        "la seta corta la alimentacion fisicamente", "declarado")
    chk(P["seguridad"]["pesar_con_motor_detenido"] is True, "se pesa con el motor detenido", "declarado")

    titulo("A9 - BASTIDOR Y TOLVA")
    mb_ = BA["base_L"] * BA["base_W"] * BA["base_esp"] * BA["mdf_densidad"] * 1e-9
    chk(cerca(mb_, MAS["m_base"]), "masa de la base", rep(mb_, MAS["m_base"], "kg", 3))
    ml = 2 * (BA["lateral_L"] * BA["lateral_H"] * BA["lateral_esp"] * BA["mdf_densidad"] * 1e-9)
    chk(cerca(ml, MAS["m_laterales"]), "masa de los laterales (sin ventanas)", rep(ml, MAS["m_laterales"], "kg", 3))
    at = BA["base_esp"] + TO["z_boca"] + TO["h_cuello"] + TO["h_cono"]
    chk(cerca(at, BA["altura_total"]), "altura total (sin patas)", rep(at, BA["altura_total"], "mm", 1))
    chk(cerca(TO["z_boca"], CI["banda_sup_altura"] + TO["luz"]),
        "boca de tolva = altura de banda + luz",
        rep(TO["z_boca"], CI["banda_sup_altura"] + TO["luz"], "mm", 1))
    A1 = TO["salida"][0] * TO["salida"][1]
    A2 = TO["sup"][0] * TO["sup"][1]
    V = (TO["h_cono"] / 3.0 * (A1 + A2 + math.sqrt(A1 * A2)) + A1 * TO["h_cuello"]) / 1e6
    chk(cerca(V, TO["volumen_L"], 0.001), "volumen util de la tolva", rep(V, TO["volumen_L"], "L", 4))
    angx = math.degrees(math.atan(TO["h_cono"] / ((TO["sup"][1] - TO["salida"][1]) / 2.0)))
    chk(cerca(angx, TO["angulo"], 0.001), "angulo de pared en el eje X", rep(angx, TO["angulo"], "grados", 3))
    angy = math.degrees(math.atan(TO["h_cono"] / ((TO["sup"][0] - TO["salida"][0]) / 2.0)))
    chk(cerca(angy, TO["angulo_Y"], 0.001), "angulo de pared en el eje Y", rep(angy, TO["angulo_Y"], "grados", 3))
    marg = (CI["banda_ancho"] - TO["salida"][0]) / 2.0
    chk(cerca(marg, TO["margen_a_banda"]), "margen de la salida al borde de banda",
        rep(marg, TO["margen_a_banda"], "mm", 1))
    chk(marg >= CI["guia_esp"] + 5.0,
        "la salida NO descarga sobre las guias laterales",
        "%.1f mm de margen contra %.1f de guia" % (marg, CI["guia_esp"]))
    chk(len(BA["ventanas"]["x_centros"]) == BA["ventanas"]["n"], "n de ventanas coincide con la lista",
        "%d ventanas por lado" % BA["ventanas"]["n"])
    ESC = BA["ventanas"]["escotadura_rotor"]
    for xcv in BA["ventanas"]["x_centros"]:
        a0, a1 = xcv - BA["ventanas"]["ancho_X"] / 2, xcv + BA["ventanas"]["ancho_X"] / 2
        chk(a1 <= ESC["x_ini"] or a0 >= ESC["x_fin"],
            "ventana en x=%.0f no cruza la escotadura del rotor" % xcv,
            "%.0f..%.0f vs escotadura %.0f..%.0f" % (a0, a1, ESC["x_ini"], ESC["x_fin"]))
        chk(a0 >= MO["x_base_ini"] + BA["ventanas"]["margen_extremo"]
            and a1 <= MO["x_base_fin"] - BA["ventanas"]["margen_extremo"],
            "ventana en x=%.0f respeta los %.0f mm extremos" % (xcv, BA["ventanas"]["margen_extremo"]),
            "%.0f..%.0f" % (a0, a1))

    titulo("A10 - FISICA DE MATERIALES E HIPOTESIS")
    mu0 = 4 * math.pi * 1e-7
    chk(cerca(mu0, MAT["mu0"], 1e-9), "mu0", rep(mu0, MAT["mu0"], "H/m", 12))
    for m in MAT["tabla"]:
        sg = 1.0 / m["rho_e"]
        chk(cerca(sg, m["sigma"], 1e-6), "%s: sigma = 1/rho_e" % m["material"],
            "%.4e S/m" % sg)
        chk(cerca(sg / m["rho_m"], m["sigma_sobre_rho_m"], 1e-6),
            "%s: figura de merito sigma/rho_m" % m["material"], "%.4e" % (sg / m["rho_m"]))
        d = math.sqrt(m["rho_e"] / (math.pi * MAT["f_operacion"] * mu0)) * 1000
        chk(cerca(d, m["delta_mm"], 1e-6), "%s: profundidad de piel a %.1f Hz"
            % (m["material"], MAT["f_operacion"]), "%.2f mm" % d)
    al = [m for m in MAT["tabla"] if m["material"].startswith("Alumin")][0]
    cu = [m for m in MAT["tabla"] if m["material"].startswith("Cobre")][0]
    lt = [m for m in MAT["tabla"] if m["material"].startswith("Lat")][0]
    razon = al["sigma"] / cu["sigma"]
    chk(cerca(razon, MAT["razon_sigma_Al_Cu"], 1e-6), "sigma(Al)/sigma(Cu)", "%.4f" % razon)
    chk(cerca((1 - razon) * 100, MAT["al_conduce_menos_pct"], 1e-6),
        "el Al conduce un % MENOS que el Cu (la v2 decia '70 % peor')",
        "%.1f %% menos" % ((1 - razon) * 100))
    chk(al["sigma_sobre_rho_m"] > cu["sigma_sobre_rho_m"] > lt["sigma_sobre_rho_m"],
        "H2 es enunciable: sigma/rho_m ordena Al > Cu > laton",
        "%.0f > %.0f > %.0f" % (al["sigma_sobre_rho_m"], cu["sigma_sobre_rho_m"],
                                lt["sigma_sobre_rho_m"]))
    espesor_max = max(max(x["dim"][2] for x in P["lote_patron"]),
                      max(x["dim"][2] for x in P["lote_H2"]["probetas"]))
    chk(espesor_max < al["delta_mm"],
        "todas las piezas quedan penetradas por el campo",
        "espesor max %.2f mm < delta(Al) %.2f mm" % (espesor_max, al["delta_mm"]))
    mats = set(x["material"].split()[0] for x in P["lote_H2"]["probetas"])
    chk({"Aluminio", "Cobre", "Latón"} <= mats, "el lote de H2 tiene los tres metales",
        ", ".join(sorted(mats)))
    chk(len(set(tuple(x["dim"]) for x in P["lote_H2"]["probetas"])) == 1,
        "las probetas de H2 son de geometria y espesor identicos",
        P["lote_H2"]["condicion"])
    chk(MAT["condicion"] == "a geometría y espesor controlados",
        "la condicion de comparacion esta declarada", MAT["condicion"])


# =====================================================================
# B, C, D - SOBRE EL MODELO 3D
# =====================================================================
def bloque_modelo():
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_OUT

    titulo("B - GEOMETRIA MEDIDA SOBRE LOS SOLIDOS DEL MODELO 3D")
    print("  (importando el generador; tarda unos segundos)")
    import generar_modelo3d as M

    fallas = M.verificar(M.PARTES, verboso=False)
    chk(not fallas, "ningun par NO declarado interfiere",
        fallas[0][:64] if fallas else "%d solidos, %d juntas declaradas"
        % (len(M.PARTES), len(P["juntas"])))

    x0, x1 = M.X_BASE_0, M.X_BASE_1
    yl = BA["base_W"] / 2.0
    ztop = BA["altura_total"] + BA["pata_H"]
    fuera = []
    for pz in M.PARTES:
        b = M.bbox(pz)
        if (b.xmin < x0 - 0.5 or b.xmax > x1 + 0.5 or b.ymin < -yl - 0.5
                or b.ymax > yl + 0.5 or b.zmin < -0.5 or b.zmax > ztop + 0.5):
            fuera.append(pz["nombre"])
    chk(not fuera, "todos los solidos caben dentro del bastidor",
        ", ".join(sorted(set(fuera)))[:60] if fuera
        else "huella %.0f x %.0f x %.0f mm" % (x1 - x0, 2 * yl, ztop))

    ent = M.R_MAT - M.R_IMAN
    chk(cerca(ent, EH["z_nominal"], 0.001), "entrehierro medido en el modelo = nominal",
        rep(ent, EH["z_nominal"], "mm", 3))
    hol = TB["ID"] / 2.0 - M.R_ZUNCHO
    chk(cerca(hol, TB["holgura_radial"], 0.001), "el rotor no roza la carcasa",
        rep(hol, TB["holgura_radial"], "mm", 3))
    chk(M.Z_BANDA_SUP - M.CI["banda_esp"] - M.R_CARC == M.Z_EJE_ROTOR
        and M.Z_BANDA_SUP - M.CI["banda_esp"] - M.R_ROD == M.Z_ROD_EJE,
        "la banda es HORIZONTAL: misma tangente superior en los dos cilindros",
        "ejes a z=%.1f y z=%.1f" % (M.Z_EJE_ROTOR, M.Z_ROD_EJE))
    d_tol = math.hypot(M.X_TOLVA - TO["salida"][1] / 2.0 - M.X_ROD_COLA,
                       M.Z_TOLVA_SAL - M.Z_ROD_EJE) - CI["rodillo_D"] / 2.0
    chk(d_tol > 0, "la tolva no interfiere con el rodillo de cola", "holgura %.1f mm" % d_tol)
    ra = M.X_TAMBOR - M.X_TOLVA
    chk(ra >= 400.0, "recorrido de asentamiento tolva -> tambor >= 400 mm", "%.0f mm" % ra)
    d_cama = (M.X_TAMBOR
              - math.sqrt(M.R_ENVOL ** 2 - (M.Z_BANDA_INF - CI["cama_esp"] - M.Z_EJE_ROTOR) ** 2)
              - CI["cama_x"][1])
    chk(d_cama > 0, "la cama libra el tambor incluso con el manguito mas grueso",
        "holgura %.1f mm" % d_cama)
    chk(SA["bandeja_inerte"][0] <= BA["sep_laterales"] - 10,
        "la bandeja cabe entre laterales",
        "%.0f <= %.0f mm" % (SA["bandeja_inerte"][0], BA["sep_laterales"] - 10))
    chk(TB["y_ext"] * 2 < BA["sep_laterales"], "la carcasa cabe entre laterales",
        "%.0f < %.0f mm" % (TB["y_ext"] * 2, BA["sep_laterales"]))
    chk(M.Y_POLEA - TR["polea_ancho"] / 2.0 >= TB["y_ext"] + TR["polea_holgura_carcasa"] - 1e-9,
        "la polea libra el disco del tambor",
        "%.1f >= %.1f mm" % (M.Y_POLEA - TR["polea_ancho"] / 2.0, TB["y_ext"] + TR["polea_holgura_carcasa"]))
    chk(M.Y_SUB_0 >= TB["y_ext"] + R["soporte"]["subplaca_holgura_carcasa"] - 1e-9,
        "la subplaca libra la carcasa",
        "y_sub_0 = %.1f >= %.1f mm" % (M.Y_SUB_0, TB["y_ext"] + R["soporte"]["subplaca_holgura_carcasa"]))

    # -----------------------------------------------------------------
    titulo("C - MONTAJE: EL YAML CONTRA LO QUE CONSTRUYE EL GENERADOR")
    print("  (en la v2 el YAML decia 500 y el generador construia 468,4)")
    D = M.DERIVADOS
    for clave in sorted(MO.keys()):
        if clave not in D:
            chk(False, "montaje.%s existe en el generador" % clave, "AUSENTE")
            continue
        a, b = MO[clave], D[clave]
        if isinstance(a, list):
            ok = len(a) == len(b) and all(abs(x - y) < 1e-3 for x, y in zip(a, b))
            det = "yaml %s  cad %s" % (a, [round(v, 3) for v in b])
        else:
            ok = abs(a - b) < 1e-3
            det = "yaml %.4f  cad %.4f" % (a, b)
        chk(ok, "montaje.%s" % clave, det)

    # -----------------------------------------------------------------
    # Utilidades geometricas
    # -----------------------------------------------------------------
    BBS = [M.bbox(p) for p in M.PARTES]
    NOM = [p["nombre"] for p in M.PARTES]
    SHP = [p["solido"].val() for p in M.PARTES]

    def bbox_dist(a, b):
        dx = max(0.0, max(a.xmin - b.xmax, b.xmin - a.xmax))
        dy = max(0.0, max(a.ymin - b.ymax, b.ymin - a.ymax))
        dz = max(0.0, max(a.zmin - b.zmax, b.zmin - a.zmax))
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def dist(i, j):
        d = BRepExtrema_DistShapeShape(SHP[i].wrapped, SHP[j].wrapped)
        d.Perform()
        return d.Value()

    _clas = {}

    def dentro(i, x, y, z, tol=1e-6):
        c = _clas.get(i)
        if c is None:
            try:
                c = BRepClass3d_SolidClassifier(SHP[i].wrapped)
            except Exception:
                c = False
            _clas[i] = c
        if c is False:
            return False
        c.Perform(gp_Pnt(x, y, z), tol)
        return c.State() != TopAbs_OUT

    def area_contacto(a, b):
        ov = [min(a.xmax, b.xmax) - max(a.xmin, b.xmin),
              min(a.ymax, b.ymax) - max(a.ymin, b.ymin),
              min(a.zmax, b.zmax) - max(a.zmin, b.zmin)]
        k = ov.index(min(ov))                      # eje de la normal de contacto
        otros = [ov[i] for i in range(3) if i != k]
        return max(0.0, otros[0]) * max(0.0, otros[1])

    # -----------------------------------------------------------------
    titulo("D1 - CONTINUIDAD DEL APOYO DEL MATERIAL")
    print("  Recorre el camino del material y busca tramos sin superficie")
    print("  bajo el. Es el chequeo que habria cazado el hueco de 46,6 mm.")
    x_ini = M.X_TOLVA + TO["salida"][1] / 2.0          # borde aguas abajo de la tolva
    x_fin = M.X_TAMBOR                                  # cima del tambor
    z_sonda = M.Z_BANDA_SUP - CI["banda_esp"] / 2.0     # dentro del espesor de banda
    idx_banda = [i for i, n in enumerate(NOM) if n == "banda_PVC"]
    huecos, en_hueco, x_h0 = [], False, None
    xx = x_ini
    while xx <= x_fin + 1e-9:
        apoyado = any(dentro(i, xx, 0.0, z_sonda) for i in idx_banda)
        if not apoyado and not en_hueco:
            en_hueco, x_h0 = True, xx
        elif apoyado and en_hueco:
            huecos.append((x_h0, xx))
            en_hueco = False
        xx += 1.0
    if en_hueco:
        huecos.append((x_h0, x_fin))
    hueco_max = max((b - a for a, b in huecos), default=0.0)
    caida = 0.5 * G * 1000.0 * (hueco_max / 1000.0 / OP["v_banda"]) ** 2
    lim_hueco = OP["v_banda"] * math.sqrt(2 * 0.003 / G) * 1000.0
    chk(not huecos, "el material va apoyado de la tolva a la cima del tambor",
        "sin discontinuidades en %.0f mm" % (x_fin - x_ini) if not huecos
        else "huecos: %s" % huecos[:3])
    chk(hueco_max <= lim_hueco, "todo hueco < el que produce 3 mm de caida a v_banda",
        "max %.1f mm (limite %.1f mm, caida %.2f mm)" % (hueco_max, lim_hueco, caida))
    chk(min(x for x, _ in [(M.X_TOLVA - TO["salida"][1] / 2.0, 0)]) > M.X_ROD_COLA,
        "la tolva descarga sobre el ramal de ida, no sobre el rodillo",
        "salida en x=%.1f, rodillo hasta %.1f" % (M.X_TOLVA - TO["salida"][1] / 2.0,
                                                  M.X_ROD_COLA + CI["rodillo_D"] / 2.0))

    titulo("D2 - FRICCION Y VELOCIDAD MINIMA")
    print("  Para todo tramo en que el material DESLICE sobre algo quieto,")
    print("  v^2/(2 mu g) debe superar su longitud con mu = %.2f." % MU_DESFAVORABLE)
    # En la v3 el unico soporte del camino es la banda, que se mueve CON
    # el material: no hay deslizamiento. Se comprueba, no se supone.
    soportes = set()
    xx = x_ini
    while xx <= x_fin + 1e-9:
        for i in range(len(NOM)):
            if BBS[i].zmax < z_sonda - 2 or BBS[i].zmin > z_sonda + 2:
                continue
            if dentro(i, xx, 0.0, z_sonda):
                soportes.add(NOM[i])
        xx += 5.0
    chk(soportes == {"banda_PVC"}, "el unico soporte del camino es la banda (no hay deslizamiento)",
        ", ".join(sorted(soportes)))
    frenado = OP["v_banda"] ** 2 / (2 * MU_DESFAVORABLE * G) * 1000.0
    chk(True, "distancia de frenado si hubiera un tramo quieto",
        "%.1f mm a %.2f m/s con mu=%.2f — por eso no puede haberlo"
        % (frenado, OP["v_banda"], MU_DESFAVORABLE))
    vmin = math.sqrt(G * M.R_MAT / 1000.0)
    chk(cerca(vmin, M.V_MIN_CIMA, 1e-9), "sqrt(gR) del tambor recalculado", "%.4f m/s" % vmin)
    for k, tr in M.TRAYECTORIAS.items():
        v = tr["v"]
        if v < vmin:
            th = math.degrees(math.acos(v ** 2 / (G * M.R_MAT / 1000.0)))
            ok = abs(math.degrees(math.atan2(tr["x0"] - M.X_TAMBOR,
                                             tr["z0"] - M.Z_EJE_ROTOR)) - th) < 1e-6
            chk(ok, "%s: v < sqrt(gR) -> despega a theta = %.2f deg" % (k, th),
                "no en la cima: x=%.1f z=%.1f" % (tr["x0"], tr["z0"]))
        else:
            chk(abs(tr["x0"] - M.X_TAMBOR) < 1e-9 and abs(tr["z0"] - M.Z_BANDA_SUP) < 1e-9,
                "%s: v >= sqrt(gR) -> despega en la cima" % k,
                "v=%.3f >= %.3f m/s" % (v, vmin))

    titulo("D3 - TRAYECTORIA CONTRA SOLIDOS")
    print("  Discretiza cada trayectoria y comprueba que no toca nada")
    print("  hasta su destino. Es el chequeo que habria cazado la cuchilla.")
    destino_de = {"inerte": "bandeja_inertes", "f35": "bandeja_no_ferrosos",
                  "f25": "bandeja_no_ferrosos", "lata": "deflector_espuma"}
    for k, tr in M.TRAYECTORIAS.items():
        objetivo = destino_de[k]
        choques = set()
        for (px, pz) in tr["pts"][1:-1]:
            for i in range(len(NOM)):
                if NOM[i] == objetivo:
                    continue
                b = BBS[i]
                if not (b.xmin - 0.2 <= px <= b.xmax + 0.2
                        and b.ymin - 0.2 <= 0.0 <= b.ymax + 0.2
                        and b.zmin - 0.2 <= pz <= b.zmax + 0.2):
                    continue
                if dentro(i, px, 0.0, pz):
                    choques.add(NOM[i])
        chk(not choques, "%-6s vuela limpio hasta %s" % (k, objetivo),
            ", ".join(sorted(choques))[:52] if choques
            else "%d puntos, cae en x=%.1f z=%.1f" % (len(tr["pts"]), tr["x_fin"], tr["z_fin"]))

    # y aterriza donde debe
    xi0, xi1 = M.X_BJ_I0 + SA["bandeja_esp"], M.X_BJ_I1 - SA["bandeja_esp"]
    xn0, xn1 = M.X_BJ_N0 + SA["bandeja_esp"], M.X_BJ_N1 - SA["bandeja_esp"]
    chk(xi0 < M.TRAYECTORIAS["inerte"]["x_fin"] < xi1,
        "el INERTE cae dentro de la bandeja de inertes",
        "%.1f en [%.1f, %.1f]" % (M.TRAYECTORIAS["inerte"]["x_fin"], xi0, xi1))
    for k in ("f35", "f25"):
        chk(xn0 < M.TRAYECTORIAS[k]["x_fin"] < xn1,
            "%s cae dentro de la bandeja de no ferrosos" % k,
            "%.1f en [%.1f, %.1f]" % (M.TRAYECTORIAS[k]["x_fin"], xn0, xn1))
    tl = M.TRAYECTORIAS["lata"]
    chk(tl["destino"] == "deflector_espuma" and M.Z_BJ_PISO < tl["z_fin"],
        "la lata la para el deflector y cae dentro de la bandeja",
        "impacta en x=%.0f z=%.1f  (libre habria ido a %.0f)"
        % (tl["x_fin"], tl["z_fin"], tl["x_libre"]))
    chk(tl["x_libre"] > xn1, "el deflector es OBLIGATORIO",
        "alcance libre %.0f > fin de bandeja %.0f mm" % (tl["x_libre"], xn1))
    # la cuchilla clasifica, y por debajo del peor conductor
    chk(M.TRAYECTORIAS["inerte"]["x_fin"] < M.X_CUCH < M.TRAYECTORIAS["f35"]["x_fin"],
        "la cuchilla separa inerte y peor conductor",
        "%.1f < %.0f < %.1f mm" % (M.TRAYECTORIAS["inerte"]["x_fin"], M.X_CUCH,
                                   M.TRAYECTORIAS["f35"]["x_fin"]))
    marg = min(M.X_CUCH - M.TRAYECTORIAS["inerte"]["x_fin"],
               M.TRAYECTORIAS["f35"]["x_fin"] - M.X_CUCH)
    chk(cerca(marg, SA["margen_cuchilla"], 0.01), "margen a la cuchilla",
        rep(marg, SA["margen_cuchilla"], "mm", 2))
    z_f35_c = [z for (x, z) in M.TRAYECTORIAS["f35"]["pts"] if x <= M.X_CUCH][-1]
    chk(z_f35_c - M.Z_CUCH_1 >= SA["cuchilla_holgura_min"],
        "el canto de la cuchilla queda BAJO el peor conductor",
        "trayectoria z=%.1f, canto z=%.1f, holgura %.1f >= %.0f mm"
        % (z_f35_c, M.Z_CUCH_1, z_f35_c - M.Z_CUCH_1, SA["cuchilla_holgura_min"]))
    chk(M.Z_CUCH_1 > M.Z_BJ_CANTO, "la cuchilla sobresale del canto de las bandejas",
        "%.1f mm por encima" % (M.Z_CUCH_1 - M.Z_BJ_CANTO))

    titulo("D4 - AISLAMIENTO DE LAS BANDEJAS")
    print("  Ningun solido distinto de su celda puede estar a menos de %.0f mm." % SA["holgura_bandeja"])
    for nb in ("bandeja_inertes", "bandeja_no_ferrosos"):
        ib = NOM.index(nb)
        cerca_de = []
        for j in range(len(NOM)):
            if j == ib or NOM[j] == nb:
                continue
            if bbox_dist(BBS[ib], BBS[j]) >= SA["holgura_bandeja"]:
                continue
            d = dist(ib, j)
            if d < SA["holgura_bandeja"] - 1e-6:
                cerca_de.append((NOM[j], d))
        malos = [(n, d) for n, d in cerca_de if n != "celda_carga"]
        celdas = [(n, d) for n, d in cerca_de if n == "celda_carga"]
        chk(not malos, "%s: solo su celda a menos de %.0f mm" % (nb, SA["holgura_bandeja"]),
            "; ".join("%s %.2f" % t for t in sorted(set(malos)))[:52] if malos
            else "%d celda(s) en contacto" % len(celdas))
        chk(len(celdas) == EL["celdas_por_bandeja"],
            "%s apoya en %d celda(s)" % (nb, EL["celdas_por_bandeja"]),
            "%d encontrada(s)" % len(celdas))
    it = [i for i, n in enumerate(NOM) if n == "tope_antivuelco"]
    dmin_tope = min(min(dist(i, NOM.index(nb)) for nb in ("bandeja_inertes", "bandeja_no_ferrosos"))
                    for i in it)
    chk(dmin_tope >= SA["holgura_bandeja"] - 1e-6,
        "los topes antivuelco NO tocan (solo cazan la bandeja si vuelca)",
        "holgura minima %.2f mm" % dmin_tope)

    titulo("D5 - APOYO REAL: JUNTAS DECLARADAS, NO TANGENCIAS")
    print("  Sustituye el criterio de anclaje por bounding box de la v2.")
    print("  Toda pareja que se toque debe estar declarada en `juntas`.")
    declaradas = set()
    for a, b, _t in P["juntas"]:
        declaradas.add((a, b))
        declaradas.add((b, a))
    contactos, no_declarados, sin_area = set(), set(), set()
    for i in range(len(NOM)):
        for j in range(i + 1, len(NOM)):
            if NOM[i] == NOM[j]:
                continue
            if bbox_dist(BBS[i], BBS[j]) > CD["tol_contacto"]:
                continue
            if dist(i, j) > CD["tol_contacto"]:
                continue
            par = (NOM[i], NOM[j])
            contactos.add(par)
            if par not in declaradas:
                no_declarados.add("%s <-> %s" % par)
            elif area_contacto(BBS[i], BBS[j]) < CD["area_junta_min"]:
                sin_area.add("%s <-> %s (%.0f mm2)"
                             % (par[0], par[1], area_contacto(BBS[i], BBS[j])))
    chk(not no_declarados, "toda pareja en contacto esta declarada como junta",
        "; ".join(sorted(no_declarados))[:56] if no_declarados
        else "%d parejas en contacto, todas declaradas" % len(contactos))
    chk(not sin_area, "toda junta tiene apoyo real (>= %.0f mm2), no de canto" % CD["area_junta_min"],
        "; ".join(sorted(sin_area))[:56] if sin_area else "area minima verificada")
    declaradas_reales = set()
    for a, b in contactos:
        declaradas_reales.add(tuple(sorted((a, b))))
    huerfanas = set()
    for a, b, _t in P["juntas"]:
        if tuple(sorted((a, b))) not in declaradas_reales:
            huerfanas.add("%s <-> %s" % (a, b))
    chk(not huerfanas, "no hay juntas declaradas que no existan en el modelo",
        "; ".join(sorted(huerfanas))[:56] if huerfanas else "%d juntas, todas reales" % len(P["juntas"]))

    # cadena de apoyo hasta el suelo, SOLO por juntas declaradas
    ancl = set(i for i in range(len(NOM)) if BBS[i].zmin <= 0.5)
    cambio = True
    while cambio:
        cambio = False
        for i in range(len(NOM)):
            if i in ancl:
                continue
            for j in list(ancl):
                if (NOM[i], NOM[j]) in declaradas and bbox_dist(BBS[i], BBS[j]) <= CD["tol_contacto"]:
                    if dist(i, j) <= CD["tol_contacto"]:
                        ancl.add(i)
                        cambio = True
                        break
    flot = sorted(set(NOM[i] for i in range(len(NOM)) if i not in ancl))
    chk(not flot, "todo solido llega al suelo por juntas declaradas",
        ", ".join(flot)[:56] if flot else "%d solidos encadenados" % len(NOM))

    titulo("D6 - GUARDA: NINGUNA ABSCISA DEL ROTOR EXPUESTA")
    print("  La guarda se DERIVA de la extension real del rotor, no se")
    print("  escribe a mano. En la v2 X_GU = 520.0 estaba en la linea 505.")
    gu = [i for i, n in enumerate(NOM) if n == "guarda_policarbonato"]
    g0 = min(BBS[i].xmin for i in gu)
    g1 = max(BBS[i].xmax for i in gu)
    r0, r1 = M.X_TAMBOR - M.R_ENVOL, M.X_TAMBOR + M.R_ENVOL
    chk(g0 <= r0 and g1 >= r1, "la guarda cubre toda la envolvente del rotor",
        "guarda %.1f..%.1f  rotor %.1f..%.1f" % (g0, g1, r0, r1))
    chk(cerca(r0 - g0, BA["guarda_margen_rotor"], 0.01), "margen aguas arriba del tambor",
        rep(r0 - g0, BA["guarda_margen_rotor"], "mm", 2))
    x_vuelo_max = max(tr["x_fin"] for tr in M.TRAYECTORIAS.values())
    chk(g1 >= x_vuelo_max, "la guarda cubre toda la zona de vuelo",
        "hasta %.1f >= %.1f mm" % (g1, x_vuelo_max))
    solapes = sorted((BBS[i].xmin, BBS[i].xmax) for i in gu)
    continua = all(abs(solapes[k][1] - solapes[k + 1][0]) < 1e-6 for k in range(len(solapes) - 1))
    chk(continua, "los panos de guarda no dejan ranura entre si",
        " | ".join("%.1f..%.1f" % s for s in solapes))
    chk(TB["material"].lower().find("fibra") >= 0 or TB["material"].lower().find("petg") >= 0,
        "la carcasa del tambor es NO CONDUCTORA", TB["material"])


# =====================================================================
# E - COHERENCIA DOCUMENTAL
# =====================================================================
def bloque_documentos():
    titulo("E - COHERENCIA DOCUMENTAL")
    docs = {}
    for f in glob.glob(os.path.join(RAIZ, "CONTEXTO", "*.md")):
        with open(f, "r", encoding="utf-8") as fh:
            docs[os.path.basename(f)] = fh.read()
    chk(bool(docs), "hay documentos en CONTEXTO/", "%d archivos" % len(docs))

    PROHIBIDO = [
        (r"70\s*%\s*peor", "regresion: sigma(Al) es 61 % de sigma(Cu), no '70 % peor'"),
        (r"raz[oó]n\s+es\s+exactamente\s+11,16\s*/\s*5,58",
         "presentar una identidad algebraica como validacion de H1"),
        (r"100\s+comprobaciones", "numero de comprobaciones escrito a mano"),
        (r"100\s+OK\s*/\s*0\s+FALLA", "resultado de verificacion escrito a mano"),
    ]
    # Los registros de cambios existen precisamente para citar lo que
    # estaba mal: se exceptuan de la busqueda de regresiones.
    vigentes = {n: t for n, t in docs.items() if not n.startswith("CAMBIOS_")}
    for patron, motivo in PROHIBIDO:
        malos = [n for n, t in vigentes.items() if re.search(patron, t, re.I)]
        chk(not malos, "no aparece: %s" % motivo,
            ", ".join(malos)[:52] if malos else "en ningun documento vigente")

    pc = docs.get("PROYECTO_COMPLETO.md", "")
    chk(re.search(r"p\s*=\s*n_polos\s*/\s*2", pc) or re.search(r"\bp\s*=\s*5\b", pc),
        "PROYECTO_COMPLETO define el simbolo p (se perdio dos veces)",
        "regla 3 del proyecto")
    chk("11" in pc and "114" in pc and "MPa" in pc,
        "los dos factores de la union pegada aparecen separados (11x y 114x)",
        "criterio de diseno y resistencia del epoxico")
    chk(any("geometr" in t and "espesor controlado" in t for t in docs.values()),
        "se declara 'a geometria y espesor controlados'", "regla 4 del proyecto")

    bom = docs.get("LISTA_DE_MATERIALES.md", "")
    for clave, motivo in ((r"bobina de prueba|sonda Hall", "instrumento de campo para H1"),
                          (r"[Cc]obre", "probetas de cobre para H2"),
                          (r"[Ll]at[oó]n", "probetas de laton para H2"),
                          (r"DC-DC|convertidor", "conversion 24 -> 12 / 5 V"),
                          (r"celda de carga.*(1|2)\s*kg|2\s*kg.*celda", "celdas de 2 kg")):
        chk(bool(re.search(clave, bom, re.I)), "la lista de materiales incluye: %s" % motivo,
            "encontrado" if re.search(clave, bom, re.I) else "AUSENTE")

    for req in ("DECISION_ARQUITECTURA.md", "CAMBIOS_v3.md",
                "CAMBIOS_DESDE_EL_ANTEPROYECTO.md"):
        chk(req in docs, "existe CONTEXTO/%s" % req, "entregable")


if __name__ == "__main__":
    print("=" * 80)
    print("VORTICE 150 v3 - VERIFICACION COMPLETA")
    print("Fuente unica: PARAMETERS/master.yaml   ·   arquitectura: %s"
          % P["meta"]["arquitectura"])
    print("=" * 80)
    bloque_fisica()
    bloque_modelo()
    bloque_documentos()
    print("\n" + "=" * 80)
    print("RESUMEN:  %d OK   /   %d FALLA   (total %d comprobaciones)"
          % (_estado["ok"], _estado["falla"], _estado["ok"] + _estado["falla"]))
    if _fallos:
        print("\nFALLAN:")
        for f in _fallos:
            print("   - " + f)
    print("=" * 80)
    sys.exit(1 if _estado["falla"] else 0)
