# Service Identity for OK2SHIP

## Get Model from DB
```
uv run sqlacodegen "mssql+pyodbc://sa:YourStrong(!)Password@localhost:1433/OK2SHIP_SMT?driver=ODBC+Driver+17+for+SQL+Server" --outfile domain/models/generated_models.py
```