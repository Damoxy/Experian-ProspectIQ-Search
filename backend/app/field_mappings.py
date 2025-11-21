"""
Field mappings for Experian API response transformation
"""

import logging
from typing import Dict, Any, List
from collections import OrderedDict
from value_mappings import transform_response_data

logger = logging.getLogger('experian_api.field_mappings')

# Field priority configuration - lower numbers show first
FIELD_PRIORITIES: Dict[str, int] = {
    # High priority fields (show first in exact order)
    "First Name": 1,
    "Last Name": 2,
    "Address Line 1": 3,
    "Address City": 4,
    "State": 5,
    "Address Postal Code": 6,
    "Street1": 7,  # Adding the actual field name from results
    # Medium priority fields will be sorted alphabetically after high priority
    # Low priority fields will appear at the end
}

# Fields to completely hide from results
HIDDEN_FIELDS: List[str] = [
    "RECORD_ID",
    "BATCH_ID", 
    "PROCESS_DATE",
    "API_VERSION",
    "DEBUG_INFO",
    "INTERNAL_ID",
    "Raw Response",
    "Processing Timestamp",
    "Client Id",
    "Timetracker",
    "Result Code",
    "Type",
    # Add more fields to hide as needed
]

# Suffix mappings from API field suffixes to user-friendly names
SUFFIX_MAPPINGS: Dict[str, str] = {
    "FIRST NAME": "First Name",
    "LAST NAME": "Last Name",
    "EDUCATION LEVEL MODEL": "Level of Education",
    "PERMARITALSTATUS": "Marital Status", 
    "LIVUCOUNTCHILDREN": "Number of Children in Household",
    "LIVULENGTHRESIDENCE": "Length of Residence",
    "LIVUHOMEOWNER": "Homeowner",
    "RENTER": "Renter",
    "LIV LU MAILRESP": "Mail Responder",
    "ESTIMATED CURRENT HOME VALUE": "Estimated Current Home Value",
    "ADDRESS QUALITY": "Address Quality Indicator",
    "ADDR RSIZ PROP": "Property Type",
    "ADDR RVAL TOTL": "Home Total Value",
    "LIVU ADDR RSIZ BUILDSF": "Home Square Footage",
    "ADDR RVAL TAX": "Real Estate Tax",
    "ADDR RVAL LAND": "Home Land Value",
    "ADDR RSIZ BEDR": "Home: Number of Bedrooms",
    "LIV RCHR SWIM POOL IND": "Home: Swimming Pool",
    "LIVUADDRRSIZBASF": "Home: Base Square Footage",
    "MORTGAGE TERM": "Home: Mortgage Term",
    "MORTGAGE PURCHASE DATE": "Home: Purchase Date",
    "LIV TRAN AMNT": "Home: Home Purchase Price",
    "MDN POCN 4 6 SCORE V3": "Child Age 4-6 Present",
    "MDN POCN 7 9 SCORE V3": "Child Age 7-9 Present",
    "MDN POCN 10 12 SCORE V3": "Child Age 10-12 Present",
    "MDN POCN 13 15 SCORE V3": "Child Age 1-15 Present",
    "MDN POCN 16 18 SCORE V3": "Child Age 16-18 Present",
    "LIV PRCH AMNT I1": "Investment Property: Purchase Amount",
    "MORTGAGE LENDER OTHER": "Investment Property: Mortgage Lender",
    "MORTGATE TERM OTHER": "Investment Property: Mortgage Term",
    "LIV RSIZ BLD SQF RNG": "Property/Realty: Building square footage ranges",
    "MORTGAGE AMOUNT RANGES": "Mortgage/Home Purchase: Purchase amount ranges",
    "LIV MORT AMNT RNG": "Mortgage/Home Purchase: Mortgage amount ranges",
    "LIV GREEN AWARE": "Green Aware Household",
    "COMPOSITION CODE": "Household Composition",
    "ZIPLENGTHRESIDENCE": "Length of Residence",
    "ZIP DWELLING UNIT SIZE CD": "Dwelling Size in Livable Units",
    "ZIPCOUNTADULT": "Number of Adults in Home",
    "LIV POCN 4 6 GENDER": "Children by Age/Gender",
    "LIV POCN 7 9 GENDER": "Children by Age/Gender",
    "STREET2": "Address Line 1",
    "FULL ADDRESS": "Address Line 2", 
    "CITY": "Address City",
    "ZIP": "Address Postal Code",
    "PERBIRTHDATE": "Person #: Birth Year and Month",
    "PERBUSINESSOWNER": "Person #: Business Owner",
    "PERETHNICCODE": "Person #: Ethnic - Ethnic",
    "NEW MOVER INDICATOR": "New Mover: Indicator last 6 months",
    "LIVU NEW HOMEOWNER": "New Homeowner Indicator 6M",
    "ESTIMATED CUR MONTHLY MORTGAGE PAYMENT": "Estimated Currently Monthly Mortgage",
    "YEAR BUILT": "Property/Realty: Year Built",
    "ZIP4 MDN HHINC": "Median: Est HH Income Range V6",
    "PSCS AUA0300 AVG": "Average number of auto loan and lease trades",
    "AVG AUTO LOAN TRD": "Average number of auto loan trades",
    "AVG EXT COLLECTION TRD": "Average number of external collection trades",
    "AVG INSTLMT TRD": "Average number of installment trades",
    "PSCS VANTAGE AVG": "Overall Financial Health Score",
    "HIGH VS LOW AFFLUENCE SCORE": "Affluence Score",
    "LIV SURV COLLECT OTHER B2150": "HH:Acty/Int:Collecting:Other Collectibles",
    "LIV SURV COLLECT ART ANTQ B2151": "HH:Acty/Int:Collecting:Art/Antiques",
    "LIV SURV COLLECT COINS B2152": "HH:Acty/Int:Collecting:Stamps/Coins",
    "LIV SURV COLLECT DOLLS B2154": "HH:Acty/Int:Collecting:Dolls",
    "LIV SURV COLLECT FIGURINES B2155": "HH:Acty/Int:Collecting:Figurines",
    "LIV SURV COLLECT SP MEMO B2157": "HH:Acty/Int:Collecting:Sports Memorabilia",
    "LIV SURV COOK COOKING B2170": "HH:Acty/Int:Cooking/Entertaining:Cooking",
    "LIV SURV COOK BAKING B2171": "HH:Acty/Int:Cooking/Entertaining:Baking",
    "LIV SURV COOK WT CONS B2172": "HH:Acty/Int:Cooking/Entertaining:Cook/Weight Con",
    "LIV SURV COOK WINE APR B2173": "HH:Acty/Int:Cooking/Entertaining:Wine Appreciation",
    "LIV SURV COOK GOURMET B2174": "HH:Acty/Int:Cooking/Entertaining:Cooking- Gourmet",
    "LIV SURV CRAFT CRAFTS B2185": "HH:Acty/Int:Crafts:Crafts",
    "LIV SURV CRAFT NEEDLE B2186": "HH:Acty/Int:Crafts:Knitting/Needlework",
    "LIV SURV CRAFT QUILTING B2187": "HH:Acty/Int:Crafts:Quilting",
    "LIV SURV CRAFT SEWING B2188": "HH:Acty/Int:Crafts:Sewing",
    "LIV SURV CRAFT WOODWORK B2189": "HH:Acty/Int:Crafts:Woodworking",
    "SURVEY INTEREST HEALTH FITNESS": "HH:Acty/Int:Health/Fitness:Losing Weight",
    "SURVEY HEALTH SUPPLEMENT": "SRVY:HH Acty/Int:Health/Fitness:Vit Supplements",
    "LIV SURV HEALTH NAT FOODS B2212": "HH:Acty/Int:Health/Fitness:Hlth/Nat Foods",
    "LIV SURV HOBBY PHOTO B2250": "HH:Acty/Int:Hobbies:Photography Hobbies",
    "LIV SURV HOBBY GARDEN B2251": "HH:Acty/Int:Hobbies:Gardening Hobbies",
    "LIV SURV HOBBY CAR AUTO B2258": "HH:Acty/Int:Hobbies:Cars And Auto Repair",
    "LIV SURV HOBBY SELF IMPR B2260": "HH:Acty/Int:Hobbies:Self-Improvement",
    "LIV SURV MUSIC CHRISTIAN B2280": "HH:Acty/Int:Music:Christian/Gospel",
    "LIV SURV MUSIC R AND B B2281": "HH:Acty/Int:Music:R And B",
    "LIV SURV MUSIC JAZZ B2282": "HH:Acty/Int:Music:Jazz/New Age",
    "LIV SURV MUSIC CLASSICAL B2283": "HH:Acty/Int:Music:Classical",
    "LIV SURV MUSIC ROCKNROLL B2284": "HH:Acty/Int:Music:Rock N Roll",
    "LIV SURV MUSIC COUNTRY B2285": "HH:Acty/Int:Music:Country",
    "LIV SURV MUSIC GENERAL B2287": "HH:Acty/Int:Music:Music In General",
    "LIV SURV MUSIC OTHER B2268": "HH:Acty/Int:Music:Other Music",
    "LIV SURV READ FICTION B2301": "HH:Acty/Int:Reading:Best Selling Fiction",
    "LIV SURV READ CHILDRENS B2304": "HH:Acty/Int:Reading:Childrens Reading",
    "LIV SURV READ COMPUTER B2305": "HH:Acty/Int:Reading:Computer",
    "LIV SURV READ COOKING B2306": "HH:Acty/Int:Reading:Cooking/Culinary",
    "LIV SURV READ CTY LIFE B2307": "HH:Acty/Int:Reading:Country Lifestyle",
    "LIV SURV READ ENT PEOPLE B2308": "HH:Acty/Int:Reading:Entertainment/People",
    "LIV SURV READ FASHION B2309": "HH:Acty/Int:Reading:Fashion",
    "LIV SURV READ HISTORY B2310": "HH:Acty/Int:Reading:History",
    "LIV SURV READ INT DECOR B2311": "HH:Acty/Int:Reading:Interior Decorating",
    "LIV SURV READ HEALTH B2313": "HH:Acty/Int:Reading:Medical/Health",
    "LIV SURV READ MILITARY B2314": "HH:Acty/Int:Reading:Military",
    "LIV SURV READ MYSTERY B2315": "HH:Acty/Int:Reading:Mystery",
    "LIV SURV READ HLTH REMDES B2316": "HH:Acty/Int:Reading:Natural Health Remedies",
    "LIV SURV READ ROMANCE B2319": "HH:Acty/Int:Reading:Romance",
    "LIV SURV READ SC FICTION B2320": "HH:Acty/Int:Reading:Science Fiction",
    "LIV SURV READ SC TECH B2321": "HH:Acty/Int:Reading:Science/Technology",
    "LIV SURV READ SPORTS B2322": "HH:Acty/Int:Reading:Sports Reading",
    "LIV SURV READ CUR AFFAIRS B2323": "HH:Acty/Int:Reading:World News/Politics",
    "LIV SURV READ BOOK READER B2327": "HH:Acty/Int:Reading:Book Reader",
    "LIV SURV SOCL ANIMAL B2350": "HH:Acty/Int:Socl Caus/Con:Animal Wf Soc/Caus/Con",
    "LIV SURV SOCL ENV WILDLIFE B2351": "HH:Acty/Int:Socl Caus/Con:Environment/Wildlife",
    "LIV SURV SOCL POL CNSRVTIVE B2352": "HH:Acty/Int:Socl Caus/Con:Political- Conservative",
    "LIV SURV SOCL POL LIBERAL B2353": "HH:Acty/Int:Socl Caus/Con:Political- Liberal",
    "LIV SURV SOCL CHILDREN B2355": "HH:Acty/Int:Socl Caus/Con:Children",
    "LIV SURV SOCL VETERANS B2356": "HH:Acty/Int:Socl Caus/Con:Veterans",
    "LIV SURV SOCL HEALTH B2357": "HH:Acty/Int:Socl Caus/Con:Hlty/Soc Cause/Con",
    "LIV SURV SOCL OTHER B2358": "HH:Acty/Int:Socl Caus/Con:Othr Soc/Cause Con",
    "LIV SURV SPORT BASEBALL B2375": "HH:Acty/Int:Sports/Rec:Baseball",
    "LIV SURV SPORT BASKTBALL B2377": "HH:Acty/Int:Sports/Rec:Basketball",
    "LIV SURV SPORT HOCKEY B2378": "HH:Acty/Int:Sports/Rec:Hockey",
    "LIV SURV SPORT CAMPING B2379": "HH:Acty/Int:Sports/Rec:Camping/Hiking",
    "LIV SURV SPORT HUNTING B2380": "HH:Acty/Int:Sports/Rec:Hunting",
    "LIV SURV SPORT FISHING B2381": "HH:Acty/Int:Sports/Rec:Fishing",
    "LIV SURV SPORT NASCAR B2382": "HH:Acty/Int:Sports/Rec:Nascar",
    "LIV SURV SPORT FITNESS B2383": "HH:Acty/Int:Sports/Rec:Personal Fitness/Exercise",
    "LIV SURV SPORT SCUBA B2384": "HH:Acty/Int:Sports/Rec:Scuba Diving",
    "LIV SURV SPORT FOOTBALL B2385": "HH:Acty/Int:Sports/Rec:Football",
    "LIV SURV SPORT GOLF B2386": "HH:Acty/Int:Sports/Rec:Golf",
    "LIV SURV SPORT SKIING B2387": "HH:Acty/Int:Sports/Rec:Snow Skiing/Boarding",
    "LIV SURV SPORT BOATING B2389": "HH:Acty/Int:Sports/Rec:Boating/Sailing",
    "LIV SURV SPORT WALKING B2390": "HH:Acty/Int:Sports/Rec:Walking",
    "LIV SURV SPORT CYCLING B2393": "HH:Acty/Int:Sports/Rec:Cycling",
    "LIV SURV SPORT MTRCYCLE B2395": "HH:Acty/Int:Sports/Rec:Motorcycles",
    "LIV SURV SPORT RUNNING B2396": "HH:Acty/Int:Sports/Rec:Running/Jogging",
    "LIV SURV SPORT SOCCER B2398": "HH:Acty/Int:Sports/Rec:Soccer",
    "LIV SURV SPORT SWIMMING B2399": "HH:Acty/Int:Sports/Rec:Swimming",
    "LIV SURV SPORT PLAY GEN B2402": "HH:Acty/Int:Sports/Rec:Play Sports In General",
    "LIV SURV SWEEP SWEEPSTKS B2425": "HH:Acty/Int:Sweepstakes:Sweepstakes",
    "LIV SURV SWEEP LOTTERIES B2426": "HH:Acty/Int:Sweepstakes:Lotteries",
    "LIV SURV TRVL CRUISE B2440": "HH:Acty/Int:Travel:Cruise",
    "LIV SURV TRVL FOREIGN B2441": "HH:Acty/Int:Travel:International",
    "LIV SURV TRVL DOMESTIC B2442": "HH:Acty/Int:Travel:Domestic",
    "LIV SURV TRVL TIMESHARE B2443": "HH:Acty/Int:Travel:Time Share",
    "LIV SURV TRVL ENJ RC VECLE B2446": "HH:Acty/Int:Travel:Recreational Vehicle",
    "LIV SURV TRVL ENJ RV B2447": "HH:Acty/Int:Travel:Would Enjoy Rv Travel",
    "LIV SURV TRVL BUSINESS B2448": "HH:Acty/Int:Travel:Business Travel",
    "LIV SURV TRVL PERSONAL B2449": "HH:Acty/Int:Travel:Personal Travel",
    "LIV SURV INET OWN COMPUTER B2475": "HH:Acty/Int:PC & Internet:Own Computer",
    "SURVEY USE INTERNET": "HH:Acty/Int:PC & Internet:Use Internet Service",
    "LIV SURV INET DSL B2478": "HH:Acty/Int:PC & Internet:Usedsl/Hispd",
    "LIV SURV INET BY COMPUTER B2482": "HH:Acty/Int:PC & Internet:Plan To Buy Computer",
    "SURVEY CELL PHONE": "HH:Acty/Int:Elctrncs/Gdgts:Cell Phone",
    "LIV SURV GADG CD PLAYER B2501": "HH:Acty/Int:Elctrncs/Gdgts:Compact Disc Player",
    "LIV SURV GADG DVD PLAYER B2503": "HH:Acty/Int:Elctrncs/Gdgts:Dvd Player",
    "LIV SURV GADG SATDISH B2504": "HH:Acty/Int:Elctrncs/Gdgts:Satellite Dish",
    "LIV SURV GADG DIGCAM B2510": "HH:Acty/Int:Elctrncs/Gdgts:Digital Camera",
    "LIV SURV GADG HDTV B2512": "HH:Acty/Int:Elctrncs/Gdgts:Hdtv",
    "LIV SURV GADG INTSTELEC B2513": "HH:Acty/Int:Elctrncs/Gdgts:Interest In Electronics",
    "LIV SURV GADG PDA BBERRY B2516": "HH:Acty/Int:Elctrncs/Gdgts:Pda/Blackberry",
    "LIV SURV GADG VDOCAMERA B2519": "HH:Acty/Int:Elctrncs/Gdgts:Video Camera",
    "LIV SURV GADG VDO GAMESYS 2520": "HH:Acty/Int:Elctrncs/Gdgts:Video Game System",
    "LIV SURV ARTS CULTURAL B2531": "HH:Acty/Int:Cltrl/Arts:Interest In Cultrual Arts",
    "LIV SURV MAGZ BUSINESS B2547": "HH:Acty/Int:Magazines:Business And Finance",
    "LIV SURV MAGZ CHILDRENS B2548": "HH:Acty/Int:Magazines:Childrens Magazines",
    "LIV SURV MAGZ COMPUTER B2549": "HH:Acty/Int:Magazines:Computer/Electronics",
    "LIV SURV MAGZ GAMES B2550": "HH:Acty/Int:Magazines:Crafts Games And Hobbies",
    "LIV SURV MAGZ FITNESS B2554": "HH:Acty/Int:Magazines:Fitness",
    "LIV SURV MAGZ FOOD B2555": "HH:Acty/Int:Magazines:Food/Wine/Cooking",
    "LIV SURV MAGZ GARDEN B2556": "HH:Acty/Int:Magazines:Gardening Magazines",
    "LIV SURV MAGZ FISHING B2558": "HH:Acty/Int:Magazines:Hunting And Fishing",
    "LIV SURV MAGZ MENS B2559": "HH:Acty/Int:Magazines:Mens",
    "LIV SURV MAGZ MUSIC B2560": "HH:Acty/Int:Magazines:Music",
    "LIV SURV MAGZ SPORTS B2566": "HH:Acty/Int:Magazines:Sports Magazines",
    "LIV SURV MAGZ SUBSCRIBE B2568": "HH:Acty/Int:Magazines:Subscription",
    "LIV SURV MAGZ TRAVEL B2569": "HH:Acty/Int:Magazines:Travel",
    "LIV SURV MAGZ WOMENS B2570": "HH:Acty/Int:Magazines:Womens",
    "LIV SURV MAGZ NEWS B2573": "HH:Acty/Int:Magazines:Current Events/News",
    "LIV SURV MEM MUSIC CLUB B2858": "HH:Lifestyl:Affiliation/Member:Music Club",
    "LIV SURV CARD AMEX PRM B2900": "HH:Lifestyl:Credit Cards:American Express/Premium",
    "LIV SURV CARD AMEX REG B2901": "HH:Lifestyl:Credit Cards:American Express/Regular",
    "LIV SURV CARD DISC PRM B2903": "HH:Lifestyl:Credit Cards:Discover/Premium",
    "LIV SURV CARD DISC REG B2904": "HH:Lifestyl:Credit Cards:Discover/Regular",
    "LIV SURV CARD PRM CREDIT B2905": "HH:Lifestyl:Credit Cards:Other Card/Premium",
    "LIV SURV CARD OTHER REG B2906": "HH:Lifestyl:Credit Cards:Other Card/Regular",
    "LIV SURV CARD STORE REG B2907": "HH:Lifestyl:Credit Cards:Store Or Retail/Regular",
    "LIV SURV CARD VISA REG B2909": "HH:Lifestyl:Credit Cards:Visa/Regular",
    "LIV SURV CARD MSTR REG B2912": "HH:Lifestyl:Credit Cards:Mastercard/Regular",
    "LIV SURV FUN PREREC VDO B3050": "HH:Lifestyl:Entertainment:Buy Pre-Recorded Videos",
    "LIV SURV FUN WATCH TV B3055": "HH:Lifestyl:Entertainment:Watch Cable Tv",
    "LIV SURV FUN WATCH VIDEO B3056": "HH:Lifestyl:Entertainment:Watch Videos",
    "LIV SURV INVST CDS MNYMKT B3075": "HH:Lifestyl:Financial:Cds/Money Mkt - Cur",
    "LIV SURV INVST IRA CURR B3077": "HH:Lifestyl:Financial:Iras - Currently",
    "LIV SURV INVST IRA FUTR B3078": "HH:Lifestyl:Financial:Iras - Future Interest",
    "LIV SURV INVST LIFINS CURR B3079": "HH:Lifestyl:Financial:Life Insur. - Cur",
    "LIV SURV INVST MUTL CURR B3080": "HH:Lifestyl:Financial:Mutual Funds - Currently",
    "LIV SURV INVST MUTL FUTR B3081": "HH:Lifestyl:Financial:Mutl Funds/ - Fut Int",
    "LIV SURV INVST OTHER CURR B2082": "HH:Lifestyl:Financial:Othr Invest - Cur",
    "LIV SURV INVST OTHER FUTR B3083": "HH:Lifestyl:Financial:Othr Invest - Future",
    "LIV SURV INVST RL EST CURR B3084": "HH:Lifestyl:Financial:Real Estate- Currently",
    "LIV SURV INVST RL EST FUTR B3085": "HH:Lifestyl:Financial:Real Estate - Fut",
    "LIV SURV INVST STOCKS CURR B3086": "HH:Lifestyl:Financial:Stks/Bond - Cur",
    "LIV SURV INVST STOCKS FUTR B3087": "HH:Lifestyl:Financial:Stks/Bond - Fut",
    "LIV SURV LIFE GRAND KIDS B3125": "HH:Lifestyl:Grandkids:Proud Grandparent",
    "SURVEY MILITARY GOV VETERAN": "HH:Lifestyl:Military/Gov:Vetern",
    "LIV SURV LIFE PETS CAT B3225": "HH:Lifestyl:Pets:Own A Cat",
    "LIV SURV LIFE PETS DOG B3226": "HH:Lifestyl:Pets:Own A Dog",
    "LIV SURV LIFE PETS OTHER B3227": "HH:Lifestyl:Pets:Own A Pet",
    "PREFER BUY COMPUTER": "HH:Lifestyl:Buying Interest:Comp/Elec",
    "PREFER BUY SPORTS REL": "HH:Lifestyl:Buying Interest:Sports Related",
    "EST AVAILABLE EQUITY AMT": "Real Estate: Available Equity Amount",
    "EST CUR MORTGAGE AMT": "Real Estate: Estimated Current Mortgage Amount",
    "STREET2": "Address Line 1",
    "FULL ADDRESS": "Address Line 2",
    "CITY": "Address City",
    "ZIP": "Address Postal Code",
    "PERBIRTHDATE": "Person #: Birth Year and Month",
    "PERBUSINESSOWNER": "Person #: Business Owner",
    "PERETHNICCODE": "Person #: Ethnic - Ethnic",
    "NEW MOVER INDICATOR": "New Mover: Indicator last 6 months",
    "LIVU NEW HOMEOWNER": "New Homeowner Indicator 6M",
    "ESTIMATED CUR MONTHLY MORTGAGE PAYMENT": "Estimated Currently Monthly Mortgage",
    "YEAR BUILT": "Property/Realty: Year Built",
    "LIV DSE APPAREL": "DSE: Apparel",
    "LIV DSE MISC": "DSE: Travel",
    "LIV DSE DINE OUT": "DSE: Dine Out",
    "LIV DSE ALCOHOL WINE": "DSE: Alcohol and Wine",
    "LIV DSE ENTERTAINMENT": "DSE: Entertainment",
    "LIV DSE PERSONAL": "DSE: Personal",
    "LIV DSE READING": "DSE: Reading",
    "LIV DSE EDUCATION": "DSE: Education",
    "LIV DSE DONATION": "DSE: Donation",
    "LIV DSE FURNISHINGS": "DSE: Furnishings",
    "DSE DINE OUT": "DSE: Dine Out",
    "DSE ALCOHOL WINE": "DSE: Alcohol and Wine",
    "DSE APPAREL": "DSE: Apparel",
    "DSE ENTERTAINMENT": "DSE: Entertainment",
    "DSE PERSONAL": "DSE: Personal",
    "DSE READING": "DSE: Reading",
    "DSE EDUCATION": "DSE: Education",
    "DSE TRAVEL": "DSE: Travel",
    "DSE DONATION": "DSE: Donation",
    "DSE FURNISHINGS": "DSE: Furnishings",
    "LIV IQ WNAS": "IQ: WealthIQ Net Assets Score",
    "ACT INT AMUSEMENT PARK VISITORS": "Act/Int: Amusement Park Visitors",
    "ACT INT ZOO VISITORS": "Act/Int: Zoo Visitors",
    "ACT INT COFFEE CONNOISSEURS": "Act/Int: Coffee Connoisseurs",
    "ACT INT DO-IT-YOURSELFERS": "Act/Int: Do-it-yourselfers",
    "ACT INT HOME IMPROVEMENT SPENDERS": "Act/Int: Home Improvement Spenders",
    "ACT INT HUNTING ENTHUSIASTS": "Act/Int: Hunting Enthusiasts",
    "BUYER LAPTOP OWNERS": "Buyer: Laptop Owners",
    "BUYER SECURITY SYSTEM OWNERS": "Buyer: Security System Owners",
    "BUYER TABLET OWNERS": "Buyer: Tablet Owners",
    "BUYER COUPON USERS": "Buyer: Coupon Users",
    "BUYER LUXURY STORE SHOPPERS": "Buyer: Luxury Store Shoppers",
    "BUYER YOUNG ADULT CLOTHING SHOPPERS": "Buyer: Young Adult Clothing Shoppers",
    "BUYER SUPERCENTER SHOPPERS": "Buyer: Supercenter Shoppers",
    "BUYER WAREHOUSE CLUB MEMBERS": "Buyer: Warehouse Club Members",
    "LIFESTYLE LIFE INSURANCE POLICY HOLDERS": "Lifestyle: Life Insurance Policy Holders",
    "ACT INT DIGITAL MAGAZINE NEWSPAPERS BUYERS": "Act/Int: Digital Magazine/Newspapers Buyers",
    "ACT INT ATTEND ORDER EDUCATIONAL PROGRAMS": "Act/Int: Attend/Order Educational Programs",
    "ACT INT VIDEO GAMER": "Act/Int: Video Gamer",
    "ACT INT MLB ENTHUSIAST": "Act/Int: MLB Enthusiast",
    "ACT INT NASCAR ENTHUSIAST": "Act/Int: NASCAR Enthusiast",
    "ACT INT NBA ENTHUSIAST": "Act/Int: NBA Enthusiast",
    "ACT INT NFL ENTHUSIAST": "Act/Int: NFL Enthusiast",
    "ACT INT NHL ENTHUSIAST": "Act/Int: NHL Enthusiast",
    "ACT INT PGA TOUR ENTHUSIAST": "Act/Int: PGA Tour Enthusiast",
    "ACT INT POLITICAL VIEWING ON TV-LIBERAL": "Act/Int: Political Viewing on TV - Liberal",
    "ACT INT POLITICAL VIEWING ON TV-LIBERAL COMEDY": "Act/Int: Political Viewing on TV - Liberal Comedy",
    "ACT INT POLITICAL VIEWING ON TV-CONSERVATIVE": "Act/Int: Political Viewing on TV - Conservative",
    "ACT INT EATS AT FAMILY RESTAURANTS": "Act/Int: Eats at Family Restaurants",
    "ACT INT EATS AT FAST FOOD RESTAURANTS": "Act/Int: Eats at Fast Food Restaurants",
    "ACT INT CANOEING KAYAKING": "Act/Int: Canoeing/Kayaking",
    "ACT INT PLAY GOLF": "Act/Int: Play Golf",
    "BUYER PRESENCE OF AUTOMOBILE": "Buyer: Presence of Automobile",
    "BUYER LOYALTY CARD USER": "Buyer: Loyalty Card User",
    "BUYER LUXURY HOME GOODS STORE SHOPPER": "Buyer: Luxury Home Goods Store Shopper",
    "MEMBERSHIPS UNION MEMBER": "Memberships: Union Member",
    "INVEST HAVE A RETIREMENT FINANCIAL PLAN": "Invest: Have a Retirement Financial Plan",
    "INVEST PARTICIPATE IN ONLINE TRADING": "Invest: Participate in Online Trading",
    "ACT INT GOURMET COOKING": "Act/Int: Gourmet Cooking",
    "ACT INT CAT OWNERS": "Act/Int: Cat Owners",
    "ACT INT DOG OWNERS": "Act/Int: Dog Owners",
    "ACT INT ARTS AND CRAFTS": "Act/Int: Arts and Crafts",
    "ACT INT SCRAPBOOKING": "Act/Int: Scrapbooking",
    "ACT INT CULTURAL ARTS": "Act/Int: Cultural Arts",
    "HOBBIES GARDENING": "Hobbies: Gardening",
    "ACT INT PHOTOGRAPHY": "Act/Int: Photography",
    "ACT INT BOOK READER": "Act/Int: Book Reader",
    "ACT INT E-BOOK READER": "Act/Int: E-Book Reader",
    "ACT INT AUDIO BOOK LISTENER": "Act/Int: Audio Book Listener",
    "ACT INT PET ENTHUSIAST": "Act/Int: Pet Enthusiast",
    "ACT INT MUSIC DOWNLOAD": "Act/Int: Music Download",
    "ACT INT MUSIC STREAMING": "Act/Int: Music Streaming",
    "ACT INT AVID RUNNERS": "Act/Int: Avid Runners",
    "ACT INT OUTDOOR ENTHUSIAST": "Act/Int: Outdoor Enthusiast",
    "ACT INT FISHING": "Act/Int: Fishing",
    "ACT INT SNOW SPORTS": "Act/Int: Snow Sports",
    "ACT INT BOATING": "Act/Int: Boating",
    "ACT INT PLAYS HOCKEY": "Act/Int: Plays Hockey",
    "ACT INT PLAYS SOCCER": "Act/Int: Plays Soccer",
    "ACT INT PLAYS TENNIS": "Act/Int: Plays Tennis",
    "ACT INT SPORTS ENTHUSIAST": "Act/Int: Sports Enthusiast",
    "ACT INT HEALTHY LIVING": "Act/Int: Healthy Living",
    "ACT INT FITNESS ENTHUSIAST": "Act/Int: Fitness Enthusiast",
    "ACT INT ON A DIET": "Act/Int: On a Diet",
    "ACT INT WEIGHT CONSCIOUS": "Act/Int: Weight Conscious",
    "LIFESTYLE HIGH FREQUENCY CRUISE ENTHUSIAST": "Lifestyle: High Frequency Cruise Enthusiast",
    "LIFESTYLE HIGH FREQUENCY DOMESTIC VACATIONER": "Lifestyle: High Frequency Domestic Vacationer",
    "LIFESTYLE HIGH FREQUENCY FOREIGN VACATIONER": "Lifestyle: High Frequency Foreign Vacationer",
    "LIFESTYLE FREQUENT FLYER PROGRAM MEMBER": "Lifestyle: Frequent Flyer Program Member",
    "LIFESTYLE HOTEL GUEST LOYALTY PROGRAM": "Lifestyle: Hotel Guest Loyalty Program",
    "DONOR CONTRIBUTES BY VOLUNTEERING": "Donor: Contributes by Volunteering",
    "FINANCIAL DEBIT CARD USER": "Financial: Debit Card User",
    "FINANCIAL MAJOR CREDIT CARD USER": "Financial: Major Credit Card User",
    "FINANCIAL PREMIUM CREDIT CARD USER": "Financial: Premium Credit Card User",
    "FINANCIAL CREDIT CARD USER": "Financial: Credit Card User",
    "FINANCIAL STORE CREDIT CARD USER": "Financial: Store Credit Card User",
    "INVEST BROKERAGE ACCOUNT OWNER": "Invest: Brokerage Account Owner",
    "INVEST ACTIVE INVESTOR": "Invest: Active Investor",
    "INVEST MUTUAL FUND INVESTOR": "Invest: Mutual Fund Investor",
    "TECH USAGE SKILL LEVEL": "Person #: Technology Adoption",
    "ACT INT LISTENS TO CHRISTIAN MUSIC": "Act/Int: Listens to Christian Music",
    "ACT INT LISTENS TO CLASSICAL MUSIC": "Act/Int: Listens to Classical Music",
    "ACT INT LISTENS TO COUNTRY MUSIC": "Act/Int: Listens to Country Music",
    "ACT INT LISTENS TO MUSIC": "Act/Int: Listens to Music",
    "ACT INT LISTENS TO OLDIES MUSIC": "Act/Int: Listens to Oldies Music",
    "ACT INT LISTENS TO ROCK MUSIC": "Act/Int: Listens to Rock Music",
    "ACT INT LISTENS TO 80S MUSIC": "Act/Int: Listens to 80's Music",
    "ACT INT LISTENS TO HIP HOP MUSIC": "Act/Int: Listens to Hip Hop Music",
    "ACT INT LISTENS TO ALTERNATIVE MUSIC": "Act/Int: Listens to Alternative Music",
    "ACT INT LISTENS TO JAZZ MUSIC": "Act/Int: Listens to Jazz Music",
    "ACT INT LISTENS TO POP MUSIC": "Act/Int: Listens to Pop Music",
    "LIFESTYLE MILITARY ACTIVE": "Lifestyle: Military - Active",
    "LIFESTYLE MILITARY INACTIVE": "Lifestyle: Military - Inactive",
    "PERS EMAIL ENGAGEMENT": "Person 1: TrueTouch Email Engagement",
    "HH PREFER EMAIL AD": "TrueTouch: Email Engagement",
    "PERS TT SAVVY RESEARCHERS": "Person 1: TrueTouch: Savvy Researchers",
    "PERS TT ORGANIC NATURAL": "Person 1: TrueTouch: Organic and natural",
    "PERS TT BRAND LOYALISTS": "Person 1: TrueTouch: Brand Loyalists",
    "PERS TT TRENDSETTERS": "Person 1: TrueTouch: Trendsetters",
    "PERS TT DEAL SEEKERS": "Person 1: TrueTouch: Deal Seekers",
    "PERS TT RECREATIONAL SHOPPERS": "Person 1: TrueTouch: Recreational Shoppers",
    "PERS TT QUALITY MATTERS": "Person 1: TrueTouch: Quality Matters",
    "PERS TT IN THE MOMENT SHOPPERS": "Person 1: TrueTouch: In the Moment Shoppers",
    "PERS TT MAINSTREAM ADOPTERS": "Person 1: TrueTouch: Mainstream Adopters",
    "PERS TT NOVELTY SEEKERS": "Person 1: TrueTouch: Novelty Seekers",
    "TT SAVVY RESEARCHERS": "True Touch: Savvy researchers",
    "TT ORGANIC NATURAL": "TrueTouch: Organic and natural",
    "TT BRAND LOYALISTS": "TrueTouch: Brand loyalists",
    "TT TRENDSETTERS": "TrueTouch: Trendsetters",
    "TT DEAL SEEKERS": "TrueTouch: Deal seekers",
    "TT RECREATIONAL SHOPPERS": "TrueTouch: Recreational shoppers",
    "TT QUALITY MATTERS": "TrueTouch: Quality matters",
    "TT IN THE MOMENT SHOPPERS": "TrueTouch: In the moment shoppers",
    "TT MAINSTREAM ADOPTERS": "TrueTouch: Mainstream adopters",
    "TT NOVELTY SEEKERS": "TrueTouch: Novelty seekers",
    "ZIP4 MDN HHINC": "Median: Est HH Income Range V6",
    "PERS TT ENG BROADCAST CABLE TV": "Person 1: TrueTouch Eng: Broadcast Cable TV",
    "PERS TT ENG DIGITAL DISPLAY": "Person 1: TrueTouch Eng: Digital Display",
    "PERS TT ENG DIRECT MAIL": "Person 1: TrueTouch Eng: Direct Mail",
    "PERS TT ENG DIGITAL NEWSPAPER": "Person 1: TrueTouch Eng: Digital Newspaper",
    "PERS TT ENG DIGITAL VIDEO": "Person 1: TrueTouch Eng: Digital Video",
    "PERS TT ENG RADIO": "Person 1: TrueTouch Eng: Radio",
    "PERS TT ENG STREAMING TV": "Person 1: TrueTouch Eng: Streaming TV",
    "PERS TT ENG TRADITIONAL NEWSPAPER": "Person 1: TrueTouch Eng: Traditional Newspaper",
    "PERS TT ENG MOBILE SMS MMS": "Person 1: TrueTouch Eng: Mobile SMS MMS",
    "PERS TT CONV ONLINE DEAL VOUCHER": "Person 1: TT Conv: Online Deal Voucher",
    "PERS TT CONV DISCOUNT SUPERCENTERS": "Person 1: TT Conv: Discount Supercenters",
    "PERS TT CONV EBID SITES": "Person 1: TT Conv: Ebid Sites",
    "PERS TT CONV ETAIL ONLY": "Person 1: TT Conv Conv: Etail only",
    "PERS TT CONV MID HIGH END STORE": "Person 1: TT Conv: Mid-High End Store",
    "PERS TT CONV SPECIALTY DEPT STORE": "Person 1: TT Conv Conv: Specialty Dept Store",
    "PERS TT CONV WHOLESALE": "Person 1: TT Conv Conv: Wholesale",
    "PERS TT CONV SPECIALTY BOUTIQUE": "Person 1: TT Conv Conv: Specialty or Boutique",
    "PSCS AUA0300 AVG": "Average number of auto loan and lease trades",
    "AVG AUTO LOAN TRD": "Average number of auto loan trades",
    "AVG EXT COLLECTION TRD": "Average number of external collection trades",
    "AVG INSTLMT TRD": "Average number of installment trades",
    "AVG MTHLY PYMT OPN 1ST MRGG TRD LS 6 MTH": "Average monthly payment on open first mortgage trades reported in the last 6 months",
    "AVG 2ND MRGG TRD": "Average number of second mortgage trades",
    "AVG MTHLY PYMT OPN 2ND MRGG TRD LS 6 MTH": "Average monthly payment on open second mortgage trades reported in the last 6 months",
    "AVG RVLV TRD": "Average number of revolving trades",
    "PSCS VANTAGE AVG": "Overall Financial Health Score",
    "HIGH VS LOW AFFLUENCE SCORE": "Affluence Score",
    
    # Person 1 TrueTouch Behavioral Fields
    "HH:P1:TrueTouch:DealSeekers": "Person 1: TrueTouch: Deal Seekers",
    "HH:P1:TrueTouch:InTheMomentShoppers": "Person 1: TrueTouch: In The Moment Shoppers",
    "HH:P1:TrueTouch:MainstreamAdopters": "Person 1: TrueTouch: Mainstream Adopters",
    "HH:P1:TrueTouch:NoveltySeekers": "Person 1: TrueTouch: Novelty Seekers",
    "HH:P1:TrueTouch:QualityMatters": "Person 1: TrueTouch: Quality Matters",
    "HH:P1:TrueTouch:RecreationalShoppers": "Person 1: TrueTouch: Recreational Shoppers",
    "HH:TrueTouch:OrganicAndNatural": "TrueTouch: Organic And Natural",
    "HH:TrueTouch:SavvyResearchers": "TrueTouch: Savvy Researchers",
    "HH:TrueTouch:BrandLoyalists": "TrueTouch: Brand Loyalists",
    "HH:TrueTouch:DealSeekers": "TrueTouch: Deal Seekers",
    "HH:TrueTouch:RecreationalShoppers": "TrueTouch: Recreational Shoppers",
    "HH:TrueTouch:Trendsetters": "TrueTouch: Trendsetters",
    
    # Dwelling Information
    "HH:DwellingSizeInLivableUnits": "Dwelling Size in Livable Units",
    
    # New Homeowner and Mover Indicators
    "HH:NewHomeownerIndicator6M": "New Homeowner Indicator 6M",
    "HH:NewMoverIndicatorLast6Months": "New Mover: Indicator Last 6 Months",
    
    # Business Owner Indicator
    "HH:PersonBusinessOwner": "Person #: Business Owner",
    
    # Birth Date Information
    "HH:PersonBirthYearAndMonth": "Person #: Birth Year And Month",
    
    # Ethnic Information
    "HH:PersonEthnic": "Person #: Ethnic",
}




