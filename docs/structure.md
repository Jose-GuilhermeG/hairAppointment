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
                ├── hashEncrypt.py
                ├── repository.py
            └── 📁application
                └── 📁ports
                    ├── hashsEncrypt.py
                    ├── repository.py
                └── 📁use_cases
                    ├── userUseCases.py
                ├── __init__.py
            └── 📁domain
                ├── __init__.py
                ├── entities.py
                ├── enums.py
                ├── exceptions.py
            ├── __init__.py
        └── 📁configs
            ├── __init__.py
            ├── settings.py
        ├── __init__.py
        ├── main.py
    ├── .gitignore
    └── .pre-commit-config.yaml
```

## Folders functions:
- domain : business rules having entites as User and appoinment , exceptions , enums
- application : ports (topic of hexagonal Architecture ) as repository and hash , use cases (topic of clean Architecture)
- adapters : implementation of ports and controllers then uses the use cases , using fast api and another tools
- configs : has the application settings
