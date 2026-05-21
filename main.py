import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book():
    print("\n=== Добавление книги ===")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()
    books = load_books()
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print("Такая книга уже есть!")
            return
    rating = int(input("Оценка (1-5): "))
    date_read = input("Дата (ГГГГ-ММ-ДД): ") or datetime.now().strftime("%Y-%m-%d")
    books.append({"author": author, "title": title, "rating": rating, "date_read": date_read})
    save_books(books)
    print("Книга добавлена!")

def show_all_books():
    books = load_books()
    if not books:
        print("Нет книг")
        return
    for i, b in enumerate(books, 1):
        print(f"{i}. {b['author']} - {b['title']} ({b['rating']}/5)")

def show_avg_rating():
    books = load_books()
    if books:
        avg = sum(b["rating"] for b in books) / len(books)
        print(f"Средняя оценка: {avg:.2f}")

def show_author_stats():
    books = load_books()
    stats = {}
    for b in books:
        stats[b["author"]] = stats.get(b["author"], 0) + 1
    for a, c in stats.items():
        print(f"{a}: {c} книг")

def delete_book():
    books = load_books()
    if not books:
        print("Нет книг")
        return
    for i, b in enumerate(books, 1):
        print(f"{i}. {b['author']} - {b['title']}")
    try:
        idx = int(input("Номер для удаления: ")) - 1
        if 0 <= idx < len(books):
            deleted = books.pop(idx)
            save_books(books)
            print(f"Удалена: {deleted['title']}")
    except ValueError:
        print("Введите число")

def main():
    while True:
        print("\n1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        choice = input("Выберите: ")
        if choice == "1": add_book()
        elif choice == "2": show_all_books()
        elif choice == "3": show_avg_rating()
        elif choice == "4": show_author_stats()
        elif choice == "5": delete_book()
        elif choice == "6": break
        else: print("Неверный ввод")

if __name__ == "__main__":
    main()