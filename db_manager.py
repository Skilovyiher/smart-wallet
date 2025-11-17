import psycopg2

class DatabaseManager:
    def __init__(self):
        # Настройки для Docker PostgreSQL
        self.connection_params = {
            'host': 'localhost',
            'database': 'postgres',    # база по умолчанию
            'user': 'postgres',        # пользователь по умолчанию  
            'password': 'password',    # пароль из docker run
            'port': 5432
        }
        self._create_database()
        self._create_table()
    
    def _get_connection(self, database='postgres'):
        """Создает соединение с PostgreSQL"""
        params = self.connection_params.copy()
        params['database'] = database
        try:
            return psycopg2.connect(**params)
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            raise
    
    def _create_database(self):
        """Создает базу данных для кошельков"""
        conn = self._get_connection('postgres')  # подключаемся к основной базе
        conn.autocommit = True  # для создания БД нужен autocommit
        cursor = conn.cursor()
        
        try:
            cursor.execute("CREATE DATABASE smart_wallet_db")
            print("✅ База данных smart_wallet_db создана")
        except Exception as e:
            print(f"⚠️ База уже существует: {e}")
        finally:
            conn.close()
    
    def _create_table(self):
        """Создает таблицу в новой базе"""
        conn = self._get_connection('smart_wallet_db')  # подключаемся к нашей БД
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wallets (
                    id SERIAL PRIMARY KEY,
                    owner VARCHAR(100) UNIQUE NOT NULL,
                    balance DECIMAL(15,2) NOT NULL CHECK (balance >= 0),
                    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("✅ Таблица wallets создана")
        except Exception as e:
            print(f"❌ Ошибка создания таблицы: {e}")
        finally:
            conn.close()

    def save_wallet(self, wallet):
        """Сохраняет кошелек в PostgreSQL"""
        conn = self._get_connection('smart_wallet_db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO wallets (owner, balance, currency)
                VALUES (%s, %s, %s)
                ON CONFLICT (owner) 
                DO UPDATE SET balance = EXCLUDED.balance, currency = EXCLUDED.currency
            ''', (wallet.owner, wallet.balance, wallet.currency))
            
            conn.commit()
            print(f"✅ Кошелек {wallet.owner} сохранен в PostgreSQL")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            conn.rollback()
        finally:
            conn.close()

    def load_wallet(self, owner):
        """Загружает кошелек из PostgreSQL"""
        conn = self._get_connection('smart_wallet_db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT owner, balance, currency FROM wallets WHERE owner = %s', 
                (owner,)
            )
            row = cursor.fetchone()
            
            if row:
                return {'owner': row[0], 'balance': float(row[1]), 'currency': row[2]}
            return None
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return None
        finally:
            conn.close()