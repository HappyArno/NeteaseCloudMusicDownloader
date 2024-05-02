from decimal import Decimal
# One line of lyrics
class Line:
    def __init__(self, min: str, sec: str, text: str) -> None:
        self.min, self.sec = Decimal(min), Decimal(sec)
        self.text = text
    def parse(lyric: str) -> object:
        try:
            timeTag = lyric[:lyric.index("]")]
            min, sec = timeTag[timeTag.index("[") + 1:].split(":", 1)
            return Line(min, sec, lyric)
        except:
            return Line("-1", "-1", lyric)
    def __str__(self) -> str:
        return self.text
    def __eq__(self, value: object) -> bool:
        return self.text == value.text
    def __lt__(self, value: object) -> bool:
        return (self.min, self.sec) < (value.min, value.sec)
def merge(*lyrics: str) -> str:
    ret = []
    # Merge
    for lyric in lyrics:
        ret.extend([Line.parse(i) for i in lyric.split('\n') if i != ""])
    # Sort
    ret = sorted(ret)
    # Deduplicate
    for i in range(len(ret) - 1, -1, -1):
        if ret.count(ret[i]) > 1:
            ret.pop(i)
    # Return
    return "\n".join([str(i) for i in ret])