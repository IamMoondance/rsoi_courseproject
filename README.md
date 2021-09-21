# Template for KP RSOI

## Требования к программной реализации

1. В соответствии с вариантом задания реализовать систему, состоящую из нескольких взаимодействующих друг с другом сервисов. 
 Каждый сервис реализует свою функциональность и взаимодействует с другими сервисами по протоколу HTTP (придерживаться нотации RESTful), либо через очередь. 
 Также для межсервисного взаимодействия допускается использовать другие протоколы, например gRPC.
 
1. Каждый сервис имеет свое собственное хранилище, если оно ему нужно.
 
1. Выделить отдельный сервис Авторизации (Session Service), который хранит в себе информацию о пользователях и
 используется для пользовательской авторизации и аутентификации.
 
1. Для авторизация пользователь отправляет login + password, в ответ получает JWT токен. Токен выдает Session Service,
 валидация токена выполняется так же на Session Service. Пароли хранить в базе в хэшированном виде. 
 
1. Также выделить Gateway Service, который будет единой точкой входа в систему. Все запросы, кроме авторизации пользователя,
 проходят через него. 
 
1. Валидацию пользовательского JWT-токена также выполняет сервис Gateway. 
 
1. Т.к. компоненты системы смотрят в интернет, реализовать межсервисную авторизацию. Пример:
    * если сервису A требуется сделать запрос к сервису B, то он должен получить для этого токен; 
    * сервис A имеет некоторые clientId / clientSecret, которые он передает как basic-авторизацию в сервис B и 
      сервис B возвращает в ответ подписанный JWT-токен;
    * система A сохраняет этот токен у себя и все следующие запросы выполняет с ним;
    * токен имеет время жизни, если время жизни у него закончилось, то сервис B вернет HTTP 403:Forbidden ошибку, 
      значит сервису A нужно повторно получить токен у системы B и повторить запрос с новым токеном; 
    * в межсервисной авторизации участвуют только системы A и B, Session Service не задействован.

1. Реализовать пользовательский интерфейс HTML+CSS, желательно SPA (react, angular, vue) или мобильный клиент.
 Использование CSS обязательно. 
 
1. Запросы от UI могут быть к только к сервису Gateway либо Session Service для получения токена. 
 
1. Реализовать валидацию входных данных как на front-end’е, так и на back-end’е. 
 
1. Реализовать ролевую модель, создать минимум одного пользователя с ролью Admin и одного пользователя с ролью User. 
 
1. Выделить сервис статистики, туда отправлять через очередь статистику по операциям. В зависимости от задания
 по пришедшим данным строить отчет, доступ к которому должен быть только у пользователя с ролью Admin. 
 
1. Предусмотреть ситуацию недоступности систем, обработку таймаутов и ошибок сервисов. В случае ошибки/недоступности
 некритичного функционала выполнять деградацию функциональности. 
 
1. Весь код хранить на GitHub, автоматизировать процесс сборки, тестирования и релиза на внешней платформе.
 Для CI/CD использовать Github Actions. 
 
1. Каждому сервису поставить в соответствие доменное имя (возможно 3 или 4 уровня), главная страница должна открываться
 по основному имени. Например:
    * UI: aero-ticket.ru
    * Gateway: gw.air-ticket.ru
    * Airport Service: airport.air-ticket.ru 
    * Flight Service: flight.air-ticket.ru
    * Ticket Service: ticket.air-ticket.ru
    * Miles Service: miles.air-ticket.ru

## Требования к Техническому Заданию

Техническое задание является основополагающим документом, по которому ведётся разработка и приёмка работы.
Поэтому ТЗ должно быть максимально четким и полным, не допускать двусмысленную трактовку фраз. Любой невыполненный функционал,
описанный в ТЗ, приводит к автоматическому снижению оценки. Следовательно, в ТЗ описываются:
* все требования к курсовой работе;ваш вариант задания (если взят предложенный вариант) или функционал вашей системы,
согласованный с преподавателем;
* любой дополнительный и не противоречащий п. 1. и 2. функционал, который Вы уверены на 200%, что реализуете.

Лучше реализовать больше, чем указано в ТЗ, чем наоборот.

### Пример

_Неправильное ТЗ_: "Реализовать систему управления полётами".

