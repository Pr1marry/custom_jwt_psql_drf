# Реализация кастомной аутентификации на основе drf, jwt без использования сторонних библиотек.
### Создал несколько эндпоинтов, из которых ключевые:
##### 1: http://127.0.0.1:8000/api/tokens  Возвращает Access и Refresh токены
##### В теле запроса необходимо передать id пользователя для отображения access и refresh токенов пользователя, refresh token передается на фронт посредством httponly в cookie(исключительно для чтения, без возможности изменения), access в заголовках ответа:

<img width="1029" alt="Снимок экрана 2022-09-21 в 09 26 12" src="https://user-images.githubusercontent.com/104326167/191430552-14d1ac8e-50ab-4d45-9a8f-989ffbb45571.png">
-----------
<img width="1020" alt="Снимок экрана 2022-09-21 в 09 25 48" src="https://user-images.githubusercontent.com/104326167/191431761-e24f97cc-86f8-4b2e-9acc-d8a73b3c4ba3.png">
-----------
<img width="1021" alt="Снимок экрана 2022-09-21 в 09 25 59" src="https://user-images.githubusercontent.com/104326167/191432219-8f6e1629-24a4-4273-859b-77d3b53f30b3.png">

##### 2: http://127.0.0.1:8000/api/refresh_access Генерирует новый Access токен посредством обращения к действующему refresh токену (если refresh валидный)
##### Необходимо чтобы в cookie был сохранен действующий refresh токен

<img width="1027" alt="Снимок экрана 2022-09-21 в 09 46 10" src="https://user-images.githubusercontent.com/104326167/191433482-162224eb-80a4-44b2-a197-19b79758ef8a.png">

##### 3: http://127.0.0.1:8000/api/refresh_all Принудительно обновляет refresh и access токены
##### В теле запроса необходимо передать id пользователя, механизм передачи токенов схожий с пунктом 1
<img width="1025" alt="Снимок экрана 2022-09-21 в 09 50 35" src="https://user-images.githubusercontent.com/104326167/191434355-781c95ad-c552-4564-8daf-fc45e2782a08.png">
