from dataclasses import dataclass
from datetime import date
from dateparser import parse


@dataclass
class Cpu():
    name : str
    code_name : str
    cores : int
    clock : int # in GHz
    max_clock : int # in GHz
    socket : str
    process : int # in nm
    tdp : int
    release : date

    def getAttributeFromDfRow(self, row):
        """Get attributes from a row of a dataframe
            Sample :
                "Name": "Core Ultra 7 265",
                "Codename": "Arrow Lake-S",
                "Cores": "20 ",
                "Clock": "2.4 to 5.3 GHz",
                "Socket": "Socket 1851",
                "Process": "7 nm",
                "L3 Cache": "33 MB",
                "TDP": "65 W",
                "Released": "Oct 2024"
            """
        
        self.name = row['name']
        self.code_name = row['code_name']
        self.cores = int(row['cores'])
        self.clock = float(row['clock'].split(" ")[0])
        self.max_clock = float(row['clock'].split(" ")[2])
        self.socket = row['socket']
        self.process = int(row['process'].split(" ")[0])
        self.tdp = int(row['tdp'].split(" ")[0])
        self.release = date(parse(row['release']))
    
    def toDict(self):
        return {
            "name": self.name,
            "code_name": self.code_name,
            "cores": self.cores,
            "clock": self.clock,
            "max_clock": self.max_clock,
            "socket": self.socket,
            "process": self.process,
            "tdp": self.tdp,
            "release": self.release.strftime("%m/%d/%Y")
        }