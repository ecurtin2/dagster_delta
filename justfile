@lint:
    ruff {{justfile_directory()}}/dagster_delta
    ruff {{justfile_directory()}}/dagster_delta
    printf "\n-------------✅ ruff  ✅ -----------------------\n"
    black --check {{justfile_directory()}}/dagster_delta
    printf "\n-------------✅ black ✅ -----------------------\n"

@check: lint
    mypy {{justfile_directory()}}/dagster_delta
    printf "\n-------------✅ mypy  ✅ -----------------------\n"

@fix:
    black {{justfile_directory()}}/dagster_delta
    black {{justfile_directory()}}/tests
    ruff {{justfile_directory()}}/dagster_delta --fix
    ruff {{justfile_directory()}}/tests --fix

@docs:
    mkdocs build
    printf "\n-------------✅ mkdocs ✅ -----------------------\n"

@test:
    python -m pytest tests


@ci: check test docs
    echo '   | _ \ __ _    ___    ___    ___   __| |   | |'
    echo '   |  _// _` |  (_-<   (_-<   / -_) / _` |   |_|'
    echo '  _|_|_ \__,_|  /__/_  /__/_  \___| \__,_|  _(_)_'
    echo ' | """ _|"""""_|"""""_|"""""_|"""""_|"""""_| """ |'
    echo '  -0-0-  -0-0-  -0-0-  -0-0-  -0-0-  -0-0-  -0-0-'