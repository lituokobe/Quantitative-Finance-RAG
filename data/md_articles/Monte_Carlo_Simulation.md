# Monte Carlo Simulation: What It Is, How It Works, History, 4 Key Steps

### Key Takeaways

- Monte Carlo simulations forecast a range of possible outcomes by modeling randomness in a system.
- They test multiple values for uncertain variables to generate an average of many potential results.
- These simulations rely on historical data and statistical assumptions about market behavior.
- Monte Carlo methods are increasingly combined with artificial intelligence to enhance forecasting accuracy.

## What Is a Monte Carlo Simulation?

A Monte Carlo simulation is a way to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of [random variables](https://www.investopedia.com/terms/r/random-variable.asp). It is a technique used to understand the impact of risk and uncertainty. Monte Carlo simulations can be applied to a range of problems in many fields, including investing, business, physics, and engineering. It is also referred to as a multiple probability simulation.

## How the Monte Carlo Simulation Assesses Risk

When faced with significant uncertainty in making a forecast or estimate, some methods replace the uncertain variable with a single average number. The Monte Carlo simulation instead uses multiple values and then averages the results.

Monte Carlo simulations have a vast array of applications in fields that are plagued by random variables, notably business and investing. They are used to estimate the probability of cost overruns in large projects and the likelihood that an asset price will move in a certain way.

[Telecommunications companies](https://www.investopedia.com/ask/answers/070815/what-telecommunications-sector.asp)use them to assess network performance in various scenarios, which helps them to optimize their networks. Insurers use them to measure the risks they may be taking on and to price their policies accordingly. Investment analysts use [Monte Carlo simulations to assess the risk](https://www.investopedia.com/articles/financial-theory/08/monte-carlo-multivariate-model.asp) that an entity will default, and to analyze [derivatives](https://www.investopedia.com/terms/d/derivative.asp) such as options. Financial planners can use them to predict the likelihood that a client will [run out of money in retirement](https://www.investopedia.com/financial-edge/0113/planning-your-retirement-using-the-monte-carlo-simulation.aspx).

Monte Carlo simulations also have many applications outside of business and finance, such as in meteorology, astronomy, and physics.

Today, Monte Carlo simulations are increasingly used in conjunction with new [artificial intelligence (AI)](https://www.investopedia.com/terms/a/artificial-intelligence-ai.asp) models. For example, as IBM noted in 2024, many financial firms now use high-performance computing systems to run Monte Carlo simulations and, "As the numbers of these simulations grow over ever-increasing portfolios of financial assets and instruments, the interpretation of these as an entirety becomes a growing challenge." That is where AI comes in. "The use of AI to assist a professional in their assessment of these simulations can both improve accuracy as well as deliver more timely insights. In a business where time-to-market is a key differentiator, this has direct business value," IBM says.

## History of the Monte Carlo Simulation

The Monte Carlo simulation was named after the famous gambling destination in Monaco because chance and random outcomes are central to this modeling technique, as they are to games like roulette, dice, and slot machines.

The technique was initially developed by Stanislaw Ulam, a mathematician who worked on the Manhattan Project, the secret effort to create the first atomic weapon. He shared his idea with John Von Neumann, a colleague at the Manhattan Project, and the two collaborated to refine the Monte Carlo simulation.

## How Monte Carlo Simulations Work

The Monte Carlo method acknowledges an issue for any simulation technique: The probability of varying outcomes cannot be firmly pinpointed because of random variable interference. Therefore, a Monte Carlo simulation focuses on constantly repeating random samples.

A Monte Carlo simulation takes the variable that has uncertainty and assigns it a random value. The model is then run, and a result is provided. This process is repeated again and again while assigning many different values to the variable in question. Once the simulation is complete, the results are averaged to arrive at an estimate.

## The 4 Steps in a Monte Carlo Simulation

To perform a Monte Carlo simulation, there are four main steps. As an example, Microsoft [Excel](https://www.investopedia.com/articles/investing/093015/create-monte-carlo-simulation-using-excel.asp) or a similar program can be used to create a Monte Carlo simulation that estimates the probable price movements of stocks or other assets.

There are two components to an asset's price movement: drift, which is its constant directional movement, and a random input, which represents market [volatility](https://www.investopedia.com/terms/v/volatility.asp).

By analyzing historical price data, you can determine the drift, [standard deviation](https://www.investopedia.com/terms/s/standarddeviation.asp), [variance](https://www.investopedia.com/terms/v/variance.asp), and average price movement of a security. These are the building blocks of a Monte Carlo simulation.

The four steps are as follows:

**Step 1.** To project one possible price trajectory, use the historical price data of the asset to generate a series of periodic daily returns using the natural logarithm (note that this equation differs from the usual percentage change formula):
$$\text{Periodic Daily Return} = \ln(\frac{\text{Day's Price}}{\text{Previous Day's Price}})$$

**Step 2.** Next, use the AVERAGE, STDEV.P, and VAR.P functions on the entire resulting series to obtain the average daily return, standard deviation, and variance inputs, respectively. The drift is equal to:
$$\text{Drift} = \text{Average Daily Return} - \frac{\text{Variance}}{2}$$
where:
- $\text{Average Daily Return} = \text{Produced from Excel’s AVERAGE function from periodic daily returns series}$
- $\text{Variance} = \text{Produced from Excel’s VAR.P function from periodic daily returns series}$

Alternatively, drift can be set to 0; this choice reflects a certain theoretical orientation, but the difference will not be huge, at least for shorter time frames.

**Step 3.** Next, obtain a random input:
$$\text{Random Value} = \sigma * \text{NORMSINV(RAND())}$$
where:
- $\sigma = \text{Standard deviation, produced from Excel’s STDEV.P function from periodic daily returns series}$
- $\text{NORMSINV and RAND} = \text{Excel functions}$

The equation for the following day's price is:
$$\text{Next Day’s Price} = \text{Today’s Price} * e^{(\text{Drift} + \text{Random Value})}$$

**Step 4.** To take *e* to a given power *x* in Excel, use the EXP function: EXP(x). Repeat this calculation the desired number of times. (Each repetition represents one day.) The result is a simulation of the asset's future price movement.
By generating an arbitrary number of simulations, you can assess the probability that a security's price will follow a given trajectory.

## Monte Carlo Simulation Results Explained

In many models, outcomes follow a [normal distribution](https://www.investopedia.com/terms/n/normaldistribution.asp) or [bell-curve,](https://www.investopedia.com/terms/b/bell-curve.asp) with the most likely return at the center. This means the actual result is just as likely to fall above that point as below it.

The probability that the actual return will be within one standard deviation of the most probable ("expected") rate is 68%. The probability is 95% that it will be within two standard deviations and 99.7% that it will be within three standard deviations.

Still, there is no guarantee that the most expected outcome will occur, or that actual movements will not exceed the wildest projections.

Crucially, a Monte Carlo simulation ignores everything not built into the price movement, such as [macro trends](https://www.investopedia.com/terms/m/macro-environment.asp), a company's leadership, market hype, and [cyclical factors](https://www.investopedia.com/terms/b/businesscycle.asp).

In other words, it assumes a perfectly [efficient market](https://www.investopedia.com/terms/e/efficientmarkethypothesis.asp), where price movements follow statistically consistent patterns derived from historical data, even though real-world markets can behave unpredictably.

## Advantages and Disadvantages of a Monte Carlo Simulation

The Monte Carlo simulation was created to overcome a perceived disadvantage of other methods of estimating a probable outcome.

The difference is that the Monte Carlo method tests a number of random variables and then averages them, rather than starting out with an average.

Like any financial simulation, the Monte Carlo method relies on historical price data as the basis for a projection of future price data. It then disrupts the pattern by introducing random variables, represented by numbers. Finally, it averages those numbers to arrive at an estimate of the risk that the pattern will be disrupted in real life.

Of course, no simulation can pinpoint an inevitable outcome. The Monte Carlo method aims at a sounder estimate of the probability that an outcome will differ from a projection.

## How Is the Monte Carlo Simulation Used in Finance?

A Monte Carlo simulation is used to estimate the probability of a certain outcome. As such, it is widely used by investors and financial analysts to evaluate the probable success of investments they're considering. Some common uses include:

- Pricing stock options: The potential price movements of the underlying asset are tracked, given every possible variable. The results are averaged and then discounted to the asset's current price. This is intended to indicate the probable payoff of the options.
- [Portfolio](https://www.investopedia.com/terms/p/portfolio.asp) valuation: A number of alternative portfolios can be tested using the Monte Carlo simulation in order to arrive at a measure of their comparative risk.
- Fixed-income investments: The short rate is the random variable here. The simulation is used to calculate the probable impact of movements in the short rate on fixed-income investments, such as bonds.

## What Professions Use the Monte Carlo Simulation?

It may be best known for its financial applications, but the Monte Carlo simulation is used in virtually every profession that must measure risks and prepare to meet them.

For example, a telecommunications company may build its network to sustain all of its users all of the time. To do that, it must consider all of the possible variations in demand for the service. It must determine whether the system will stand the strain of peak hours and peak seasons.

A Monte Carlo simulation may help the company decide whether its service is likely to stand the strain of a Super Bowl Sunday as well as an average Sunday in August.

## What Factors Are Evaluated in a Monte Carlo Simulation?

A Monte Carlo simulation in investing is based on historical price data for the asset or assets being evaluated.

The building blocks of the simulation, derived from the historical data, are drift, standard deviation, variance, and average price movement.

## The Bottom Line

The Monte Carlo simulation shows the spectrum of probable outcomes for an uncertain scenario. This technique assigns multiple values to uncertain variables, obtains multiple results, and then takes the average of these results to arrive at an estimate.

From investing to engineering, the Monte Carlo method is used in many fields to measure risk, including estimating the likelihood of a gain or loss in an investment, or the odds that a project will run over budget.

