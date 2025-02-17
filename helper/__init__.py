# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

from .images import split_image, draw_statics  # noqa
from pyrogram.types import InputMediaPhoto
from typing import Iterator, List
from .printer import Printer  # noqa
from pathlib import Path
import asyncio


async def settings_parser(link: str, inline_keyboard: list) -> Printer:
    """Function to parse render settings from inline-keyboard."""
    split, resolution = False, ""
    for settings in inline_keyboard:
        text = settings[0].text
        if "Format" in text:
            if "PDF" in text:
                _format = "pdf"
            else:
                _format = "png" if "PNG" in text else "jpeg"
        if "Page" in text:
            page_value = True if "Full" in text else False
        if "Scroll" in text:
            if "No" in text:
                scroll_control = None
            elif "Auto" in text:
                scroll_control = False
            elif "Manual" in text:
                scroll_control = True
        if "Split" in text:
            split = True if "Yes" in text else False
        if "resolution" in text:
            resolution = text
        await asyncio.sleep(0.00001)
    printer = Printer(_format, link)  # type: ignore
    printer.scroll_control = scroll_control
    printer.fullpage = page_value
    printer.split = split
    if resolution:
        if "1280" in resolution:
            printer.resolution = {"width": 1280, "height": 720}
        elif "2560" in resolution:
            printer.resolution = {"width": 2560, "height": 1440}
        elif "640" in resolution:
            printer.resolution = {"width": 640, "height": 480}
    return printer


def mediagroup_gen(loc: List[Path]) -> Iterator[List[InputMediaPhoto]]:
    """Generator function that yields 10 InputMediaPhoto at a time."""
    media_group = [
        InputMediaPhoto(image, str(count)) for count, image in enumerate(loc, start=1)
    ]
    for i in range(0, len(media_group), 10):
        yield media_group[i : i + 10]  # noqa: E203


def inject_reader() -> str:
    """Function to read string from file."""
    r_string = ""
    with open(Path("assets", "inject.js")) as f:
        r_string = f.read()
    return r_string
