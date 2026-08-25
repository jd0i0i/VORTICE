# VÓRTICE 150 — Proyecto completo

### Separador de metales no ferrosos por corrientes de Foucault
**Banco de ensayo instrumentado · XIII GeoExpoFísica-Uninorte 2026**

*Actualizado: 24/08/2026 · Corresponde a `PARAMETERS/master.yaml` **v3***
*Todas las cotas en milímetros salvo indicación explícita.*

---

# 1 · Qué es

Un rotor de acero con **60 imanes de neodimio N52 en polaridad alternada** gira **dentro de una carcasa no conductora que hace de tambor de cabeza de una cinta transportadora**. La banda envuelve esa carcasa, así que el material va apoyado sobre ella hasta el instante mismo del lanzamiento. El campo magnético variable induce **corrientes de Foucault** en las piezas conductoras, que las repele y las lanza hacia adelante; el plástico y el vidrio no reciben empuje, no alcanzan la velocidad de despegue y caen prácticamente bajo el tambor. Una cuchilla divisora ajustable separa según dónde cae cada pieza, y **dos bandejas, cada una sobre una celda de carga**, pesan las dos fracciones.

**Dos fracciones, dos celdas, dos canales de datos:**

- **INERTES** — plástico, vidrio y todo lo que no conduce.
- **NO FERROSOS** — aluminio, cobre y demás metales no ferromagnéticos.

**No se presenta como una máquina que separa basura.** Se presenta como un **experimento que mide** cómo dependen el alcance y la eficiencia de separación de la velocidad del rotor y de la distancia al material.

El banco opera **aguas abajo de la separación ferrosa convencional**: la alimentación no contiene material ferromagnético, igual que en una planta real donde el acero se retira antes. El acero se *pega* al rotor en vez de lanzarse; con él en la alimentación no hay experimento, hay un atasco.

> **La arquitectura cambió en la v3.** La v2 lanzaba desde una plancha fija sobre el rotor y **no podía funcionar**: quedaba un hueco abierto de 46,6 mm entre la banda y la plancha, y sobre la plancha la fricción paraba el inerte en 12,5 mm de los 80 disponibles. Ver `DECISION_ARQUITECTURA.md` y `CAMBIOS_v3.md`.

---

# 2 · Estructura del paquete

```
VORTICE/
├── PARAMETERS/
│   ├── master.yaml              ← FUENTE ÚNICA DE VERDAD NUMÉRICA
│   └── derivados_cad.json         (geometría y trayectorias, las escribe el generador)
├── CAD/
│   ├── STEP/   VORTICE_maquina · _rotor · _guarda
│   ├── STL/    los mismos tres
│   ├── PLANOS/ 3 láminas acotadas (SVG + PNG) y 3 renders
│   └── _legacy/  el paquete v1, archivado
├── CONTEXTO/
│   ├── PROYECTO_COMPLETO.md            ← este documento
│   ├── DECISION_ARQUITECTURA.md          A / B / C cuantificadas, y por qué A
│   ├── CAMBIOS_v3.md                     qué cambió y qué números quedan invalidados
│   ├── CAMBIOS_DESDE_EL_ANTEPROYECTO.md  la razón física de cada cambio
│   ├── DECISIONES_CONFIRMADAS.md         qué se decidió y por qué
│   ├── DECISIONES_PENDIENTES.md          qué falta resolver
│   └── LISTA_DE_MATERIALES.md            qué comprar y cuánto cuesta
├── .claude/skills/
│   ├── vortice-cad/        generar_modelo3d.py · generar_planos.py
│   └── vortice-validation/ verificar.py
└── FIRMWARE/               (vacío — ver P-09)
```

### Cómo se regenera todo

```bash
python .claude/skills/vortice-cad/generar_modelo3d.py   # STEP, STL, renders, derivados
python .claude/skills/vortice-cad/generar_planos.py     # las 3 láminas
python .claude/skills/vortice-validation/verificar.py   # todas las comprobaciones
```

