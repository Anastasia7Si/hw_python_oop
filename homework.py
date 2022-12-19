from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MSG: str = ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.MSG.format(self.training_type,
                               self.duration,
                               self.distance,
                               self.speed,
                               self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_WEIGHT_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KMH_IN_MSEC: float = 0.278
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight)
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_WEIGHT_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration)


TYPES_WORKOUT: dict[str, Training] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}


def read_package(workout_type: str, data: dict[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TYPES_WORKOUT:
        raise ValueError(f'Код тренировки {workout_type} не опознан')
    return TYPES_WORKOUT[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
