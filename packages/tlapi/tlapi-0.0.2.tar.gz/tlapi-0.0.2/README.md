# TLAPI

![Static Badge](https://img.shields.io/badge/fork-opentele-blue)
![Static Badge](https://img.shields.io/badge/customize-HashemDalijeh-red)
![Static Badge](https://img.shields.io/badge/version-0.0.1-yellow)

A **Python Telegram API Library** for converting between **tdata** and **telethon** sessions, with built-in **official Telegram APIs**. [**Read the documentation**](https://opentele.readthedocs.io/en/latest/documentation/telegram-desktop/tdesktop/).

## Features
- **[tlapi]** - add random app version
- **[tlapi]** - add new Api ID - Api Hash
- **[opentele]** - Convert [Telegram Desktop](https://github.com/telegramdesktop/tdesktop) **tdata** sessions to [telethon](https://github.com/LonamiWebs/Telethon) sessions and vice versa.
- **[opentele]** - Use **telethon** with [official APIs](#authorization) to avoid bot detection.
- **[opentele]** - Randomize [device info](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/#generate) using real data that recognized by Telegram server.

## Dependencies

- [telethon](https://github.com/LonamiWebs/Telethon) - Widely used Telegram's API library for Python.
- [tgcrypto](https://github.com/pyrogram/tgcrypto) - AES-256-IGE encryption to works with `tdata`.
- [pyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Used by Telegram Desktop to streams data from files.

## Installation
- Install from [PyPI](https://pypi.org/project/tlapi/):
```pip title="pip"
pip install --upgrade tlapi
```

## Examples
The best way to learn anything is by looking at the examples. Am I right?

- Example on [readthedocs](https://opentele.readthedocs.io/en/latest/examples/)
