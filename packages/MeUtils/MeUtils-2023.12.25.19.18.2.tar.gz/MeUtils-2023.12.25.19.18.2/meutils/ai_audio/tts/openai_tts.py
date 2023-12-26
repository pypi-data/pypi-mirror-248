#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_asr
# @Time         : 2023/11/23 13:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE'),
    max_retries=3
)

_ = client.audio.speech.create(input="你好哇", model="tts-1", voice="alloy")

_.stream_to_file("hi.wav")
