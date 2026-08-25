# VÓRTICE 150 — Cambios de la v2 a la v3

*Qué cambió, por qué, y qué números anteriores quedan invalidados.*
*Actualizado: 24/08/2026 · `PARAMETERS/master.yaml` v3*

---

## 0 · Resumen en una frase

La v2 tenía **cinco defectos bloqueantes** que sus 100 comprobaciones no podían ver, porque validaban números contra fórmulas y sólidos contra sólidos, pero **nunca el camino que recorre el material**. La v3 cambia la arquitectura del lanzamiento, corrige los cinco, y añade las cinco familias de comprobación que los habrían cazado.

---

## 1 · Los cinco bloqueantes y qué se hizo con cada uno

### B‑1 · La cuchilla interceptaba el 100 % de la fracción conductora

**Era.** La cuchilla iba de z=262 a z=462. El plano de lanzamiento estaba en z=448: el canto quedaba **14 mm por encima del punto de salida del material**. Recalculando cada trayectoria hasta x=841:

| | z al llegar a la cuchilla | |
|---|---|---|
| Fragmento 35 mm | 289,7 mm | **choca** |
| Fragmento 25 mm | 360,5 mm | **choca** |
| Media lata | 428,9 mm | **choca** |

Las tres conductoras golpeaban la cara aguas arriba y caían en la bandeja de inertes: **la máquina clasificaba al revés**.

**Es.** La cuchilla es un **canto**, no un muro: `cuchilla_H = 40 mm` medidos sobre el tejadillo, con el filo en z=274, o sea **38 mm sobre el canto de las bandejas**. La trayectoria más baja pasa por z=323,6 en esa abscisa: **49,6 mm de holgura**, contra un mínimo exigido de 20. Lo comprueba D3 en cada ejecución.

### B‑2 · Hueco abierto de 46,6 mm entre la banda y la plancha

**Era.** Al corregir el bug B‑02 de la v1, la v2 desplazó **toda la cinta** 31,6 mm aguas arriba pero **no movió la plancha**. Quedaban 46,60 mm de aire entre la descarga (x=468,4) y el borde de la plancha (x=515). Una pieza a 0,35 m/s cruzaba ese hueco en 0,1331 s y caía **86,9 mm**: impactaba el flanco del rotor en x=501,1 · z=405,3, a **73,4° aguas arriba de la cima**, contra una superficie a 8,18 m/s.

**Es.** No hay transferencia. **El rotor es el tambor de cabeza** y la banda lo envuelve: el material va apoyado hasta el instante del lanzamiento. Lo comprueba D1, que recorre el camino sólido a sólido.

### B‑3 · El inerte se detenía por fricción sobre la plancha

**Era.** Plancha horizontal de 80 mm. Distancia de frenado a 0,35 m/s: **25,0 mm** con μ=0,25 y **12,5 mm** con μ=0,50. El inerte no llegaba nunca al borde.

**Es.** No hay plancha. El único soporte del camino del material es la banda, **que se mueve con él**. D2 lo comprueba sobre los sólidos: enumera qué soporta el material en cada abscisa y exige que sea sólo `banda_PVC`.

### B‑4 · A 0,35 m/s nada puede volar sobre el rotor

**El número es correcto**: `√(gR) = √(9,81 × 0,0563) = 0,743 m/s`, y la banda va al 47 % de eso.

**Pero no era la causa raíz de B‑2 ni de B‑3.** En la arquitectura v2 el material nunca tenía que volar sobre un cilindro: la plancha era un puente plano. Lo que mataba aquella arquitectura era B‑3 (una placa quieta, sin nada que empuje) agravado por B‑2. √(gR) solo pasa a ser vinculante en la arquitectura nueva, y allí **no es un obstáculo: es lo que fija el punto de lanzamiento**. A 0,35 m/s el inerte no despega en la cima; sigue la banda hasta θ = 77,95° y sale tangencialmente.

La conclusión operativa de B‑4 —*no lo arregles moviendo la plancha*— se mantiene, y por una razón más fuerte: aunque se pegara la plancha a la banda y el hueco fuera cero, B‑3 seguiría parando el inerte en 12,5 mm.

