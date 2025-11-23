# Plan de Pruebas Manuales - Sistema de Control Gestual

## Información del Documento

**Versión:** 1.0
**Fecha de creación:** 2025-11-23
**Proyecto:** Sistema de Control de Interfaces mediante Gestos Humanos
**Autor:** Omar Luna Hernández

---

## 1. Objetivos de las Pruebas

### 1.1 Objetivos Principales
- Evaluar la **precisión** del sistema de detección de gestos en diferentes condiciones
- Medir la **latencia** entre el gesto realizado y la acción ejecutada
- Identificar **condiciones límite** que afectan el rendimiento del sistema
- Obtener **métricas cuantitativas** para análisis estadístico
- Documentar **casos de fallo** y sus condiciones asociadas

### 1.2 Métricas a Recolectar
- **Tasa de detección correcta** (True Positive Rate): % de gestos correctamente detectados
- **Tasa de falsos positivos**: % de detecciones incorrectas
- **Tasa de falsos negativos**: % de gestos no detectados
- **Latencia promedio**: Tiempo entre gesto y acción (ms)
- **Latencia máxima y mínima**: Rangos de tiempo de respuesta
- **Precisión del movimiento del cursor**: Desviación del objetivo
- **Tasa de éxito por tipo de gesto**: Precisión para cada gesto específico

---

## 2. Configuración del Entorno de Pruebas

### 2.1 Requisitos de Hardware
- **Cámara**: Resolución mínima 720p, 30 fps
- **Computadora**: Especificaciones del sistema de prueba
  - CPU: [Anotar modelo y velocidad]
  - RAM: [Anotar cantidad]
  - Sistema operativo: [Anotar versión]
- **Iluminación controlable**: Lámparas con intensidad variable
- **Luxómetro o app de medición de luz** (opcional pero recomendado)
- **Cronómetro de alta precisión** o software de medición de tiempo

### 2.2 Configuración del Software
- Python 3.12 o superior
- Todas las dependencias instaladas según [README.md](README.md)
- **Versión del sistema**: [Anotar commit hash o versión]
- **Configuración inicial** (`config.json`):
```json
{
  "left_hand_mode": "keyboard",
  "right_hand_mode": "mouse",
  "left_blink_mode": "left_click",
  "right_blink_mode": "right_click"
}
```

### 2.3 Preparación del Espacio
- **Distancia a la cámara**: 50-70 cm (anotar distancia exacta)
- **Altura de la cámara**: A nivel de los ojos del usuario
- **Fondo**: Preferiblemente uniforme y sin objetos en movimiento
- **Posición del usuario**: Sentado, frente a la cámara

---

## 3. Protocolo de Pruebas

### 3.1 Variables a Evaluar

#### Variable 1: Condiciones de Iluminación
- **IL-1**: Iluminación óptima (300-500 lux, luz natural o artificial frontal)
- **IL-2**: Baja iluminación (50-100 lux, penumbra)
- **IL-3**: Iluminación excesiva (>1000 lux, luz directa)
- **IL-4**: Contraluz (fuente de luz detrás del usuario)
- **IL-5**: Iluminación variable (transiciones luz/sombra cada 30s)

#### Variable 2: Ruido Visual
- **RV-1**: Fondo limpio (sin distracciones)
- **RV-2**: Fondo con objetos estáticos
- **RV-3**: Fondo con movimiento (personas caminando, objetos moviéndose)
- **RV-4**: Usuario con ropa similar al tono de piel
- **RV-5**: Usuario con accesorios (anillos, pulseras, reloj)

#### Variable 3: Velocidad de Movimientos
- **VM-1**: Movimientos lentos (1-2 gestos por segundo)
- **VM-2**: Movimientos normales (3-4 gestos por segundo)
- **VM-3**: Movimientos rápidos (5-6 gestos por segundo)
- **VM-4**: Movimientos muy rápidos (>7 gestos por segundo)

