import collections
import re
import unittest

from base_test import BaseUniversityTest

# Self-contained: this table and the check logic below are intentionally not
# shared with any other test file or with the AIOps reviewer script. It's
# used only as a tie-breaker for an (alpha_two_code, country) pairing that
# has no precedent elsewhere in the file (see test_country_matches_code).
# Sets list the ISO 3166-1 English short name plus common accepted variants,
# not every possible spelling.
ISO_3166_ALPHA2_COUNTRIES = {
    "AD": {"Andorra"},
    "AE": {"United Arab Emirates"},
    "AF": {"Afghanistan"},
    "AG": {"Antigua and Barbuda"},
    "AI": {"Anguilla"},
    "AL": {"Albania"},
    "AM": {"Armenia"},
    "AO": {"Angola"},
    "AQ": {"Antarctica"},
    "AR": {"Argentina"},
    "AS": {"American Samoa"},
    "AT": {"Austria"},
    "AU": {"Australia"},
    "AW": {"Aruba"},
    "AX": {"Åland Islands"},
    "AZ": {"Azerbaijan"},
    "BA": {"Bosnia and Herzegovina"},
    "BB": {"Barbados"},
    "BD": {"Bangladesh"},
    "BE": {"Belgium"},
    "BF": {"Burkina Faso"},
    "BG": {"Bulgaria"},
    "BH": {"Bahrain"},
    "BI": {"Burundi"},
    "BJ": {"Benin"},
    "BL": {"Saint Barthélemy"},
    "BM": {"Bermuda"},
    "BN": {"Brunei", "Brunei Darussalam"},
    "BO": {
        "Bolivia",
        "Plurinational State of Bolivia",
        "Bolivia, Plurinational State of",
    },
    "BQ": {"Bonaire, Sint Eustatius and Saba"},
    "BR": {"Brazil"},
    "BS": {"Bahamas"},
    "BT": {"Bhutan"},
    "BV": {"Bouvet Island"},
    "BW": {"Botswana"},
    "BY": {"Belarus"},
    "BZ": {"Belize"},
    "CA": {"Canada"},
    "CC": {"Cocos (Keeling) Islands"},
    "CD": {
        "Democratic Republic of the Congo",
        "DR Congo",
        "Congo, the Democratic Republic of the",
    },
    "CF": {"Central African Republic"},
    "CG": {"Congo", "Republic of the Congo"},
    "CH": {"Switzerland"},
    "CI": {"Côte d'Ivoire", "Ivory Coast", "Cote d'Ivoire"},
    "CK": {"Cook Islands"},
    "CL": {"Chile"},
    "CM": {"Cameroon"},
    "CN": {"China"},
    "CO": {"Colombia"},
    "CR": {"Costa Rica"},
    "CU": {"Cuba"},
    "CV": {"Cabo Verde", "Cape Verde"},
    "CW": {"Curaçao"},
    "CX": {"Christmas Island"},
    "CY": {"Cyprus"},
    "CZ": {"Czech Republic", "Czechia"},
    "DE": {"Germany"},
    "DJ": {"Djibouti"},
    "DK": {"Denmark"},
    "DM": {"Dominica"},
    "DO": {"Dominican Republic"},
    "DZ": {"Algeria"},
    "EC": {"Ecuador"},
    "EE": {"Estonia"},
    "EG": {"Egypt"},
    "EH": {"Western Sahara"},
    "ER": {"Eritrea"},
    "ES": {"Spain"},
    "ET": {"Ethiopia"},
    "FI": {"Finland"},
    "FJ": {"Fiji"},
    "FK": {"Falkland Islands"},
    "FM": {"Micronesia", "Federated States of Micronesia"},
    "FO": {"Faroe Islands"},
    "FR": {"France"},
    "GA": {"Gabon"},
    "GB": {"United Kingdom"},
    "GD": {"Grenada"},
    "GE": {"Georgia"},
    "GF": {"French Guiana"},
    "GG": {"Guernsey"},
    "GH": {"Ghana"},
    "GI": {"Gibraltar"},
    "GL": {"Greenland"},
    "GM": {"Gambia"},
    "GN": {"Guinea"},
    "GP": {"Guadeloupe"},
    "GQ": {"Equatorial Guinea"},
    "GR": {"Greece"},
    "GS": {"South Georgia and the South Sandwich Islands"},
    "GT": {"Guatemala"},
    "GU": {"Guam"},
    "GW": {"Guinea-Bissau"},
    "GY": {"Guyana"},
    "HK": {"Hong Kong"},
    "HM": {"Heard Island and McDonald Islands"},
    "HN": {"Honduras"},
    "HR": {"Croatia"},
    "HT": {"Haiti"},
    "HU": {"Hungary"},
    "ID": {"Indonesia"},
    "IE": {"Ireland"},
    "IL": {"Israel"},
    "IM": {"Isle of Man"},
    "IN": {"India"},
    "IO": {"British Indian Ocean Territory"},
    "IQ": {"Iraq"},
    "IR": {"Iran", "Islamic Republic of Iran"},
    "IS": {"Iceland"},
    "IT": {"Italy"},
    "JE": {"Jersey"},
    "JM": {"Jamaica"},
    "JO": {"Jordan"},
    "JP": {"Japan"},
    "KE": {"Kenya"},
    "KG": {"Kyrgyzstan"},
    "KH": {"Cambodia"},
    "KI": {"Kiribati"},
    "KM": {"Comoros"},
    "KN": {"Saint Kitts and Nevis"},
    "KP": {
        "North Korea",
        "Democratic People's Republic of Korea",
        "Korea, Democratic People's Republic of",
    },
    "KR": {"South Korea", "Republic of Korea", "Korea, Republic of"},
    "KW": {"Kuwait"},
    "KY": {"Cayman Islands"},
    "KZ": {"Kazakhstan"},
    "LA": {"Laos", "Lao People's Democratic Republic"},
    "LB": {"Lebanon"},
    "LC": {"Saint Lucia"},
    "LI": {"Liechtenstein"},
    "LK": {"Sri Lanka"},
    "LR": {"Liberia"},
    "LS": {"Lesotho"},
    "LT": {"Lithuania"},
    "LU": {"Luxembourg"},
    "LV": {"Latvia"},
    "LY": {"Libya"},
    "MA": {"Morocco"},
    "MC": {"Monaco"},
    "MD": {"Moldova", "Republic of Moldova", "Moldova, Republic of"},
    "ME": {"Montenegro"},
    "MF": {"Saint Martin"},
    "MG": {"Madagascar"},
    "MH": {"Marshall Islands"},
    "MK": {"North Macedonia", "Macedonia"},
    "ML": {"Mali"},
    "MM": {"Myanmar", "Burma"},
    "MN": {"Mongolia"},
    "MO": {"Macao"},
    "MP": {"Northern Mariana Islands"},
    "MQ": {"Martinique"},
    "MR": {"Mauritania"},
    "MS": {"Montserrat"},
    "MT": {"Malta"},
    "MU": {"Mauritius"},
    "MV": {"Maldives"},
    "MW": {"Malawi"},
    "MX": {"Mexico"},
    "MY": {"Malaysia"},
    "MZ": {"Mozambique"},
    "NA": {"Namibia"},
    "NC": {"New Caledonia"},
    "NE": {"Niger"},
    "NF": {"Norfolk Island"},
    "NG": {"Nigeria"},
    "NI": {"Nicaragua"},
    "NL": {"Netherlands"},
    "NO": {"Norway"},
    "NP": {"Nepal"},
    "NR": {"Nauru"},
    "NU": {"Niue"},
    "NZ": {"New Zealand"},
    "OM": {"Oman"},
    "PA": {"Panama"},
    "PE": {"Peru"},
    "PF": {"French Polynesia"},
    "PG": {"Papua New Guinea"},
    "PH": {"Philippines"},
    "PK": {"Pakistan"},
    "PL": {"Poland"},
    "PM": {"Saint Pierre and Miquelon"},
    "PN": {"Pitcairn"},
    "PR": {"Puerto Rico"},
    "PS": {"Palestine", "State of Palestine", "Palestine, State of"},
    "PT": {"Portugal"},
    "PW": {"Palau"},
    "PY": {"Paraguay"},
    "QA": {"Qatar"},
    "RE": {"Réunion"},
    "RO": {"Romania"},
    "RS": {"Serbia"},
    "RU": {"Russia", "Russian Federation"},
    "RW": {"Rwanda"},
    "SA": {"Saudi Arabia"},
    "SB": {"Solomon Islands"},
    "SC": {"Seychelles"},
    "SD": {"Sudan"},
    "SE": {"Sweden"},
    "SG": {"Singapore"},
    "SH": {"Saint Helena, Ascension and Tristan da Cunha"},
    "SI": {"Slovenia"},
    "SJ": {"Svalbard and Jan Mayen"},
    "SK": {"Slovakia"},
    "SL": {"Sierra Leone"},
    "SM": {"San Marino"},
    "SN": {"Senegal"},
    "SO": {"Somalia"},
    "SR": {"Suriname"},
    "SS": {"South Sudan"},
    "ST": {"Sao Tome and Principe"},
    "SV": {"El Salvador"},
    "SX": {"Sint Maarten"},
    "SY": {"Syria", "Syrian Arab Republic"},
    "SZ": {"Eswatini", "Swaziland"},
    "TC": {"Turks and Caicos Islands"},
    "TD": {"Chad"},
    "TF": {"French Southern Territories"},
    "TG": {"Togo"},
    "TH": {"Thailand"},
    "TJ": {"Tajikistan"},
    "TK": {"Tokelau"},
    "TL": {"Timor-Leste", "East Timor"},
    "TM": {"Turkmenistan"},
    "TN": {"Tunisia"},
    "TO": {"Tonga"},
    "TR": {"Turkey", "Türkiye", "Turkiye"},
    "TT": {"Trinidad and Tobago"},
    "TV": {"Tuvalu"},
    "TW": {"Taiwan", "Taiwan, Province of China"},
    "TZ": {"Tanzania", "United Republic of Tanzania", "Tanzania, United Republic of"},
    "UA": {"Ukraine"},
    "UG": {"Uganda"},
    "UM": {"United States Minor Outlying Islands"},
    "US": {"United States", "United States of America"},
    "UY": {"Uruguay"},
    "UZ": {"Uzbekistan"},
    "VA": {"Vatican City", "Holy See", "Holy See (Vatican City State)"},
    "VC": {"Saint Vincent and the Grenadines"},
    "VE": {
        "Venezuela",
        "Bolivarian Republic of Venezuela",
        "Venezuela, Bolivarian Republic of",
    },
    "VG": {"British Virgin Islands", "Virgin Islands, British"},
    "VI": {"United States Virgin Islands"},
    "VN": {"Vietnam", "Viet Nam"},
    "VU": {"Vanuatu"},
    "WF": {"Wallis and Futuna"},
    "WS": {"Samoa"},
    "YE": {"Yemen"},
    "YT": {"Mayotte"},
    "ZA": {"South Africa"},
    "ZM": {"Zambia"},
    "ZW": {"Zimbabwe"},
    # Not an official ISO 3166-1 code, but a widely used user-assigned one
    # for Kosovo (already present in this dataset).
    "XK": {"Kosovo"},
}


