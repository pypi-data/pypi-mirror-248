import asyncio
import json
from datetime import datetime, UTC

from _decimal import Decimal
from dataclass_factory import Factory
from di import Container
from python_orders.application.save_order.dto import SaveOrderDTO, OrderUserDTO, ItemDTO
from python_orders.application.save_order.use_case import SaveOrder
from python_orders.domain.models.email import Email

from python_orders.presentation.socket.config import SocketConfig
from python_orders.presentation.socket.dto import SaveOrderRequestDTO


class SocketServer:
    def __init__(
        self,
        config: SocketConfig,
        save_order: SaveOrder,
        factory: Factory,
        container: Container,
    ) -> None:
        self.__config = config
        self.__save_order = save_order
        self.__factory = factory
        self.__container = container

    async def run(self) -> None:
        server = await asyncio.start_server(
            self.__handle_client,
            self.__config.host,
            self.__config.port,
        )
        async with server:
            await server.serve_forever()

    async def __handle_client(self, reader, writer) -> None:
        request = None
        while request != "quit":
            request = await reader.read(9164)
            print(request)
            try:
                msg_dict = json.loads(request)
                print(msg_dict)
                request_dto = self.__factory.load(msg_dict, SaveOrderRequestDTO)
                print(request_dto)
                await self.__save_order(
                    SaveOrderDTO(
                        created_at=datetime.now(tz=UTC),
                        user=OrderUserDTO(
                            email=Email(request_dto.User.Email),
                        ),
                        items=[
                            ItemDTO(
                                name=item.Name,
                                price=Decimal(item.Price),
                                quantity=item.Count,
                            )
                            for item in request_dto.User.items
                        ],
                    )
                )
                writer.write("ok".encode("utf8"))
                await writer.drain()
            except Exception as e:
                writer.write("not ok".encode("utf8"))
                await writer.drain()
                raise e

        writer.close()
