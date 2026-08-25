# VÓRTICE 150 — Decisiones pendientes

*Lo que falta resolver antes de mecanizar, comprar o medir.*
*Actualizado: 24/08/2026 · `PARAMETERS/master.yaml` v3*

Ordenado por lo que **bloquea** primero. Cada punto dice qué hay que hacer, quién puede hacerlo y qué pasa si sale mal.

---

## P-01 · BLOQUEA LA COMPRA — El techo y la máquina son incompatibles

**Estado:** abierto · **Bloquea:** toda la compra

| | COP |
|---|---|
| Techo citado en la documentación del proyecto | 1.000.000 |
| Techo que dice el **anteproyecto entregado** (*"~15.000 de margen sobre el límite de 500.000"*) | 500.000 |
| Estimación de esta lista de materiales | **3.401.000** |

**Hay dos cifras de techo circulando y ninguna de las dos alcanza.** Los 60 imanes N52 solos (780.000 COP) valen el **78 %** del techo de 1.000.000 y el **156 %** del de 500.000.

**Y no hay combinación de recortes que la meta.** Sumadas *todas* las palancas —incluida bajar a una sola fila de imanes, que deja la máquina en una prueba de concepto— el ahorro máximo real es de **731.000 COP** y el suelo queda en **2.670.000**, o sea **2,67 veces** el techo de 1.000.000.

> **Ojo con la aritmética de la tabla vieja.** Las dos palancas de imanes (2 filas / 1 fila) **son excluyentes**: la segunda contiene a la primera. Sumarlas era lo que hacía parecer que la tabla llegaba al techo.

**Hay que decidir explícitamente cuál de los dos cambia. Solo hay tres salidas honestas:**

1. **Sube el techo.** VÓRTICE 150 se construye tal cual. Requiere financiación adicional o patrocinio, **y hay que pedirla ahora, no en octubre.**
2. **Cambia la máquina.** Se vuelve a una escala tipo anteproyecto y se acepta perder la velocidad de banda como variable experimental. **Entonces hay que rehacer el paquete entero**, no recortar este.
3. **Se construye por fases y solo se compra lo que se financia**, empezando por la prueba de concepto del rotor (≈ 15 %), que es lo que decide si el proyecto sigue.

> **Regla que no se toca:** no se gasta el presupuesto completo antes de validar el rotor.

---

## P-02 · BLOQUEA LA COMPRA — Eje de magnetización de los imanes

**Estado:** abierto · **Bloquea:** el pedido de imanes

Todo el diseño supone magnetización **a través de los 5 mm** (el espesor radial). Si el proveedor envía imanes magnetizados a través de los 10 mm o de los 60, **el rotor no funciona** y no hay forma de arreglarlo después.

**Qué hacer:** exigirlo por escrito en la orden de compra, con la figura. Al recibir, verificar con la **sonda Hall SS49E (H5)** o una brújula **antes de pegar el primero**.

---

## P-03 · Taller de balanceo dinámico

**Estado:** abierto · **Bloquea:** superar las 1.400 rpm

Un rotor de **6,12 kg** girando a Ø111,6 y hasta 2.000 rpm necesita balanceo dinámico. La energía almacenada a 2.000 rpm es de **251 J** y cada imán tira con **52,6 N**.

**Qué hacer:**
- Localizar un taller en Barranquilla con balanceadora para rotores de esta masa y diámetro (talleres de turbo, alternadores o bombas industriales).
- Pedir grado **G6.3 o mejor**.
- Confirmar que aceptan un rotor **con imanes permanentes** — algunos no, por la máquina de medida.
- **Balancear el rotor SIN la carcasa**: la carcasa no gira con él.

**Si no aparece taller:** limitar el firmware a 1.400 rpm y anotarlo como restricción del experimento. No subir «a ver qué pasa».

---

## P-04 · Medir `D_r` real tras el zunchado y recalcular λ

**Estado:** abierto · **Bloquea:** la validez de las predicciones

Todo el modelo cuelga de `λ = π·D_r/p = 70,12 mm`. `D_r` es el diámetro **en la cara del imán**, y el zunchado de fibra lo modifica: el espesor real del laminado no será exactamente 0,5 mm.

**Qué hacer, en este orden:**
1. Armar el rotor y zuncharlo.
2. Medir `D_r` con calibrador en **al menos 6 posiciones angulares y 3 axiales**. Anotar media y dispersión.
3. Escribir el valor medido en `master.yaml → rotor.geometria.D_r`.
4. Volver a ejecutar los tres scripts.

