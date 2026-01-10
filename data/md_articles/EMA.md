# Exponential Moving Average (EMA): Definition, Formula, and Usage

## What Is an Exponential Moving Average (EMA)?

The Exponential Moving Average (EMA) is a refined [moving average (MA)](https://www.investopedia.com/terms/m/movingaverage.asp) that emphasizes recent data points more heavily, offering a crucial edge in tracking price dynamics. Unlike the [Simple Moving Average (SMA)](https://www.investopedia.com/terms/s/sma.asp), which distributes weight equally across data points, the EMA’s technique gives it a distinct advantage in responding swiftly to price fluctuations. This makes it an essential tool for traders seeking to capitalize on the most current market trends and movements.

### Key Takeaways

- An Exponential Moving Average (EMA) is a moving average that places greater emphasis on recent data points, making it more sensitive to recent price changes than a Simple Moving Average (SMA).
- The formula for calculating an EMA includes a multiplier that gives more weight to recent observations, which allows traders to better capture current trends.
- EMAs are popular among traders for identifying short-term trends using periods such as the 12- and 26-day EMAs or for long-term trends with 50- and 200-day EMAs.
- While EMAs respond more quickly to recent data, they can produce false signals; hence, they are most effective when used alongside other technical indicators.
- The effectiveness of EMAs is debated, as they rely solely on historical data, and some argue that markets reflect all available information, which historical data may not always accurately predict.

## Formula for Exponential Moving Average (EMA)

$$\text{EMA}_{\text{Today}} = (\text{Value}_{\text{Today}} * \frac{\text{Smoothing}}{1 + \text{Days}}) + \text{EMA}_{\text{Yesterday}} * (1 - \frac{\text{Smoothing}}{1 + \text{Days}})$$
where:
- $\text{EMA} = \text{Exponential Moving Average}$

While there are many possible choices for the smoothing factor, the most common choice is:
- Smoothing = 2

That gives the most recent observation more weight. If the smoothing factor is increased, more recent observations have more influence on the EMA.

## How to Calculate the Exponential Moving Average

Calculating the EMA needs one more observation than the SMA. If you choose 20 days for your EMA, wait until the 20th day to get the SMA. Then, use that SMA as the first EMA on the 21st day.

Calculating the SMA is straightforward. It involves adding up the stock's closing prices over a period and then dividing by the number of observations. For example, a 20-day SMA is just the sum of the closing prices for the past 20 trading days, divided by 20.

Next, you must calculate the multiplier for smoothing (weighting) the EMA, which typically follows the formula: $2 / (\text{number of observations} + 1)$. For a 20-day moving average, the multiplier would be [2/(20+1)]= 0.0952.

Use this formula to calculate the current EMA:

- $$\text{EMA} = \text{Closing price} * \text{multiplier} + \text{EMA (previous day)} * (1 - \text{multiplier})$$

EMAs give more weight to recent prices, while SMAs give equal weight to all values. Shorter-period EMAs give more weight to recent prices than longer-period EMAs. For example, an 18.18% multiplier is applied to the most recent price data for a 10-period EMA, while the weight is only 9.52% for a 20-period EMA.

Variations of the EMA can be calculated using the open, high, low, or median price instead of the closing price.

## Insights From the Exponential Moving Average

The 12- and 26-day EMAs are often the most quoted short-term averages. They are used to create indicators like the [moving average convergence divergence (MACD)](https://www.investopedia.com/terms/m/macd.asp) and the [percentage price oscillator (PPO)](https://www.investopedia.com/terms/p/ppo.asp). In general, the 50- and 200-day EMAs are used as indicators for long-term trends. When a stock price crosses its 200-day moving average, it is a technical signal that a [reversal](https://www.investopedia.com/terms/r/reversal.asp) has occurred.

Traders who employ [technical analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp) find moving averages very useful and insightful when applied correctly. However, they also realize that these signals can create havoc when used improperly or misinterpreted. All the moving averages commonly used in technical analysis are [lagging indicators](https://www.investopedia.com/terms/l/laggingindicator.asp).

Consequently, the conclusions drawn from applying a moving average to a particular market chart should be to confirm a market move or indicate its strength. The optimal time to enter the market often passes before a moving average shows that the trend has changed.

An EMA does serve to alleviate the negative impact of lags to some extent. Because the EMA calculation places more weight on the latest data, it “hugs” the price action a bit more tightly and reacts more quickly. This is desirable when an EMA is used to derive a trading entry signal.

Like all moving average indicators, EMAs are much better suited for [trending markets](https://www.investopedia.com/terms/t/trending-market.asp). When the market is in a strong and sustained uptrend, the [EMA indicator line](https://www.investopedia.com/ask/answers/122314/what-are-best-technical-indicators-complement-exponential-moving-average-ema.asp) will also show an uptrend and vice-versa for a downtrend. A vigilant trader will pay attention to both the direction of the EMA line and the relation of the [rate of change](https://www.investopedia.com/terms/r/rateofchange.asp) from one bar to the next. For example, suppose the price action of a strong uptrend begins to flatten and reverse. From an [opportunity cost](https://www.investopedia.com/terms/o/opportunitycost.asp) point of view, it might be time to switch to a more bullish investment.

## Practical Applications of the Exponential Moving Average

EMAs are commonly used in conjunction with other indicators to confirm significant market moves and to gauge their validity. For traders who trade [intraday](https://www.investopedia.com/terms/i/intraday.asp) and fast-moving markets, the EMA is more applicable. Quite often, traders use EMAs to determine a trading bias. If an EMA on a [daily chart](https://www.investopedia.com/terms/d/dailychart.asp) shows a strong upward trend, an intraday trader’s strategy may be to trade only on the long side.

## Comparing EMA and SMA: Key Differences Explained

The major [difference between an EMA and an SMA](https://www.investopedia.com/ask/answers/difference-between-simple-exponential-moving-average/) is the sensitivity each one shows to changes in the data used in its calculation.

More specifically, the EMA gives higher weights to recent prices, while the SMA assigns equal weights to all values. The two averages are similar because they are interpreted in the same manner and are both commonly used by technical traders to smooth out price fluctuations.

Because EMAs give more weight to recent data, they respond faster to [price changes](https://www.investopedia.com/terms/p/price-change.asp) than SMAs. This timeliness is why many traders prefer them.

## Recognizing the Limitations of the Exponential Moving Average

It is unclear whether or not more emphasis should be placed on the most recent days in the time period. Many traders believe that new data better reflects the current trend of the security. At the same time, others feel that overweighting recent dates creates a bias that leads to more false alarms.

Similarly, the EMA relies wholly on historical data. Many economists believe that [markets are efficient](https://www.investopedia.com/articles/basics/04/022004.asp), which means that current market prices already reflect all available information. If markets are indeed efficient, using historical data should tell us nothing about the future direction of asset prices.

## What Is a Good Exponential Moving Average?

The longer-day EMAs (i.e. 50 and 200-day) tend to be used more by long-term investors, while short-term investors tend to use 8- and 20-day EMAs.

## Is Exponential Moving Average Better Than Simple Moving Average?

The EMA focused more on recent price moves, which means it tends to respond more quickly to price changes than the SMA.

## How Do You Read Exponential Moving Averages?

Investors tend to interpret a rising EMA as a support to price action and a falling EMA as a resistance. With that interpretation, investors look to buy when the price is near the rising EMA and sell when the price is near the falling EMA.

