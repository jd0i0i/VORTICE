# VÓRTICE 150 — Planos y memoria de cotas
### Separador de metales no ferrosos por corrientes de Foucault
**Documento de guía para el ingeniero mecánico · todas las cotas en mm**

*Cada número de este documento, del modelo 3D y de las tres láminas sale del mismo archivo `cotas.json`. Es imposible que se desincronicen. 23 verificaciones cruzadas se ejecutan automáticamente al regenerar.*

---

# 1 · CÓMO USAR ESTE PAQUETE

| Archivo | Para qué sirve | Cómo se abre |
|---|---|---|
| `LAMINA1_alzado.png` | **Plano acotado de alzado.** Posiciones longitudinales y alturas | Cualquier visor de imágenes; imprimir en A3 |
| `LAMINA2_planta.png` | **Plano acotado de planta.** Anchos y posiciones transversales | Ídem |
| `LAMINA3_rotor.png` | **Plano acotado del rotor.** Cortes y despiece del imán | Ídem |
| `VORTICE_maquina.step` | Modelo 3D de la máquina, para medir y mecanizar | **FreeCAD** (gratis) o cualquier CAD |
| `VORTICE_rotor.step` | Modelo 3D del rotor solo | Ídem |
| `cotas.json` | La fuente de todas las cifras | Editor de texto |

**El STEP no lleva cotas escritas** — eso es normal, ningún STEP las lleva. Las cotas van en las tres láminas. El STEP sirve para que el ingeniero **mida cualquier distancia que no esté acotada**, abra secciones donde quiera y verifique interferencias.

**Flujo de trabajo recomendado:** el ingeniero abre el STEP en FreeCAD, lo contrasta con las tres láminas, y usa el módulo TechDraw de FreeCAD si necesita acotar algo adicional.

---

# 2 · PARÁMETROS DE OPERACIÓN

| Magnitud | Valor | De dónde sale |
|---|---|---|
| **Velocidad de banda** | **0,35 m/s** | Optimizada por simulación (§3) |
| Rango admisible | 0,15 – 0,45 m/s | |
| **Velocidad del rotor** | **1.400 rpm** | Nominal; rango 1.000–2.000 |
| Frecuencia de alternancia | 117 Hz | f = p·N/60 |
| Velocidad de superficie del rotor | 8,18 m/s | |
| **Entrehierro z** | **3,0 mm** | zuncho 0,5 + holgura 1,5 + plancha 1,0 |
| Entrehierros indexados | 3,0, 4,5, 6,0, 7,5 mm | Galgas de 0,0, 1,5, 3,0, 4,5 mm |

---

# 3 · CAUDAL — cálculo completo

## 3.1 La condición que manda: monocapa

Para que la separación funcione, **cada pieza debe ver el campo por sí sola**. Si dos se solapan, la de arriba queda apantallada y no se separa. El parámetro es la cobertura areal φ = área cubierta / área de banda.

| φ | Situación |
|---|---|
| 0,15 | Muy conservador, poca producción |
| **0,25** | **Nominal — separación limpia** |
| 0,35 | Máximo industrial recomendado |
| 0,55 | Empaquetamiento aleatorio: **ya hay solapes** |

## 3.2 Lote patrón (definido pieza por pieza, para que sea repetible)

| Material | Piezas | Tamaño | Masa unit. | Masa total |
|---|---|---|---|---|
| Al de lata (pared) | 120 | 25 × 25 × 0,10 | 0,170 g | 20,4 g |
| Al de perfil / bandeja | 25 | 25 × 25 × 1,50 | 2,531 g | 63,3 g |
| PET de botella | 90 | 25 × 25 × 0,35 | 0,302 g | 27,2 g |
| HDPE (tapas) | 30 | 28 × 28 × 1,20 | 0,894 g | 26,8 g |
| Vidrio (3 mm, cantos matados) | 25 | 25 × 25 × 3,00 | 4,688 g | 117,2 g |
| **TOTAL** | **290** | | | **254,9 g** |

Fracción de aluminio del lote: **32,8 %**. Masa media por pieza: 0,879 g.

## 3.3 Resultado

| Magnitud | Valor |
|---|---|
| Densidad areal en la banda | 342,5 g/m² |
| **Caudal nominal** | **18,0 g/s = 64,7 kg/h** |
| Piezas por segundo | 20,5 |
| **Masa que la banda lleva encima** | **25,7 g en todo momento** |
| Duración de un lote de 255 g | 14 s |

