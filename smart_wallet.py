import requests
from db_manager import DatabaseManager

class CurrencyConverter():
    
    def __init__(self):
        self.rates = self._get_rates()
    
    def _get_rates(self):
        
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
            data = response.json()
            return data['rates']
        except:
            return {'USD': 1.0, 'EUR': 0.85, 'RUB': 75.0, 'GBP': 0.75}
        
    def convert(self, amount, from_currency, to_currency):
        
        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]

        usd_amout = amount / from_rate
        target_amount = usd_amout * to_rate

        return  target_amount


class SmartWallet():

    def __init__(self, owner, balance=0, currency='USD'):
        self.owner = owner
        self.__balance = balance
        self.currency = currency
        self._transaction_history = []
        self.converter = CurrencyConverter()
        self.db = DatabaseManager()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Депозит не должен быть отрицательным!")
        self.__balance += amount
        self._transaction_history.append(f'Поплнение на {amount}')

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")
        if amount > self.__balance:
            raise ValueError("Недостаточно средств!")
        self.__balance -= amount
        self._transaction_history.append(f'Снятие - {amount}')
    
    def transfer(self, other_wallet, amount):
        if not isinstance(other_wallet, SmartWallet):
            raise ValueError('Введите корректный кошелёк!')
        self.withdraw(amount)
        other_wallet.deposit(amount)
        self._transaction_history.append(f'Перевод - {amount}')

    def get_balance_in(self, target_currency):
        return self.converter.convert(self.__balance, self.currency, target_currency)


    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, balance):
        if 0 > balance:
            raise ValueError('Баланс не может быть отрицательным!')
        self.__balance = balance

    def save(self):
        """Сохраняет кошелёк в базу данных"""
        self.db.save_wallet(self)

    @classmethod
    def load(cls, owner):
        """Загружает кошелек из базы данных по имени владельца"""
        db = DatabaseManager()
        wallet_data = db.load_wallet(owner)
        
        if wallet_data:
            # PostgreSQL возвращает словарь {'owner': 'name', 'balance': 100, 'currency': 'USD'}
            return cls(
                wallet_data['owner'],
                wallet_data['balance'],
                wallet_data['currency']
            )
        return None

    
if __name__ == "__main__":
    # Добавь в конец smart_wallet.py (в if __name__ == "__main__")
    print("\n=== Тест PostgreSQL ===")
    pg_wallet = SmartWallet("DockerUser", 3000, 'GBP')
    pg_wallet.save()

    loaded_pg = SmartWallet.load("DockerUser")
    if loaded_pg:
        print(f"✅ Из PostgreSQL: {loaded_pg.owner}, баланс: {loaded_pg.balance}")
