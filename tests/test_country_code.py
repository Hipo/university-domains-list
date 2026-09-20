import collections
import re
import unittest

from base_test import BaseUniversityTest

from iso_3166_countries import ISO_3166_ALPHA2_COUNTRIES


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
