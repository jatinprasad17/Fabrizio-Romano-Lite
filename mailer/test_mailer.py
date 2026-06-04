from smtp import send_transfer_email

analysis = """
1. Enzo Fernandez, Chelsea → Manchester City, Rumour, £100m+, 8/10
2. Bernardo Silva, Manchester City → Exit, Confirmed, 10/10
3. Savinho, Manchester City → Tottenham, Rumour, 6/10
"""

send_transfer_email(
    to_email="b22266@students.iitmandi.ac.in",
    team="Manchester City",
    analysis=analysis
)