**Ninguna cota vive en un script.** Todas están en `master.yaml`, incluidas las once que la v2 llevaba sueltas en el generador y la que llevaba `generar_planos.py` (que dibujaba la cinta 3,4 mm fuera de sitio respecto del STEP). `generar_planos.py` **no calcula ninguna posición**: lee `derivados_cad.json`, que escribe el generador del modelo 3D, de modo que **las láminas dibujan exactamente la misma trayectoria que verifica `verificar.py`**, punto por punto.

Y `verificar.py` **contrasta toda la sección `montaje` del YAML contra lo que construye el generador**, cota a cota, y falla si algo difiere en más de una micra. En la v2 el YAML decía `x_rodillo_cabeza = 500` y el generador construía 468,4: nadie lo comprobaba.

### Qué abre cada archivo

| Archivo | Para qué | Cómo se abre |
|---|---|---|
| `LAMINA1_alzado.png` | Posiciones longitudinales, alturas y **trayectorias predichas** | Visor de imágenes; imprimir en A3 |
| `LAMINA2_planta.png` | Anchos y posiciones transversales | Ídem |
| `LAMINA3_rotor.png` | Cortes del rotor y del tambor, entrehierro indexado, despiece del imán | Ídem |
| `VORTICE_maquina.step` | Modelo 3D para medir y mecanizar | **FreeCAD** (gratis) o cualquier CAD |
| `VORTICE_rotor.step` | Rotor + tambor + transmisión aislados | Ídem |
| `VORTICE_guarda.step` | La guarda sola, para poder ocultarla | Ídem |
| `master.yaml` | Todas las cifras | Editor de texto |

> **El STEP no lleva cotas escritas** — ningún STEP las lleva. Las cotas van en las tres láminas. El STEP sirve para **medir cualquier distancia que no esté acotada**, abrir secciones y verificar interferencias.

---

# 3 · Física del proyecto

| Concepto | Ecuación | Valor en VÓRTICE 150 |
|---|---|---|
| Faraday | ε = −dΦ_B/dt | Origen de la fem inducida |
| Corrientes de Foucault | J = σE | Corrientes reales en el volumen del metal |
| Lenz | (signo negativo) | Repulsión; lo exige la conservación de la energía |
| Frecuencia de alternancia | f = p·N/60, **p = n_polos/2 = 5 pares de polos** | **116,7 Hz** a 1.400 rpm |
| Paso polar | **λ = π·D_r/p** — el paso de un **par** de polos, un ciclo N‑S completo | π·111,6/5 = **70,12 mm** |
| Decaimiento del **campo** | B(z) ≈ B₀·e^(−2πz/λ) | longitud característica λ/2π = **11,16 mm** |
| Decaimiento de la **fuerza** | F ∝ B² ∝ e^(−4πz/λ) | longitud característica λ/4π = **5,58 mm** |
| Profundidad de piel | δ = √(ρ_e/πfμ₀) | **δ(Al) = 7,82 mm** a 116,7 Hz con ρ_e = 2,82×10⁻⁸ Ω·m |
| Figura de mérito | a ∝ (σ/ρ_m)·B²f | Al **1,313×10⁴** · Cu **6,489×10³** · latón **1,845×10³** m²/(Ω·kg) |
| Despegue en el tambor | cos θ = v²/(g·R) | El inerte no despega en la cima: sale a **θ = 77,95°** |
| Impulso por alcance | v = x·√(g/2h) | Medición con regla |
| Módulo del lema | N = (m/M)·N_A | M(Al) = 26,98 g/mol |

> **Nunca eliminar la definición de p.** Este error concreto ya ocurrió dos veces al recortar el póster: se borró la definición de p y se perdió la distinción entre 11,16 mm y 5,58 mm. `verificar.py` comprueba que este documento la conserva.

### Las dos hipótesis centrales

**H1 — la fuerza depende del cuadrado del campo.** Si `B(z) ≈ B₀e^(−2πz/λ)` y `F ∝ B²`, entonces la fuerza debe decaer con una longitud característica que es **la mitad** de la del campo: λ/4π contra λ/2π.

*Cómo se comprueba:* se mide **B(z)** con la bobina de prueba y **F(z)** por el alcance con una regla, barriendo el entrehierro indexado 4,0 / 5,5 / 7,0 / 8,5 mm. La predicción es `F(z)/F(4,0) = e^(−(z−4,0)/5,58)`, o sea 1,000 / 0,764 / 0,584 / 0,446. Lo que se contrasta es **la caída medida de la fuerza contra el λ/4π que salga del campo medido**.

