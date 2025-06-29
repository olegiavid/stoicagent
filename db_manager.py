# db_manager.py
import sqlite3

def connect_db(db_file):
    """ Создает подключение к базе данных SQLite """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_tables(conn):
    """ Создает таблицы 'authors' и 'quotes' """
    create_authors_table_sql = """
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """
    
    create_quotes_table_sql = """
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (id)
    );
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(create_authors_table_sql)
        cursor.execute(create_quotes_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def add_quote(conn, author_name, quote_text):
    """ Добавляет нового автора (если его нет) и новую цитату """
    cursor = conn.cursor()
    
    # Сначала ищем автора или добавляем его
    cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
    author = cursor.fetchone()
    
    if author:
        author_id = author[0]
    else:
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid # Получаем id только что вставленной записи
        
    # Теперь добавляем цитату
    cursor.execute("INSERT INTO quotes (author_id, content) VALUES (?, ?)", (author_id, quote_text))
    conn.commit()
    return cursor.lastrowid

def get_all_quotes(conn):
    """ Получает все цитаты с именами их авторов """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.name, q.content 
        FROM quotes q 
        JOIN authors a ON q.author_id = a.id
    """)
    
    return cursor.fetchall()

# Основной блок для демонстрации работы
if __name__ == '__main__':
    db_file = 'dharma_wisdom.db'
    
    # 1. Подключаемся к БД и создаем таблицы
    connection = connect_db(db_file)
    if connection:
        create_tables(connection)
        print("База данных и таблицы успешно созданы/проверены.")
        
        # 2. Добавляем несколько цитат (этот блок можно менять)
        print("\nДобавляем цитаты...")
        # Вы можете заменить эти цитаты на те, что извлекли из "Вопросов Милинды"
        add_quote(connection, 'Нагасена', 'Как из совокупности осей, колес, кузова и дышла возникает название «колесница», так и из совокупности телесных и духовных свойств возникает общеупотребимое название «человек».')
        add_quote(connection, 'Милинда', 'Почтенный Нагасена, что перерождается?')
        add_quote(connection, 'Нагасена', 'Государь, перерождаются имя-и-форма (нама-рупа).')
        print("Цитаты добавлены.")
        
        # 3. Получаем и выводим все цитаты
        print("\n--- Все цитаты в базе ---")
        all_quotes = get_all_quotes(connection)
        for author, content in all_quotes:
            print(f'[{author}]: "{content}"')
            
        # 4. Закрываем соединение
        connection.close()