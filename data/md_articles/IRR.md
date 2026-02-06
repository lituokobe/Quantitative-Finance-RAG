# Internal Rate of Return (IRR): Formula and Examples

## What Is IRR?

IRR, or internal rate of return, is a metric used in financial analysis to estimate the profitability of potential investments. IRR is a discount rate that makes the net present value (NPV) of all cash flows equal to zero in a discounted cash flow analysis.

In simple terms, IRR indicates the annualized rate of return a project or investment is expected to generate. A higher IRR signals a more attractive investment. No matter what type of project or investment you’re analyzing (a new factory, a real estate deal, a tech startup, etc.), the IRR formula is the same. The consistency of calculating the IRR across all opportunities makes it an excellent metric for investors to use in ranking and comparing projects.

### Key Takeaways

- IRR is calculated using the same concept as net present value (NPV), except it sets the NPV equal to zero.
- The ultimate goal of IRR is to identify the rate of discount, which makes the present value of the sum of annual nominal cash inflows equal to the initial net cash outlay for the investment.
- IRR is ideal for analyzing capital budgeting projects to understand and compare potential rates of annual return over time.
- In addition to being used by companies to determine which capital projects to use, IRR can help investors determine the investment return of various assets.

## The Formula for IRR

The formula used to determine IRR is as follows:

$$0=\text{NPV}=\sum_{t=1}^{T}\frac{C_t}{\left(1+IRR\right)^t}-C_0$$
where:
- $C_t=\text{Net cash inflow during the period t}$
- $C_0=\text{Total initial investment costs}$
- $IRR=\text{The internal rate of return}$
- $t=\text{The number of time periods}$

### How to Calculate the IRR

The manual calculation of the IRR metric involves the following steps:

1. Using the formula, one would set NPV equal to zero and solve for the discount rate, which is the IRR.
2. Note that the initial investment is always negative because it represents an outflow.
3. Each subsequent cash flow could be positive or negative, depending on the estimates of what the project delivers or requires as a capital injection in the future.

Because of the nature of the formula, IRR cannot be easily calculated analytically and instead must be calculated iteratively through trial and error or by using software programmed to calculate IRR (e.g., using Excel).

### How to Calculate IRR in Excel

Using the IRR function in Excel makes calculating the IRR easy. Excel does all the necessary work for you, arriving at the discount rate you are seeking to find.

1. Enter Cash Flows: In an Excel spreadsheet, list all the cash flows associated with the investment or project. These cash flows can be both positive (inflows) and negative (outflows).
2. Arrange Cash Flows: Organize the cash flows in chronological order, with the initial investment (usually a negative value) at the beginning and subsequent cash flows listed in the order they occur.
3. Use IRR Function: In a cell where you want the IRR value to appear, use the IRR function. The syntax for the IRR function is: =IRR(values)
4. The "values" are the range of cells containing the cash flows. Make sure to select all cash flows including the initial investment.
5. Example: Let's say your cash flows are in cells A1 through A5, where A1 represents the initial investment and A2 through A5 represent subsequent cash flows. You would input the following formula in a cell where you want the IRR displayed: =IRR(A1:A5)

Here is a simple example of an IRR analysis with cash flows that are known and annually periodic (one year apart). Assume a company is assessing the profitability of Project X. Project X requires \$250,000 in funding and is expected to generate \$100,000 in after-tax cash flows in the first year and grow by \$50,000 for each of the next four years.

|                      |       2020A | 2021P      | 2022P      | 2023P      | 2024P      | 2025P      |
|----------------------|------------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| Initial Investment   | (\$250,000) |            |            |            |            |            |
| After-Tax Cash Flows |             | \$100,000  | \$150,000  | \$200,000  | \$250,000  | \$300,000  |


In this case, the IRR is 56.72%, which is quite high.

Excel also offers two other functions that can be used in IRR calculations: the XIRR and the MIRR. XIRR is used when the cash flow model does not exactly have annual periodic cash flows. The MIRR is a rate-of-return measure that includes the integration of the cost of capital and the risk-free rate.

#### How to Calculate IRR in Excel

## Understanding IRR

The ultimate goal of IRR is to identify the rate of discount, which makes the present value of the sum of annual nominal cash inflows equal to the initial net cash outlay for the investment. Several methods can be used when seeking to identify an expected return, but IRR is often ideal for analyzing the potential return of a new project that a company is considering undertaking.

Think of IRR as the rate of growth that an investment is expected to generate annually. Thus, it can be most similar to a compound annual growth rate (CAGR). In reality, an investment will usually not have the same rate of return each year. Usually, the actual rate of return that a given investment ends up generating will differ from its estimated IRR.

## What Is IRR Used For?

In capital planning, one popular scenario for IRR is comparing the profitability of establishing new operations with that of expanding existing operations. For example, an energy company may use IRR in deciding whether to open a new power plant or to renovate and expand an existing power plant.