> **Aviso, y es importante para el criterio 2.** La razón `(λ/2π)/(λ/4π)` vale 2 **por álgebra**, con cualquier D_r y cualquier p. Comprobarla en un script o citarla en un póster **no comprueba nada de física**. La v2 la presentaba como validación de H1; se retiró del documento y del verificador.

**H2 — el aluminio se acelera más que el cobre.** El aluminio conduce **un 39 % menos** que el cobre (61 % IACS contra 100 %), y sin embargo debe lanzarse más lejos, porque lo que manda es **σ/ρ_m** y no σ.

*Cómo se comprueba:* con el lote H2 — probetas de aluminio, cobre y latón de **25 × 25 × 0,5 mm**, es decir **a geometría y espesor controlados**. Predicción: alcance Al > Cu > latón, en el orden de σ/ρ_m. Schloemann (1975) reporta un coeficiente de desviación coherente con esa razón.

> **Declarar siempre "a geometría y espesor controlados"** en toda comparación entre materiales. Si las piezas varían de forma o de grosor, no se sabe si el efecto es del material o de la geometría.

---

# 4 · Parámetros de operación

| Magnitud | Valor | De dónde sale |
|---|---|---|
| **Velocidad de banda** | **0,35 m/s** | Fija el punto de despegue del inerte y el margen a la cuchilla |
| Rango admisible | 0,15 – 0,45 m/s | El motorreductor se pide para 0,45 (143,2 rpm de rodillo) |
| **Velocidad del rotor** | **1.400 rpm** | Rango 1.000–2.000 |
| Frecuencia de alternancia | 116,7 Hz | f = p·N/60 |
| Velocidad de superficie del imán | 8,18 m/s | |
| Velocidad del **tambor** | 57,3 rpm | Gira con la banda, no con el rotor |
| **Entrehierro z** | **4,00 mm** | 0,5 zuncho + 1,0 holgura + 1,0 carcasa + 1,5 banda |
| Entrehierros indexados | 4,0 / 5,5 / 7,0 / 8,5 mm | Manguitos deslizantes de 0 / 1,5 / 3,0 / 4,5 mm de pared |
| **Caudal nominal** | **17,98 g/s = 64,7 kg/h** | σ·ancho·v |
| Piezas por segundo | 20,5 | |
| Masa sobre la banda | 25,7 g en todo momento | No depende de la velocidad |

**Por qué 0,35 m/s.** Ahora hay una razón física, no una preferencia. Para que una pieza se separe de la banda **en la cima** del tambor hace falta `v ≥ √(gR) = 0,766 m/s`. A 0,35 m/s (el 46 %) una pieza **sin empuje magnético** no se separa: sigue la banda hasta `θ = acos(v²/gR) = 77,95°` —o sea casi hasta el costado del tambor— y sale ahí, cayendo prácticamente en vertical. Una pieza **con empuje** supera ese umbral y sale por la cima, en horizontal. **Esa diferencia de comportamiento es la separación**, y se agranda cuanto más lenta va la banda; por debajo se pierde caudal sin ganar nada.

**Abrir el entrehierro es el experimento.** Pasar de 4,0 a 8,5 mm deja la fuerza en **×0,446** — con una longitud de decaimiento de 5,58 mm, la fuerza se divide por dos cada 3,87 mm. Eso es lo que hace medible H1.

**El coste de la arquitectura.** El entrehierro pasó de 3,0 mm (la v2, con plancha) a 4,00 mm (la v3, con carcasa y banda). Son **×0,836, un 16,4 % menos de fuerza**. Se paga a cambio de que el material vaya apoyado hasta el lanzamiento.

---

# 5 · Arquitectura, de la tolva a las bandejas

Posiciones en X desde el eje del rodillo de cola.

