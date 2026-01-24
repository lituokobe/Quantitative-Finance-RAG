# Understanding Value at Risk (VaR): Explanation and Calculation Methods

## What Is Value at Risk (VaR)?

Value at Risk (VaR) estimates the maximum expected loss of an investment over a set period at a chosen confidence level, making it a common tool for banks and financial firms. It can be calculated using historical data, the variance-covariance method, or Monte Carlo simulation. This article will apply these approaches to the Nasdaq 100 Index to illustrate how VaR works in practice.

### Key Takeaways

- Value at Risk (VaR) is a statistical technique used to predict the potential maximum loss of an investment over a specific time period with a certain confidence level.
- VaR is determined by three variables: time period, confidence level, and size of potential loss.
- There are three main methods to calculate VaR: the historical method, the variance-covariance method, and Monte Carlo simulation.
- The historical method uses past returns to estimate future risk, while the variance-covariance method assumes normally distributed returns.
- Monte Carlo simulations use computational models to simulate potential outcomes, providing a range of possible scenarios and losses.

## Key Components of Value at Risk (VaR)

The traditional measure of risk is volatility, and an investor's main concern is the odds of losing money. The VaR statistic has three components: a period, a confidence level, and a loss amount, or loss percentage, and can address these concerns:

- What can I expect to lose in dollars with a 95% or 99% level of confidence next month?
- What is the maximum percentage I can expect to lose with 95% or 99% confidence over the next year?

The questions include a high level of confidence, a period, and an estimate of investment loss.

## Techniques for Calculating Value at Risk (VaR)

Let's evaluate the risk of a single index that trades like a stock, the Nasdaq 100 Index, which is traded through the Invesco QQQ Trust. The QQQ is an index of the largest non-financial stocks that trade on the Nasdaq exchange.

There are three methods of calculating Value at Risk (VaR), including the historical method, the variance-covariance method, and the Monte Carlo simulation.

### Historical Approach to Calculating VaR

The historical method simply re-organizes actual historical returns, putting them in order from worst to best. It then assumes that history will repeat itself, from a risk perspective. Let's look at the Nasdaq 100 ETF, which trades under the symbol QQQ.

### Value at Risk

$$\text{Value at Risk} = v_m * (v_i / v_{i - 1})$$
where:
- $v_m = \text{Market value (often today’s portfolio value)}$
- $v_i = \text{Value at time i (e.g., today’s price or portfolio value)}$
- $v_{i - 1} = \text{ Value at time i-1 (yesterday’s price or value)}$

M = the number of days from which historical data is taken

vi = the number of variables on the day i.

In calculating each daily return, we produce a rich data set of more than 1,400 points. Let's put them in a histogram that compares the frequency of return "buckets."

At the highest bar, there were more than 250 days when the daily return was between 0% and 1%. At the far right, a tiny bar at 13% represents the one single day within five-plus years when the daily return for the QQQ was 12.4%.

### Variance-Covariance Method for Assessing VaR

This method assumes that stock returns are normally distributed and requires an estimate of only two factors, an expected return, and a standard deviation, allowing for a normal distribution curve. The normal curve is plotted against the same actual return data in the graph above.

The variance-covariance is similar to the historical method except it uses a familiar curve instead of actual data. The advantage of the normal curve is that it shows where the worst 5% and 1% lie on the curve. They are a function of desired confidence and the standard deviation.

| Confidence        | # of Standard Deviations (σ) |
|-------------------|------------------------------|
| 95% (high)        | -1.65 × σ                    |
| 99% (really high) | -2.33 × σ                    |

The curve above is based on the actual daily standard deviation of the QQQ, which is 2.64%. The average daily return happened to be fairly close to zero, so it's safe to assume an average return of zero for illustrative purposes. Here are the results of using the actual standard deviation in the formulas above:

| Confidence       | # of σ         | Calculation            | Equals   |
|------------------|----------------|------------------------|----------|
| 95% (high)       | -1.65 × σ      | -1.65 × (2.64%)        | -4.36%   |
| 99% (really high)| -2.33 × σ      | -2.33 × (2.64%)        | -6.15%   |

### Monte Carlo Simulation in Valuing VaR

A Monte Carlo simulation refers to any method that randomly generates trials, but by itself, does not tell us anything about the underlying methodology.

For most users, a Monte Carlo simulation amounts to a "black box" generator of random, probabilistic outcomes. This technique uses computational models to simulate projected returns over hundreds or thousands of possible iterations.

If 100 hypothetical trials of monthly returns for the QQQ were conducted, two of the worst outcomes may be between -15% and -20%, and three between -20% and 25%. That means the worst five outcomes were less than -15%.

The Monte Carlo simulation, therefore, leads to the following VaR-type conclusion: with 95% confidence, we do not expect to lose more than 15% during any given month.

## Explain Like I'm 5

Value at Risk (VaR)can help investors answer the question: "What's the potential maximum loss I could expect from this investment within x days/weeks/months?" In other words, VaR is a statistical method that can be used to estimate the worst-case loss of an investment over a specific period of time, considering a certain probability of that loss occurring (which is called "confidence level"). For example, if an investment's one-day VaR is \$5,000 at a 95% confidence level, it means there's a 5% (100% - 95%) chance the investment could lose more than \$5,000 in a single day.

## What Is the Disadvantage of Using Value at Risk?

While VaR is useful for predicting the risks facing an investment, it can be misleading. One critique is that different methods give different results: you might get a gloomy forecast with the historical method, while Monte Carlo Simulations are relatively optimistic. It can also be difficult to calculate the VaR for large portfolios: you can't simply calculate the VaR for each asset, since many of those assets will be correlated. Finally, any VaR calculation is only as good as the data and assumptions that go into it.

## What Are the Advantages of Using Value at Risk?

VaR is a single number that indicates the extent of risk in a given portfolio and is measured in either price or as a percentage, making understanding VaR easy. It can be applied to assets

such as bonds, shares, and currencies, and is used by banks and financial institutions to assess the profitability and risk of different investments, and allocate risk based on VaR.

## What Does a High VaR Mean?

A high value for the confidence interval percentage means greater confidence in the likelihood of the projected outcome. Alternatively, a high value for the projected outcome is not ideal and statistically anticipates a higher dollar loss to occur.

## The Bottom Line

Value at Risk (VAR) calculates the maximum expected loss on an investment over a given period at a chosen confidence level, and it can be calculated using the historical method, the variance-covariance approach, or Monte Carlo simulation. Understanding VaR helps investors and risk managers understand potential downside and compare how different market conditions might affect a portfolio.

