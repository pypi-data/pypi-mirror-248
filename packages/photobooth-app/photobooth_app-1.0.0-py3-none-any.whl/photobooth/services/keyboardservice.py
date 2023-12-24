# pylint: disable=too-few-public-methods
"""
submit events on keypress to take photos

tested following libs:
keyboard: works seamless in win/linux but needs sudo on linux, not maintained actually
pynput: works seamless in win/linux but needs sudo on linux, not working when started as service
pygame: seems to rely on x11/video for input (not avail in service on linux)
hid: untested, needs additional libraries on win/linux to be installed
evdev: linux only
sshkeyboard: ?
"""


from ..appconfig import AppConfig
from ..utils.exceptions import ProcessMachineOccupiedError
from ..vendor.packages.keyboard import keyboard
from .baseservice import BaseService
from .mediacollection.mediaitem import MediaItem
from .mediacollectionservice import MediacollectionService
from .printingservice import PrintingService
from .processingservice import ProcessingService
from .sseservice import SseService


class KeyboardService(BaseService):
    """_summary_"""

    def __init__(
        self,
        config: AppConfig,
        sse_service: SseService,
        processing_service: ProcessingService,
        printing_service: PrintingService,
        mediacollection_service: MediacollectionService,
    ):
        super().__init__(config=config, sse_service=sse_service)

        self._processing_service = processing_service
        self._printing_service = printing_service
        self._mediacollection_service = mediacollection_service

        self._started = False

    def start(self):
        if self._config.hardwareinputoutput.keyboard_input_enabled:
            self._logger.info("keyboardservice enabled - listeners installed")
            try:
                keyboard.on_press(self._on_key_callback)
                self._started = True
            except Exception as exc:
                self._logger.exception(exc)
                self._logger.error("error registering callbacks, check system config")
        else:
            self._logger.info("keyboardservice not enabled - enable for keyboard triggers")

    def stop(self):
        self._started = False

    def is_started(self) -> bool:
        return self._started

    def _on_key_callback(self, key):
        """_summary_

        Args:
            key (_type_): _description_
        """
        self._logger.debug(f"key '{key.name}' triggered.")

        if key.name == self._config.hardwareinputoutput.keyboard_input_keycode_takepic:
            self._logger.info(f"got key.name={self._config.hardwareinputoutput.keyboard_input_keycode_takepic}")
            self._logger.info("trigger start_job_1pic")

            try:
                self._processing_service.start_job_1pic()
            except ProcessMachineOccupiedError as exc:
                # raised if processingservice not idle
                self._logger.warning(f"only one capture at a time allowed, request ignored: {exc}")
            except Exception as exc:
                # other errors
                self._logger.critical(exc)

        if key.name == self._config.hardwareinputoutput.keyboard_input_keycode_takecollage:
            self._logger.info(f"got key.name={self._config.hardwareinputoutput.keyboard_input_keycode_takecollage}")
            self._logger.info("trigger start_job_collage")

            try:
                self._processing_service.start_job_collage()
            except ProcessMachineOccupiedError as exc:
                # raised if processingservice not idle
                self._logger.warning(f"only one capture at a time allowed, request ignored: {exc}")
            except Exception as exc:
                # other errors
                self._logger.critical(exc)

        if key.name == self._config.hardwareinputoutput.keyboard_input_keycode_print_recent_item:
            self._logger.info(f"got key.name={self._config.hardwareinputoutput.keyboard_input_keycode_print_recent_item}")
            self._logger.info("trigger _print_recent_item")

            try:
                mediaitem: MediaItem = self._mediacollection_service.db_get_most_recent_mediaitem()
                self._printing_service.print(mediaitem=mediaitem)
            except BlockingIOError:
                self._logger.warning(f"Wait {self._printing_service.remaining_time_blocked():.0f}s until next print is possible.")
            except Exception as exc:
                # other errors
                self._logger.critical(exc)
