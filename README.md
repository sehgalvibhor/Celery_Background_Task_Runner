# Celery_Background_Task_Runner
Run's specific user based tasks for time interval defined by the user. The REST application uses Celery for running Python tasks in the background. For example if the user wants to run a job for 300 seconds he can submit a POST request with time in headers.

<p>
Basic application stack - Flask, Python 2.7 <br>
OS : Windows 10 <br>
Tested using Postman<br>


## Running on a Windows system

1. Unzip the Redis server zip file.
2. Run the redis-server.exe file.
3. pip install -r requirements.txt
4. python server.py
5. celery -A server.celery worker -n worker1 (Assumes only one worker)
6. All 3 of the points (2,4,5) should be working and running simultaneously.

### Exposes a GET API as "api/request?connId=19&amp;timeout=80&quot"
This API will keep the request running for provided time on the server side. After the successful completion of the provided time it should return {&quot;status&quot;:&quot;ok&quot;}

### Exposes a GET API as &quot;api/serverStatus&quot;

This API returns all the running requests on the server with their time left for completion. E.g {&quot;2&quot;:&quot;15&quot;,&quot;8&quot;:&quot;10&quot;} where 2 and 8 are the connIds and 15 and 10 is the time remaining for the requests to complete (in seconds).

### Exposes a PUT API as &quot;api/kill&quot; with payload as {&quot;connId&quot;:12}

This API will finish the running request with provided connId, so that the finished request returns {&quot;status&quot;:&quot;killed&quot;} and the current request will return {&quot;status&quot;:&quot;ok&quot;}.
