# Project Structure

this project is made with a mixture between Hexagonal Architecture and clean Architecture
having ports and adapters as a Hexagonal Architecture and use cases as clean Architecture
this system is divided in two Folders and files into src Folder :

- Configs (Folder)
- app (Folder)
- main.py (file)
- __init__.py (file)

## Structure
```
└── 📁haircutSystem
    └── 📁docs
        ├── architecture.drawio
        ├── entities.drawio
        ├── flux.md
        ├── structure.md
    └── 📁requirements
        ├── local.txt
        ├── production.txt
    └── 📁src
        └── 📁app
            └── 📁adapters
                └── 📁api
                    └── 📁dependencies
                        ├── __init__.py
                        ├── auth.py
                        ├── db.py
                        ├── repository.py
                        ├── services.py
                    └── 📁routers
                        ├── __init__.py
                        ├── userRouters.py
                    └── 📁schemas
                        ├── models.py
                        ├── serializers.py
                    ├── errsHandler.py
                    ├── middlewares.py
                ├── hashEncrypt.py
                ├── mapping.py
                ├── repository.py
            └── 📁application
                └── 📁ports
                    ├── cache.py
                    ├── hashsEncrypt.py
                    ├── mapping.py
                    ├── repository.py
                └── 📁use_cases
                    ├── userUseCases.py
                ├── __init__.py
            └── 📁domain
                ├── __init__.py
                ├── entities.py
                ├── enums.py
                ├── exceptions.py
                ├── genericValidations.py
            ├── __init__.py
        └── 📁configs
            ├── __init__.py
            ├── settings.py
        └── 📁tests
            └── 📁user_tests
                ├── adapters_tests.py
                ├── entities_tests.py
                ├── routes_tests.py
                ├── use_case_tests.py
            ├── __init__.py
            ├── conftest.py
        ├── __init__.py
        ├── main.py
    ├── .gitignore
    ├── .pre-commit-config.yaml
    └── pytest.ini
```

## Folders functions:
- domain : business rules having entites as User and appoinment , exceptions , enums
- application : ports (topic of hexagonal Architecture ) as repository and hash , use cases (topic of clean Architecture)
- adapters : implementation of ports and controllers then uses the use cases , using fast api and another tools
- configs : has the application settings
- tests : has the system tests
