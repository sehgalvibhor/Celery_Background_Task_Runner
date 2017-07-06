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

