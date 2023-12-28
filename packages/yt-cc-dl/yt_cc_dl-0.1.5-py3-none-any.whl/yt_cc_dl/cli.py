#!/usr/bin/env python
# coding: utf-8

import argparse

from .downloader import DownloadYoutubeSubtitles


def _opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('channel',
                        nargs='+',
                        help='Single or multiple YouTube channel URL(s)')
    parser.add_argument(
        '-o',
        '--output-dir',
        help='Output directory name or path (default: channel name)',
        type=str)
    parser.add_argument(
        '-l',
        '--languages',
        help='Comma-separated list of languages to download (can be regex). '
        'The list may contain "all" for all available languages. The language '
        'can be prefixed with a "-" to exclude it from the requested '
        'languages (e.g., all,-live_chat)',
        type=str,
        default='en')
    parser.add_argument(
        '-i',
        '--indent',
        help='Indentation size in the output JSON files (None by default)',
        type=int)
    parser.add_argument(
        '-r',
        '--rich-data',
        help='Add a unique index and include the title and thumbnail in every '
        'subtitle entry (useful for Meilisearch)',
        action='store_true')
    parser.add_argument('-d',
                        '--disable-multithreading',
                        help='Disable multithreading',
                        action='store_true')
    return parser.parse_args()


def main():
    args = _opts()
    args.languages = [x.strip() for x in args.languages.split(',')]
    multithreading = True
    if args.disable_multithreading:
        multithreading = False
    for channel in args.channel:
        dyts = DownloadYoutubeSubtitles(output_dir=args.output_dir,
                                        languages=args.languages,
                                        indent=args.indent)
        dyts.download_channel_subtitles(channel,
                                        rich_data=args.rich_data,
                                        multithreading=multithreading,
                                        languages=args.languages)


if __name__ == '__main__':
    main()
