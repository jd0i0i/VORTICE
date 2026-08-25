# VÓRTICE — Qué cambió desde el anteproyecto entregado, y por qué

*Munición para el interrogatorio del criterio 2. No es burocracia: cada fila explica una decisión de ingeniería.*
*Actualizado: 24/08/2026 · fuentes: `Documentos/02_VORTICE_Proyecto_Completo.md` (anteproyecto) y `PARAMETERS/master.yaml` v3*

---

## Por qué existe este documento

**El anteproyecto entregado describe otra máquina.** No coincide un solo número con VÓRTICE 150. Si un jurado abre el anteproyecto y luego mira la máquina, la pregunta es inmediata, y la respuesta *"es que lo mejoramos"* no vale. Cada cambio tiene una razón física o de costo, y aquí están todas.

La frase que hay que poder decir es: **el anteproyecto era una prueba de concepto; VÓRTICE 150 es un banco de medida.** Todo lo demás se sigue de ahí.

---

## 1 · Arquitectura

| | Anteproyecto | VÓRTICE 150 v3 | Razón del cambio |
|---|---|---|---|
| **Alimentación** | Rampa inclinada de acrílico, 30–35°, el visitante deja caer el material | **Cinta transportadora** de 150 mm a 0,35 m/s, con tolva de 4,33 L, vibrador y compuerta 0–25 mm | En una rampa la velocidad de entrada **no es controlable ni repetible**: depende de dónde y cómo suelte cada visitante. Sin velocidad de entrada fija no hay alcance reproducible, y sin alcance reproducible no hay curva de eficiencia. La cinta convierte la velocidad de entrada en una **variable de control** en vez de en una fuente de ruido |
| **Lanzamiento** | La rampa termina junto al rotor; el material pasa "a pocos milímetros de la superficie" | **El rotor magnético ES el tambor de cabeza**: gira dentro de una carcasa no conductora y la banda lo envuelve | Es la configuración industrial real. Con rampa o con plancha, el material recorre un tramo **sin nada que lo empuje** y la fricción lo para: a 0,35 m/s y μ=0,5, el frenado es de 12,5 mm. Ver `DECISION_ARQUITECTURA.md` |
| **Etapa ferrosa** | Imán fijo bajo la rampa que retiene el acero (12.000 COP) | **Eliminada.** El banco opera *aguas abajo* de la separación ferrosa y se declara así | El acero se **pega** al rotor y no se lanza; con él en la alimentación no hay experimento, hay un atasco. En una planta real el acero se retira antes. Declararlo es más honesto que simularlo mal |
| **Módulo didáctico** | Tubo de cobre + imán, disco de aluminio macizo y ranurado (35.000 COP) | **Se había perdido en la v2. Se recupera** | Es el gancho de interacción manual y la demostración del núcleo laminado. Cuesta 35.000 COP y es lo que el criterio 1 premia |

---

## 2 · Rotor y campo

