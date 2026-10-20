# Escenario
Se modela la fila virtual de preventa para fans de Ticketmaster como un sistema M/M/1, donde los fans llegan siguiendo un proceso de Poisson (0.8 por minuto), son atendidos uno a la vez por un único servidor con tiempos de compra exponenciales (1 por minuto) y esperan en orden de llegada hasta completar su compra.

# Reflexion
## ¿Qué ventajas ofrece usar eventos discretos? 
Solo se simulan los momentos en que algo cambia (llegadas y fin de compras), así que es rápido y eficiente. Además permite probar escenarios, como más fans o más servidores, sin tener que hacerlo en la vida real.

## ¿Qué información relevante podemos extraer de un proceso modelado como una fila?
Cuánto tiempo espera un fan en promedio, cuántas personas hay en la fila, qué tan ocupado está el servidor y cuál es la espera máxima. Con eso se puede saber si el sistema aguanta la demanda o si necesita más capacidad.
