import pytest
import seleniumwrapper


@pytest.fixture()
def browser(sub):
    sub.delete()
    chrome = seleniumwrapper.create('chrome')
    chrome.maximize_window()
    yield chrome
    chrome.quit()


def test_ui_create_sub(browser):
    """ Создадим подписку и проверим поля
    """
    browser.get('http://localhost:4000')
    browser.xpath("//h4[text()='Привет!']")

    email = 'myemail@email.com'
    my_name = 'Мое имя'
    browser.xpath("//input[@placeholder='Email']").send_keys(email)
    browser.xpath("//input[@placeholder='Имя пользователя']").send_keys(my_name)
    browser.xpath("//button[text()='Подписаться']").click()

    sub_email = browser.xpath("//th[@scope='row']").text
    user_name = browser.xpath("(//table[@class='table table-hover']//td)[1]").text
    assert sub_email == email  # тут какие-то ошибки в верстке. Названия элементов не правильные. тест падает
    assert user_name == my_name


def test_ui_refresh_and_delete_sub(browser):
    """ Создадим подписку и проверим рефреш и удаление
    """
    browser.get('http://localhost:4000')
    browser.xpath("//h4[text()='Привет!']")

    email = 'myemail@email.com'
    my_name = 'Мое имя'

    browser.silent = True
    assert not browser.xpath("//th[@scope='row']", timeout=2)

    browser.xpath("//input[@placeholder='Email']").send_keys(email)
    browser.xpath("//input[@placeholder='Имя пользователя']").send_keys(my_name)
    browser.xpath("//button[text()='Подписаться']").click()

    assert browser.xpath("//th[@scope='row']", timeout=2)

    # refresh
    browser.xpath("(//button[@type='button'])[3]").click()
    assert browser.xpath("//th[@scope='row']", timeout=2)

    # delete
    browser.xpath("(//button[@type='button'])[4]").click(postsleep=2)
    assert not browser.xpath("//th[@scope='row']", timeout=2)