#### Variable 4: Distancia a la Cámara
- **DC-1**: Muy cerca (30-40 cm)
- **DC-2**: Distancia óptima (50-70 cm)
- **DC-3**: Lejos (80-100 cm)
- **DC-4**: Muy lejos (>100 cm)

#### Variable 5: Ángulo de la Mano
- **AM-1**: Frontal (90° respecto a cámara)
- **AM-2**: Inclinada 45° izquierda
- **AM-3**: Inclinada 45° derecha
- **AM-4**: Rotación variable durante el gesto

---

## 4. Pruebas por Módulo

### 4.1 Módulo: Detección de Parpadeos (Blink Detection)

#### Prueba BL-01: Parpadeo del Ojo Izquierdo
**Objetivo:** Medir precisión y latencia en detección de parpadeo del ojo izquierdo

**Procedimiento:**
1. Configurar `left_blink_mode` = `"left_click"`
2. Abrir una aplicación de prueba (e.g., bloc de notas con texto seleccionable)
3. Realizar 50 parpadeos del ojo izquierdo
4. Anotar:
   - Número de clics detectados correctamente
   - Número de falsos positivos (clics sin parpadeo)
   - Número de falsos negativos (parpadeos sin clic)
   - Tiempo aproximado de latencia (usar video grabado si es posible)

**Plantilla de Registro:**
```
Condición: [IL-X, RV-X, etc.]
Total de parpadeos realizados: 50
Detecciones correctas: __/50
Falsos positivos: __
Falsos negativos: __
Latencia promedio estimada: __ ms
Observaciones: _______________
```

**Repetir con:**
- Todas las condiciones de iluminación (IL-1 a IL-5)
- Diferentes posiciones de cabeza (frontal, 15° izq/der, arriba/abajo)
- Con y sin gafas (si aplica)

#### Prueba BL-02: Parpadeo del Ojo Derecho
**Objetivo:** Medir precisión y latencia en detección de parpadeo del ojo derecho

**Procedimiento:** Igual que BL-01, pero con ojo derecho y `right_blink_mode` = `"right_click"`

#### Prueba BL-03: Umbral de EAR (Eye Aspect Ratio)
**Objetivo:** Determinar la sensibilidad del umbral de detección

**Procedimiento:**
1. Modificar `ear_threshold` en [blink_detector.py](blink_detector.py:25) a valores: 0.05, 0.07, 0.10, 0.12
2. Para cada valor, realizar 30 parpadeos normales
3. Anotar tasas de detección y falsos positivos/negativos
4. Identificar el umbral óptimo

**Plantilla de Registro:**
```
Umbral EAR: __
Detecciones correctas: __/30
Falsos positivos: __
Falsos negativos: __
Umbral óptimo: __
```

---

### 4.2 Módulo: Control del Mouse (Mouse Control)

#### Prueba MC-01: Precisión de Movimiento del Cursor
**Objetivo:** Evaluar la precisión del seguimiento del cursor mediante gestos de mano

**Procedimiento:**
1. Configurar `right_hand_mode` = `"mouse"`
2. Crear una cuadrícula en pantalla con objetivos (círculos de 50px de diámetro) en 9 posiciones:
   - Esquinas: superior-izq, superior-der, inferior-izq, inferior-der
   - Centros de bordes: superior-centro, inferior-centro, izq-centro, der-centro
   - Centro de pantalla
3. Para cada objetivo, realizar 10 intentos de posicionar el cursor en el centro
4. Medir:
   - Distancia promedio del cursor al centro del objetivo (en píxeles)
   - Tiempo para alcanzar el objetivo
   - Número de intentos exitosos (cursor dentro del círculo)

**Plantilla de Registro:**
```
Condición: [IL-X, VM-X, DC-X]
Objetivo: [Posición]
Intentos exitosos: __/10
Distancia promedio al centro: __ px
Tiempo promedio: __ s
Observaciones: _______________
```

