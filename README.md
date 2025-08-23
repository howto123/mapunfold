# mapunfold

Database name: mapunfold.db

## Visualization

Change to the folder `visualize`.

There is a dedicated README.


## Ollama container

Pull and start the container:

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Or, if the container already exists:

    docker start ollama

The model needs to be installed, e.g. llama2:

    docker exec -it ollama ollama pull llama2

Helpful link: https://collabnix.com/setting-up-ollama-models-with-docker-compose-a-step-by-step-guide/

Note that this should not be empty after installing a model: `http://localhost:11434/api/tags`.


## Command line tool

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

`test_get_description_runs` is a test that is suitable for experimenting.

`llama2` as a model did give too short answers or invald json if the length 
was more explicitly asked in the prompt. Conclusion: generating all four languages 
at once probably is not the right approach.