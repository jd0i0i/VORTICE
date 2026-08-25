# VÓRTICE 150 — Decisiones confirmadas

*Cada decisión de este documento está tomada y validada. No se revierten sin una razón nueva.*
*Actualizado: 24/08/2026 · Corresponde a `PARAMETERS/master.yaml` **versión 3***

---

## 1 · Cómo leer este documento

Hay cuatro clases de entrada:

| Marca | Significado |
|---|---|
| **(v1)** | Decisión que ya venía validada del paquete original. Solo se implementó. |
| **[BUG]** | Defecto real que se detectó y se corrigió. |
| **[AUTÓNOMA]** | Decisión que las cotas originales no cubrían y hubo que tomar. Criterio: **la más conservadora en seguridad y la más barata en costo.** |
| **[VERIFICAR]** | Número sin fuente citable todavía. **No puede presentarse como resultado.** |

Todo número citado sale de `PARAMETERS/master.yaml`. Para conocer el estado de la verificación, **ejecuta `verificar.py`**: no hay recuentos escritos en estos documentos, y el propio verificador falla si encuentra uno.

---

## 2 · Sistema de coordenadas

- **X** — avance del material, `X = 0` en el eje del rodillo de cola (que en la v3 es además el motriz y el tensor).
- **Y** — transversal, `Y = 0` en el plano medio.
- **Z** — dos orígenes que **no deben confundirse**:
  - `z_cotas` desde la **cara superior de la base**.
  - `z_cad` desde el **suelo**, `z_cad = z_cotas + 48`. El modelo 3D usa este, para que la verificación de sólidos tenga un `z = 0` físico real.

**En la v3 no hay desplazamientos ocultos.** El generador no mueve nada: las posiciones de `montaje` son las que construye, y `verificar.py` las contrasta **cota a cota** con tolerancia de 1 µm. En la v2 el YAML decía `x_rodillo_cabeza = 500`, el generador construía 468,4, el documento decía 477 y la lámina imprimía 480. Cuatro cifras para la misma cosa, y ninguna comprobación entre ellas.

### Identidades que cierran

| Identidad | Comprobación |
|---|---|
| `D_r = OD + 2·T` | 101,6 + 10 = **111,6** ✓ |
| `λ = π·D_r/p` | π·111,6/5 = **70,12034802812418** ✓ |
| `z_boca = banda + luz` | 400 + 60 = **460** ✓ |
| `altura_total = base + boca + cuello + cono` | 18+460+30+170 = **678** ✓ |
| `entrehierro = zuncho + holgura + carcasa + banda` | 0,5+1,0+1,0+1,5 = **4,00** ✓ |
| `R_material = OD_carcasa/2 + espesor de banda` | 58,3 + 1,5 = **59,80** ✓ |

> La quinta identidad de la v2 era `x_inerte = v·√(2h/g) = 99,95 mm`. **Se retiró**: era aritméticamente correcta y físicamente inválida — suponía que el inerte salía horizontal desde el borde de una plancha a la que nunca llegaba.

---

## 3 · La arquitectura del lanzamiento

**El rotor magnético es el tambor de cabeza.** Gira dentro de una carcasa no conductora que rueda libre sobre su mismo eje mediante dos rodamientos 6004-2RS, y la banda envuelve esa carcasa.

La comparación cuantificada de las tres opciones evaluadas está en **`CONTEXTO/DECISION_ARQUITECTURA.md`**. Resumen de por qué A:

- Cierra por construcción el hueco de transferencia, la fricción sobre placa quieta y el problema de √(gR).
- Cuesta **−16,4 %** de fuerza (entrehierro 3,0 → 4,00 mm), contra el **−30,1 %** de la alternativa C.
- La alternativa B (plancha inclinada) es **geométricamente imposible**: la cima del rotor está a 445,5 y el intradós de cualquier placa debe estar a ≥447,0, o sea el trasdós al nivel exacto de la banda. No hay altura donde inclinar nada. Forzarla bajando el rotor 18,8 mm deja **el 3,4 % de la fuerza**.
- Es la configuración industrial real, y eso vale en el criterio 2.

---

## 4 · Los cinco bloqueantes corregidos

