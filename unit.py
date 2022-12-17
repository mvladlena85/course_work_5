from __future__ import annotations

import random
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp: float = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        self.stamina -= self.weapon.stamina_per_hit
        weapon_damage = self.weapon.damage*self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            damage = weapon_damage - target_armor
            target.stamina -= target.armor.stamina_per_turn
        else:
            damage = weapon_damage
            target.stamina = 0

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        if damage > 0:
            self.hp -= damage
        return self.hp

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return f"Навык использован."
        else:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит {damage} урона."
        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if random.randint(0, 100) < 10 and not self._is_skill_used:
            self.use_skill(target=target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит Вам {damage} урона."
        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но Ваш(а) {target.armor.name} его останавливает."


