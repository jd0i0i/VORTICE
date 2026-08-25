# VÓRTICE 150 — Lista de materiales

*Todas las cantidades salen de `PARAMETERS/master.yaml` v3.*
*Actualizado: 24/08/2026*

---

## Cómo leer esta lista

- **Nombre de búsqueda** — literalmente lo que hay que escribir en MercadoLibre, Amazon o pedir en el mostrador de la ferretería.
- **Precio** — **ESTIMACIÓN, no cotización.** Referencia Colombia, agosto 2026, a **1 USD = 4.100 COP**. Verificar todo antes de comprar.
- **Prioridad** — `CRÍTICO` = sin esto no hay máquina · `IMPORTANTE` = sin esto la máquina funciona peor o es menos segura · `OPCIONAL` = mejora, no bloquea.
- **[v3]** — partida nueva o modificada respecto de la lista anterior. Ver `CAMBIOS_v3.md`.

> ### ⚠ Aviso de presupuesto, léelo antes de comprar
> El total estimado es **≈ 3.401.000 COP (≈ 830 USD)**.
> **El anteproyecto entregado fija un límite de 1.000.000 COP** *(y el propio anteproyecto decía 500.000 — las dos cifras circulan y hay que resolver cuál rige)*.
> **Esta máquina no cabe en ninguno de los dos techos, y no hay combinación de recortes que la meta.** Ver §«El techo y la máquina son incompatibles» al final.
> Es la decisión **P‑01** y hay que resolverla **antes de comprar nada**.

---

## A · Rotor y tambor de cabeza

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| A1 | `tubo acero cédula 40 3-1/2 pulgadas` | Ø ext 101,6 · pared 5,74 · largo 250 (se corta a 200) | 1 | Yugo magnético y cuerpo del rotor | 45.000 | 11 | CRÍTICO |
| A2 | `imán neodimio N52 bloque 60x10x5 mm` | **N52 · magnetizado a través de los 5 mm** · Br 1,43–1,48 T | **60** | Generan el campo alternado | **780.000** | **190** | CRÍTICO |
| A3 | `eje acero rectificado 20 mm h6` | Ø20 h6 · largo 500 (se corta a 480) | 1 | Eje del rotor **y** del tambor | 35.000 | 9 | CRÍTICO |
| A4 | `chumacera UCP204 20mm` | Soporte de pie · eje Ø20 · H 33,3 | 2 | Soportan el rotor, span 340 | 44.000 | 11 | CRÍTICO |
| A5 | `polea HTD 5M 25 dientes ancho 15` | Ø prim. 39,79 | 1 | Polea motriz | 38.000 | 9 | CRÍTICO |
| A6 | `polea HTD 5M 32 dientes ancho 15` | Ø prim. 50,93 · buje Ø20 | 1 | Polea conducida | 45.000 | 11 | CRÍTICO |
| A7 | `correa dentada HTD 5M 525 ancho 15` | Largo calculado 502,67 → comercial **525** | 2 | Transmisión motor→rotor (1 repuesto) | 32.000 | 8 | CRÍTICO |
| A8 | `mecanizado torno aluminio` | 2 cubos Ø90,07 × 30, 6 taladros Ø20 en PCD 60 | 2 | Cierran el tubo y fijan el eje | 120.000 | 29 | CRÍTICO |
| A9 | `filamento PETG 1.75mm 1kg` **[v3]** | 10 tiras + **2 discos de tambor** + **3 manguitos** de 228 mm | **2** | Retención entre polos y piezas del tambor | **190.000** | 46 | CRÍTICO |
| A10 | `epóxico estructural dos componentes` | Tipo Sikadur / JB Weld · 500 g | 1 | Pega imanes, satura zuncho **y carcasa** | 55.000 | 13 | CRÍTICO |
| A11 | `cinta fibra de vidrio 50mm` | Rollo 25 m · zuncho del rotor **y laminado de la carcasa** | 1 | Retención + carcasa del tambor | 38.000 | 9 | CRÍTICO |
| A12 | `rodamiento 6004 2RS` **[v3]** | 20 × 42 × 12 | **2** | **La carcasa rueda libre sobre el eje del rotor** | 24.000 | 6 | CRÍTICO |
| A13 | `tubo PVC 110 + cera desmoldante` **[v3]** | Mandril para laminar la carcasa y los manguitos | 1 | Molde, no va en la máquina | 25.000 | 6 | CRÍTICO |
| | | | | **Subtotal A** | **1.471.000** | **359** | |

