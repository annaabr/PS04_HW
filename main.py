from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def main():
    # Инициализация драйвера Firefox
    driver = webdriver.Firefox()

    try:
        while True:
            # Запрашиваем первоначальный запрос
            query = input("Введите запрос для поиска на Википедии: ")
            driver.get(f"https://ru.wikipedia.org/wiki/{query}")
            time.sleep(2)  # Ждем загрузки страницы

            # Проверка, существует ли статья
            if "в Википедии нет страницы" in driver.page_source:
                print("Статья не найдена. Попробуйте снова.")
                continue

            # Основной цикл для взаимодействия
            while True:
                # Листаем параграфы текущей статьи
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                for i, paragraph in enumerate(paragraphs):
                    print(f"{i + 1}: {paragraph.text}\n")

                # Предлагаем действия
                print("Выберите действие:")
                print("1: Листать параграфы текущей статьи")
                print("2: Перейти на одну из связанных страниц")
                print("3: Выйти из программы")
                action = input("Введите номер действия (1, 2 или 3): ")

                if action == '1':
                    print("Листаем параграфы... (вы можете ввести цифры для просмотра других параграфов)")
                    continue  # Переход к следующему итерации и повторный показ параграфов

                elif action == '2':
                    # Получаем ссылки на связанные страницы
                    links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/wiki/"]')
                    related_links = {link.text: link for link in links if link.text}  # Сохраняем текст ссылки и саму ссылку
                    print("Связанные страницы:")
                    for i, (text, link) in enumerate(related_links.items()):
                        print(f"{i + 1}: {text}")

                    link_choice = int(input("Выберите номер страницы для перехода (или 0 для возврата): ")) - 1
                    if link_choice == -1:
                        continue  # Возврат к выбору действия
                    if 0 <= link_choice < len(related_links):
                        # Переход на выбранную связанную страницу
                        selected_link = list(related_links.values())[link_choice]
                        driver.get(selected_link.get_attribute('href'))
                        time.sleep(2)
                    else:
                        print("Неверный выбор. Пожалуйста, попробуйте снова.")

                elif action == '3':
                    print("Выход из программы.")
                    return  # Завершение программы

                else:
                    print("Неверный выбор. Пожалуйста, попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()