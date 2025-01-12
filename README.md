# AMNII-BT - Automated Trading Bot

## Overview

AMNII-BT is an automated trading bot designed to trade on financial markets. It integrates with **MetaTrader 5 (MT5)** using the Python `MetaTrader5` library for executing trades. The bot employs four trading strategies to make decisions:

- **FVG Strategytit** (Fair Value Gap)
- **Order Blocks Strategy**
- **SMA & EMA Crossover Strategy**
- **Support and Resistance Strategy**

The backend is built with **Django**, and once ready, API endpoints will be provided for frontend integration.

## Features

- **Django Backend**: Handles user authentication, portfolio management, and trade execution.
- **MT5 Integration**: Uses the MetaTrader5 Python package to connect to a MetaTrader terminal for executing buy/sell orders.
- **Four Trading Strategies**:
  - **FVG Strategy**: Identifies fair value gaps in the market and trades based on them.
  - **Order Blocks Strategy**: Recognizes order block levels and trades when price interacts with these blocks.
  - **SMA & EMA Crossover Strategy**: Trades based on the crossover of Simple Moving Average (SMA) and Exponential Moving Average (EMA).
  - **Support and Resistance Strategy**: Trades based on support and resistance levels, identifying key price zones where the market may reverse.

## Technologies Used

- **Python**: Primary programming language.
- **Django**: Backend framework for managing user portfolios, trades, and market data.
- **MetaTrader5 (MT5)**: A popular trading platform used for executing trades via API integration.
- **SQLite** (or another database of your choice): Database used to store user portfolios, market data, and trade history.
- **Celery/Redis** (Optional for task management): Future implementation may include Celery with Redis for background task processing (e.g., executing trades in parallel or handling data fetching tasks).

## How the Bot Works

The bot operates through a Django backend that communicates with MetaTrader 5 for trade execution. Below are the details of the core functionalities:

### 1. Django Backend
Users can create a portfolio where their balance and trade history are tracked. Trades are executed based on the signals generated from the selected strategies.

### 2. Strategies
The bot uses four trading strategies to generate signals for trade execution:
- **FVG Strategy**: Identifies significant gaps in the price (Fair Value Gaps). The bot detects these gaps and places trades based on the theory that prices will fill these gaps.
- **Order Blocks Strategy**: The bot detects areas where significant market orders have occurred, known as order blocks. The bot places trades when the price reaches or reacts to these levels.
- **SMA & EMA Crossover Strategy**: This strategy uses the crossing of two moving averages (SMA and EMA) as a trading signal. When the shorter-term moving average crosses above the longer-term moving average, a "Buy" signal is generated, and vice versa for a "Sell" signal.
- **Support and Resistance Strategy**: The bot identifies major support and resistance levels. When price approaches these levels, it analyzes the probability of a breakout or reversal and places trades accordingly.

### 3. Trade Execution via MetaTrader5 (MT5)
The bot connects to the MetaTrader5 terminal using the `MetaTrader5` Python module, which allows it to send trade orders to the market. The bot executes trades (buy/sell) with calculated **Take Profit (TP)** and **Stop Loss (SL)** based on the chosen strategy.

### 4. Django API Endpoints
API endpoints will be provided to serve the frontend with data such as the user's portfolio, trade history, and real-time market data. The endpoints will allow the frontend to access live trades, strategy details, and market analytics.

## Setup Instructions

### Prerequisites
- **Python** version 3.8 or higher.
- **MetaTrader 5 (MT5)** installed on your system.
- **Django** installed in your Python environment.

### Install Dependencies
Install the required Python packages by running:

