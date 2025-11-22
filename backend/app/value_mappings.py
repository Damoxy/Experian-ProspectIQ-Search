"""
Value mappings for Experian API response codes to human-readable descriptions
"""

from typing import Dict, Any, Optional

# Value mappings for converting API response codes to readable descriptions
VALUE_MAPPINGS: Dict[str, Dict[str, str]] = {
    # Education Level mappings
    "EDUCATION_LEVEL": {
        "00": "Unknown",
        "11": "HS Diploma - Extremely Likely",
        "12": "Some College - Extremely Likely",
        "13": "Bach Degree - Extremely Likely",
        "14": "Grad Degree - Extremely Likely",
        "15": "Less than HS Diploma - Extremely Likely",
        "51": "HS Diploma - Likely",
        "52": "Some College - Likely",
        "53": "Bach Degree - Likely",
        "54": "Grad Degree - Likely",
        "55": "Less than HS Diploma - Likely",
        "": "Null",
        " ": "Null"
    },
    
    # Marital Status mappings
    "MARITAL_STATUS": {
        "0U": "Unknown Not scored",
        "1M": "Married Extremely Likely",
        "5M": "Married Likely",
        "5S": "Single Likely never married",
        "5U": "Unknown Scored",
        "": "Null",
        " ": "Null"
    },
    
    # Add more field mappings here as needed
    # Template for new mappings:
    # "FIELD_NAME": {
    #     "code1": "Description 1",
    #     "code2": "Description 2",
    #     "": "Null",
    #     " ": "Null"
    # },
        "number_of_children_in_household": {
            "0": "0 Children",
            "1": "1 Child",
            "2": "2 Children",
            "3": "3 Children",
            "4": "4 Children",
            "5": "5 Children",
            "6": "6 Children",
            "7": "7 Children",
            "8": "8 Children",
            "": "Blank",
        },
        "HOMEOWNER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "RENTER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "MAIL_RESPONDER": {
            "M": "Multi-buyer",
            "U": "Unknown",
            "Y": "Single buyer",
        },
        "ADDRESS_QUALITY_INDICATOR": {
            "E": "Excellent",
            "G": "Good",
            "M": "Marginal",
            "N": "Phone only",
            "S": "Satisfactory",
        },
        "PROPERTY_TYPE": {
            "0": "Unknown",
            "1": "Residential",
            "2": "Condominium",
            "3": "Duplex",
            "4": "Apartment",
            "5": "Commercial Condo",
            "6": "Agricultural",
            "7": "Mobile Home",
        },
        "HOME_NUMBER_OF_BEDROOMS": {
            "00": "0 bedrooms",
            "01": "1 bedroom",
            "02": "2 bedrooms",
            "03": "3 bedrooms",
            "04": "4 bedrooms",
            "05": "5 bedrooms",
            "06": "6 bedrooms",
            "07": "7 bedrooms",
            "08": "8 bedrooms",
            "09": "9 bedrooms",
            "10": "10 bedrooms",
            "11": "11 bedrooms",
            "12": "12 bedrooms",
            "13": "13 bedrooms",
            "14": "14 bedrooms",
            "15": "15 bedrooms",
            "16": "16 bedrooms",
        },
        "HOME_SWIMMING_POOL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "PRESENCE_OF_CHILD": {
            "00": "Deceased and Child only households",
            "1Y": "Known Data",
            "5N": "Not Likely to have a child",
            "5U": "Modeled Not as Likely to have a child",
            "5Y": "Modeled Likely to have a child",
        },
        "GREEN_AWARE_HOUSEHOLD": {
            "0": "Unknown",
            "1": "Behavioral Greens",
            "2": "Think Greens",
            "3": "Potential Greens",
            "4": "True Browns",
        },
        "HOUSEHOLD_COMPOSITION": {
            "A": "HH w/1 adult F (no adult M - no child)",
            "B": "HH w/1 adult M (no adult F - no child)",
            "C": "HH w/1 adult F and 1 adult M (no child)",
            "D": "HH w/1 adult F + 1 adult M and child present",
            "E": "HH w/1 adult F and child present (no adult M)",
            "F": "HH w/1 adult M and child present (no adult F)",
            "G": "HH w/2 + adult M (no child - may have adult F)",
            "H": "HH w/2 + adult F (no child - may have adult M)",
            "I": "HH w/2 + adult M w/ child present (adult F pos)",
            "J": "HH w/2 + adult F w/ child present (adult M pos)",
            "U": "Unable to code",
        },
        "DWELLING_SIZE_IN_LIVABLE_UNITS": {
            "A": "SFDU",
            "B": "Duplex",
            "C": "Triplex",
            "D": "4",
            "E": "5-9",
            "F": "10-19",
            "G": "20-49",
            "H": "50-100",
            "I": "101+",
        },
        "NUMBER_OF_CHILDREN_IN_HOME": {
            "0": "0 Children",
            "1": "1 Children",
            "2": "2 Children",
            "3": "3 Children",
            "4": "4 Children",
            "5": "5 Children",
            "6": "6 Children",
            "7": "7 Children",
            "8": "8 Children",
            "blank": "Blank",
        },
        "NUMBER_OF_ADULTS_IN_HOME": {
            "0": "0 Adults",
            "1": "1 Adults",
            "2": "2 Adults",
            "3": "3 Adults",
            "4": "4 Adults",
            "5": "5 Adults",
            "6": "6 Adults",
            "7": "7 Adults",
            "8": "8 Adults",
            "blank": "Blank",
        },
            "HH_ACTY_INT_COLLECTING_OTHER_COLLECTIBLES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COLLECTING_ART_ANTIQUES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COLLECTING_STAMPS_COINS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COLLECTING_DOLLS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COLLECTING_FIGURINES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COLLECTING_SPORTS_MEMORABILIA": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COOKING_ENTERTAINING_COOKING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COOKING_ENTERTAINING_BAKING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COOKING_ENTERTAINING_COOK_WEIGHT_CON": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COOKING_ENTERTAINING_WINE_APPRECIATION": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_COOKING_ENTERTAINING_COOKING_GOURMET": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_CRAFTS_CRAFTS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_CRAFTS_KNITTING_NEEDLEWORK": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_CRAFTS_QUILTING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_CRAFTS_SEWING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_CRAFTS_WOODWORKING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HEALTH_FITNESS_LOSING_WEIGHT": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "SRVY_HH_ACTY_INT_HEALTH_FITNESS_VIT_SUPPLEMENTS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HEALTH_FITNESS_HLTH_NAT_FOODS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HOBBIES_PHOTOGRAPHY_HOBBIES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HOBBIES_GARDENING_HOBBIES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HOBBIES_CARS_AUTO_REPAIR": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_HOBBIES_SELF_IMPROVEMENT": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_CHRISTIAN_GOSPEL": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_R_AND_B": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_JAZZ_NEW_AGE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_CLASSICAL": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_ROCK_N_ROLL": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_COUNTRY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_MUSIC_IN_GENERAL": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_MUSIC_OTHER_MUSIC": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_BEST_SELLING_FICTION": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_CHILDRENS_READING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_BOOK_READER": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_ANIMAL_WF_SOC_CAUS_CON": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_ENVIRONMENT_WILDLIFE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_CONSERVATIVE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_LIBERAL": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_CHILDREN": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_VETERANS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_HLTY_SOC_CAUSE_CON": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_SOCL_CAUS_CON_OTHR_SOC_CAUSE_CON": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_COOKING_CULINARY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_COUNTRY_LIFESTYLE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_ENTERTAINMENT_PEOPLE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_FASHION": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_HISTORY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_INTERIOR_DECORATING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_MEDICAL_HEALTH": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_MILITARY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_MYSTERY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_NATURAL_HEALTH_REMEDIES": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_ROMANCE": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_SCIENCE_FICTION": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_SCIENCE_TECHNOLOGY": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_SPORTS_READING": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_WORLD_NEWS_POLITICS": {
                "U": "Unknown",
                "Y": "Yes",
            },
            "HH_ACTY_INT_READING_BOOK_READER": {
                "U": "Unknown",
                "Y": "Yes",
            },
                "CHILDREN_BY_AGE_GENDER": {
                    "B": "Both",
                    "Blank": "Blank",
                    "F": "Female",
                    "M": "Male",
                    "U": "Unknown",
                },
                "PROPERTY_REALTY_BUILDING_SQ_FOOTAGE_RANGES": {
                    "A": "100-999",
                    "B": "1000-2999",
                    "C": "3000-4999",
                    "D": "5000-5999",
                    "E": "6000-9999",
                    "F": "10000+",
                    "U": "Unknown",
                },
                "MORTGAGE_HOME_PURCHASE_PURCHASE_AMOUNT_RANGES": {
                    "A": "$1,000-$9,999",
                    "B": "$10,000-$24,999",
                    "C": "$25,000-$39,999",
                    "D": "$40,000-$59,999",
                    "E": "$60,000-$79,999",
                    "F": "$80,000-$99,999",
                    "G": "$100,000-$119,999",
                    "H": "$120,000-$139,999",
                    "I": "$140,000-$159,999",
                    "J": "$160,000-$199,999",
                    "K": "$200,000-$249,999",
                    "L": "$250,000-$349,999",
                    "M": "$350,000-$449,999",
                    "N": "$450,000-$749,999",
                    "O": "$750,000-$999,999",
                    "P": "$1MM+",
                    "U": "Unknown",
                },
                "MORTGAGE_HOME_PURCHASE_MORTGAGE_AMOUNT_RANGES": {
                    "A": "$1,000-$9,999",
                    "B": "$10,000-$24,999",
                    "C": "$25,000-$39,999",
                    "D": "$40,000-$59,999",
                    "E": "$60,000-$79,999",
                    "F": "$80,000-$99,999",
                    "G": "$100,000-$119,999",
                    "H": "$120,000-$139,999",
                    "I": "$140,000-$159,999",
                    "J": "$160,000-$199,999",
                    "K": "$200,000-$249,999",
                    "L": "$250,000-$349,999",
                    "M": "$350,000-$449,999",
                    "N": "$450,000-$749,999",
                    "O": "$750,000-$999,999",
                    "P": "$1MM+",
                    "U": "Unknown",
                },
        # Additional Reading Fields
        "HH_ACTY_INT_READING_INTERIOR_DECORATING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_MEDICAL_HEALTH": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_MILITARY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_MYSTERY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_NATURAL_HEALTH_REMEDIES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_ROMANCE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_SCIENCE_FICTION": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_SCIENCE_TECHNOLOGY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_SPORTS_READING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_WORLD_NEWS_POLITICS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_READING_BOOK_READER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Social Causes and Concerns
        "HH_ACTY_INT_SOCL_CAUS_CON_ANIMAL_WF_SOC_CAUS_CON": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_ENVIRONMENT_WILDLIFE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_CONSERVATIVE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_LIBERAL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_CHILDREN": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_VETERANS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_HLTY_SOC_CAUSE_CON": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SOCL_CAUS_CON_OTHR_SOC_CAUSE_CON": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Sports and Recreation
        "HH_ACTY_INT_SPORTS_REC_BASEBALL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_BASKETBALL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_HOCKEY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_CAMPING_HIKING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_HUNTING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_FISHING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_NASCAR": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_PERSONAL_FITNESS_EXERCISE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_SCUBA_DIVING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_FOOTBALL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_GOLF": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_SNOW_SKIING_BOARDING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_BOATING_SAILING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_WALKING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_CYCLING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_MOTORCYCLES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_RUNNING_JOGGING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_SOCCER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_SWIMMING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SPORTS_REC_PLAY_SPORTS_IN_GENERAL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Travel and Sweepstakes
        "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_DOMESTIC_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_FOREIGN_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_SWEEPSTAKES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_CASINO_GAMBLING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # TrueTouch Behavioral Scores
        "TRUETOUCH_EMAIL_ENGAGEMENT": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_SAVVY_RESEARCHERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_ORGANIC_AND_NATURAL": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_BRAND_LOYALISTS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_TRENDSETTERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        
        # Income and Financial
        "MEDIAN_EST_HH_INCOME_RANGE_V6": {
            "A": "$1,000-$14,999",
            "B": "$15,000-$24,999",
            "C": "$25,000-$34,999",
            "D": "$35,000-$49,999",
            "E": "$50,000-$74,999",
            "F": "$75,000-$99,999",
            "G": "$100,000-$124,999",
            "H": "$125,000-$149,999",
            "I": "$150,000-$174,999",
            "J": "$175,000-$199,999",
            "K": "$200,000-$249,999",
            "L": "$250,000+",
            "U": "Unknown",
            "Blank": "Unknown",
        },
        
        # Electronics and Technology
        "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_COMPUTERS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_VIDEO_GAMES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_ELECTRONICS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_HOME_TECH": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Cultural Arts and Electronics/Gadgets
        "HH_ACTY_INT_CLTRL_ARTS_INTEREST_IN_CULTURAL_ARTS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_COMPACT_DISC_PLAYER": {
            "U": "Unknown", 
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_CELL_PHONE": {
            "U": "Unknown",
            "Y": "Yes", 
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_DIGITAL_CAMERA": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_DVD_PLAYER": {
            "U": "Unknown", 
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_HDTV": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_INTEREST_IN_ELECTRONICS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_PDA_BLACKBERRY": {
            "U": "Unknown",
            "Y": "Yes", 
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_SATELLITE_DISH": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_VIDEO_CAMERA": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_ELCTRNCS_GDGTS_VIDEO_GAME_SYSTEM": {
            "U": "Unknown", 
            "Y": "Yes",
        },
        
        # Magazine Interest Fields
        "HH_ACTY_INT_MAGAZINES_BUSINESS_AND_FINANCE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_CHILDRENS_MAGAZINES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_COMPUTER_ELECTRONICS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_CRAFTS_GAMES_AND_HOBBIES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_CURRENT_EVENTS_NEWS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_FITNESS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_FOOD_WINE_COOKING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_GARDENING_MAGAZINES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_HUNTING_AND_FISHING": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_MENS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_MUSIC": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_SPORTS_MAGAZINES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_SUBSCRIPTION": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_MAGAZINES_WOMENS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # PC & Internet Fields
        "HH_ACTY_INT_PC_INTERNET_OWN_COMPUTER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_PC_INTERNET_PLAN_TO_BUY_COMPUTER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_PC_INTERNET_USE_INTERNET_SERVICE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_PC_INTERNET_USEDSL_HISPD": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Reading Fields
        "HH_ACTY_INT_READING_COMPUTER": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Sweepstakes Fields
        "HH_ACTY_INT_SWEEPSTAKES_LOTTERIES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_SWEEPSTAKES_SWEEPSTAKES": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Travel Fields
        "HH_ACTY_INT_TRAVEL_BUSINESS_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_CRUISE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_DOMESTIC": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_INTERNATIONAL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_PERSONAL_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_RECREATIONAL_VEHICLE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_TIME_SHARE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_ACTY_INT_TRAVEL_WOULD_ENJOY_RV_TRAVEL": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Lifestyle Fields
        "HH_LIFESTYL_AFFILIATION_MEMBER_MUSIC_CLUB": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_BUYING_INTEREST_COMP_ELEC": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_BUYING_INTEREST_SPORTS_RELATED": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_ENTERTAINMENT_BUY_PRE_RECORDED_VIDEOS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_ENTERTAINMENT_WATCH_CABLE_TV": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_ENTERTAINMENT_WATCH_VIDEOS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_FINANCIAL_IRAS_FUTURE_INTEREST": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_GRANDKIDS_PROUD_GRANDPARENT": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_PETS_OWN_A_CAT": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_PETS_OWN_A_DOG": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "HH_LIFESTYL_PETS_OWN_A_PET": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Lifestyle Categories
        "LIFESTYLE_INTERESTS_GAMBLING_PROPENSITY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "LIFESTYLE_INTERESTS_INVESTMENT_PROPENSITY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "LIFESTYLE_INTERESTS_INSURANCE_PROPENSITY": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Magazine Interests
        "MAGAZINE_INTERESTS_NEWS_POLITICS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "MAGAZINE_INTERESTS_AUTOMOTIVE": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "MAGAZINE_INTERESTS_SPORTS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "MAGAZINE_INTERESTS_HEALTH_FITNESS": {
            "U": "Unknown",
            "Y": "Yes",
        },
        "MAGAZINE_INTERESTS_HOME_GARDEN": {
            "U": "Unknown",
            "Y": "Yes",
        },
        
        # Ethnicity Demographics  
        "ETHNICITY_DETAIL_HISPANIC_COUNTRY_CODE": {
            "1": "Mexican",
            "2": "Puerto Rican", 
            "3": "Cuban",
            "4": "Dominican",
            "5": "Central American",
            "6": "South American",
            "7": "Other Hispanic",
            "U": "Unknown",
            "Blank": "Unknown",
        },
        "ETHNICITY_DETAIL_AFRICAN_COUNTRY_CODE": {
            "1": "Ethiopian",
            "2": "Nigerian",
            "3": "Kenyan",
            "4": "Ghanaian",
            "5": "South African",
            "6": "Other African",
            "U": "Unknown",
            "Blank": "Unknown",
        },
        "ETHNICITY_DETAIL_ASIAN_COUNTRY_CODE": {
            "1": "Chinese",
            "2": "Asian Indian",
            "3": "Filipino",
            "4": "Vietnamese",
            "5": "Korean",
            "6": "Japanese",
            "7": "Other Asian",
            "U": "Unknown",
            "Blank": "Unknown",
        },
        
        # Additional TrueTouch Behavioral Scores
        "TRUETOUCH_QUALITY_MATTERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_IN_THE_MOMENT_SHOPPERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_MAINSTREAM_ADOPTERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_NOVELTY_SEEKERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        
        # TrueTouch Engagement Channels
        "TRUETOUCH_ENG_BROADCAST_CABLE_TV": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_DIGITAL_DISPLAY": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_DIRECT_MAIL": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_DIGITAL_NEWSPAPER": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_DIGITAL_VIDEO": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_RADIO": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_STREAMING_TV": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_TRADITIONAL_NEWSPAPER": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        "TRUETOUCH_ENG_MOBILE_SMS_MMS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
            "Blank": "Not Scored",
        },
        
        # TrueTouch Conversion Channels
        "TRUETOUCH_CONV_ONLINE_DEAL_VOUCHER": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_DISCOUNT_SUPERCENTERS": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_EBID_SITES": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_ETAIL_ONLY": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_MID_HIGH_END_STORE": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_SPECIALTY_DEPT_STORE": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_WHOLESALE": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        "TRUETOUCH_CONV_SPECIALTY_OR_BOUTIQUE": {
            "0": "Unknown",
            "1": "Extremely Likely",
            "2": "Highly Likely",
            "3": "Very Likely",
            "4": "Somewhat Likely",
            "5": "Likely",
            "6": "Somewhat Unlikely",
            "7": "Very Unlikely",
            "8": "Highly Unlikely",
            "9": "Extremely Unlikely",
        },
        
        # Financial and Credit Scores
        "OVERALL_FINANCIAL_HEALTH_SCORE": {
            "300-499": "Deep Subprime",
            "500-600": "Subprime", 
            "601-660": "Nonprime",
            "661-780": "Prime",
            "781-850": "Super Prime",
        },
        "AFFLUENCE_SCORE": {
            # Range 1-99999, higher = more affluent
        },
        
        # Home Value and Real Estate Fields
        "ESTIMATED_CURRENT_HOME_VALUE": {
            # Dollar values - actual dollar amounts
        },
        "HOME_PURCHASE_PRICE": {
            # Dollar values in thousands (0001-9999), 0000=Unknown
        },
        "HOME_ORIGINAL_LOAN_TO_VALUE": {
            # Percentage values 01-99, 00=Unknown
            "00": "Unknown",
        },
        "REAL_ESTATE_AVAILABLE_EQUITY_AMOUNT": {
            # Dollar values - equity in thousands with confidence flag
            # Position 1 = confidence (1=Extremely Likely, 2=Highly Likely, 3=Likely)
            # Positions 2-5 = Equity amount in thousands (0000-9999)
        },
        "REAL_ESTATE_ESTIMATED_CURRENT_MORTGAGE_AMOUNT": {
            # Dollar values - mortgage amount in thousands
        },
        
        # Additional Home Value and Financial Fields (values in thousands)
        "HOME_TOTAL_VALUE": {
            # Dollar values in thousands - add "K" suffix
        },
        "REAL_ESTATE_TAX": {
            # Dollar values in thousands - add "K" suffix
        },
        "HOME_LAND_VALUE": {
            # Dollar values in thousands - add "K" suffix
        },
        "HOME_PURCHASE_MORTGAGE_AMOUNT": {
            # Dollar values in thousands - add "K" suffix
        },
        "INVESTMENT_PROPERTY_PURCHASE_AMOUNT": {
            # Dollar values in thousands - add "K" suffix
        },
        
    # DSE (Direct Spend Estimate) fields - Dollar amounts from 00010 to 99000
    "DSE_DINE_OUT": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_ALCOHOL_WINE": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_APPAREL": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_ENTERTAINMENT": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_PERSONAL": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_READING": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_EDUCATION": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_TRAVEL": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_DONATION": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    "DSE_FURNISHINGS": {
        "00000": "$0",
        "00010": "$10",
        "00020": "$20",
        "00050": "$50",
        "00100": "$100",
        "00250": "$250",
        "00500": "$500",
        "01000": "$1,000",
        "02500": "$2,500",
        "05000": "$5,000",
        "10000": "$10,000",
        "15000": "$15,000",
        "20000": "$20,000",
        "25000": "$25,000",
        "30000": "$30,000",
        "99000": "$99,000",
        "": "Not Available",
        " ": "Not Available"
    },
    
    # Person 1 TrueTouch Behavioral Mappings (Likelihood Scale)
    "P1_TRUETOUCH_DEAL_SEEKERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "P1_TRUETOUCH_IN_THE_MOMENT_SHOPPERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "P1_TRUETOUCH_MAINSTREAM_ADOPTERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "P1_TRUETOUCH_NOVELTY_SEEKERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "P1_TRUETOUCH_QUALITY_MATTERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "P1_TRUETOUCH_RECREATIONAL_SHOPPERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    
    # Additional TrueTouch Behavioral Mappings (Likelihood Scale)
    "TRUETOUCH_ORGANIC_AND_NATURAL": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "TRUETOUCH_SAVVY_RESEARCHERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "TRUETOUCH_BRAND_LOYALISTS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "TRUETOUCH_DEAL_SEEKERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "TRUETOUCH_RECREATIONAL_SHOPPERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    "TRUETOUCH_TRENDSETTERS": {
        "0": "Unknown",
        "1": "Extremely Likely",
        "2": "Highly Likely",
        "3": "Very Likely",
        "4": "Somewhat Likely",
        "5": "Likely",
        "6": "Somewhat Unlikely",
        "7": "Very Unlikely",
        "8": "Highly Unlikely",
        "9": "Extremely Unlikely"
    },
    
    # Dwelling Information
    "DWELLING_SIZE_LIVABLE_UNITS": {
        "A": "SFDU",
        "B": "Duplex",
        "C": "Triplex",
        "D": "4",
        "E": "5-9",
        "F": "10-19",
        "G": "20-49",
        "H": "50-100",
        "I": "101+"
    },
    
    # Mortgage Payment Information
    "ESTIMATED_CURRENTLY_MONTHLY_MORTGAGE": {
        "A": "$1-199",
        "B": "$200-299",
        "C": "$300-399",
        "D": "$400-499",
        "E": "$500-599",
        "F": "$600-699",
        "G": "$700-799",
        "H": "$800-899",
        "I": "$900-999",
        "J": "$1,000-1,199",
        "K": "$1,200-1,399",
        "L": "$1,400-1,699",
        "M": "$1,700-1,999",
        "N": "$2,000+",
        "U": "Unknown"
    },
    
    # New Homeowner and Mover Indicators
    "NEW_HOMEOWNER_INDICATOR_6M": {
        "N": "No",
        "Y": "Yes"
    },
    "NEW_MOVER_INDICATOR_LAST_6_MONTHS": {
        "N": "No",
        "Y": "Yes"
    },
    
    # Business Owner Indicator
    "PERSON_BUSINESS_OWNER": {
        "U": "Unknown",
        "Y": "Yes"
    },
    
    # Ethnic Information
    "PERSON_ETHNIC": {
        "00": "Unknown", "01": "English", "02": "Scottish", "03": "Danish", "04": "Swedish",
        "05": "Norwegian", "06": "Finnish", "07": "Icelandic", "08": "Dutch", "09": "Belgian",
        "10": "German", "11": "Austrian", "12": "Hungarian", "13": "Czech", "14": "Slovak",
        "15": "Irish", "16": "Welsh", "17": "French", "18": "Swiss", "19": "Italian",
        "20": "Hispanic", "21": "Portuguese", "22": "Polish", "23": "Estonian", "24": "Latvian",
        "25": "Lithuanian", "26": "Ukrainian", "27": "Georgian", "28": "Byelorussian", "29": "Armenian",
        "30": "Russian", "31": "Turkish", "32": "Kurdish", "33": "Greek", "34": "Persian",
        "35": "Moldovan", "36": "Bulgarian", "37": "Romanian", "38": "Albanian", "39": "Native American",
        "40": "Slovenian", "41": "Croat", "42": "Serb", "43": "Bosniak", "44": "Azerbaijani",
        "45": "Kazakh", "46": "Afghan", "47": "Pakistani", "48": "Bengali", "49": "Indonesian",
        "50": "Asian Indian", "51": "Burmese (Myanmar)", "52": "Mongolian", "53": "Chinese", "55": "Taiwanese",
        "56": "Korean", "57": "Japanese", "58": "Thai", "59": "Malaysian", "60": "Laotian",
        "61": "Khmer", "62": "Vietnamese", "63": "Sri Lankan", "64": "Uzbek", "65": "Hmong",
        "66": "Jewish", "67": "Aleut", "68": "Hebrew", "70": "Arab", "71": "Brazilian",
        "72": "Turkmen", "73": "Tajik", "74": "Kirghiz", "75": "Saudi", "76": "Iraqi",
        "77": "Libyan", "78": "Egyptian", "79": "Rwandan", "7B": "Djiboutian", "7C": "Manx",
        "7E": "Nepalese", "7F": "Samoan", "7G": "Mauritanian", "7H": "Inuit", "7M": "Trinidadian",
        "7N": "Southern African", "80": "Tongan", "81": "Senegalese", "82": "Malawian", "83": "South Sudanese",
        "84": "Moroccan", "85": "African American", "86": "Kenyan", "87": "Nigerian (Nigeria)", "88": "Ghanaian",
        "89": "Zambian", "8A": "Congolese", "8B": "Central African (Central African Republic)", "8C": "Togolese", "8D": "Bahraini",
        "8E": "Qatari", "8F": "Guyanese", "8G": "Tibetan", "8H": "Fijian", "8I": "Swazi",
        "8J": "Zulu", "8K": "Xhosa", "8M": "Afrikaner", "8N": "Liberian", "8O": "Comoran",
        "8P": "Beninese", "8Q": "Burkinabe (Burkina Faso)", "8R": "Nigerian (Niger)", "8S": "Akan", "8T": "Swahili",
        "8U": "Haitian", "8V": "Malian", "8W": "Jamaican", "8X": "Hausa", "8Y": "African Continental",
        "91": "Surinamese", "92": "Mozambican (Mozambique)", "93": "Ivorian (Ivory Coast)", "94": "Bhutanese", "95": "Ethiopian",
        "96": "Ugandan", "97": "Batswana (Botswana)", "98": "Cameroonian", "99": "Zimbabwean", "9A": "Namibian",
        "9B": "Burundi", "9C": "Tanzanian", "9D": "Gambian", "9E": "Somali", "9F": "Macedonian",
        "9G": "Chadian", "9H": "Gabonese", "9I": "Angolan", "9J": "Chechen", "9K": "Igbo",
        "9L": "Yoruba", "9M": "Algerian", "9N": "Filipino", "9O": "Sotho (Lesotho)", "9P": "Tunisian",
        "9Q": "Hawaiian", "9R": "Malagasy (Madagascar)", "9T": "Sierra Leonean", "9U": "Kuwaiti", "9V": "Yemeni",
        "9W": "Guinean (Guinea-Bissau)", "9X": "Papua New Guinean", "9Y": "Equatorial Guinean", "9Z": "Syrian",
        "A1": "African American (Arabic)", "A2": "African American (Arabic)", "A3": "African American (Arabic)",
        "A4": "African American (Arabic)", "A5": "African American (Arabic)", "D1": "African American (Dutch)",
        "D2": "African American (Dutch)", "D3": "African American (Dutch)", "D4": "African American (Dutch)",
        "D5": "African American (Dutch)", "E1": "African American (English)", "E2": "African American (English)",
        "E3": "African American (English)", "E4": "African American (English)", "E5": "African American (English)",
        "F1": "African American (French)", "F2": "African American (French)", "F3": "African American (French)",
        "F4": "African American (French)", "F5": "African American (French)", "I1": "African American (Irish)",
        "I2": "African American (Irish)", "I3": "African American (Irish)", "I4": "African American (Irish)",
        "I5": "African American (Irish)", "S1": "African American (Scotch)", "S2": "African American (Scotch)",
        "S3": "African American (Scotch)", "S4": "African American (Scotch)", "S5": "African American (Scotch)",
        "U1": "African American (Unknown)", "U2": "African American (Unknown)", "U3": "African American (Unknown)",
        "U4": "African American (Unknown)", "U5": "African American (Unknown)", "W1": "African American (Welsh)",
        "W2": "African American (Welsh)", "W3": "African American (Welsh)", "W4": "African American (Welsh)",
        "W5": "African American (Welsh)", "blank": "Null", "UC": "Uncodable", "ZZ": "Multi-Ethnic"
    },
    
    # Credit Cards Lifestyle Mappings
    "CREDIT_CARDS_AMERICAN_EXPRESS_PREMIUM": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_AMERICAN_EXPRESS_REGULAR": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_DISCOVER_PREMIUM": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_DISCOVER_REGULAR": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_MASTERCARD_REGULAR": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_OTHER_CARD_PREMIUM": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_OTHER_CARD_REGULAR": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_STORE_OR_RETAIL_REGULAR": {"U": "Unknown", "Y": "Yes"},
    "CREDIT_CARDS_VISA_REGULAR": {"U": "Unknown", "Y": "Yes"},
    
    # Financial Investment Lifestyle Mappings
    "FINANCIAL_CDS_MONEY_MKT_CUR": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_IRAS_CURRENTLY": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_LIFE_INSUR_CUR": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_MUTL_FUNDS_FUT_INT": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_MUTUAL_FUNDS_CURRENTLY": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_OTHR_INVEST_CUR": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_OTHR_INVEST_FUTURE": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_REAL_ESTATE_FUT": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_REAL_ESTATE_CURRENTLY": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_STKS_BOND_CUR": {"U": "Unknown", "Y": "Yes"},
    "FINANCIAL_STKS_BOND_FUT": {"U": "Unknown", "Y": "Yes"},
    
    # Pets Lifestyle Mappings
    "PETS_OWN_A_CAT": {"U": "Unknown", "Y": "Yes"},
    "PETS_OWN_A_DOG": {"U": "Unknown", "Y": "Yes"},
    "PETS_OWN_A_PET": {"U": "Unknown", "Y": "Yes"},
    
    # Military/Government Veteran Mapping
    "MILITARY_GOV_VETERAN": {"U": "Unknown", "Y": "Yes"},
    
    # Mortgage Term Mappings (format as months)
    "HOME_MORTGAGE_TERM": "format_as_months",
    "INVESTMENT_PROPERTY_MORTGAGE_TERM": "format_as_months",
}

# Field name to mapping key lookup (using mapped field names)
FIELD_TO_MAPPING_KEY: Dict[str, str] = {
    "Level of Education": "EDUCATION_LEVEL",     # Mapped from "EDUCATION LEVEL MODEL"
    "Marital Status": "MARITAL_STATUS",          # Mapped from "PERMARITALSTATUS"
        "Number of Children in Household": "number_of_children_in_household",
        "Homeowner": "HOMEOWNER",
        "Renter": "RENTER",
        "Mail Responder": "MAIL_RESPONDER",
        "Address Quality Indicator": "ADDRESS_QUALITY_INDICATOR",
        "Property Type": "PROPERTY_TYPE",
        "Home: Number of Bedrooms": "HOME_NUMBER_OF_BEDROOMS",
        "Home: Swimming Pool": "HOME_SWIMMING_POOL",
        "Presence of Child": "PRESENCE_OF_CHILD",
        "Green Aware Household": "GREEN_AWARE_HOUSEHOLD",
        "Household Composition": "HOUSEHOLD_COMPOSITION",
        "Dwelling Size in Livable Units": "DWELLING_SIZE_IN_LIVABLE_UNITS",
        "Number of Children in Home": "NUMBER_OF_CHILDREN_IN_HOME",
        "Number of Adults in Home": "NUMBER_OF_ADULTS_IN_HOME",
            "HH:Acty/Int:Collecting:Other Collectibles": "HH_ACTY_INT_COLLECTING_OTHER_COLLECTIBLES",
            "HH:Acty/Int:Collecting:Art/Antiques": "HH_ACTY_INT_COLLECTING_ART_ANTIQUES",
            "HH:Acty/Int:Collecting:Stamps/Coins": "HH_ACTY_INT_COLLECTING_STAMPS_COINS",
            "HH:Acty/Int:Collecting:Dolls": "HH_ACTY_INT_COLLECTING_DOLLS",
            "HH:Acty/Int:Collecting:Figurines": "HH_ACTY_INT_COLLECTING_FIGURINES",
            "HH:Acty/Int:Collecting:Sports Memorabilia": "HH_ACTY_INT_COLLECTING_SPORTS_MEMORABILIA",
            "HH:Acty/Int:Cooking/Entertaining:Cooking": "HH_ACTY_INT_COOKING_ENTERTAINING_COOKING",
            "HH:Acty/Int:Cooking/Entertaining:Baking": "HH_ACTY_INT_COOKING_ENTERTAINING_BAKING",
            "HH:Acty/Int:Cooking/Entertaining:Cook/Weight Con": "HH_ACTY_INT_COOKING_ENTERTAINING_COOK_WEIGHT_CON",
            "HH:Acty/Int:Cooking/Entertaining:Wine Appreciation": "HH_ACTY_INT_COOKING_ENTERTAINING_WINE_APPRECIATION",
            "HH:Acty/Int:Cooking/Entertaining:Cooking- Gourmet": "HH_ACTY_INT_COOKING_ENTERTAINING_COOKING_GOURMET",
            "HH:Acty/Int:Crafts:Crafts": "HH_ACTY_INT_CRAFTS_CRAFTS",
            "HH:Acty/Int:Crafts:Knitting/Needlework": "HH_ACTY_INT_CRAFTS_KNITTING_NEEDLEWORK",
            "HH:Acty/Int:Crafts:Quilting": "HH_ACTY_INT_CRAFTS_QUILTING",
            "HH:Acty/Int:Crafts:Sewing": "HH_ACTY_INT_CRAFTS_SEWING",
            "HH:Acty/Int:Crafts:Woodworking": "HH_ACTY_INT_CRAFTS_WOODWORKING",
            "HH:Acty/Int:Health/Fitness:Losing Weight": "HH_ACTY_INT_HEALTH_FITNESS_LOSING_WEIGHT",
            "SRVY:HH Acty/Int:Health/Fitness:Vit Supplements": "SRVY_HH_ACTY_INT_HEALTH_FITNESS_VIT_SUPPLEMENTS",
            "HH:Acty/Int:Health/Fitness:Hlth/Nat Foods": "HH_ACTY_INT_HEALTH_FITNESS_HLTH_NAT_FOODS",
            "HH:Acty/Int:Hobbies:Photography Hobbies": "HH_ACTY_INT_HOBBIES_PHOTOGRAPHY_HOBBIES",
            "HH:Acty/Int:Hobbies:Gardening Hobbies": "HH_ACTY_INT_HOBBIES_GARDENING_HOBBIES",
            "HH:Acty/Int:Hobbies:Cars And Auto Repair": "HH_ACTY_INT_HOBBIES_CARS_AUTO_REPAIR",
            "HH:Acty/Int:Hobbies:Self-Improvement": "HH_ACTY_INT_HOBBIES_SELF_IMPROVEMENT",
            "HH:Acty/Int:Music:Christian/Gospel": "HH_ACTY_INT_MUSIC_CHRISTIAN_GOSPEL",
            "HH:Acty/Int:Music:R And B": "HH_ACTY_INT_MUSIC_R_AND_B",
            "HH:Acty/Int:Music:Jazz/New Age": "HH_ACTY_INT_MUSIC_JAZZ_NEW_AGE",
            "HH:Acty/Int:Music:Classical": "HH_ACTY_INT_MUSIC_CLASSICAL",
            "HH:Acty/Int:Music:Rock N Roll": "HH_ACTY_INT_MUSIC_ROCK_N_ROLL",
            "HH:Acty/Int:Music:Country": "HH_ACTY_INT_MUSIC_COUNTRY",
            "HH:Acty/Int:Music:Music In General": "HH_ACTY_INT_MUSIC_MUSIC_IN_GENERAL",
            "HH:Acty/Int:Music:Other Music": "HH_ACTY_INT_MUSIC_OTHER_MUSIC",
            "HH:Acty/Int:Reading:Best Selling Fiction": "HH_ACTY_INT_READING_BEST_SELLING_FICTION",
            "HH:Acty/Int:Reading:Childrens Reading": "HH_ACTY_INT_READING_CHILDRENS_READING",
            "HH:Acty/Int:Reading:Computer": "HH_ACTY_INT_READING_COMPUTER",
            "HH:Acty/Int:Reading:Cooking/Culinary": "HH_ACTY_INT_READING_COOKING_CULINARY",
            "HH:Acty/Int:Reading:Country Lifestyle": "HH_ACTY_INT_READING_COUNTRY_LIFESTYLE",
            "HH:Acty/Int:Reading:Entertainment/People": "HH_ACTY_INT_READING_ENTERTAINMENT_PEOPLE",
            "HH:Acty/Int:Reading:Fashion": "HH_ACTY_INT_READING_FASHION",
            "HH:Acty/Int:Reading:History": "HH_ACTY_INT_READING_HISTORY",
            "HH:Acty/Int:Reading:Interior Decorating": "HH_ACTY_INT_READING_INTERIOR_DECORATING",
            "HH:Acty/Int:Reading:Medical/Health": "HH_ACTY_INT_READING_MEDICAL_HEALTH",
            "HH:Acty/Int:Reading:Military": "HH_ACTY_INT_READING_MILITARY",
            "HH:Acty/Int:Reading:Mystery": "HH_ACTY_INT_READING_MYSTERY",
            "HH:Acty/Int:Reading:Natural Health Remedies": "HH_ACTY_INT_READING_NATURAL_HEALTH_REMEDIES",
            "HH:Acty/Int:Reading:Romance": "HH_ACTY_INT_READING_ROMANCE",
            "HH:Acty/Int:Reading:Science Fiction": "HH_ACTY_INT_READING_SCIENCE_FICTION",
            "HH:Acty/Int:Reading:Science/Technology": "HH_ACTY_INT_READING_SCIENCE_TECHNOLOGY",
            "HH:Acty/Int:Reading:Sports Reading": "HH_ACTY_INT_READING_SPORTS_READING",
            "HH:Acty/Int:Reading:World News/Politics": "HH_ACTY_INT_READING_WORLD_NEWS_POLITICS",
            "HH:Acty/Int:Reading:Book Reader": "HH_ACTY_INT_READING_BOOK_READER",
            "HH:Acty/Int:Socl Caus/Con:Animal Wf Soc/Caus/Con": "HH_ACTY_INT_SOCL_CAUS_CON_ANIMAL_WF_SOC_CAUS_CON",
            "HH:Acty/Int:Socl Caus/Con:Environment/Wildlife": "HH_ACTY_INT_SOCL_CAUS_CON_ENVIRONMENT_WILDLIFE",
            "HH:Acty/Int:Socl Caus/Con:Political- Conservative": "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_CONSERVATIVE",
            "HH:Acty/Int:Socl Caus/Con:Political- Liberal": "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_LIBERAL",
            "HH:Acty/Int:Socl Caus/Con:Children": "HH_ACTY_INT_SOCL_CAUS_CON_CHILDREN",
            "HH:Acty/Int:Socl Caus/Con:Veterans": "HH_ACTY_INT_SOCL_CAUS_CON_VETERANS",
            "HH:Acty/Int:Socl Caus/Con:Hlty/Soc Cause/Con": "HH_ACTY_INT_SOCL_CAUS_CON_HLTY_SOC_CAUSE_CON",
            "HH:Acty/Int:Socl Caus/Con:Othr Soc/Cause Con": "HH_ACTY_INT_SOCL_CAUS_CON_OTHR_SOC_CAUSE_CON",
            "HH:Acty/Int:Sports/Rec:Baseball": "HH_ACTY_INT_SPORTS_REC_BASEBALL",
            "HH:Acty/Int:Sports/Rec:Basketball": "HH_ACTY_INT_SPORTS_REC_BASKETBALL",
            "HH:Acty/Int:Sports/Rec:Hockey": "HH_ACTY_INT_SPORTS_REC_HOCKEY",
            "HH:Acty/Int:Sports/Rec:Camping/Hiking": "HH_ACTY_INT_SPORTS_REC_CAMPING_HIKING",
            "HH:Acty/Int:Sports/Rec:Hunting": "HH_ACTY_INT_SPORTS_REC_HUNTING",
            "HH:Acty/Int:Sports/Rec:Fishing": "HH_ACTY_INT_SPORTS_REC_FISHING",
            "HH:Acty/Int:Sports/Rec:Nascar": "HH_ACTY_INT_SPORTS_REC_NASCAR",
            "HH:Acty/Int:Sports/Rec:Personal Fitness/Exercise": "HH_ACTY_INT_SPORTS_REC_PERSONAL_FITNESS_EXERCISE",
            "HH:Acty/Int:Sports/Rec:Scuba Diving": "HH_ACTY_INT_SPORTS_REC_SCUBA_DIVING",
            "HH:Acty/Int:Sports/Rec:Football": "HH_ACTY_INT_SPORTS_REC_FOOTBALL",
            "HH:Acty/Int:Sports/Rec:Golf": "HH_ACTY_INT_SPORTS_REC_GOLF",
            "HH:Acty/Int:Sports/Rec:Snow Skiing/Boarding": "HH_ACTY_INT_SPORTS_REC_SNOW_SKIING_BOARDING",
            "HH:Acty/Int:Sports/Rec:Boating/Sailing": "HH_ACTY_INT_SPORTS_REC_BOATING_SAILING",
            "HH:Acty/Int:Sports/Rec:Walking": "HH_ACTY_INT_SPORTS_REC_WALKING",
            "HH:Acty/Int:Sports/Rec:Cycling": "HH_ACTY_INT_SPORTS_REC_CYCLING",
            "HH:Acty/Int:Sports/Rec:Motorcycles": "HH_ACTY_INT_SPORTS_REC_MOTORCYCLES",
            "HH:Acty/Int:Sports/Rec:Running/Jogging": "HH_ACTY_INT_SPORTS_REC_RUNNING_JOGGING",
            "HH:Acty/Int:Sports/Rec:Soccer": "HH_ACTY_INT_SPORTS_REC_SOCCER",
            "HH:Acty/Int:Sports/Rec:Swimming": "HH_ACTY_INT_SPORTS_REC_SWIMMING",
            "HH:Acty/Int:Sports/Rec:Play Sports In General": "HH_ACTY_INT_SPORTS_REC_PLAY_SPORTS_IN_GENERAL",
            "TrueTouch: Email Engagement": "TRUETOUCH_EMAIL_ENGAGEMENT",
            "Person 1: TrueTouch: Savvy Researchers": "TRUETOUCH_SAVVY_RESEARCHERS",
            "Person 1: TrueTouch: Organic and natural": "TRUETOUCH_ORGANIC_AND_NATURAL",
            "Person 1: TrueTouch: Brand Loyalists": "TRUETOUCH_BRAND_LOYALISTS",
            "Person 1: TrueTouch: Trendsetters": "TRUETOUCH_TRENDSETTERS",
            "Median: Est HH Income Range V6": "MEDIAN_EST_HH_INCOME_RANGE_V6",
                "Children by Age/Gender": "CHILDREN_BY_AGE_GENDER",
                "Property/Realty: Building square footage ranges": "PROPERTY_REALTY_BUILDING_SQ_FOOTAGE_RANGES",
                "Mortgage/Home Purchase: Purchase amount ranges": "MORTGAGE_HOME_PURCHASE_PURCHASE_AMOUNT_RANGES",
                "Mortgage/Home Purchase: Mortgage amount ranges": "MORTGAGE_HOME_PURCHASE_MORTGAGE_AMOUNT_RANGES",
                
        # Additional Reading Fields
        "HH:Acty/Int:Reading:Interior Decorating": "HH_ACTY_INT_READING_INTERIOR_DECORATING",
        "HH:Acty/Int:Reading:Medical/Health": "HH_ACTY_INT_READING_MEDICAL_HEALTH", 
        "HH:Acty/Int:Reading:Military": "HH_ACTY_INT_READING_MILITARY",
        "HH:Acty/Int:Reading:Mystery": "HH_ACTY_INT_READING_MYSTERY",
        "HH:Acty/Int:Reading:Natural Health Remedies": "HH_ACTY_INT_READING_NATURAL_HEALTH_REMEDIES",
        "HH:Acty/Int:Reading:Romance": "HH_ACTY_INT_READING_ROMANCE",
        "HH:Acty/Int:Reading:Science Fiction": "HH_ACTY_INT_READING_SCIENCE_FICTION",
        "HH:Acty/Int:Reading:Science/Technology": "HH_ACTY_INT_READING_SCIENCE_TECHNOLOGY",
        "HH:Acty/Int:Reading:Sports Reading": "HH_ACTY_INT_READING_SPORTS_READING",
        "HH:Acty/Int:Reading:World News/Politics": "HH_ACTY_INT_READING_WORLD_NEWS_POLITICS",
        "HH:Acty/Int:Reading:Book Reader": "HH_ACTY_INT_READING_BOOK_READER",
        
        # Social Causes and Concerns
        "HH:Acty/Int:Socl Caus/Con:Animal Wf Soc/Caus/Con": "HH_ACTY_INT_SOCL_CAUS_CON_ANIMAL_WF_SOC_CAUS_CON",
        "HH:Acty/Int:Socl Caus/Con:Environment/Wildlife": "HH_ACTY_INT_SOCL_CAUS_CON_ENVIRONMENT_WILDLIFE",
        "HH:Acty/Int:Socl Caus/Con:Political- Conservative": "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_CONSERVATIVE",
        "HH:Acty/Int:Socl Caus/Con:Political- Liberal": "HH_ACTY_INT_SOCL_CAUS_CON_POLITICAL_LIBERAL",
        "HH:Acty/Int:Socl Caus/Con:Children": "HH_ACTY_INT_SOCL_CAUS_CON_CHILDREN",
        "HH:Acty/Int:Socl Caus/Con:Veterans": "HH_ACTY_INT_SOCL_CAUS_CON_VETERANS",
        "HH:Acty/Int:Socl Caus/Con:Hlty/Soc Cause/Con": "HH_ACTY_INT_SOCL_CAUS_CON_HLTY_SOC_CAUSE_CON",
        "HH:Acty/Int:Socl Caus/Con:Othr Soc/Cause Con": "HH_ACTY_INT_SOCL_CAUS_CON_OTHR_SOC_CAUSE_CON",
        
        # Sports and Recreation
        "HH:Acty/Int:Sports/Rec:Baseball": "HH_ACTY_INT_SPORTS_REC_BASEBALL",
        "HH:Acty/Int:Sports/Rec:Basketball": "HH_ACTY_INT_SPORTS_REC_BASKETBALL",
        "HH:Acty/Int:Sports/Rec:Hockey": "HH_ACTY_INT_SPORTS_REC_HOCKEY",
        "HH:Acty/Int:Sports/Rec:Camping/Hiking": "HH_ACTY_INT_SPORTS_REC_CAMPING_HIKING",
        "HH:Acty/Int:Sports/Rec:Hunting": "HH_ACTY_INT_SPORTS_REC_HUNTING",
        "HH:Acty/Int:Sports/Rec:Fishing": "HH_ACTY_INT_SPORTS_REC_FISHING",
        "HH:Acty/Int:Sports/Rec:Nascar": "HH_ACTY_INT_SPORTS_REC_NASCAR",
        "HH:Acty/Int:Sports/Rec:Personal Fitness/Exercise": "HH_ACTY_INT_SPORTS_REC_PERSONAL_FITNESS_EXERCISE",
        "HH:Acty/Int:Sports/Rec:Scuba Diving": "HH_ACTY_INT_SPORTS_REC_SCUBA_DIVING",
        "HH:Acty/Int:Sports/Rec:Football": "HH_ACTY_INT_SPORTS_REC_FOOTBALL",
        "HH:Acty/Int:Sports/Rec:Golf": "HH_ACTY_INT_SPORTS_REC_GOLF",
        "HH:Acty/Int:Sports/Rec:Snow Skiing/Boarding": "HH_ACTY_INT_SPORTS_REC_SNOW_SKIING_BOARDING",
        "HH:Acty/Int:Sports/Rec:Boating/Sailing": "HH_ACTY_INT_SPORTS_REC_BOATING_SAILING",
        "HH:Acty/Int:Sports/Rec:Walking": "HH_ACTY_INT_SPORTS_REC_WALKING",
        "HH:Acty/Int:Sports/Rec:Cycling": "HH_ACTY_INT_SPORTS_REC_CYCLING",
        "HH:Acty/Int:Sports/Rec:Motorcycles": "HH_ACTY_INT_SPORTS_REC_MOTORCYCLES",
        "HH:Acty/Int:Sports/Rec:Running/Jogging": "HH_ACTY_INT_SPORTS_REC_RUNNING_JOGGING",
        "HH:Acty/Int:Sports/Rec:Soccer": "HH_ACTY_INT_SPORTS_REC_SOCCER",
        "HH:Acty/Int:Sports/Rec:Swimming": "HH_ACTY_INT_SPORTS_REC_SWIMMING",
        "HH:Acty/Int:Sports/Rec:Play Sports In General": "HH_ACTY_INT_SPORTS_REC_PLAY_SPORTS_IN_GENERAL",
        
        # Travel and Sweepstakes
        "HH:Acty/Int:Travel/Sweepstakes:Domestic Travel": "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_DOMESTIC_TRAVEL",
        "HH:Acty/Int:Travel/Sweepstakes:Foreign Travel": "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_FOREIGN_TRAVEL",
        "HH:Acty/Int:Travel/Sweepstakes:Sweepstakes": "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_SWEEPSTAKES",
        "HH:Acty/Int:Travel/Sweepstakes:Casino Gambling": "HH_ACTY_INT_TRAVEL_SWEEPSTAKES_CASINO_GAMBLING",
        
        # TrueTouch Behavioral Scores
        "TrueTouch: Email Engagement": "TRUETOUCH_EMAIL_ENGAGEMENT",
        "Person 1: TrueTouch: Savvy Researchers": "TRUETOUCH_SAVVY_RESEARCHERS",
        "Person 1: TrueTouch: Organic and natural": "TRUETOUCH_ORGANIC_AND_NATURAL",
        "Person 1: TrueTouch: Brand Loyalists": "TRUETOUCH_BRAND_LOYALISTS",
        "Person 1: TrueTouch: Trendsetters": "TRUETOUCH_TRENDSETTERS",
        
        # Income and Financial
        "Median: Est HH Income Range V6": "MEDIAN_EST_HH_INCOME_RANGE_V6",
        
        # Electronics and Technology
        "HH:Acty/Int:Electronics/Technology:Computers": "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_COMPUTERS",
        "HH:Acty/Int:Electronics/Technology:Video Games": "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_VIDEO_GAMES",
        "HH:Acty/Int:Electronics/Technology:Electronics": "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_ELECTRONICS",
        "HH:Acty/Int:Electronics/Technology:Home Tech": "HH_ACTY_INT_ELECTRONICS_TECHNOLOGY_HOME_TECH",
        
        # Lifestyle Categories
        "Lifestyle/Interests: Gambling Propensity": "LIFESTYLE_INTERESTS_GAMBLING_PROPENSITY",
        "Lifestyle/Interests: Investment Propensity": "LIFESTYLE_INTERESTS_INVESTMENT_PROPENSITY",
        "Lifestyle/Interests: Insurance Propensity": "LIFESTYLE_INTERESTS_INSURANCE_PROPENSITY",
        
        # Magazine Interests
        "Magazine Interests: News/Politics": "MAGAZINE_INTERESTS_NEWS_POLITICS",
        "Magazine Interests: Automotive": "MAGAZINE_INTERESTS_AUTOMOTIVE",
        "Magazine Interests: Sports": "MAGAZINE_INTERESTS_SPORTS",
        "Magazine Interests: Health/Fitness": "MAGAZINE_INTERESTS_HEALTH_FITNESS",
        "Magazine Interests: Home/Garden": "MAGAZINE_INTERESTS_HOME_GARDEN",
        
        # Ethnicity Demographics
        "Ethnicity Detail: Hispanic Country Code": "ETHNICITY_DETAIL_HISPANIC_COUNTRY_CODE",
        "Ethnicity Detail: African Country Code": "ETHNICITY_DETAIL_AFRICAN_COUNTRY_CODE",
        "Ethnicity Detail: Asian Country Code": "ETHNICITY_DETAIL_ASIAN_COUNTRY_CODE",
        
        # Additional TrueTouch Behavioral Scores
        "TrueTouch: Quality matters": "TRUETOUCH_QUALITY_MATTERS",
        "TrueTouch: In the moment shoppers": "TRUETOUCH_IN_THE_MOMENT_SHOPPERS",
        "TrueTouch: Mainstream adopters": "TRUETOUCH_MAINSTREAM_ADOPTERS",
        "TrueTouch: Novelty seekers": "TRUETOUCH_NOVELTY_SEEKERS",
        
        # TrueTouch Engagement Channels  
        "Person 1: TrueTouch Eng: Broadcast Cable TV": "TRUETOUCH_ENG_BROADCAST_CABLE_TV",
        "TrueTouch Eng: Broadcast Cable TV": "TRUETOUCH_ENG_BROADCAST_CABLE_TV",
        "Person 1: TrueTouch Eng: Digital Display": "TRUETOUCH_ENG_DIGITAL_DISPLAY",
        "TrueTouch Eng: Digital Display": "TRUETOUCH_ENG_DIGITAL_DISPLAY",
        "Person 1: TrueTouch Eng: Direct Mail": "TRUETOUCH_ENG_DIRECT_MAIL",
        "TrueTouch Eng: Direct Mail": "TRUETOUCH_ENG_DIRECT_MAIL",
        "Person 1: TrueTouch Eng: Digital Newspaper": "TRUETOUCH_ENG_DIGITAL_NEWSPAPER",
        "TrueTouch Eng: Digital Newspaper": "TRUETOUCH_ENG_DIGITAL_NEWSPAPER",
        "Person 1: TrueTouch Eng: Digital Video": "TRUETOUCH_ENG_DIGITAL_VIDEO",
        "TrueTouch Eng: Digital Video": "TRUETOUCH_ENG_DIGITAL_VIDEO",
        "Person 1: TrueTouch Eng: Radio": "TRUETOUCH_ENG_RADIO",
        "TrueTouch Eng: Radio": "TRUETOUCH_ENG_RADIO",
        "Person 1: TrueTouch Eng: Streaming TV": "TRUETOUCH_ENG_STREAMING_TV",
        "TrueTouch Eng: Streaming TV": "TRUETOUCH_ENG_STREAMING_TV",
        "Person 1: TrueTouch Eng: Traditional Newspaper": "TRUETOUCH_ENG_TRADITIONAL_NEWSPAPER",
        "TrueTouch Eng: Traditional Newspaper": "TRUETOUCH_ENG_TRADITIONAL_NEWSPAPER",
        "Person 1: TrueTouch Eng: Mobile SMS MMS": "TRUETOUCH_ENG_MOBILE_SMS_MMS",
        "TrueTouch Eng: Mobile SMS MMS": "TRUETOUCH_ENG_MOBILE_SMS_MMS",
        
        # TrueTouch Conversion Channels
        "Person 1: TT Conv: Online Deal Voucher": "TRUETOUCH_CONV_ONLINE_DEAL_VOUCHER",
        "TT Conv: Online Deal Voucher": "TRUETOUCH_CONV_ONLINE_DEAL_VOUCHER",
        "Person 1: TT Conv: Discount Supercenters": "TRUETOUCH_CONV_DISCOUNT_SUPERCENTERS",
        "TT Conv: Discount Supercenters": "TRUETOUCH_CONV_DISCOUNT_SUPERCENTERS",
        "Person 1: TT Conv: Ebid Sites": "TRUETOUCH_CONV_EBID_SITES",
        "TT Conv: EBid Sites": "TRUETOUCH_CONV_EBID_SITES",
        "Person 1: TT Conv Conv: Etail only": "TRUETOUCH_CONV_ETAIL_ONLY",
        "TT Conv: Etail only": "TRUETOUCH_CONV_ETAIL_ONLY",
        "Person 1: TT Conv: Mid-High End Store": "TRUETOUCH_CONV_MID_HIGH_END_STORE",
        "TT Conv: Mid-High End Store": "TRUETOUCH_CONV_MID_HIGH_END_STORE",
        "Person 1: TT Conv Conv: Specialty Dept Store": "TRUETOUCH_CONV_SPECIALTY_DEPT_STORE",
        "TT Conv: Specialty Dept Store": "TRUETOUCH_CONV_SPECIALTY_DEPT_STORE",
        "Person 1: TT Conv Conv: Wholesale": "TRUETOUCH_CONV_WHOLESALE",
        "TT Conv: Wholesale": "TRUETOUCH_CONV_WHOLESALE",
        "Person 1: TT Conv Conv: Specialty or Boutique": "TRUETOUCH_CONV_SPECIALTY_OR_BOUTIQUE",
        "TT Conv: Specialty or Boutique": "TRUETOUCH_CONV_SPECIALTY_OR_BOUTIQUE",
        
        # Financial and Credit Scores
        "Overall Financial Health Score": "OVERALL_FINANCIAL_HEALTH_SCORE",
        "Affluence Score": "AFFLUENCE_SCORE",
        
        # Home Value and Real Estate Fields
        "Estimated Current Home Value": "ESTIMATED_CURRENT_HOME_VALUE",
        "Home: Home Purchase Price": "HOME_PURCHASE_PRICE",
        "Home: Original Loan to Value": "HOME_ORIGINAL_LOAN_TO_VALUE",
        "Real Estate: Available Equity Amount": "REAL_ESTATE_AVAILABLE_EQUITY_AMOUNT",
        "Real Estate: Estimated Current Mortgage Amount": "REAL_ESTATE_ESTIMATED_CURRENT_MORTGAGE_AMOUNT",
        
        # Additional Home Value and Financial Fields
        "Home Total Value": "HOME_TOTAL_VALUE",
        "Real Estate Tax": "REAL_ESTATE_TAX",
        "Home Land Value": "HOME_LAND_VALUE",
        "Home: Home Purchase Price": "HOME_PURCHASE_PRICE",  # Duplicate mapping for consistency
        "Home Purchase Mortgage Amount": "HOME_PURCHASE_MORTGAGE_AMOUNT",
        "Investment Property: Purchase Amount": "INVESTMENT_PROPERTY_PURCHASE_AMOUNT",
        
        # Cultural Arts and Electronics/Gadgets Fields
        "HH:Acty/Int:Cltrl/Arts:Interest In Cultrual Arts": "HH_ACTY_INT_CLTRL_ARTS_INTEREST_IN_CULTURAL_ARTS",
        "HH:Acty/Int:Elctrncs/Gdgts:Compact Disc Player": "HH_ACTY_INT_ELCTRNCS_GDGTS_COMPACT_DISC_PLAYER", 
        "HH:Acty/Int:Elctrncs/Gdgts:Cell Phone": "HH_ACTY_INT_ELCTRNCS_GDGTS_CELL_PHONE",
        "HH:Acty/Int:Elctrncs/Gdgts:Digital Camera": "HH_ACTY_INT_ELCTRNCS_GDGTS_DIGITAL_CAMERA",
        "HH:Acty/Int:Elctrncs/Gdgts:Dvd Player": "HH_ACTY_INT_ELCTRNCS_GDGTS_DVD_PLAYER",
        "HH:Acty/Int:Elctrncs/Gdgts:Hdtv": "HH_ACTY_INT_ELCTRNCS_GDGTS_HDTV",
        "HH:Acty/Int:Elctrncs/Gdgts:Interest In Electronics": "HH_ACTY_INT_ELCTRNCS_GDGTS_INTEREST_IN_ELECTRONICS",
        "HH:Acty/Int:Elctrncs/Gdgts:Pda/Blackberry": "HH_ACTY_INT_ELCTRNCS_GDGTS_PDA_BLACKBERRY",
        "HH:Acty/Int:Elctrncs/Gdgts:Satellite Dish": "HH_ACTY_INT_ELCTRNCS_GDGTS_SATELLITE_DISH",
        "HH:Acty/Int:Elctrncs/Gdgts:Video Camera": "HH_ACTY_INT_ELCTRNCS_GDGTS_VIDEO_CAMERA",
        "HH:Acty/Int:Elctrncs/Gdgts:Video Game System": "HH_ACTY_INT_ELCTRNCS_GDGTS_VIDEO_GAME_SYSTEM",
        
        # Magazine Interest Fields
        "HH:Acty/Int:Magazines:Business And Finance": "HH_ACTY_INT_MAGAZINES_BUSINESS_AND_FINANCE",
        "HH:Acty/Int:Magazines:Childrens Magazines": "HH_ACTY_INT_MAGAZINES_CHILDRENS_MAGAZINES",
        "HH:Acty/Int:Magazines:Computer/Electronics": "HH_ACTY_INT_MAGAZINES_COMPUTER_ELECTRONICS",
        "HH:Acty/Int:Magazines:Crafts Games And Hobbies": "HH_ACTY_INT_MAGAZINES_CRAFTS_GAMES_AND_HOBBIES",
        "HH:Acty/Int:Magazines:Current Events/News": "HH_ACTY_INT_MAGAZINES_CURRENT_EVENTS_NEWS",
        "HH:Acty/Int:Magazines:Fitness": "HH_ACTY_INT_MAGAZINES_FITNESS",
        "HH:Acty/Int:Magazines:Food/Wine/Cooking": "HH_ACTY_INT_MAGAZINES_FOOD_WINE_COOKING",
        "HH:Acty/Int:Magazines:Gardening Magazines": "HH_ACTY_INT_MAGAZINES_GARDENING_MAGAZINES",
        "HH:Acty/Int:Magazines:Hunting And Fishing": "HH_ACTY_INT_MAGAZINES_HUNTING_AND_FISHING",
        "HH:Acty/Int:Magazines:Mens": "HH_ACTY_INT_MAGAZINES_MENS",
        "HH:Acty/Int:Magazines:Music": "HH_ACTY_INT_MAGAZINES_MUSIC",
        "HH:Acty/Int:Magazines:Sports Magazines": "HH_ACTY_INT_MAGAZINES_SPORTS_MAGAZINES",
        "HH:Acty/Int:Magazines:Subscription": "HH_ACTY_INT_MAGAZINES_SUBSCRIPTION",
        "HH:Acty/Int:Magazines:Travel": "HH_ACTY_INT_MAGAZINES_TRAVEL",
        "HH:Acty/Int:Magazines:Womens": "HH_ACTY_INT_MAGAZINES_WOMENS",
        
        # PC & Internet Fields
        "HH:Acty/Int:PC & Internet:Own Computer": "HH_ACTY_INT_PC_INTERNET_OWN_COMPUTER",
        "HH:Acty/Int:PC & Internet:Plan To Buy Computer": "HH_ACTY_INT_PC_INTERNET_PLAN_TO_BUY_COMPUTER",
        "HH:Acty/Int:PC & Internet:Use Internet Service": "HH_ACTY_INT_PC_INTERNET_USE_INTERNET_SERVICE",
        "HH:Acty/Int:PC & Internet:Usedsl/Hispd": "HH_ACTY_INT_PC_INTERNET_USEDSL_HISPD",
        
        # Reading Fields
        "HH:Acty/Int:Reading:Computer": "HH_ACTY_INT_READING_COMPUTER",
        
        # Sweepstakes Fields
        "HH:Acty/Int:Sweepstakes:Lotteries": "HH_ACTY_INT_SWEEPSTAKES_LOTTERIES",
        "HH:Acty/Int:Sweepstakes:Sweepstakes": "HH_ACTY_INT_SWEEPSTAKES_SWEEPSTAKES",
        
        # Travel Fields
        "HH:Acty/Int:Travel:Business Travel": "HH_ACTY_INT_TRAVEL_BUSINESS_TRAVEL",
        "HH:Acty/Int:Travel:Cruise": "HH_ACTY_INT_TRAVEL_CRUISE",
        "HH:Acty/Int:Travel:Domestic": "HH_ACTY_INT_TRAVEL_DOMESTIC",
        "HH:Acty/Int:Travel:International": "HH_ACTY_INT_TRAVEL_INTERNATIONAL",
        "HH:Acty/Int:Travel:Personal Travel": "HH_ACTY_INT_TRAVEL_PERSONAL_TRAVEL",
        "HH:Acty/Int:Travel:Recreational Vehicle": "HH_ACTY_INT_TRAVEL_RECREATIONAL_VEHICLE",
        "HH:Acty/Int:Travel:Time Share": "HH_ACTY_INT_TRAVEL_TIME_SHARE",
        "HH:Acty/Int:Travel:Would Enjoy Rv Travel": "HH_ACTY_INT_TRAVEL_WOULD_ENJOY_RV_TRAVEL",
        
        # Lifestyle Fields
        "HH:Lifestyl:Affiliation/Member:Music Club": "HH_LIFESTYL_AFFILIATION_MEMBER_MUSIC_CLUB",
        "HH:Lifestyl:Buying Interest:Comp/Elec": "HH_LIFESTYL_BUYING_INTEREST_COMP_ELEC",
        "HH:Lifestyl:Buying Interest:Sports Related": "HH_LIFESTYL_BUYING_INTEREST_SPORTS_RELATED",
        "HH:Lifestyl:Entertainment:Buy Pre-Recorded Videos": "HH_LIFESTYL_ENTERTAINMENT_BUY_PRE_RECORDED_VIDEOS",
        "HH:Lifestyl:Entertainment:Watch Cable Tv": "HH_LIFESTYL_ENTERTAINMENT_WATCH_CABLE_TV",
        "HH:Lifestyl:Entertainment:Watch Videos": "HH_LIFESTYL_ENTERTAINMENT_WATCH_VIDEOS",
        "HH:Lifestyl:Financial:Iras - Future Interest": "HH_LIFESTYL_FINANCIAL_IRAS_FUTURE_INTEREST",
        "HH:Lifestyl:Grandkids:Proud Grandparent": "HH_LIFESTYL_GRANDKIDS_PROUD_GRANDPARENT",
        "HH:Lifestyl:Pets:Own A Cat": "HH_LIFESTYL_PETS_OWN_A_CAT",
        "HH:Lifestyl:Pets:Own A Dog": "HH_LIFESTYL_PETS_OWN_A_DOG",
        "HH:Lifestyl:Pets:Own A Pet": "HH_LIFESTYL_PETS_OWN_A_PET",
        
        # DSE (Direct Spend Estimate) Fields
        "DSE: Dine Out": "DSE_DINE_OUT",
        "DSE: Alcohol and Wine": "DSE_ALCOHOL_WINE", 
        "DSE: Apparel": "DSE_APPAREL",
        "DSE: Entertainment": "DSE_ENTERTAINMENT",
        "DSE: Personal": "DSE_PERSONAL",
        "DSE: Reading": "DSE_READING",
        "DSE: Education": "DSE_EDUCATION",
        "DSE: Travel": "DSE_TRAVEL",
        "DSE: Donation": "DSE_DONATION",
        "DSE: Furnishings": "DSE_FURNISHINGS",
        
        # Date Fields
        "Home: Purchase Date": "HOME_PURCHASE_DATE",
        
        # Person 1 TrueTouch Behavioral Fields
        "Person 1: TrueTouch: Deal Seekers": "P1_TRUETOUCH_DEAL_SEEKERS",
        "Person 1: TrueTouch: In The Moment Shoppers": "P1_TRUETOUCH_IN_THE_MOMENT_SHOPPERS",
        "Person 1: TrueTouch: Mainstream Adopters": "P1_TRUETOUCH_MAINSTREAM_ADOPTERS",
        "Person 1: TrueTouch: Novelty Seekers": "P1_TRUETOUCH_NOVELTY_SEEKERS",
        "Person 1: TrueTouch: Quality Matters": "P1_TRUETOUCH_QUALITY_MATTERS",
        "Person 1: TrueTouch: Recreational Shoppers": "P1_TRUETOUCH_RECREATIONAL_SHOPPERS",
        
        # Additional TrueTouch Behavioral Fields
        "TrueTouch: Organic And Natural": "TRUETOUCH_ORGANIC_AND_NATURAL",
        "TrueTouch: Savvy Researchers": "TRUETOUCH_SAVVY_RESEARCHERS",
        "TrueTouch: Brand Loyalists": "TRUETOUCH_BRAND_LOYALISTS",
        "TrueTouch: Deal Seekers": "TRUETOUCH_DEAL_SEEKERS",
        "TrueTouch: Recreational Shoppers": "TRUETOUCH_RECREATIONAL_SHOPPERS",
        "TrueTouch: Trendsetters": "TRUETOUCH_TRENDSETTERS",
        
        # Dwelling Information
        "Dwelling Size in Livable Units": "DWELLING_SIZE_LIVABLE_UNITS",
        
        # Mortgage Payment Information
        "Estimated Currently Monthly Mortgage": "ESTIMATED_CURRENTLY_MONTHLY_MORTGAGE",
        
        # New Homeowner and Mover Indicators
        "New Homeowner Indicator 6M": "NEW_HOMEOWNER_INDICATOR_6M",
        "New Mover: Indicator last 6 months": "NEW_MOVER_INDICATOR_LAST_6_MONTHS",
        
        # Business Owner Indicator
        "Person #: Business Owner": "PERSON_BUSINESS_OWNER",
        
        # Birth Date Information
        "Person #: Birth Year and Month": "PERSON_BIRTH_YEAR_AND_MONTH",
        
        # Ethnic Information
        "Person #: Ethnic - Ethnic": "PERSON_ETHNIC",
        
    # Mortgage Payment Fields
    "Average monthly payment on open first mortgage trades reported in the last 6 months": "AVG_MTHLY_PYMT_1ST_MORTGAGE",
    "Average monthly payment on open second mortgage trades reported in the last 6 months": "AVG_MTHLY_PYMT_2ND_MORTGAGE",
    
    # Credit Cards Lifestyle Fields
    "HH:Lifestyl:Credit Cards:American Express/Premium": "CREDIT_CARDS_AMERICAN_EXPRESS_PREMIUM",
    "HH:Lifestyl:Credit Cards:American Express/Regular": "CREDIT_CARDS_AMERICAN_EXPRESS_REGULAR",
    "HH:Lifestyl:Credit Cards:Discover/Premium": "CREDIT_CARDS_DISCOVER_PREMIUM",
    "HH:Lifestyl:Credit Cards:Discover/Regular": "CREDIT_CARDS_DISCOVER_REGULAR",
    "HH:Lifestyl:Credit Cards:Mastercard/Regular": "CREDIT_CARDS_MASTERCARD_REGULAR",
    "HH:Lifestyl:Credit Cards:Other Card/Premium": "CREDIT_CARDS_OTHER_CARD_PREMIUM",
    "HH:Lifestyl:Credit Cards:Other Card/Regular": "CREDIT_CARDS_OTHER_CARD_REGULAR",
    "HH:Lifestyl:Credit Cards:Store Or Retail/Regular": "CREDIT_CARDS_STORE_OR_RETAIL_REGULAR",
    "HH:Lifestyl:Credit Cards:Visa/Regular": "CREDIT_CARDS_VISA_REGULAR",
    
    # Financial Investment Lifestyle Fields
    "HH:Lifestyl:Financial:Cds/Money Mkt - Cur": "FINANCIAL_CDS_MONEY_MKT_CUR",
    "HH:Lifestyl:Financial:Iras - Currently": "FINANCIAL_IRAS_CURRENTLY",
    "HH:Lifestyl:Financial:Life Insur. - Cur": "FINANCIAL_LIFE_INSUR_CUR",
    "HH:Lifestyl:Financial:Mutl Funds/ - Fut Int": "FINANCIAL_MUTL_FUNDS_FUT_INT",
    "HH:Lifestyl:Financial:Mutual Funds - Currently": "FINANCIAL_MUTUAL_FUNDS_CURRENTLY",
    "HH:Lifestyl:Financial:Othr Invest - Cur": "FINANCIAL_OTHR_INVEST_CUR",
    "HH:Lifestyl:Financial:Othr Invest - Future": "FINANCIAL_OTHR_INVEST_FUTURE",
    "HH:Lifestyl:Financial:Real Estate - Fut": "FINANCIAL_REAL_ESTATE_FUT",
    "HH:Lifestyl:Financial:Real Estate- Currently": "FINANCIAL_REAL_ESTATE_CURRENTLY",
    "HH:Lifestyl:Financial:Stks/Bond - Cur": "FINANCIAL_STKS_BOND_CUR",
    "HH:Lifestyl:Financial:Stks/Bond - Fut": "FINANCIAL_STKS_BOND_FUT",
    
    # Pets Lifestyle Fields
    "HH:Lifestyl:Pets:Own A Cat": "PETS_OWN_A_CAT",
    "HH:Lifestyl:Pets:Own A Dog": "PETS_OWN_A_DOG",
    "HH:Lifestyl:Pets:Own A Pet": "PETS_OWN_A_PET",
    
    # Military/Government Veteran Field
    "HH:Lifestyl:Military/Gov:Vetern": "MILITARY_GOV_VETERAN",
    
    # Mortgage Term Fields
    "Home: Mortgage Term": "HOME_MORTGAGE_TERM",
    "Investment Property: Mortgage Term": "INVESTMENT_PROPERTY_MORTGAGE_TERM",
}

