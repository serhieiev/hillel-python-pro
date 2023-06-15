# lesson_01: Unix CLI utils

## Home assignment

Ваш викладач випивши пляшку рому, вирішив написати калькулятор у зворотній польскій нотації. В нього щось вийшло, але ніхто не знає що.

Необхідно:

1. Покрити unit тестами усі функції у файлі.
2. Покрити програму интеграційними тестами

Acceptance criteria:

1. Завантажити код тестів на github.
2. Завантажити на github файл с тест репортом.
3. Завантажити на github файл з coverage репортом.

УСІ ВИЩЕЗГАДАНІ ПУНКТИ – ОБОВʼЯЗКОВІ. Невиконання будь-якого з них - 10 балів.

## Solution

To run the `test_drunk_polish_calculator.py` test file with pytest. The `-vv` flag is used to increase verbosity, providing more detailed output about each individual test case:

```bash
pytest -vv test_drunk_polish_calculator.py
```

To generate an HTML report of the test results. The `--html=report.html` option specifies that the output should be saved to `report.html`. The `--self-contained-html` option ensures that all resources (such as CSS and JS) are embedded in the single HTML file, making it easy to share or archive.

```bash
pytest --html=report.html --self-contained-html
```

To generate a coverage report in HTML format. The --cov-report=html:coverage_report option specifies that the coverage report should be output as an HTML file in the coverage_report directory. The --cov=. option tells pytest to measure coverage for the current directory.

```bash
pytest --cov-report=html:coverage_report --cov=.
```