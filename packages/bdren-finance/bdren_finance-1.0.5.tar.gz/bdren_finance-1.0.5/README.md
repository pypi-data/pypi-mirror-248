### Setup

you need to add 3 variables in your settings.py file:

```python
# settings.py

BDREN_FINANCE_URL = 'https://finance.bdren.net.bd'
BDREN_FINANCE_AUTH_EMAIL = 'your_username'
BDREN_FINANCE_AUTH_PASSWORD = 'your_password'
```

### Usage

```python
from bdren_finance import finance_login_session

finance_request = finance_login_session()
```

### Example

```python
from django.conf import settings

from bdren_finance import finance_login_session

finance_request = finance_login_session()


def get_accounts(session, query: str, _type: str = "all", field: str = "no") -> dict:
    """
    Get accounts from BdREN Finance API
    :param session:
    :param query:
    :param _type:
    :param field:
    :return: Dict
    """

    url = settings.BDREN_FINANCE_URL + 'account/search/?q=' + query + '&type=' + _type + '&field=' + field
    res = session.get(url)
    return res.json()


print(get_accounts(finance_request))
```