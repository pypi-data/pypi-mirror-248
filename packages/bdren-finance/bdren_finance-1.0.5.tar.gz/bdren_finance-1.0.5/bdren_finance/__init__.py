import requests
from django.conf import settings

BASE_URL = settings.BDREN_FINANCE_URL


def finance_login_session():
    session = requests.Session()
    res = session.get(BASE_URL + 'csrf/')
    csrfToken = res.json()['csrfToken']
    login_data = {
        'email': settings.BDREN_FINANCE_AUTH_EMAIL,
        'password': settings.BDREN_FINANCE_AUTH_PASSWORD,
        'csrfmiddlewaretoken': csrfToken
    }
    login = session.post(BASE_URL + 'login/', data=login_data, headers=dict(Referer=BASE_URL))
    if login.status_code != 200:
        raise Exception('Login failed to BdREN Finance')
    return session


re = finance_login_session()


def get_accounts(session, query: str, _type: str = "all", field: str = "no") -> dict:
    """
    Get accounts from BdREN Finance API
    :param session: Requests session
    :param query: Query string
    :param _type: all, parent, sub
    :param field: no, name
    :return: Dict
    """

    url = BASE_URL + 'account/search/?q=' + query + '&type=' + _type + '&field=' + field
    res = session.get(url)
    return res.json()
