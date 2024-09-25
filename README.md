# Course Robot

Скрипт автоматически проходит материалы на образовательной платформе. Для каждого аккаунта открывается отдельное окно браузера, которое выполняет действия с материалами (PDF, видео или iframe) и переходит на следующую страницу.

## Установка зависимостей

Для работы скрипта необходимо установить следующие библиотеки:

```bash
python3 -m pip install selenium
```

Также потребуется установить [ChromeDriver](https://sites.google.com/chromium.org/driver/) для взаимодействия с браузером Chrome. Убедитесь, что версия ChromeDriver совпадает с версией вашего браузера Chrome.

## Структура

1. **accounts.csv** — файл с учетными записями в формате:  

   ```csv
   email,password
   ```

2. **INITIAL_URL** — стартовая ссылка на материал платформы.

## Запуск скрипта

1. Поместите учетные данные в файл `accounts.csv`.
2. Запустите скрипт:

   ```bash
   python3 main.py
   ```

3. Скрипт работает параллельно для всех аккаунтов из файла.