While both projects could add value to the company, one will likely be the more logical decision as prescribed by IRR. Note that because IRR does not account for changing discount rates, it’s often not adequate for longer-term projects with discount rates that are expected to vary.

IRR is also useful for corporations in evaluating stock buyback programs. Clearly, if a company allocates substantial funding to repurchasing its shares, then the analysis must show that the company’s own stock is a better investment—that is, has a higher IRR—than any other use of the funds, such as creating new outlets or acquiring other companies.

Individuals can also use IRR when making financial decisions—for instance, when evaluating different insurance policies using their premiums and death benefits. The consensus is that policies that have the same premiums and a high IRR are much more desirable.

Note that life insurance has a very high IRR in the early years of the policy—often more than 1,000%. It then decreases over time. This IRR is very high during the early days of the policy because if you made only one monthly premium payment and then suddenly died, your beneficiaries would still get a lump sum benefit.

Another common use of IRR is in analyzing investment returns. In most cases, the advertised return will assume that any interest payments or cash dividends are reinvested back into the investment. What if you don’t want to reinvest dividends but need them as income when paid? And if dividends are not assumed to be reinvested, are they paid out, or are they left in cash? What is the assumed return on the cash? IRR and other assumptions are particularly important on instruments like annuities, where the cash flows can become complex.

Finally, IRR is a calculation used for an investment’s money-weighted rate of return (MWRR). The MWRR helps determine the rate of return needed to start with the initial investment amount factoring in all of the changes to cash flows during the investment period, including sales proceeds.

## Using IRR With WACC

Most IRR analyses will be done in conjunction with a view of a company’s weighted average cost of capital (WACC) and NPV calculations. IRR is typically a relatively high value, which allows it to arrive at an NPV of zero.

Most companies will require an IRR calculation to be above the WACC. WACC is a measure of a firm’s cost of capital in which each category of capital is proportionately weighted. All sources of capital, including common stock, preferred stock, bonds, and any other long-term debt, are included in a WACC calculation.

In theory, any project with an IRR greater than its cost of capital should be profitable. In planning investment projects, firms will often establish a required rate of return (RRR) to determine the minimum acceptable return percentage that the investment in question must earn to be worthwhile. The RRR will be higher than the WACC.

Any project with an IRR that exceeds the RRR will likely be deemed profitable, although companies will not necessarily pursue a project on this basis alone. Rather, they will likely pursue projects with the highest difference between IRR and RRR, as these will likely be the most profitable.

IRR may also be compared against prevailing rates of return in the securities market. If a firm can’t find any projects with an IRR greater than the returns that can be generated in the financial markets, then it may simply choose to invest money in the market. Market returns can also be a factor in setting an RRR.

### Fast Fact

Analyses will also typically involve NPV calculations at different assumed discount rates.

## IRR vs. Compound Annual Growth Rate

The CAGR measures the annual return on an investment over a period of time. The IRR is also an annual rate of return; however, the CAGR typically uses only a beginning and ending value to provide an estimated annual rate of return.

IRR differs in that it involves multiple periodic cash flows—reflecting that cash inflows and outflows often constantly occur when it comes to investments. Another distinction is that CAGR is simple enough that it can be calculated easily.

## IRR vs. Return on Investment (ROI)

Companies and analysts may also look at the return on investment (ROI) when making capital budgeting decisions. ROI tells an investor about the total growth, start to finish, of the investment. It is not an annual rate of return. IRR tells the investor what the annual growth rate is. The two numbers normally would be the same over the course of one year but won’t be the same for longer periods.

ROI is the percentage increase or decrease of an investment from beginning to end. It is calculated by taking the difference between the current or expected future value and the original beginning value, divided by the original value, and multiplied by 100.

ROI figures can be calculated for nearly any activity into which an investment has been made and an outcome can be measured. However, ROI is not necessarily the most helpful for lengthy time frames. It also has limitations in capital budgeting, where the focus is often on periodic cash flows and returns.

## Limitations of IRR

IRR is generally ideal for use in analyzing capital budgeting projects. It can be misconstrued or misinterpreted if used outside of appropriate scenarios. In the case of positive cash flows followed by negative ones and then by positive ones, the IRR may have multiple values. Moreover, if all cash flows have the same sign (i.e., the project never turns a profit), then no discount rate will produce a zero NPV.

Within its realm of uses, IRR is a very popular metric for estimating a project’s annual return; however, it is not necessarily intended to be used alone. IRR is typically a relatively high value, which allows it to arrive at an NPV of zero. The IRR itself is only a single estimated figure that provides an annual return value based on estimates. Since estimates of IRR and NPV can differ drastically from actual results, most analysts will choose to combine IRR analysis with scenario analysis. Scenarios can show different possible NPVs based on varying assumptions.

As mentioned, most companies do not rely on IRR and NPV analyses alone. These calculations are usually also studied in conjunction with a company’s WACC and an RRR, which provides for further consideration.