> **A2 es la partida que decide el proyecto.** Confirmar el eje de magnetización por escrito (P‑02) y cotizar en tres sitios (P‑01).
> **A12 y A13 son la arquitectura nueva.** La carcasa se lamina con la misma fibra y el mismo epóxico del zuncho: **no añade material**, solo el mandril. Ver `DECISION_ARQUITECTURA.md`.
> **La carcasa DEBE ser no conductora.** Si se sustituye por un tubo de aluminio se convierte en una espira en cortocircuito girando en el campo: se calienta y frena el rotor.

---

## B · Cinta transportadora

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| B1 | `banda transportadora PVC lisa 2mm` **[v3]** | Ancho 150 · largo desarrollado **1.279** · sin tacos · con unión | 1 | Transporta y **envuelve el tambor** | 95.000 | 23 | CRÍTICO |
| B2 | `rodillo transportador 60mm con eje` **[v3]** | Ø60 × 170 · eje pasante. **Solo el de cola** | **1** | Rodillo motriz y tensor | 70.000 | 17 | CRÍTICO |
| B3 | `motorreductor 24V DC 150 rpm` **[v3]** | 24 V · **≥ 143,2 rpm** · par ≥ 2 N·m · con PWM | 1 | Mueve la banda de 0,15 a 0,45 m/s | 155.000 | 38 | CRÍTICO |
| B4 | `perfil aluminio plano 25x3` | 2 guías de 400 × 3 × 29,5 | 1 | Guías laterales, apoyadas en la cama | 25.000 | 6 | IMPORTANTE |
| B5 | `lámina acrílico 3mm` | Cama de deslizamiento 400 × 150 × 3 | 1 | Impide que el ramal superior se hunda | 20.000 | 5 | IMPORTANTE |
| B6 | `tornillo tensor M8 + ranura` **[v3]** | Recorrido **40 mm** (±20) en el rodillo de cola | 1 | Tensa la banda **y absorbe el cambio de manguito** (14,69 mm) | 18.000 | 4 | IMPORTANTE |
| | | | | **Subtotal B** | **383.000** | **93** | |

> **B2: un rodillo, no dos.** El rotor es el tambor de cabeza. Se ahorran 60.000 COP.
> **B3: 100 rpm no alcanzaba.** El rodillo necesita **111,4 rpm** para 0,35 m/s y **143,2** para el `v_banda_max` de 0,45 que el proyecto declara admisible.

---

## C · Bastidor y estructura

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| C1 | `MDF 18mm lámina` **[v3]** | 1,53 × 2,44 m. Base (1300×500), 2 laterales (1300×460), travesaños, pórticos, pedestales | 1 | Toda la estructura | 95.000 | 23 | CRÍTICO |
| C2 | `pata de caucho 40mm` | Ø40 × 30 | 4 | Aíslan vibración | 12.000 | 3 | IMPORTANTE |
| C3 | `tornillería madera + escuadras` | Tirafondos 4×40, escuadras 40×40, insertos M6 | 1 lote | Ensamble del bastidor | 55.000 | 13 | CRÍTICO |
| C4 | `platina aluminio 10mm mecanizada` **[v3]** | 2 subplacas **240 × 131 × 10**, taladros para UCP204 | 2 | Alojan las chumaceras sobre las galgas | 110.000 | 27 | CRÍTICO |
| C5 | `lámina policarbonato 6mm` **[v3]** | **2 paños de 371 × 330 × 6** | 1 | **Guarda sobre el rotor y la zona de vuelo** | 125.000 | 30 | **CRÍTICO** |
| | | | | **Subtotal C** | **397.000** | **97** | |

