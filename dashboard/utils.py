import secrets
import string

from users.models import User
from utils.string_loader import StringLoader


def generate_password():
    PASSWORD_LENGTH = 12

    alphabet = string.ascii_letters + string.digits
    random_password = ''.join(secrets.choice(alphabet) for i in range(PASSWORD_LENGTH))

    return random_password


def share_user_password(user: User, password: str):
    # text = StringLoader.get_string('dashboard.create_user.email_message')
    # try: send password to user.email
    # except:

    with open('new_users.txt', 'a', encoding='utf-8') as file:
        file.write(f"\n{user.email}\n{password}\n\n")
