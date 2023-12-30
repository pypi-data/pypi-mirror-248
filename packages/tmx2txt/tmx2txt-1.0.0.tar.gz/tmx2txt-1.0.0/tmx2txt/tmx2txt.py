#!/usr/bin/env python
"""This script converts a tmx file to tab-delimited txt file."""

import os
import re
import time
import argparse
import xml.etree.ElementTree as ET


def build_trg_file_name(path):
    """Return the target file name."""
    head, tail = os.path.split(path)
    target_file_name = '{}.txt'.format(os.path.splitext(tail)[0])

    return head, target_file_name


def clean_text(text):
    """Return text with removed tabs, newlines, and carriage return chars."""
    # # Replace tabs with spaces and strip leading/trailing whitespace
    # text = text.replace('\t', ' ').strip()

    # # Remove newline and carriage return characters
    # text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'[\t\n\r]', r' ', text).strip()

    return text


def extract_tmx_content(tmx_file_path, langauge_codes='en-US#ru-RU'):
    """Extract TUs a tmx file."""
    src_lang_code, trg_lang_code = langauge_codes.split('#')
    src_lang_str = f"""tuv[@{{http://www.w3.org/XML/1998/namespace}}lang="{src_lang_code}"]"""
    trg_lang_str = f"""tuv[@{{http://www.w3.org/XML/1998/namespace}}lang="{trg_lang_code}"]"""
    tree = ET.parse(tmx_file_path)
    root = tree.getroot()
    src_trg_lst = []
    for tu in root.findall('.//tu'):
        try:
            src_tuv = tu.find(src_lang_str).find('seg')
            trg_tuv = tu.find(trg_lang_str).find('seg')
            src_text = ''.join(src_tuv.itertext()).strip('<b>').strip('</b>')
            trg_text = ''.join(trg_tuv.itertext()).strip('<b>').strip('</b>')
        except AttributeError as err:
            err_msg = 'CHECK YOUR LANGUAGE CODES! (MUST BE SEPERATED BY #)'
            print(err_msg)
            raise err

        src_text = clean_text(src_text)
        trg_text = clean_text(trg_text)
        src_trg_lst.append((src_text, trg_text))
    return src_trg_lst


def write_txt(dsn, tus):
    """Write TUs to file and return the number of lines written."""
    count = 0
    with open(dsn, 'w', encoding='utf-8') as to_f:
        for src, trg in tus:
            to_f.write(f'{src}\t{trg}\n')
            count += 1
    return count


def main():
    """Run the script."""
    description = """Tmx-to-txt converter. Accepts one bilingual tmx file and
    one optional argument containing langauge codes separated by
    the # symbol.  Examples: en-US#ar-SA; EN-US#RU-RU. All characters here
    are case sensitive. The default codes are en-US and ru-RU.
    The script extracts TU text only. No fields are extracted. The output
    is a bilingual tab-delimited txt file."""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('path', help='Provide your tmx file path')
    parser.add_argument(
        '-c',
        '--codes',
        help='Provide language codes (eg. EN-US#RU-RU)'
        )

    args = parser.parse_args()

    start_time = time.time()
    print(f'\nStart time: {time.strftime("%b %d %Y %H:%M:%S", time.localtime(start_time))}')

    if args.codes is not None:
        tus = extract_tmx_content(args.path, args.codes)
    else:
        tus = extract_tmx_content(args.path)

    head, target_file_name = build_trg_file_name(args.path)
    dsn = os.path.join(head, target_file_name)
    count = write_txt(dsn, tus)

    print(f'\n{count:,} TUs were extracted and written to {dsn}\n')

    print('-' * 20)
    print(f'Job completed in {(time.time() - start_time)/60:.2f} minutes')
    print('-' * 20)


if __name__ == "__main__":
    main()
