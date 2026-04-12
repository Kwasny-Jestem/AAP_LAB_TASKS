# -*- coding: utf-8 -*-
"""Testy pytest dla klasy Product.

Uruchomienie: pytest test_product_pytest.py -v
"""

import pytest
from product import Product


# --- Fixture ---

@pytest.fixture
def product():
    """Tworzy instancje Product do testow (odpowiednik setUp)."""
    return Product("Laptop", 2999.99, 10)


# --- Testy is_available ---

def test_is_available(product):
    """Sprawdz dostepnosc produktu gdy quantity > 0."""
    assert product.is_available() == True


def test_is_not_available_when_empty():
    """Sprawdz, ze produkt z quantity=0 nie jest dostepny."""
    empty = Product("Empty", 10.0, 0)
    assert empty.is_available() == False


# --- Testy total_value ---

def test_total_value(product):
    """Sprawdz wartosc calkowita."""
    assert product.total_value() == pytest.approx(2999.99 * 10)


# --- Testy add_stock z parametryzacja ---

@pytest.mark.parametrize("amount, expected_quantity", [
    (5, 15),
    (0, 10),
    (100, 110),
    (1, 11),
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    """Testuje add_stock z roznymi wartosciami."""
    product.add_stock(amount)
    assert product.quantity == expected_quantity


# --- Testy remove_stock z parametryzacja ---

@pytest.mark.parametrize("amount, expected_quantity", [
    (1, 9),
    (5, 5),
    (10, 0),
])
def test_remove_stock_parametrized(product, amount, expected_quantity):
    """Testuje remove_stock z roznymi wartosciami."""
    product.remove_stock(amount)
    assert product.quantity == expected_quantity


# --- Testy bledow ---

def test_remove_stock_too_much_raises(product):
    """Sprawdz, czy proba usuniecia za duzej ilosci rzuca ValueError."""
    with pytest.raises(ValueError):
        product.remove_stock(100)


def test_add_stock_negative_raises(product):
    """Sprawdz, czy ujemna wartosc w add_stock rzuca ValueError."""
    with pytest.raises(ValueError):
        product.add_stock(-5)


def test_remove_stock_negative_raises(product):
    """Sprawdz, czy ujemna wartosc w remove_stock rzuca ValueError."""
    with pytest.raises(ValueError):
        product.remove_stock(-1)


def test_init_negative_price_raises():
    """Sprawdz, czy ujemna cena przy tworzeniu rzuca ValueError."""
    with pytest.raises(ValueError):
        Product("Bad", -1.0, 5)


# --- Testy apply_discount z parametryzacja ---

@pytest.mark.parametrize("percent, expected_price", [
    (0, 2999.99),
    (50, 2999.99 * 0.5),
    (100, 0.0),
    (10, 2999.99 * 0.9),
    (25, 2999.99 * 0.75),
])
def test_apply_discount_parametrized(product, percent, expected_price):
    """Testuje apply_discount z roznymi wartosciami procentowymi."""
    product.apply_discount(percent)
    assert product.price == pytest.approx(expected_price)


def test_apply_discount_out_of_range_raises(product):
    """Sprawdz, czy procent > 100 rzuca ValueError."""
    with pytest.raises(ValueError):
        product.apply_discount(101)


def test_apply_discount_negative_raises(product):
    """Sprawdz, czy ujemny procent rzuca ValueError."""
    with pytest.raises(ValueError):
        product.apply_discount(-5)