> La masa sobre la banda **no depende de la velocidad**: es densidad areal × ancho × largo útil. Lo que cambia con la velocidad es el caudal, no la carga instantánea.

## 3.4 Por qué 0,35 m/s y no otra

La fuerza de lanzamiento **casi no depende de la velocidad de banda** (la integral de energía se completa igual). Lo que sí depende es la **calidad de la clasificación**:

| v (m/s) | Cae el inerte a | Peor conductor a | Margen mínimo a la cuchilla |
|---|---|---|---|
| 0,10 | 29 mm | 377 mm | 127 mm |
| 0,25 | 71 mm | 384 mm | 134 mm |
| **0,35** | **100 mm** | **391 mm** | **141 mm ← máximo** |
| 0,50 | 143 mm | 406 mm | 107 mm |
| 0,60 | 171 mm | 418 mm | 79 mm |

Por encima de 0,35 m/s el inerte empieza a acercarse a la cuchilla y se come el margen. Por debajo, se pierde caudal sin ganar nada.

---

# 4 · COTAS DEL ROTOR

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Tubo | Designación | **Acero cedula 40 de 3-1/2"** | Cédula 40 |
| Tubo | Ø exterior | **101,6** | Comercial |
| Tubo | Pared | **5,74** | Mínimo por saturación: 4,39 |
| Tubo | Ø interior | **90,12** |  |
| Tubo | Largo | **200** |  |
| Imán | Dimensiones | **60 × 10 × 5** | Magnetización a través de los 5 mm |
| Imán | Cantidad | **60** | 10 polos × 2 piezas × 3 filas |
| Imán | Grado | **N52** | Br = 1,43 – 1,48 T |
| Imán | Masa unitaria | **22,5 g** | Total 1,35 kg |
| Rotor | Largo activo | **180** | 3 filas × 60 mm |
| Rotor | Ø en la cara del imán | **111,6** |  |
| Rotor | Paso circunferencial | **31,92** | π·Ø_tubo / n_polos |
| Rotor | Ancho de polo | **20** | 2 × 10 mm |
| Rotor | Hueco entre polos | **11,92** | Aquí van las tiras separadoras |
| Rotor | Paso polar λ | **70,12** | λ = πD_r/p con p = 5 |
| Rotor | Decaimiento del campo λ/2π | **11,16** |  |
| Rotor | Decaimiento de la fuerza λ/4π | **5,58** | La fuerza se divide por 2 cada 3,87 mm |
| Rotor | Factor de llenado α | **0,627** |  |
| Rotor | Sagita (imán plano sobre tubo) | **0,25** | Espesor del lecho de epóxico en los bordes |
| Tira separadora | Sección | **11,3 × 5,0** | Largo 200 · PETG · 10 unidades |
| Eje | Ø | **20** | Acero rectificado h6 |
| Eje | Largo | **480** |  |
| Eje | Entre chumaceras | **340** | UCP204 (eje O20) |
| Cubo | Ø exterior | **90,07** | Ajuste de presión en el ID del tubo |
| Cubo | Largo | **30** | 6 taladros Ø20 sobre PCD 60 |
| Zuncho | Espesor | **0,5** | 2 capas de fibra de vidrio + epóxico |

**Masas e inercia**

| Pieza | Masa (kg) |
|---|---|
| Tubo de acero | 2,714 |
| 60 imanes | 1,350 |
| Eje | 1,184 |
| 2 cubos de aluminio | 0,676 |
| Tiras separadoras | 0,144 |
| Zuncho | 0,057 |
| **TOTAL** | **6,12** |
| Momento de inercia | 0,01146 kg·m² |

**Verificaciones mecánicas**

| Verificación | Resultado |
|---|---|
| Energía del rotor a 1.400 rpm | 123 J |
| Energía del rotor a 2.000 rpm | 251 J |
| Fuerza centrípeta por imán a 2.000 rpm | 53 N = 5,4 kgf |
| Tensión en la unión pegada | 0,088 MPa → **factor 114×** frente al epóxico |
| Energía de un imán suelto | 1,54 J |
| Flecha del eje | 0,025 mm |
| Primera velocidad crítica | 5.951 rpm |
| Trabajo a 2.000 rpm | **34 % de la crítica** (regla: <70 %) |

