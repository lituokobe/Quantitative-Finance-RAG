import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag, NavigableString

HEADERS = {
    "User-Agent": "Tuo Li RAG Agent"
}

def clean_whitespace(text: str) -> str:
    """
    Collapse multiple spaces/newlines into a single space,
    but DO NOT strip leading/trailing whitespace blindly.
    This preserves the natural spacing between inline elements.
    """
    if not text:
        return ""
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    # Collapse multiple internal spaces to one
    return re.sub(r'\s+', ' ', text)

def is_math_container(elem: Tag) -> bool:
    """Check if an element is a wrapper for a math formula."""
    # Check for Investopedia's formula image pattern
    if elem.find("img", alt=re.compile(r"formula|equation|=", re.I)):
        return True
    # Check for MathJax or specific classes
    classes = elem.get("class", [])
    if "math" in classes or "comp-math-block" in str(classes):
        return True
    return False

def extract_math_latex(elem: Tag) -> str:
    """Extract the best available LaTeX representation from a math container."""
    # 1. Try to find an image with an alt tag (common in Investopedia)
    img = elem.find("img", alt=True)
    if img:
        alt = img['alt']
        # Clean up common prefixes like "Net Present Value ="
        if "=" in alt:
            return alt

    # 2. If no image, try to grab raw text but clean it heavily
    text = elem.get_text(" ", strip=True)
    return text

def elem_to_md_inline(elem: Tag) -> str:
    """
    Convert inline elements to Markdown while preserving boundary spacing.
    """
    if isinstance(elem, NavigableString):
        return clean_whitespace(str(elem))

    text = ""
    for child in elem.children:
        if isinstance(child, NavigableString):
            text += clean_whitespace(str(child))

        elif isinstance(child, Tag):
            # Recurse first
            inner_text = elem_to_md_inline(child)

            # Handle Tags
            if child.name == "a" and child.has_attr("href"):
                # Markdown link: [text](href)
                # We do NOT strip inner_text here to preserve internal spacing
                text += f"[{inner_text.strip()}]({child['href']})"
            elif child.name in ["strong", "b"]:
                text += f"**{inner_text.strip()}**"
            elif child.name in ["em", "i"]:
                text += f"*{inner_text.strip()}*"
            elif child.name == "br":
                text += "  \n"
            elif child.name == "sub":
                text += f"_{{{inner_text.strip()}}}"
            elif child.name == "sup":
                text += f"^{{{inner_text.strip()}}}"
            elif child.name == "span":
                # If it's an inline math span, treat it specially
                if "math" in child.get("class", []):
                    text += f"${inner_text.strip()}$"
                else:
                    text += inner_text
            else:
                text += inner_text

    return text

def table_to_md(table: Tag) -> str:
    """Convert HTML table to Markdown."""
    rows_md = []

    # Extract headers
    headers = [clean_whitespace(th.get_text(strip=True)) for th in table.find_all("th")]
    if not headers:
        # Try first row as header if no <th> tags
        first_row = table.find("tr")
        if first_row:
            headers = [clean_whitespace(td.get_text(strip=True)) for td in first_row.find_all("td")]

    if headers:
        rows_md.append("| " + " | ".join(headers) + " |")
        rows_md.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # Extract body
    for tr in table.find_all("tr"):
        # Skip header row if we already processed it
        if tr.find("th"):
            continue

        cells = [elem_to_md_inline(td).strip() for td in tr.find_all(["td"])]
        if not cells:
            continue

        # Pad row to match header length
        if len(cells) < len(headers):
            cells += [""] * (len(headers) - len(cells))

        rows_md.append("| " + " | ".join(cells) + " |")

    return "\n".join(rows_md) + "\n\n"

