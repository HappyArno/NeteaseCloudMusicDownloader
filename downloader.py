import requests
def getDetail(id :int) -> dict:
    return requests.post(
        "https://music.163.com/api/v3/song/detail",
        data = {"c": str([{"id": id}])}
    ).json()
def getAudio(id: int) -> bytes:
    response = requests.get(
        "http://music.163.com/song/media/outer/url",
        params = {"id": id}
    )
    if not response.headers["Content-Type"].startswith("audio/"):
        raise RuntimeError("Not a audio")
    return response.content
def getLyric(id: int) -> dict:
    return requests.post(
        "https://music.163.com/api/song/lyric?_nmclfl=1",
        data = {"id": id, "tv": -1, "lv": -1, "rv": -1, "kv": -1}
    ).json()