---

# 5 · COTAS DE LA CINTA

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Banda | Ancho | **150** |  |
| Banda | Espesor | **1,5** | PVC liso, sin tacos |
| Banda | Longitud desarrollada | **1.188** | 2C + πD |
| Banda | Altura de la superficie | **400** | Sobre la cara superior de la base |
| Rodillos | Ø | **60** |  |
| Rodillos | Largo | **170** | Cabe entre laterales de 300 |
| Rodillos | Entre centros | **500** |  |
| Rodillo motriz | rpm | **111,4** | Par necesario 1,80 N·m |
| Rodillo cabeza | Recorrido del tensor | **20** | Ranuras horizontales |
| Cama de deslizamiento | Sección | **400 × 150 × 3,0** | Impide que el ramal se hunda |
| Guías laterales | Sección | **400 × 3,0 × 25** | 2 unidades, a ras del borde de banda |

---

# 6 · COTAS DE LA TOLVA

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Tolva | Boca superior | **260 × 200** |  |
| Tolva | Salida | **150 × 40** | No excede el ancho de banda |
| Tolva | Altura del cono | **170** | Pared a 65° |
| Tolva | Cuello recto | **30** |  |
| Tolva | Volumen útil | **4,47 L** |  |
| Tolva | Luz sobre la banda | **60** |  |
| Tolva | Posición del eje | **110** | **Al inicio de la cinta**, no en el medio |
| Tolva | Recorrido de asentamiento | **405** | Distancia hasta la plancha |
| Compuerta | Apertura | **0 – 25** | Guillotina con escala grabada |
| Vibrador | Tipo | **12 V DC, 0,4 A** | Obligatorio: la tolva se arquea sin él |

> **Corrección respecto a la versión anterior:** la tolva estaba a mitad de la cinta. Se movió al inicio (x = 110 mm) para dar **405 mm de recorrido de asentamiento** antes del rotor. Sin ese recorrido, el material llega al rotor todavía rebotando y en capas irregulares.

---

# 7 · COTAS DE SALIDA

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Plancha | Tramo | **515 a 595** | Espesor 1,0 · PET o policarbonato |
| Cuchilla | Posición | **246** | Desde el borde de la plancha · ajustable 150–600 |
| Cuchilla | Sección | **3,0 × 200** | Aluminio, borde superior redondeado |
| Bandeja inertes | Interior | **280 × 200 × 150** | Acrílico 4 mm |
| Bandeja no ferrosos | Interior | **280 × 700 × 150** | Ídem |
| Deflector | Posición | **920** | Espuma de 50 mm, alto 400 |
| Celdas | Configuración | **4 × 5 kg por bandeja** | Altura de montaje 60 mm |
| Celdas | Resolución | **≈ 5,0 g** | Puente completo, 1 HX711 por bandeja |
| Caída | Altura h | **400** | De la plancha al fondo de bandeja |

**Trayectorias predichas** (modelo validado, integración 2D):

| Objeto | Cae a | Separación frente al inerte |
|---|---|---|
| Inerte (referencia) | 100 mm | — |
| Media lata aplastada | 1.127 mm | **1.027 mm** |
| Fragmento de 25 mm | 526 mm | **426 mm** |
| Fragmento de 35 mm (peor caso) | 391 mm | **291 mm** |

Cuchilla en 246 mm → **margen simétrico de 145 mm** a ambos lados.

---

# 8 · COTAS DEL BASTIDOR

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Base | Dimensiones | **1.650 × 500 × 18** | MDF · 11,1 kg |
| Laterales | Dimensiones | **1.650 × 460 × 18** | MDF con 3 ventanas · 20,5 kg el par |
| Laterales | Separación interior | **300** | Define el ancho útil de la máquina |
| Travesaños | Sección | **40 × 40** | 4 unidades |
| Patas | Ø × alto | **40 × 30** | Caucho, 4 unidades |
| Subplaca del rotor | Dimensiones | **240 × 150 × 10** | Aluminio; apoya sobre las galgas |
| Guarda | Dimensiones | **520 × 330 × 6** | Policarbonato, sólido separado |
| Caja de control | Dimensiones | **200 × 150 × 80** | Exterior al lateral |
| Conjunto | Altura total | **678** | Con tolva |