def process_block_element(elem: Tag) -> str:
    """
    Process block elements. Returns a string of Markdown.
    """
    # 1. Check for Math Container FIRST to avoid duplication
    # If this div/p contains a formula image, we ONLY want the formula, not the text labels around it.
    if is_math_container(elem):
        latex = extract_math_latex(elem)
        return f"\n$$\n{latex}\n$$\n\n"

    md_output = ""

    # 2. Headers
    if elem.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        level = int(elem.name[1])
        text = elem_to_md_inline(elem).strip()
        md_output += f"\n{'#' * level} {text}\n\n"

    # 3. Paragraphs
    elif elem.name == "p":
        # Get inline markdown with whitespace preserved
        content = elem_to_md_inline(elem)
        # Collapse excessive internal whitespace only now, then strip ends
        content = re.sub(r'\s+', ' ', content).strip()

        if content:
            md_output += f"{content}\n\n"

    # 4. Lists
    elif elem.name in ["ul", "ol"]:
        items = elem.find_all("li", recursive=False)
        for idx, li in enumerate(items):
            # Process content of the LI
            # We treat LI content as block-ish to handle nested stuff
            li_content = ""
            for child in li.children:
                if isinstance(child, Tag) and child.name in ["ul", "ol"]:
                    continue  # handled separately
                if isinstance(child, Tag):
                    # If the LI contains a P tag, process it as inline text to avoid breaking the list bullet
                    if child.name == "p":
                        li_content += elem_to_md_inline(child)
                    else:
                        li_content += elem_to_md_inline(child)
                elif isinstance(child, NavigableString):
                    li_content += clean_whitespace(str(child))

            li_content = re.sub(r'\s+', ' ', li_content).strip()
            prefix = f"{idx + 1}." if elem.name == "ol" else "-"
            md_output += f"{prefix} {li_content}\n"

            # Handle Nested Lists
            for nested in li.find_all(["ul", "ol"], recursive=False):
                nested_md = process_block_element(nested)
                indented = "\n".join(["  " + line for line in nested_md.strip().split('\n')])
                md_output += indented + "\n"
        md_output += "\n"

    # 5. Tables
    elif elem.name == "table":
        md_output += table_to_md(elem)

    # 6. Container Divs/Sections
    elif elem.name in ["div", "section", "article"]:
        for child in elem.children:
            if isinstance(child, Tag):
                md_output += process_block_element(child)

    return md_output


def scrape_investopedia(url: str, save_dir: str, safe_title:str| None):
    print(f"Fetching {url}...")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate Title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Article"

    # Locate Main Content
    # Strategy: Try specific ID first, then fallback to classes
    content_root = soup.find(id="mntl-sc-page_1-0")
    if not content_root:
        content_root = soup.find("main")

    if not content_root:
        raise ValueError("Could not find content root")

    md_lines = [f"# {title}\n\n"]

    # Process children
    for child in content_root.children:
        if isinstance(child, Tag):
            # Filter out ads and hidden instrumentation
            if "id" in child.attrs and "ad-" in str(child.attrs["id"]): continue
            if "class" in child.attrs and "mntl-sc-block-instrumentation" in child.attrs["class"]: continue

            md_lines.append(process_block_element(child))

    full_md = "".join(md_lines)

    # Final Cleanup: Remove excessive newlines (more than 2)
    full_md = re.sub(r'\n{3,}', '\n\n', full_md)

    # Save
    if not safe_title:
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    file_path = save_path / f"{safe_title}.md"
    file_path.write_text(full_md, encoding="utf-8")

    return file_path

