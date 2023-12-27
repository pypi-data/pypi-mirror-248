from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import email
import imaplib
import os
import subprocess
import argparse
import psycopg2

globals()
kastleUser = ""
kastlePass = ""
kastleReportMail = ""
kastleFromMail = "mykastleadmin@kastle.com"

postgresIp = ""
postgresPort = ""
postgresUser = ""
postgresPassword = ""
postgresDb = ""
postgresTable = "reader_activity"
userName = 'test'
passwd = 'wrongfpfujywsqsxbcnkj'
detach_dir = '.'
driver = ""
url = "https://www.mykastle.com"
default_timeout = 60 #seconds
xpath_values = \
    {
        "email": "//input[@placeholder='Please Enter Email Address']",
        "next": "//input[@type='submit' and @value='Next']",
        "password": "//input[@placeholder='Password']",
        "login": "//input[@type='submit' and @value='Log In']",
        "goto_reports_link": "//a[@id='gotoReportsLink'][text()='Go to Reports']",
        "reader_activity_report_yesterday": "//li//div[span='Reader Activity Report']//following-sibling::div//a[text()='Yesterday']",
        "report_mail": "//div[@class='toolbar']//a[@title='Mail' and text() ='Mail']",
        "send_email": "//div[@id='dvEmailReport']//input[@id='txtEmailId']",
        "send": "//div[@id='dvEmailReport']//input[@type='button' and @value = 'Send']",
        #"table_date": "//table//th[div='Date and Time']"
        "table_date": "//div[contains(@class,'border-bottom-gray')][contains(@class,'hDivBox')]//table//th[div='Date and Time']"
    }

def get_element(xpath_string):
    print(xpath_string)
    elem = WebDriverWait(driver, default_timeout).until(EC.presence_of_element_located((By.XPATH, xpath_string)))
    return elem

def connect_postgres():
    conn_details = psycopg2.connect(host=postgresIp, database=postgresDb, user=postgresUser, password=postgresPassword,
                                    port=postgresPort)
    return conn_details

def deleteTable(conn_details, table):
    cursor = conn_details.cursor()
    delete_tbl_data = "TRUNCATE {};".format(table)
    cursor.execute(delete_tbl_data)
    delete_tbl_data = "DELETE FROM {};".format(table)
    cursor.execute(delete_tbl_data)
    conn_details.commit()
    print("Delete all records")


def updatePostgres(conn_details, csv_path, table, fields):
    cursor = conn_details.cursor()
    f = open(csv_path)
    fields = fields.split(",")
    sql_query = f"""COPY {table} ({','.join(fields)}) FROM STDIN WITH (FORMAT CSV)"""
    print(sql_query)
    cursor.copy_expert(sql_query, f)
    conn_details.commit()
    print("Update new records")

def gmail_login():
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    print("username {}".format(userName))
    typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print('Not able to sign in!')
        print(typ)
        return False
    else:
        print("login success")
    imapSession.select('Inbox')
    return imapSession

def gmail_delete(imapSession):
    typ, data = imapSession.search(None, '(FROM "mykastleadmin@kastle.com")')
    for num in data[0].split():
        imapSession.store(num, '+FLAGS', '\\Deleted')
    return True

def gmail_get_attachment(imapSession):
    retry_count = 1
    while(retry_count<=10):
        imapSession.select('Inbox')
        typ, data = imapSession.search(None, '(FROM "mykastleadmin@kastle.com")')
        if typ != 'OK':
            print('Error searching Inbox.')
            print(typ)
            return False
        else:
            print("Inbox selected")
        if (len(data[0].split()) > 0):
            print("Email received. Attempt {}/10".format(retry_count))
            break
        else:
            print("Email not received yet. Wait 1 min and retry.")
            print(len(data[0].split()))
            retry_count+=1
            time.sleep(60)

    msgId = data[0].split()[-1]
    typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
    if typ != 'OK':
        print('Error fetching mail.')
        print(typ)
        return False
    else:
        print("Mail fetched")

    emailBody = messageParts[0][1]
    print("emailBody fetched")
    mail = email.message_from_string(emailBody.decode('utf-8'))
    for part in mail.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(detach_dir, 'DataFiles', fileName)
            print(filePath)
            if not os.path.isfile(filePath) :
                print(fileName)
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    return filePath




def data_parser(kastleuser, kastlepassword, kastlefrommail, postgresip, postgresport, postgresuser, postgrespassword, database, emailaddress, emailpassword):
    print(globals()['userName'])
    globals()['kastleUser'] = kastleuser
    globals()['kastlePass'] = kastlepassword
    globals()['postgresPort'] = postgresport
    globals()['postgresIp'] = postgresip
    globals()['postgresUser'] = postgresuser
    globals()['postgresPassword'] = postgrespassword
    globals()['postgresDb'] = database
    globals()['userName'] = emailaddress
    globals()['passwd'] = emailpassword
    globals()['kastleReportMail'] = emailaddress
    globals()['kastleFromMail'] = kastlefrommail


    if 'DataFiles' not in os.listdir(detach_dir):
        os.mkdir('DataFiles')

    imapSession = gmail_login()

    gmail_delete(imapSession)

    svc = webdriver.ChromeService(executable_path=binary_path)
    chrome_options = Options()
    #chrome_options.add_argument("--headless=new")  # for Chrome >= 109
    #chrome_options.add_argument("--no-sandbox")  # for Chrome >= 109
    #chrome_options.add_argument("--disable-gpu")  # for Chrome >= 109
    #driver = webdriver.Chrome(options=chrome_options)
    globals()['driver'] = webdriver.Chrome(service=svc, options=chrome_options)
    print(xpath_values["email"])
    start_url = url
    driver.get(start_url)
    username_element = get_element(xpath_values["email"])
    username_element.send_keys(kastleUser)
    next_element = get_element(xpath_values["next"])
    next_element.click()
    password_element = get_element(xpath_values["password"])
    password_element.send_keys(kastlePass)
    login_element = get_element(xpath_values["login"])
    login_element.click()
    gotoreport_element = get_element(xpath_values["goto_reports_link"])
    gotoreport_element.click()
    time.sleep(30)
    yesterday_element = get_element(xpath_values["reader_activity_report_yesterday"])
    yesterday_element.click()
    print("sday clicked")
    time.sleep(60)
    date_element = get_element(xpath_values["table_date"])
    time.sleep(30)
    print("Table populated")
    mail_element = get_element(xpath_values["report_mail"])
    mail_element.click()
    print("report mail clicked")
    rmail_element = get_element(xpath_values["send_email"])
    rmail_element.clear()
    rmail_element.send_keys(kastleReportMail)
    send_element = get_element(xpath_values["send"])
    send_element.click()
    time.sleep(30)
    driver.quit()

    filePath = gmail_get_attachment(imapSession)
    imapSession.close()
    imapSession.logout()

    conn = connect_postgres()
    deleteTable(conn, postgresTable)
    fields = "dateandtime,personnelname,cardnumber,lockoutreason,companyname,reader"
    updatePostgres(conn, filePath, table=postgresTable, fields=fields)
    conn.close()