> **C5 no es opcional.** Un imán suelto a 2.000 rpm lleva **1,54 J**, comparable a un perdigón de aire comprimido. En la v3 el rotor queda además **encerrado por la carcasa**, pero eso es una segunda barrera, no un sustituto.
> Dos paños en vez de uno para poder abrir solo la mitad y llegar a las bandejas sin destapar el rotor.

---

## D · Electrónica y control

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| D1 | `ESP32 DevKit V1` | 30 pines | **2** | Controlador (1 repuesto: punto único de falla) | 70.000 | 17 | CRÍTICO |
| D2 | `driver motor BTS7960 43A` | Puente H 43 A | 2 | Uno para el rotor, otro para la cinta | 76.000 | 19 | CRÍTICO |
| D3 | `encoder óptico de ranura LM393` | Herradura + disco ranurado | 1 | Mide rpm reales del rotor | 15.000 | 4 | CRÍTICO |
| D4 | `módulo HX711` | 24 bit | **2** | **Uno por celda: dos canales de datos** | 24.000 | 6 | CRÍTICO |
| D5 | `fuente conmutada 24V 15A 360W` | 24 V / 15 A | 1 | Alimenta ambos motores | 135.000 | 33 | CRÍTICO |
| D6 | `pulsador seta emergencia + contactor 24V` | Enclavamiento, NC · **corte físico** | 1 | Seguridad — no pasa por software | 65.000 | 16 | **CRÍTICO** |
| D7 | `cable + bornera + caja 200x150x80` | Calibre 14 AWG para potencia | 1 lote | Cableado y caja de control | 70.000 | 17 | CRÍTICO |
| D8 | `convertidor DC-DC 24V a 12V 2A` **[v3]** | Buck, aislado o no | 1 | **Vibrador de tolva (12 V)** | 15.000 | 4 | CRÍTICO |
| D9 | `convertidor DC-DC 24V a 5V 3A` **[v3]** | Buck | 1 | **ESP32, HX711, encoder, sensores** | 20.000 | 5 | CRÍTICO |
| | | | | **Subtotal D** | **490.000** | **120** | |

> **D8 y D9: la lista anterior no los tenía.** Había una sola fuente de 24 V, un vibrador de 12 V y lógica de 5 V / 3,3 V. Sin conversión, la máquina no arranca.
> **D6: el corte es físico.** Si el ESP32 se cuelga con el PWM al 100 %, la seta tiene que apagar el rotor igual.

---

## E · Tolva, cuchilla, bandejas y celdas

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| E1 | `polipropileno corrugado 3mm` + `ángulo aluminio 15x15x1.5` **[v3]** | Bandejas de 280×214×120 y 280×428×120 interiores, sobre marco de aluminio | 2 | Reciben cada fracción | 55.000 | 13 | CRÍTICO |
| E2 | `celda de carga 2kg monopunto` **[v3]** | 2 kg · monopunto (parallelogram) · 4 hilos | **2** | **Una por bandeja. Dos canales de datos** | 44.000 | 11 | CRÍTICO |
| E3 | `lámina acrílico 3mm` (tolva) **[v3]** | Boca 260×200 · **salida 130×40** · cono 170 · cuello 30 · **4,33 L** | 1 | Depósito de alimentación | 45.000 | 11 | CRÍTICO |
| E4 | `platina aluminio 3mm` **[v3]** | Cuchilla 40 mm de filo + tejadillo 25 + 2 montantes | 1 | Divide la trayectoria | 30.000 | 7 | CRÍTICO |
| E5 | `guillotina + escala grabada` | Apertura 0–25 mm | 1 | Regula el caudal de la tolva | 25.000 | 6 | IMPORTANTE |
| E6 | `motor vibrador 12V DC` | 12 V · 0,4 A | 1 | **Obligatorio: la tolva se arquea sin él** | 28.000 | 7 | CRÍTICO |
| E7 | `espuma de embalaje 50mm` + `platina 3mm` **[v3]** | Deflector 270 mm de ancho, colgado del bastidor | 1 | **Retén de la media lata** | 20.000 | 5 | CRÍTICO |
| | | | | **Subtotal E** | **247.000** | **60** | |

