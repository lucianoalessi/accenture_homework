from datetime import datetime
from pydantic import BaseModel

# Definimos una clase que representa una entrada de log del sistema
class LogEntry(BaseModel):
    timestamp: datetime       # Fecha y hora de la medición
    sala: str                 # Sala donde se registró la medición (ej: Sala_1)
    estado: str               # Nivel de severidad del log (ej: "INFO", "WARNING")
    temperatura: float        # Temperatura medida (en grados Celsius)
    humedad: float            # Humedad relativa (%)
    co2: int                  # Concentración de CO2 medida (en ppm)
    mensaje: str              # Descripción del evento (texto libre)

    # Método especial que permite comparar dos objetos LogEntry usando el operador <
    def __lt__(self, other: 'LogEntry'):
        """Permite comparar objetos LogSensor por su timestamp."""
        assert isinstance(other, LogEntry), NotImplemented
        return self.timestamp < other.timestamp


    @staticmethod
    def from_csv_row(row: dict) -> 'LogEntry':
        """Crea una instancia de LogSensor a partir de una fila de CSV."""
        return LogEntry(
            timestamp=datetime.fromisoformat(row['timestamp']),
            sala=row['sala'],
            estado=row['estado'],
            temperatura=float(row['temperatura']),
            humedad=float(row['humedad']),
            co2=int(row['co2']),
            mensaje=row['mensaje']
        )

    # Clase interna de configuración de Pydantic
    class Config:
        frozen = True  # Hace que los objetos sean inmutables
