# Vextor
The title of the project comes from a mix of the words _backtester_, _vector_ and _saxo_, since it was conceived of as a vectorized backtester connected to the [SaxoTrader](https://www.home.saxo/platforms/saxotrader) trading platform. At this point the project is more of a package containing a trading strategy base class, from which to implement quantitative trading rules, and a loop backtester. In the near future, a vectorized backtester will also be implemented, perhaps retiring the loop.

The package itself is a lightweight framework providing a simple interface for defining trading strategies and fast calculations of the equity curve and a range of quantitative metrics. The data, as well as the indicators derived from it, are calculated by hand and should be well defined for each point-in-time, and are passed through to the calculating objects, removing the need for the backtester to have any internal data itself. See the `examples` folder for examples on how to use the package.

Finally, to install the project from github

`pip install git+https://github.com/NicolaiBanke/Baxter.git`.
