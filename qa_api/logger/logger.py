"""Logger engine"""

from logging import Logger, FileHandler, Formatter, INFO
import os


class CustomLogger(Logger):
    """Create logs"""

    def __init__(self, name: str) -> None:
        """Logger base settings"""

        super().__init__(name)
        self.setLevel(INFO)

        os.makedirs('logger/logs', exist_ok=True)
        self._handler: FileHandler = FileHandler(filename=f"logger/logs/{name}.log", mode='w')
        self._formatter: Formatter = Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        self._handler.setFormatter(self._formatter)
        self.addHandler(self._handler)


logger = CustomLogger("qa_api")