> Si `D_r` sube 1 mm, λ sube 0,63 mm. **Y en la v3 hay un efecto nuevo:** `D_r` también fija el ID de la carcasa (`D_r + 2·zuncho + 2·holgura`), así que **la carcasa hay que laminarla DESPUÉS de medir el rotor**, no antes.

---

## P-05 · Laminar la carcasa y los manguitos, y medir su espesor real

**Estado:** abierto · **Bloquea:** el entrehierro y todo H1

El entrehierro nominal de **4,00 mm** es la suma de cuatro espesores, y **dos de ellos se fabrican a mano**: el zuncho (0,5) y la pared de carcasa (1,0). Un laminado de fibra y epóxico rara vez sale al espesor nominal a la primera.

**Qué hacer:**
1. Laminar sobre el mandril (A13) una probeta de prueba antes que la pieza buena. Medir su espesor en 6 puntos.
2. Ajustar el número de capas hasta acercarse a 1,0 mm, y anotar la dispersión.
3. Laminar la carcasa. Medir su **OD real** en 6 posiciones angulares y 3 axiales.
4. Escribir el valor medido en `master.yaml → tambor.OD` y regenerar.
5. Imprimir los manguitos **después**, con la ID ajustada al OD medido.

> Cada 0,1 mm de error en el OD de la carcasa es un 1,8 % de fuerza (`e^(−0,1/5,58)`). Y si el OD sale mayor de lo previsto, **el entrehierro nominal ya no es 4,00**: hay que reescribirlo, no ignorarlo.

**Si el laminado no sale bien:** la alternativa es un tubo de PETG impreso de 1,5 mm de pared, que sube el entrehierro a 5,0 mm y cuesta un 8,6 % más de fuerza. Es peor, pero es controlable.

---

## P-06 · Las cuatro velocidades de salida son `[VERIFICAR]`

**Estado:** abierto · **Bloquea:** fiarse de la posición de la cuchilla

Las velocidades de salida (0,35 / 1,369 / 1,842 / 3,946 m/s) proceden del modelo balístico original, con factores de derrateo por **giro de la pieza** y **campo real** que son *estimaciones de ingeniería, no medidas*. Y el empuje de la arquitectura v3 actúa sobre el **arco de envolvimiento**, no sobre una placa plana: no hay derivación citable para ninguna de las tres conductoras.

La única que se puede calcular sin suponer nada es la del inerte, porque solo depende de `v_banda` y de la geometría del tambor.

**Contexto de magnitud, para saber qué se está suponiendo:** en la arquitectura vieja, `x_lata = 1127` implicaba **6,2 g** sostenidos sobre los 126,6 mm que iban de la descarga al borde de plancha, o **16,1 g** si solo contaba la zona de ±24,4 mm donde el entrehierro efectivo se mantiene dentro de un λ/4π. Es alto incluso para lámina de lata.

**Qué hacer:**
1. Montar el rotor y la carcasa, sin cinta.
2. Colgar cada tipo de pieza de un hilo y medir el **impulso por desviación del péndulo**, a las cuatro posiciones de entrehierro.
3. Convertir a velocidad de salida y escribirla en `master.yaml → salida.lanzamiento.v_salida`.
4. Regenerar: los alcances, la cuchilla y las bandejas se recolocan solos.

> **Mientras tanto:** la cuchilla es **ajustable en 6 posiciones** (643 a 743, cada 25 mm) y **las bandejas se mueven con ella**. Está diseñada para que la medición pueda desmentir la predicción sin rehacer la máquina.
>
> **Regla de redacción que aplica aquí:** ningún resultado propio como hecho consumado. En el póster, el video y la exposición, estos números van como **predicciones**.

---

## P-07 · Medir la resolución y el error de esquina de las celdas

**Estado:** abierto · **Bloquea:** los resultados D y E

Dos números de la instrumentación están marcados `[VERIFICAR]` y **hay que medirlos antes de fiarse de ningún resultado de masa**:

**a) Resolución.** `resolucion_celda = 1 g` es un **objetivo de diseño**, no un dato. No es FS/2²⁴: la fija el piso de ruido mecánico y eléctrico.
*Qué hacer:* masa patrón de 10 g, 20 repeticiones, **con el motor detenido**. Reportar la desviación típica. Si sale peor de 2 g, el 1,19 % de cuantización sobre los 83,7 g de aluminio del lote deja de ser cierto.

