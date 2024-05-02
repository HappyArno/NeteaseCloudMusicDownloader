import downloader
import merge
import getopt
import sys
import codecs
help = \
r"""A program to download songs and lyrics from Netease Cloud Music (music.163.com)
Usage: python main.py <music_id(s)> [options]
Options:
  -h                        show SIMPLE help
  --help                    show DETAILED help
  -a/--audio                download audio
  -l/--lyric                download lyric
  -n/--noAction             download nothing, extremely useful when using with -d/--detail
  -o/--output <f-str1>      set output file name format
  --audioOutput <f-str1>    set output audio name format only
  --lyricOutput <f-str1>    set output lyric name format only
+     where <f-str1> is a python format string, and the following replacement fields are supported:
+       id: the id of the song
+       name: the name of the song
+       ar: the artist of the song
+       alia: the alias of the song
+       al: the album of the song
+       detail: the information json of the song
+         (You can use '--detail' to show the detailed information json of the music)
+       format: the format of the output file
+     eg:
+       -o "{name} - {ar}({alia}).{format}"
+       --audioOutput {name}({ar}).{format}
+       --audioOutput {detail[songs][0][tns][0]}.mp3
+       --lyricOutput {name}.lrc
  --lyricComposition <str>  set what the lyrics consist of
+     where <str> is an ordered sequence of the following characters:
+       l: lrc (original lyric)
+       k: klyric
+       t: tlyric (translated lyric)
+       r: romalrc (romanized lyric)
+     The final lyric will be synthesized from the lyrics you set
+     eg: --lyricComposition lt
  --lyricEncoding <name>    set lyric encoding
+     eg: --lyricEncoding gbk
  --lyricNewline <char>     set lyric newline characters
+     eg: --lyricNewline "\r\n"
  --detail                  show the detailed information json of the music"""
# Get options and arguments
if len(sys.argv) <= 1:
    print("Copyright (C) 2024 HappyArno")
    print("Try '-h' or '--help' option for more information.")
    exit()
try:
    opts, args = getopt.gnu_getopt(
        sys.argv[1:],
        "halno:d",
        ["help", "audio", "lyric", "noAction", "output=", "audioOutput=", "lyricOutput=", "lyricComposition=", "lyricEncoding=", "lyricNewline=", "detail"]
    )
except getopt.GetoptError as err:
    print(err)
    print("Try '-h' or '--help' option for more information.")
    exit(1)
# Parse options
config = {
    "downloadAudio": False,
    "downloadLyric": False,
    "noAction": False,
    "audioOutput": "{name}.{format}",
    "lyricOutput": "{name}.{format}",
    "lyricComposition": "l",
    "lyricEncoding": "utf-8",
    "lyricNewline": "\n",
    "showDetail": False,
}
for opt, arg in opts:
    if opt == "-h":
        for s in help.split("\n"):
            if s[0] != "+":
                print(s)
        exit()
    elif opt == "--help":
        for s in help.split("\n"):
            print(s if s[0] != "+" else " " + s[1:])
        exit()
    elif opt in ("-a", "--audio"):
        config["downloadAudio"] = True
    elif opt in ("-l", "--lyric"):
        config["downloadLyric"] = True
    elif opt in ("-n", "--noAction"):
        config["noAction"] = True
    elif opt in ("-o", "--output"):
        config["audioOutput"] = config["lyricOutput"] = arg
    elif opt == "--audioOutput":
        config["audioOutput"] = arg
    elif opt == "--lyricOutput":
        config["lyricOutput"] = arg
    elif opt == "--lyricComposition":
        config["lyricComposition"] = arg
    elif opt == "--lyricEncoding":
        config["lyricEncoding"] = arg
    elif opt == "--lyricNewline":
        config["lyricNewline"] = codecs.getdecoder("unicode_escape")(arg)[0]
    elif opt in ("-d", "--detail"):
        config["showDetail"] = True
    else:
        raise RuntimeError("Unknown option")
if not (config["downloadAudio"] or config["downloadLyric"] or config["noAction"]):
    print("WARNING: What to download is not specified")
    print("WARNING: Audio will be automatically downloaded")
    print("NOTE: Use -a/--audio to download audio and use -l/--lyric to download lyric")
    print("NOTE: Or use -n/--noAction to specify doing nothing")
    config["downloadAudio"] = True
# Parse arguments and download
if not args:
    print("ERROR: No input music id.")
    exit(1)
for id in args:
    if not id.isdigit():
        print(f"ERROR: '{id}' is not a music id.")
        continue
    detail = downloader.getDetail(id)
    if config["showDetail"]:
        print(detail)
    nameReplacementFields = {
        "id": detail["songs"][0]["id"],
        "name": detail["songs"][0]["name"],
        "ar": ",".join([i["name"] for i in detail["songs"][0]["ar"]]),
        "alia": ",".join(detail["songs"][0]["alia"]),
        "al": detail["songs"][0]["al"]["name"],
        "detail": detail,
    }
    if config["downloadAudio"]:
        with open(config["audioOutput"].format(**nameReplacementFields, format = "mp3"), "wb") as f:
            f.write(downloader.getAudio(id))
    if config["downloadLyric"]:
        lyrics = downloader.getLyric(id)
        lyric = []
        for c in config["lyricComposition"]:
            if c == "l":
                lyric.append(lyrics["lrc"]["lyric"])
            elif c == "k":
                lyric.append(lyrics["klyric"]["lyric"])
            elif c == "t":
                lyric.append(lyrics["tlyric"]["lyric"])
            elif c == "r":
                lyric.append(lyrics["romalrc"]["lyric"])
            else:
                print(f"WARNING: Unknown lyric mark '{c}'")
                print("WARNING: Skip")
        lyric = merge.merge(*lyric)
        with open(config["lyricOutput"].format(**nameReplacementFields, format = "lrc"),
                  "w",
                  encoding = config["lyricEncoding"],
                  newline = config["lyricNewline"]) as f:
            f.write(lyric)