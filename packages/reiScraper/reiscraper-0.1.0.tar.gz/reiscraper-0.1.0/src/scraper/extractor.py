import pandas as pd
import json

from typing import Any
from os.path import join


class Extract(object):

    def to_csv(self, data: list[dict[str,Any]], filepath: str):
        df = pd.DataFrame(data=data)
        df.to_csv(filepath, index=False)
        return "Excel Generated at{}".format(filepath)
    
    def to_excel(self, data: list[dict[str,Any]], filepath: str):
        df= pd.DataFrame(data=data)
        df.to_csv(filepath, index=False)
        return "Excel Generated at{}".format(filepath)
    
    def to_json(self, data: list[dict[str,Any]], filepath: str):
        df = pd.DataFrame(data=data)
        df.to_json(filepath, orient='records', lines=True)
        return "JSON Generated at {}".format(filepath)