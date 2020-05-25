# OneHitWonders Musician Finder Application

### Team Members:
#### Charlie Ylijoki
#### Jordan Hamilton
#### Sean Murphy
#### Stephen Sullivan
#### Maxime Desmet Vanden Stock

## Created Using
 - Python
 - Django
 - AWS
 
 ## Team Operation
 Our team operates using [Scrum methodologies](https://www.scrumguides.org/scrum-guide.html#team-po).
 
 ## Background and Description
The OneHitWonder application is a Django based web-app that enables both Musicians looking for work and Venue owners looking for Musicians to connect with one another via skill level specific advertisement. Employers can post experience targeted advertisements to Musicians that match the employers desired criteria. All data interactions and storage of the web application is done using the AWS relational database.

## Usage Instructions
To access the application, visit https://onehitwonder.rocks and login using the following credentials:

Username: subramar

Password: OSUSWE361!

Note that the administrative interface is accessible using the same credentials through https://onehitwonder.rocks/admin.

Alternatively, you can visit https://onehitwonder.rocks/register to access the application as a new user.

To run the application locally:
1. Clone the master branch via Git, or download the latest release [here](https://github.com/ylijokic/CS361_Team21/releases).
2. Create and activate a Python 3 environment.
3. Install dependencies.
4. Run the server.

**Note:** Running the application locally requires a Mapbox access token. You can sign up for a Mapbox account [here](https://www.mapbox.com/signup/). Once your account is created, copy your default public token from your Mapbox account's [access tokens page](https://account.mapbox.com/access-tokens/), then create a new file named `config.py` in the [CS361_Team21/one_hit_wonder/account](https://github.com/ylijokic/CS361_Team21/tree/master/one_hit_wonder/account) directory. The config.py file consists of a single line: `api_token = 'YOUR_MAPBOX_ACCESS_TOKEN'`. Once the config.py file is saved, the application will start successfully in development mode.

## Example Usage
```
python -m venv env
source env/bin/activate
cd one_hit_wonder
pip install -r requirements.txt
echo "api_key = 'YOUR_MAPBOX_ACCESS_TOKEN'" > account/config.py
python manage.py runserver
```
