# Adaptador (output): genera clientes usando distribución de Poisson para llegadas
# y distribución exponencial para tiempos de servicio

import random
from typing import Tuple, Dict, Any
from ..domain.ports.customer_generator import CustomerGeneratorPort
from ..domain.priority import Priority
from ..domain.transaction_type import TransactionType

# parte-Mauricio
class ConfigurableGenerator(CustomerGeneratorPort):
    """
    Adaptador (output): genera clientes utilizando distribuciones estadísticas configurables.
    Permite simular llegadas usando procesos de Poisson (distribución exponencial de tiempos entre llegadas)
    o intervalos fijos. Además, permite simular la duración de los servicios utilizando distribuciones
    exponenciales, normales o constantes.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Tasa promedio de llegada de clientes por unidad de tiempo (lambda)
        self.arrival_rate = config.get("arrival_rate", 1.0) 
        # Tipo de distribución para las llegadas ('exponential' para procesos de Poisson, o 'fixed' para fijos)
        self.arrival_dist = config.get("arrival_dist", "exponential") 
        
        # Tiempo promedio requerido para atender a un cliente (mu)
        self.service_mean = config.get("service_mean", 5.0) 
        # Tipo de distribución para la duración del servicio ('exponential', 'normal', o 'constant')
        self.service_dist = config.get("service_dist", "exponential") 
        # Desviación estándar utilizada únicamente cuando la distribución del servicio es 'normal'
        self.service_stddev = config.get("service_stddev", 1.0) 
        
        # Probabilidades de asignar cada nivel de prioridad al generar un cliente (Alta, Media, Baja)
        self.priority_weights = config.get("priority_weights", [0.1, 0.3, 0.6]) 

    def get_next_arrival_interval(self) -> float:
        """
        Calcula y devuelve el tiempo que transcurrirá hasta la llegada del próximo cliente.
        Utiliza distribución exponencial si está configurado como Poisson, o tiempos fijos en caso contrario.
        """
        if self.arrival_dist == "exponential":
            # Para llegadas de Poisson, el tiempo entre llegadas sigue una distribución exponencial
            return random.expovariate(self.arrival_rate)
        elif self.arrival_dist == "fixed":
            # Si el tiempo es fijo, es simplemente la inversa de la tasa de llegada
            return 1.0 / self.arrival_rate
        else:
            return random.expovariate(self.arrival_rate)

    def get_service_time(self) -> float:
        """
        Calcula y devuelve la duración del servicio que requerirá un nuevo cliente en la ventanilla.
        Soporta distribuciones exponenciales, normales (con límite inferior > 0) y constantes.
        """
        if self.service_dist == "exponential":
            return random.expovariate(1.0 / self.service_mean)
        elif self.service_dist == "normal":
            time = random.gauss(self.service_mean, self.service_stddev)
            return max(1.0, time) # Asegura que el tiempo de servicio resultante sea siempre positivo
        elif self.service_dist == "constant":
            return self.service_mean
        else:
            return self.service_mean

    def get_next_customer_attributes(self) -> Tuple[int, str]:
        """
        Selecciona aleatoriamente los atributos de un nuevo cliente que acaba de llegar.
        Elige su prioridad basada en los pesos configurados y asigna un tipo de transacción uniforme.
        """
        # Elige la prioridad del cliente según las ponderaciones (pesos) definidas
        prio = random.choices(
            [Priority.HIGH.value, Priority.MEDIUM.value, Priority.LOW.value],
            weights=self.priority_weights,
            k=1
        )[0]
        # Selecciona aleatoriamente un tipo de transacción bancaria
        txn = random.choice(list(TransactionType)).value
        return prio, txn
