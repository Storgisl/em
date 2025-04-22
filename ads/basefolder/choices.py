from enum import Enum

class CategoryChoices(Enum):
    ELECTRONICS = "Электроника"
    CLOTHING = "Одежда"
    HOME = "Товары для дома"
    BEAUTY = "Красота и здоровье"
    BOOKS = "Книги"
    TOYS = "Игрушки"
    SPORTS = "Спорт и отдых"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

class ConditionChoices(Enum):
    NEW = "Новый"
    WARNED = "Поношенный"
    FORMERLY_USED = "Б/У"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

class StatusChoices(Enum):
    AWAITING = "Ожидает"
    ACCEPTED = "Принят"
    CANCELED = "Отклонен"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]
