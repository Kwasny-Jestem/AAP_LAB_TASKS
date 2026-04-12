# -*- coding: utf-8 -*-
"""Klasa Product -- zadanie do samodzielnego wykonania."""


class Product:
    """Reprezentuje produkt w sklepie internetowym."""

    def __init__(self, name: str, price: float, quantity: int):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_stock(self, amount: int):
        """Dodaje okreslona ilosc produktow do magazynu.

        Raises:
            ValueError: jesli amount jest ujemne
        """
        if amount < 0:
            raise ValueError("Amount to add cannot be negative")
        self.quantity += amount

    def remove_stock(self, amount: int):
        """Usuwa okreslona ilosc produktow z magazynu.

        Raises:
            ValueError: jesli amount jest ujemne lub wieksze niz dostepna ilosc
        """
        if amount < 0:
            raise ValueError("Amount to remove cannot be negative")
        if amount > self.quantity:
            raise ValueError("Cannot remove more than available stock")
        self.quantity -= amount

    def is_available(self) -> bool:
        """Zwraca True jesli produkt jest dostepny (quantity > 0)."""
        return self.quantity > 0

    def total_value(self) -> float:
        """Zwraca calkowita wartosc produktow w magazynie (price * quantity)."""
        return self.price * self.quantity

    def apply_discount(self, percent: float):
        """Obniza cene o podany procent (0-100).

        Raises:
            ValueError: jesli percent nie jest w zakresie 0-100
        """
        if percent < 0 or percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        self.price = self.price * (1 - percent / 100)
