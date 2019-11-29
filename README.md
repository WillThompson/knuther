# knuther

## Set-up (Linux)

0. Clone project and open a terminal in the parent directory

1. Set up the virtual environment:
```
virtualenv .venv -p python3
```

2. Create symbolic link to activate file in the parent directory:
```
ln -s .venv/bin/activate
```

3. Activate the virtual environment:
```
source activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

5. Run the tests on a sample set of data:

```
python main.py
```
