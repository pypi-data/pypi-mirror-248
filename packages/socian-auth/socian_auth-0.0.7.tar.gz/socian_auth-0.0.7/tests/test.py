# Example usage
from socian_auth import SocianAuthApiClient

# Replace 'your_base_url' with the actual base URL of your API
base_url = 'your_base_url'
api_client = SocianAuthApiClient(base_url)

# Replace 'user_id' with the actual user ID you want to fetch
user_info = api_client.get_user_info(user_id='user_id')

print(user_info)
