# mapunfold

## Visualization

Change to the folder `visualize`. 

Install dependencies

    npm install

Dev mode

    npm run dev

Screenshots

![found](/screenshots/visualize_found.png)
![not found](/screenshots/visualize_not_found.png)

Database name: mapunfold.db
## Commands

Create venv

    python -m venv .mapunfold_venv

Activate venv

    source .mapunfold_venv/bin/activate

Install dependencies

     pip install -r requirements.txt

Run the module (from inside the venv)

    python -m src.mapunfold

Tests

    pytest

## Notes

Update requirements:

    pip freeze > requirements.txt