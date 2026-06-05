from pydantic import BaseModel

class RabbitMQTopology(BaseModel):
    """
    Опис топології RabbitMQ для системи.
    Містить назви обмінників (exchanges), черг (queues) та ключів маршрутизації (routing keys),
    що використовуються для синхронізації даних між сервісами.
    """

    # Назва головного обмінника подій. Використовується для публікації всіх подій додатку.
    exchange_name: str = "app.events"
    
    # Тип 'topic' дозволяє консюмерам підписуватися на певні шаблони повідомлень
    # (наприклад, 'auth.*' або '#.registered')
    exchange_type: str = "topic"
    taskiq_exchange_name: str = "taskiq.events"
    taskiq_exchange_type: str = "topic"
    # --- Список черг (Queues) ---

    # Черга, яку слухає сервіс сповіщень для відправки електронних листів
    email_notifications_queue: str = "auth.notifications.email"

    # --- Ключі маршрутизації (Routing keys) ---

    # Публікується, коли користувач ініціює процедуру скидання пароля
    rk_password_reset: str = "auth.password.reset"
    
    # Публікується після успішної реєстрації нового користувача в системі
    rk_user_registered: str = "auth.user.registered"

    chat_access_queue: str = "chat_access_queue"
    # TaskIQ використовує імʼя черги як routing key за замовчуванням
    # тому для AioPikaBroker вказуємо окрему чергу для задач
    taskiq_queue: str = "auth.taskiq.tasks"


# Створюємо єдиний об'єкт конфігурації (Singleton) для використання в коді
rabbit_topology = RabbitMQTopology()
