# Regression: Definition, Analysis, Calculation, and Example

## What Is Regression?

Regression is a statistical method that analyzes the relationship between a dependent variable and one or more independent variables. It helps predict or understand how changes in the independent variable(s) are associated with changes in the dependent variable.

Linear regression is the most common form of this technique. It establishes the [linear relationship](https://www.investopedia.com/terms/l/linearrelationship.asp) between two variables and is also referred to as simple regression or ordinary least squares (OLS) regression.

Linear regression is graphically depicted using a straight [line of best fit](https://www.investopedia.com/terms/l/line-of-best-fit.asp), with the slope defining how the change in one variable impacts a change in the other. The y-intercept of a linear regression relationship represents the value of the dependent variable when the value of the independent variable is zero. [Nonlinear regression](https://www.investopedia.com/terms/n/nonlinear-regression.asp) models also exist but are far more complex.

### Key Takeaways

- Regression is a statistical technique that relates a dependent variable to one or more independent variables.
- A regression model shows whether changes observed in the dependent variable are associated with changes in one or more of the independent variables.
- It does this by determining a best-fit line to see how the data is dispersed around this line.
- Regression helps economists and financial analysts with challenges ranging from asset valuation to making predictions.
- Several assumptions about the data and the model itself must hold for regression results to be properly interpreted.

Regression is used in economics to help investment managers value assets and understand the relationships between factors such as [commodity](https://www.investopedia.com/terms/c/commodity.asp) prices and the [stocks](https://www.investopedia.com/terms/s/stock.asp) of businesses dealing in those commodities. It’s a powerful tool for uncovering the associations between variables observed in data, but it can’t easily indicate causation.

Regression as a statistical technique shouldn’t be confused with the concept of regression to the mean, also known as [mean reversion](https://www.investopedia.com/terms/m/meanreversion.asp).

## How Regression Works

Regression captures the correlation between variables observed in a dataset and quantifies whether those correlations are [statistically significant](https://www.investopedia.com/terms/s/statistical-significance.asp). The two basic types of regression are simple linear regression and [multiple linear regression](https://www.investopedia.com/terms/m/mlr.asp), but there are nonlinear regression methods for more complicated data and analysis.

Simple linear regression uses one independent variable to explain or predict the outcome of the dependent variable Y. Multiple linear regression uses two or more independent variables to predict the outcome. Analysts can use [stepwise regression](https://www.investopedia.com/terms/s/stepwise-regression.asp) to examine each independent variable contained in the linear regression model.

Regression can help finance and investment professionals. A company might use it to predict sales based on weather, previous sales, gross domestic product (GDP) growth, or other types of conditions. The [capital asset pricing model (CAPM)](https://www.investopedia.com/terms/c/capm.asp) is a regression model that’s often used in finance for pricing assets and discovering the costs of capital.

## Regression and Econometrics

Econometrics is a set of statistical techniques that are used to analyze data in finance and economics. It effectively studies the income effect using observable data. An economist might hypothesize that a consumer’s spending will increase as they increase their [income](https://www.investopedia.com/terms/i/income.asp).

A regression analysis can then be conducted to understand the strength of the relationship between income and consumption if the data show that such an association is present. It can indicate whether that relationship is statistically significant.

You can have several independent variables in an analysis, such as changes to GDP and inflation in addition to unemployment in explaining stock market prices. It’s referred to as multiple linear regression when more than one independent variable is used. This is the most commonly used tool in econometrics.

### Important

Econometrics is sometimes criticized for relying too heavily on the interpretation of regression output without linking it to economic theory or looking for causal mechanisms. It’s crucial that the findings revealed in the data can be adequately explained by a theory.

## Calculating Regression

Linear regression models often use a least-squares approach to determine the line of best fit. The least-squares technique is determined by minimizing the [sum of squares](https://www.investopedia.com/terms/s/sum-of-squares.asp) created by a mathematical function. A square is then determined by squaring the distance between a data point and the regression line or mean value of the dataset.

A regression model is constructed when this process has been completed. It’s usually accomplished with software. The general form of each type of regression model is:

**Simple linear regression:**

$$Y = a + b*X + u$$

**Multiple linear regression:**

$$Y = a + b_1 * X_1 + b_2 * X_2 + b_3 * X_3 + ... + b_t * X_t + u$$
where: 
- $Y = \text{The dependent variable you are trying to predict or explain}$ 
- $X = \text{The explanatory (independent) variable(s) you are using to predict or associate with Y}$ 
- $a = \text{The y-intercept}$ 
- $b = \text{(beta coefficient) is the slope of the explanatory variable(s)}$ 
- $u = \text{The regression residual or error term}$

## Example of Regression Analysis in Finance

Regression is often used to determine how specific factors such as the price of a commodity, interest rates, particular industries, or sectors influence the price movement of an asset. The CAPM is based on regression and is used to project the expected returns for stocks and generate costs of capital. A stock’s returns are regressed against the returns of a broader index such as the S&P 500 to generate a [beta](https://www.investopedia.com/terms/b/beta.asp) for the particular stock.

Beta is the stock’s risk in relation to the market or index, and it’s reflected as the slope in the CAPM. The return for the stock in question would be the dependent variable Y. The independent variable X would be the market risk premium.

Additional variables such as the market capitalization of a stock, valuation ratios, and recent returns can be added to the CAPM to get better estimates for returns. These additional factors are known as the Fama-French factors. They’re named after the professors who developed the multiple linear regression model to better explain asset returns.

## Explain Like I’m 5 Years Old

Regression tries to see if there’s a relationship between two things, such as whether there’s a link between how you do one thing and how you do one or more other things.

Regression helps you make educated guesses, or predictions, based on past information. It’s about finding a pattern between two or more things and using that pattern to make a good guess about what might happen in the future.

## Why Is This Method Called Regression?

There’s some debate about the origins of the name, but this statistical technique was most likely termed “regression” by Sir Francis Galton in the 19th century. It described the statistical feature of biological data, such as the heights of people in a population, to regress to a mean level. There are shorter and taller people, but only outliers are very tall or short, and most people cluster somewhere around or “regress” to the average.

## What Is the Purpose of Regression?

Regression is used in statistical analysis to identify the associations between variables occurring in some data. It can show the magnitude of such an association and determine its statistical significance. Regression is a powerful tool for statistical inference and has been used to try to predict future outcomes based on past observations.

## How Do I Interpret a Regression Model?

A regression model output may be in the form of Y = 1.0 + (3.2)*X*_{*1*}- 2.0(*X_{2}*) + 0.21.

Here we have a multiple linear regression that relates some variable Y with two explanatory variables X_{1} and X_{2}. We would interpret the model as the value of Y changes by 3.2× for every one-unit change in X_{1.}If X_{1} goes up by 2, Y goes up by 6.4, holding all else constant.

This means that when controlling for X_{2}, X_{1} has this observed relationship. Every one-unit increase in X_{2} is associated with a 2× decrease**in Y if X_{1} holds constant. We can also note the y-intercept of 1.0, indicating that Y = 1 when X_{1} and X_{2} are both zero. The [error term](https://www.investopedia.com/terms/e/errorterm.asp) or residual is 0.21.

## What Are the Assumptions That Must Hold for Regression Models?

Four main assumptions about the underlying data process of what you’re analyzing must hold to properly interpret the output of a regression model:

- The relationship between variables is linear.
- There must be homoskedasticity, or the variance of the variables and the error term must remain constant.
- All explanatory variables are independent of each other.
- All variables are normally distributed.

## The Bottom Line

Regression is a statistical method that tries to determine the strength and character of the relationship between one dependent variable and a series of other variables. It’s used in finance, investing, and other disciplines.

Regression analysis uncovers the associations between variables observed in data, but it can’t easily indicate causation.

