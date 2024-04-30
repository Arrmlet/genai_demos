import yfinance as yf
from datetime import date
import pandas as pd
import plotly.graph_objects as go

from newsapi import NewsApiClient
from config import settings
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

NEWS_API = settings.news_api# ''
OPENAI_API_KEY = settings.openai_api #
newsapi = NewsApiClient(api_key=NEWS_API)

llm = OpenAI(model="gpt-4-1106-preview",api_key=OPENAI_API_KEY)

class FinanceTools(BaseToolSpec):
    """Finance tools spec."""
    spec_functions = [
        "stock_prices",
        "last_stock_price",
        "search_news",
        "summarize_news_news_api",
        "plot_stock_price"
    ]

    def __init__(self) -> None:
        """Initialize the Yahoo Finance tool spec."""

    def stock_prices(self, ticker: str) -> pd.DataFrame:
        """
        Get the historical prices and volume for a ticker for the last month.
        Args:
            ticker (str): the stock ticker to be given to yfinance
        """
        stock = yf.Ticker(ticker)
        df = stock.history()
        return df

    def last_stock_price(self, ticker: str) -> pd.DataFrame:
        """
        Get the last historical prices and volume for a ticker.
        Args:
            ticker (str): the stock ticker to be given to yfinance
        """
        stock = yf.Ticker(ticker)
        df = stock.history()
        df_last = df.iloc[-1:]
        return df_last

    def search_news(self, ticker: str, num_articles: int = 5, from_datetime="2024-04-10", to_datetime=date.today()):
        """
        Get the most recent news of a stock or an instrument
        Args:
            ticker (str): the stock ticker to be given to NEWSAPI
            num_articles (int): Number of news article to collect
        """
        all_articles = newsapi.get_everything(q=ticker,
                                              from_param=from_datetime,
                                              to=to_datetime,
                                              language='en',
                                              sort_by='relevancy',
                                              page_size=num_articles)
        news_concat = [
            f"{article['title']}, {article['description']}, {article['content'][0:100]}"
            for article in all_articles['articles']
        ]
        return (".\\n").join(news_concat)

    def summarize_news_news_api(self, ticker: str) -> str:
        """
        Summarize the news of a given stock or an instrument
        Args:
            news (str): the news articles to be summarized for a given instruments.
        """
        news = self.search_news(ticker)
        prompt = f"Summarize the following text by extractin the key insights: {news}"
        response = llm.complete(prompt).text
        return response

    def plot_stock_price(self, ticker: str) -> str:
        """
        Plot the closing prices for a given ticker symbol using the historical data.
        Args:
            ticker (str): the stock ticker to be given to yfinance
        """
        df = self.stock_prices(ticker)

        # Create the candlestick trace
        candlestick = go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing=dict(line=dict(color='#00FF00')),
            decreasing=dict(line=dict(color='#FF0000'))
        )

        # Create the volume trace
        volume = go.Bar(
            x=df.index,
            y=df['Volume'],
            visible=False,
            yaxis='y2',
            name='Volume',
            marker=dict(color='#0000FF')
        )

        # Create the layout
        layout = go.Layout(
            title=f'{ticker} Stock Price',
            xaxis=dict(
                title='Date',
                rangeslider=dict(visible=True),
                type='date'
            ),
            yaxis=dict(title='Price'),
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0, y=1, orientation='h'),
            plot_bgcolor='#FFFFFF',
            hovermode='x',
            hoverlabel=dict(bgcolor='#EEEEEE'),
            margin=dict(l=50, r=50, t=50, b=50)
        )

        # Create the figure
        fig = go.Figure(data=[candlestick, volume], layout=layout)

        # Customize the hover tooltip
        fig.update_layout(
            hoverlabel=dict(
                bgcolor='#EEEEEE',
                font=dict(size=12),
                align='left'
            )
        )

        # Add buttons to toggle volume visibility
        fig.update_layout(
            updatemenus=[dict(
                buttons=[
                    dict(
                        label='Volume On',
                        method='update',
                        args=[{'visible': [True, True]}, {'yaxis2': {'title': 'Volume'}}]
                    ),
                    dict(
                        label='Volume Off',
                        method='update',
                        args=[{'visible': [True, False]}, {'yaxis2': {'title': ''}}]
                    )
                ],
                direction='down',
                pad={'r': 10, 't': 10},
                showactive=True,
                x=0.1,
                xanchor='left',
                y=1.1,
                yanchor='top'
            )]
        )

        # Show the plot
        # fig.show()
        fig.write_json("charts/chart.json")

        return 'plotted'
        # print(df)
        #  # Create a new DataFrame with the desired column names and data
        # plot_data = pd.DataFrame({
        #     'Open': df['Open'],
        #     'High': df['High'],
        #     'Low': df['Low'],
        #     'Close': df['Close'],
        #     'Volume': df['Volume']
        # })
        # plot_data.index.name = 'Date'

        # # Customize the plot style
        # mc = mpf.make_marketcolors(up='g', down='r', volume='in')
        # s = mpf.make_mpf_style(marketcolors=mc)

        # # Create the plot
        # mpf.plot(plot_data, type='candle', volume=True, style=s, title=f'{ticker} Stock Price')

        # return 'Plotted'


finance_tool = FinanceTools()
finance_tool_list = finance_tool.to_tool_list()
agent = ReActAgent.from_tools(finance_tool_list, llm=llm, verbose=True)