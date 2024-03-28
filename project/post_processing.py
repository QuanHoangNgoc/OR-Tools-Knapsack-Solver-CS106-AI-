from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os, sys 


# Create a list of data for the table
# data:: list of list [[ , , ], [ , , ]] 
folder_path = 'D:\\cd_data_C\\Desktop\\run_stage\\running_output'
""" -------------------------------------------------------------------------------------------------------------------------
create main table (data) and sub table (data2) for report
""" 
data = []
data.append(["testcase", "Nitems", "value", "weight", "time", "optimal"])
data2 = [["testgroup", "total_time", "rate_optimal"]]
for name_file in os.listdir(folder_path): 
  # print(name_file) 
  total_time, rate_optiaml = 0, 0 
  file_path = os.path.join(folder_path, name_file) 
  with open(file_path, 'r') as file: # x13 
    for i in range(16): # x16
      line = file.readline()
      for s in [',', '(', ')', "'"]: line = line.replace(s, "") 
      words = line.split()
      value, weight = int(words[0]), int(words[1]) 
      number = int(words[2]) 
      time = float(words[3]) 
      time = round(time)
      # print("time = ", time) 
      optimal = words[4] 
      if(time <= 179): optimal = True
      else: optimal = False  
      testcase = str(words[5]) 
      testcase = testcase.replace("/kaggle/working/kplib", "")
      data.append([testcase, number, value, weight, time, optimal])
      total_time += time 
      if(optimal): rate_optiaml += 1 
  data2.append([name_file.replace(".txt", ""), total_time, rate_optiaml/16])
print(len(data)) 
print(len(data2)) 


# df 
import pandas as pd 
df = pd.DataFrame(data=data[1:], columns=data[0])
file = open('table.txt', 'w')
file.write(df.to_latex(index=False, longtable=True)) 

df2 = pd.DataFrame(data=data2[1:], columns=data2[0])
file = open('table2.txt', 'w')
file.write(df2.to_latex(index=False, longtable=True)) 


import random 
CREATE = True 
if(CREATE): 
  # Create a PDF document
  rdstr = str(random.randint(1, 100)) 
  pdf_filename = "table{}.pdf".format(rdstr)
  doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
  table = Table(data)

  # Add style to the table
  style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                      ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                      ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                      ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                      ('GRID', (0, 0), (-1, -1), 1, colors.black)])
  table.setStyle(style)

  # Add table to the PDF document
  elements = [table]
  doc.build(elements)

  print(f"PDF created: {pdf_filename}")