Companies usually compare IRR analysis to other tradeoffs. If another project has a similar IRR with less up-front capital or simpler extraneous considerations, then a simpler investment may be chosen despite IRRs.

In some cases, issues can also arise when using IRR to compare projects of different lengths. For example, a project of a short duration may have a high IRR, making it appear to be an excellent investment. Conversely, a longer project may have a low IRR, earning returns slowly and steadily. The ROI metric can provide some more clarity in these cases, although some managers may not want to wait out the longer time frame.

## Investing Based on IRR

The internal rate of return rule is a guideline for evaluating whether to proceed with a project or investment. The IRR rule states that if the IRR on a project or investment is greater than the minimum RRR—typically the cost of capital, then the project or investment can be pursued.

Conversely, if the IRR on a project or investment is lower than the cost of capital, then the best course of action may be to reject it. Overall, while there are some limitations to IRR, it is an industry standard for analyzing capital budgeting projects.

## IRR Example

Assume a company is reviewing two projects. Management must decide whether to move forward with one, both, or neither. Its cost of capital is 10%. The cash flow patterns for each are as follows:

**Project A**

- Initial Outlay = \$5,000
- Year one = \$1,700
- Year two = \$1,900
- Year three = \$1,600
- Year four = \$1,500
- Year five = \$700

**Project B**

- Initial Outlay = \$2,000
- Year one = \$400
- Year two = \$700
- Year three = \$500
- Year four = \$400
- Year five = \$300

The company must calculate the IRR for each project. The initial outlay (period = 0) will be negative. Solving for IRR is an iterative process using the following equation:

$$\$0 = Σ CF*t ÷ (1 + IRR)*t$$

where:
- $CF = \text{net cash flow}$
- $IRR = \text{internal rate of return}$
- $t = \text{period (from 0 to last period)}$

-or-

$$\$0 = (\text{initial outlay} * −1) + CF1 ÷ (1 + IRR)*1 + CF2 ÷ (1 + IRR)*2 + ... + CFX ÷ (1 + IRR)*X$$

Using the above examples, the company can calculate IRR for each project as:

**IRR Project A**

$$\$0 = (−\$5,000) + \$1,700 ÷ (1 + IRR)*1 + \$1,900 ÷ (1 + IRR)*2 + \$1,600 ÷ (1 + IRR)*3 + \$1,500 ÷ (1 + IRR)*4 + \$700 ÷ (1 + IRR)*5$$

IRR Project A = **16.61%**

**IRR Project B**

$$\$0 = (−\$2,000) + \$400 ÷ (1 + IRR)*1 + \$700 ÷ (1 + IRR)*2 + \$500 ÷ (1 + IRR)*3 + \$400 ÷ (1 + IRR)*4 + \$300 ÷ (1 + IRR)*5$$

IRR Project B = **5.23%**

Given that the company’s cost of capital is 10%, management should proceed with Project A and reject Project B.

## What Does Internal Rate of Return Mean?

The internal rate of return (IRR) is a financial metric used to assess the attractiveness of a particular investment opportunity. When you calculate the IRR for an investment, you are effectively estimating the rate of return of that investment after accounting for all of its projected cash flows together with the time value of money. When selecting among several alternative investments, the investor would then select the investment with the highest IRR, provided it is above the investor’s minimum threshold. The main drawback of IRR is that it is heavily reliant on projections of future cash flows, which are notoriously difficult to predict.

## Is IRR the Same as ROI?

Although IRR is sometimes referred to informally as a project’s “return on investment,” it is different from the way most people use that phrase. Often, when people refer to ROI, they are simply referring to the percentage return generated from an investment in a given year or across a period. However, that type of ROI does not capture the same nuances as IRR, and for that reason, IRR is generally preferred by investment professionals.

Another advantage of IRR is that its definition is mathematically precise, whereas the term ROI can mean different things depending on the context or the speaker.

## What Is a Good Internal Rate of Return?

Whether an IRR is good or bad will depend on the cost of capital and the opportunity cost of the investor. For instance, a real estate investor might pursue a project with a 25% IRR if comparable alternative real estate investments offer a return of, say, 20% or lower. However, this comparison assumes that the riskiness and effort involved in making these difficult investments are roughly the same. If the investor can obtain a slightly lower IRR from a project that is considerably less risky or time-consuming, then they might happily accept that lower-IRR project. In general, though, a higher IRR is better than a lower one, all else being equal.

## The Bottom Line

The internal rate of return (IRR) is a metric used to estimate the return on an investment. The higher the IRR, the better the return of an investment. As the same calculation applies to varying investments, it can be used to rank all investments to help determine which is the best. The one with the highest IRR is generally the best investment choice.

IRR is an important tool for companies in determining where to invest their capital. Companies have a variety of options to help grow their business. These include building out new operations, improving existing operations, making acquisitions, and so on. IRR can help determine which option to choose by showing which will have the best return.