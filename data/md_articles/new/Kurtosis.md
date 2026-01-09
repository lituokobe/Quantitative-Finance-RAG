# Kurtosis: Definition, Types, and Importance

## What Is Kurtosis?

Kurtosis is a statistical measure used to describe a characteristic of a dataset. It generally takes the form of a bell when normally distributed data is plotted on a graph. This is called the bell curve. The plotted data that are farthest from the [mean](https://www.investopedia.com/terms/m/mean.asp) of the data usually form the tails on each side of the curve. Kurtosis indicates how much data resides in the tails.

### Key Takeaways

- Kurtosis describes the “fatness” of the tails found in probability distributions.
- There are three kurtosis categories: mesokurtic (normal), platykurtic (less than normal), and leptokurtic (more than normal).
- Kurtosis risk is a measurement of how often an investment’s price moves dramatically.
- A curve’s kurtosis characteristic tells you how much kurtosis risk there is for the investment you’re evaluating.

## How Kurtosis Works

Kurtosis is a measure of the combined weight of a distribution’s tails relative to the center of the distribution curve referred to as the mean. It shows a peak when a set of approximately normal data is graphed via a histogram with most of the data residing within three standard plus or minus deviations of the mean. The tails extend farther than the three standard deviations of the normal bell-curved distribution when high kurtosis is present, however.

Kurtosis is sometimes confused with a measure of the peakedness of a distribution but kurtosis is a measure that describes the shape of a distribution’s tails in relation to its overall shape. A distribution can be sharply peaked with low kurtosis and a distribution can have a lower peak with high kurtosis so kurtosis measures “tailedness” not “peakedness.”

Distributions with a large kurtosis have more tail data than normally distributed data, which appears to bring the tails in toward the mean. Distributions with low kurtosis have fewer tail data, which appears to push the tails of the bell curve away from the mean.

High kurtosis of the return distribution curve implies that there have been many positive or negative price fluctuations in the past away from the average returns for the investment. An investor might experience extreme price fluctuations with an investment with high kurtosis. This phenomenon is known as kurtosis risk.

## Formula and Calculation of Kurtosis

There are several different methods for calculating kurtosis.

### Calculating With Spreadsheets

The simplest way to calculate is to use the Excel or Google Sheets formula. Assume you have the following sample data: 4, 5, 6, 3, 4, 5, 6, 7, 5, and 8 residing in cells A1 through A10 on your spreadsheet. The spreadsheets use this formula for calculating kurtosis:

n ( n + 1 ) ( n − 1 ) ( n − 2 ) ( n − 3 ) × ( ∑ x i − x ˉ s )4 − 3 ( n − 1 )2 ( n − 2 ) ( n − 3 ) \begin{aligned}& \frac { n ( n + 1 ) }{ (n - 1)(n - 2)(n - 3) } \times \Big ( \sum \frac { x_i - \bar{x} }{ s } \Big ) ^ 4 - \frac { 3 (n - 1) ^ 2 }{ (n - 2)(n - 3)} \\\end{aligned} ​(n−1)(n−2)(n−3)n(n+1)​×(∑sxi​−xˉ​)4−(n−2)(n−3)3(n−1)2​​

We’ll use the following formula in Google Sheets which calculates it for us, assuming the data resides in cells A1 through A10:

= KURT(A1:A10) \begin{aligned}&= \text{KURT(A1:A10)} \\\end{aligned} ​=KURT(A1:A10)​

The result is a kurtosis of -0.1518, indicating that the curve has lighter tails and is platykurtic.

### Calculating by Hand

Calculating kurtosis by hand is a lengthy endeavor and it takes several steps to get to the results. We’ll use new data points and limit their number to simplify the calculation. These data points are 27, 13, 17, 57, 113, and 25.

### Important

It’s important to note that a sample size should be much larger than this. We're using six numbers to reduce the calculation steps. A good rule of thumb is to use 30% of your data for populations under 1,000. You can use 10% for larger populations.

You must first calculate the mean. Add up the numbers and divide by six to get 42. Next use the following formulas to calculate two sums: s2 (the square of the deviation from the mean) and s4 (the square of the deviation from the mean squared). Note that these numbers do not represent standard deviation. They represent the variance of each data point.

s2 = ∑ ( y i − y ˉ )2 s4 = ∑ ( y i − y ˉ )4 where: y i = ith variable of the sample y ˉ = Mean of the sample \begin{aligned}&\text{s2} = \sum ( y_i - \bar{y} ) ^ 2 \\&\text{s4} = \sum ( y_i - \bar{y} ) ^ 4 \\&\textbf{where:} \\&y_i = \text{ith variable of the sample} \\&\bar{y} = \text{Mean of the sample} \\\end{aligned} ​s2=∑(yi​−yˉ​)2s4=∑(yi​−yˉ​)4where:yi​=ith variable of the sampleyˉ​=Mean of the sample​

Use each variable, subtract the mean, and then square the result to get s2. Add all the results together:

( 27 − 42 )2 = ( − 15 )2 = 225 ( 13 − 42 )2 = ( − 29 )2 = 841 ( 17 − 42 )2 = ( − 25 )2 = 625 ( 57 − 42 )2 = ( 15 )2 = 225 ( 113 − 42 )2 = ( 71 )2 = 5 , 041 ( 25 − 42 )2 = ( − 17 )2 = 289 225 + 841 + 625 + 225 + 5 , 041 + 289 = 7 , 246 \begin{aligned}&(27 - 42) ^ 2 = (-15) ^ 2 = 225 \\&(13 - 42) ^ 2 = (-29) ^ 2 = 841 \\&(17 - 42) ^ 2 = (-25) ^ 2 = 625 \\&(57 - 42) ^ 2 = (15) ^ 2 = 225 \\&(113 - 42) ^ 2 = (71) ^ 2 = 5,041 \\&(25 - 42) ^ 2 = (-17) ^ 2 = 289 \\&225 + 841 + 625 + 225 + 5,041 + 289 = 7,246 \\\end{aligned} ​(27−42)2=(−15)2=225(13−42)2=(−29)2=841(17−42)2=(−25)2=625(57−42)2=(15)2=225(113−42)2=(71)2=5,041(25−42)2=(−17)2=289225+841+625+225+5,041+289=7,246​

Use each variable, subtract the mean, and raise the result to the fourth power to get s4. Add all the results together:

( 27 − 42 )4 = ( − 15 )4 = 50 , 625 ( 13 − 42 )4 = ( − 29 )4 = 707 , 281 ( 17 − 42 )4 = ( − 25 )4 = 390 , 625 ( 57 − 42 )4 = ( 15 )4 = 50 , 625 ( 113 − 42 )4 = ( 71 )4 = 25 , 411 , 681 ( 25 − 42 )4 = ( − 17 )4 = 83 , 521 50 , 625 + 707 , 281 + 390 , 625 + 50 , 625 + 25 , 411 , 681 + 83 , 521 = 26 , 694 , 358 \begin{aligned}&(27 - 42) ^ 4 = (-15) ^ 4 = 50,625 \\&(13 - 42) ^ 4 = (-29) ^ 4 = 707,281 \\&(17 - 42) ^ 4 = (-25) ^ 4 = 390,625 \\&(57 - 42) ^ 4 = (15) ^ 4 = 50,625 \\&(113 - 42) ^ 4 = (71) ^ 4 = 25,411,681 \\&(25 - 42) ^ 4 = (-17) ^ 4 = 83,521 \\&50,625 + 707,281 + 390,625 + 50,625 + 25,411,681 \\&+ 83,521 = 26,694,358 \\\end{aligned} ​(27−42)4=(−15)4=50,625(13−42)4=(−29)4=707,281(17−42)4=(−25)4=390,625(57−42)4=(15)4=50,625(113−42)4=(71)4=25,411,681(25−42)4=(−17)4=83,52150,625+707,281+390,625+50,625+25,411,681+83,521=26,694,358​

Our sums are therefore:

s2 = 7 , 246 s4 = 26 , 694 , 358 \begin{aligned}&\text{s2} = 7,246 \\&\text{s4} = 26,694,358 \\\end{aligned} ​s2=7,246s4=26,694,358​

Now calculate m2 and m4, the second and fourth moments of the kurtosis formula:

m2 = s2 n = 7 , 246 6 = 1 , 207.67 \begin{aligned}\text{m2} &= \frac { \text{s2} }{ n } \\&= \frac { 7,246 }{ 6} \\& = 1,207.67 \\\end{aligned} m2​=ns2​=67,246​=1,207.67​

m4 = s4 n = 26 , 694 , 358 6 = 4 , 449 , 059.67 \begin{aligned}\text{m4} &= \frac { \text{s4} }{ n } \\&= \frac { 26,694,358 }{ 6} \\& = 4,449,059.67 \\\end{aligned} m4​=ns4​=626,694,358​=4,449,059.67​

We can now calculate kurtosis using a formula found in many statistics textbooks that assumes a perfectly normal distribution with a kurtosis of zero:

k = m4 m22 − 3 where: k = Kurtosis m4 = Fourth moment m2 = Second moment \begin{aligned}&k = \frac { \text{m4} }{ \text{m2} ^ 2 } - 3 \\&\textbf{where:} \\&k = \text{Kurtosis} \\&\text{m4} = \text{Fourth moment} \\&\text{m2} = \text{Second moment} \\\end{aligned} ​k=m22m4​−3where:k=Kurtosism4=Fourth momentm2=Second moment​

The kurtosis for the sample variables is therefore:

4 , 449 , 059.67 1 , 458 , 466.83 − 3 = . 05 \begin{aligned}&\frac { 4,449,059.67 }{ 1,458,466.83 } - 3 = .05 \\\end{aligned} ​1,458,466.834,449,059.67​−3=.05​

## Types of Kurtosis

There are three categories of kurtosis that a set of data can display: mesokurtic, leptokurtic, and platykurtic. All measures of kurtosis are compared against a normal distribution curve.

### Mesokurtic (kurtosis = 3.0)

The first category of kurtosis is mesokurtic distribution. This has a kurtosis similar to that of the normal distribution. The extreme value characteristic of the distribution is similar to that of a normal distribution. A stock with a mesokurtic distribution therefore generally depicts a moderate level of risk.

### Leptokurtic (kurtosis > 3.0)

The second category is [leptokurtic](https://www.investopedia.com/terms/l/leptokurtic.asp) distribution. Any distribution that's leptokurtic displays greater kurtosis than a mesokurtic distribution. This distribution appears as a curve with long tails or outliers. The “skinniness” of a leptokurtic distribution is a consequence of the outliers that stretch the horizontal axis of the histogram graph, making the bulk of the data appear in a narrow (“skinny”) vertical range.

A stock with a leptokurtic distribution generally depicts a high level of risk but the possibility of higher returns because the stock has typically demonstrated large price movements.

### Fast Fact

A leptokurtic distribution may be “skinny” in the center but it also features “fat tails.”

### Platykurtic (kurtosis < 3.0)

The final type of distribution is [platykurtic](https://www.investopedia.com/terms/p/platykurtic.asp) distribution. These types of distributions have short tails and fewer outliers. Platykurtic distributions have demonstrated more stability than other curves because extreme price movements have rarely occurred in the past. This translates into a less-than-moderate level of risk.

## Kurtosis vs. Skewness

Kurtosis and [skewness](https://www.investopedia.com/terms/s/skewness.asp) are both statistical measures used to describe the shape of a probability distribution but they focus on different aspects. Kurtosis measures the tailedness of a distribution. Skewness measures the asymmetry of a distribution.

Skewness indicates the direction and degree to which the data deviates from a symmetrical bell curve. A distribution with zero skewness is perfectly symmetrical. The left and right sides of the distribution are mirror images. Positive skewness means that the right tail is longer or fatter than the left, suggesting that the data tends to have higher values. Negative skewness indicates that the left tail is longer or fatter, implying a tendency toward lower values.

Skewness focuses on the balance of data around the mean but kurtosis focuses on the distribution's peak and the weight of its tails. A dataset can have high kurtosis with many outliers but still be symmetric and therefore have zero skewness. A dataset can be skewed with either positive or negative skewness but has low kurtosis, however, indicating fewer extreme values.

## Using Kurtosis

Kurtosis is used in financial analysis to measure an investment’s risk of price volatility. It measures the amount of [volatility](https://www.investopedia.com/terms/v/volatility.asp) that an investment’s price has experienced regularly. High kurtosis of the return distribution implies that an investment will yield occasional extreme returns. This can swing both ways, however. High kurtosis indicates either large positive returns or extreme negative returns.

Imagine that a stock had an average price of $25.85 per share. The bell curve would have heavy tails and high kurtosis if the stock’s price swung widely and often enough. There's a lot of variation in the stock price. An investor should anticipate wide price swings often.

A [portfolio](https://www.investopedia.com/terms/p/portfolio.asp) with a low kurtosis value indicates a more stable and predictable return profile which may indicate lower risk. Investors may intentionally seek investments with lower kurtosis values when they're building safer, less volatile portfolios.

Kurtosis can also be used to strategically implement an investment allocation approach. A [portfolio manager](https://www.investopedia.com/terms/p/portfoliomanager.asp) who specializes in value investing might prefer to invest in assets with a negative kurtosis value because this indicates a flatter distribution with more frequent small returns. Conversely, a portfolio manager who specializes in momentum investing may prefer to invest in assets with a positive kurtosis value with peaked distributions of less frequent but larger returns.

## Other Commonly Used Measurements

Kurtosis risk differs from more commonly used measurements. [Alpha](https://www.investopedia.com/terms/a/alpha.asp) measures excess return relative to a benchmark index. Kurtosis measures the nature of the peak or flatness of the distribution while alpha measures the skewness or asymmetry of the distribution.

[Beta](https://www.investopedia.com/terms/b/beta.asp) measures the volatility of a stock compared to the broader market. Each security or investment has a single beta that indicates whether that security is more or less volatile compared to a market benchmark. Beta measures the degree of asymmetry of the distribution while kurtosis measures the peak or flatness of the distribution.

[R-squared](https://www.investopedia.com/terms/r/r-squared.asp) measures the percentage of movement within a portfolio or fund that can be explained by a benchmark. R-squared is used in regression analysis to assess the goodness of fit of a regression model but kurtosis is used in descriptive statistics to describe the shape of a distribution.

The [Sharpe ratio](https://www.investopedia.com/terms/s/sharperatio.asp) compares return to risk. It's used by investors to better understand whether the level of returns they're receiving is commensurate with the level of risk incurred. Kurtosis analyzes the distribution of a dataset. The Sharpe ratio is more commonly used to evaluate investment performance.

## Why Is Kurtosis Important?

Kurtosis explains how often observations in some datasets fall in the tails versus the center of a probability distribution. Excess kurtosis in finance and investing is interpreted as a type of risk known as [tail risk](https://www.investopedia.com/terms/t/tailrisk.asp), the chance of a loss occurring due to a rare event as predicted by a probability distribution. The tails are said to be “fat” if such events are more common than predicted by a distribution.

## How Is Kurtosis Used in Finance?

Kurtosis is used to assess the risk of extreme returns in investment portfolios by analyzing the tailedness of return distributions. A higher kurtosis indicates a greater probability of significant deviations from the mean. An investment with higher kurtosis is more likely to deviate from its average return.

## Is a High Kurtosis Good or Bad?

A higher kurtosis isn't inherently good or bad. It depends on the context and the investor's risk tolerance. High kurtosis indicates more frequent extreme values or outliers which can imply higher risk and potential for large gains or losses. This is good for some investors. For others, it's bad.

## What Is Excess Kurtosis?

Excess kurtosis compares the kurtosis coefficient with that of a normal distribution. Most normal distributions are assumed to have a kurtosis of three so excess kurtosis would be more or less than three. Some models assume that a normal distribution has a kurtosis of zero, however, so excess kurtosis would be more or less than zero.

## The Bottom Line

Kurtosis describes how much of a probability distribution falls in the tails instead of its center. The kurtosis is equal to three or zero in some models in a normal distribution. Positive or negative excess kurtosis will then change the shape of the distribution accordingly.

Kurtosis is important for investors in understanding tail risk or how frequently “infrequent” events occur given one’s assumption about the distribution of price returns.

