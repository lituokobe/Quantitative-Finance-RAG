evaluation_set = [
	#-- -- - A.Core Definitions-- -- -
    {
		"id": 1,
		"category": "Core",
		"question": "What is Net Present Value (NPV)?",
		"reference": "The difference between the present value of cash inflows and the present value of cash outflows over a period of time, accounting for the time value of money. It determines the profitability of an investment by discounting future cash flows to today's value. A positive NPV indicates a potentially profitable project, while a negative NPV suggests it may not be worthwhile. It is used in capital budgeting to analyze profitability."
	},
	{
		"id": 2,
		"category": "Core",
		"question": "What does internal rate of return (IRR) represent?",
		"reference": "The Internal Rate of Return (IRR) is a financial metric representing the annualized rate of return an investment is expected to yield, calculated as the discount rate that makes the Net Present Value (NPV) of all cash flows from a particular project equal to zero. IRR is the interest rate where the investment breaks even."
	},
	{
		"id": 3,
		"category": "Core",
		"question": "What is a call option?",
		"reference": "A financial contract that gives the buyer the right, but not the obligation, to purchase an underlying asset (such as stocks, commodities, or currency) at a specified strike price within a specific time period. Investors buy call options when they are bullish, expecting the asset's price to rise. "
	},
	{
		"id": 4,
		"category": "Core",
		"question": "What is volatility in financial markets?",
		"reference": "Volatility measures the degree of variation in the price of a financial asset or market index over a specific period, commonly measured by standard deviation. It acts as a key indicator of risk, with higher volatility signifying larger, often unpredictable price swings in both directions, and lower volatility indicating more stable, gradual movements. "
	},
	{
		"id": 5,
		"category": "Core",
		"question": "What does beta measure in CAPM?",
		"reference": "Beta measures the sensitivity of an asset’s returns to movements in the overall market and represents systematic risk relative to the overall market. It determines how much an investment's price is expected to swing in response to market movements, representing risk that cannot be eliminated through diversification. Beta of 1.0 moves in line with the market; >1.0 is more volatile."
	},
	{
		"id": 6,
		"category": "Core",
		"question": "What is liquidity?",
		"reference": "Liquidity measures how quickly and easily an asset can be converted into cash without significantly affecting its market price. It represents the ease of trading (market liquidity) or a company's ability to cover short-term debts (accounting liquidity). Cash is the most liquid asset, while real estate or specialized equipment are generally illiquid. "
	},
	{
		"id": 7,
		"category": "Core",
		"question": "What is a zero-coupon bond?",
		"reference": "A zero-coupon bond is a fixed-income security that pays no regular interest (coupons) but is issued at a deep discount to its face value, allowing the investor to receive the full face value at maturity. The profit is the difference between the purchase price and the face value. These are popular for long-term, goal-based investing like retirement or education. "
	},
	{
		"id": 8,
		"category": "Core",
		"question": "What is the time value of money?",
		"reference": "The concept that a sum of money is worth more now than the same sum in the future due to its potential earning capacity."
	},
	{
		"id": 9,
		"category": "Core",
		"question": "What is dividend yield?",
		"reference": "A financial ratio showing how much a company pays out in dividends each year relative to its stock price: $\\text{Dividend Yield} = \\frac{\\text{Annual Dividends per Share}}{\\text{Price per Share}}$. It indicates the cash return an investor can expect to receive for every dollar invested in a stock, acting as a key metric for income-focused investors."
	},
	{
		"id": 10,
		"category": "Core",
		"question": "What is systematic risk?",
		"reference": "The inherent risk to the entire market or market segment that cannot be eliminated through diversification. It's also known as undiversifiable risk, volatility risk, or market risk. It’s the result of macroeconomic events that affect the market as a whole and cannot be controlled, at least by an investor."
	},
	{
		"id": 11,
		"category": "Core",
		"question": "What is operating revenue?",
		"reference": "Income generated from a company's primary business activities before deducting operating expenses. It is a crucial indicator of a company's operational efficiency, sustainability, and ability to generate consistent, day-to-day income. "
	},
	{
		"id": 12,
		"category": "Core",
		"question": "What is the risk-free rate?",
		"reference": "The theoretical rate of return of an investment with zero risk, typically represented by government bond yields. It serves as a foundational benchmark for calculating expected returns, cost of equity (CAPM), and valuing investments. "
	},
	{
		"id": 13,
		"category": "Core",
		"question": "What is a Russian option?",
		"reference": "A Russian option is a perpetual American-style lookback option that provides the holder with the maximum price of the underlying asset achieved during the option's life. Introduced by Larry Shepp and A.N. Shiryaev to reduce 'regret' for not exercising at the optimal time, this path-dependent derivative guarantees a minimum payout based on the historical maximum price without a fixed expiration date. "
	},
	{
		"id": 14,
		"category": "Core",
		"question": "What is a coupon bond?",
		"reference": "A debt instrument that pays fixed or floating periodic interest (coupons) to the bondholder and returns principal at maturity."
	},
	{
		"id": 15,
		"category": "Core",
		"question": "What is the equity risk premium?",
		"reference": "The excess return that investing in the stock market provides over a risk-free rate. It serves as compensation for the higher volatility and risk associated with equities, typically calculated as the difference between the expected stock market return and the risk-free rate. "
	},

	#-- -- - B. Direct Comparison of Closely Related Concepts (Precision Stress) -- -- -
    {
		"id": 16,
		"category": "Comparison",
		"question": "What is the difference between NPV and IRR?",
		"reference": "NPV (Net Present Value) shows a project's absolute dollar value added by discounting future cash flows. IRR (Internal Rate of Return) gives the percentage return, the rate where NPV is zero, indicating project efficiency. NPV is scale-dependent; IRR is not."
	},
	{
		"id": 17,
		"category": "Comparison",
		"question": "How does nominal rate of return differ from real rate of return?",
		"reference": "The nominal rate of return is the raw, advertised, or historical percentage increase in an investment's value, ignoring inflation. The real rate of return is the inflation-adjusted rate, reflecting the true increase in purchasing power: $\\text{Real Rate} \\approx \\text{Nominal Rate} - \\text{Inflation Rate}$. While nominal shows how much more money you have, the real rate shows what that money is actually worth. "
	},
	{
		"id": 18,
		"category": "Comparison",
		"question": "What is the difference between a call option and a put option?",
		"reference": "A call option is the right to buy (holders betting on price increase); a put option is the right to sell (holders betting on price decrease)."
	},
	{
		"id": 19,
		"category": "Comparison",
		"question": "How does systematic risk differ from unsystematic risk?",
		"reference": "Systematic risk (market risk) affects the entire market, driven by macro factors like inflation or recessions, and cannot be diversified away; unsystematic risk is unique to a company or industry and can be reduced or eliminated through portfolio diversification. Diversification spreads risk across assets, mitigating the impact of company-specific problems, while systematic risk remains, as broad economic forces impact all investments to some degree."
	},
	{
		"id": 20,
		"category": "Comparison",
		"question": "What is the difference between Russian options and European options?",
		"reference": "Russian options are a type of perpetual 'lookback' option that allow the holder to exercise at any time, with a payoff based on the maximum (for calls) or minimum (for puts) underlying asset price achieved during the option's life. In contrast, European options can only be exercised on the specific expiration date. Russian options are designed to reduce 'regret' for not selling at the peak (or buying at the trough). European options are generally used for hedging or speculation on a specific future date. Due to their flexible exercise and lookback nature, Russian options are generally more expensive than standard European options. "
	},
	{
		"id": 21,
		"category": "Comparison",
		"question": "How does the spot market differ from the futures market?",
		"reference": "The spot market involves buying or selling assets for immediate delivery and payment at current prices, resulting in instant ownership. Conversely, the futures market uses contracts to trade assets at a predetermined price on a future date, often used for hedging or speculation without immediate ownership. "
	},
	{
		"id": 22,
		"category": "Comparison",
		"question": "What is the difference between dividend yield and earnings yield?",
		"reference": "Dividend yield measures the cash return paid to shareholders relative to the share price ($\text{Annual Dividend Per Share} / \text{Price Per Share}$). Earnings yield is the inverse of P/E ratio ($\text{Earnings Per Share} / \text{Price Per Share}$), measuring earnings relative to price. Dividend yield indicates immediate income, whereas earnings yield indicates potential value, often highlighting if a stock is cheap or expensive. "
	},
	{
		"id": 23,
		"category": "Comparison",
		"question": "How does CAPM differ from the Gordon Growth Model?",
		"reference": "CAPM determines the expected return on equity based on risk/beta, making it suitable for any risky asset; GGM calculates stock value or cost of equity based on constant dividend growth, limiting it to stable, dividend-paying companies. "
	},
	{
		"id": 24,
		"category": "Comparison",
		"question": "What is the difference between liquidity and market depth?",
		"reference": "Liquidity refers to the ease and speed with which an asset can be bought or sold without significantly affecting its price, emphasizing the immediate trade-off between transaction speed and price. Market depth (Depth of Market, or DOM) measures a market's ability to absorb large, unexpected orders without causing significant price fluctuations. While liquidity is the general concept of market activity, depth is a specific metric shows the volume of orders available at various price levels. "
	},
	{
		"id": 25,
		"category": "Comparison",
		"question": "How does volatility differ from variance?",
		"reference": "Variance is the average squared deviation; Volatility is the square root of variance (Standard Deviation)."
	},
	{
		"id": 26,
		"category": "Comparison",
		"question": "What is the difference between bond valuation and bond yield?",
		"reference": "Bond valuation determines price by discounting future cash flows; bond yield is the discount rate that equates the bond’s price to its cash flows."
	},
	{
		"id": 27,
		"category": "Comparison",
		"question": "How does hedging differ from speculation?",
		"reference": "Speculation aims to profit from future price movements by taking calculated risks, embracing volatility for potential high returns, while hedging seeks to reduce risk by taking offsetting positions, acting like insurance to protect against adverse price changes, prioritizing stability over maximum profit. "
	},

	#-- -- - C.Math Formula -- -- -
    {
		"id": 28,
		"category": "Formula",
		"question": "What is the formula for expected return in CAPM?",
		"reference": "$E(R_i) = R_f + \\beta_i * (ER_m - R_f)$"
	},
	{
		"id": 29,
		"category": "Formula",
		"question": "What is the formula for return on equity (ROE)?",
		"reference": "$ROE = \\frac{\\text{Net Income}}{\\text{Shareholder's Equity}}$"
	},
	{
		"id": 30,
		"category": "Formula",
		"question": "What is the formula for portfolio variance?",
		"reference": "For 2 assets: $\\sigma_p^2 = w_A^2 * \\sigma_A^2 + w_B^2 * \\sigma_B^2 + 2 * w_A * w_B * \\sigma_A * \\sigma_B * \\rho_{AB}$"
	},
	{
		"id": 31,
		"category": "Formula",
		"question": "What is the formula for standard deviation in finance?",
		"reference": "$\\sigma = \\sqrt{\\frac{1}{N} * \\sum_{i=1}^{N} (R_i - \\bar{R})^2}$"
	},
	{
		"id": 32,
		"category": "Formula",
		"question": "What is the formula for Value at Risk (VaR)?",
		"reference": "$VaR = \\mu - Z * \\sigma$"
	},
	# -- -- - D.Quantitative / Calculation -- -- -
	{
		"id": 33,
		"category": "Calculation",
		"question": "What is the Black-Scholes model for call options, and how is it used to calculate the call option price if stock price = 100, strike price = 102, risk-free rate = 4%, volatility = 20%, time to maturity = 1 year?",
		"reference": "The Black-Scholes model call option formula is $C = S * N(d_1) - K * e^{-r * T} * N(d_2)$, where $d_1= \frac{1}{\sigma * \sqrt{t}}\left[\ln{\left(\frac{S}{K}\right)} + {\left(r + \frac{\sigma^2}{2}\right)} * t\right]$, $d_2= d_1 - \sigma*\sqrt{t}$, $C = \text{Call option price}$, and where $S = \text{Current stock (or other underlying) price}$, $K = \text{Strike price}$, $r = \text{Risk-free interest rate}$, $t = \text{Time to maturity}$, $N(\cdot) = \text{Cumulative distribution function (CDF) of the standard normal distribution}$. With the inputs, $d_1$ is roughly 0.2010, $d_2$ is 0.0010, the call price is approximately \$8.93."
	},
	{
		"id": 34,
		"category": "Calculation",
		"question": "What is the formula for the exponential moving average (EMA)? How is it calculated over three periods for prices 100, 102, and 101 using smoothing factor 0.2? Please set the first EMA to the first price.",
		"reference": "$EMA_t = [\\text{Price}_t * \\alpha] + [EMA_{t-1} * (1 - \\alpha)]$. For 100, 102, 101 with $\\alpha=0.2$, EMA is 100.52."
	},
	{
		"id": 35,
		"category": "Calculation",
		"question": "What is the formula for future value with compounding? What is the future value of 1,000 at 5% for 3 years?",
		"reference": "$FV = PV * (1 + r)^n$. For 1,000 at 5% for 3 years, $FV = 1,157.63$."
	},
	{
		"id": 36,
		"category": "Calculation",
		"question": "What is the formula for the Sharpe ratio? Calculate it for portfolio return 8%, risk-free 2%, and std dev 10%.",
		"reference": "$S_p = \\frac{R_p - R_f}{\\sigma_p}$. Result: $\\frac{0.08 - 0.02}{0.10} = 0.6$."
	},
	{
		"id": 37,
		"category": "Calculation",
		"question": "How is WACC calculated if the cost of equity is 10%, the cost of debt is 5%, equity weight is 60%, debt weight is 40%, and corporate tax rate is 20%?",
        "reference": "$WACC = w_e * r_e + w_d * r_d * (1-T)$. With $w_e=0.6$, $r_e=0.10$, $w_d=0.4$, $r_d=0.05$, $T=0.20$, $WACC = 0.6 * 0.10 + 0.4 * 0.05 * (1-0.20) = 0.076$."

	},

	#-- -- - E.Compounded Topics-- -- -
    {
		"id": 38,
		"category": "Compound",
		"question": "How do stocks and bonds differ as asset classes?",
		"reference": "Stocks represent equity ownership in a company with higher risk/return potential, while bonds represent debt, acting as a loan to an entity for steady income. Stocks offer capital appreciation and dividends, whereas bonds provide fixed, regular interest payments and return of principal. "
	},
	{
		"id": 39,
		"category": "Compound",
		"question": "How do futures and options differ?",
		"reference": "Futures require buying/selling an asset at a set price on a future date (obligation), while options give the buyer the right, not obligation, to do so, risking only the premium paid. Futures are riskier with unlimited loss potential for both parties. But in option trading, buyers risk limited to premium, while sellers risk unlimited losses. Both are leveraged derivatives, magnifying gains and losses, but options offer downside protection for buyers."
	},
	{
		"id": 40,
		"category": "Compound",
		"question": "How does monetary policy influence inflation?",
		"reference": "Monetary policy influences inflation primarily by adjusting interest rates and managing the money supply to control aggregate demand. Central banks raise interest rates to increase borrowing costs, decrease money supply and spending, which lowers inflation. Conversely, lowering rates encourages borrowing, boosting economic activity to increase inflation."
	},
	{
		"id": 41,
		"category": "Compound",
		"question": "How does interest rate risk affect bond prices?",
		"reference": "They have an inverse relationship. When market interest rates rise, bond prices fall, and when interest rates fall, bond prices rise. This occurs because newly issued bonds with higher coupons make existing, lower-rate bonds less attractive, reducing their market value. "
	},
	{
		"id": 42,
		"category": "Compound",
		"question": "How does diversification reduce portfolio risk?",
		"reference": "Diversification reduces portfolio risk by spreading investments across various asset classes, industries, and geographies, ensuring that poor performance in one area is offset by gains in another. By avoiding over-concentration in a single asset, it mitigates unsystematic risks and lowers overall volatility. "
	},
	{
		"id": 43,
		"category": "Compound",
		"question": "How does inflation affect real returns?",
		"reference": "Inflation erodes purchasing power, lowering the real value of the nominal return. If inflation exceeds the nominal investment return, the real return becomes negative, meaning the investment loses purchasing power over time."
	},
	{
		"id": 44,
		"category": "Compound",
		"question": "How does credit risk affect bond yields?",
		"reference": "High credit risk directly causes bond yields to rise as investors demand higher compensation (risk premiums) for holding riskier debt. When credit risk increases, or a credit rating is downgraded, bond prices fall, which drives up the yield to compensate for the higher probability of default."
	},
	{
		"id": 45,
		"category": "Compound",
		"question": "How do primary markets and secondary markets differ?",
		"reference": "Primary is for new security issuance created and sold for the first time (e.g., IPOs) directly from issuers to investors to raise capital; secondary is for trading existing securities among investors, providing liquidity without direct involvement from the issuing company."
	},

	# -- -- - E.Edge / Recall Stress-- -- -
    {
		"id": 46,
		"category": "Edge",
		"question": "What is Gamma in options Greeks?",
		"reference": "Gamma measures the rate of change in Delta for a \$1 move in the underlying asset's price. It acts as a second-order risk measure. High Gamma means Delta changes rapidly, often peaking for at-the-money options near expiration. "
	},
	{
		"id": 47,
		"category": "Edge",
		"question": "What does Theta measure in option pricing?",
		"reference": "Theta measures the rate of decline in option value due to the passage of time (time decay). It quantifies how much value an option loses as it approaches expiration, assuming all other factors like underlying price and volatility remain constant."
	},
	{
		"id": 48,
		"category": "Edge",
		"question": "What is Value at Risk (VaR)?",
		"reference": "A statistical measure of the maximum potential loss over a specific timeframe at a given confidence level. It provides a single, easy-to-understand figure representing the threshold of maximum expected loss, often used for risk management. "
	},
	{
		"id": 49,
		"category": "Edge",
		"question": "What is the purpose of a structured product?",
		"reference": "Structured products are pre-packaged, fixed-term investments designed to meet specific investor needs by tailoring risk-return profiles. They combine conventional assets (like bonds) with derivatives to provide customized exposure, such as capital protection, enhanced yield, or access to specific market, equity, or commodity indices."
	},
	{
		"id": 50,
		"category": "Edge",
		"question": "What is stochastic modeling used for in finance?",
		"reference": "Stochastic modeling in finance analyzes and predicts the behavior of financial markets by incorporating random variables, allowing professionals to quantify uncertainty in asset prices, interest rates, and investment returns. It is heavily used for option pricing, risk management, asset-liability management, and portfolio optimization. "
	}
]