**b) Error de esquina.** Una celda monopunto bajo una plataforma de **434 × 280 mm** está por encima del tamaño para el que se compensa el momento.
*Qué hacer:* 100 g en el centro y en las cuatro esquinas. Reportar la dispersión.
*Si supera el 2 %:* la corrección son **dos celdas en paralelo por bandeja** — cuatro en total, pero **siguen siendo dos canales de datos**. Cuesta 44.000 COP más.

---

## P-08 · Curva par-velocidad de los dos motores

**Estado:** abierto · **No bloquea**

- **Motor del rotor.** La relación 25T/32T supone que el motor mantiene rpm bajo la carga de la rampa (33,5 W de 350 disponibles). Medir rpm en vacío y con el rotor montado; si cae más del 10 %, recalcular la relación.
- **Motorreductor de banda.** Se pide para **≥143,2 rpm** (el `v_banda_max` de 0,45 m/s). Verificar que los da **con carga**, no solo en vacío: si el catálogo dice 150 rpm en vacío y cae a 110 con par, el rango experimental de velocidad de banda se queda en nada.

---

## P-09 · Verificaciones documentales

**Estado:** abierto · **No bloquea la construcción**

- [ ] Páginas exactas de los dos artículos de Schloemann (1975).
- [ ] Fuente y página de ρ_e y ρ_m de Al 1050, Cu ETP y latón CuZn37 (CRC / ASM).
- [ ] Precio de la chatarra de aluminio en una chatarrería de Barranquilla.
- [ ] Confirmar que los dos lotes (patrón y H2) son **reproducibles**.

---

## P-10 · FIRMWARE está vacío

**Estado:** abierto · **Bloquea:** la instrumentación entera

No se escribió código de ESP32, ni lectura de HX711, ni control PWM, ni el techo de 2.000 rpm. **El techo existe hoy solo como número en el YAML.**

Lo mínimo que tiene que hacer:
- PWM de los dos motores con rampa de 15 s en el rotor.
- Lectura del encoder → rpm reales (no confiar en el PWM como medida).
- Lectura de los **dos HX711** → dos masas, tara automática antes de cada ciclo.
- **Techo de 2.000 rpm en firmware.**
- Publicar por WiFi: rpm, entrehierro seleccionado, masa de cada fracción, tasa de recuperación, pureza y `N = (m/M)·N_A`.
- **Pesar solo con el motor detenido.**

---

## P-11 · Logística: cómo entra la máquina al Coliseo

**Estado:** abierto · **Bloquea:** el montaje del 30 de octubre

La máquina mide **1.300 × 500 × 708 mm** (1.526 de extensión real) y pesa del orden de **40 kg**. Con la base de 1.300 cabe en el maletero de muchos autos, pero no entra por una puerta estrecha en horizontal ni la levanta una persona sola.

**Qué hay que decidir, y pronto:**
1. **¿Se transporta entera o desmontable en módulos?** Los cortes naturales son tres: *(a)* bastidor + cinta, *(b)* conjunto rotor + tambor + subplacas + motor (sale como una pieza sobre sus pedestales), *(c)* bandejas, cuchilla, deflector y guarda. Si se decide desmontable, hay que preverlo **antes de cortar el MDF**: insertos M6 en vez de tirafondos en las juntas de módulo.
2. **¿Quién la transporta y en qué vehículo?** Medir la puerta del Coliseo y la del aula donde se ensamble.
3. **¿Hay toma de 110 V en el stand?** La fuente es de 360 W.
4. **¿Se puede dejar montada la noche anterior?** Si no, hay que poder montarla en menos de 30 minutos, y eso solo pasa si es modular.

> El rotor lleva **60 imanes N52**. No se transporta suelto, no viaja cerca de tarjetas ni de discos duros, y quien lo cargue debe saber que un imán suelto a 2.000 rpm lleva 1,54 J. **Se transporta con la guarda puesta.**

---

## P-12 · Lo que este trabajo NO tocó

Para que nadie lo dé por hecho:

- **No hay análisis de elementos finitos.** La flecha del eje y la velocidad crítica salen de fórmulas de viga biapoyada y del método de Rayleigh, adecuadas para este caso pero no sustitutas de un FEA si se decide subir de 2.000 rpm.
- **No se validó el modelo electromagnético.** Este paquete verifica que los números son *consistentes entre sí* y que la máquina es *construible y coherente*, no que describa la realidad. Eso lo decide el péndulo (P‑06).
- **La tensión de banda (39,07 N) es derivada, no medida.** De ella cuelga la velocidad crítica.
- **Los precios de la lista de materiales son estimaciones**, no cotizaciones.