> ### Por qué las celdas bajan de 8 × 5 kg a 2 × 2 kg
> La lista anterior ponía **20 kg de fondo de escala por bandeja** para medir **83,7 g de aluminio por lote**, con una tara de bandeja de **2,36 kg** en acrílico de 4 mm. Con la resolución declarada de 5 g eso da una **cuantización del 5,97 %** antes de ruido y deriva: los resultados D y E habrían salido dominados por el instrumento.
>
> La v3 aligera las bandejas (polipropileno corrugado sobre marco de aluminio: **0,36 y 0,55 kg**) y usa **una celda monopunto de 2 kg por bandeja**. La cuantización baja al **1,19 %** y el ahorro es de 76.000 COP.
>
> **Dos advertencias, las dos marcadas `[VERIFICAR]` en el YAML:**
> - La **resolución de 1 g es un objetivo de diseño, no un dato**. No es FS/2²⁴: la fija el piso de ruido mecánico y eléctrico. Se mide antes de fiarse: masa patrón de 10 g, 20 repeticiones, motor detenido, y se reporta la desviación típica.
> - Una celda monopunto bajo una plataforma de **434 × 280 mm** está por encima del tamaño para el que se compensa el momento. **Se mide el error de esquina**: 100 g en el centro y en las cuatro esquinas. Si la dispersión supera el 2 %, la corrección son **dos celdas en paralelo por bandeja** — cuatro en total, pero **siguen siendo dos canales de datos**.

---

## F · Pegado, retención y acabado

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| F1 | `cianoacrilato gel + activador` | 20 g | 1 | Fijación rápida | 20.000 | 5 | IMPORTANTE |
| F2 | `silicona transparente` | Cartucho | 1 | Sella uniones de tolva y bandejas | 15.000 | 4 | IMPORTANTE |
| F3 | `cinta doble faz espuma 3M` | 19 mm × 5 m | 1 | Montaje de electrónica | 10.000 | 2 | OPCIONAL |
| F4 | `sellador + pintura para MDF` | Base + acabado | 1 lote | **El MDF sin sellar se hincha con la humedad del Caribe** | 55.000 | 13 | IMPORTANTE |
| | | | | **Subtotal F** | **100.000** | **24** | |

---

## G · Seguridad y EPP

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| G1 | `gafas de seguridad policarbonato` | Norma ANSI Z87 | 4 | **Una por integrante**, obligatorias al manipular imanes | 40.000 | 10 | **CRÍTICO** |
| G2 | `guantes de carnaza` | Talla L | 2 pares | Los N52 de este tamaño pellizcan de verdad | 36.000 | 9 | **CRÍTICO** |
| | | | | **Subtotal G** | **76.000** | **19** | |

> Los imanes se manipulan **de a uno**, con separadores, y nunca cerca de la cara. Un N52 de 60×10×5 que se cierra sobre un dedo lo abre.

---

## H · Muestras de ensayo e instrumentos de medida

El lote patrón está **definido pieza por pieza** para que sea reproducible. Total **290 piezas / 254,9 g**, con **32,8 % de aluminio**.

| Material | Piezas | Tamaño (mm) | Masa unit. | Masa total | De dónde sale |
|---|---|---|---|---|---|
| Al de lata (pared) | 120 | 25 × 25 × 0,10 | 0,170 g | 20,4 g | Latas de bebida cortadas |
| Al de perfil / bandeja | 25 | 25 × 25 × 1,50 | 2,531 g | 63,3 g | Retal de perfil o bandeja de horno |
| PET de botella | 90 | 25 × 25 × 0,35 | 0,302 g | 27,2 g | Botellas cortadas |
| HDPE (tapas) | 30 | 28 × 28 × 1,20 | 0,894 g | 26,8 g | Tapas de garrafa |
| Vidrio 3 mm, **cantos matados** | 25 | 25 × 25 × 3,00 | 4,688 g | 117,2 g | Retal de vidriería |
| **TOTAL** | **290** | | | **254,9 g** | |

### Lote H2 — **a geometría y espesor controlados** **[v3]**

