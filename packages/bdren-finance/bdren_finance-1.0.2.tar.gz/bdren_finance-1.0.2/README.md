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

session = finance_login_session()
```
