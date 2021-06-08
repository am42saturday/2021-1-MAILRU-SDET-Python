##    Найденные баги:
###    UI
1) Python dropdown открывает страница python.org  
(Ожидание Открывается только меню)  
(test_ui_check_dropdown)
2) Download Centos7 ведет к загрузке Fedora  
(Ожидание - загрузка Centos)  
(test_ui_open_links)
3) History of Python открывается в той же вкладке  
(Ожидание Все ссылки перенаправляющий на сторонний сайт открываются в новых вкладках)  
(test_ui_open_links)
4) Грамматическая ошибка при регистрации уже существующего пользователя User already exist  
(Ожидается User already exists)  
(test_api_create_existing_user, test_ui_create_existing_user)
5) При создании пользователя с email уже зарегистрированным в бд - 500 Internal Server Error  
(Ожидается 409 User with this email already exists)  
(test_api_create_existing_user, test_ui_create_existing_user)
6) При вводе слишком длинного email 500 Internal Server Error  
(ожидается 400 Incorrect Email Length)  
(test_api_registration_invalid_data, test_ui_registration_invalid_data)
7) При вводе слишком длинного пароля 500 Internal Server Error  
(ожидается 400 Incorrect Password Length)  
(test_api_registration_invalid_data, test_ui_registration_invalid_data)
   
 ###      API
 ####               TestAPIUsers

8) При добавлении пользователя (add_user), успешно добавляется, но статус код 210 (в т.ч. с существующим паролем)  
(Ожидается 201)  
(test_api_add_user)
9) При добавлении пользователя с невалидными данными, возвращается 210
(иногда успешно добавляется, если не нарушены лимиты бд)  
(ожидается 400 Bad request)  
(test_api_negative_add_user)
10) При добавлении пользователя с существующим email, успешно добавляется, статус код 210  
(Ожидается 304)  
(test_api_add_existing_user)

####     TestAuth

11) При попытке авторизоваться с слишком длинным или коротким login на фронт выводится ошибка, а status_code 200  
(ожидается 400)  
(test_api_unsuccessful_login)

####  TestRegistration

12) При отправке запроса регистации пользователя с term равном любому значению кроме пустой строки, считается, что user принял согласие  
(Ожидается 400, You dont want to be a SDET)  
(test_api_registration_without_acceptance)
10) При api запросах add user нет валидации полей  
(Ожидается что пользователи с неверными данными не создаются)  
(test_api_negative_add_user)