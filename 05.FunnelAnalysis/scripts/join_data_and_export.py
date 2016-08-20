from rds_connections import *

outF = open("/projects/DSTakeHomeChallenges/05.FunnelAnalysis/processing/joined_table.csv", "w")
outF.write(",".join(["UserID", "Date", "Device", "Sex", "HomePage", "SearchPage", "PaymentPage", "ConfirmationPage"]) + "\n")
with CONN.cursor() as cur:
    cur.execute(
            ("SELECT User.UserID, User.Date, User.Device, User.Sex, HomePage.HomePage, SearchPage.SearchPage, PaymentPage.PaymentPage, ConfirmationPage.ConfirmationPage "
                 "FROM User "
                 "LEFT JOIN HomePage ON User.UserID = HomePage.UserID "
                 "LEFT JOIN SearchPage ON User.UserID = SearchPage.UserID "
                 "LEFT JOIN PaymentPage ON User.UserID = PaymentPage.UserID "
                 "LEFT JOIN ConfirmationPage ON User.UserID = ConfirmationPage.UserID ")
    )
    for row in cur:
        outF.write(",".join([str(s) for s in row]) + '\n')
