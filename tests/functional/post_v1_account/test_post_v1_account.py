import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)

def test_account_creation(account_helper, prepare_user):
    # регистрация нового пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.create_user(login=login, password=password, email=email)