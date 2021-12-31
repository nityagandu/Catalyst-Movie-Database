import json

class Serializable:
    def __init__(self) -> None:
        pass

    def toJSON(self) -> None:
        pass

    def toJSONStr(self) -> str:
        return json.dumps( self.toJSON() )