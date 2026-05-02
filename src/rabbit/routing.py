#my_project/maxbot_rebbit/src/rabbit/routing.py
import json
from pathlib import Path
from typing import Dict, Tuple
from src.exceptions import RoutingConfigError


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
            raise RoutingConfigError(f"Не найден файл для создания карты роутинга: {self.path}")

        try:
            data = json.loads(self.path.read_text())
        except Exception as e:
            raise RoutingConfigError(f"from Не корретный routing.json: {e}")

        routes = data.get("routes", [])

        if routes is None:
            raise RoutingConfigError("В файле routing.json отсутствует поле «routes»")

        # (platform, chat_id) -> {platform, chat_id}
        self._map = {
            (r["from"]["platform"], r["from"]["chat_id"]): r["to"]
            for r in routes
        }

    def resolve(self, platform: str, chat_id: str) -> Dict | None:
        """
        Задаем источник , получаем кому предназначается.
        :param platform:
        :param chat_id:
        :return: {'platform': '...', 'chat_id': '...'}
        """
        return self._map.get((platform, chat_id))

if __name__ == "__main__":
    path_r = Path(__file__).parent.parent / "routing.json"
    router = Router(path_r)
    #print(router.resolve("max", "-72932271489781"))
    rout = router._map
    print(rout)
    for k, v in rout.items():
        print(k, v)