Sin esto, la hipótesis 2 no es medible: hace falta comparar metales **con la misma forma y el mismo espesor**, o no se sabe si el efecto es del material o de la pieza.

| Material | Piezas | Tamaño (mm) | Masa unit. | σ/ρ_m (m²/Ω·kg) |
|---|---|---|---|---|
| Aluminio 1050 | 10 | 25 × 25 × 0,50 | 0,844 g | **1,313 × 10⁴** |
| Cobre ETP | 10 | 25 × 25 × 0,50 | 2,800 g | 6,489 × 10³ |
| Latón CuZn37 | 10 | 25 × 25 × 0,50 | 2,647 g | 1,845 × 10³ |

**Predicción de H2:** alcance Al > Cu > latón, en el orden de σ/ρ_m — **pese a que el aluminio conduce un 39 % menos que el cobre** (61 % IACS contra 100 %).

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| H1 | Material recuperado | Latas, PET, HDPE, vidrio | 1 lote | Lote patrón | 0 | 0 | CRÍTICO |
| H2 | `cizalla de mano / tijera para lámina` | Para cortar a 25 mm | 1 | Preparar los lotes | 45.000 | 11 | CRÍTICO |
| H3 | `calibrador digital 150mm` | Resolución 0,01 mm | 1 | **Medir `D_r` tras el zunchado (P‑04)** y verificar los lotes | 55.000 | 13 | CRÍTICO |
| H4 | `alambre esmaltado AWG32 + carrete` **[v3]** | Bobina de prueba, 200 esp. sobre Ø10 | 1 | **Medir B(z) — sin esto H1 no es medible** | 25.000 | 6 | **CRÍTICO** |
| H5 | `sensor efecto hall lineal SS49E` **[v3]** | Salida analógica, ±0,1 T | 3 | Contraste estático del campo y verificación de polaridad antes de pegar | 12.000 | 3 | CRÍTICO |
| H6 | `lámina de cobre 0.5mm` **[v3]** | Para 10 probetas de 25×25 | 1 | **Probetas de H2** | 35.000 | 9 | CRÍTICO |
| H7 | `lámina de latón 0.5mm` **[v3]** | Para 10 probetas de 25×25 | 1 | **Probetas de H2** | 30.000 | 7 | CRÍTICO |
| | | | | **Subtotal H** | **202.000** | **49** | |

> **H4 y H5 cierran un agujero de la lista anterior**: el documento del proyecto decía *"se mide el campo con una bobina de prueba"* y esa bobina **no estaba en la lista de compras**. H1 no era medible con lo que se iba a comprar.
> **H6 y H7 recuperan algo que el anteproyecto ya tenía** y que la versión anterior había perdido: sin cobre y latón, H2 tampoco era medible.

---

## I · Módulo didáctico **[v3 — recuperado del anteproyecto]**

| # | Nombre de búsqueda | Especificación | Cant. | Función | COP | USD | Prior. |
|---|---|---|---|---|---|---|---|
| I1 | `tubo de cobre 22mm` + `imán neodimio Ø15` + discos de aluminio | Un disco macizo y uno ranurado | 1 lote | **Demostración manual**: caída frenada en el tubo, y núcleo macizo contra laminado | 35.000 | 9 | IMPORTANTE |
| | | | | **Subtotal I** | **35.000** | **9** | |

> Estaba en el anteproyecto y se había perdido. Es el **gancho de interacción manual** del stand y la demostración física del porqué de las corrientes de Foucault, sin encender la máquina. Es lo que premia el criterio 1.

---

## Resumen de costos

| Sección | Contenido | COP | USD | % |
|---|---|---|---|---|
| **A** | Rotor y tambor de cabeza | **1.471.000** | 359 | **43,3 %** |
| **B** | Cinta transportadora | 383.000 | 93 | 11,3 % |
| **C** | Bastidor y estructura | 397.000 | 97 | 11,7 % |
| **D** | Electrónica y control | 490.000 | 120 | 14,4 % |
| **E** | Tolva, cuchilla, bandejas y celdas | 247.000 | 60 | 7,3 % |
| **F** | Pegado, retención y acabado | 100.000 | 24 | 2,9 % |
| **G** | Seguridad y EPP | 76.000 | 19 | 2,2 % |
| **H** | Muestras e instrumentos de medida | 202.000 | 49 | 5,9 % |
| **I** | Módulo didáctico | 35.000 | 9 | 1,0 % |
| | **TOTAL** | **3.401.000** | **830** | 100 % |

