#my_project/maxbot_rebbit/src/rabbit/routing.py
import json
from pathlib import Path
from typing import Dict, Tuple

from src.exceptions import RoutingConfigError
from src.logging import log_state, logger


class Router:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._map: Dict[Tuple[str, str], Dict] = {}
        self.load()

    def load(self):
        """
        Превращаем routes → dict для O(1) lookup
        """

        if not self.path.exists():
            logger.error("routing_file_not_found path=%s", self.path)
            raise RoutingConfigError(f"Не найден файл routing: {self.path}")

        try:
            data = json.loads(self.path.read_text())
        except Exception as e:
            logger.error("routing_json_invalid error=%s", str(e))
            raise RoutingConfigError(f"Некорректный routing.json: {e}")

        routes = data.get("routes")

        if routes is None:
            logger.error("routing_missing_routes_field")
            raise RoutingConfigError("В routing.json отсутствует поле 'routes'")

        try:
            self._map = {
                (r["from"]["platform"], r["from"]["chat_id"]): r["to"]
                for r in routes
            }
        except Exception as e:
            logger.error("routing_invalid_structure error=%s", str(e))
            raise RoutingConfigError(f"Ошибка структуры routing.json: {e}")

        log_state("ROUTING_LOADED", routes_count=len(self._map))

    def resolve(self, platform: str, chat_id: str) -> Dict | None:
        """
        Получаем маршрут назначения
        """

        route = self._map.get((platform, chat_id))

        if not route:
            # это НЕ ошибка → это нормальная бизнес-ветка
            log_state("ROUTE_NOT_FOUND", platform=platform, chat_id=chat_id)

        return route