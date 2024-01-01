import logging
from string import Template

from PyQt6 import QtCore, QtNetwork, QtWidgets

from .abstract_input_dialog import (AbstractInputDialog,
                                    AbstractRequestInputDialog)
from .game_list import GameList

API_KEY_URL = "https://steamcommunity.com/dev/apikey"
TEST_STEAM_API_KEY_URL = Template("https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1"
                                  "?key=$api_key")
TEST_STEAM_ID_URL = Template("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2"
                             "?key=$api_key&steamids=$steam_id")


class SteamAPIKeyDialog(AbstractRequestInputDialog):
    """Prompts the user for their Steam API key"""

    TITLE = "Steam API Key"
    TEXT = f"Please enter your Steam API key (<a href='{API_KEY_URL}'>{API_KEY_URL}</a>):"
    INPUT_NAME = "key"

    def validate(self, text: str) -> bool:
        return len(text) == 32 and text.isalnum()

    def url(self, text: str) -> str:
        return TEST_STEAM_API_KEY_URL.substitute(api_key=text)

    def validate_reply(self, reply: QtNetwork.QNetworkReply) -> bool:
        return reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError


class SteamUserIdDialog(AbstractRequestInputDialog):
    """Prompts the user for their Steam ID"""

    TITLE = "Steam ID"
    TEXT = "Please enter your Steam ID:"
    INPUT_NAME = "Steam ID"

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key

    def validate(self, text: str) -> bool:
        return len(text) == 17 and text.isnumeric()

    def url(self, text: str) -> str:
        return TEST_STEAM_ID_URL.substitute(api_key=self.api_key, steam_id=text)

    def validate_reply(self, reply: QtNetwork.QNetworkReply) -> bool:
        if reply.error() != QtNetwork.QNetworkReply.NetworkError.NoError:
            return False
        text = reply.readAll().data().decode()
        return text != "{\"response\":{\"players\":[]}}"


class Settings(QtCore.QSettings):
    """Provides access to the application settings

    Settings:
        steam_api_key (str): Steam API key
        steam_user_id (str): Steam user ID
        game_list_cache (str): Cached game list
        selected_game (int): Selected game
        position (QtCore.QPoint): Window position
        size (QtCore.QSize): Window size

    Raises:
        RuntimeError: If a setting is not found and the user rejects the dialog

    Args:
        parent (QtWidgets.QWidget): Parent widget
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.define_if_not_exists("steam_api_key", SteamAPIKeyDialog())
        self.define_if_not_exists("steam_user_id", SteamUserIdDialog(self.value("steam_api_key")))

    def define_if_not_exists(self, key: str, dialog: AbstractInputDialog) -> None:
        """ Shows the dialog and sets the value if it is not already set

        Raises:
            RuntimeError: If the dialog is rejected

        Args:
            key (str): Key to check
            dialog (AbstractRequestInputDialog): Dialog to show
        """
        if not self.contains(key):
            logging.info(f"Setting {key} not found, prompting user")
            dialog.exec()
            if dialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
                self.setValue(key, dialog.input.text())
            else:
                raise RuntimeError(f"No {key} provided")

    @property
    def steam_api_key(self) -> str:
        """Loads the Steam API key from the settings

        Raises:
            TypeError: If the value is not a string

        Returns:
            str: Steam API key
        """
        value = self.value("steam_api_key", type=str)
        if not isinstance(value, str):
            raise TypeError("steam_api_key is not a string")
        return value

    @property
    def steam_user_id(self) -> str:
        """Set the Steam user ID in the settings

        Raises:
            RuntimeError: If the value is not a string

        Returns:
            str: Steam user ID
        """
        value = self.value("steam_user_id", type=str)
        if not isinstance(value, str):
            raise RuntimeError("steam_user_id is not a string")
        return value

    @property
    def game_list_cache(self) -> GameList | None:
        """Loads the game list from the settings or returns None if it is not set

        Raises:
            TypeError: If the value is not a dict

        Returns:
            GameList | None: Game list or None if it is not set
        """
        value = self.value("schemes", type=dict, defaultValue=None)
        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError("game_list is not a GameList")
        return value

    @game_list_cache.setter
    def game_list_cache(self, value: GameList) -> None:
        """Sets the game list in the settings

        Args:
            value (GameList): Game list to serialize
        """
        self.setValue("schemes", value)

    @property
    def selected_game(self) -> int | None:
        """Loads the selected game from the settings or returns None if it is not set

        Raises:
            TypeError: If the value is not an int

        Returns:
            int | None: Selected game or None if it is not set
        """
        value = self.value("selected_game", None, type=int)
        if value is None:
            return None
        if not isinstance(value, int):
            raise TypeError("selected_game is not an int")
        return value

    @selected_game.setter
    def selected_game(self, value: int) -> None:
        """Sets the selected game in the settings

        Args:
            value (int): Selected game
        """
        self.setValue("selected_game", value)

    @property
    def position(self) -> QtCore.QPoint | None:
        """Loads the window position from the settings or returns None if it is not set

        Raises:
            TypeError: If the value is not a QPoint

        Returns:
            QtCore.QPoint | None: Window position or None if it is not set
        """
        value = self.value("position", None, type=QtCore.QPoint)
        if value is None:
            return None
        if not isinstance(value, QtCore.QPoint):
            raise TypeError("position is not a QPoint")
        return value

    @position.setter
    def position(self, value: QtCore.QPoint) -> None:
        """Sets the window position in the settings

        Args:
            value (QtCore.QPoint): Window position
        """
        self.setValue("position", value)

    @property
    def size(self) -> QtCore.QSize | None:
        """Loads the window size from the settings or returns None if it is not set

        Raises:
            TypeError: If the value is not a QSize

        Returns:
            QtCore.QSize | None: Window size or None if it is not set
        """
        value = self.value("size", None, type=QtCore.QSize)
        if value is None:
            return None
        if not isinstance(value, QtCore.QSize):
            raise TypeError("size is not a QSize")
        return value

    @size.setter
    def size(self, value: QtCore.QSize) -> None:
        """Sets the window size in the settings

        Args:
            value (QtCore.QSize): Window size
        """
        self.setValue("size", value)
