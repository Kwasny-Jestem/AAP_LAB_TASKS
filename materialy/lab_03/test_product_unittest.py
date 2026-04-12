# -*- coding: utf-8 -*-
"""Testy unittest dla klasy Product.

Uruchomienie: python -m unittest test_product_unittest -v
"""

import unittest
from product import Product


class TestProduct(unittest.TestCase):

    def setUp(self):
        """Przygotuj instancje Product do testow."""
        self.product = Product("Laptop", 2999.99, 10)

    # --- Testy __init__ / walidacja ---

    def test_init_negative_price_raises(self):
        """Sprawdz, czy ujemna cena przy tworzeniu rzuca ValueError."""
        with self.assertRaises(ValueError):
            Product("Bad", -1.0, 5)

    def test_init_negative_quantity_raises(self):
        """Sprawdz, czy ujemna ilosc przy tworzeniu rzuca ValueError."""
        with self.assertRaises(ValueError):
            Product("Bad", 10.0, -1)

    # --- Testy add_stock ---

    def test_add_stock_positive(self):
        """Sprawdz, czy dodanie towaru zwieksza quantity."""
        self.product.add_stock(5)
        self.assertEqual(self.product.quantity, 15)

    def test_add_stock_zero(self):
        """Sprawdz, czy dodanie 0 nie zmienia quantity."""
        self.product.add_stock(0)
        self.assertEqual(self.product.quantity, 10)

    def test_add_stock_negative_raises(self):
        """Sprawdz, czy ujemna wartosc rzuca ValueError."""
        with self.assertRaises(ValueError):
            self.product.add_stock(-3)

    # --- Testy remove_stock ---

    def test_remove_stock_positive(self):
        """Sprawdz, czy usuniecie towaru zmniejsza quantity."""
        self.product.remove_stock(4)
        self.assertEqual(self.product.quantity, 6)

    def test_remove_stock_all(self):
        """Sprawdz, czy mozna usunac caly stan magazynowy."""
        self.product.remove_stock(10)
        self.assertEqual(self.product.quantity, 0)

    def test_remove_stock_too_much_raises(self):
        """Sprawdz, czy proba usuniecia wiecej niz jest dostepne rzuca ValueError."""
        with self.assertRaises(ValueError):
            self.product.remove_stock(100)

    def test_remove_stock_negative_raises(self):
        """Sprawdz, czy ujemna wartosc rzuca ValueError."""
        with self.assertRaises(ValueError):
            self.product.remove_stock(-1)

    # --- Testy is_available ---

    def test_is_available_when_in_stock(self):
        """Sprawdz, czy produkt z quantity > 0 jest dostepny."""
        self.assertTrue(self.product.is_available())

    def test_is_not_available_when_empty(self):
        """Sprawdz, czy produkt z quantity == 0 nie jest dostepny."""
        empty_product = Product("Empty", 10.0, 0)
        self.assertFalse(empty_product.is_available())

    # --- Testy total_value ---

    def test_total_value(self):
        """Sprawdz, czy total_value zwraca price * quantity."""
        self.assertAlmostEqual(self.product.total_value(), 2999.99 * 10)

    def test_total_value_empty_stock(self):
        """Sprawdz, czy total_value dla quantity=0 zwraca 0."""
        empty = Product("Empty", 50.0, 0)
        self.assertEqual(empty.total_value(), 0.0)

    # --- Testy apply_discount ---

    def test_apply_discount_50_percent(self):
        """Sprawdz, czy znizka 50% obniza cene o polowe."""
        self.product.apply_discount(50)
        self.assertAlmostEqual(self.product.price, 2999.99 * 0.5)

    def test_apply_discount_0_percent(self):
        """Sprawdz, czy znizka 0% nie zmienia ceny."""
        self.product.apply_discount(0)
        self.assertAlmostEqual(self.product.price, 2999.99)

    def test_apply_discount_100_percent(self):
        """Sprawdz, czy znizka 100% daje cene 0."""
        self.product.apply_discount(100)
        self.assertAlmostEqual(self.product.price, 0.0)

    def test_apply_discount_out_of_range_raises(self):
        """Sprawdz, czy procent poza zakresem 0-100 rzuca ValueError."""
        with self.assertRaises(ValueError):
            self.product.apply_discount(101)

    def test_apply_discount_negative_raises(self):
        """Sprawdz, czy ujemny procent rzuca ValueError."""
        with self.assertRaises(ValueError):
            self.product.apply_discount(-10)


if __name__ == "__main__":
    unittest.main()
