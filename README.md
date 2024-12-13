**Activate the virtual environment**

```
source blockchain-env/bin/activate
```

**Install all packages**

```
pip3 install -r requirements.txt
```

**Run the tests**
Make sure to activate the virtual environment

```
python3 -m pytest Backend/Tests
```

**Run the Application and API**
Make sure to activate the virtual environment

```
python3 -m Backend.App
```

**Run a peer instance**
Make sure to activate the virtual environment

```
export PEER=True && python3 -m Backend.App
```

**Run the frontend**

In the frontend directory:

```
npm run start
```

**Seed the backend with data**
Make sure to activate the virtual environment

```
export SEED_DATA=True && python3 -m Backend.App
```