| # | Elemento | Posición X | Función |
|---|---|---|---|
| 1 | **Tolva** 4,33 L | 95 | Boca 260×200, **salida 130×40** (10 mm de margen a cada borde de banda), compuerta 0–25, vibrador obligatorio |
| 2 | **Cinta** PVC 150 × 1,5 | 0 … 500 | Rodillo de cola **motriz y tensor** Ø60. Cama de deslizamiento y guías laterales |
| 3 | **Tambor de cabeza** | 500 | **El rotor magnético dentro de una carcasa no conductora Ø116,6.** La banda lo envuelve |
| 4 | **Cuchilla divisora** | 718 | Filo a 40 mm sobre el tejadillo. Ajustable en 6 posiciones de 643 a 743, con las bandejas |
| 5 | **Dos bandejas** sobre 1 celda c/u | 491,5…711,5 y 724,5…1158,5 | Pesan cada fracción. **Nada las toca salvo su celda** |
| 6 | **Deflector acolchado** | 1.090 | Espuma de 50 mm. **Obligatorio**: la lata alcanzaría 1.542 y la bandeja acaba en 1.158 |
| 7 | **Guarda** de policarbonato | 417 … 1.158 | Dos paños. Cubre toda la envolvente del rotor y toda la zona de vuelo |
| 8 | **Bastidor** MDF 1300×500 | −85 … 1.215 | Base + 2 laterales con 2 ventanas cada uno + 4 travesaños |

**Recorrido de asentamiento: 405 mm** de la tolva al tambor. Sin ese recorrido el material llega todavía rebotando y en capas irregulares.

**Extensión real de la máquina: 1.526 mm** (de −31,5 a 1.158,5), sobre una base de 1.300.

---

# 6 · Cotas principales

### Rotor

| Pieza | Cota | Valor |
|---|---|---|
| Tubo | Acero cédula 40 de 3-1/2" · Ø ext / pared / int | **101,6 / 5,74 / 90,12** |
| Tubo | Largo | 200 |
| Imán | Dimensiones · **magnetización a través de los 5 mm** | **60 × 10 × 5** |
| Imán | Cantidad · grado · masa unit. | **60** · N52 · 22,5 g |
| Rotor | Largo activo · Ø en la cara del imán | 180 · **111,6** |
| Rotor | Paso circunferencial · ancho de polo · hueco | 31,92 · 20 · **11,92** |
| Rotor | Paso polar λ · λ/2π · λ/4π | **70,12** · 11,16 · 5,58 |
| Rotor | Factor de llenado α | 0,627 |
| Rotor | Sagita: **pieza de 10** / **POLO real de 20** | 0,247 / **0,994** |
| Tira separadora | 11,3 × 5,0 × 200 · PETG · 10 uds. | |
| Eje | Ø20 h6 · largo 480 · entre chumaceras **340** | UCP204 |
| Cubo | Ø90,07 × 30 · 6 taladros Ø20 en PCD 60 | Ajuste de presión en el ID |
| Zuncho | 0,5 · 2 capas fibra + epóxico | |

> **La sagita del polo no es la del imán.** Las dos piezas de 10 mm de un polo se montan **coplanares**, así que el polo real de 20 mm deja **0,994 mm** de luz en los bordes, no 0,247. Es lo que hay que rellenar de epóxico, y lo que engorda el entrehierro efectivo en el borde del polo.

### Tambor de cabeza

| Pieza | Cota | Valor |
|---|---|---|
| Carcasa | ID / OD / pared / largo | **114,6 / 116,6 / 1,0 / 228** |
| Carcasa | Material | **Laminado de fibra de vidrio y epóxico — NO CONDUCTOR** |
| Discos de extremo | Espesor · material | 12 · PETG impreso |
| Rodamientos | 2 × **6004-2RS** (20 × 42 × 12) | La carcasa rueda libre sobre el eje del rotor |
| Manguitos | Pared 1,5 / 3,0 / 4,5 · PETG deslizante | Indexan el entrehierro |
| Superficie del material | R = OD/2 + espesor de banda | **59,80** |
| Masa del conjunto | | 0,559 kg |

### Masas y verificaciones mecánicas

