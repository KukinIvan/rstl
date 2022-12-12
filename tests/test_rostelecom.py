import pytest
import param
from pages.auth_page import AuthPage
from pages.registration_page import RegPage


# Тест-кейс  EXP-001 (Bug PB-001)
@pytest.mark.xfail(reason="Таб выбора 'Номер' не соответсвует ожидаемым требованиям")
def test_phone_tab(web_browser):
    """
    Проверка названия таба выбора "Номер"
    """
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


# Тест-кейс EXP-001
def test_start_page_is_correct(web_browser):
    """
    Корректное отображение "Стандартной страницы авторизации" в соответствии с тербованиями.
    """
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"
    assert page.slogan_lk.get_text() == "Персональный помощник в цифровом мире Ростелекома"


# Тест-кейс EXP-002
def test_mail_tab(web_browser):
    """
    При вводе  почты в таб "телефон", выбор таба аутентификации меняется автоматически.
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.email)
    page.password.click()
    mail_tab_class = page.mail_tab.get_attribute("class")
    assert mail_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс EXP-003 (Bug PB-002)
@pytest.mark.xfail(reason="При вводе почты по табу 'Логин' - таб выбора аутентификации не меняется автоматически.")
def test_login_tab(web_browser):
    """
    При вводе почты в таб "Логин", выбор таба аутентификации меняется автоматически.
    """
    page = AuthPage(web_browser)
    page.login_tab.click()
    page.phone.send_keys(param.email)
    page.password.click()
    mail_tab_class = page.mail_tab.get_attribute("class")
    assert mail_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс EXP-004
def test_ls_tab_for_email(web_browser):
    """
    При вводе почты в таб "Лицевой счет", выбор таба аутентификации меняется автоматически.
    """
    page = AuthPage(web_browser)
    page.ls_tab.click()
    page.phone.send_keys(param.email)
    page.password.click()
    mail_tab_class = page.mail_tab.get_attribute("class")
    assert mail_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс EXP-007 (Bug PB-004)
@pytest.mark.xfail(reason="При вводе Мобильного телефона по табу 'Лицевой счет' - таб выбора аутентификации"
                          " не меняется автоматически.")
def test_ls_tab_for_phone(web_browser):
    """
    При вводе номера телефона в таб "лицевого счета", выбор таба аутентификации меняется автоматически.
    """
    page = AuthPage(web_browser)
    page.ls_tab.click()
    page.phone.send_keys(param.phone)
    page.password.click()
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс EXP-008
def test_authorisation_valid_phone(web_browser):
    """
    Тестирование аутентификации зарегестрированного пользователя через телефон
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.phone)
    page.password.send_keys(param.password)
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс EXP-010
def test_authorisation_empty_phone(web_browser):
    """
    Авторизации клиента по номеру телефона (пустое поле "Мобильный телефон")
    Система перекрасит красным цветом надпись "Мобильный телефон" в поле ввода телефона и
    ниже поле появится красная надпись "Введите номер телефона"
    """
    page = AuthPage(web_browser)
    page.phone.send_keys("")
    page.password.send_keys(param.password)
    page.btn_login.click()
    assert page.message_invalid_username.get_text() == "Введите номер телефона"


# Тест-кейс EXP-012
def test_authorisation_valid_mail(web_browser):
    """
    Тестирование аутентификации зарегестрированного пользователя через E-mail
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys(param.email)
    page.password.send_keys(param.password)
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс EXP-013
def test_authorisation_invalid_mail(web_browser):
    """
    Авторизации клиента по почте ( неверный пароль для входа).
    В блоке Авторизации выводится сообщение "Неверный логин или пароль" и
    элемент "Забыл пароль" перекрашивается в оранжевый цвет.
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys(param.email)
    page.password.send_keys(param.password2)
    page.btn_login.click()
    forgot_the_password = page.the_element_forgot_the_password.get_attribute("class")
    assert forgot_the_password == "rt-link rt-link--orange login-form__forgot-pwd login-form__forgot-pwd--animated"


# Тест-кейс EXP-020
def test_forgot_the_password_invalid_sms_password(web_browser):
    """
    Сценарий восстановления пароля клиента по номеру телефона, кнопка "По номеру телефона" Неверный код из смс
    Отображается ошибка "Неверный код. Повторите попытку"
    """
    page = AuthPage(web_browser)
    page.the_element_forgot_the_password.click()
    page.phone.send_keys(param.phone)
    page.captcha.send_keys(param.captcha)
    page.resetbtn.click()
    assert page.reseterror.get_text() == "Неверный логин или текст с картинки"


