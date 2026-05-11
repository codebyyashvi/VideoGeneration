#!/usr/bin/env python
"""
Launcher script for Windows compatibility with Playwright.
Sets the event loop policy before uvicorn starts.
"""
import sys
import asyncio

# Windows event loop fix for Playwright subprocess support
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