### B‑5 · La cuchilla y el deflector puenteaban las bandejas pesadas al bastidor

**Era.** El `deflector_placa` iba de z=108 a z=508 **atravesando el piso de la bandeja de no ferrosos** (piso en z=112). La `cuchilla_divisora` arrancaba en z=262, exactamente el canto de las dos bandejas. Con esos contactos, las celdas medían una fracción indeterminada del peso.

Los dos mecanismos por los que se escapaba eran **distintos**:

- El deflector estaba en la lista `PERMITIDO`, que lo silenciaba por diseño.
- **La cuchilla NO estaba en `PERMITIDO`.** Se escapaba porque apoyaba *exactamente* en z=262: el chequeo de interferencia usaba tolerancia **+0,6** y veía solape −0,6 (callaba), mientras el de anclaje usaba **−0,6** y veía contacto +0,6 (la daba por apoyada). **La misma tangencia era invisible como choque y válida como apoyo.**

**Es.** Ni la cuchilla ni el deflector tocan bandeja. Ambos cuelgan del bastidor:

- Cuchilla: filo + tejadillo + dos montantes de solape + travesaño atornillado a los laterales. Holgura a cada bandeja: **5,0 mm**.
- Deflector: placa y espuma colgadas de su propio travesaño, con **5 mm** al piso y **5 mm** a las paredes interiores.
- Entre las dos bandejas hay una **ranura de 13 mm** que el tejadillo cubre desde 5 mm por encima del canto.
- **Se eliminó la lista `PERMITIDO` entera** y se sustituyó por una tabla `juntas` de 57 entradas: toda pareja que se toque debe estar declarada, y toda junta declarada debe tener **≥ 100 mm² de contacto real**. Una tangencia sin declarar es una falla. Lo comprueban D4 y D5.

---

## 2 · Números de la v2 que quedan INVALIDADOS

No los conserves, no los cites y no los reutilices.

| Magnitud | v2 | v3 | Por qué |
|---|---|---|---|
| **Los cuatro alcances** (99,9 / 391 / 526 / 1.127) | desde el borde de plancha | **574,0 / 861,5 / 986,3 / 1.541,9** absolutos | Otra arquitectura, otro punto de lanzamiento, y el piso real está a z=106 |
| `h_caida` | 400 mm nominal / 336 real | **342 mm, derivado** | Ya no es una cota: sale de `z_banda_sup − z_bandeja_piso` |
| `cuchilla_x` | 246 desde la plancha (841 abs.) | **718 absoluto** | Equidistante entre el inerte y el peor conductor |
| `cuchilla_H` | 200 mm | **40 mm** | Era un muro; es un canto |
| `margen_cuchilla` | 145 mm | **143,5 mm** | Recalculado sobre la balística nueva |
| Entrehierro nominal | 3,0 mm | **4,00 mm** | 0,5 zuncho + 1,0 holgura + 1,0 carcasa + 1,5 banda |
| `z_index` | 3,0 / 4,5 / 6,0 / 7,5 | **4,0 / 5,5 / 7,0 / 8,5** | Se indexa con manguitos, no bajando el rotor |
| `banda_L` | 1.188,50 mm | **1.279,00 mm** | Dos diámetros distintos: 116,6 y 60 |
| `x_rodillo_cabeza` | 500 (real 468,4) | **no existe** | El tambor sustituye al rodillo de cabeza |
| `recorrido_asentamiento` | 405 en el YAML, 477 en el doc, 480 en la lámina, 476,6 real | **405 en los cuatro sitios** | Una sola cifra, verificada contra el generador |
| `N_critica` / `pct_critica` | 5.951 rpm / 33,6 % | **4.500 rpm / 44,4 %** | La v2 **no contabilizaba** la carga de banda sobre el eje |
| `flecha_eje` | 0,0253 mm | **0,0442 mm** | Ídem |
| `base_L` | 1.650 mm | **1.300 mm** | La máquina mide 1.526 de extremo a extremo |
| Celdas de carga | 8 × 5 kg (20 kg de FS por bandeja) | **2 × 2 kg, una por bandeja** | 20 kg de fondo de escala para medir 83,7 g de aluminio |
| `resolucion_celda` | 5 g, como hecho | **1 g, marcado `[VERIFICAR]`** con protocolo | No es FS/2²⁴; la fija el piso de ruido |
| Bandejas | acrílico 4 mm, 280×200 y 280×700 | **PP corrugado 3 mm + marco de aluminio**, 280×214 y 280×428 | Tara de 2,36 kg para pesar 83,7 g |
| `plancha_*`, `plancha_carril` | existían | **eliminados** | Ver `DECISION_ARQUITECTURA.md` |
| Guarda | 520×330, `X_GU=520` a mano | **741×330 en dos paños, derivada** | Debe cubrir toda la envolvente del rotor y toda la zona de vuelo |
| Salida de tolva | 150 mm sobre banda de 150 | **130 mm** | El material caía justo sobre los cantos y las guías |
| `tolva.volumen_L` / `angulo` | 4,47 L / 65,0° | **4,329 L / 64,799°** | Consecuencia de la salida de 130; el 65,0 nunca fue exacto |
| Ventanas de inspección | 3 por lado | **2 por lado** | Con base de 1.300 no caben tres sin cruzar la escotadura |

