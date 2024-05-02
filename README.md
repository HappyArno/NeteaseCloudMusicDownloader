# NeteaseCloudMusicDownloader

A program to download songs and lyrics from [Netease Cloud Music](https://music.163.com/).

## Usage

```
python main.py <music_id(s)> [options]
```

## Options

```
-h                        show SIMPLE help
--help                    show DETAILED help
-a/--audio                download audio
-l/--lyric                download lyric
-n/--noAction             download nothing, extremely useful when using with -d/--detail
-o/--output <f-str1>      set output file name format
--audioOutput <f-str1>    set output audio name format only
--lyricOutput <f-str1>    set output lyric name format only
    where <f-str1> is a python format string, and the following replacement fields are supported:
      id: the id of the song
      name: the name of the song
      ar: the artist of the song
      alia: the alias of the song
      al: the album of the song
      detail: the information json of the song
        (You can use '--detail' to show the detailed information json of the music)
      format: the format of the output file
    eg:
      -o "{name} - {ar}({alia}).{format}"
      --audioOutput {name}({ar}).{format}
      --audioOutput {detail[songs][0][tns][0]}.mp3
      --lyricOutput {name}.lrc
--lyricComposition <str>  set what the lyrics consist of
    where <str> is an ordered sequence of the following characters:
      l: lrc (original lyric)
      k: klyric
      t: tlyric (translated lyric)
      r: romalrc (romanized lyric)
    The final lyric will be synthesized from the lyrics you set
    eg: --lyricComposition lt
--lyricEncoding <name>    set lyric encoding
    eg: --lyricEncoding gbk
--lyricNewline <char>     set lyric newline characters
    eg: --lyricNewline "\r\n"
--detail                  show the detailed information json of the music
```

## Reference

[binaryify/NeteaseCloudMusicApi](https://gitlab.com/Binaryify/neteasecloudmusicapi)

## License

Copyright (C) 2024 HappyArno

This program is released under the [MIT](./LICENSE) license.