| Pieza | kg | | Verificación | Resultado |
|---|---|---|---|---|
| Tubo | 2,714 | | Energía a 1.400 rpm | 123 J |
| 60 imanes | 1,350 | | Energía a 2.000 rpm | **251 J** |
| Eje | 1,184 | | Fuerza centrípeta por imán a 2.000 | **52,6 N** |
| 2 cubos | 0,676 | | Tensión en la unión pegada | **0,088 MPa** |
| Tiras | 0,144 | | … contra el **criterio de diseño** (1 MPa) | factor **11×** |
| Zuncho | 0,057 | | … contra la **resistencia del epóxico** (10 MPa) | factor **114×** |
| **ROTOR** | **6,124** | | **Energía de un imán suelto** | **1,54 J** |
| Tambor (no gira con el rotor) | 0,559 | | Flecha del eje (rotor **+ carga de banda**) | **0,044 mm** |
| Inercia del rotor | 0,01146 kg·m² | | Primera velocidad crítica | **4.500 rpm** |
| | | | Trabajo a 2.000 rpm | **44,4 %** de la crítica |

> **Son dos cifras distintas y hay que citarlas por separado.** El **criterio de diseño** del proyecto para la unión pegada es 1 MPa, y da factor 11×. La **resistencia real** del epóxico estructural es del orden de 10 MPa, y da factor 114×. Mezclarlas fue un error de la v1 que ya se corrigió una vez.
>
> **La velocidad crítica bajó de 5.951 a 4.500 rpm** porque la v2 **no contabilizaba** la carga radial que la banda transmite al eje a través de los rodamientos del tambor (39,1 N en y = ±106). Se sigue trabajando muy por debajo del límite del 70 %.

### Cinta, tolva, salida y bastidor

| Elemento | Cotas |
|---|---|
| Banda | 150 ancho · 1,5 esp. · **1.279,0** desarrollada · superficie a 400 sobre la base |
| Rodillo de cola (motriz + tensor) | Ø60 × 170 · entrecentros 500 · 111,4 rpm a 0,35 m/s · **143,2 a 0,45** |
| Tensor | **40 mm** de recorrido — absorbe los 14,7 mm del cambio de manguito |
| Cama / guías | 400×150×3 / 400×3×29,5 |
| Tolva | Boca 260×200 · **salida 130×40** · cono 170 a 64,80° · cuello 30 · **4,33 L** · luz 60 |
| Cuchilla | 3 de espesor · filo 40 sobre el tejadillo · tejadillo 25 · **5 mm de holgura a cada bandeja** |
| Bandejas | 280×214×120 y 280×428×120 interiores · PP corrugado 3 mm sobre marco de aluminio |
| Celdas | **1 monopunto de 2 kg por bandeja** · 1 HX711 cada una · **2 canales de datos** |
| Deflector | Espuma 50 · placa 3 · 270 de ancho · colgado del bastidor, 5 mm al piso y a las paredes |
| Base / laterales | 1300×500×18 / 1300×460×18 · separación interior **300** |
| Guarda | **2 paños de 371 × 330 × 6** policarbonato, de x=417 a x=1.158 |
| Altura total | **678** sin patas (708 desde el suelo) |

### Motor y transmisión

| Elemento | Valor |
|---|---|
| Motor rotor | DC escobillas **24 V / 350 W** · 2.750 rpm · Ø90 × 150 · driver BTS7960 |
| Poleas | 25T / 32T HTD-5M ancho 15 · relación **1,28** · Ø prim. 39,79 / 50,93 |
| Correa | Calculada 502,7 → pedir **HTD-5M de 525** |
| Entrecentros | **180** a 220° del eje del rotor — aleja el motor de los imanes |
| Rotor a fondo | 2.148 rpm · techo de firmware **2.000** |
| Rampa | 0,160 N·m · 33,5 W en 15 s (de 350 W disponibles) |
| Motor de banda | Motorreductor 24 V, **≥ 143,2 rpm**, par ≥ 2 N·m |
| Alimentación | 24 V / 15 A **+ DC-DC a 12 V (vibrador) y a 5 V (lógica)** |

---

# 7 · Salida y trayectorias

> ## Todas las velocidades de salida son PREDICCIONES marcadas `[VERIFICAR]`
>
> `master.yaml` guarda **velocidades de salida**, no alcances; los alcances se derivan de ellas y de la geometría real. Las cuatro velocidades proceden del modelo balístico de la v1, con factores de derrateo **estimados, no medidos** (P‑06), y el empuje de la arquitectura nueva actúa sobre el arco de envolvimiento y no sobre una placa plana: **no hay derivación citable para ninguna**. La cuchilla, las bandejas y el deflector están posicionados **bajo ese supuesto declarado**, y por eso la cuchilla es ajustable. Lo cierra el péndulo (P‑06).