class CountryCodeTests(BaseUniversityTest):
    def test_country_matches_code(self):
        """Test that alpha_two_code and country agree with each other.

        An entry's (alpha_two_code, country) pairing is accepted if either:
        - another entry in the file already uses that exact pairing (this
          dataset's own established convention for that code), or
        - no other pairing exists yet for that code and this one matches
          the ISO 3166-1 name (or a known variant) for it.
        This flags an actual mismatch (e.g. the wrong code copy-pasted onto
        a country, or vice versa) without fighting real spelling variance
        the dataset already tolerates for a given code.
        """
        entries = self.valid_json
        pair_counts = collections.Counter()
        countries_by_code = collections.defaultdict(set)
        for university in entries:
            code, country = university.get("alpha_two_code"), university.get("country")
            if code and country:
                pair_counts[(code, country)] += 1
                countries_by_code[code].add(country)

        errors = []
        for i, university in enumerate(entries):
            code, country = university.get("alpha_two_code"), university.get("country")
            if not code or not country:
                continue
            if not re.fullmatch(r"[A-Z]{2}", code):
                errors.append(
                    f"Entry {i} ({university.get('name')}): "
                    f"alpha_two_code '{code}' is not a two-letter uppercase code"
                )
                continue
            if pair_counts[(code, country)] > 1:
                continue  # an established pairing elsewhere in the file
            if len(countries_by_code[code]) == 1:
                # only pairing ever used for this code — check it against
                # the ISO table instead of accepting it unconditionally
                canonical = ISO_3166_ALPHA2_COUNTRIES.get(code)
                if canonical is None or country in canonical:
                    continue
            errors.append(
                f"Entry {i} ({university.get('name')}): alpha_two_code "
                f"'{code}' does not match country '{country}'"
            )

        if errors:
            error_message = (
                f"Found {len(errors)} country/code mismatches:\n"
                + "\n".join(errors[:10])
            )
            if len(errors) > 10:
                error_message += f"\n... and {len(errors) - 10} more errors"
            self.fail(error_message)


if __name__ == "__main__":
    unittest.main()
