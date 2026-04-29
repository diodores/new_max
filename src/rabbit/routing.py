#my_project/maxbot_rebbit/src/rabbit/routing.py
import json
from pathlib import Path
from typing import Optional, Dict, Tuple


class Router:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._map: Dict[Tuple[str, str], Dict] = {}
        self.load()

    def load(self):
        """
        способ превратить список routes в словарь для поиска по ключу.
        :return: {('platform', 'chat_id') --> {'platform':'...', 'chat_id':'...'} и т.д
        """
        if not self.path.exists():
            raise RuntimeError(f"Routing file not found: {self.path}")

        data = json.loads(self.path.read_text())

        routes = data.get("routes", [])

        # быстрый lookup:
        # (platform, chat_id) -> {platform, chat_id}
        self._map = {
            (r["from"]["platform"], r["from"]["chat_id"]): r["to"]
            for r in routes
        }

    def resolve(self, platform: str, chat_id: str) -> Optional[Dict]:
        """
        Задаем источник , получаем кому предназначается.
        :param platform:
        :param chat_id:
        :return: {'platform': '...', 'chat_id': '...'}
        """

        return self._map.get((platform, chat_id))

# if __name__ == "__main__":
#     path_r = Path(__file__).parent.parent / "routing.json"
#     router = Router(path_r)
#     print(router.resolve("max", "-72932271489781"))
#     print(router._map)