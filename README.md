# Tide programming task
Simple service to retrieve dynamically changed features to client apps.

The technologies used for the implementation have been the following:
* Flask
* Redis
* gunicorn (for prod deploy)

## Purpose
The system is composed by just one endpoint. It is used by client apps, which should always call it as soon as the app is launched. The response will contain an array of features they can activate for the client. By doing so, client apps can continuously push new features and changes to end clients and remain silent. Once decided, those features can be activated from the backoffice, and when the client apps check the endpoint, they will get a new set of features they can activate.

```
GET /features
response:
{
    "active_features": ["feature_1", "feature_2"]
}
```

## Current version
The system has been thought as an initial approach to the problem. For the moment it allows the following:
* Define a set of globally enabled features.
* Define a set of features per user.
* For each of the users, which features are available.

So for example, if the app does not have an authenticated user, the request to the endpoint will just return the globally enabled features. If the user is authenticated, though, the system will check which are the features enabled for that user, and will compare them to the ones available. With this final check we can enable and disable features per user. Lots of users can have "feature_7" enabled, but as long as it is not included in the available ones, they won't see it. It is also useful in case we need to rollback. We might deploy a feature, find some tricky bug and decide to retire it. Simply deleting it from the available features will make it disappear for every user.

The technologies used should allow handling a big load. The overhead that the access to the Redis instances add is negligible, and the endpoint is light enough to respond very quickly.

## Solution
The previously mentioned stack has been used the following way:
* Flask is the framework that serves the API.
  * It should be launched with gunicorn in production, as it allows "parallel" processing while I/O is being produced in the system (for example, accessing Redis).
* Two Redis instances are required, one for user authentication and other one for the features.
  * The user Redis requires the following format for each entry:
  ```
  token:token_1 => user_id_1
  token:token_2 => user_id_2
  ...
  ```
  * The features Redis requires two specific keys pointing to a set each, and then one key pointing to a set per user.
  ```
  global_features => set(feature_1, feature_2)
  active_features => set(feature_7)

  features:user:1 => set()
  features:user:2 => set(feature_7, feature_8)
  ...
  ```

## Running the service
The system just needs a running Redis cluster with at least 2 instances. The steps to execute the server would be the following:
* Not needed but recommended. Create a virtual environment for the project with virtualenv.
* Add two environment variables, REDIS_USERS_URL and REDIS_FEATURES_URL, pointing to the redis instances. For example, `redis://127.0.0.1:6379/1` and `redis://127.0.0.1:6379/1`. In the virtualenv it can be added at the end of the bin/activate file as a typical bash export.
* Install the dependencies with `pip install -r requirements.txt`.
* Run the server with `./run.py`. It will be accessible at `http://127.0.0.1:5000`.

Calling `/features` will simply return an empty array, as the system does not contain anything. In order to do more tests, you can access the Redis instances and add the following:
* Add a token for a user in the users Redis instance. In this case associate user ID 1 with the token 1234.
 ```
 SET token:1234 1
 ```
* Add some features in the features Redis instance, both globally and for the previously added user.  
 `feature_1` and `feature_2` are globally available, so they will always be returned.  
 `feature_3` is available to those users who have it included.  
 Even if `feature_4` is included for user 1 it will not be retrieved, as it is not active.  
 ```
 SADD global_features feature_1 feature_2
 SADD active_features feature_3
 SADD features:user:1 feature_3 feature_4
 ```

## How to run tests
* Install the dependencies with `pip install -r requirements-test.txt`.
* Execute the tests with `pytest .`

## Future work
This is a quick approach to feature switches, it puts in place a working system with some restrictions (such as different features per user), but the work could be extended to be used in different locations, schedules, etc.
For instance, a new set of keys could be added to the features Redis instance, such as:
```
location:location1 => set_of_features
location:location2 => set_of_features
```
This way we could get the name of the location of the user (or checking with the IP, or any other method) and apply an extra set of different features.

Regarding growth, if the load continues to increase, simply tweaking the gunicorn configuration to launch more child processes should be enough. Or launching more servers with the same server instance. The only shared resource are the Redis instances, so we can just replicate servers to have a larger throughput.
