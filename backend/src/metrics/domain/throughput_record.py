# Value Object: registro de throughput por intervalo de tiempo
# Contiene: timestamp, customers_served, customers_rejected
from dataclasses import dataclass

@dataclass
class ThroughputRecord:
    """
    parte-Jhonny:
    Registra cuántos clientes fueron atendidos y cuántos abandonaron
    hasta un punto en el tiempo (timestamp). Sirve para graficar
    o entender la eficiencia a lo largo del tiempo de simulación.
    """
    timestamp: float
    customers_served: int
    customers_rejected: int
