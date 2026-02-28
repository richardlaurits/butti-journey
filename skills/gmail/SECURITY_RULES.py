"""
SECURITY RULES - ButtiBot Gmail Access

This file enforces strict security rules around email accounts.
Never bypass these checks.
"""

# Allowed sending accounts (can use SMTP)
ALLOWED_SEND_FROM = [
    "butti.nightrider@gmail.com",
]

# Read-only accounts (IMAP only, NO SMTP)
READ_ONLY_ACCOUNTS = [
    "richardlaurits@gmail.com",
]

def check_smtp_permission(email_address):
    """
    Check if an email account is allowed to send via SMTP.
    
    Args:
        email_address (str): Email to check
        
    Returns:
        bool: True if allowed, False otherwise
        
    Raises:
        PermissionError: If account is read-only
    """
    
    if email_address in READ_ONLY_ACCOUNTS:
        raise PermissionError(
            f"❌ SMTP blocked for {email_address}\n"
            f"   This account is READ-ONLY (IMAP only)\n"
            f"   Security rule enforced: Cannot send emails from Richard's personal account"
        )
    
    if email_address not in ALLOWED_SEND_FROM:
        raise PermissionError(
            f"❌ SMTP not configured for {email_address}\n"
            f"   Allowed accounts: {', '.join(ALLOWED_SEND_FROM)}"
        )
    
    return True


def check_imap_permission(email_address):
    """
    Check if an email account is allowed to read via IMAP.
    All accounts are readable.
    """
    return True


# Example usage in send_email():
"""
def send_email(from_email, to_email, subject, body):
    # Check permissions FIRST
    check_smtp_permission(from_email)
    
    # Only then proceed with SMTP
    smtp = smtplib.SMTP_SSL('smtp.gmail.com')
    ...
"""