**Repetir con:**
- Diferentes condiciones de iluminación (IL-1 a IL-5)
- Diferentes velocidades de movimiento (VM-1 a VM-4)
- Diferentes distancias a la cámara (DC-1 a DC-4)

#### Prueba MC-02: Suavizado de Movimiento (Smoothing)
**Objetivo:** Evaluar el efecto del suavizado en la precisión del cursor

**Procedimiento:**
1. Modificar `smoothing_factor` en [gesture_controller.py](gesture_controller.py:34) a valores: 0.1, 0.3, 0.5, 0.7, 0.9
2. Para cada valor, realizar 20 trazos de línea recta en pantalla (usando app de dibujo)
3. Evaluar visualmente:
   - Estabilidad del trazo
   - Capacidad de seguir la intención
   - Retraso percibido
4. Anotar el factor de suavizado óptimo

**Plantilla de Registro:**
```
Smoothing factor: __
Estabilidad (1-5): __
Precisión (1-5): __
Latencia percibida (1-5): __
Factor óptimo: __
```

#### Prueba MC-03: Latencia de Movimiento
**Objetivo:** Medir el tiempo de respuesta del movimiento del cursor

**Procedimiento:**
1. Grabar en video (cámara externa a 60fps o más) la mano y la pantalla simultáneamente
2. Realizar 20 movimientos rápidos de mano en direcciones cardinales (arriba, abajo, izq, der)
3. Analizar el video frame por frame:
   - Frame donde inicia el movimiento de la mano
   - Frame donde el cursor comienza a moverse
   - Calcular la diferencia en milisegundos
4. Calcular latencia promedio, mínima y máxima

**Plantilla de Registro:**
```
Movimiento #: __
Frame inicio mano: __
Frame inicio cursor: __
Latencia (ms): __
---
Latencia promedio: __ ms
Latencia mínima: __ ms
Latencia máxima: __ ms
Desviación estándar: __ ms
```

---

### 4.3 Módulo: Control del Teclado (Keyboard Control)

#### Prueba KC-01: Detección de Dirección de Movimiento
**Objetivo:** Evaluar la precisión en la detección de direcciones (arriba, abajo, izquierda, derecha)

**Procedimiento:**
1. Configurar `left_hand_mode` = `"keyboard"`
2. Abrir un editor de texto o juego que responda a flechas direccionales
3. Realizar 50 gestos por cada dirección:
   - 50 movimientos hacia arriba
   - 50 movimientos hacia abajo
   - 50 movimientos hacia la izquierda
   - 50 movimientos hacia la derecha
4. Anotar:
   - Detecciones correctas por dirección
   - Falsos positivos (dirección incorrecta detectada)
   - Falsos negativos (sin detección)

**Plantilla de Registro:**
```
Condición: [IL-X, VM-X, DC-X]
Dirección: [arriba/abajo/izq/der]
Total de gestos: 50
Detecciones correctas: __/50
Falsos positivos: __
Falsos negativos: __
Precisión: __%
```

**Repetir con:**
- Diferentes velocidades de movimiento (VM-1 a VM-4)
- Diferentes ángulos de mano (AM-1 a AM-4)
- Diferentes distancias (DC-1 a DC-4)

#### Prueba KC-02: Umbral de Movimiento (Movement Threshold)
**Objetivo:** Determinar el umbral óptimo para detectar direcciones

**Procedimiento:**
1. Modificar `movement_threshold` en [gesture_controller.py](gesture_controller.py:34) a valores: 40, 60, 80, 100 píxeles
2. Para cada valor, realizar 30 gestos direccionales
3. Evaluar:
   - Sensibilidad (detección de movimientos pequeños)
   - Estabilidad (evitar detecciones espurias)
4. Identificar el umbral óptimo

**Plantilla de Registro:**
```
Umbral (px): __
Detecciones correctas: __/30
Detecciones espurias: __
Gestos no detectados: __
Umbral óptimo: __
```

