Student-Project
==============================

[![CI Pipeline](https://github.com/Edureka-AI/Student-Placement-Prediction/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Edureka-AI/Student-Placement-Prediction/actions/workflows/ci-cd.yml)

A short description of the project.

CI/CD
------------

This project includes a GitHub Actions workflow for continuous integration
and continuous deployment:

- CI runs on pull requests and pushes to main/master.
- CI validates linting and Python runtime compatibility.
- CD runs when a tag beginning with v is pushed, builds a package,
  uploads the artifact, and publishes to PyPI when credentials are set.

Workflow file:

- .github/workflows/ci-cd.yml
- GitHub repository: https://github.com/Edureka-AI/Student-Placement-Prediction
- GitHub Actions page: https://github.com/Edureka-AI/Student-Placement-Prediction/actions
- Run workflow page: https://github.com/Edureka-AI/Student-Placement-Prediction/actions/new

To enable PyPI deployment, add this repository secret in GitHub:

- PYPI_API_TOKEN

Example release flow:

1. Create and push a version tag like v0.1.1.
2. GitHub Actions runs CI then CD.
3. If PYPI_API_TOKEN is present, the package is published to PyPI.

To check the running status, open the GitHub Actions page and select
the latest CI Pipeline run. If you open a pull request, the same status also
appears in the PR checks panel.

Model Versioning Demonstration
------------

This project includes a hands-on demonstration for registering and managing
model versions with MLflow Model Registry.

Demo script:

- src/models/model_registry_demo.py

Run the demonstration from the project root:

1. Train a model to create a fresh MLflow run:

    python src/models/train_model.py

2. Register the latest run as a new model version (assigns alias candidate):

    python src/models/model_registry_demo.py register

3. List all registered versions and aliases:

    python src/models/model_registry_demo.py list

4. Promote a chosen version to production alias (example: version 3):

    python src/models/model_registry_demo.py set-alias --alias production --version 3

5. Load by alias or by fixed version:

    python src/models/model_registry_demo.py load --alias production

    python src/models/model_registry_demo.py load --version 3

Prediction service integration:

- By default, predictions load from models/model.pkl (existing behavior).
- To use a registry-managed version, set environment variables before running API:

  USE_MODEL_REGISTRY=true

  MODEL_REGISTRY_NAME=student-placement-model

  MODEL_REGISTRY_ALIAS=production

- With these variables set, src/models/predict_model.py loads the model from
  MLflow registry using models:/<name>@<alias>.

GitHub setup:

1. Create a GitHub repository.
2. Add the GitHub remote to this project.
3. Push the `master` branch so the workflow file exists on GitHub.
4. Open the repository's Actions tab to see the CI run status.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
