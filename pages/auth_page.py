from pages.base import WebPage
from pages.elements import WebElement


class AuthPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = 'https://b2c.passport.rt.ru'

        super().__init__(web_driver, url)

    phone = WebElement(id='username')
    email = WebElement(id='username')
    password = WebElement(id='password')
    btn_login = WebElement(id='kc-login')
    auth_title = WebElement(xpath='//*[@id="page-right"]/div/div/h1')
    registration_link = WebElement(id='kc-register')
    phone_tab = WebElement(id='t-btn-tab-phone')
    mail_tab = WebElement(id='t-btn-tab-mail')
    login_tab = WebElement(id='t-btn-tab-login')
    ls_tab = WebElement(id='t-btn-tab-ls')
    logo_lk = WebElement(xpath='//*[@id="page-left"]/div/div[2]/h2')
    slogan_lk = WebElement(xpath='//*[@id="page-left"]/div/div[2]/p')
    auth_form = WebElement(xpath='//*[@id="page-left"]/div/div')
    lk_form = WebElement(xpath='//*[@id="page-right"]/div/div')
    message_invalid_username_or_password = WebElement(xpath='//*[@id="page-right"]/div/div/p')
    the_element_forgot_the_password = WebElement(xpath='//*[@id="forgot_password"]')
    message_invalid_username = WebElement(xpath='// *[ @ id = "page-right"] / div / div / div / form / div[1] / div[2] / span')
    captcha = WebElement(id='captcha')
    resetbtn = WebElement(id='reset')
    reseterror = WebElement(id='form-error-message')







