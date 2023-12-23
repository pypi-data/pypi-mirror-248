from enum import Enum


class DjangoEnum(Enum):
    """Enum class with choices method, which converts all choices into Django format

    Example:
        key = models.CharField(choices=DjangoChoice.choices())
    """

    @classmethod
    def choices(cls):
        choices = []
        for choice in cls:
            choices.append((choice.value, choice.name))
        return choices
