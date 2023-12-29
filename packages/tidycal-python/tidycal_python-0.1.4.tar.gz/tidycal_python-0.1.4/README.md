
# tidycal-python
![](https://img.shields.io/badge/version-0.1.4-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*tidycal-python* is an API wrapper for Tidycal, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install tidycal-python
```
### Usage
```python
from tidycal.client import Client
client = Client(client_id, client_secret, redirect_uri=redirect_uri)
```
To obtain and set an access token, follow this instructions:
1. **Get authorization URL**
```python
url = client.authorization_url(state=None)
# This call generates the url necessary to display the pop-up window to perform oauth authentication
# param state(code) is required for direct request for oauth, for local test isn't necessary
```
2. **Get access token using code**
```python
token = client.get_access_token(code)
# "code" is the same response code after login with oauth with the above url.
```

3. **Refresh access token using refresh_token**
```python
token = client.refresh_access_token(refresh_token)
# "refresh_token" is the token refresh in response after login with oauth with the above url.
```

#### - Get current user
```python
client.get_current_user()
```
#### - List of Bookings
```python
client.list_bookings(starts_at=None, ends_at=None, cancelled=None, page=None)
# Receives only one parameter at a time
# starts_at = DATE, Get bookings starting from a specific date.
# ends_at = DATE, Get bookings ending before a specific date.
# cancelled = BOOLEAN, Get only cancelled bookings.
# page = NUMBER, Page number.
```
#### - List of Booking Types
```python
client.list_booking_types()
```
#### - List of Contacts
```python
client.list_contacts()
```