| | Anteproyecto | VÓRTICE 150 v3 | Razón del cambio |
|---|---|---|---|
| **Imanes** | 12 uds. N35–N42 | **60 uds. N52** de 60×10×5, magnetizados a través de los 5 mm | 10 polos × 2 piezas de ancho × 3 filas axiales. Las 3 filas dan **180 mm de largo activo**, que es lo que permite usar una banda de 150 mm de ancho útil. Con 12 imanes el rotor solo cubre una franja estrecha |
| **Diámetro del rotor** | Ø60, PVC o impresión 3D | **Ø111,6** en la cara del imán, sobre **tubo de acero cédula 40 de 3‑1/2"** | El PVC **no es yugo magnético**: sin hierro detrás, la mitad del flujo se cierra por el aire. La pared de acero debe superar el mínimo por saturación, `t = W·Br/(2·B_sat) = 4,39 mm`; la cédula 40 da 5,74 |
| **Pares de polos p** | 6 | **5** | Consecuencia de 10 polos. Menos polos con más diámetro da **mayor paso polar**, y el paso polar es lo que fija hasta dónde llega el campo por encima del rotor |
| **Definición de λ** | «paso polar del orden de 1,5 cm» = π·60/12, o sea el **paso entre polos contiguos** | **λ = π·D_r/p = 70,12 mm**, o sea el paso de un **par** de polos (un ciclo N‑S completo) | **No es solo un número distinto: es una definición distinta.** En la literatura de separadores (Schloemann) λ es la longitud de onda del campo, que abarca un N y un S. El anteproyecto usó la mitad. Con su propia convención, sus decaimientos eran 2,5 y 1,25 mm; con la convención correcta habrían sido 5,0 y 2,5 |
| **Decaimiento del campo λ/2π** | 2,4 mm (con su convención) | **11,16 mm** | Un campo que solo llega a 2,4 mm exige un entrehierro imposible de mantener con una rampa manual. Con 11,16 mm, abrir el entrehierro de 4,0 a 8,5 deja la fuerza en ×0,446 — que es **medible**, y es el experimento de H1 |
| **Decaimiento de la fuerza λ/4π** | 1,2 mm (con su convención) | **5,58 mm** | Ídem |
| **Frecuencia de alternancia** | 300 Hz a 3.000 rpm | **116,67 Hz a 1.400 rpm** | f = p·N/60. Bajar de 3.000 a 1.400 rpm con un rotor de 6,12 kg y Ø111,6 es **una decisión de seguridad**: la energía almacenada crece con N². A 2.000 rpm ya son 251 J |
| **Profundidad de piel δ(Al)** | 4,9 mm a 300 Hz | **7,82 mm a 116,67 Hz** | δ = √(ρ_e/πfμ₀), con ρ_e(Al) = 2,82×10⁻⁸ Ω·m — **la misma ρ que usó el anteproyecto**. Baja la frecuencia, sube δ. Las piezas del lote miden de 0,10 a 1,50 mm: quedan completamente penetradas en los dos casos, y **eso es lo que hay que decir**, no la cifra |
| **Retención de imanes** | Alojamientos + epóxico + 2 vueltas de fibra | **Doble seguro**: tiras de PETG impreso entre polos (retención mecánica positiva) + zunchado de fibra y epóxico | A 2.000 rpm cada imán tira con **52,6 N**. El pegado solo no se considera suficiente; el hueco entre polos (11,92 mm) admite la tira (11,3) con 0,6 de juego |
| **Entrehierro** | «3 a 5 mm», ajustando la inclinación de la rampa | **4,00 mm nominal**, indexado a 5,5 / 7,0 / 8,5 con manguitos deslizantes | Un entrehierro que se ajusta inclinando una rampa **no es constante a lo largo de X**, y H1 exige que lo sea |

---

## 3 · Accionamiento

| | Anteproyecto | VÓRTICE 150 v3 | Razón del cambio |
|---|---|---|---|
| **Motor** | DC 775, 12 V, 0–10.000 rpm | **DC 24 V / 350 W** (tipo MY1020), 2.750 rpm | El 775 mueve un rotor impreso de gramos. El de la v3 pesa **6,12 kg** con 0,0115 kg·m² de inercia; la rampa de arranque pide 33,5 W sostenidos y el par de un 775 no lo da con margen |
| **Transmisión** | **Montaje directo al eje del motor**, con acople de aluminio | **Correa HTD‑5M**, entrecentros 180 mm, relación 25T/32T | Dos razones. Física: los imanes de neodimio a 20 mm del motor **interfieren con los de ferrita del estátor**. Mecánica: el par de arranque de un rotor de 6 kg destroza el eje de un motor pequeño y su rodamiento delantero |
| **Rodamientos del rotor** | 608ZZ, eje Ø8 | **2 chumaceras UCP204**, eje Ø20 rectificado h6, span 340 | Un eje de 8 mm con 6 kg colgados flecta demasiado. Con Ø20 la flecha es de 0,044 mm y la primera crítica queda en 4.500 rpm: se trabaja al **44 %** |
| **Alimentación** | Fuente 12 V / 5 A | **24 V / 15 A** + convertidores DC‑DC a 12 V (vibrador) y a 5 V (lógica) | Dos motores en vez de uno, y uno de 350 W |

