import csv
import re
import dns.resolver
import socket
import smtplib

input_file = open("test_list.csv", "r").readlines()
with open("Final_file.csv", "w") as contact:
  employee_writer = csv.writer(contact, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  print(len(input_file))
  csv_reader = csv.reader(input_file)
  regex = re.compile(
    r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$')
  try:
    for line_count, row in enumerate(csv_reader, 1):
      print('Checking {0} of {1}'.format(line_count, len(input_file)))
      # Don't make a set out of this
      fname = row[0]
      lname = row[1]
      # Don't make a list out of this; trim spaces
      email = row[2].strip()
      print(email)
      print('Checking contact name {}'.format(fname))
      match = regex.match(email)
      if match is None:
        print("Bad Email")
        employee_writer.writerow([fname, lname, email, 'Invalid Email'])
      else:
        try:
          splitAddress = email.split('@')
          domain = str(splitAddress[1])
          records = dns.resolver.query(domain, 'MX')
          mxRecord = records[0].exchange
          mxRecord = str(mxRecord)
          server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
          server.set_debuglevel(1)
          server.starttls()
          server.login('bhanukrsingh@outlook.com', 'Vaishali@1')
          server.connect(mxRecord)
          server.ehlo('gmail.com')
          print(repr(email))
          server.mail('bhanukrsingh@outlook.com')
          server.rcpt(email)
          code, message = server.rcpt(str(email))
          server.quit()
          if code == 250:
            print('Success smpt mail')
            employee_writer.writerow([fname, lname, email, 'Valid Email'])
            print('')
          elif code == 550:
            print('usernmae does not exist')
          else:
            print('Bad smpt mail')
          print("Good Email")
          print(mxRecord)
          print('')
          print('')
          print('')
          print('')
        except Exception as e:
          print(e)
          print("Bad Domain")
          employee_writer.writerow([fname, lname, email, 'Invalid Domain / Marked Sphamous'])
  except IndexError as error:
    print('')
    print('')
    print('')
    print('###################################')
