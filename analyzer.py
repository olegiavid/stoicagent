# analyzer.py
import string
from textblob import TextBlob

def analyze_text(filepath):
    # 1. Чтение файла
    # Конструкция 'with open' гарантирует, что файл будет корректно закрыт.
    # 'encoding="utf-8"' важен для правильной работы с текстом.
    with open(filepath, 'r', encoding='windows-1251') as file:
        text = file.read()

    # 2. Очистка текста
    # Переводим в нижний регистр для унификации ('The' и 'the' - одно слово).
    lower_text = text.lower()
    # Удаляем всю пунктуацию. str.maketrans создает "таблицу замен".
    # Здесь мы заменяем все знаки пунктуации на None (удаляем).
    cleaned_text = lower_text.translate(str.maketrans('', '', string.punctuation))

    # 3. Токенизация (разделение на слова)
    # Метод split() разделяет строку по пробелам на список отдельных слов.
    words = cleaned_text.split()

    # 4. Подсчет частоты слов
    # Используем словарь (dict) для хранения пар "слово: количество".
    word_counts = {}
    for word in words:
        # метод .get(word, 0) безопасно получает значение.
        # Если слова еще нет в словаре, он вернет 0.
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # 5. Сортировка для вывода топ-10 слов
    # sorted() сортирует элементы. Здесь мы сортируем по второму элементу пары (x[1]),
    # то есть по количеству. reverse=True — для сортировки по убыванию.
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # 6. Анализ тональности с помощью TextBlob
    # TextBlob требует оригинальный текст с пунктуацией для лучшего анализа.
    blob = TextBlob(text)
    # .sentiment возвращает два значения:
    # Polarity: [-1.0, 1.0] (отрицательный ... положительный)
    # Subjectivity: [0.0, 1.0] (объективный ... субъективный)
    sentiment = blob.sentiment

    # --- Вывод результатов ---
    print("--- Анализ текста: meditations.txt ---")
    print(f"Всего уникальных слов: {len(word_counts)}")
    print("\nТоп-10 самых частых слов:")
    for word, count in sorted_words[:10]:
        print(f"- {word}: {count}")

    print("\n--- Анализ тональности ---")
    print(f"Полярность: {sentiment.polarity:.4f} (Чем ближе к 1, тем позитивнее)")
    print(f"Субъективность: {sentiment.subjectivity:.4f} (Чем ближе к 1, тем субъективнее)")

if __name__ == '__main__':
    analyze_text('milinda.txt')