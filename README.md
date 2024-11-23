# PC Components Analysis
An application that get data of pc components then perform analysis on such data

### Architecture
![architecture](./architecture.svg)
- Bot1 collects the components and their according specifications (e.g. CPU and clock speed, num cores, etc). This will be the static information
- After getting the data from manufacturer websites or APIs, data gets normalized and added to database
- Bot2 will iterate through database and for each item, it will search for dynamic information (price, benchmark, yearly running cost, etc)
- Because there will unlikely be an APIs, we will use the LLM to try to extract the dynamic information
- Dynamic information will always be attached to a specific time, normalized then update to database
- Analysis using the data we have collected so far

### Conventions
- All the sizes will be converted to MB

### Running
First run could take up some time
```docker compose up -d```
