import asyncio
import sys
from di.dependent import Dependent

from di.executors import AsyncExecutor
from python_orders.main.di_builder import build_di
from python_orders.presentation.qt.window_to_show_items import TableWindow
from PyQt5 import QtWidgets


async def main():
    di_container = await build_di()
    solved = di_container.solve(
        Dependent(TableWindow, scope="request"), scopes=["request"]
    )
    async with di_container.enter_scope("request") as state:
        app = QtWidgets.QApplication(sys.argv)
        return await solved.execute_async(executor=AsyncExecutor(), state=state), app
        mainWin.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    window, app = asyncio.run(main())
    window.show()
    sys.exit(app.exec_())