# TODO: Scrape Investopedia articles, manual revision needed later
if __name__ == "__main__":
    # url = "https://www.investopedia.com/terms/n/npv.asp" #NPV
    # url = "https://www.investopedia.com/terms/b/blackscholes.asp"  #BSM
    # url = "https://www.investopedia.com/terms/c/capm.asp" #CAPM
    # url = "https://www.investopedia.com/terms/r/randomwalktheory.asp"  # random walk
    # url = "https://www.investopedia.com/terms/c/calloption.asp"  # call option
    # url = "https://www.investopedia.com/terms/p/putoption.asp"  # call option
    # url = "https://www.investopedia.com/terms/s/strikeprice.asp"  # strike price
    # url = "https://www.investopedia.com/terms/b/binomialoptionpricing.asp"  # binomial option pricing
    # url = "https://www.investopedia.com/terms/p/premium.asp"  # premium
    # url = "https://www.investopedia.com/terms/r/riskpremium.asp"  # risk premium
    # url = "https://www.investopedia.com/terms/g/governmentsecurity.asp" # government security
    # url = "https://www.investopedia.com/terms/r/riskfreeasset.asp"  # risk-free asset
    # url = "https://www.investopedia.com/terms/v/volatility.asp"  # volatility
    # "Market_Sentiment": "https://www.investopedia.com/terms/m/marketsentiment.asp",
    # "Black_Monday": "https://www.investopedia.com/terms/b/blackmonday.asp",
    # "Correction": "https://www.investopedia.com/terms/c/correction.asp",
    # "Entry-point": "https://www.investopedia.com/terms/e/entry-point.asp",
    # "Capitulation": "https://www.investopedia.com/terms/c/capitulation.asp",
    # "Federal_Fund_Rate": "https://www.investopedia.com/terms/f/federalfundsrate.asp",
    # "Great_Depression": "https://www.investopedia.com/terms/g/great_depression.asp",
    # "Infrastructure": "https://www.investopedia.com/terms/i/infrastructure.asp",
    # "Public-good": "https://www.investopedia.com/terms/p/public-good.asp",
    # "Private-good": "https://www.investopedia.com/terms/p/private-good.asp",
    # "Public-private-partnerships": "https://www.investopedia.com/terms/p/public-private-partnerships.asp",
    # "Tax_Revenue": "https://www.investopedia.com/tax-revenue-definition-5115103#:~:text=Tax%20revenue%20is%20defined%20as,of%20property%3B%20and%20other%20taxes.",
    # "OECD": "https://www.investopedia.com/terms/o/oecd.asp",
    # "Economy": "https://www.investopedia.com/terms/e/economy.asp",
    # "OTM": "https://www.investopedia.com/terms/o/outofthemoney.asp",
    # "ITM": "https://www.investopedia.com/terms/i/inthemoney.asp",
    # "ATM": "https://www.investopedia.com/terms/a/atthemoney.asp",
    # "Intrinsic_Value": "https://www.investopedia.com/terms/i/intrinsicvalue.asp",
    # "DJIA": "https://www.investopedia.com/terms/d/djia.asp",
    # "Bull_Market": "https://www.investopedia.com/terms/b/bullmarket.asp",
    # "Buy-and-hold": "https://www.investopedia.com/terms/b/buyandhold.asp",
    # "Bear_Market": "https://www.investopedia.com/terms/b/bearmarket.asp",
    # "Private_Company": "https://www.investopedia.com/terms/p/privatecompany.asp",
    # "Great_Recession": "https://www.investopedia.com/terms/g/great-recession.asp",
    # "MACD": "https://www.investopedia.com/terms/m/macd.asp",
    # "Value_at_Risk(VaR)": "https://www.investopedia.com/articles/04/092904.asp",
    # "Greeks": "https://www.investopedia.com/terms/g/greeks.asp",
    # "Regression": "https://www.investopedia.com/terms/r/regression.asp",
    # "Error_Term": "https://www.investopedia.com/terms/e/errorterm.asp",
    # "Normal_Distribution": "https://www.investopedia.com/terms/n/normaldistribution.asp",
    # "Kurtosis": "https://www.investopedia.com/terms/k/kurtosis.asp",
    # "Sharpe_Ratio": "https://www.investopedia.com/terms/s/sharperatio.asp",
    # "Portfolio_Return": "https://www.investopedia.com/terms/p/portfolio-return.asp",
    # "Expected_Return": "https://www.investopedia.com/terms/e/expectedreturn.asp",
    # "Stochastic_Modeling": "https://www.investopedia.com/terms/s/stochastic-modeling.asp",
    # "Divergence": "https://www.investopedia.com/terms/d/divergence.asp",
    # "RSI": "https://www.investopedia.com/terms/r/rsi.asp",
    # "Moving_Average": "https://www.investopedia.com/terms/m/movingaverage.asp",
    # "SMA": "https://www.investopedia.com/terms/s/sma.asp",
    # "EMA": "https://www.investopedia.com/terms/e/ema.asp",
    # "Quantitative_Analysis": "https://www.investopedia.com/terms/q/quantitativeanalysis.asp",
    # "DCF": "https://www.investopedia.com/terms/d/dcf.asp",
    # "Monte_Carlo_Simulation": "https://www.investopedia.com/terms/m/montecarlosimulation.asp",
    # "Option": "https://www.investopedia.com/terms/o/option.asp",
    # "Underlying_Asset": "https://www.investopedia.com/terms/u/underlying-asset.asp",
    # "Futures": "https://www.investopedia.com/terms/f/futures.asp",
    # "Golden_Cross": "https://www.investopedia.com/terms/g/goldencross.asp",
    # "Skewness": "https://www.investopedia.com/terms/s/skewness.asp",
    # "Standard_Deviation": "https://www.investopedia.com/terms/s/standarddeviation.asp",
    # "Log-normal_Distribution": "https://www.investopedia.com/articles/investing/102014/lognormal-and-normal-distribution.asp",
    # "Delta": "https://www.investopedia.com/terms/d/delta.asp",
    # "Theta": "https://www.investopedia.com/terms/t/theta.asp",
    # "Gamma": "https://www.investopedia.com/terms/g/gamma.asp",
    # "Vega": "https://www.investopedia.com/terms/v/vega.asp",
    # "Rho": "https://www.investopedia.com/terms/r/rho.asp",
    # "Risk": "https://www.investopedia.com/terms/r/risk.asp",

    try:
        url_dict = {

        }

        for k, v in url_dict.items():
            path = scrape_investopedia(v, "md_articles/new", k)
            print(f"Done: {path}")
    except Exception as e:
        print(f"Error: {e}")