def normalize_field_key(field_key: str) -> str:
    """
    Normalize field key by removing spaces, underscores and converting to uppercase
    for consistent matching regardless of format variations
    """
    return field_key.replace(" ", "").replace("_", "").upper()

def find_suffix_mapping(suffix: str) -> str:
    """
    Find mapping for suffix, handling different format variations
    (spaces, underscores, or jammed together)
    """
    # Normalize the input suffix for comparison
    normalized_suffix = normalize_field_key(suffix)
    
    # Check each mapping key for a match
    for mapping_key, display_name in SUFFIX_MAPPINGS.items():
        normalized_mapping_key = normalize_field_key(mapping_key)
        if normalized_suffix == normalized_mapping_key:
            return display_name
    
    return None  # No mapping found

def clean_field_name(field_name: str) -> str:
    """
    Clean field name by mapping suffix or formatting it
    
    Args:
        field_name: Raw field name from API
        
    Returns:
        Cleaned, user-friendly field name
    """
    # Extract the last part after the final dot
    suffix = field_name.split(".")[-1]
    
    # First try to find a mapping using flexible matching
    mapped_name = find_suffix_mapping(suffix)
    if mapped_name:
        return mapped_name
    
    # If no mapping found, clean up the suffix automatically
    cleaned = suffix.replace("_", " ").title()
    return cleaned

