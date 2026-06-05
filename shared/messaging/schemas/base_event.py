from datetime import datetime, UTC
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    """
    Базовий клас для всіх подій у системі (Event Bus).
    
    Містить спільні метадані, необхідні для трасування повідомлень, 
    аудиту та синхронізації часу між мікросервісами.
    """

    # Унікальний ідентифікатор події. Використовується для дедуплікації 
    # повідомлень на стороні споживача (Consumer).
    event_id: UUID = Field(default_factory=uuid4)
    
    # Час виникнення події в форматі UTC. 
    # Використання default_factory гарантує створення актуального таймстемпу 
    # в момент створення об'єкта, а не під час ініціалізації модуля.
    occurred_at: datetime = Field(default_factory=lambda : datetime.now(UTC))
    
    # Назва сервісу-відправника. Допомагає визначити джерело події 
    # при аналізі логів або роботі декількох сервісів.
    service: str = "auth"