_Правильное ТЗ (задание 2019-2020 уч. года)_: "Разработать прототип системы поиска объектов туризма и отдыха на базе веб-интерфейса.
Система должна состоять из микросервисов, каждый из которых отвечает за свою задачу: сервис пользовательского интерфейса;
сервис авторизации и данных пользовательских аккаунтов; сервис объектов туризма и отдыха; сервис тегов; сервис статистики;
сервис агрегирования запросов и предоставления ограниченного функционала для сторонних приложений.
Каждый сервис при необходимости может иметь доступ к связанной с ним базе данных, но не должен иметь доступа
к базам данных других сервисов. Все запросы между сервисами требуют авторизацию. Запросы пользователей делятся на две категории:
запросы, требующие авторизации пользователя, и запросы, доступные для всех пользователей, даже неавторизованных.
Все ошибки должны обрабатываться; в случае недоступности некритичного функционала должна осуществляться деградация функциональности.
Все действия на сервисах должны логироваться. Все сервисы должны собираться и разворачиваться через CI/CD."

## Требования к Расчетно-Пояснительной Записке

Расчетно-пояснительная записка является документом, описывающим как работает ваша система. Написать ее надо так,
как будто вы получаете на поддержку незнакомую систему. Другими словами, любое архитектурное решение, костыль,
нетривиальная оптимизация должна иметь пояснение почему сделано именно так.

РПЗ должна состоять из трех частей:

1. **Аналитический раздел.** В данном разделе приводится обзор существующих систем описываются основные требования, к системе.
 Здесь же формулируется бизнес-логика будущей системы.
1. **Конструкторский раздел.** Описание архитектуры и алгоритмов, используемых в системе. Если алгоритм стандартный –
 достаточно поставить ссылку на него. В этом разделе приводится общая схема системы и описание каждого компонента в отдельности.
 Обязательно описать выделенные сущности, чем они характеризуются, дать описание ролевой модели,
 описать схему взаимодействия систем с помощью Диаграммы последовательности действий.
