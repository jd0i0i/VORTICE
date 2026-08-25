# VÓRTICE 150 — Decisión de arquitectura del lanzamiento

*Cuantificada antes de implementar. Actualizado: 24/08/2026 · `master.yaml` v3*

---

## 1 · Por qué hay que decidir

La v2 lanzaba el material desde una **plancha fija horizontal** de 80 mm montada sobre el rotor. Una auditoría externa encontró cinco defectos bloqueantes; tres de ellos son de esta arquitectura y **no se arreglan moviendo cotas**:

| | Medida sobre el modelo v2 |
|---|---|
| Hueco abierto entre la descarga de banda (x=468,4) y el borde de la plancha (x=515) | **46,60 mm** |
| Caída libre en ese hueco a 0,35 m/s | **86,9 mm** — la pieza no aterriza en la plancha |
| Dónde acaba realmente | impacta el flanco del rotor en **x=501,1 · z=405,3**, a **73,4°** aguas arriba de la cima, contra una superficie a 8,18 m/s |
| Distancia de frenado del inerte sobre la plancha (μ=0,25 / μ=0,50) | **25,0 / 12,5 mm** de los 80 disponibles |
| Velocidad de banda para cruzar los 46,6 mm perdiendo < 1 mm de altura | **3,26 m/s** — nueve veces la de proyecto |

Barrido de velocidades sobre el modelo: a 0,45 m/s (el `v_banda_max` que el YAML declaraba admisible) la pieza impacta el rotor a 62,4°; a 2,0 m/s, a 19,3°. **Ninguna velocidad de banda salva esa geometría.**

---

## 2 · Las tres salidas, con números

Se evaluaron tres. La comparación es contra la v2 como línea base (entrehierro nominal 3,0 mm), y el criterio duro es **qué le pasa a H1**, que es el corazón del proyecto: H1 exige un entrehierro **constante a lo largo de X** e **indexable**.

### Opción A — el rotor pasa a ser el tambor de cabeza *(ADOPTADA)*

El rotor magnético gira dentro de una carcasa no conductora que rueda libre sobre su mismo eje mediante dos rodamientos propios, y **la banda envuelve esa carcasa**. Es la configuración industrial de un separador de corrientes de Foucault, a escala.

```
rotor + zuncho   Ø112,6
+ 1,0 holgura →  ID de carcasa  114,6
+ 1,0 pared   →  OD de carcasa  116,6
+ 1,5 banda   →  material a R = 59,80 mm
entrehierro = 59,80 − 55,80 = 4,00 mm
```

- **Coste magnético:** el entrehierro pasa de 3,0 a 4,0 mm. `F/F₀ = e^(−1,0/5,58) = 0,8359` → **−16,4 %** de fuerza.
- **Lanzamiento:** una pieza sin empuje no despega en la cima. `v_mín = √(gR) = 0,7659 m/s`; a 0,35 m/s (el 46 %) sigue la banda hasta `θ = acos(v²/gR) = 77,95°` y sale tangencialmente en x=558,48 · z=400,69, con vx=0,073 y vz=−0,342 m/s. Cae en **x = 574,0**.
- **B‑2, B‑3 y B‑4 desaparecen por construcción:** no hay transferencia, no hay hueco, no hay plancha y no hay tramo donde el material deslice sobre algo quieto.

### Opción B — plancha inclinada *(DESCARTADA: geométricamente imposible)*

No se descarta por coste ni por el entrehierro variable. Se descarta porque **no hay altura donde inclinar nada**:

- La cara superior de la plancha está en z=448, al ras de la banda.
- La cima del rotor con zuncho está en z=445,5.
- Con la holgura de 1,5 mm, el intradós de cualquier placa sobre el rotor debe estar en z ≥ 447,0, o sea el trasdós en **z ≥ 448,0 — exactamente el nivel de la banda**.

**El presupuesto vertical disponible es cero.** Una placa que descienda entre la descarga y la cima estaría *dentro* del rotor. Para conseguir los 22° sobre los 46,6 mm hay que bajar el plano de lanzamiento **18,8 mm**, y eso abre el entrehierro efectivo de 3,0 a 21,8 mm:

$$e^{-18{,}8/5{,}58} = 0{,}034 \quad\longrightarrow\quad \textbf{3,4 \% de la fuerza nominal.}$$

Y hay un segundo error en el enunciado de B: **22° está por debajo de arctan(0,5) = 26,57°**. Con el μ desfavorable que el propio proyecto exige usar, una rampa de 22° **decelera**: `a = g(sin22° − 0,5·cos22°) = −0,87 m/s²`.

### Opción C — la banda se prolonga sobre el rotor usando una cama de deslizamiento

La banda actual no voltea antes del rotor: pasa **por encima** de él sobre una cama rígida no conductora y voltea en un rodillo pequeño aguas abajo.