def map_field_names(data: Any, parent_key: str = "") -> Any:
    """
    Recursively map Experian field names to user-friendly names
    
    Args:
        data: The data structure to transform
        parent_key: The parent key path for building full field paths
        
    Returns:
        Transformed data with user-friendly field names
    """
    if isinstance(data, dict):
        mapped = {}
        for key, value in data.items():
            # Always clean the field name by extracting suffix
            display_name = clean_field_name(key)
            
            # Recursively process nested objects
            mapped_value = map_field_names(value, f"{parent_key}.{key}" if parent_key else key)
            mapped[display_name] = mapped_value
            
        return mapped
    
    elif isinstance(data, list):
        return [map_field_names(item, parent_key) for item in data]
    
    else:
        return data

def filter_hidden_fields(data: Any) -> Any:
    """
    Remove fields that should be hidden from the results
    
    Args:
        data: The data structure to filter
        
    Returns:
        Filtered data with hidden fields removed
    """
    if isinstance(data, dict):
        filtered = {}
        for key, value in data.items():
            # Skip hidden fields
            if key not in HIDDEN_FIELDS:
                # Recursively filter nested objects
                filtered_value = filter_hidden_fields(value)
                filtered[key] = filtered_value
        return filtered
    
    elif isinstance(data, list):
        return [filter_hidden_fields(item) for item in data]
    
    else:
        return data