#### Prueba KC-03: Latencia de Detección de Dirección
**Objetivo:** Medir el tiempo de respuesta de las teclas direccionales

**Procedimiento:**
1. Grabar video de la mano y la pantalla (app que muestre input del teclado en tiempo real)
2. Realizar 25 gestos direccionales rápidos
3. Analizar frame por frame para calcular latencia
4. Calcular estadísticas

**Plantilla de Registro:**
```
Gesto #: __
Latencia (ms): __
---
Latencia promedio: __ ms
Latencia mínima: __ ms
Latencia máxima: __ ms
Desviación estándar: __ ms
```

---

### 4.4 Módulo: Detección de Landmarks (Landmark Detection)

#### Prueba LD-01: Tasa de Detección de Manos
**Objetivo:** Evaluar la capacidad de detectar manos en diferentes condiciones

**Procedimiento:**
1. Ejecutar el sistema durante 60 segundos con la mano visible
2. Contar frames totales procesados (asumiendo ~30 fps = ~1800 frames)
3. Contar frames donde se detectó la mano correctamente
4. Calcular tasa de detección

**Plantilla de Registro:**
```
Condición: [IL-X, RV-X, DC-X, AM-X]
Duración: 60s
Frames totales: ~1800
Frames con detección: __
Tasa de detección: __%
Frames con falsos positivos: __
Observaciones: _______________
```

**Repetir con:**
- Todas las condiciones de iluminación (IL-1 a IL-5)
- Diferentes fondos (RV-1 a RV-5)
- Diferentes distancias (DC-1 a DC-4)
- Diferentes ángulos (AM-1 a AM-4)

#### Prueba LD-02: Detección de Múltiples Manos
**Objetivo:** Evaluar la detección simultánea de ambas manos

**Procedimiento:**
1. Mostrar ambas manos en el encuadre
2. Realizar 100 frames de prueba
3. Anotar:
   - Frames donde se detectaron ambas manos
   - Frames donde solo se detectó una mano
   - Frames sin detección
   - Confusiones entre manos (izquierda detectada como derecha o viceversa)

**Plantilla de Registro:**
```
Condición: [IL-X, RV-X]
Frames con ambas manos detectadas: __/100
Frames con solo una mano: __/100
Frames sin detección: __/100
Confusiones izq/der: __
```

#### Prueba LD-03: Detección de Rostro
**Objetivo:** Evaluar la detección de landmarks faciales

**Procedimiento:**
1. Posicionar el rostro frente a la cámara
2. Ejecutar durante 60 segundos
3. Contar frames con detección facial exitosa
4. Evaluar con diferentes orientaciones de cabeza (frontal, 15°, 30°, 45° en todas direcciones)

**Plantilla de Registro:**
```
Condición: [IL-X]
Orientación cabeza: [frontal/15°/30°/45°] [izq/der/arriba/abajo]
Frames con detección: __/~1800
Tasa de detección: __%
```

---

## 5. Pruebas de Integración

### 5.1 Prueba INT-01: Uso Combinado (Mouse + Blink)
**Objetivo:** Evaluar el sistema completo con control de mouse y clics por parpadeo

**Procedimiento:**
1. Configurar:
   - `right_hand_mode` = `"mouse"`
   - `left_blink_mode` = `"left_click"`
   - `right_blink_mode` = `"right_click"`
2. Realizar tarea compleja:
   - Abrir un programa de dibujo
   - Mover cursor a 10 posiciones diferentes
   - En cada posición, realizar clic con parpadeo
   - Dibujar líneas conectando los puntos
3. Medir:
   - Tiempo total de la tarea
   - Número de errores (clics no deseados, movimientos incorrectos)
   - Tasa de éxito general

**Plantilla de Registro:**
```
Tarea: Dibujo de 10 puntos conectados
Tiempo total: __ s
Puntos colocados correctamente: __/10
Clics no deseados: __
Errores de movimiento: __
Tasa de éxito: __%
Observaciones: _______________
```

