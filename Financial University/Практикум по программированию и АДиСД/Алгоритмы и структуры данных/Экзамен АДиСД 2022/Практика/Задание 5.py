from collections import namedtuple

Route = namedtuple('Route', ('Place_of_departure', 'Place_of_arrival'))


class Plane(object):
    """5.	Создать класс Plane (самолетов), имеющий атрибуты: название самолета, количество пассажиров на борту,
    курс движения (откуда и куда). Методы: - определить загрузку самолета, если максимальная вместимость =200
    пассажиров; – определить все имена самолетов,
    летящих по одному маршруту; - определить среднюю загрузку всех самолетов. """

    __max_capacity = 200

    def __init__(self, name: str, passengers_number: int, route: Route):
        self.name = name
        self.passengers_number = passengers_number
        self.route = route

    def check_capacity(self): return 'Overload' if self.passengers_number > self.__max_capacity else 'Normal capacity'

    @staticmethod
    def check_routes(planes):
        same_routes = {}
        for plane in planes:
            if plane.route not in same_routes.keys():
                same_routes.setdefault(plane.route, [plane.name])
            else:
                same_routes[plane.route].append(plane.name)
        return same_routes


class Airport:
    @staticmethod
    def check_routes(__planes):
        same_routes = {}
        for __plane in __planes:
            if __plane.route not in same_routes.keys():
                same_routes.setdefault(__plane.route, [__plane.name])
            else:
                same_routes[__plane.route].append(__plane.name)
        return same_routes

    @staticmethod
    def check_average_load(__planes):
        avg = 0
        for __plane in __planes:
            avg += __plane.passengers_number
        return avg / len(__planes)


Airbus_310 = Plane('Airbus', 136, Route('Moscow', 'Berlin'))
Boeing_15 = Plane('Boeing', 154, Route('Moscow', 'Saint-Petersburg'))
IL_96 = Plane('Ilyushin', 112, Route('Moscow', 'Berlin'))
Planes = (Airbus_310, Boeing_15, IL_96)
print(Airport.check_routes(Planes))
print(Airport.check_average_load(Planes))
