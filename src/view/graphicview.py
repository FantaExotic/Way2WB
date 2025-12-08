from model.model import Model
import matplotlib.pyplot as plt
from view.mainview import Mainview
from model.tickerwrapper import TickerWrapper
import matplotlib.dates as mdates

class Graphicview:
    def __init__(self, model: Model, mainview: Mainview):
        self.model = model
        self.mainview = mainview
        self.currentTimezone = 'Etc/GMT-2'

    #TODO: change self.model.tickerwrappers to symbollist, because we want to analyze only those, where hook is set at checkbox
    def initstaticGraph(self, symbollist: list) -> None:
        """Initialize the static graph for each symbol and apply timezone conversion to +02:00."""
        plt.figure(figsize=(10, 6))
        for symbol in symbollist:
            tickerwrapper = self.model.tickerwrappers[symbol]
            tickerwrapper: TickerWrapper

            # Get 'Close' prices for the current ticker
            close_prices = tickerwrapper.tickerhistory["current"]['Close']

            # Convert the timezone of the index to +02:00 (assuming the index is timezone-aware)
            if close_prices.index.tz is not None:
                close_prices.index = close_prices.index.tz_convert(self.currentTimezone)  # Convert to +02:00 timezone

            # Plot shortName for graph of dataframe
            close_prices.plot(label=f'{tickerwrapper.ticker.info["shortName"]}', linewidth=1)
            # If no analysis methods are selected, plot stock data only
            if len(self.model.methods) == 0:
                continue

            # Apply analysis methods (e.g., moving averages)
            for value in self.model.methods.values():
                methodArgs = [int(each) for each in value]  # Extract method arguments (window sizes)

            # Compute moving averages for each window size
            methods = [close_prices.rolling(window=methodArg).mean() for methodArg in methodArgs]

            # Plot each moving average
            for i, ma in enumerate(methods):
                ma.plot(label=f'{tickerwrapper.ticker.info["shortName"]} - Moving Average: {methodArgs[i]}', linestyle='--', linewidth=1)

            # Display the graph with the updated timezone
        self.printGraph(timezone=close_prices.index.tz)


    def printGraph(self, timezone) -> None:
        """Display the graph, showing full timestamps including the timezone if available."""
        plt.title('Stock data')

        ax = plt.gca()  # Get the current axis

        # Set the x-axis formatter to display full timestamp including timezone
        if timezone is not None:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S %Z', tz=timezone))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

        # Automatically adjust the rotation of the x-axis labels for better readability
        plt.gcf().autofmt_xdate()

        # Plot the legend and show the graph
        plt.legend()
        plt.tight_layout()
        plt.show()  # This will display the plot and block until closed
