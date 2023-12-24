# Socian Auth Python SDK

[![Version](https://img.shields.io/pypi/v/socian-auth)](https://pypi.org/project/socian-auth/)
[![License](https://img.shields.io/pypi/l/socian-auth)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/socian-auth)](https://pypi.org/project/socian-auth/)

## Overview

The Socian Auth Python SDK provides a convenient way to interact with the Socian Auth API for authentication and user management.

## Installation

You can install the library using pip:

```bash
pip install socian-auth
```
## Usage

### Initialization
```python
from socian_auth import SocianAuthApiClient

client = SocianAuthApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    ssh_public_key="your_ssh_public_key"
)
```
### Getting Intent
```python
intent_obj = client.get_intent("auth.signIn", "http://localhost:3000/auth/callback")
print(intent_obj)
```

### Checking User Existence
```python
email = "example@example.com"
is_user_exist = client.check_user_exists(intent_id=intent_obj.intent_id, email=email)
print(is_user_exist)
```

### User Signup
```python
user_info = client.user_signup(intent_id=intent_obj.intent_id, name="John Doe", email=email, password="password123")
print(user_info)
```


### User Signin
```python
login_data = client.user_signin(email=email, password="password123")
print(login_data)
```


### User Information
```python
user_info = client.user_info(access_token=login_data.access_token)
print(user_info)
```


## Documentation

For more details and API documentation, please refer to [Socian Auth SDK Documentation](https://github.com/Socian-Ltd/socian_auth_sdk_python.git).

## Contributing

If you find any issues or have suggestions for improvement, please open an issue or create a pull request on [GitHub](https://github.com/Socian-Ltd/socian_auth_sdk_python.git).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



