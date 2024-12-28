import argparse
import asyncio
import logging
import os
import time

import aiohttp
from dotenv import load_dotenv

## Frames
from pipecat.frames.frames import EndFrame, LLMMessagesFrame

## Pipeline
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

## Processors
from pipecat.processors.aggregators.llm_response import (
    LLMAssistantResponseAggregator,
    LLMUserResponseAggregator,
)

## Services
from pipecat.services.openai import OpenAILLMService

# Pipecat
## Transports
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pipecat.vad.silero import SileroVADAnalyzer

## VAD
from pipecat.vad.vad_analyzer import VADParams

from backend.helpers import get_daily_config
from backend.processors import (
    CartesiaTerrify,
    DeepgramTerrify,
    ElevenLabsTerrify,
    TranscriptionLogger,
    XTTSTerrify,
)
from backend.prompts import LLM_BASE_PROMPT, LLM_INTRO_PROMPT

load_dotenv()

if os.environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


async def main(room_url, token=None, xtts=False, elevenlabs=False):
    async with aiohttp.ClientSession() as session:
        # -------------- Transport --------------- #

        transport = DailyTransport(
            room_url,
            token,
            "TerifAI",
            DailyParams(
                # audio_in_enabled=True,
                audio_out_enabled=True,
                # transcription_enabled=True,
                vad_enabled=True,
                vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
                vad_audio_passthrough=True,
            ),
        )

        logging.info("Transport created for room:" + room_url)

        # -------------- Services --------------- #

        stt_service = DeepgramTerrify()

        llm_service = OpenAILLMService(
            api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"
        )

        if xtts:
            logging.info("Using XTTS")
            tts_service = XTTSTerrify(
                aiohttp_session=session,
                voice_id="Claribel Dervla",
                language="en",
                base_url="https://deeptrust-ai-dev--xtts-xtts-web.modal.run",
            )
        elif elevenlabs:
            logging.info("Using ElevenLabs")
            tts_service = ElevenLabsTerrify(
                aiohttp_session=session,
                api_key=os.getenv("ELEVENLABS_API_KEY"),
            )
        else:
            logging.info("Using Cartesia")
            tts_service = CartesiaTerrify()

        # --------------- Setup ----------------- #

        message_history = [LLM_BASE_PROMPT]

        # We need aggregators to keep track of user and LLM responses
        llm_responses = LLMAssistantResponseAggregator(message_history)
        user_responses = LLMUserResponseAggregator(message_history)
        transcription_logger = TranscriptionLogger()

        # -------------- Pipeline ----------------- #

        pipeline = Pipeline(
            [
                # Transport user input
                transport.input(),
                # STT
                stt_service,
                # Transcription logger
                transcription_logger,
                # User responses
                user_responses,
                # LLM
                llm_service,
                # TTS
                tts_service,
                # Transport bot output
                transport.output(),
                # Assistant spoken responses
                llm_responses,
            ]
        )

        task = PipelineTask(
            pipeline,
            PipelineParams(
                allow_interruptions=True,
                enable_metrics=True,
                report_only_initial_ttfb=True,
            ),
        )

        # --------------- Events ----------------- #

        # When the first participant joins, the bot should introduce itself.
        @transport.event_handler("on_first_participant_joined")
        async def on_first_participant_joined(transport, participant):
            # Kick off the conversation.
            logging.info(f"Participant joined: {participant['id']}")
            transport.capture_participant_transcription(participant["id"])
            time.sleep(1)
            await task.queue_frame(LLMMessagesFrame([LLM_INTRO_PROMPT]))

        # When the participant leaves, we exit the bot.
        @transport.event_handler("on_participant_left")
        async def on_participant_left(transport, participant, reason):
            logging.info(f"Participant left: {participant['id']}")
            await task.queue_frame(EndFrame())

        # If the call is ended make sure we quit as well.
        @transport.event_handler("on_call_state_updated")
        async def on_call_state_updated(transport, state):
            if state == "left":
                await task.queue_frame(EndFrame())

        # --------------- Runner ----------------- #

        runner = PipelineRunner()

        await runner.run(task)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TerifAI Bot")
    parser.add_argument("--room_url", type=str, help="Room URL")
    parser.add_argument("--token", type=str, help="Token")
    parser.add_argument("--default", action="store_true", help="Default configurations")
    parser.add_argument("--xtts", action="store_true", help="Use XTTS")
    parser.add_argument("--elevenlabs", action="store_true", help="Use ElevenLabs")
    config = parser.parse_args()

    if config.default:
        config = get_daily_config()

    if config.room_url is None:
        raise ValueError("Room URL is required")

    asyncio.run(main(config.room_url, config.token, config.xtts, config.elevenlabs))