- Resuelve B‑2 y B‑3 igual de bien que A: el material va sobre banda todo el tiempo y la banda **arrastra**.
- Cumple B‑4 sobrado: con un rodillo de cabeza de Ø30, `√(gR) = 0,40 m/s` con R = 16,5 mm; a 0,35 la pieza acompaña la banda hasta 38,7°.
- **Su única ventaja real sobre A:** el entrehierro se sigue indexando **bajando el rotor con las galgas**, con cero piezas nuevas. En A hace falta un juego de manguitos.

Lo que la hace perder:

| | Cálculo |
|---|---|
| Espesor de cama mínimo | Una cama de PET de 1 mm sobre el vano de 140 mm flecta **0,48 mm** solo por el peso de banda y material (viga apoyada, E=3 GPa), y la holgura al zuncho es de 1,0 mm. Con la componente normal de la tensión de banda por desalineación (T·θ ≈ 0,7 N a 2°) la flecha se duplica. **2 mm es el mínimo prudente.** |
| Entrehierro resultante | 0,5 zuncho + 1,0 holgura + **2,0 cama** + 1,5 banda = **5,0 mm** |
| Coste magnético | `e^(−2,0/5,58) = 0,699` → **−30,1 %**, contra el −16,4 % de A |
| Ramal de retorno | Hoy pasaría por dentro del rotor: hacen falta **2 rodillos de reenvío** para bajarlo |
| Rodillo de cabeza | Debe librar el rotor: con Ø30 queda en x ≈ 620, o sea el lanzamiento se **retrasa** 120 mm y la máquina se alarga |

---

## 3 · Comparación

| | **A · tambor magnético** | B · plancha inclinada | C · cama bajo la banda |
|---|---|---|---|
| Entrehierro nominal | **4,00 mm** | ≥ 21,8 mm | 5,00 mm |
| Fuerza relativa a la v2 (3,0 mm) | **0,836  (−16,4 %)** | 0,034 (−96,6 %) | 0,699 (−30,1 %) |
| ¿Entrehierro constante a lo largo de X? | **sí** | **no** | sí |
| ¿Indexable? cómo | sí — 3 manguitos deslizantes | — | sí — galgas, sin piezas nuevas |
| B‑2 hueco de 46,6 mm | **eliminado por construcción** | persiste | eliminado |
| B‑3 fricción con μ=0,5 | **no hay tramo deslizante** | no resuelto (22° < 26,57°) | no hay tramo deslizante |
| B‑4 √(gR) | fija el punto de despegue (78°) | — | cumplido (rodillo Ø30) |
| B‑1 cuchilla y B‑5 aislamiento | **hay que corregirlos aparte** | ídem | ídem |
| Piezas nuevas | carcasa + 2 discos + 2 rodamientos 6004 + 3 manguitos | plancha inclinada | 3 rodillos + cama rígida |
| Piezas que se eliminan | plancha fija, 2 carriles, 1 rodillo | — | plancha fija, 2 carriles |
| Coste incremental sobre la lista v2 | **+144.000 COP** | n/a | +165.000 COP |
| Largo total de la máquina | **1.526 mm** | ~1.600 mm | ~1.650 mm |
| Criterio 2 de la feria | configuración **real de planta**, a escala | rampa | híbrido sin referente industrial |

### Desglose del coste incremental de A

| Concepto | COP |
|---|---|
| 2 rodamientos 6004‑2RS (20×42×12) | +24.000 |
| Mandril de laminado + desmoldante | +25.000 |
| Filamento PETG adicional (2 discos + 3 manguitos ≈ 1,3 kg) | +95.000 |
| Guarda mayor: de 520×330 a 741×330 en dos paños | +40.000 |
| Banda a medida más larga (1.279 contra 1.188 mm) | +10.000 |
| Motorreductor de 150 rpm en vez de 100 (ver §7.4 del informe) | +10.000 |
| **Un rodillo menos**: el tambor sustituye al rodillo de cabeza | **−60.000** |
| **Neto de la arquitectura** | **+144.000** |

El laminado de la carcasa **no añade material**: usa la misma cinta de fibra de vidrio y el mismo epóxico que ya compra el zunchado (A10, A11), y es la misma técnica que el equipo tiene que dominar de todos modos.

---

## 4 · Decisión: **A**

Por tres razones, en este orden:

1. **Cierra B‑2, B‑3 y B‑4 por construcción**, no por ajuste de cotas. Ninguna cota futura puede reabrirlos.
2. **Cuesta la mitad de fuerza que C** (−16,4 % contra −30,1 %) por un coste incremental prácticamente igual (+144.000 contra +165.000 COP).
3. Es la configuración industrial. En el interrogatorio del criterio 2, poder decir *"el rotor magnético es el tambor de cabeza y la banda lo envuelve; es lo que hace una planta real, a escala"* — y enseñar el rotor visible dentro de su carcasa transparente — vale más que cualquier rampa.

### Lo que hay que asumir de frente

**A, tal como se dimensionó al principio, eliminaba el experimento de H1.** En la v2 el entrehierro se indexaba **bajando el rotor** con la pila de galgas. Con el rotor concéntrico dentro de su propia carcasa, bajarlo no cambia el entrehierro: lo fija el **diámetro exterior del tambor**. El argumento "A conserva el experimento y B lo pierde" **no se sostiene sin hardware añadido**.