| Objeto | v de salida `[VERIFICAR]` | Dónde cae (x absoluto) | Separación frente al inerte |
|---|---|---|---|
| **Inerte** (referencia) | 0,35 m/s — **sale a 77,95° de la cima** | **574,0 mm** | — |
| Fragmento de 35 mm (**peor caso conductor**) | 1,369 m/s | **861,5 mm** | 287,4 mm |
| Fragmento de 25 mm | 1,842 m/s | **986,3 mm** | 412,2 mm |
| Media lata aplastada | 3,946 m/s | *alcance libre 1.541,9* → **la para el deflector en 1.090** | 967,9 mm |

**Cuchilla en 718 mm → margen de 143,5 mm** al inerte y 143,5 al peor conductor.

Lo único que se puede calcular **sin suponer nada** es el inerte: solo depende de `v_banda` y de la geometría del tambor. Cae en **574,0 mm**.

Caída desde la cima al piso de bandeja: **342 mm**, derivada de la geometría (`z_banda_sup − z_bandeja_piso`), no una cota.

---

# 8 · Seguridad

Cinco reglas, ninguna negociable:

1. **La guarda de policarbonato es obligatoria.** Un imán suelto a 2.000 rpm lleva **1,54 J**, comparable a un perdigón de aire comprimido. La guarda cubre toda abscisa donde exista el rotor y toda la zona de vuelo; `verificar.py` lo comprueba y su posición se **deriva**, no se escribe.
2. **El rotor queda encerrado por su carcasa.** Es una ganancia de la arquitectura v3 y una **segunda** barrera, no un sustituto de la guarda.
3. **La seta corta la alimentación físicamente**, no por software. Si el ESP32 se cuelga con el PWM al 100 %, la seta apaga el rotor igual.
4. **Gafas y guantes de carnaza al manipular imanes.** Se manejan de a uno, con separadores, nunca cerca de la cara. Un N52 de 60×10×5 que se cierra sobre un dedo lo abre.
5. **Se pesa con el motor detenido.** Elimina vibración y ruido eléctrico, que es la causa habitual de lecturas erráticas con celdas de carga.

Además: empezar en 1.000 rpm y no pasar de 2.000 hasta que el rotor esté balanceado (**P‑03**), con el techo programado en firmware.

---

# 9 · Estado de la verificación

`verificar.py` recalcula desde las fórmulas —no copia— cada magnitud derivada, mide sobre los sólidos reales del modelo 3D, contrasta el YAML contra el generador, **recorre el camino del material** y revisa la coherencia de estos documentos.

**Ejecútalo para conocer el resultado.** No hay un recuento escrito aquí a propósito: el propio verificador falla si encuentra uno en cualquier documento, porque un número escrito a mano se queda obsoleto en la siguiente ejecución.

Bloques:

| | Qué mide |
|---|---|
| **A** | Física y mecánica: geometría magnética, tambor y entrehierro, operación, masas e inercia, energía y retención, eje y velocidad crítica, transmisión, cinta y caudal, instrumentación, bastidor y tolva, física de materiales e hipótesis |
| **B** | Geometría medida sobre los sólidos reales: interferencias, encaje, entrehierro, holguras |
| **C** | **Montaje: cada cota del YAML contra lo que construye el generador**, con tolerancia de 1 µm |
| **D1** | **Continuidad del apoyo** — recorre el camino del material y busca tramos sin superficie debajo |
| **D2** | **Fricción y velocidad mínima** — qué soporta el material en cada abscisa, y √(gR) |
| **D3** | **Trayectoria contra sólidos** — 240 puntos por trayectoria contra los 139 sólidos |
| **D4** | **Aislamiento de las bandejas** — nada a menos de 5 mm salvo su celda |
| **D5** | **Apoyo real** — juntas declaradas, área ≥ 100 mm², cadena al suelo |
| **D6** | **Guarda** — ninguna abscisa del rotor expuesta |
| **E** | Coherencia documental: regresiones que ya ocurrieron antes |

