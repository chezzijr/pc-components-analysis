# PC Components Analysis
An application that get data of pc components then perform analysis on such data

### Architecture
![architecture](./architecture.svg)
- Bot1 collects the components and their according specifications (e.g. CPU and clock speed, num cores, num threads, etc). This will be the static information
- After getting the data from manufacturer websites or APIs, data gets normalized and added to database
- Bot2 will iterate through database and for each item, it will search for dynamic information (price, benchmark, yearly running cost, etc)
- Because there will unlikely be an APIs, we will use the LLM to try to extract the dynamic information
- Dynamic information will always be attached to a specific time, normalized then update to database
- Analysis using the data we have collected so far

### Components
We do not include the unnecessary properties that the majority of users will likely not care about
The list of components:
- `gpu`: Name, Released date, Bus, Memory, GPU clock, Memory clock
- `cpu`: Name, Codename, Cores, Clock, Socket, Process, TDP, Released

### Conventions
- All the sizes will be converted to MB

### Sources
[Tech Power Up](https://www.techpowerup.com)
