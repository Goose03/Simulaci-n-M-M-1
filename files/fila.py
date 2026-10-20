import simpy
import random
import statistics

SEMILLA = 42
TASA_LLEGADA = 0.8
TASA_SERVICIO = 1.0
TIEMPO_SIMULACION = 10000

tiempos_espera = []
tiempos_sistema = []
muestras_cola = []
tiempo_ocupado = 0.0


# Registra periodicamente cuantos fans hay esperando en la fila virtual.
def monitor_cola(env, servidor):
    while True:
        muestras_cola.append(len(servidor.queue))
        yield env.timeout(1)


# Simula a un fan que entra a la fila virtual, espera su turno y completa su compra.
def fan(env, nombre, servidor):
    global tiempo_ocupado
    llegada = env.now
    with servidor.request() as turno:
        yield turno
        espera = env.now - llegada
        tiempos_espera.append(espera)
        duracion = random.expovariate(TASA_SERVICIO)
        yield env.timeout(duracion)
        tiempo_ocupado += duracion
        tiempos_sistema.append(env.now - llegada)


# Genera llegadas de fans con tiempos entre llegadas exponenciales (proceso de Poisson).
def generador_fans(env, servidor):
    i = 0
    while True:
        yield env.timeout(random.expovariate(TASA_LLEGADA))
        i += 1
        env.process(fan(env, f"Fan {i}", servidor))


# Calcula las metricas teoricas de una fila M/M/1 para compararlas con la simulacion.
def metricas_teoricas(lam, mu):
    rho = lam / mu
    return {
        "rho": rho,
        "L": rho / (1 - rho),
        "Lq": rho ** 2 / (1 - rho),
        "W": 1 / (mu - lam),
        "Wq": rho / (mu - lam),
    }


# Ejecuta la simulacion completa y muestra los resultados simulados contra los teoricos.
def main():
    random.seed(SEMILLA)
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacity=1)
    env.process(generador_fans(env, servidor))
    env.process(monitor_cola(env, servidor))
    env.run(until=TIEMPO_SIMULACION)

    teoricas = metricas_teoricas(TASA_LLEGADA, TASA_SERVICIO)

    print("=== Fila virtual de preventa para fans (M/M/1) ===")
    print(f"Fans atendidos: {len(tiempos_sistema)}")
    print(f"{'Metrica':<35}{'Simulado':>12}{'Teorico':>12}")
    print(f"{'Utilizacion (rho)':<35}{tiempo_ocupado / TIEMPO_SIMULACION:>12.3f}{teoricas['rho']:>12.3f}")
    print(f"{'Tiempo promedio en cola (Wq)':<35}{statistics.mean(tiempos_espera):>12.3f}{teoricas['Wq']:>12.3f}")
    print(f"{'Tiempo promedio en sistema (W)':<35}{statistics.mean(tiempos_sistema):>12.3f}{teoricas['W']:>12.3f}")
    print(f"{'Fans promedio en cola (Lq)':<35}{statistics.mean(muestras_cola):>12.3f}{teoricas['Lq']:>12.3f}")
    print(f"{'Espera maxima':<35}{max(tiempos_espera):>12.3f}{'-':>12}")


if __name__ == "__main__":
    main()