La solución implementada, y su coste, están en el presupuesto de arriba:

| Manguito (pared) | OD del tambor | Entrehierro | F/F₀ | Banda necesaria |
|---|---|---|---|---|
| 0,0 mm (sin manguito) | 116,6 | **4,00 mm** | 1,000 | 1.279,00 mm |
| 1,5 mm | 119,6 | 5,50 mm | 0,764 | 1.283,89 mm |
| 3,0 mm | 122,6 | 7,00 mm | 0,584 | 1.288,79 mm |
| 4,5 mm | 125,6 | 8,50 mm | 0,446 | 1.293,69 mm |

- Los manguitos son **deslizantes, no partidos**: se retira un disco de extremo y salen axialmente. Un manguito partido dejaría dos costuras bajo la banda.
- El cambio de manguito mueve el desarrollo de banda **14,69 mm**; el tensor se dimensionó a **40 mm** de recorrido (±20) para absorberlo con margen para el estirado.
- **Las galgas siguen existiendo, con otro cometido:** ahora bajan el eje `galga = pared del manguito` para que la línea de banda se mantenga en z=400 con cualquier manguito. La convención de signo A‑17 se conserva intacta.
- La caída de fuerza entre el manguito 0 y el 3 es de **×0,446**: el barrido sigue siendo tan medible como el de la v2.

### Consecuencias que se aceptan

- **La balística de la v1/v2 queda invalidada entera.** No se conservó ningún alcance. Ver §5.
- El rotor magnético queda **encerrado por construcción** dentro de la carcasa y la banda. Es una ganancia de seguridad que la v2 no tenía, y no sustituye a la guarda.
- El tambor añade carga radial al eje a través de sus rodamientos, en y = ±106. Se recalculó: flecha 0,0442 mm, crítica **4.500 rpm**, se trabaja al **44,4 %** (límite 70 %). La v2 daba 5.951 rpm porque **no contabilizaba esa carga**.
- La carcasa **debe ser no conductora**. Una carcasa metálica sería una espira en cortocircuito girando en el campo: se calentaría y frenaría el rotor.

---

## 5 · La balística hubo que rehacerla, y no se pudo "recalcular"

Los cuatro alcances de la v1/v2 no eran válidos ni antes de esta sesión: codificaban `h = 400 mm` en una máquina cuyo piso real estaba a 336, y su velocidad de salida solo era recuperable dividiendo por √(2h/g) — o sea que **escondían la altura dentro del número**.

El problema de fondo es otro: esa velocidad de salida procede de un empuje de entre **6,2 g** (sobre los 126,6 mm que van de la descarga al borde de plancha) y **16,1 g** (si solo cuenta la zona de ±24,4 mm donde el entrehierro efectivo se mantiene dentro de un λ/4π), y **no tiene derivación citable**. Cambiada la arquitectura, el empuje actúa sobre el arco de envolvimiento y no sobre una placa plana: tampoco hay número para eso.

**Decisión tomada, y hay que saberla al exponer:**

- `master.yaml` guarda ahora **velocidades de salida**, no alcances, y las cuatro van marcadas **`[VERIFICAR]`**.
- Los alcances se **derivan** de esas velocidades y de la geometría real. Si cambia el piso de bandeja, cambian solos.
- La cuchilla, las bandejas y el deflector se posicionaron **bajo un supuesto declarado**, y el criterio de aceptación "las cuatro trayectorias no intersectan ningún sólido" se evalúa **contra ese supuesto**, no contra un hecho.
- Lo cierra **P‑06** (péndulo). Hasta entonces, la cuchilla es **ajustable en seis posiciones indexadas** de 643 a 743 mm, y las bandejas se mueven con ella sobre un carril común.

Lo único que **sí** se puede calcular sin suponer nada es la trayectoria del inerte, que solo depende de `v_banda` y de la geometría: cae en **x = 574,0 mm**.

---

## 6 · Un error propio que este trabajo cazó

Al implementar la nueva balística se escribió el tiempo de vuelo como

```python
t = (-vz + sqrt(vz**2 + 2*g*dz)) / g        # MAL
```

que es la raíz del lanzamiento **hacia arriba**. Con `vz` negativo — que es el caso del inerte, que despega a 78° de la cima bajando — la trayectoria atravesaba el piso de la bandeja y terminaba en z = −87 mm. El signo correcto es

```python
t = ( vz + sqrt(vz**2 + 2*g*dz)) / g        # BIEN
```

y mueve el alcance del inerte de 579,1 a **574,0 mm**.

**Lo detectó la comprobación D3** (trayectoria contra sólidos), que lo reportó como *"el inerte choca con base_MDF y celda_carga"*. Ninguna comprobación de la v2 lo habría visto: todas comparaban números contra fórmulas o sólidos contra sólidos, y ninguna seguía el camino del material. Es exactamente el argumento por el que se añadieron las cinco familias nuevas.
