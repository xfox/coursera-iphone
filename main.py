import re
import os
import subprocess

MP4BOX='/usr/local/bin/MP4Box'
MP4TAGS='mp4tags' # from mp4v2
COURSERADL='coursera-dl'


def main():
    path = '.'
    for chapter in os.listdir(path):
        chapther_path = os.path.join(path, chapter)
        if not os.path.isdir(chapther_path):
            continue
        for part in os.listdir(chapther_path):
            video_path = os.path.join(chapther_path, part)
            if not os.path.isdir(video_path):
                continue
            files = os.listdir(video_path)

            video_file = filter(lambda x: x.endswith('.mp4'), files)[0]
            srt_file = filter(lambda x: x.endswith('.srt'), files)[0]

            tags = {}
            tags['mp4tags'] = MP4TAGS
            tags['album'] = re.match('\d{2}\s-\s(.+)', chapter).group(1)
            tags['song'] = part

            matches = re.match('(\d+)\s-\s(\d+)\s', video_file)

            tags['season'] = matches.group(1)
            tags['episode'] = matches.group(2)
            tags['show'] = 'Coursera'

            video_file = os.path.join(video_path, video_file)
            srt_file = os.path.join(video_path, srt_file)

            command = '{mp4box} ' \
                '-add "{subtitle}":lang=eng:group=2:hdlr="sbtl:tx3g" ' \
                '"{video}"'

            params = {
                'mp4box': MP4BOX,
                'subtitle': srt_file,
                'video': video_file
            }

            run = command.format(**params)
            subprocess.call(run, shell=True)

            tags['video'] = video_file
            command = '{mp4tags} -i tvshow ' \
                      '-episode {episode} -season {season} ' \
                      '-show "{show}" -song "{song}" ' \
                      '-description "{album}" -album "{album}" ' \
                      '"{video}"'

            run = command.format(**tags)
            subprocess.call(run, shell=True)


if __name__ == "__main__":
    main()