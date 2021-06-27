# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available

• `{i}unzip <reply to zip file>`
    unzip the replied file.
"""

import asyncio
import os
import time
import zipfile
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from . import *
import shutil
from telethon.tl.types import DocumentAttributeVideo,DocumentAttributeAudio


# HACK :)-----------------------------------------------


def open_zip(zip_yolu: str):
    with open(zip_yolu, 'rb') as zip_dosyasi:
        z = zipfile.ZipFile(zip_dosyasi, allowZip64=True)
        for eleman in z.infolist():
            try:
                return z.extract(eleman)
            except zipfile.error as hata:
                return hata

# HACK :)------------------------------------------------


def opened_zip(zip_yolu: str):
    for adres in os.walk(zip_yolu.split('.zip')[0]):
        # 2. İndex Dosyalara Denk Geliyor!
        if adres[2]:
            for dosya in adres[2]:
                return f"{adres[0]}/{dosya}"





@ultroid_cmd(pattern="unzip$")
async def _(ult):
    if not ult.is_reply:
        return await eor(ult, "`Reply to a Zipfile..`")
    gt = await ult.get_reply_message()
    msg = await eor(ult, "`Processing...`")
    if not (
        gt.media
        and gt.media.document
        and gt.media.document.mime_type == "application/zip"
    ):
        return await msg.edit("`Reply to a Zipfile...`")
    k = time.time()
    d = "resources/downloads/"
    dnl = await ultroid_bot.download_media(
        gt,
        d,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, msg, k, "Downloading to my Storage..."),
        ),
    )
    place = "resources/downloads/extracted/"
    shutil.unpack_archive(downloaded_file_name, extracted)
    files = [f for f in glob(dnl+"./**",
                                 recursive=True) if os.path.isfile(f)]
    filename = set(list(files))
    #with zipfile.ZipFile(dnl, "r") as zip_ref:
        #zip_ref.extractall(place)
    #filename = sorted(get_lst_of_files(place, []))
    await msg.edit("Unzipping now")
    THUMB = udB.get("THUMB_URL")
    Enum = 0
    Elist = "**Errors Occured while Unzip**\n\n"
    for single_file in filename:
        if os.path.exists(single_file):
            caption_rts = os.path.basename(single_file)
                force_document = False
                supports_streaming = True
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm",".jpeg",".jpg")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(
                            createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
            #caption_rts = os.path.basename(single_file)
            try:
                await ultroid_bot.send_file(
                    ult.chat_id,
                    single_file,
                    caption=f"`{caption_rts}`",
                    force_document=force_document,
                    supports_streaming=supports_streaming,
                    allow_cache=False,
                    attributes=document_attributes,
                    reply_to=ult.message.id,
                )
            except Exception as e:
                Enum += 1
                Elist += f"{Enum}. {caption_rts}\n- __{str(e)}__\n"
            os.remove(single_file)
    os.remove(dnl)
    await msg.edit(f"**Unzipped `{len(filename)-Enum}/{len(filename)}` Files**")
    if Enum > 0:
        if len(Elist) < 4096:
            await ultroid_bot.send_message(Var.LOG_CHANNEL, Elist)
        else:
            file = open("UnzipError.txt", "w").write(Elist)
            file.close()
            await ultroid_bot.send_message(
                Var.LOG_CHANNEL,
                "UnzipError.txt",
                caption=f"`Error Occured on Unzip cmd",
            )
            os.remove("UnzipError.txt")


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
