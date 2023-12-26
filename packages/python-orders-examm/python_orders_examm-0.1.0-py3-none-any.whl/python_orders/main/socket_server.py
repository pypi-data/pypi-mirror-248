import asyncio
from di.dependent import Dependent
from python_orders.main.di_builder import build_di
from python_orders.presentation.socket.server import SocketServer

from di.executors import AsyncExecutor


async def main() -> None:
    di_container = await build_di()
    solved = di_container.solve(
        Dependent(SocketServer, scope="request"), scopes=["request"]
    )
    async with di_container.enter_scope("request") as state:
        server = await solved.execute_async(executor=AsyncExecutor(), state=state)
        await server.run()


if __name__ == "__main__":
    asyncio.run(main())