---

## 4 · Instrumentación — *lo que NO cambió*

| | Anteproyecto | VÓRTICE 150 v3 | |
|---|---|---|---|
| **Celdas de carga** | **2 de 1 kg** + 2 HX711 | **2 de 2 kg**, una por bandeja, + 2 HX711 | El anteproyecto acertó y la v2 se equivocó: llegó a poner **8 celdas de 5 kg** (20 kg de fondo de escala) para medir **83,7 g de aluminio**. La v3 vuelve a dos, con dos canales de datos, y sube a 2 kg solo porque las bandejas de la v3 son mayores |
| **Muestras** | «Al, Cu, latón, acero, plástico, vidrio» | Lote patrón (Al, PET, HDPE, vidrio) **+ lote H2 de Al, Cu y latón** a 25×25×0,5 mm | El anteproyecto **ya tenía Cu y latón**. La v2 los perdió, y con ellos H2 dejó de ser medible. La v3 los recupera y añade la condición que faltaba: *a geometría y espesor controlados* |
| **Medida del campo** | «brújula o sensor Hall» para verificar polaridad | **Bobina de prueba** (200 esp. AWG32 sobre Ø10) + **sonda Hall SS49E** | Verificar la polaridad no es medir B(z). H1 exige medir el **perfil** del campo, y para eso hace falta un instrumento que la v2 mencionaba en el texto y no tenía en la lista de compras |
| **RPM** | Sensor óptico reflectivo | Encoder de ranura óptica | Sin cambio de fondo |

---

## 5 · Escala, costo y calendario

| | Anteproyecto | VÓRTICE 150 v3 |
|---|---|---|
| Masa del rotor | gramos (PVC/impreso) | **6,12 kg** |
| Masa de la máquina | mesa de acrílico y MDF | del orden de **40 kg** |
| Huella | no acotada | **1.300 × 500 × 708 mm** (extensión real 1.526 mm) |
| **Presupuesto** | **485.000 COP**, con «límite de 500.000» | **3.366.000 COP** |
| Factor sobre el techo del anteproyecto | 0,97× | **6,7×** |

> ### El techo está en disputa y hay que resolverlo
> El **anteproyecto** dice literalmente *"deja ~15.000 de margen sobre el límite de **500.000**"*. La documentación posterior del proyecto cita un techo de **1.000.000**. **Son dos cifras distintas y ninguna de las dos alcanza.** Está abierto como **P‑01** y bloquea toda la compra. No es un problema de recortes: es una decisión sobre qué máquina se construye.

---

## 6 · Lo que sí sobrevivió intacto

Conviene tenerlo a mano: no todo cambió.

- **La física**: Faraday, Lenz, `f = p·N/60`, `B(z) ≈ B₀e^(−2πz/λ)`, `F ∝ B²`, la profundidad de piel, y la figura de mérito **σ/ρ_m** como razón de que el aluminio se lance más que el cobre.
- **La medida por masa** en dos recipientes instrumentados, y de ahí tasa de recuperación y pureza.
- **El módulo del lema**: `N = (m/M)·N_A` sobre el aluminio recuperado.
- **La cuchilla divisora ajustable** entre dos recipientes.
- **Las dos hipótesis** H1 y H2.
- **La carcasa cerrada como requisito de seguridad**, no como acabado.

---

## 7 · Cómo contarlo en tres frases

1. *"El anteproyecto era una prueba de concepto con una rampa; lo que trajimos es un banco de medida con cinta, porque sin velocidad de entrada controlada no hay curva de eficiencia reproducible."*
2. *"Subimos el rotor de Ø60 en PVC a Ø111,6 sobre tubo de acero porque el PVC no hace de yugo: sin hierro detrás se pierde la mitad del flujo. Y bajamos de 3.000 a 1.400 rpm porque la energía almacenada crece con el cuadrado."*
3. *"Y corregimos una definición: el anteproyecto llamaba paso polar al paso entre polos contiguos; λ es el paso de un par completo. Por eso nuestros decaimientos son el doble."*
