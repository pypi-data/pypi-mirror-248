# Credit scoring package

## Общая информация

Данный проект представляет собой пакет Python, предназначенный для работы с данными, связанный с кампаниями прямого маркетинга (телефонными звонками) португальского банковского учреждения, который может быть использован для изучения структуры ML моделей, задействованных в Production сфере.

## Структура кода 
### Configs

Параметры модели задаются через configs. Конфиги представлены файлами yaml. Ценности для параметров можно установить в файле `credit_scoring_model/config.yml`. Configs анализируются и проверяются в `credit_scoring_model/config/core.py` модуль, использующий библиотеку [StrictYaml](https://github.com/crdoconnor/strictyaml) для разбора и [Pydantic](https://pydantic-docs.helpmanual.io/) для проверки типов значений. 

## Настройка пайплайна и обучение

Pipeline установлен в credit_scoring_model/pipeline.py файл. Обучение проходит в файле `credit_scoring_model/train_pipeline.py`. Все этапы обработки данных выполняются в [Scikit-learn](https://scikit-learn.org/stable/), включая пользовательские преобразования, хранящиеся в файле `credit_scoring_model/processing/features.py`. 


### Как делать прогнозы

Код для предсказания устанавливается из файла `credit_scoring_model/predict.py`. Перед каждым предсказанием производится проверка входных данных. Код для проверки можно найти в файле `credit_scoring_model/processing/validation.py`. 


## Как запустить код 

Код можно запустить с помощью инструмента [Tox](https://pypi.org/project/tox/). Tox — это удобный способ автоматической настройки среды и путей Python и запуска необходимых команд из командной строки. Файл с описанием tox можно найти в файле `tox.ini`. Следующие команды можно запустить из командной строки используя Tox:

* Запустить обучение: сначала создайте каталог для сохранения моделей, если такового нет `mkdir ./credit_scoring_model/trained_models`, а затем запустите `tox -e train`
* Запустить тестирование (через [pytest](https://docs.pytest.org/en/6.2.x/)): `tox -e test_package`
* Запустить проверку типов (через [mypy](https://mypy.readthedocs.io/en/stable/)): `tox -e typechecks`
* Запустить проверку стиля (через [black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort), [mypy](https://mypy.readthedocs.io/en/stable/)
и [flake8](https://pypi.org/project/flake8/)): `tox -e stylechecks`

## Как установить пакет

Для установки пакета запустите 

```
pip install credit-scoring-model
```

После этого вы можете делать прогнозы, используя пакет: 

```
from credit_scoring_model.predict import make_prediction

# Пример входных данных
input_dict = {'ID': [7], 'CRIM': [0.08829], 'ZN': [12.5], 'INDUS': [7.87], 'CHAS': [0.0], 
              'NOX': [0.524], 'RM': [6.012], 'AGE': [66.6], 'DIS': [5.5605], 'RAD': [5.0], 
              'TAX': [311.0], 'PTRATIO': [15.2], 'B': [395.6], 'LSTAT': [12.43]}

result = make_prediction(input_data=input_dict)

print(result)
```
