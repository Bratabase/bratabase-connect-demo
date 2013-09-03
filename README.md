# Bratabase connect sample Django project

This is a Django project that shows sample code on how to use the Bratabase API and authenticating/authorizing using OAuth.

You can see the app running at http://bratabase-connect.herokuapp.com/

## Requirements

* Python
* Virtualenvwrapper (Optional but recommended)

Before beginning, you will need to register your Application on http://www.bratabase.com/my/developer/applications/

On the `Redirect URI` field, enter the host you will be running this from (possibly `http://localhost:8000`) and make sure the path is `/complete/bratabase/`.

Then create a `local_settings.py` file at the root of your repository with the following contents:

```
BRATABASE_APP_ID = '{{Your APP ID}}'
BRATABASE_API_SECRET = '{{Your Secret Key}}'
```

Now you are good to launch the app:

```
$ mkvirtualenv --no-site-packages  bratabase-connect
$ pip install -r requirements.txt
$ ./manage.py syncdb --noinput
$ ./manage.py runserver
```
Open your browser on http://localhost:8000/ and you should see the same application that is running at http://bratabase-connect.herokuapp.com/

## Understanding the code

All the custom code is under https://github.com/Bratabase/bratabase-connect-demo/blob/master/apps/website/views.py

The function you want to look at is `get_user_bras()`:

```
def get_user_bras(token):
    request = get_request(BratabaseAuth.ME_URL, token)
    body = json.load(urlopen(request))
    bras_url = body['links']['bras']
    request = get_request(bras_url, token)
    bras = json.load(urlopen(request))
    return bras

```

It will first hit the Bratabase API "ME" url, where it will fetch the information for the authorized user (identified by her token) and then will follow the `bras` url under the `link` section of the response.

Consuming this `bras` url will return a JSON response that contains the list of bras for this user.

