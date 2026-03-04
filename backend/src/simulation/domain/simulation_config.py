from dataclasses import dataclass, field
from typing import Dict, Any

# parte-Mauricio
@dataclass
class SimulationConfig:
    """
    Value Object: Agrupa todos los parámetros de entrada necesarios para configurar y lanzar la simulación.
    Define la estructura básica del banco, sus tiempos operativos y el comportamiento estadístico de su entorno.
    """
    num_tellers: int = 3 # Número total de ventanillas físicas disponibles para atender clientes simultáneamente
    
    # Configuración de llegadas: define la tasa (lambda), el modelo probabilístico y el peso de las prioridades de los clientes
    arrival_config: Dict[str, Any] = field(default_factory=lambda: {
        "arrival_rate": 1.0,
        "arrival_dist": "exponential",
        "priority_weights": [0.1, 0.3, 0.6]
    })
    
    # Configuración de servicio: define el tiempo medio en ventanilla (mu), su distribución y desviación estándar
    service_config: Dict[str, Any] = field(default_factory=lambda: {
        "service_mean": 5.0,
        "service_dist": "exponential",
        "service_stddev": 1.0
    })
    
    max_simulation_time: float = 8.0 * 3600 # Horizonte de tiempo límite de la simulación. Por defecto, representa 8 horas de trabajo en segundos
    max_queue_capacity: int = 100 # Capacidad estricta máxima de personas que pueden esperar físicamente en las filas del banco
