# Understanding Geometric Mean: Calculation Method and Examples

## What Is the Geometric Mean?

The geometric mean is the average of a set of products. It is calculated using the products of the terms.

The geometric mean can help analysts, investors, and portfolio managers evaluate the performance of an investment [portfolio](https://www.investopedia.com/terms/p/portfolio.asp).

By accounting for the effects of compounding, the geometric mean provides more accurate return measures than the arithmetic mean.

Calculating the geometric mean can be understood by multiplying two simple numbers like 2 and 8 and taking the square root of the product. Calculation involving many numbers increases the difficulty unless you use a calculator or computer program.

The geometric mean is preferable for [investment](https://www.investopedia.com/terms/i/investment.asp) performance evaluation because of its handling of serial correlation in returns. The calculation works best for series with serial correlation, like investment portfolios. Most returns in finance—including market risk premiums, stock returns, and bond yields—are correlated.

### Key Takeaways

- The geometric mean is an average calculated via the product of terms, ideal for assessing investment performance.
- It accounts for year-over-year compounding, offering a precise measure of an investment's true return.
- Unlike the arithmetic mean, the geometric mean handles percentages, making it essential for financial analyses.
- The geometric mean is always slightly less than the arithmetic mean, reflecting its focus on compounded growth.
- Compounding effects make the geometric mean crucial for long-term portfolio performance evaluation.

## Why the Geometric Mean Is Essential in Finance

The geometric mean, sometimes referred to as [compounded annual growth rate (CAGR)](https://www.investopedia.com/terms/c/cagr.asp) or [time-weighted rate of return](https://www.investopedia.com/terms/t/time-weightedror.asp), is the average rate of return of a set of values calculated using the products of the terms. What does that mean? The geometric mean multiplies several values and sets them to the 1/nth power.

For various reasons, the geometric mean is an important tool for calculating [portfolio performance](https://www.investopedia.com/articles/08/performance-measure.asp). One of the most significant of those reasons is that it takes into account the [effects of compounding](https://www.investopedia.com/terms/c/compounding.asp).

For example, the geometric mean calculation can be easily understood with simple numbers, such as 2 and 8. If you multiply 2 and 8, then take the square root (the ½ power since there are only two numbers), the answer is 4. However, when there are many numbers, it is more difficult to calculate unless a calculator or computer program is used.

A key benefit of the geometric mean is that you don't need to know the actual amounts invested. It focuses only on return figures, offering a direct comparison between two investment options over time.

The geometric mean is usually smaller than the [arithmetic mean](https://www.investopedia.com/terms/a/arithmeticmean.asp), a simple average.

## Calculating the Geometric Mean: Formula and Example

#### Formula for the Geometric Mean

μ geometric = [ ( 1 + R 1 ) ( 1 + R 2 ) … ( 1 + R n ) ] 1 / n − 1 where: ∙ R 1 … R n are the returns of an asset (or other observations for averaging) . \begin{aligned} &\mu _{\text{geometric}} = [(1+R _1)(1+R _2)\ldots(1+R _n)]^{1/n} - 1\\ &\textbf{where:}\\ &\bullet R_1\ldots R_n \text{ are the returns of an asset (or other}\\ &\text{observations for averaging)}. \end{aligned} ​μgeometric​=[(1+R1​)(1+R2​)…(1+Rn​)]1/n−1where:∙R1​…Rn​ are the returns of an asset (or otherobservations for averaging).​

#### Calculating Geometric Mean

Imagine that your portfolio returned the following amounts each year for five years:

- Year one: 5%
- Year two: 3%
- Year three: 6%
- Year four: 2%
- Year five: 4%

You would use the formula with those values:

- [ ( 1 + 0.05)(1 + 0.03)(1 + 0.06)(1 + 0.02)(1 + 0.04) ] 1/5 - 1
- [1.05 × 1.03 × 1.06 × 1.02 × 1.04]1/5 - 1
- [1.2161]1/5 - 1
- [1.2161].2 -1 = 0.0399

Multiply the result by 100%, and your portfolio returned a geometric mean of 3.99% over five years, slightly less than the arithmetic mean of (5+3+6+2+4) ÷ 5 = 4.

#### Using Spreadsheets to Compute the Geometric Mean

You can also use the *Geomean* function of a Google Sheet to calculate the geometric mean of the previous returns. A B 1 Period Return 2 Year one 1.05 3 Year two 1.03 4 Year three 1.06 5 Year four 1.02 6 Year five 1.04 In an empty cell, enter the following (make sure you click Format> Number> Plain Text): =GEOMEAN(B2:B6) Important The longer the time horizon, the more critical compounding becomes, and the more appropriate the use of geometric mean. What Is the Geometric Mean of N Terms? The geometric mean of *n*terms is the product of the terms to the *n*th root where *n* represents the number of terms. Can You Calculate the Geometric Mean With Negative Values? You cannot—it is impossible to calculate a geometric mean that includes negative numbers. To use negative numbers in a geometric mean calculation, you have to convert them to a proportion. For example, if you had an investment that returned -3%, you would use 1 - 0.03 = 0.97 as your value. How Do You Find the Geometric Mean Between Two Numbers? To calculate the geometric mean of two numbers, you would multiply the numbers together and take the square root of the result. The Bottom Line In math, the geometric mean is the average of a set of values calculated using the products of the terms. In finance, the geometric mean helps with investment portfolio performance evaluation. The geometric mean assesses the performance of investment portfolios by considering year-over-year compounding, which smooths the mean. The geometric mean differs from the arithmetic mean (the sum of a series of numbers divided by the number of numbers summed) in that it handles percentages. Therefore, it often provides a more accurate measurement for volatile numbers such as investment portfolios. What the geometric mean is not suitable for is calculating averages with negative values. However, solutions exist, such as using proportions. Understanding the geometric mean can guide investors to make better investment decisions and portfolio adjustments.

