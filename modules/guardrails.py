import re
from typing import Tuple

class SQLGuardrails:
    """
    Security validation engine to ensure generated SQL queries are safe,
    read-only SELECT statements without destructive operations or multi-statement injections.
    """
    FORBIDDEN_KEYWORDS = {
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", 
        "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "COPY"
    }

    @classmethod
    def validate_sql(cls, sql_query: str) -> Tuple[bool, str]:
        """
        Validates the SQL query against read-only safety criteria.
        Returns: (is_safe, error_or_reason)
        """
        clean_sql = sql_query.strip()
        if not clean_sql:
            return False, "Empty SQL query."

        # Remove trailing semicolon for multi-statement checks
        if clean_sql.endswith(";"):
            clean_sql = clean_sql[:-1].strip()

        # Reject multi-statement queries
        if ";" in clean_sql:
            return False, "Security Violation: Multi-statement queries containing multiple semicolons are forbidden."

        # Extract tokens/words using regex
        tokens = set(re.findall(r"\b[A-Za-z_]+\b", clean_sql.upper()))

        # Enforce SELECT-only start
        first_word = clean_sql.split()[0].upper()
        if first_word != "SELECT" and not clean_sql.upper().startswith("WITH"):
            return False, f"Security Violation: Query must begin with 'SELECT' or 'WITH'. Got '{first_word}'."

        # Check for forbidden mutation keywords
        found_forbidden = tokens.intersection(cls.FORBIDDEN_KEYWORDS)
        if found_forbidden:
            return False, f"Security Violation: Query contains forbidden mutation keywords: {list(found_forbidden)}"

        return True, "SQL safety check passed."


if __name__ == "__main__":
    print("SQLGuardrails module ready.")