# Тест-кейс EXP-037 (Bug PB-010)
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить' и в блоке слева должен быть логотип и слоган")
def test_registration_page_and_continue_button(web_browser):
    """
    Страница формы регистрации должна соответствовать требованиям
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    try:
        assert reg_page.name_field_text.get_text() == "Имя"
        assert reg_page.last_name_field_text.get_text() == "Фамилия"
        assert reg_page.region_field_text.get_text() == "Регион"
        assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
        assert reg_page.password_field_text.get_text() == "Пароль"
        assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
        assert reg_page.continue_button.get_text() == "Продолжить"
    except AssertionError:
        try:
            assert reg_page.logo_lk.get_text() == "Личный кабинет"
        except AssertionError:
            assert reg_page.slogan_lk.get_text() == "Персональный помощник в цифровом мире Ростелекома"


# Тест-кейс EXP-038
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    """
    Страница формы регистрации, Имя  состоит из 1 буквы кирилицы.
    Отображается ошибка "Необходимо заполнить поле кириллицей. От 2 до 30 символов".
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.fname)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-039
def test_instead_of_cyrillic_invalid_characters(web_browser):
    """
    Страница формы регистрации, Имя и Фамилия  написано латиницей.
    Отображается ошибка "Необходимо заполнить поле кириллицей. От 2 до 30 символов".
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.engname)
    reg_page.last_name_field.send_keys(param.englastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. " \
                                                                     "От 2 до 30 символов."


# Тест-кейс EXP-040
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    """
    Страница формы регистрации, Фамилия  состоит из 31 буквы килицы.
    Отображается ошибка "Необходимо заполнить поле кириллицей. От 2 до 30 символов".
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.flastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-041
def test_symbol_dash_in_name_registration(web_browser):
    """
    Страница формы регистрации, есть знак тире (-) в формах "Имя" и "Фамилия"
    Система не отображает ошибку о недопустимости символа."
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.namedash)
    reg_page.last_name_field.send_keys(param.lastnamedash)
    # assert reg_page.findElements(message_symbol_error)
    assert not reg_page.message_symbol_error.is_presented()


# Тест-кейс EXP-042
def test_incorrect_password_during_registration(web_browser):
    """
    Страница формы регистрации, ввод пароля меньше 8ми символов (7).
    Система отображает ошибку под полями ввода пароля: "Длина пароля должна быть не менее 8 символов"
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.fpassword)
    reg_page.password_confirmation_field.send_keys(param.fpassword)
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс EXP-043 (Bug PB-011)
@pytest.mark.xfail(reason="В форме регистрации ошибка корректности пароля по правилам не совпадает с Требованиями")
def test_password_lowercase_letters_in_reg(web_browser):
    """
    Страница формы регистрации, ввод пароля без заглавных символов
    Система отображает ошибку под полями ввода пароля: "Пароль должен содержать хотя бы одну заглавную букву"
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.passmall)
    reg_page.password_confirmation_field.send_keys(param.passmall)
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароль должен содержать хотя бы одну заглавную букву"


# Тест-кейс EXP-044
def test_password_and_password_confirmation_do_not_match(web_browser):
    """
    Страница формы регистрации, ввод пароля в поле "Подтверждение пароля" отличный от пароля в поле "Пароль".
    Система отображает ошибку под полем "Подтверждение пароля": "Пароли не совпадают"
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password2)
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс EXP-045 (Bug PB-012)
@pytest.mark.xfail(reason="Отсутствует Кнопка 'х' - закрыть всплывающее окно оповещения"
                          " в форме регистрации на существующиую почту")
def test_registration_of_an_already_email_registered_user(web_browser):
    """
    Страница формы регистрации, ввод E-mail уже зарегистрированный в системе,
    отображается оповещающая форма соответствующая требованиям
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# Тест-кейс EXP-046 (Bug PB-013)
@pytest.mark.xfail(reason="Кнопки 'Зарегистрироваться' и 'Войти' не соответствуют Требованиям")
def test_registration_of_an_already_phone_registered_user(web_browser):
    """
    Страница формы регистрации, ввод телефон уже зарегистрированный в системе,
    отображается оповещающая форма соответствующая требованиям
    """
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.phone)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible
    assert reg_page.login_button.get_text() == 'Зарегистрироваться'
    assert reg_page.recover_password_button.get_text() == 'Отмена'