Detalle completo en `CAMBIOS_v3.md`. Resumen de lo que se decidió:

### [BUG] B-1 · La cuchilla interceptaba toda la fracción conductora

La cuchilla iba de z=262 a z=462 con el lanzamiento en z=448: **14 mm por encima**. Las tres trayectorias conductoras golpeaban su cara aguas arriba. **La máquina clasificaba al revés.**

**Corrección.** La cuchilla es un **canto**, no un muro: filo a **40 mm** sobre el tejadillo, 38 mm sobre el canto de las bandejas. La trayectoria más baja pasa 49,6 mm por encima, contra un mínimo exigido de 20.

### [BUG] B-2 · Hueco abierto de 46,6 mm entre la banda y la plancha

**Corrección.** No hay transferencia: la banda envuelve el tambor y el material va apoyado hasta el lanzamiento.

### [BUG] B-3 · El inerte se paraba por fricción sobre la plancha

Frenado a 0,35 m/s: **25,0 mm** con μ=0,25 y **12,5 mm** con μ=0,50, de los 80 disponibles.

**Corrección.** No hay plancha. El único soporte del camino es la banda, **que se mueve con el material**.

### [BUG] B-4 · Velocidad mínima de despegue

`√(gR) = 0,743 m/s` con R=56,3; la banda va al 47 %. **El número es correcto pero no era la causa de B-2 ni de B-3** — en la arquitectura vieja el material nunca tenía que volar sobre un cilindro. En la nueva, √(gR) no es un obstáculo: **es lo que fija el punto de lanzamiento**, y la diferencia entre despegar en la cima (conductoras) y no despegar (inertes) **es la separación**.

### [BUG] B-5 · La cuchilla y el deflector puenteaban las bandejas al bastidor

Dos mecanismos distintos, y esto importa:

- El deflector estaba en la lista `PERMITIDO`, que lo silenciaba **por diseño**.
- **La cuchilla NO estaba en `PERMITIDO`.** Apoyaba *exactamente* en z=262: el chequeo de interferencia (tolerancia **+0,6**) veía solape −0,6 y callaba, mientras el de anclaje (tolerancia **−0,6**) veía contacto +0,6 y la daba por apoyada. **La misma tangencia era invisible como choque y válida como apoyo.**

**Corrección.** Se eliminó la lista `PERMITIDO` entera. En su lugar hay una tabla **`juntas`** en el YAML: toda pareja que se toque debe estar declarada, con su tipo de unión, y toda junta declarada debe tener **≥ 100 mm² de contacto real**. Cuchilla y deflector cuelgan del bastidor con **5 mm** de holgura a las bandejas en todas las direcciones.

---

## 5 · Decisiones de ingeniería confirmadas

| Decisión | Razón |
|---|---|
| Tubo **acero cédula 40 de 3-1/2"** | Pared 5,74 mm > mínimo por saturación 4,39 mm, con `t = W·Br/(2·B_sat)` |
| **60 imanes N52 60×10×5**, magnetizados **a través de los 5 mm** | 10 polos × 2 piezas × 3 filas. Da λ = 70,12 mm y α = 0,627 |
| Retención **doble**: tiras PETG + zunchado | El hueco entre polos (11,92 mm) admite la tira (11,3) con 0,6 de juego. El pegado solo no basta para 52,6 N por imán |
| **Dos chumaceras UCP204**, span 340 | Flecha 0,044 mm, crítica **4.500 rpm**, se trabaja al **44,4 %** |
| Motor **DC 24 V / 350 W** desplazado 180 mm a 220°, correa **HTD-5M** | Nunca acoplado directo: los imanes interferirían con los del motor y el par de arranque dañaría el eje. A 220° el ramal de retorno libra la cima del motor por 26,5 mm (a 215° eran 15) |
| **Entrehierro 4,00 mm** indexable a 5,5 / 7,0 / 8,5 | Desglose 0,5 zuncho + 1,0 holgura + 1,0 carcasa + 1,5 banda. Abrirlo al máximo deja la fuerza en **×0,446**: es el experimento de H1 |
| **Cuchilla ajustable** 643–743 en 6 posiciones de 25 mm | El inerte cae a 574,0 y el peor conductor a 861,5: margen de **143,5 mm** a cada lado. **Las bandejas se mueven con ella** sobre un carril común — si no, "ajustable" sería mentira |
| **Deflector obligatorio** a 1.090 | La media lata alcanzaría 1.541,9 y la bandeja acaba en 1.158,5. Golpea la espuma a z=338 y cae dentro |
| **Una celda de 2 kg por bandeja, dos canales** | Dos fracciones, dos celdas. 20 kg de fondo de escala para medir 83,7 g de aluminio era una cuantización del 6 % |
| **Seta que corta la alimentación físicamente** | No es una entrada de software: si el ESP32 se cuelga, la seta sigue funcionando |

