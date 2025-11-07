import sys
import os
# Добавляем родительскую папку в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_wallet import SmartWallet

def test_wallet_creation():
    """Тест создания кошелька"""
    wallet = SmartWallet("Тест", 1000, 'USD')
    assert wallet.owner == "Тест"
    assert wallet.balance == 1000
    assert wallet.currency == 'USD'

def test_deposit():
    """Тест пополнения счета"""
    wallet = SmartWallet("Тест", 1000, 'USD')
    wallet.deposit(500)
    assert wallet.balance == 1500

def test_withdraw():
    """Тест снятия средств"""
    wallet = SmartWallet("Тест", 1000, 'USD')
    wallet.withdraw(300)
    assert wallet.balance == 700

def test_negative_withdraw():
    """Тест что нельзя снять больше чем есть"""
    wallet = SmartWallet("Тест", 1000, 'USD')
    try:
        wallet.withdraw(1500)
        assert False, "Должна быть ошибка при снятии больше баланса"
    except ValueError as e:
        assert "Недостаточно средств" in str(e)

def test_negative_deposit():
    """Тест что нельзя пополнить отрицательной суммой"""
    wallet = SmartWallet("Тест", 1000, 'USD')
    try:
        wallet.deposit(-100)
        assert False, "Должна быть ошибка при отрицательном депозите"
    except ValueError as e:
        assert "отрицательным" in str(e)

def test_currency_conversion():
    """Тест конвертации валют"""
    wallet = SmartWallet("Тест", 100, 'USD')
    eur_balance = wallet.get_balance_in('EUR')
    # Просто проверяем что конвертация работает (число > 0)
    assert eur_balance > 0