def map_field_values(data: Any, field_name: str = "") -> Any:
    """
    Convert API response codes to human-readable descriptions
    
    Args:
        data: The value to transform
        field_name: The field name to determine which mapping to use
        
    Returns:
        Transformed value with human-readable description
    """
    if not isinstance(data, (str, int)):
        return data
    
    # Convert to string for mapping lookup
    value_str = str(data).strip()
    
    # Find the mapping key for this field
    mapping_key = FIELD_TO_MAPPING_KEY.get(field_name)
    if not mapping_key:
        return data
    
    # Special handling for dollar value fields
    if mapping_key in [
        "ESTIMATED_CURRENT_HOME_VALUE", 
        "HOME_PURCHASE_PRICE", 
        "REAL_ESTATE_AVAILABLE_EQUITY_AMOUNT",
        "REAL_ESTATE_ESTIMATED_CURRENT_MORTGAGE_AMOUNT",
        "HOME_TOTAL_VALUE",
        "REAL_ESTATE_TAX", 
        "HOME_LAND_VALUE",
        "HOME_PURCHASE_MORTGAGE_AMOUNT",
        "INVESTMENT_PROPERTY_PURCHASE_AMOUNT",
        # DSE (Direct Spend Estimate) fields
        "DSE_DINE_OUT",
        "DSE_ALCOHOL_WINE",
        "DSE_APPAREL", 
        "DSE_ENTERTAINMENT",
        "DSE_PERSONAL",
        "DSE_READING",
        "DSE_EDUCATION",
        "DSE_TRAVEL",
        "DSE_DONATION",
        "DSE_FURNISHINGS",
        # Mortgage Payment Fields (values come with leading zeros and need division by 100)
        "AVG_MTHLY_PYMT_1ST_MORTGAGE",
        "AVG_MTHLY_PYMT_2ND_MORTGAGE"
    ]:
        try:
            # Handle mortgage payment fields that need division by 100 (0000064560 -> $6,456)
            if mapping_key in ["AVG_MTHLY_PYMT_1ST_MORTGAGE", "AVG_MTHLY_PYMT_2ND_MORTGAGE"]:
                dollar_value = int(value_str) / 100
                if dollar_value == 0:
                    return "$0"
                else:
                    return f"${dollar_value:,.0f}"
            # Handle fields that should be formatted in thousands (K format)
            elif mapping_key in ["REAL_ESTATE_AVAILABLE_EQUITY_AMOUNT", "REAL_ESTATE_ESTIMATED_CURRENT_MORTGAGE_AMOUNT", "INVESTMENT_PROPERTY_PURCHASE_AMOUNT"]:
                dollar_value = int(value_str)
                if dollar_value == 0:
                    return "$0"
                else:
                    return f"${dollar_value:,}k"
            else:
                # For other dollar fields, use value as-is
                dollar_value = int(value_str)
                if dollar_value == 0:
                    return "$0"
                else:
                    return f"${dollar_value:,}"
        except ValueError:
            # If conversion fails, fall back to original value
            return data
    
    # Special handling for date fields (YYYYMMDD format)
    if mapping_key == "HOME_PURCHASE_DATE":
        try:
            # Convert YYYYMMDD to readable date format
            if len(value_str) == 8 and value_str.isdigit():
                year = value_str[:4]
                month = value_str[4:6]
                day = value_str[6:8]
                
                # Convert month number to name
                month_names = {
                    "01": "January", "02": "February", "03": "March", "04": "April",
                    "05": "May", "06": "June", "07": "July", "08": "August",
                    "09": "September", "10": "October", "11": "November", "12": "December"
                }
                
                month_name = month_names.get(month, month)
                # Remove leading zero from day
                day_formatted = str(int(day))
                
                return f"{month_name} {day_formatted}, {year}"
            else:
                return data
        except (ValueError, IndexError):
            # If conversion fails, fall back to original value
            return data
    
    # Special handling for birth year and month fields (MMYYYY format)
    if mapping_key == "PERSON_BIRTH_YEAR_AND_MONTH":
        try:
            # Convert MMYYYY to readable date format
            if len(value_str) == 6 and value_str.isdigit():
                month = value_str[:2]
                year = value_str[2:]
                
                # Convert month number to name
                month_names = {
                    "01": "January", "02": "February", "03": "March", "04": "April",
                    "05": "May", "06": "June", "07": "July", "08": "August",
                    "09": "September", "10": "October", "11": "November", "12": "December"
                }
                
                month_name = month_names.get(month, month)
                return f"{month_name} {year}"
            else:
                return data
        except (ValueError, IndexError):
            # If conversion fails, fall back to original value
            return data
    
    # Special handling for mortgage term fields (format as months)
    if mapping_key in ["HOME_MORTGAGE_TERM", "INVESTMENT_PROPERTY_MORTGAGE_TERM"]:
        try:
            # Remove leading zeros and format as months
            numeric_value = int(value_str)
            return f"{numeric_value} months"
        except (ValueError, TypeError):
            # If conversion fails, fall back to original value
            return data
    
    # Get the mapping dictionary for coded values
    mapping_dict = VALUE_MAPPINGS.get(mapping_key, {})
    
    # Return mapped value or original if no mapping found
    mapped_value = mapping_dict.get(value_str, data)
    
    return mapped_value

