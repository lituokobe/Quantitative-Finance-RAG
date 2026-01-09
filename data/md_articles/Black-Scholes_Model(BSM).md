# Black-Scholes Model: What It Is, How It Works, and the Options Formula

### Key Takeaways

- The Black-Scholes model is also known as the Black-Scholes-Merton or BSM model.
- It's a differential equation that's widely used to price options contracts.
- The Black-Scholes model requires five input variables: the strike price of an option, the current stock price, the time to expiration, the risk-free rate, and the volatility.
- The Black-Scholes model is usually accurate, but it makes certain assumptions that can lead to predictions that deviate from real-world results.
- The standard BSM model is only used to price European options because it doesn't take into account that American options could be exercised before the expiration date.

## What Is the Black-Scholes Model?

The Black-Scholes model, also known as the Black-Scholes-Merton (BSM) model, is one of the most important concepts in modern financial theory. It helps [traders and investors](https://www.investopedia.com/best-online-brokers-4587872) determine the fair value of an options contract.

This mathematical equation estimates the theoretical value of derivatives based on other investment instruments. It considers the impact of time and other risk factors in its calculation.

It was developed in 1973 and is still regarded as one of the best ways to price an options contract.

## History of the Black-Scholes Model

Developed by Fischer Black, Robert Merton, and Myron Scholes, the Black-Scholes model was the first widely used mathematical method to calculate the theoretical value of an option contract.

It uses current [stock prices](https://www.investopedia.com/best-stock-screeners-5120586), expected dividends, the option's strike price, expected interest rates, time to expiration, and expected volatility.

The initial equation was introduced in Black and Scholes' 1973 paper, "The Pricing of Options and Corporate Liabilities," published in the *Journal of Political Economy*.

Robert C. Merton helped edit the paper. He published his own article, "Theory of Rational Option Pricing," in *The Bell Journal of Economics and Management Science*later that year. He expanded the mathematical understanding and applications of the model, coining the term "Black–Scholes theory of options pricing."

Scholes and Merton received the Nobel Memorial Prize in Economic Sciences in 1997 for their work in finding "a new method to determine the value of derivatives."

Black died two years earlier, so he couldn't receive the Nobel Prize, as it isn't given posthumously. However, the Nobel Committee acknowledged his role in developing the Black-Scholes model.

## How the Black-Scholes Model Works

Black-Scholes posits that instruments such as stock shares or futures contracts will have a lognormal distribution of prices following a [random walk](https://www.investopedia.com/terms/r/randomwalktheory.asp) with constant drift and volatility. The equation uses this assumption and factors in other important variables to derive the price of a European-style [call option](https://www.investopedia.com/terms/c/calloption.asp).

The Black-Scholes equation requires six variables:

1. [Volatility](https://www.investopedia.com/terms/v/volatility.asp)
2. The price of the underlying asset
3. The [strike price](https://www.investopedia.com/terms/s/strikeprice.asp) of the option
4. The time until the expiration of the option
5. The risk-free interest rate
6. The type of option (call or put)

It's theoretically possible for options sellers to set rational prices with these variables for the options that they're selling.

The model predicts that the price of heavily traded assets follows a geometric Brownian motion with constant drift and volatility.

It incorporates the constant price variation of the [stock](https://www.investopedia.com/best-stock-screeners-5120586), the time value of money, the option's strike price, and the time to the option's expiry when it's applied to a stock option.

### Fast Fact

The Black-Scholes model is often contrasted against the [binomial model](https://www.investopedia.com/terms/b/binomialoptionpricing.asp) or a [Monte Carlo simulation](https://www.investopedia.com/terms/m/montecarlosimulation.asp).

### Black-Scholes Assumptions

The Black-Scholes model makes certain assumptions:

- No dividends are paid out during the life of the option.
- Markets are random because market movements can't be predicted.
- There are no transaction costs when buying the option.
- The [risk-free rate](https://www.investopedia.com/terms/r/risk-freerate.asp) and volatility of the underlying asset are known and constant.
- The returns of the underlying asset are normally distributed.
- The option is [European](https://www.investopedia.com/terms/e/europeanoption.asp) and can only be [exercised](https://www.investopedia.com/ask/answers/06/excerciseonexpiration.asp) at expiration.

The original Black-Scholes model didn't consider the effects of dividends paid during the life of the option, but the model is frequently adapted to account for dividends by determining the [ex-dividend](https://www.investopedia.com/terms/e/ex-dividend.asp) date value of the underlying stock.

The model is also modified by many option-selling market makers to account for the effect of options that can be exercised before expiration.

### Important

Firms will alternatively use a binomial or [trinomial](https://www.investopedia.com/terms/t/trinomialoptionpricingmodel.asp) model or the [Bjerksund-Stensland](https://www.investopedia.com/terms/b/bjerksundstensland-model.asp) model for the pricing of the more commonly traded [American-style](https://www.investopedia.com/terms/a/americanoption.asp) options.

## The Black-Scholes Model Formula

The mathematics involved in the formula are complicated and can be intimidating, but you don't have to know or even understand the math to use Black-Scholes modeling in your strategies.

Options traders have access to various online options calculators, and many of the top trading platforms boast robust options analysis tools that include indicators and spreadsheets that perform the calculations and output the options pricing values.

The Black-Scholes call option formula is calculated by multiplying the stock price by the cumulative standard normal probability distribution function.

The [net present value (NPV)](https://www.investopedia.com/terms/n/npv.asp) of the strike price multiplied by the cumulative standard normal distribution is then subtracted from the resulting value of the previous calculation.

$$C = S * N(d_1) − K * e^{-r * t} * N(d_2)$$
where:  
$$d_1= \frac{1}{\sigma * \sqrt{t}}\left[\ln{\left(\frac{S}{K}\right)} + {\left(r + \frac{\sigma^2}{2}\right)} * t\right]$$
and  
$$ d_2= d_1 - \sigma*\sqrt{t} $$
and where:  
- $C = \text{Call option price}$
- $S = \text{Current stock (or other underlying) price}$
- $K = \text{Strike price}$
- $r = \text{Risk-free interest rate}$
- $t = \text{Time to maturity}$
- $N(\cdot) = \text{Cumulative distribution function (CDF) of the standard normal distribution}$

## Volatility Skew

Black-Scholes assumes that stock prices follow a lognormal distribution because asset prices can't be negative; they're bounded by zero.

Asset prices are often observed to have significant right [skewness](https://www.investopedia.com/terms/s/skewness.asp) and some degree of [kurtosis](https://www.investopedia.com/terms/k/kurtosis.asp) or fat tails. High-risk downward moves often happen more often in the market than a normal distribution predicts.

According to the Black-Scholes model, the assumption of lognormal underlying asset prices should show that implied volatilities are similar for each strike price.

Since the 1987 market crash, at-the-money options have had lower implied volatility than options that are far out-of-the-money or deep in-the-money. The market is signaling a higher chance of a big drop in volatility.

This has led to the presence of the volatility skew. A smile or skewed shape can be seen when the implied volatilities for options with the same [expiration date](https://www.investopedia.com/terms/e/expiration-date.asp) are mapped out on a graph.

The Black-Scholes model is therefore not efficient for calculating implied volatility.

## Benefits and Limitations of the Black-Scholes Model

**Benefits:**
- Acts as a stable framework based on a defined method.
- Allows investors to mitigate risk by better understanding exposure
- May be used to devise strategies for creating a portfolio based on an investor's preferences.
- Streamlines and improves efficient calculating and reporting of figures

**Limitations:**
- Doesn't take all types of options into consideration
- May lack cashflow flexibility based on the future projections of a security
- May make inaccurate assumptions about future stable volatility
- Relies on several other assumptions that may not materialize into the actual price of the security

### Benefits of the Black-Scholes Model

The Black-Scholes model has been successfully implemented and used by many financial professionals due to the variety of benefits it has to offer.

- **Provides a framework:** The Black-Scholes model provides a theoretical framework for pricing options. This allows investors and traders to determine the fair price of an option using a structured, defined methodology that has been tried and tested.
- **Allows for risk management:** Investors can use the Black-Scholes model to manage their risk exposure to various assets by knowing the theoretical value of an option. The Black-Scholes model is therefore useful to investors not only in evaluating potential returns but also in understanding portfolio weakness and deficient investment areas.
- **Allows for portfolio optimization:** The Black-Scholes model can be used to optimize portfolios by providing a measure of the expected returns and risks associated with different options. This allows investors to make smarter choices that are better aligned with their risk tolerance and pursuit of profit.
- **Enhances market efficiency:** The Black-Scholes model has led to greater market efficiency and transparency as traders and investors are better able to price and trade options. This simplifies the pricing process because there's a greater implicit understanding of how prices are derived.
- **Streamlines pricing:** The Black-Scholes model is widely accepted and used by practitioners in the financial industry, allowing for greater consistency and comparability across markets and jurisdictions.

### Limitations of the Black-Scholes Model

The Black-Scholes model is widely used, but there are still some drawbacks to the model.

- **Limits usefulness:** The Black-Scholes model is only used to price European options. It doesn't take into account that U.S. options could be exercised before the expiration date.
- **Lacks cash flow flexibility:** The model assumes dividends and risk-free rates are constant, but this may not be the case. The Black-Scholes model may therefore lack the ability to truly reflect the accurate future cash flow of an investment due to model rigidity.
- **Assumes constant volatility:** The model also assumes that volatility remains constant over the option's life. This is often not the case because volatility fluctuates with the level of supply and demand.
- **Misleads other assumptions:** The Black-Scholes model also leverages other assumptions. These include: there are no transaction costs or taxes, the risk-free interest rate is constant for all maturities, short selling of securities with the use of proceeds is permitted, and no arbitrage opportunities come without risk. Each of these assumptions can lead to prices that deviate from actual results.

## What Does the Black-Scholes Model Do?

The Black-Scholes model, also known as the Black-Scholes-Merton (BSM), was the first widely used model for option pricing. The equation calculates the price of a European-style call option based on known variables like the current price, maturity date, and strike price, based on certain assumptions about the behavior of asset prices.

It does so by subtracting the [net present value (NPV)](https://www.investopedia.com/terms/n/npv.asp) of the strike price multiplied by the cumulative standard normal distribution from the product of the stock price and the cumulative standard normal probability distribution function.

## What Are the Inputs for the Black-Scholes Model?

The inputs for the Black-Scholes equation are volatility, the price of the underlying asset, the strike price of the option, the time until the expiration of the option, the risk-free interest rate, and the type of option. It's theoretically possible for options sellers to set rational prices with these variables for the options they're selling.

## What Assumptions Does the Black-Scholes Model Make?

The original Black-Scholes model assumes that the option is a European-style option and can only be exercised at expiration.

It also assumes that no dividends are paid out during the option's life, that market movements follow a random walk and can't be predicted, that there are no transaction costs involved in buying the option, that the risk-free rate and volatility of the underlying option are known and constant, and that the prices of the underlying asset follow a log-normal distribution.

## What Are the Limitations of the Black-Scholes Model?

The Black-Scholes model is only used to price European options. It doesn't take into account that American options could be exercised before the expiration date. The model also assumes that dividends, volatility, and risk-free rates remain constant over the option's life. Not taking taxes, commissions, or trading costs into account can also lead to valuations that deviate from real-world results.

## The Bottom Line

The Black-Scholes model is a mathematical model that's used by [traders](https://www.investopedia.com/best-online-brokers-4587872) to calculate the fair price or theoretical value of an asset.

It provides a way to calculate the theoretical value of an option by taking into account the underlying asset's current price, the option's type, the option's strike price, the time remaining until expiration, the risk-free interest rate, and the volatility of the underlying asset.

The Black-Scholes model has had a profound impact on finance and has led to the development of a wide range of derivative products such as futures, swaps, and options.

