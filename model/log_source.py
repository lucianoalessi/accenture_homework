from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .log_entry import LogEntry
import logging

# Interfaz base para fuentes de logs
class LogSource(ABC):
    @abstractmethod
    def read_logs(self) -> List[LogEntry]:
        pass

# Implementación simulada: fuente CSV en memoria
class InMemoryCSVLogSource(LogSource):
    REQUIRED_FIELDS = {'timestamp', 'sala', 'estado', 'temperatura', 'humedad', 'co2', 'mensaje'}

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    def read_logs(self) -> List[LogEntry]:
        logs = []
        for row in self.data:
            if not self.REQUIRED_FIELDS.issubset(row.keys()):
                logging.warning(f"Registro mal formado descartado: {row}")
                continue
            try:
                log = LogEntry.from_csv_row(row)
                logs.append(log)
            except Exception as e:
                logging.warning(f"Error al parsear registro: {row} - {e}")
        return logs

# Factory para fuentes de logs
class LogSourceFactory:
    @staticmethod
    def create(source_type: str, data: Any) -> LogSource:
        if source_type == "inmemory_csv":
            return InMemoryCSVLogSource(data)
        # Aquí se pueden agregar más fuentes en el futuro
        raise ValueError(f"Tipo de fuente no soportado: {source_type}")
