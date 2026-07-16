from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from commands import keyboard as keyboard_commands
from commands import mouse, volume, windows


class CommandExecutionError(Exception):
    pass


@dataclass(frozen=True)
class CommandSpec:
    name: str
    handler: Callable[..., None]
    description: str


class CommandExecutor:
    """Executes normalized commands from fuzzy matching or AI interpretation."""

    def __init__(self) -> None:
        self._commands: dict[str, CommandSpec] = {}
        self._register_defaults()

    def register(self, name: str, handler: Callable[..., None], description: str) -> None:
        self._commands[name] = CommandSpec(name, handler, description)

    def execute(self, command: str, **params: Any) -> None:
        if command not in self._commands:
            raise CommandExecutionError(f"Comando desconhecido: {command}")
        self._commands[command].handler(**params)

    def execute_intent(self, intent: dict[str, Any]) -> None:
        command = intent.get("command")
        if not isinstance(command, str) or not command:
            raise CommandExecutionError("Intent sem campo 'command'.")
        params = {key: value for key, value in intent.items() if key != "command"}
        self.execute(command, **params)

    def available_commands(self) -> list[str]:
        return sorted(self._commands)

    def _register_defaults(self) -> None:
        self.register("space", lambda: keyboard_commands.press_key("space"), "Pressiona espaco")
        self.register("enter", lambda: keyboard_commands.press_key("enter"), "Pressiona Enter")
        self.register("esc", lambda: keyboard_commands.press_key("esc"), "Pressiona Esc")
        self.register("tab", lambda amount=1: keyboard_commands.press_key("tab", amount), "Pressiona Tab")
        self.register("key", lambda key: keyboard_commands.press_key(key), "Pressiona uma tecla comum")
        self.register("alt_f4", windows.alt_f4, "Fecha a janela atual")
        self.register("ctrl_c", lambda: keyboard_commands.hotkey("ctrl", "c"), "Copia")
        self.register("ctrl_v", lambda: keyboard_commands.hotkey("ctrl", "v"), "Cola")
        self.register("ctrl_z", lambda: keyboard_commands.hotkey("ctrl", "z"), "Desfaz")
        self.register("nexttrack", lambda: keyboard_commands.press_key('nexttrack'), "Avanca musica")
        self.register("prevtrack", lambda: keyboard_commands.press_key("prevtrack"), "Volta musica")
        self.register("playpause", lambda: keyboard_commands.press_key("playpause"), "Pausar musica")
        self.register("fullscreen", lambda: keyboard_commands.press_key("f"), "Alterna tela cheia em players")
        self.register("video_forward", lambda amount=1: keyboard_commands.press_key("right", amount), "Avanca video")
        self.register("video_back", lambda amount=1: keyboard_commands.press_key("left", amount), "Volta video")
        self.register("volume_up", volume.volume_up, "Aumenta volume")
        self.register("volume_down", volume.volume_down, "Diminui volume")
        self.register("set_volume", volume.set_volume, "Define volume")
        self.register("mute", volume.mute, "Silencia volume")
        self.register("open_program", windows.open_program, "Abre programa")
        self.register("close_program", windows.close_program, "Fecha programa")
        self.register("shutdown", windows.shutdown, "Desliga o computador")
        self.register("restart", windows.restart, "Reinicia o computador")
        self.register("mouse_click", mouse.click, "Clique do mouse")
