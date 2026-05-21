import json
import os
from datetime import datetime

DATA_FILE = "books.json"


def load_books():
    """Загрузка книг из JSON-файла"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_books(books):
    """Сохранение книг в JSON-файл"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def add_book():
    """Добавление новой книги"""
    print("\n=== Добавление книги ===")
    
    author = input("Автор: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым!")
        return
    
    title = input("Название: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым!")
        return
    
    # Проверка на дубликаты
    books = load_books()
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print(f"Ошибка: книга '{title}' автора {author} уже есть в трекере!")
            return
    
    # Ввод и валидация оценки
    while True:
        try:
            rating = int(input("Оценка (от 1 до 5): ").strip())
            if 1 <= rating <= 5:
                break
            else:
                print("Ошибка: оценка должна быть от 1 до 5!")
        except ValueError:
            print("Ошибка: введите целое число от 1 до 5!")
    
    # Ввод даты
    date_read = input("Дата прочтения (ГГГГ-ММ-ДД) или Enter для сегодняшней: ").strip()
    if not date_read:
        date_read = datetime.now().strftime("%Y-%m-%d")
    else:
        # Простая валидация формата даты
        try:
            datetime.strptime(date_read, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты, используется сегодняшняя дата")
            date_read = datetime.now().strftime("%Y-%m-%d")
    
    # Добавление книги
    books.append({
        "author": author,
        "title": title,
        "rating": rating,
        "date_read": date_read
    })
    
    save_books(books)
    print(f"✓ Книга '{title}' успешно добавлена!")


def show_all_books():
    """Показать все книги"""
    books = load_books()
    
    if not books:
        print("\n=== Список книг ===")
        print("Нет добавленных книг.")
        return
    
    print("\n=== Список книг ===")
    for i, book in enumerate(books, 1):
        print(f"\n{i}. {book['author']} - {book['title']}")
        print(f"   Оценка: {book['rating']}/5, Дата: {book['date_read']}")
    
    print(f"\nВсего книг: {len(books)}")


def show_avg_rating():
    """Показать среднюю оценку всех книг"""
    books = load_books()
    
    if not books:
        print("\n=== Средняя оценка ===")
        print("Нет книг для подсчёта средней оценки.")
        return
    
    total = sum(book["rating"] for book in books)
    average = total / len(books)
    
    print("\n=== Средняя оценка ===")
    print(f"Средняя оценка всех книг: {average:.2f}")
    print(f"Всего оценок: {len(books)}")


def show_author_stats():
    """Показать статистику по авторам"""
    books = load_books()
    
    if not books:
        print("\n=== Статистика по авторам ===")
        print("Нет книг для статистики.")
        return
    
    # Подсчёт книг по авторам
    stats = {}
    for book in books:
        author = book["author"]
        stats[author] = stats.get(author, 0) + 1
    
    print("\n=== Статистика по авторам ===")
    for author, count in sorted(stats.items()):
        print(f"{author}: {count} книг(а/и)")


def delete_book():
    """Удаление книги"""
    books = load_books()
    
    if not books:
        print("\n=== Удаление книги ===")
        print("Нет книг для удаления.")
        return
    
    print("\n=== Удаление книги ===")
    print("Список книг:")
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - {book['title']} (оценка: {book['rating']}/5)")
    
    while True:
        try:
            choice = input("\nВведите номер книги для удаления (0 - отмена): ").strip()
            if choice == "0":
                print("Удаление отменено.")
                return
            
            index = int(choice) - 1
            if 0 <= index < len(books):
                removed_book = books.pop(index)
                save_books(books)
                print(f"✓ Книга '{removed_book['title']}' автора {removed_book['author']} удалена!")
                break
            else:
                print(f"Ошибка: введите число от 1 до {len(books)} или 0 для отмены!")
        except ValueError:
            print("Ошибка: введите корректный номер!")


def main():
    """Главное меню приложения"""
    while True:
        print("\n" + "=" * 40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("=" * 40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        print("-" * 40)
        
        choice = input("Выберите пункт меню (1-6): ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_avg_rating()
        elif choice == "4":
            show_author_stats()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("\nДо свидания!")
            break
        else:
            print("Ошибка: введите число от 1 до 6!")


if __name__ == "__main__":
    main() 