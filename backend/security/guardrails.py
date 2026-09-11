import re

FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", 
    "GRANT", "REVOKE", "EXEC", "CREATE", "RENAME"
]

def validate_sql_safety(sql: str) -> tuple[bool, str]:
    """
    Validates that generated SQL is strictly a read-only SELECT or WITH statement.
    """
    clean_sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE).strip().upper()
    
    if not (clean_sql.startswith("SELECT") or clean_sql.startswith("WITH")):
        return False, "Query violation: Only SELECT or WITH statements are allowed."
        
    for word in FORBIDDEN_KEYWORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, clean_sql):
            return False, f"Security violation: Detected forbidden SQL keyword '{word}'."
            
    return True, "Query passed security validation."