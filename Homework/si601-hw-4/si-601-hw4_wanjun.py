import sqlite3,urllib2,json,re

#step1
url = "https://mcommunity-beta.dsc.umich.edu/miPeople/services/person/search.json"
data = {"searchCriteria":{"givenNameSearchType":"starts with","snSearchType":"starts with",
                    "uniqnameSearchType":"is equal","emailSearchType":"is equal",
                    "titleSearchType":"starts with","affiliationSearchType":"starts with",
                    "phoneSearchType":"ends with","cnSearchType":"starts with",
                    "ownerSearchType":"is equal","title":"Arthur F Thurnau Professor","searchForm":"People"}}
json_data = json.dumps(data)
request = urllib2.Request(url, json_data, {'Content-Type': 'application/json', 'Content-Length': len(json_data)})
search_results = urllib2.urlopen(request).read()
results = search_results[28:(len(search_results)-3)]
match_results = results.split('},')
final_results = []

for i in range((len(match_results)-1)):
    final_results.append(match_results[i]+'}')

final_results.append(match_results[len(match_results)-1])

profs = []
affis = []
prafs = []
for i in range(len(final_results)):
    line_json = json.loads(final_results[i])
    s_prof = [str(line_json['uniqname'].encode('utf-8')),str(line_json['displayName'].encode('utf-8')),
              str(line_json['title'][0].encode('utf-8'))]
    profs.append(s_prof)
    s_affi = line_json['affiliation']
    for i in range(len(s_affi)):
        s_affi[i] = s_affi[i].encode('utf-8')#.replace(' - Faculty and Staff','')
        prof_affi = [s_prof[0],s_affi[i]]
        prafs.append(prof_affi)
        s_affi[i] = [s_affi[i]]
    affis.extend(s_affi)

#step2 and step3
conn = sqlite3.connect('si-601-hw4_wanjun.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS professor
             (uniqname VARCHAR(100),
              name VARCHAR(100),
              title TEXT)''')
cur.executemany("INSERT INTO professor VALUES (?,?,?)", profs)
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS affiliation
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                description VARCHAR(200),
                UNIQUE(description))''')