### 5.2 Prueba INT-02: Uso Combinado (Keyboard + Blink)
**Objetivo:** Evaluar control direccional con teclado y clics

**Procedimiento:**
1. Configurar:
   - `left_hand_mode` = `"keyboard"`
   - Parpadeos configurados para clics
2. Jugar un juego simple (e.g., Snake, Pacman) durante 3 minutos
3. Medir:
   - Puntuación obtenida
   - Número de errores direccionales
   - Percepción subjetiva de fluidez (escala 1-5)

**Plantilla de Registro:**
```
Juego: [nombre]
Duración: 3 min
Puntuación: __
Errores direccionales: __
Fluidez percibida (1-5): __
Observaciones: _______________
```

### 5.3 Prueba INT-03: Cambio Dinámico de Configuración
**Objetivo:** Evaluar la recarga automática de configuración

**Procedimiento:**
1. Iniciar el sistema con configuración base
2. Durante la ejecución, modificar `config.json`:
   - Cambiar `right_hand_mode` de `"mouse"` a `"keyboard"`
   - Cambiar `left_blink_mode` de `"left_click"` a `"right_click"`
3. Observar:
   - Tiempo hasta que los cambios surten efecto
   - Correctitud de los nuevos comportamientos
4. Realizar 20 gestos con la nueva configuración

**Plantilla de Registro:**
```
Cambio realizado: [descripción]
Tiempo hasta efecto: __ s
Gestos correctos con nueva config: __/20
Observaciones: _______________
```

---

## 6. Pruebas de Estrés y Casos Extremos

### 6.1 Prueba EST-01: Condiciones Adversas Combinadas
**Objetivo:** Evaluar rendimiento en el peor escenario posible

**Procedimiento:**
1. Combinar:
   - IL-4 (Contraluz)
   - RV-3 (Fondo con movimiento)
   - VM-3 (Movimientos rápidos)
   - DC-3 (Distancia lejana)
2. Realizar 50 gestos variados
3. Medir tasa de éxito general

**Plantilla de Registro:**
```
Condiciones: IL-4 + RV-3 + VM-3 + DC-3
Gestos totales: 50
Gestos detectados correctamente: __/50
Tasa de éxito: __%
```

### 6.2 Prueba EST-02: Sesión Prolongada
**Objetivo:** Evaluar estabilidad del sistema en uso continuo

**Procedimiento:**
1. Usar el sistema continuamente durante 30 minutos
2. Realizar tareas variadas cada 5 minutos
3. Anotar:
   - Degradación de rendimiento (si existe)
   - Uso de CPU y memoria a lo largo del tiempo
   - Aparición de errores o fallos

**Plantilla de Registro:**
```
Minuto: __
CPU: __%
RAM: __ MB
Tasa de detección: __%
Errores observados: _______________
```

### 6.3 Prueba EST-03: Gestos Ambiguos
**Objetivo:** Evaluar la capacidad de distinguir gestos similares

**Procedimiento:**
1. Realizar gestos intencionalmente ambiguos:
   - Movimiento diagonal (¿arriba-derecha o derecha-arriba?)
   - Movimiento circular (¿qué dirección detecta?)
   - Parpadeo rápido de ambos ojos
2. Anotar cómo el sistema interpreta cada gesto

**Plantilla de Registro:**
```
Gesto ambiguo: [descripción]
Interpretación del sistema: _______________
Consistencia (repite 10 veces, cuenta interpretaciones iguales): __/10
```

---

## 7. Análisis de Resultados

### 7.1 Métricas Consolidadas

Al finalizar todas las pruebas, consolidar los datos en las siguientes tablas:

#### Tabla 1: Precisión por Módulo
| Módulo | Condición Óptima | Precisión (%) | Condición Peor | Precisión (%) |
|--------|------------------|---------------|----------------|---------------|
| Blink Detection - Izq | | | | |
| Blink Detection - Der | | | | |
| Mouse Control | | | | |
| Keyboard Control | | | | |
| Landmark Detection - Manos | | | | |
| Landmark Detection - Rostro | | | | |

