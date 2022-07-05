# node-exercise-with-python

You'll need to have python3 installed.
```
python3 -m venv venv
source ./venv/bin/activate
# verify pip3 is in virtualenv
which pip3
pip3 install -r requirements.txt
python3 app.py
```
Then you can either visit the GUI or open another terminal and run:
```
curl http://127.0.0.1:5000/people
curl http://127.0.0.1:5000/people?sortBy=height
curl http://127.0.0.1:5000/people?sortBy=name
curl http://127.0.0.1:5000/people?sortBy=mass
curl http://127.0.0.1:5000/planets
```
