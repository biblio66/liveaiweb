#!/usr/bin/env python
#
# Copyright (C) 2025 Salahuddin <salahuddin66@bell01.com>
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>.


import asyncio
import time
from websockets.asyncio.server import serve
import re

import anthropic
from anthropic.types import TextBlockParam

ai_warning_message = "<head>AI-Generated Content Notice: This content was created using live artificial intelligence.</head>"
website_content_message = "Generate a blog with first post hello world. It will have menu Home and about us. Generate only Home page <body> html code. local html link should follow demo.html?q= format. Please add css color light blue."

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="",
)

async def ai_web(websocket):
    async for message in websocket:
        if message == "/demo":
            plaintext = "loading ai..."
            await websocket.send(plaintext)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": website_content_message }
                ]
            )

            for content_block in message.content:
                if content_block.type == "text":
                    print(content_block.text)
                    #index = content_block.text.find("<body")
                    x = re.search("<body.*>", content_block.text) 
                    if x:
                        index = x.end()
                        await websocket.send(ai_warning_message + content_block.text[index:])
                    else:
                        await websocket.send(content_block.text)
        else:
            await websocket.send("no logic")


async def main():
    async with serve(ai_web, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