#### Tabla 2: Latencia por Módulo
| Módulo | Latencia Promedio (ms) | Latencia Mín (ms) | Latencia Máx (ms) | Desv. Estándar |
|--------|------------------------|-------------------|-------------------|----------------|
| Blink Detection | | | | |
| Mouse Movement | | | | |
| Keyboard Direction | | | | |

#### Tabla 3: Impacto de Variables Ambientales
| Variable | Nivel | Impacto en Precisión (%) | Impacto en Latencia (ms) |
|----------|-------|--------------------------|--------------------------|
| Iluminación | IL-1 (Óptima) | | |
| Iluminación | IL-2 (Baja) | | |
| Iluminación | IL-3 (Alta) | | |
| Iluminación | IL-4 (Contraluz) | | |
| Distancia | DC-1 (Muy cerca) | | |
| Distancia | DC-2 (Óptima) | | |
| Distancia | DC-3 (Lejos) | | |
| Velocidad | VM-1 (Lento) | | |
| Velocidad | VM-2 (Normal) | | |
| Velocidad | VM-3 (Rápido) | | |

### 7.2 Gráficas Recomendadas
1. **Gráfica de barras**: Precisión por módulo en condiciones óptimas vs adversas
2. **Gráfica de línea**: Latencia a lo largo de una sesión prolongada
3. **Diagrama de caja (Box plot)**: Distribución de latencias por módulo
4. **Mapa de calor**: Precisión de detección según iluminación y distancia
5. **Gráfica de dispersión**: Relación entre velocidad de gesto y precisión

### 7.3 Análisis Estadístico
Calcular para cada conjunto de datos:
- **Media aritmética**
- **Mediana**
- **Desviación estándar**
- **Rango (mín-máx)**
- **Percentiles** (25%, 50%, 75%)
- **Intervalo de confianza** (95%)

---

## 8. Formato de Reporte Final

### 8.1 Estructura del Reporte
```
1. Resumen Ejecutivo
   - Métricas clave obtenidas
   - Hallazgos principales
   - Recomendaciones

2. Metodología
   - Configuración del entorno
   - Protocolos aplicados
   - Variables controladas

3. Resultados por Módulo
   - Blink Detection
   - Mouse Control
   - Keyboard Control
   - Landmark Detection

4. Resultados de Integración
   - Pruebas combinadas
   - Uso en escenarios reales

5. Análisis de Condiciones Adversas
   - Impacto de iluminación
   - Impacto de ruido visual
   - Impacto de velocidad
   - Impacto de distancia/ángulo

6. Conclusiones
   - Fortalezas del sistema
   - Debilidades identificadas
   - Condiciones óptimas de uso
   - Limitaciones técnicas

7. Recomendaciones
   - Mejoras sugeridas
   - Optimizaciones de parámetros
   - Casos de uso recomendados

8. Anexos
   - Datos crudos
   - Gráficas adicionales
   - Videos de prueba (si aplican)
```

---

## 9. Plantillas de Registro

### 9.1 Plantilla General de Sesión de Pruebas
```
=================================================
SESIÓN DE PRUEBAS - [MÓDULO]
=================================================
Fecha: ___/___/______
Hora inicio: __:__
Hora fin: __:__
Evaluador: _______________
Versión del sistema: _______________

Configuración del Entorno:
- CPU: _______________
- RAM: _______________
- Cámara: _______________
- Sistema operativo: _______________
- Distancia a cámara: ___ cm
- Iluminación (lux): ___

Configuración del Software:
- left_hand_mode: _______________
- right_hand_mode: _______________
- left_blink_mode: _______________
- right_blink_mode: _______________
- movement_threshold: ___
- smoothing_factor: ___
- ear_threshold: ___

Condiciones de Prueba:
- Iluminación: [IL-__]
- Ruido visual: [RV-__]
- Velocidad: [VM-__]
- Distancia: [DC-__]
- Ángulo: [AM-__]

Resultados:
[Ver secciones específicas por prueba]

Observaciones Generales:
_______________________________________________
_______________________________________________

Problemas Encontrados:
_______________________________________________
_______________________________________________

Conclusiones de la Sesión:
_______________________________________________
_______________________________________________

=================================================
```