1. **Технологический раздел.** В данном разделе приводится описание типов и структур данных (структура БД),
 а также описываются нюансы реализации. Здесь же надо описать как выполняется сборка и деплой системы.
 Выбор языка (если это С#/Java/Python/Go) писать не надо, это информация не несет никакого смысла.
 Здесь описывается тестирование системы и ее поведение в случае отказа компонентов, ее составляющих.

Записка должна быть оформлена по ГОСТ 7.32-2017. В конце обязательно привести список литературы.

ТЗ, написанное в рамках лабораторных работ по курсу Технология программирования, не является РПЗ.
Из ТЗ можно использовать формальную постановку задачи и требования к системе, их привести в Аналитическом разделе.

## Критерии оценки

Для допуска к защите курсового проекта требуется:
* законченная рабочая программная реализация с выполнением всех пунктов задания;
* согласованные ТЗ и РПЗ;
* код хранящийся на GitHub в групповом репозитории;
* пройденные интеграционные тесты;
* на оценку "удовлетворительно" развернутые сервисы на Heroku либо подобной платформе;
* на оценку "отлично" развернутые сервисы в management Kubernetes Cluster (Google K8S cluster, DO, AWS и т.п.).

В Электронном Университете предусмотрены модули по выполнению курсового проекта. Требования для сдачи каждого модуля:
* 1 модуль (3 неделя) – выбрана и согласована тема курсового проекта (если она не совпадает с вариантом);
* 2 модуль (9 неделя) – согласованное ТЗ и аналитический раздел РПЗ;
* 3 модуль (12 неделя) – прототип курсовой (выполнено 50% требований к функционалу) и конструкторский раздел РПЗ;
* 4 модуль (15 неделя) – сдача курсового проекта (программа и РПЗ).

## Задания по вариантам
Вариант задания берется по номеру студента на начало семестра из ЭУ и фиксируется.

Общие методы для всех вариантов заданий

1. Авторизация.
```
header: Authorization: basic(<login>:<password>)
POST /auth -> JWT token
```
1. Проверка токена пользователя.
```
header: Authorization: bearer <jwt>
POST /verify
```
1. Список всех пользователей. [A][G]
```
GET /users
```
1. Добавление нового пользователя. [A][G]
```
POST /users
body: { login, password }
```

Пояснение:
* [S] – требуют авторизации;
* [G] – запрос проходит через Gateway Service.
* [A] – требуют авторизации и прав администратора;
* [M] – операция модификации.

В блоке Структура данных описаны примерные связи между сервисами и сущностями, это не описание ER-диаграммы и не схема базы данных.

## Вариант 1: Flight Booking System
Система предоставляет пользователю возможность поиска и покупки билетов. В зависимости от количества выполненных перелетов,
пользователю предоставляется скидка на перелет и начисляются баллы, которые он может использовать для оплаты.

**Бизнес сервисы:**
* Аэропорты (Airport Service)
* Система покупки билетов (Ticket Service)
* Рейсы (Flight Service)
* Бонусная система (Bonus (Miles) Service)

**Дополнительные сервисы:**
* Gateway
* Авторизация (Session Service)
* Админка (Report Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**Ticket (Ticket Service):**
```
+ ticket_uid
+ flight_uid -> FK to Flight Service (Flight::flight_uid)
+ user_uid -> FK to Session Service (User::user_uid)
```

**Flight (Flight Service):**
```
+ from_airport_uid FK to Airport Service (Airport::airport_uid)
+ to_airport_uid FK to Airport Service (Airport::airport_uid)
+ date
```

**Airport (Airport Service):**
```
+ name
+ airport_uid
```

**Miles (Bonus Service):**
```
+ user_uid -> FK to Session Service (User::user_uid)
+ balance 
```

### Основные операции

Специфические для варианта задания:

1. Список рейсов. [G]
    ```
    GET /tickets
    ```
1. Список аэропортов. [G]
    ```
    GET /airports
    ```
1. Информация об аэропорте. [G]
    ```
    GET /airports/{airportUid}
    ```
1. Купить билет. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /tickets
    body: { flightUid, date }
    ```
1. Вернуть билет. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /tickets/{ticketUid}
    ```
1. Информация по билету. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /tickets/{ticketUid}
    ```
1. Посмотреть баланс бонусной программы. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /miles
    ```
1. Посмотреть мои билеты. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /tickets
    ```
1. Добавить рейс. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /flights
    body: { airportTo, airportFrom }
    ```
1. Изменить информацию о рейсе. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    PATCH /flights/{flightUid}
    body: { airportTo, airportFrom }
    ```
1. Посмотреть статистику полетов по пользователям: при покупке билета данные отправляются в статистику. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/flights
    ```
1. Посмотреть статистику наполнения рейсов: сколько мест занято на рейсах, общее количество мест к количеству купленных билетов. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/flights-filling
    ```

## Вариант 2: Hotels Booking System

Система предоставляет пользователю сервис поиска и бронирования отелей на интересующие даты. В зависимости
от количества заказов система лояльности дает скидку пользователю на новые бронирования.

**Бизнес сервисы:**

* Гостиницы (Hotel Service)
*Система бронирования (Booking Service)
* Платежная система (Payment Service)
* Система лояльности (Loyalty Service)

**Дополнительные сервисы:**

* Gateway
* Авторизация (Session Service)
* Админка (Report Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**Hotels (Hotel Service):**
```
+ name
+ location: { country, city, address }
+ hotel_uid
```

**Reservations (Booking Service):**
```
+ hotel_uid -> FK to Hotel Service (Hotels::hotel_uid)
+ user_uid -> FK to Session Service (User::user_uid)
+ payment_uid-> FK to Payment Service (Payment::payment_uid)
+ date
```

**Payments (Payment Service):**
```
+ payment_uid
+ status [NEW, PAID, REVERSED, CANCELED]
+ price
```

**UserLoyalty (Loyalty Service):**
```
+ user_uid -> FK to Session Service (User::user_uid)
+ status: [BRONZE, SILVER, GOLD]
+ discount
```

### Основные операции

Специфические для варианта задания:

1. Список отелей. [G]
    ```
    GET /hotels
    ```
1. Информация об отеле. [G]
    ```
    GET /hotels/{hotelUid}
    ```
1. Забронировать номер. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /booking
    body: { hotelUid, room, paymentInfo }
    ```
1. Аннулировать бронь номера. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /booking/{bookingUid}
    ```
1. Информация по бронированию. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /booking/{bookingUid}
    ```
1. Посмотреть мои бронирования. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /booking
    ```
1. Посмотреть баланс бонусной программы. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /loyalty
    ```
1. Добавить отель. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /hotels
    body: { rooms, name, address }
    ```
1. Изменить информацию о доступности комнат. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    PATCH /hotels/{hotelUid}/rooms
    body: { rooms: { number, interval, status } }
    ```
1. Посмотреть статистику бронирования по пользователям: при бронировании отеля данные отправляются в статистику. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/booking
    ```
1. Посмотреть статистику наполнения отелей: сколько мест на текущий момент свободно. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/hotels-filling
    ```

## Вариант 3: Car Rental System

Система предоставляет пользователю возможность забронировать автомобиль на выбранные даты. Пользователь может взять автомобиль
в одном офисе, а отдать в другом. Тем самым это авто станет доступно для бронирования в новом месте с даты окончания
предыдущей аренды.

**Бизнес сервисы:**

* Машины (Car Service)
* Офисы бронирования (Rent Office Service)
* Система бронирования (Booking Service)
* Платежная Система (Payment Service)

**Дополнительные сервисы:**

* Gateway
* Авторизация (Session Service)
* Админка (Report Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**Cars (Car Service):**
```
+ car_uid
+ brand
+ model
+ power
+ type: [SEDAN, SUV, MIVIVAN, ROADSTER]
```

**RentOffice (Rent Service):**
```
+ rent_office_uid
+ location
```

**AvailableCars (Rent Service):**
```
+ car -> FK to Car Service (Cars::car_uid)
+ registration_number
+ availability_schedule
```

**CarBooking (Booking Service):**
```
+ car -> FK to Car Service (Cars::car_uid)
+ user_uid -> FK to Session Service (User::user_uid)
+ payment_uid -> FK to Payment Service (Payment::payment_uid)
+ booking_period
+ status: [NEW, FINISHED, CANCELED, EXPIRED]
+ taken_from_office -> FK to Rent Service (RentOffice::rent_office_uid)
+ return_to_office -> FK to Rent Service (RentOffice::rent_office_uid)
```

**Payments (Payment Service):**
```
+ payment_uid
+ status [NEW, PAID, REVERSED, CANCELED]
+ price
```

### Основные операции

Специфические для варианта задания:

1. Получить список офисов. [G]
    ```
    GET /offices
    ```
1. Получить список всех машин. [G]
    ```
    GET /cars
    ```
1. Получить информацию обо всех машинах в офисе. [G]
    ```
    GET /offices/{officeUid}/cars
    ```
1. Получить информацию о машине и ее доступности в конкретном офисе. [G]
    ```
    GET /offices/{officeUid}/cars/{carUid}
    ```
1. Получить информацию о машине и ее доступности во всех офисах. [G]
    ```
    GET /offices/cars/{carUid}
    ```
1. Забронировать машину. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /booking
    body: { car_uid, taken_from_office, return_to_office, booking_period, payment_data: { ... } }
    ```
1. Отменить бронирование. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /booking/{bookingUid}
    ```
1. Завершить бронирование. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    PATCH /booking/{bookingUid}/finish
    ```
1. Добавить новый автомобиль. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /cars
    body: { brand, model, type, power }
    ```
1. Удалить информацию об автомобиле. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /cars/{carUid}
    ```
1. Добавить новый автомобиль в офис. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /offices/{officeUid}/car/{carUid}
    body: { registration_number, available }
    ```
1. Удалить автомобиль из офиса. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /offices/{officeUid}/car/{carUid}
    ```
1. Посмотреть статистику бронирования автомобилей по моделям. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/booking-by-models
    ```
1. Посмотреть статистику бронирования по офисам. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/booking-by-offices
    ```

## Вариант 4: Library System

Система позволяет пользователю найти интересующую книгу и взять ее в библиотеке. Если у пользователя на руках есть уже N книг,
то он не может взять новую, пока не сдал старые. Если пользователь возвращает книги в хорошем состоянии и сдает их в срок,
то максимальное количество книг у него на руках увеличивается.

**Бизнес сервисы:**

* Книги (Books Service)
* Библиотеки (Library Service)
* Централизованная система контроля сдачи книг (Control Service)
* Рейтинг пользователей (Rating Service)

**Дополнительные сервисы:**

* Gateway
* Авторизация (Session Service)
* Админка (Report Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**Books (Book Service):**
```
+ name
+ book_uid
+ author { first_name, last_name }
+ genre
+ [libraries] -> FK to Library Service (Library::library_uid)
```

**Library (Library Service):**
```
+ library_uid
+ location { city, address }
```

**LibraryBooks (Library Service):**
```
+ library_id -> FK to Library(id)
+ book_uid -> FK to Book Service (Book::book_uid)
+ available_count
```

**TakenBooks (Library Service):**
```
+ taken_book_uid
+ book_uid -> FK to Book Service (Book::book_uid)
+ user_uid -> FK to Session Service (User::user_uid)
+ date
+ status: [NEW, USED, BAD_CONDION, LOST]
```

**UserMonitoring (Control Service):**
```
+ user_uid -> FK to Session Service (User::user_uid)
+ [taken_books] -> FK to Library Service (TakenBooks::taken_book_uid)
+ limit
```

**Rating (Rating Service):**
```
+ user_uid -> FK to Session Service (User::user_uid)
+ status
```

### Основные операции

Специфические для варианта задания:

1. Список книг в библиотеке. [G]
    ```
    GET /library/{libraryUid}/books
    ```
1. Подробная информация о книге. [G]
    ```
    GET /books/{bookUid}
    ```
1. Поиск по названию книги. [G]
    ```
    GET /books?name=...& author=...
    ```
1. Информация об авторе. [G]
    ```
    GET /author/{authorUid}
    ```
1. Краткая информация об авторе и список его книг. [G]
    ```
    GET /author/{authorUid}/books
    ```
1. Найти книгу в библиотеке. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /library/book/{bookUid}
    ```
1. Взять книгу в библиотеке. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /library/{libraryUid}/book/{bookUid}/take
    ```
1. Вернуть книгу. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /library/{libraryUid}/book/{bookUid}/return
    ```
1. Добавить книгу. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /books/{bookUid}
    body: { name, author, gerne }
    ```
1. Удалить книгу. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /books/{bookUid}
    ```
1. Добавить книгу в библиотеку. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /library/{libraryUid}/book/{bookUid}
    ```
1. Убрать книгу из библиотеки. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /library/{libraryUid}/book/{bookUid}
    ```
1. Посмотреть список взятых книг. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /library/user/{userUid}/books
    ```
1. Посмотреть мой рейтинговый статус. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /rating/user/{userUid}
    ```
1. Посмотреть статистику по возвращенным в срок книгам в разрезе пользователя. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/books-return
    ```
1. Посмотреть статистику жанров книг: какие жанры берут чаще всего. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/books-genre
    ```

## Вариант 5: Equipment monitoring System

Система позволяет пользователю мониторить состояние выбранного оборудования. Система состоит из сервиса оборудования
(конкретных экземпляров с серийными номерами) и моделей (классов) оборудования, сервиса, имитирующего получение
данных с экземпляров оборудования, и экранов мониторинга, отображающего данные по оборудованию для пользователей.

**Бизнес сервисы:** 

* Табло мониторинга (Monitor Service)
* Оборудование (Equipment Service)
* Файловое хранилище документов по оборудованию (Documentation Service)
* Данные с оборудования (Generator Service)

**Дополнительные сервисы:**

* Gateway
* Авторизация (Session Service)
* Админка (Report Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**Monitor (Monitor Service):**
```
+ monitor_uid
+ name
+ [equipment_uid] -> FK to Equipment Service (Equipment::equipment_uid)
+ [equipment_models_uid] -> FK to Equipment Service (EquipmentModel::equipment_models_uid)
+ [params] -> FK to Equipment Service (EquipmentModel::params)
```

**Equipment (Equipment Service):**
```
+ equipment_uid
+ [model_uid] -> FK to Equipment Service (EquipmentModel::equipment_model_uid)
+ status
```

**Equipment Model (Equipment Service):**
```
+ equipment_model_uid
+ [params]
```

**Files (Documentation Service):**
```
+ file_uid
+ file_name
+ content
+ equipment_model_uid -> FK to Equipment Service (EquipmentModel::equipment_model_uid)
```

**DataGenerator (Generator Service):**
```
+ data_uid
+ equipment_uid -> FK to Equipment Service (Equipment::equipment_uid)
+ value
+ param
```
(!) Указанный набор полей характерен для "получаемой с оборудования информации", использование базы данных
в данном сервисе определяется студентом на этапе проектирования.

### Основные операции

Специфические для варианта задания:

1. Список экранов мониторинга. [G]
    ```
    GET /monitors
    ```
1. Экран мониторинга. [G]
    ```
    GET /monitors/{monitorUid}
    ```
1. Настройка экрана мониторинга. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /monitor
    body: { monitorUid, name, [equipment_uid], [equipment_models_uid], [params] }
    ```
1. Добавить модель оборудования. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /equipment-model
    ```
1. Создать экземпляр оборудования. [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /equipment
    body: { ... }
    ```
1. Изменить статус оборудования (активировать, деактивировать, списать). [A][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /equipment/{equipmentUid}/{activate/deactivate/remove}
    ```
1. Просмотр модели оборудования. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /model/{equipmentModelUid}
    ```
1. Просмотр конкретного оборудования. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /equipment/{equipmentUid}
    ```
1. Посмотреть статистику по "популярности" оборудования (на скольких экранах отслеживается). [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/equipment-popular
    ```
1. Посмотреть статистику по количеству работающего оборудования. [A][G]
    ```
    header: Authorization: bearer <jwt>
    GET /reports/equipment-active
    ```

## Вариант 6: Chat System (*)

Реализовать систему группового обмена сообщениями. В группах есть пользователи с разными ролями, в зависимости от этих ролей
им доступен разный набор команд. Система обмена должна быть асинхронная. Отправку, модификацию и получение сообщений в чате
реализовать через WebSocket, внутреннюю обработку на основе неблокирующих потоков.

**Бизнес сервисы:**

* Пользователь чата (User Data Service)
* Чат (Chat Service)
* Файловое хранилище документов (Files Service)

**Дополнительные сервисы:**

* Gateway
* Авторизация (Session Service)

### Структуры данных

**User (Session Service):**
```
+ login
+ password
+ user_uid
```

**UserData (User Data Service):**
```
+ user_uid -> FK to Session Service (User::user_uid)
+ avatar
+ name {first_name, last_name }
+ status: [ONLINE, AWAY, OFFLINE]
```

**Topic (Chat Service):**
```
+ topic_uid
+ name
+ [user_uid, role] -> FK to Session Service (User::user_uid)
```

**Messages (Chat Service):**
```
+ message_uid
+ topic_uid -> FK to Chat Service (Topics::topic_uid)
+ user_uid -> FK to Session Service (User::user_uid)
+ data
+ status
```

**Files (Files Service):**
```
+ file_uid
+ file_name
+ content
+ message_uid -> FK to Chat Service (Messages::message_uid)
```

### Основные операции

Специфические для варианта задания:

1. Список диалогов. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /topics
    ```
1. Показать информацию про диалог. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /topics/{topicUid}
    ```
1. Показать пользователей в диалоге. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /topic/{topicUid}/users
    ```
1. Показать информацию о пользователе. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /users/{userUid}
    ```
1. Изменение роли пользователя в диалоге. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /topic/{topicUid}/{user_uid}
    body: { role }
    ```
1. Добавить диалог. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    POST /topics
    body: { name, [user_uid, role] }
    ```
1. Удалить диалог. [S][M][G]
    ```
    header: Authorization: bearer <jwt>
    DELETE /topics/{topicUid}
    ```
1. Написать сообщение. [S]
    ```
    WebSocket
    body: { topic_uid, message }
    ```
1. Изменить сообщение. [S]
    ```
    WebSocket
    body: { message_uid, message }
    ```
1. Удалить сообщение. [S]
    ```
    WebSocket
    ```
1. Получить сообщение. [S]
    ```
    WebSocket
    ```
1. Загрузить файл. [S][G]
    ```
    header: Authorization: bearer <jwt>
    POST /files
    body: { topic_uid, file_data }
    ```
1. Скачать файл. [S][G]
    ```
    header: Authorization: bearer <jwt>
    GET /files/{fileUid}/download
    ```