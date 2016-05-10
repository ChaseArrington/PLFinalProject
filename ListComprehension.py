s_emp = (('ID', 'LAST_NAME', 'FIRST_NAME', 'USERID', 'START_DATE', 'COMMENTS', 'TITLE', 'SALARY', 'COMMISSION', 'DEPT_ID', 'MANAGER_ID'),
         (1, 'Martin', 'Carmen', 'martincu', '3-Mar-90', '', 'President', 4500, '', 50, ''),
         (10, 'Jackson', 'Marta', 'jacksomt', '27-Feb-91', '', 'Warehouse Manager', 1507, '', 45, 2),
         (11, 'Henderson', 'Colin', 'hendercs', '14-May-90', '', 'Sales Representative', 1400, 10, 31, 3),
         (12, 'Gilson', 'Sam', 'gilsonsj', '18-Jan-92', '', 'Sales Representative', 1490, 12.5, 32, 3),
         (13, 'Sanders', 'Jason', 'sanderjk', '18-Feb-91', '', 'Sales Representative', 1515, 10, 33, 3),
         (14, 'Dameron', 'Andre', 'dameroap', '9-Oct-91', '', 'Sales Representative', 1450, 17.5, 35, 3),
         (15, 'Hardwick', 'Elaine', 'hardwiem', '7-Feb-92', '', 'Stock Clerk', 1400, '', 41, 6),
         (16, 'Brown', 'George', 'browngw', '8-Mar-90', '', 'Stock Clerk', 940,'' , 41, 6),
         (17, 'Washington', 'Thomas', 'washintl', '9-Feb-91', '', 'Stock Clerk', 1200,'' , 42, 7),
         (18, 'Patterson', 'Donald', 'patterdv', '6-Aug-91', '', 'Stock Clerk', 795, '', 42, 7),
         (19, 'Bell', 'Alexander', 'bellag', '26-May-91', '', 'Stock Clerk', 850, '', 43, 8),
         (2, 'Smith', 'Doris', 'smithdj', '8-Mar-90', '', 'VP, Operations', 2450, '', 41, 1),
         (20, 'Gantos', 'Eddie', 'gantosej', '30-Nov-90', '', 'Stock Clerk', 800, '', 44, 9),
         (21, 'Stephenson', 'Blaine', 'stephebs', '17-Mar-91', '', 'Stock Clerk', 860, '', 45, 10),
         (22, 'Chester', 'Eddie', 'chesteek', '30-Nov-90', '', 'Stock Clerk', 800, '', 44, 9),
         (23, 'Pearl', 'Roger', 'pearlrg', '17-Oct-90', '', 'Stock Clerk', 795, '', 34, 9),
         (24, 'Dancer', 'Bonnie', 'dancerbw', '17-Mar-91', '', 'Stock Clerk', 860, '', 45, 7),
         (25, 'Schmitt', 'Sandra', 'schmitss', '9-May-91', '', 'Stock Clerk', 1100, '', 45, 8),
         (3, 'Norton', 'Michael', 'nortonma', '17-Jun-91', '', 'VP, Sales', 2400, '', 31, 1),
         (4, 'Quentin', 'Mark', 'quentiml', '7-Apr-90', '', 'VP, Finance', 2450, '', 10, 1),
         (5, 'Roper', 'Joseph', 'roperjm', '4-Mar-90', '', 'VP, Administration', 2550, '', 50, 1),
         (6, 'Brown', 'Molly', 'brownmr', '18-Jan-91', '', 'Warehouse Manager', 1600, '', 41, 2),
         (7, 'Hawkins', 'Roberta', 'hawkinrt', '14-May-90', '', 'Warehouse Manager', 1650, '', 42, 2),
         (8, 'Burns', 'Ben', 'burnsba', '7-Apr-90', '', 'Warehouse Manager', 1500, '', 43, 2),
         (9, 'Catskill', 'Antoinette', 'catskiaw', '9-Feb-92', '', 'Warehouse Manager', 1700, '', 44, 2))

s_dept = (('ID', 'NAME', 'REGION_ID'),
          (10, 'Finance', 1),
          (31, 'Sales', 1),
          (32, 'Sales', 2),
          (33, 'Sales', 3),
          (34, 'Sales', 4),
          (35, 'Sales', 5),
          (41, 'Operations', 1),
          (42, 'Operations', 2),
          (43, 'Operations', 3),
          (44, 'Operations', 4),
          (45, 'Operations', 5),
          (50, 'Administration', 1))


print '\nselect * from s_dept: ', s_dept

print '\nselect last_name, first_name, title, salary from s_emp: ', [[i[1], i[2], i[6], i[7]] for i in s_emp[1::]]

print '\nselect last_name, first_name, title, salary from s_emp where salary > 1500 and dept_id > 40: ', [[i[1], i[2], i[6], i[7]] for i in s_emp[1::] if i[7] > 1500 and i[9] > 40]

print '\nselect last_name, first_name, title, salary from s_emp where salary > 1500 and dept_id > 40 order by last_name: ', sorted([[i[1], i[2], i[6], i[7]] for i in s_emp[1::] if i[7] > 1500 and i[9] > 40], key = lambda x: x[0])

print '\nselect last_name, first_name, title, salary from s_emp where salary > 1500 and dept_id > 40 order by salary desc: ', sorted([[i[1], i[2], i[6], i[7]] for i in s_emp[1::] if i[7] > 1500 and i[9] > 40], key = lambda x: x[3], reverse = True)

print '\nselect last_name, first_name, title, salary, name from s_emp e join s_dept d on(e.dept_id = d.id): ', [[i[1], i[2], i[6], i[7], j[1]] for i in s_emp[1::] for j in s_dept[1::] if i[9] == j[0]]

print '\nselect dept_id, avg(salary) from s_emp group by dept_id order by dept_id: '
llist = []
for department in { d[9] for d in s_emp[1::] }: llist.append([department, (lambda l: round(sum(l) / len(l), 2))(map(float,[e[7] for e in s_emp[1::] if e[9] == department]))])
print sorted(llist, key = lambda x: x[0])

print '\nselect dept_id, avg(salary) from s_emp group by dept_id having avg(salary) < 1500;'
for department in { d[9] for d in s_emp[1::] }: print (lambda dept_id, avgSal: (dept_id, avgSal) if avgSal <1500 else "")(department, (lambda l: round(sum(l) / len(l), 2))(map(float,[ e[7] for e in s_emp[1::] if e[9] == department ])))