def transform_response_data(data: Any, parent_field: str = "") -> Any:
    """
    Recursively transform response data by mapping both field names and values
    
    Args:
        data: The data structure to transform
        parent_field: The parent field name for context
        
    Returns:
        Fully transformed data with mapped field names and values
    """
    if isinstance(data, dict):
        transformed = {}
        for key, value in data.items():
            # First, transform nested objects
            if isinstance(value, (dict, list)):
                transformed_value = transform_response_data(value, key)
            else:
                # Map the field value using the field name as context
                transformed_value = map_field_values(value, key)
            
            transformed[key] = transformed_value
            
        return transformed
    
    elif isinstance(data, list):
        return [transform_response_data(item, parent_field) for item in data]
    
    else:
        # For leaf values, try to map using parent field context
        return map_field_values(data, parent_field)

def add_value_mapping(field_name: str, mapping_key: str, mappings: Dict[str, str]) -> None:
    """
    Add a new value mapping for a field
    
    Args:
        field_name: The display name of the field
        mapping_key: The key to use in VALUE_MAPPINGS dictionary
        mappings: Dictionary of code -> description mappings
    """
    VALUE_MAPPINGS[mapping_key] = mappings
    FIELD_TO_MAPPING_KEY[field_name] = mapping_key

def get_available_mappings() -> Dict[str, list]:
    """
    Get a summary of all available mappings
    
    Returns:
        Dictionary with mapping keys and their available codes
    """
    return {
        key: list(mapping.keys()) 
        for key, mapping in VALUE_MAPPINGS.items()
    }