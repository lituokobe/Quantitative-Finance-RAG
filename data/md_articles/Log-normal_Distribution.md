# Understanding Lognormal vs. Normal Distributions in Financial Analysis

Lognormal and normal distributions can help you analyze investments accurately. [Lognormal](https://www.investopedia.com/terms/l/log-normal-distribution.asp) distributions are often used to model stock prices, which can’t fall below zero and tend to grow exponentially. [Normal distributions](https://www.investopedia.com/terms/n/normaldistribution.asp) are commonly applied to portfolio returns, which can fluctuate above and below an average. Choosing the correct distribution method can help you make more reliable predictions and informed financial decisions.

### Key Takeaways

- Normal distributions are symmetrical and can model outcomes like portfolio returns that can be positive or negative.
- Lognormal distributions are right-skewed and ideal for modeling stock prices, which can't fall below zero.
- Stock prices follow a lognormal distribution because they grow at a compounded rate and remain positive.
- The Black-Scholes model uses lognormal distribution to price options.
- Choosing between normal and lognormal distribution impacts how investment results and probabilities are analyzed.

## Understanding the Differences Between Normal and Lognormal Distributions

Both normal and lognormal distributions are used in statistical mathematics to describe the probability of an event occurring. Flipping a coin is an easily understood example of probability. If you flip a coin 1000 times, what is the distribution of results? That is, how many times will it land on heads or tails? There is a 50% probability that it will land on either heads or tails. This basic example describes the probability and distribution of results.

There are many types of distributions, one of which is the normal or bell curve distribution.

In a normal distribution, 68% (34%+34%) of the results fall within one standard deviation, and 95% (68%+13.5%+13.5%) fall within two standard deviations. At the center (the 0 point in the image above) the median (the middle value in the set), the mode (the value that occurs most often), and the [mean](https://www.investopedia.com/terms/m/mean.asp) ([arithmetic average](https://www.investopedia.com/ask/answers/06/geometricmean.asp)) are all the same.

The lognormal distribution differs from the normal distribution in several ways. A major difference is in its shape: the normal distribution is symmetrical, whereas the lognormal distribution is not. Because the values in a lognormal distribution are positive, they create a right-skewed curve.

This skewness is important in determining which distribution is appropriate to use in investment decision-making. A further distinction is that the values used to derive a lognormal distribution are normally distributed.

Let's clarify with an example. An investor wants to know an expected future stock price. Since stocks grow at a compounded rate, they need to use a growth factor.

To calculate possible expected prices, they will take the current stock price and multiply it by various [rates of return](https://www.investopedia.com/terms/r/rateofreturn.asp) (which are mathematically derived [exponential factors](https://www.investopedia.com/terms/e/exponential-growth.asp) based on [compounding](https://www.investopedia.com/terms/c/compounding.asp)), which are assumed to be normally distributed. When the investor continuously compounds the returns, they create a lognormal distribution.

This distribution is always positive even if some of the rates of return are negative, which will happen 50% of the time in a normal distribution. The future stock price will always be positive because stock prices cannot fall below $0.

## Choosing the Right Distribution for Investment Analysis

The preceding example helped us arrive at what really matters to investors: when to use each method. Lognormal is extremely useful when analyzing stock prices. As long as the growth factor used is assumed to be normally distributed (as we assume with the rate of return), then the lognormal distribution makes sense. Normal distribution cannot be used to model stock prices because it has a negative side, and stock prices cannot fall below zero.

Another similar use of the lognormal distribution is with the pricing of [options](https://www.investopedia.com/terms/o/option.asp). The [Black-Scholes](https://www.investopedia.com/terms/b/blackscholes.asp) model—used to price options—uses the lognormal distribution as its basis to determine [option prices](https://www.investopedia.com/articles/optioninvestor/09/buying-options.asp).

Conversely, normal distribution works better when calculating [total portfolio returns](https://www.investopedia.com/terms/t/totalreturn.asp). The normal distribution is used because the [weighted](https://www.investopedia.com/terms/w/weighted.asp) average return (the product of the weight of a security in a portfolio and its rate of return) is more accurate in describing the actual [portfolio return](https://www.investopedia.com/terms/p/portfolio-return.asp) (positive or negative), particularly if the weights vary by a large degree. The following is a typical example:

| Portfolio Holdings                | Weights | Returns | Weighted Returns       |
|-----------------------------------|---------|---------|------------------------|
| Stock A                           | 40%     | 12%     | 40% * 12% = 4.8%       |
| Stock B                           | 60%     | 6%      | 60% * 6% = 3.6%        |
| **Total Weighted Average Return** |         |         | **4.8% + 3.6% = 8.4%** |


Although the lognormal return for total portfolio performance may be quicker to calculate over a longer time period, it fails to capture the individual stock weights, which can distort the return tremendously. Also, portfolio returns can be positive or negative, and a lognormal distribution will fail to capture the negative aspects.

## The Bottom Line

Lognormal distributions are best suited for modeling stock prices, which can’t fall below zero, while normal distributions are more appropriate for portfolio returns. Grasping these distinctions can help you make better investment decisions.