Diferencia respecto de la lista anterior: **+190.000 COP**. De esos, **+144.000 son la arquitectura nueva** (rodamientos, mandril, filamento del tambor, guarda mayor, banda más larga, motorreductor correcto, menos un rodillo) y el resto son los instrumentos y probetas que faltaban, menos el ahorro de celdas y bandejas.

---

## El techo y la máquina VÓRTICE 150 son incompatibles

**Esta sección sustituye a la antigua «Si hay que caber en 1.000.000 COP», que prometía algo que no cumplía.**

| | COP |
|---|---|
| Techo citado en la documentación del proyecto | 1.000.000 |
| Techo que dice el **anteproyecto entregado** (*"~15.000 de margen sobre el límite de 500.000"*) | 500.000 |
| Estimación de esta lista | **3.401.000** |

**Solo los imanes (A2) valen el 78 % del techo de 1.000.000 y el 156 % del de 500.000.**

### Todas las palancas de recorte, sumadas

| Recorte | Ahorro | Qué se pierde |
|---|---|---|
| 1 fila de imanes en vez de 3 (20 uds.) | 520.000 | Largo activo 180 → 60 mm. Deja de aprovechar la banda de 150 y pasa a ser una prueba de concepto |
| Bandejas y bastidor en material recuperado | 60.000 | Acabado — y el criterio 1 del jurado es presentación estética |
| Un solo ESP32, sin repuesto | 35.000 | Punto único de falla el día de la feria |
| Módulo didáctico | 35.000 | El gancho de interacción manual del stand |
| Probetas de H2 donadas o prestadas | 65.000 | Nada, si aparecen. **H2 no es negociable** |
| Sin repuesto de correa | 16.000 | Punto único de falla |

> **Ojo con la aritmética.** Las dos palancas de imanes de la lista anterior (bajar a 2 filas, 260.000 · bajar a 1 fila, 520.000) **son excluyentes**: la segunda ya contiene la primera. Sumarlas era el error que hacía parecer que la tabla llegaba al techo.

**Ahorro máximo real: 731.000 COP → suelo de 2.670.000 COP.**

$$\textbf{2,67 veces el techo de 1.000.000. \quad 5,34 veces el de 500.000.}$$

Y ese suelo ya es una máquina **mutilada**: sin repuestos, sin módulo didáctico, con un tercio del largo activo y con acabado de material recuperado.

### La decisión que hay que tomar (P‑01)

No es un problema de recortes. **Hay que decidir explícitamente cuál de los dos cambia**, y solo hay tres salidas honestas:

1. **Sube el techo.** VÓRTICE 150 se construye tal cual. Requiere financiación adicional o patrocinio; hay que pedirla ya, no en octubre.
2. **Cambia la máquina.** Se vuelve a una escala tipo anteproyecto —rotor pequeño, menos imanes, sin cinta— y se acepta perder la velocidad de banda como variable experimental. **Entonces hay que rehacer el paquete entero**, no recortar este.
3. **Se construye por fases y solo se compra lo que se financia.** Fase 1 (≈ 15 %): unos pocos imanes, el tubo, epóxico y EPP, para comprobar que un imán pegado aguanta y que hay repulsión medible. Es lo que decide si el proyecto sigue.

**Regla que no se toca:** no se gasta el presupuesto completo antes de validar el rotor.

**Orden recomendado de compra**

1. **Fase 1 — prueba de concepto (≈ 15 %).** Unos pocos imanes, el tubo, epóxico, EPP, sonda Hall.
2. **Fase 2 — rotor y tambor completos.** El resto de imanes, eje, chumaceras, carcasa, rodamientos, transmisión, balanceo.
3. **Fase 3 — máquina.** Cinta, bastidor, electrónica, bandejas, guarda, instrumentos.