---

## 6 · Decisiones [AUTÓNOMA] de la v3

### 6.1 Del tambor de cabeza

| # | Decisión | Por qué |
|---|---|---|
| A-19 | **Holgura radial rotor→carcasa: 1,0 mm** | Es lo mínimo que admite un montaje concéntrico con el zuncho laminado a mano. Cada décima cuenta: va directa al entrehierro |
| A-20 | **Pared de carcasa 1,0 mm, laminado de fibra y epóxico** | Mismo material y misma técnica del zuncho: no añade partidas a la lista, solo el mandril. **Debe ser no conductora** o sería una espira en cortocircuito girando en el campo |
| A-21 | **Largo de carcasa 228 mm** (y = ±114) | Cubre la banda de 150 y deja sitio a los discos de extremo fuera del tubo de 200 |
| A-22 | **2 discos de PETG impreso de 12 mm con 6004-2RS** | El rodamiento (12 mm de ancho) no cabe en los 10 mm que quedan entre el largo activo y el extremo del tubo: los discos van **por fuera** del tubo |
| A-23 | **Manguitos deslizantes, no partidos**, de 1,5 / 3,0 / 4,5 | Un manguito partido dejaría dos costuras bajo la banda. Se cambian retirando un disco de extremo |
| A-24 | **Las galgas cambian de cometido** | Ya no indexan el entrehierro (lo hace el manguito): ahora **bajan el eje** `galga = pared del manguito` para que la línea de banda se mantenga en z=400. La convención de signo de A-17 se conserva intacta |
| A-25 | **Tensor de 40 mm** (±20) | El cambio de manguito mueve el desarrollo de banda 14,69 mm; el resto es margen para el estirado |
| A-26 | **El rodillo de cola es el motriz y el tensor** | Accionar el tambor obligaría a atravesar la carcasa que rueda libre |

### 6.2 De la salida

| # | Decisión | Por qué |
|---|---|---|
| A-27 | **Ranura de 13 mm entre bandejas + tejadillo de 25** | Las bandejas no pueden tocarse entre sí (acoplaría las dos medidas) ni tocar la cuchilla. El tejadillo cubre la ranura desde 5 mm por encima del canto para que nada se cuele a la base |
| A-28 | **Bandejas de PP corrugado sobre marco de aluminio** | 0,36 y 0,55 kg contra los 2,36 kg de acrílico de 4 mm. La tara es lo que fija el fondo de escala, y el fondo de escala es lo que fija la resolución |
| A-29 | **Topes antivuelco con 6 mm de holgura** | No tocan nunca: solo cazan la bandeja si alguien la golpea. Si tocaran, falsearían el peso |
| A-30 | **Deflector adelantado a x=1.090** | Con el deflector al final, la bandeja de no ferrosos habría medido 768 mm y ninguna celda monopunto tolera esa plataforma. Adelantándolo, la bandeja baja a 434 |

### 6.3 Del bastidor

| # | Decisión | Por qué |
|---|---|---|
| A-31 | **Base de 1.300 mm** (era 1.650) | La máquina mide 1.526 de extremo a extremo. El lanzamiento se adelantó 95 mm y el deflector 375 |
| A-32 | **Dos ventanas de inspección por lado** (eran tres) | Con base de 1.300 no caben tres de 300 sin cruzar la escotadura del rotor (380–620) ni los 100 mm extremos |
| A-33 | **Subplaca de 240 × 131 × 10** (era ×150) | Con 150 llegaba a y=100, que era tangente al tubo. La carcasa llega a y=±114: con 131 queda a 5 mm de ella |
| A-34 | **Guarda derivada, dos paños de 371 × 330** | Debe cubrir la envolvente real del rotor **con el manguito más grueso** (437,2…562,8) y toda la zona de vuelo. Dos paños para abrir solo la mitad |
| A-35 | **Cuña de motor en V** | Un bloque recto dejaba el motor 0,8 mm por encima, sin apoyarse en nada |
| A-36 | **Eje de motor modelado, Ø12** | Con la polea calzada contra la carcasa, la correa rozaba el motor |