cur.executemany("INSERT OR IGNORE INTO affiliation (description) VALUES (?)",affis)
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS praf
               (uniqname VARCHAR(100),
                description VARCHAR(200))''')
cur.executemany("INSERT INTO praf VALUES (?,?)",prafs)
conn.commit()
#step4 and step5
cur.execute('''CREATE TABLE IF NOT EXISTS professor_affiliation
               (uniqname VARCHAR(100),
                id INTEGER)''')
cur.execute('''INSERT INTO professor_affiliation
               SELECT p.uniqname, a.id FROM praf p LEFT JOIN affiliation a ON p.description=a.description''')
conn.commit()
#step6
cur.execute("SELECT description FROM affiliation")
affis_db = cur.fetchall()
affis_ls = []
for affi in affis_db:
    affis_ls.append(list(affi)[0].encode('utf-8'))

dep_col = dict()
for aff in affis_ls:
    if (re.findall(r'^LSA', aff)):
        dep_col[aff] = 'College of Lit, Science & Arts - Faculty and Staff'
    elif (re.findall(r'^CoE',aff)):
        dep_col[aff] = 'College of Engineering - Faculty and Staff'
    elif (re.findall(r'^COE',aff)):
        dep_col[aff] = 'College of Engineering - Faculty and Staff'
    else:
        continue

dep_col['UMH MCIT CIO Administration - Sponsored Affiliate'] = 'UMH MCIT CIO Administration - Sponsored Affiliate'
dep_col['Mechanical Engineering - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Industrial & Operations Engin - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['EECS - CSE Division - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Chemical Engineering Dept - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Materials Science & Engin. - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Civil & Environmental Engr - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Aerospace Engineering - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Nuclear Eng & Radiological Sci - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Biomedical Engineering - Faculty and Staff'] = 'College of Engineering - Faculty and Staff'
dep_col['Health Management and Policy - Faculty and Staff'] = 'School of Public Health - Faculty and Staff'
dep_col['G. Ford Sc Pub Pol - Faculty and Staff'] = 'Ford School of Public Policy - Faculty and Staff'
dep_col['Vice President for Research - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['VP Academic & Graduate Study - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['VP Global Engmt & Intrdspl AA - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['VProv_Global_Engmt_Intrdspl_AA - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['VP Academic & Graduate Study - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['Ofc Provost & Exec VP Acad Aff - Faculty and Staff'] = 'Vice president - Faculty and Staff'
dep_col['Inst/Research Women & Gender - Faculty and Staff'] = 'Inst/Research Women & Gender - Faculty and Staff'
dep_col['SOE-Educational Studies - Faculty and Staff'] = 'School of Education - Faculty and Staff'
dep_col['Microbiology and Immunology - Faculty and Staff'] = 'Medical School - Faculty and Staff'
dep_col['School of Information - Faculty and Staff'] = 'School of Information - Faculty and Staff'
dep_col['Ross School of Business - Faculty and Staff'] = 'Ross School of Business - Faculty and Staff'
dep_col['Michigan Society of Fellows - Faculty and Staff'] = 'Rackham Graduate School - Faculty and Staff'
dep_col['School of Music - Faculty and Staff'] = 'School of Music,Theatre&Dance - Faculty and Staff'
dep_col['SMTD Department of Dance - Faculty and Staff'] = 'School of Music,Theatre&Dance - Faculty and Staff'
dep_col['Stamps School of Art & Design - Faculty and Staff'] = 'Stamps School of Art & Design - Faculty and Staff'
dep_col['Library Dean - General - Faculty and Staff'] = 'University Library - Faculty and Staff'
dep_col['Bentley Historical Library - Faculty and Staff'] = 'University Library - Faculty and Staff'
dep_col['School of Social Work - Faculty and Staff'] = 'School of Social Work - Faculty and Staff'
dep_col['A. Alfred Taubman CA&UP - Faculty and Staff'] = 'Coll of Arch & Urban Planning - Faculty and Staff'
dep_col['School of Kinesiology - Faculty and Staff'] = 'School of Kinesiology - Faculty and Staff'
dep_col['Law School - Faculty and Staff'] = 'Law School - Faculty and Staff'
dep_col['Office of Research - Faculty and Staff'] = 'Office of Research - Faculty and Staff'
dep_col['RCGD-Rsrch Cntr for Grp Dyn - Faculty and Staff'] = 'Institute for Social Research - Faculty and Staff'
dep_col['SRC - Education & Well Being - Faculty and Staff'] = 'Institute for Social Research - Faculty and Staff'
dep_col['MI Nanotechnology Institute - Faculty and Staff'] = 'MI Nanotechnology Institute - Faculty and Staff'

depa_coll = []
for key, value in dep_col.iteritems():
    depa_coll.append([str(key),str(value)])

cur.execute('''CREATE TABLE IF NOT EXISTS department_college
            (department VARCHAR(200),
             college VARCHAR(200))''')
cur.executemany("INSERT INTO department_college VALUES (?,?)",depa_coll)
conn.commit()

cur.execute('''SELECT p.description, count(p.description),d.college
               FROM praf p JOIN department_college d ON p.description=d.department
               GROUP BY d.college,p.description
               ORDER BY d.college,count(p.description) DESC''')
num_in_dep = cur.fetchall()
#step 7 After eliminated the college and the school, the result will be the professors affiliated to departments.
#So if the professor was cross affiliated to departments, the professor will be affiliated to multiple departments(>1)
cur.execute('''SELECT count(uni) FROM
              (SELECT pa.uniqname AS uni
               FROM professor_affiliation pa
               LEFT JOIN affiliation a ON pa.id=a.id
               JOIN department_college d ON a.description=d.department
               GROUP BY pa.uniqname
               HAVING count(pa.uniqname)>1)''')
num_multi = cur.fetchall()
num_multi = num_multi[0]
num_multi = num_multi[0]
#Notice that there is a professor who affiliated directly to two schools rather than departments. So the number should increase by 1.
num_multi += 1
print "The number of Thurnau professors cross-appointed to multiple departments is "+str(num_multi)

cur.execute("DROP TABLE IF EXISTS praf")
conn.commit()
cur.execute("DROP TABLE IF EXISTS department_college")
conn.commit()