#!/usr/bin/env python
# coding: utf-8

import concurrent.futures
import json
import re
import shutil
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import yt_dlp
from loguru import logger
from tqdm import tqdm


class DownloadYoutubeSubtitles:

    def __init__(self,
                 output_dir: Optional[str] = None,
                 languages: list = ['en'],
                 indent: Optional[int] = None):
        self.output_dir = output_dir
        self.languages = languages
        self.indent = indent
        self.failed = []
        self.logger = self._logger()

    @staticmethod
    def _logger():
        logger.remove()
        logger.add(
            sys.stderr,
            format='{level.icon} <fg #3bd6c6>{time:HH:mm:ss}</fg #3bd6c6> | '
            '<level>{level: <8}</level> | '
            '<fg #f1fa8c>ln:{line: <4}</fg #f1fa8c> - <lvl>{message}</lvl>',
            level='DEBUG')
        logger.level('WARNING', color='<yellow><bold>', icon='🚧')
        logger.level('INFO', color='<bold>', icon='🚀')
        return logger

    def _keyboard_interrupt_handler(self, sig: int, _) -> None:
        self.logger.warning(
            f'\nKeyboardInterrupt (id: {sig}) has been caught...')
        self.logger.warning('Terminating the session gracefully...')
        for tmp_file in Path('.').glob('*.vtt.part'):
            tmp_file.unlink()
        sys.exit(1)

    def _check_output_dir(self) -> None:
        if self.output_dir:
            Path(self.output_dir).mkdir(exist_ok=True)
        else:
            self.output_dir = '.'

    @staticmethod
    def _time_to_seconds(time_obj: datetime.time) -> int:
        return (time_obj.hour * 60 + time_obj.minute) * 60 + time_obj.second


    def download_subtitles(self,
                           entry: dict,
                           skip_downloaded: bool = True,
                           save_to_id_dir: bool = False,
                           additional_options: Optional[dict] = None,
                           **kwargs):

        self._check_output_dir()

        video_id = entry['id']
        video_url = entry['url']
        self.logger.debug(f'[{video_id}] Started...')

        output_dir = Path(self.output_dir)
        if save_to_id_dir:
            output_dir = output_dir / video_id
            output_dir.mkdir(exist_ok=True, parents=True)

        output_file_format = str(Path(f'{output_dir}/%(id)s.%(ext)s'))
        existing_files_pattern = str(Path(f'{output_dir}/{video_id}.*.vtt'))

        yt_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'subtitleslangs': self.languages,
            'quiet': True,
            'noprogress': True,
            'outtmpl': {
                'subtitle': output_file_format,
                'infojson': output_file_format
            },
            'writeinfojson': True,
            'clean_infojson': True
        }

        if additional_options:
            yt_opts.update(**additional_options)

        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            if skip_downloaded and len(
                    list(Path('.').glob(existing_files_pattern))) == len(
                        yt_opts.get('subtitleslangs')):
                self.logger.warning(
                    f'[{video_id}] Already downloaded! Skipping...')
                return

            try:
                return_code = ydl.download(video_url)
            except yt_dlp.utils.DownloadError as e:
                logger.error(e)
                return
            if return_code != 0 or len(
                    list(Path('.').glob(existing_files_pattern))) != len(
                        yt_opts.get('subtitleslangs')):
                self.logger.debug(
                    f'[{video_id}] Downloading auto-subtitles...')
                yt_opts['writeautomaticsub'] = yt_opts.pop('writesubtitles')
                return_code = ydl.download(video_url)
                if return_code != 0:
                    self.logger.error(
                        f'[{video_id}] None-zero return code for URL: '
                        f'{video_url} (return code: {return_code})!')

        current_existing_files = list(Path('.').glob(existing_files_pattern))

        if not current_existing_files:
            self.logger.error(
                f'[{video_id}] Could not find subtitles for the requested '
                'language(s)!')
            self.failed.append(video_id)

            if save_to_id_dir:
                if video_id == Path(output_dir).name:
                    shutil.rmtree(output_dir)
        else:
            self.logger.debug(f'[{video_id}] Finished.')
            return output_dir

    @staticmethod
    def get_channel_data(channel_url: str) -> tuple:
        yt_opts = {
            'skip_download': True,
            'extract_flat': True,
            'quiet': True,
            'noprogress': True
        }

        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            info_dict = ydl.extract_info(channel_url)
        return info_dict

    def parse_vtt(self,
                  vtt_file: Union[Path, str],
                  info_file: Union[Path, str],
                  rich_data: bool = False,
                  **kwargs) -> list:

        if not Path(vtt_file).exists() or not Path(info_file).exists():
            video_id = Path(Path(vtt_file).stem).stem
            self.logger.error(
                f'[{video_id}] Could not find `*.vtt` and/or `*.info` '
                'file(s)! Skipping...')
            self.failed.append(video_id)
            return

        with open(vtt_file) as f:
            _lines = f.read().splitlines()

        with open(info_file) as j:
            info = json.load(j)

        lines = {}
        n = -1

        for _line in _lines:
            if not _line:
                continue

            ts_pattern = r'^\d{2}:\d{2}:\d{2}.\d{3}\s-->\s\d{2}:\d{2}:\d{2}.\d{3}'  # noqa
            if re.match(ts_pattern, _line):
                line = _line.replace(' align:start position:0%', '')
                line = re.sub(r'\sposition.+%', '', line)
                n += 1
                lines[n] = {'timestamp': line, 'caption': []}
                continue

            line = re.sub(r'<\d{2}:\d{2}:\d{2}.\d{3}><c>', '', _line)
            line = line.replace('</c>', '').strip()
            if n != -1 and line:
                for x in lines[n]['caption']:
                    if line.startswith(x):
                        lines[n]['caption'].remove(x)

                lines[n]['caption'].append(line)

        data = {}
        n = 0
        for k, v in lines.items():
            if k + 1 == len(lines):
                break
            current_caption = lines[k]['caption']
            next_caption = lines[k + 1]['caption']
            lines[k]['caption'] = [
                x for x in current_caption if x not in next_caption
            ]
            if v['caption']:
                lines[k]['caption'] = ' '.join(current_caption).replace(
                    '&nbsp;', ' ')
                data.update({n: v})
                n += 1

        thumb = [
            x['url'] for x in info['thumbnails']
            if 'maxresdefault.webp' in x['url']
        ]
        if thumb:
            thumb = thumb[0]
        data_timestamped = []

        for k, v in data.items():
            d = {}
            date = info['upload_date']
            start, end = v['timestamp'].split(' --> ')
            try:
                start = datetime.strptime(f'{date} {start}',
                                          '%Y%m%d %H:%M:%S.%f')
                end = datetime.strptime(f'{date} {end}', '%Y%m%d %H:%M:%S.%f')
            except ValueError:
                self.logger.error(
                    f'Could not parse the date {v["timestamp"]} in file '
                    f'{vtt_file}! Skipping the caption at index no. {k}...')
                continue

            start_in_seconds = self._time_to_seconds(start.time())
            ts_url = f'https://youtu.be/{info["id"]}&t={start_in_seconds}'

            d = {
                '_id': start.timestamp(),
                'video_id': info['id'],
                'title': info['title'],
                'date': str(start.date()),
                'timestamp_start': str(start.time()),
                'timestamp_end': str(end.time()),
                'timestamp_start_seconds': start_in_seconds,
                'caption': v['caption'],
                'timestamped_url': ts_url
            }

            if rich_data:
                d = {
                    '_id': d['_id'],
                    **d,
                    'thumbnail': thumb
                }
            data_timestamped.append(d)
        return data_timestamped

    def _process_channel_entry(self, entry: dict, **kwargs) -> None:
        try:
            current_output_dir = self.download_subtitles(entry,
                                                         save_to_id_dir=True,
                                                         **kwargs)
        except KeyError as e:
            self.logger.error(f'Encountered an error with entry: {entry}')
            self.logger.error(e)
            return

        if not current_output_dir:
            return

        video_id = entry['id']

        info_file = Path(f'{current_output_dir}/{video_id}.info.json')
        subs_json_file = Path(f'{current_output_dir}/{video_id}.subs.json')

        for lang in self.languages:
            vtt_file = Path(f'{current_output_dir}/{video_id}.{lang}.vtt')
            if not Path(vtt_file).exists():
                continue
            subs_list = self.parse_vtt(vtt_file, info_file, **kwargs)
            if not subs_list:
                return
            with open(subs_json_file, 'w') as j:
                json.dump(subs_list, j, indent=self.indent)

    def download_channel_subtitles(self,
                                   channel_url: str,
                                   multithreading: bool = False,
                                   **kwargs):

        signal.signal(signal.SIGINT, self._keyboard_interrupt_handler)

        self.logger.info(f'Processing channel: {channel_url}')
        if not self.output_dir:
            self.output_dir = f'{Path(channel_url).name}_subtitles'.replace(
                '@', '')
        self._check_output_dir()

        channel_data = self.get_channel_data(channel_url)

        with open(f'{self.output_dir}/meta.json', 'w') as j:
            json.dump(channel_data, j, indent=self.indent)

        channel_entries = sum([x['entries'] for x in channel_data['entries']],
                              [])

        for entry in channel_entries:
            if 'shorts' in entry['url']:
                entry['is_shorts'] = True
            else:
                entry['is_shorts'] = False

        if not multithreading:
            for entry in tqdm(channel_entries):
                self._process_channel_entry(entry, **kwargs)
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                _ = list(
                    tqdm(executor.map(
                        lambda entry: self._process_channel_entry(
                            entry, **kwargs), channel_entries),
                         total=len(channel_entries)))

        with open(Path(self.output_dir) / 'failed.json', 'w') as j:
            failed_dict = {'count': len(self.failed), 'ids': self.failed}
            json.dump(failed_dict, j, indent=self.indent)