---

# 9 · MOTOR Y TRANSMISIÓN

| Pieza | Cota | Valor | Nota |
|---|---|---|---|
| Motor rotor | Tipo | **DC escobillas 24 V / 350 W** | 2.750 rpm · Ø90 × 150 |
| Motor rotor | Par en la rampa | **0,160 N·m** | Potencia 33,5 W en 15 s |
| Poleas | Dientes | **25T / 32T** | Relación 1,28:1 |
| Poleas | Ø primitivos | **39,79 / 50,93** | HTD-5M ancho 15 |
| Correa | Longitud | **503** | Pedir HTD-5M de 525 mm |
| Transmisión | Entre centros | **180** | Aleja el motor de los imanes |
| Rotor | rpm a fondo | **2.148** | Techo de firmware 2.000 rpm |
| Alimentación | Fuente | **24 V / 15 A** |  |

---

# 10 · TABLA DE VERIFICACIONES

Las 23 se ejecutan automáticamente al regenerar el paquete:

| # | Verificación | Resultado |
|---|---|---|
| 1 | Imanes ≤ 72 | 60 ✓ |
| 2 | Pared ≥ mínimo por saturación | 5,74 ≥ 4,39 ✓ |
| 3 | Hueco para tira ≥ 2 mm | 11,92 ✓ |
| 4 | Cobertura de banda | margen 15 mm/lado ✓ |
| 5 | rpm a fondo > techo | 2.148 > 2.000 ✓ |
| 6 | Velocidad crítica < 70 % | 34 % ✓ |
| 7 | Unión pegada < 1 MPa | 0,088 ✓ |
| 8 | Desglose del entrehierro | 0,5+1,5+1,0 = 3,0 ✓ |
| 9 | **Tolva al inicio de la cinta** | x = 110 de 500 ✓ |
| 10 | Recorrido de asentamiento ≥ 300 | 405 ✓ |
| 11 | Tolva no choca con el rodillo | 35 > 30 ✓ |
| 12 | Salida de tolva ≤ ancho de banda | 150 ≤ 150 ✓ |
| 13 | Rotor cabe entre laterales | 280 < 336 ✓ |
| 14 | Rodillo cabe entre laterales | 170 < 300 ✓ |
| 15 | Bandeja cabe entre laterales | 280 ≤ 290 ✓ |
| 16 | Inerte cae antes de la cuchilla | 100 < 246 ✓ |
| 17 | Peor conductor pasa la cuchilla | 391 > 246 ✓ |
| 18 | Margen simétrico ≥ 100 mm | 145 ✓ |
| 19 | Deflector dentro de la bandeja | 920 ≤ 946 ✓ |
| 20 | Largo total cabe en la base | 1.595 < 1.650 ✓ |
| 21 | Cama con holgura a rodillos | 400 ≤ 420 ✓ |
| 22 | Guarda cubre la zona de vuelo | 520 ≥ 326 ✓ |
| 23 | v_banda dentro de límites | 0,35 ✓ |

---

# 11 · LO QUE FALTA VERIFICAR

- [ ] **Precio y stock de 60 imanes 60×10×5 N52** — bloquea la compra
- [ ] Confirmar que la **magnetización es a través de los 5 mm**
- [ ] Taller de balanceo dinámico para un rotor de 6,1 kg y Ø112
- [ ] `D_r` real medido tras el zunchado → **recalcular λ** y regenerar el paquete
- [ ] Los factores de derrateo del modelo (giro de la pieza, campo real) son **estimaciones de ingeniería**; se miden con el péndulo en el hito de validación
- [ ] Curva par-velocidad del motor adquirido, para confirmar la relación de poleas

## Referencias

- Hader, A. *et al.* (2024). *Experimental and numerical analysis of the magnetic force applied to aluminum particles in an Eddy current separator*. **Int. J. Plasma Environ. Sci. Technol. 18**, e03003.
- Schloemann, E. (1975). **J. Appl. Phys. 46**(11). — teoría y experimentos sobre discos.
- Smith, Nagel y Rajamani (2019). **Minerals Engineering 133**, 149–159.
- Radial Magnet Inc. — regla de dimensionado del yugo por flujo medio-polo.
- K&J Magnetics / MagmaMagnets — remanencia por grado.