### 9.2 Plantilla de Registro Individual de Gesto
```
Gesto #: ____
Tipo: [Parpadeo izq/der | Movimiento mouse | Dirección arriba/abajo/izq/der]
Condiciones: [IL-__, RV-__, VM-__, DC-__, AM-__]
Resultado esperado: _______________
Resultado obtenido: _______________
¿Éxito?: [Sí / No]
Latencia estimada: ___ ms
Observaciones: _______________
```

---

## 10. Calendario Sugerido de Pruebas

### Fase 1: Pruebas de Módulos Individuales (Semana 1)
- **Día 1**: Configuración del entorno + Pruebas BL-01, BL-02, BL-03
- **Día 2**: Pruebas MC-01, MC-02, MC-03
- **Día 3**: Pruebas KC-01, KC-02, KC-03
- **Día 4**: Pruebas LD-01, LD-02, LD-03
- **Día 5**: Análisis preliminar de resultados

### Fase 2: Pruebas de Integración (Semana 2)
- **Día 1**: Pruebas INT-01, INT-02, INT-03
- **Día 2**: Pruebas EST-01, EST-02, EST-03
- **Día 3**: Repetición de pruebas con resultados anómalos
- **Día 4**: Pruebas adicionales en condiciones variables
- **Día 5**: Consolidación de datos

### Fase 3: Análisis y Reporte (Semana 3)
- **Día 1-2**: Procesamiento estadístico de datos
- **Día 3-4**: Creación de gráficas y visualizaciones
- **Día 5**: Redacción del reporte final

---

## 11. Herramientas Auxiliares Recomendadas

### 11.1 Software
- **OBS Studio**: Grabación de pantalla y cámara simultánea
- **VLC Media Player**: Análisis frame por frame de videos
- **Luxómetro digital** (app para smartphone): Medición de iluminación
- **Python script para análisis**: Pandas, Matplotlib, Seaborn para procesar datos
- **KeyCastr** (macOS) o **Carnac** (Windows): Mostrar teclas presionadas en pantalla
- **ScreenMarker**: Dibujar cuadrículas en pantalla para pruebas de precisión

### 11.2 Equipamiento Adicional
- **Trípode** para fijar la cámara
- **Lámpara regulable** para control de iluminación
- **Cronómetro digital** de alta precisión
- **Regla o cinta métrica** para medir distancias

### 11.3 Scripts de Apoyo

#### Script para generar objetivos en pantalla (Python + Tkinter)
```python
# Crear ventana con círculos objetivos para pruebas de precisión
# Guardar en: test_target_generator.py
```

#### Script para medir latencia automáticamente
```python
# Analizar video y calcular diferencia de frames
# Guardar en: latency_analyzer.py
```

---

## 12. Consideraciones Éticas y de Seguridad

### 12.1 Consentimiento
- Si se involucran múltiples evaluadores, obtener consentimiento para uso de datos
- Informar sobre grabaciones de video/imágenes

### 12.2 Privacidad
- No almacenar grabaciones con rostros identificables sin consentimiento
- Anonimizar datos antes de compartir

### 12.3 Salud
- Realizar pausas cada 20-30 minutos para evitar fatiga ocular
- No forzar gestos que causen incomodidad

---

## 13. Contacto y Soporte

Para preguntas sobre el plan de pruebas:
- **Autor**: Omar Luna Hernández
- **Proyecto**: Sistema de Control de Interfaces mediante Gestos Humanos
- **Repositorio**: [Incluir URL si aplica]

---

**Fin del Plan de Pruebas Manuales**