Las familias D son nuevas de la v3 y son las que habrían cazado los cinco bloqueantes. De hecho **D3 cazó un error de signo en la balística nueva** durante esta misma sesión: ver `CAMBIOS_v3.md` §6.

---

# 10 · Lo que falta

Resumen de `DECISIONES_PENDIENTES.md`, por urgencia:

| # | Pendiente | Bloquea |
|---|---|---|
| **P-01** | **Presupuesto**: ≈ 3,40 M COP contra un techo de 1,00 M (y el anteproyecto decía 0,50 M) | **toda la compra** |
| **P-02** | Confirmar por escrito la **magnetización a través de los 5 mm** | el pedido de imanes |
| **P-03** | Taller de balanceo dinámico para 6,12 kg y Ø111,6 | pasar de 1.400 rpm |
| **P-04** | Medir `D_r` real tras el zunchado y **recalcular λ** | validez de las predicciones |
| **P-05** | **Laminar la carcasa y los manguitos** y medir su espesor real | el entrehierro y todo H1 |
| **P-06** | Medir las **velocidades de salida** con el péndulo | fiarse de la posición de la cuchilla |
| **P-07** | Medir la **resolución** y el **error de esquina** de las celdas | los resultados D y E |
| **P-08** | Curva par-velocidad del motor adquirido | confirmar las poleas |
| **P-09** | Páginas de Schloemann, precio de chatarra local | la documentación |
| **P-10** | **FIRMWARE está vacío** | la instrumentación entera |
| **P-11** | **Logística**: cómo entra la máquina al Coliseo el 30 de octubre | el montaje |

---

# 11 · Reglas de redacción del proyecto

Se violaron antes y costaron correcciones. Cualquier documento del proyecto debe respetarlas.

1. **Ningún resultado propio como hecho consumado.** El proyecto no tiene mediciones todavía. Todo se escribe como predicción.
2. **Ningún número sin fuente citable o sin marca `[VERIFICAR]`.**
3. **Nunca eliminar la definición de un símbolo para que el texto quepa.** En particular la de **p**, que ya se perdió dos veces.
4. **Declarar "a geometría y espesor controlados"** en toda comparación entre materiales.
5. **Evitar absolutos innecesarios.** "La conservación de la energía exige el signo negativo" es más sólido que "se aceleraría sin límite".
6. **No presentar identidades algebraicas como validación física.** Que (λ/2π)/(λ/4π) valga 2 no comprueba nada.
7. **Ningún recuento de comprobaciones escrito a mano.** Se ejecuta el verificador.
8. **El texto no debe parecer generado por IA:** debe incluir decisiones que solo el equipo pudo tomar, fracasos concretos y números medidos.

---

## Referencias

- Schloemann, E. (1975). *Separation of nonmagnetic metals from solid waste by permanent magnets. I. Theory / II. Experiments on circular disks*. **J. Appl. Phys. 46**(11).
- Smith, Y. R., Nagel, J. R. y Rajamani, R. K. (2019). *Eddy current separation for recovery of non-ferrous metallic particles: A comprehensive review*. **Minerals Engineering 133**, 149–159.
- Lungu, M. y Schlett, Z. (2001). *Vertical drum eddy-current separator with permanent magnets*. **Int. J. Mineral Processing 63**(4), 207–216.
- Hader, A. *et al.* (2024). *Experimental and numerical analysis of the magnetic force applied to aluminum particles in an Eddy current separator*. **Int. J. Plasma Environ. Sci. Technol. 18**, e03003.
- DANE (2025). *Cuenta Ambiental y Económica de Flujos de Materiales de Residuos Sólidos 2022–2023p*. Tasa de reciclaje 10,51 % en 2023.
- International Aluminium Institute (2024). Producción primaria 186 GJ/t frente a 8,3 GJ/t por refundición.
- Radial Magnet Inc. — regla de dimensionado del yugo por flujo medio-polo.
- CRC Handbook of Chemistry and Physics / ASM Metals Handbook — ρ_e y ρ_m de Al 1050, Cu ETP y latón CuZn37. **[VERIFICAR]** las páginas exactas (P‑09).
- Young y Freedman, *Física Universitaria Vol. 2*; Griffiths, *Introduction to Electrodynamics*.