---

## 3 · La afirmación que era falsa

`PROYECTO_COMPLETO.md` y `DECISIONES_CONFIRMADAS.md` decían, los dos:

> «Ningún script lleva cotas escritas a mano.»

Era falso. Había **once** en `generar_modelo3d.py` —`X_GU = 520.0`, `Y_POLEA = 120.0`, `caja_control` en x=1150, celdas en y=±110, `Z_ESC_TOP … + 7.0`, `z = 250…400` en crudo, los offsets de patas, cuñas, alivio de subplaca, soporte de cuchilla y travesaño de deflector, y el umbral `vol > 25.0`— y una duodécima, peor, en `generar_planos.py`:

```python
xrc = MO["x_rodillo_cabeza"] - 35.0     # el generador calculaba -31,5988
```

Las láminas dibujaban la cinta y la tolva **3,4 mm fuera de sitio respecto del STEP** e imprimían un recorrido de asentamiento de **480 mm** que no era el de ninguna de las dos. La línea de al lado calculaba el desplazamiento correcto y no se usaba nunca.

**En la v3 todas viven en `master.yaml`**, en las secciones `cad` y `montaje`, y `generar_planos.py` no calcula ninguna posición: lee `derivados_cad.json`, que escribe el generador del modelo 3D. **Las láminas dibujan la misma trayectoria, punto por punto, que verifica `verificar.py`.**

---

## 4 · Las cinco familias de comprobación nuevas

Se añadieron a `verificar.py` como bloque D, y **fallan de verdad**: devuelven código de salida distinto de cero.

| | Qué recorre | Qué habría cazado |
|---|---|---|
| **D1 · Continuidad del apoyo** | Sondea el camino del material milímetro a milímetro entre los sólidos reales y busca tramos sin superficie debajo | **B‑2**, el hueco de 46,6 mm |
| **D2 · Fricción y velocidad mínima** | Enumera qué sólido soporta el material en cada abscisa; exige que sea uno que se mueva con él. Recalcula √(gR) y el ángulo de despegue | **B‑3** y **B‑4** |
| **D3 · Trayectoria contra sólidos** | Discretiza las cuatro trayectorias en 240 puntos y clasifica cada punto contra los 139 sólidos | **B‑1**, la cuchilla — y de hecho cazó un error de signo propio (ver §6) |
| **D4 · Aislamiento de bandejas** | Distancia real (no *bounding box*) de cada bandeja a todo lo demás | **B‑5** |
| **D5 · Apoyo real** | Contacto declarado + área ≥ 100 mm² + cadena al suelo solo por juntas declaradas | **B‑5** por su otra vía, la tangencia invisible |

Se añadió además **D6 · Guarda**, que exige que no quede ninguna abscisa del rotor sin cubrir, con la guarda **derivada** de la envolvente real del rotor y de la zona de vuelo.

### Y una comprobación que se eliminó