### 6.4 De materiales y física

| # | Decisión | Valor | Por qué |
|---|---|---|---|
| A-10…A-15 | Densidades y B_sat | (sin cambios) | Reproducen las masas al dígito |
| A-16 | **Criterio de unión pegada: 1 MPa** | — | El **criterio de diseño** es 1 MPa (factor 11×); la **resistencia real** del epóxico es ~10 MPa (factor 114×). Se guardan y se citan **por separado** |
| A-37 | **ρ_e de Al 1050, Cu ETP y latón CuZn37** | 2,82 / 1,72 / 6,40 ×10⁻⁸ Ω·m | Se fija una ρ por material y se usa la misma en δ y en σ/ρ_m. La de aluminio es la que ya usaba el anteproyecto. **[VERIFICAR]** las páginas exactas |
| A-38 | **Densidad efectiva del PP corrugado: 250 kg/m³** | — | Es mayormente aire. **[VERIFICAR]** con el material real antes de fiarse de la tara |
| A-39 | **Salida de tolva 130 mm** (era 150) | — | Con 150 sobre una banda de 150 el material caía justo sobre los cantos y sobre las guías laterales. Con 130 quedan 10 mm de margen por lado |
| A-40 | **Tensión de banda derivada, no supuesta** | T1+T2 = 39,07 N | T2 sale de limitar la flecha del ramal de retorno a 5 mm en el vano de 500; T1 = T2 + la fuerza tangencial. La v2 no tenía este cálculo, y por eso su velocidad crítica estaba mal |

---

## 7 · Lo que se retiró de la v2 y no vuelve

- **La plancha fija y sus dos carriles.** El documento afirmaba que la plancha «apoya 20 mm sobre un carril a cada lado»; en la geometría, `plancha_fija` ocupaba y ∈ [−95, 95] y `plancha_carril` y ∈ [95, 150]: **el solape era exactamente 0 mm**. Pasaba la verificación porque el chequeo de anclaje usaba proximidad de *bounding boxes* con tolerancia −0,6 mm: **rozarse contaba como apoyarse**.
- **La lista `PERMITIDO`.** Sustituida por la tabla `juntas`.
- **La comprobación de que (λ/2π)/(λ/4π) = 2.** Da 2 por álgebra, con cualquier D_r y cualquier p. Presentarla como validación de H1 es exactamente lo que castiga el criterio 2 de la feria. Se retiró del verificador **y** del documento del proyecto.
- **La afirmación «ningún script lleva cotas escritas a mano».** Era falsa: había once en el generador del modelo y una en el de láminas, que dibujaba la cinta 3,4 mm fuera de sitio. Ahora es cierta, y por eso puede volver a escribirse.
- **`h_caida` como cota.** Ahora se deriva de la geometría.
- **Los cuatro alcances como parámetros.** Ahora se guardan **velocidades de salida** marcadas `[VERIFICAR]`, y los alcances se derivan.

---

## 8 · Trazabilidad

```
PARAMETERS/master.yaml          ← única fuente numérica
   ├── generar_modelo3d.py      → CAD/STEP · CAD/STL · 3 renders · derivados_cad.json
   ├── generar_planos.py        → 3 láminas acotadas (SVG + PNG), desde derivados_cad.json
   └── verificar.py             → física · geometría · montaje · camino del material · documentos
```

Ninguna cota vive en un script. Cambiar el YAML y volver a ejecutar los tres regenera el paquete completo y vuelve a comprobarlo. Y ahora, además, `verificar.py` **falla** si el YAML y el generador se desincronizan, si algo toca una bandeja, si una trayectoria atraviesa un sólido o si un documento contradice al modelo.