def sort_fields_by_priority(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sort dictionary fields by priority configuration
    
    Args:
        data: Dictionary with fields to sort
        
    Returns:
        OrderedDict with fields sorted by priority
    """
    if not isinstance(data, dict):
        return data
    
    def get_priority(field_name: str) -> int:
        # Return configured priority, or 1000 for unspecified fields (medium priority)
        return FIELD_PRIORITIES.get(field_name, 1000)
    
    # Sort fields by priority first, then alphabetically only for non-priority fields
    def sort_key(item):
        field_name, _ = item
        priority = get_priority(field_name)
        if priority < 1000:  # Has explicit priority
            return (priority, "")  # Empty string so priority fields don't get secondary alphabetical sort
        else:  # No explicit priority (medium priority)
            return (priority, field_name.lower())  # Alphabetical among medium priority fields
    
    sorted_items = sorted(data.items(), key=sort_key)
    
    # Recursively sort nested dictionaries using OrderedDict for guaranteed order
    sorted_dict = OrderedDict()
    for key, value in sorted_items:
        if isinstance(value, dict):
            sorted_dict[key] = sort_fields_by_priority(value)
        elif isinstance(value, list):
            sorted_dict[key] = [
                sort_fields_by_priority(item) if isinstance(item, dict) else item 
                for item in value
            ]
        else:
            sorted_dict[key] = value
    
    return sorted_dict

def flatten_for_final_sort(data: Any, result: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Completely flatten nested structure to prepare for final sorting
    
    Args:
        data: Nested data structure
        result: Accumulator for flattened results
        
    Returns:
        Completely flattened dictionary
    """
    if result is None:
        result = OrderedDict()
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively flatten nested objects
                flatten_for_final_sort(value, result)
            elif isinstance(value, list):
                # Handle lists - if they contain dicts, flatten them too
                for item in value:
                    if isinstance(item, dict):
                        flatten_for_final_sort(item, result)
                    # Skip primitive values in lists for now
            else:
                # Add leaf values to result
                result[key] = value
    
    return result

def transform_experian_response(data: Any) -> Any:
    """
    Complete transformation: field names + value mappings + filtering + flattening + final sorting
    
    Args:
        data: Raw Experian API response data
        
    Returns:
        Fully transformed, flattened, and sorted data
    """
    # Step 1: Transform field names to user-friendly labels
    mapped_fields = map_field_names(data)
    
    # Step 2: Transform field values using value mappings
    transformed_data = transform_response_data(mapped_fields)
    
    # Step 3: Filter out hidden fields
    filtered_data = filter_hidden_fields(transformed_data)
    
    # Step 4: Completely flatten the nested structure
    flattened_data = flatten_for_final_sort(filtered_data)
    
    # Step 5: Apply final sort to the flattened data
    final_sorted_data = sort_fields_by_priority(flattened_data)
    
    return final_sorted_data

def add_field_priority(field_name: str, priority: int) -> None:
    """
    Add or update field priority
    
    Args:
        field_name: Name of the field
        priority: Priority number (lower = shows first)
    """
    FIELD_PRIORITIES[field_name] = priority

def hide_field(field_name: str) -> None:
    """
    Add a field to the hidden fields list
    
    Args:
        field_name: Name of the field to hide
    """
    if field_name not in HIDDEN_FIELDS:
        HIDDEN_FIELDS.append(field_name)

def show_field(field_name: str) -> None:
    """
    Remove a field from the hidden fields list
    
    Args:
        field_name: Name of the field to show
    """
    if field_name in HIDDEN_FIELDS:
        HIDDEN_FIELDS.remove(field_name)

def get_field_priorities() -> Dict[str, int]:
    """Get current field priority configuration"""
    return FIELD_PRIORITIES.copy()

def get_hidden_fields() -> List[str]:
    """Get current list of hidden fields"""
    return HIDDEN_FIELDS.copy()