```python
chk(cerca(GE["lam_2pi"] / GE["lam_4pi"], 2.0, 0.002),
    "razon campo/fuerza = 2  (hipotesis central)")
```

Es dividir λ/2π entre λ/4π. **Da 2 por álgebra, con cualquier D_r y cualquier p**, y presentarla como validación de H1 es exactamente lo que castiga el criterio 2 de la feria. La misma frase estaba en `PROYECTO_COMPLETO.md` §3 —*"la razón es exactamente 11,16 / 5,58 = 2,000"*— y también se quitó de ahí.

En su lugar, `verificar.py` comprueba que **H1 declara con qué se va a medir** y `verificar.py` bloque E comprueba que **ese instrumento está en la lista de materiales**. Lo que se contrasta es la caída **medida** de la fuerza al abrir el entrehierro, contra `e^(−z/(λ/4π))` con el λ/4π que salga del campo medido.

---

## 5 · Correcciones documentales

| | Era | Es |
|---|---|---|
| Hipótesis 2 | «pese a conducir un **70 % peor**» | σ(Al) ≈ 0,610·σ(Cu) (61 % IACS): **conduce un 39 % menos** |
| Unión pegada | solo «0,088 MPa → factor **114×**» | **11×** contra el criterio de diseño (1 MPa) **y** 114× contra la resistencia del epóxico (10 MPa), separados |
| Profundidad de piel | no estaba en el YAML | **δ(Al) = 7,82 mm** a 116,67 Hz con ρ=2,82×10⁻⁸ Ω·m. El anteproyecto citaba 4,9 mm porque trabajaba a 300 Hz |
| Figura de mérito σ/ρ_m | citada sin tabla | **Al 1,313×10⁴ · Cu 6,489×10³ · latón 1,845×10³**, con ρ_e y ρ_m de cada uno |
| Sagita | 0,247 mm, «del imán» | **0,247 mm la pieza de 10** y **0,994 mm el POLO real de 20**, que es el que importa para el pegado |
| H1 | sin instrumento | bobina de prueba + sonda Hall, **en la lista de materiales** |
| H2 | sin probetas de Cu | lote H2: **Al, Cu y latón**, 25×25×0,5 mm, «a geometría y espesor controlados» |
| Alimentación | fuente única de 24 V | **+ dos convertidores DC‑DC**, a 12 V (vibrador) y a 5 V (lógica) |
| Motorreductor de banda | «24 V DC 100 rpm» | **≥143,2 rpm**, que es lo que pide `v_banda_max` |
| Tabla de recortes | titulada «Si hay que caber en 1.000.000 COP» | reescrita: **el techo y esta máquina son incompatibles**, y hay que decidir cuál cambia |

---

## 6 · Un error propio, cazado por las comprobaciones nuevas

Al implementar la balística nueva se escribió el tiempo de vuelo con el signo cambiado:

```python
t = (-vz + sqrt(vz**2 + 2*g*dz)) / g     # MAL: raiz del lanzamiento hacia ARRIBA
t = ( vz + sqrt(vz**2 + 2*g*dz)) / g     # BIEN
```

Con `vz` negativo —el caso del inerte, que despega a 78° de la cima bajando— la trayectoria **atravesaba el piso de la bandeja** y terminaba en z = −87 mm. **D3 lo reportó** como *"el inerte choca con base_MDF y celda_carga"*. Corregido, el alcance del inerte pasa de 579,1 a **574,0 mm**, y con él la cuchilla de 720 a **718**.

Ninguna comprobación de la v2 lo habría visto.

---

## 7 · Estado

`verificar.py` recorre ahora física, geometría, montaje, camino del material y coherencia documental. Ejecutarlo es la única forma legítima de citar el resultado: **no lo escribas a mano en ningún documento** — el bloque E falla si encuentra un recuento escrito.

```bash
python .claude/skills/vortice-cad/generar_modelo3d.py   # STEP, STL, renders, derivados
python .claude/skills/vortice-cad/generar_planos.py     # las 3 laminas
python .claude/skills/vortice-validation/verificar.py   # todas las comprobaciones
```
