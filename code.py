

import sqlite3, os, time
from datetime import date
import sys
import re
import getpass
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return
def change_upper(string):
    if string:
        return string.upper()
    else:
        return string
def input_birth(can_be_none = False):
    while True:
        try:
            bdate = input("Please input date (it should be like yyyy-mm-dd)-> ")
            bdate_result = bdate
            if (can_be_none ==  True):
                if (bdate == ""):
                    print("You entered nothing for date")
                    break
            assert len(bdate) == 10,"Please double check your input format"
            assert bdate[4] == "-","Please double check your input format"
            assert bdate[7] == "-","Please double check your input format"
            assert int(bdate[:4]),"Please double check your input format"
            assert int(bdate[5:7]),"Please double check your input format"
            assert int(bdate[8:10]),"Please double check your input format"
            assert str(bdate) <= str(date.today()),"You can't have a date later than today"
            bdate = bdate.split("-")
            for i in range(len(bdate)):
                bdate[i] = int(bdate[i])
            birth_year, birth_month, birth_day = bdate[0], bdate[1], bdate[2]
            if (1 <= birth_month <= 12):
        
                if (birth_month in (1,3,5,7,8,10,12) and (birth_day > 31 or birth_day < 1)):
               
                    raise AssertionError("Your day should between 1 and 31 in months 1, 3, 5, 7, 8, 10, 12")
                if (birth_month in (4,6,9,11) and (birth_day > 30 or birth_day < 1)):
                 
                    raise AssertionError("Your day should between 1 and 30 in months 4, 6, 9, 11")
                if (birth_month == 2):
                    if (((birth_year % 4 == 0) and (birth_year % 100 != 0)) or (birth_year % 400 == 0)) :
                        if (birth_day > 29 or birth_day < 1):
                            raise AssertionError("day should between 1 and 29")
                    else:
                        if (Day > 28 or Day < 0):
                            raise AssertionError("day should between 1 and 28")
            else:
                raise AssertionError("The month should between 1 and 12")     
        except AssertionError as e:
            print(e)
        except ValueError:
            print("Should be integer")
        else:   
            return bdate_result  
def reg_birth():
    '''
    register a birth. agent should be able to register a birth by providing the first name,
    the last name, the gender, birth date, the birth place of the newborn, as well as the first
    and last name of the parents.
    The registration date is set to the day of registration(today) and registration place is 
    set to those of the mother. 
    If any of the parents is not in the database, the system should get information about the 
    parents including first name, last name, birth date, birth place, address and phone.
    For each parent, any column other than the first name and last name can be null if it is
    not provided.
    '''
    '''
    first_name,last_name,gender,birth_date,birth_of_place,first and last name of the parents
    '''
    global connection,cursor
    print("-"*40)
    print("Register a birth")
    print("-"*40)
    while True:
        try:
            # input firstname
            fname = input("Please input first name -> ")
            assert re.match("^[A-Za-z]*$",fname),"the input should not be anything other than basic letters"
            assert 12 >= len(fname) > 0,"The length of the firstname should between 1 and 12"
            
            # input lastname
            lname = input("Please input last name -> ")
            assert re.match("^[A-Za-z]*$",lname),"the input should not be anything other than basic letters"
            assert 12 >= len(lname) > 0,"The length of the lastname should between 1 and 12"
            cursor.execute("select fname,lname from persons where up(fname) = up(?) and up(lname) = up(?)",(fname, lname))
            assert cursor.fetchone() == None,"We already have this birth's name in our record" 
            # input gender
            gender = input("Please input gender -> ")
            assert gender.upper() in ["M","F"],"gender is either M or F"
            bdate = input_birth()

            bplace = input("Please input the birth place -> ")
            assert re.match("^[A-Za-z, ]*$", bplace),"only English characters and space and comma are allowed"
      
            
            f_fname = input("Please input father's firstname ")
            assert 0 < len(f_fname) <= 12,"The firstname length should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", f_fname),\
                           "There exists characters outside A-Z a-z"            
            f_lname = input("Please input father's lastname ")
            assert 0 < len(f_lname) <= 12,"The lastname length should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", f_lname),\
                           "There exists characters outside A-Z a-z" 
            
            cursor.execute("select fname, lname from persons where up(fname) = up(?) and up(lname) = up(?);",(f_fname,f_lname))
            if cursor.fetchone() == None:
                print("Father's information is not in the database, we need information of father")
                while True:
                    try:
                        # input firstname
                        f_fname = input("Please input father's firstname ->")
                        assert re.match("^[A-Za-z]*$",f_fname),"the input should not be anything other than English character"
                        assert 12 >= len(f_fname) > 0,"The length of the firstname should between 1 and 12"          
                        # input lastname
                        f_lname = input("Please input father's lastname ->")
                        assert re.match("^[A-Za-z]*$",f_lname),"the input should not be anything other than English character"
                        assert 12 >= len(f_lname) > 0,"The length of the lastname should between 1 and 12"   
                        print("Here we need father's birthdate")  
                        # input birth
                        f_bdate = input_birth(can_be_none = True)
                        # input birthplace
                        f_bplace = input("Please input father's birth place ->")
                        assert 20 >= len(f_bplace) >= 0,"The length of birthplace should between 1 and 20"
                        assert re.match("^[A-Za-z, ]*$",f_bplace),"only English characters and space are allowed"    
                        # input address
                        f_address = input("Please input father's address ->")
                        assert 30 >= len(f_address) >= 0,"The address should between 1 and 30"
                        assert re.match("^[A-Za-z0-9, ]*$", f_address),"only digits, English characters and space are allowed"
                        # input phone  
                        f_phone = input("Please input father's phone number (it should be no more than 10 digits)->")
                        assert 10 == len(f_phone) or len(f_phone) == 0,"The phone length should be 10 or None"
                        assert re.match("^[0-9]*$",f_phone),"only digits are allowed"
                        if (f_phone != ""):
                            f_phone = f_phone[0:3]+'-'+f_phone[3:6]+'-'+f_phone[6:10]
                    except AssertionError as e:
                        print(e)
                        
                    else:
                        print("Successful input for father ")
                        # add parents' information into persons 
                        cursor.execute("insert into persons values(?,?,?,?,?,?);",(f_fname,f_lname,f_bdate,f_bplace,f_address,f_phone)) 
                        connection.commit()
                        break
              
                    print("Something wrong in your input")
                    max_len = len("Your input hasn't been finished successfully")
                    print("*"*(max_len+6))
                    print("Error Notice".center(max_len+6))
                    print("Your input hasn't been finished successfully".center(max_len+6))
                    print("Please input Y or y to input again".center(max_len+6),
                                          "or input N or n to get back to the menu".center(max_len+6),
                                              "the others are invalid input".center(max_len+6),sep="\n")
                    print("*"*(max_len+6))
                    while True:
                        result = input("Your input -> ")
                        upper_case = result.upper()
                        if upper_case == "Y":
                            print("You choose to input again")
                            break
                        elif upper_case == "N":
                            print("You choose to stop and back to the menu")
                            print("Process terminate")
                            print("-" * 40)
                            return         
                        else:
                            print("%s is not a valid input, try something new"%result)
                                        
            m_fname = input("Please input mother's firstname ->")
            assert re.match("^[A-Za-z]*$", m_fname),\
                           "There exists characters outside A-Z a-z"            
            assert 0 < len(m_fname) <= 12,"The firstname length should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
                          
            m_lname = input("Please input mother's lastname ->")   
            assert re.match("^[A-Za-z]*$", m_lname),\
                           "There exists characters outside A-Z a-z"            
            assert 0 < len(m_lname) <= 12,"The last name length should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
                          
            cursor.execute("select fname,lname from persons where up(fname) = up(?) and up(lname) = up(?);",(m_fname,m_lname))            
            if cursor.fetchone() == None:
                print("Mother's information is not in the database, we need information of father ")
                while True:
                    try:
                        # input firstname
                        m_fname = input("Please input Mother's firstname ->")
                        assert re.match("^[A-Za-z]*$",m_fname),"the input should not be anything other than English character"
                        assert len(m_fname) > 0,"The length of the lastname should between 1 and 12"   
                        # input lastname
                        m_lname = input("Please input Mother's lastname ->")
                        assert re.match("^[A-Za-z]*$",m_lname),"the input should not be anything other than English character"
                        assert len(m_lname) > 0,"The length of the lastname should between 1 and 12" 
                        print("Here we need mother's birthdate")
                        # input birth                
                        m_bdate = input_birth(can_be_none = True)
                        
                        # input birthplace
                        m_bplace = input("Please input Mother's birth place ->")
                        assert re.match("^[A-Za-z, ]*$",m_bplace),"only English characters and space are allowed" 
                        assert 20 >= len(m_bplace) >= 0,"The birthplace should between 1 and 20"
                        # input address
                        m_address = input("Please input mother's address ->")
                        assert re.match("^[A-Za-z0-9, ]*$", m_address),"only digits, English characters and space are allowed"
                        assert 30 >= len(m_address) >= 0,"The address should between 1 and 30" 
                        # input phone 
                        m_phone = input("Please input mother's phone number (it should be no more than 10 digits)->")
                        assert re.match("^[0-9]*$",m_phone),"only digits are allowed"
                        assert 10 == len(m_phone) or len(m_phone) == 0,"The phone length should be 10 or None"
                        if (m_phone != ""):
                            m_phone = m_phone[0:3]+'-'+ m_phone[3:6]+'-'+m_phone[6:10]   
                            
                    except AssertionError as e:
                        print(e)
                        
                    else:
                        print("Successful input for mom ")
                        # add parents' information into persons 
                        cursor.execute("insert into persons values(?,?,?,?,?,?);",(m_fname,m_lname,m_bdate,m_bplace,m_address,m_phone))
                        break
        
                    print("Something wrong in your input")
                    max_len = len("Your input hasn't been finished successfully")
                    print("*"*(max_len+6))
                    print("Error Notice".center(max_len+6))
                    print("Your input hasn't been finished successfully".center(max_len+6))
                    print("Please input Y or y to input again".center(max_len+6),
                              "or input N or n to get back to the menu".center(max_len+6),
                                  "the others are invalid input".center(max_len+6),sep="\n")
                    print("*"*(max_len+6))
                    while True:
                        result = input("Your input -> ")
                        upper_case = result.upper()
                        if upper_case == "Y":
                            print("You choose to input again")
                            break
                        elif upper_case == "N":
                            print("You choose to stop and back to the menu")
                            print("Process terminate")
                            print("-" * 40)
                            return         
                        else:
                            print("%s is not a valid input, try something new"%result)
                
        except AssertionError as e:
            print(e)
        except ValueError:
            print("Should be integer")
        
        else:
            print("Your input is done")
            print("The information you provided has been recorded")
            break
        
        print("Something wrong in your input")
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
                  "or input N or n to get back to the menu".center(max_len+6),
                  "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result) 

    
    # add every thing in births
    cursor.execute("select address from persons where up(persons.fname) = up(?) and up(persons.lname) = up(?);",(m_fname,m_lname))
    regplace = cursor.fetchone()[0]
    regdate = date.today()
    cursor.execute("select ifnull(max(regno),0) from births;")
    regno = cursor.fetchone()[0] + 1
    cursor.execute("insert into births values(?,?,?,?,?,?,?,?,?,?);",(regno,fname,lname,regdate,regplace,gender,f_fname,f_lname,m_fname,m_lname))
    connection.commit()
    # add phone and address into newborns' information
    cursor.execute("select phone from persons where up(fname) = up(?) and up(lname) = up(?);",(m_fname,m_lname))
    phone = cursor.fetchone()[0]
    cursor.execute("select address from persons where up(fname) = up(?) and up(lname) = up(?);",(m_fname,m_lname))
    address = cursor.fetchone()[0]    
    cursor.execute("insert into persons values(?,?,?,?,?,?);",(fname,lname,bdate,bplace,address,phone))    
    connection.commit()
    input("Press any thing to get back to the menu")
def reg_marriage(user_city):
    '''
    The user should be able to provide the names of the partners and the system should
    assign the registration date and place and a unique registration number as discussed in registering a birth. 
    If any of the partners is not found in the database, the system should get information about the partner 
    including first name, last name, birth date, birth place, address and phone. 
    For each partner, any column other than the first name and last name can be null if it is not provided.
    '''
    '''name,regdate,regplace,unique regno'''
    '''if not in database, first name, last name, birth date, birth place, address, phone'''
    '''  
    fname char(12),
      lname char(12),
      bdate date,
      bplace char(20), 
      address char(30),
      phone char(12),
      
    regno int,
      regdate date,
      regplace char(20),
      p1_fname char(12),
      p1_lname char(12),
      p2_fname char(12),
      p2_lname char(12),
      primary key (regno),
      foreign key (p1_fname,p1_lname) references persons,
      foreign key (p2_fname,p2_lname) references persons
      
      '''
    global connection,cursor
    print("-"*40)
    print("This function will help user to register a marriage")
    
    while True:
        try:
            p1_fname = input("Please input the partner one's first name ->")
            assert 0 < len(p1_fname) <= 12,"The length of the firstname should between 1 and 12"
            assert re.match("^[A-Za-z]*$", p1_fname),"There exists characters outside A-Z a-z"            
            p1_lname = input("Please input the partner one last name ->")
            assert 0 < len(p1_lname) <= 12,"The length of the firstname should between 1 and 12"
            assert re.match("^[A-Za-z]*$", p1_lname),"There exists characters outside A-Z a-z"  
            cursor.execute("select fname, lname from persons where up(fname) = up(?) and up(lname) = up(?);", (p1_fname,p1_lname))
            # p1 not in
            
            if cursor.fetchone() == None:
                print("This partner is not recorded in our record, we need the information")
                while True:
                    try:
                        # input first name
                        p1_fname = input("Please input the partner one's first name ->")
                        assert 0 < len(p1_fname) <= 12,"The length of the firstname should between 1 and 12"
                        assert re.match("^[A-Za-z]*$", p1_fname),"There exists characters outside A-Z a-z"  
                        
                        # input last name
                        p1_lname = input("Please input the partner one's last name ->")
                        assert 0 < len(p1_lname) <= 12,"The length of the firstname should between 1 and 12"
                        assert re.match("^[A-Za-z]*$", p1_lname),"There exists characters outside A-Z a-z" 
                        print("Here please input partner 1's birthdate")
                        p1_bdate = input_birth(can_be_none = True)
                        if p1_bdate == "":
                            print("You choose not to provide this partner's birthdate")
                        
                        # input birthplace
                        p1_bplace = input("Please input partner 1's birth place ->")
                        assert 20 >= len(p1_bplace) >= 0,"The length of birthplace should between 0 and 20"
                        assert re.match("^[A-Za-z, ]*$",p1_bplace),"only English characters and space are allowed" 
                        
                        #input address
                        p1_address = input("Please input partner 1's address -> ")
                        assert 30 >= len(p1_address) >= 0,"The address should between 0 and 30"
                        assert re.match("^[A-Za-z0-9, ]*$", p1_address),"only digits, English characters and space are allowed"
                        
                        #input phone
                        p1_phone = input("Please input partner 1's phone number -> ")
                        assert 10 == len(p1_phone) or (len(p1_phone) == 0),"The phone length should be 10 or None"
                        assert re.match("^[0-9]*$", p1_phone),"only digits are allowed"
                        if ( p1_phone != ""):
                                p1_phone =  p1_phone[0:3]+'-'+ p1_phone[3:6]+'-'+ p1_phone[6:10]                 
                    except AssertionError as e:
                        print(e)
                    else:
                        cursor.execute("insert into persons values(?,?,?,?,?,?);",(p1_fname, p1_lname, p1_bdate, p1_bplace, p1_address, p1_phone)) 
                        connection.commit()                        
                        print("Success input partner 1's information")
                        break
                    max_len = len("Your input hasn't been finished successfully")
                    print("*"*(max_len+6))
                    print("Error Notice".center(max_len+6))
                    print("Your input hasn't been finished successfully".center(max_len+6))
                    print("Please input Y or y to input again".center(max_len+6),
                                      "or input N or n to get back to the menu".center(max_len+6),
                                          "the others are invalid input".center(max_len+6),sep="\n")
                    print("*"*(max_len+6))
                    while True:
                        result = input("Your input -> ")
                        upper_case = result.upper()
                        if upper_case == "Y":
                            print("You choose to input again")
                            break
                        elif upper_case == "N":
                            print("You choose to stop and back to the menu")
                            print("Process terminate")
                            print("-" * 40)
                            return         
                        else:
                            print("%s is not a valid input, try something new"%result)
  
            p2_fname = input("Please input the partner two's first name ->")
            assert 0 < len(p2_fname) <= 12,"The length of the firstname should between 1 and 12"
            assert re.match("^[A-Za-z]*$", p2_fname),"There exists characters outside A-Z a-z"            
            p2_lname = input("Please input the partner two's last name ->")
            assert 0 < len(p2_lname) <= 12,"The length of the firstname should between 1 and 12"
            assert re.match("^[A-Za-z]*$", p2_lname),"There exists characters outside A-Z a-z"            
 
            cursor.execute("select fname, lname from persons where up(fname) = up(?) and up(lname) = up(?);",(p2_fname,p2_lname))
            #p2 not in
            if cursor.fetchone() == None:
                print("This partner is not recorded in our record, we need the information")
                while True:
                    try:
                        # input first name
                        p2_fname = input("Please input the partner two's first name ->")
                        assert 0 < len(p2_fname) <= 12,"The length of the firstname should between 1 and 12"
                        assert re.match("^[A-Za-z]*$", p2_fname),"There exists characters outside A-Z a-z"  
                        
                        # input last name
                        p2_lname = input("Please input the partner two's last name ->")
                        assert 0 < len(p2_lname) <= 12,"The length of the firstname should between 1 and 12"
                        assert re.match("^[A-Za-z]*$", p2_lname),"There exists characters outside A-Z a-z" 
                        print("Here please input partner 2's birthdate")
                        p2_bdate = input_birth(can_be_none = True)
                        if p2_bdate == "":
                            print("You choose not to provide this partner's birthdate")
                        
                        # input birthplace
                        p2_bplace = input("Please input partner 2's birth place ->")
                        assert 20 >= len(p2_bplace) >= 0,"The length of birthplace should between 0 and 20"
                        assert re.match("^[A-Za-z, ]*$",p2_bplace),"only English characters and space are allowed" 
                        
                        #input address
                        p2_address = input("Please input partner 2's address -> ")
                        assert 30 >= len(p2_address) >= 0,"The address should between 0 and 30"
                        assert re.match("^[A-Za-z0-9, ]*$", p2_address),"only digits, English characters and space are allowed"
                        
                        #input phone
                        p2_phone = input("Please input partner 2's phone number -> ")
                        assert 10 == len(p2_phone) or len(p2_phone) == 0,"The phone length should be 10 or None"
                        assert re.match("^[0-9]*$", p2_phone),"only digits are allowed"
                        if ( p2_phone != ""):
                                p2_phone =  p2_phone[0:3]+'-'+ p2_phone[3:6]+'-'+ p2_phone[6:10]                     
                    except AssertionError as e:
                        print(e)
                    else:
                        cursor.execute("insert into persons values(?,?,?,?,?,?);",(p2_fname, p2_lname, p2_bdate, p2_bplace, p2_address, p2_phone))
                        connection.commit()                       
                        print("Success input partner 2's information")
                        break
                    max_len = len("Your input hasn't been finished successfully")
                    print("*"*(max_len+6))
                    print("Error Notice".center(max_len+6))
                    print("Your input hasn't been finished successfully".center(max_len+6))
                    print("Please input Y or y to input again".center(max_len+6),
                                      "or input N or n to get back to the menu".center(max_len+6),
                                          "the others are invalid input".center(max_len+6),sep="\n")
                    print("*"*(max_len+6))
                    while True:
                        result = input("Your input -> ")
                        upper_case = result.upper()
                        if upper_case == "Y":
                            print("You choose to input again")
                            break
                        elif upper_case == "N":
                            print("You choose to stop and back to the menu")
                            print("Process terminate")
                            print("-" * 40)
                            return         
                        else:
                            print("%s is not a valid input, try something new"%result)
            
        except AssertionError as e:
            print(e)
        else:
            print("Your input is done")
            print("The information you provided has been recorded")
            break                        
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
                              "or input N or n to get back to the menu".center(max_len+6),
                                          "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result)                  
    # assign a unique regno
    cursor.execute("select ifnull(max(regno),0) from marriages;")
    regno = cursor.fetchone()[0] + 1
    cursor.execute("insert into marriages values(?,?,?,?,?,?,?);",(regno, date.today(), user_city, p1_fname, p1_lname, p2_fname, p2_lname))
    connection.commit()
    print("marriage record finished")
    input("Press any thing to get back to the menu")
    
'''Renew a vehicle registration.The user should be able to provide an existing registration number and renew 
the registration. The system should set the new expiry date to one year from today's date if the current 
registration either has expired or expires today. Otherwise, the system should set the new expiry to one year 
after the current expiry date.
'''    
def renew_vehicle_registration():
    global connection, cursor
    print("-" * 40)
    print("Renew the expiry date ")
    print("-" * 40)
    while True:
        try:
            regno = int(input("Please input the registration number ->"))
            assert 0 <= regno,"The registration number have to be non-negative"
            #assert re.match("^[0-9]*$", regno),"The registration number have to be three digits"
            cursor.execute("select regno from registrations where regno = ?;",(regno,))
            assert cursor.fetchone() != None,"This registration number does not exist."
        except AssertionError as e:
            print(e)
        except ValueError:
            print("Sorry, you should input a non-negative integer")
        else:
            print("success input")
            break
        print("Not successful input ")
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
                  "or input N or n to get back to the menu".center(max_len+6),
                      "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result)   
    
    cursor.execute("select expiry from registrations where regno = ?;",(regno,)) 
    year_base = max(cursor.fetchone()[0], str(date.today())) # compare the max between expiry and today's date

        
    '''    if expiry <= today_date:
        year = int(str(today_date)[0:4])+1
        new_expiry = str(year)+str(today_date)[4:7]+str(today_date)[7:10]
        print(new_expiry)

    else:'''

    new_expiry = str(int(str(year_base)[0:4])+1)+str(year_base)[4:7]+str(year_base)[7:10]
    print("The new expiry is: %s"%new_expiry)
    cursor.execute("update registrations set expiry = ? where regno = ?;",(new_expiry, regno))    
    connection.commit()
    input("Press any thing to get back to the menu")
def process_bill_sale():
    global connection, cursor
    '''
    logic here:
    1. set current registration's expiry date to today's date 
    2. create new registration, set the registration date to today and 
    set the expiry date to a year after today
    3. a unique registration number should be assigned by 
    the system to the new registration
    use the max reg number in the database and + 1 then. 
    4. The vin will be copied from the current registration to the new one.
    
    '''
    print("-" * 40)
    print("Process a bill of sale")
    print("-" * 40)
    vin, current_owner_fname, current_owner_lname,\
    new_owner_fname, new_owner_lname, plate_number = "", "", "", "", "", ""
    while True:
        # pay more attention to the case sensitive
        try:
            # do exception handling, should be char(5)
            vin = input("Please input the car's vin -> ").replace(" ","")  
            assert 0 < len(vin) <= 5,\
                   "This is not a valid vin since "\
                   "the length should be no more than 5 or less than 1"
            # regular expression, we only allow A-Z a-z 0-9 here
            assert re.match("^[A-Za-z0-9]*$", vin),\
                   "There exists characters outside 0-9 A-Z a-z"
            check_vehicle = '''select ifnull(count(*), 0) 
            from vehicles where up(vin) = up(?);'''
            cursor.execute(check_vehicle, (vin,))
            assert cursor.fetchone()[0] != 0, \
                   "This vehicle is not in our record"
            
            check_whether_have_registered = '''select ifnull(count(*),0) 
            from registrations 
            where up(vin) = up(?);'''
            cursor.execute(check_whether_have_registered,(vin,))
            assert cursor.fetchone()[0] != 0,"This car has no owner"
            
            
            get_owner_content = '''select fname, lname from registrations 
            where up(vin) = up(?) and regdate = (select max(regdate) 
            from registrations where up(vin) = up(?));'''
            cursor.execute(get_owner_content, (vin, vin)) 
            recent_owner_name = cursor.fetchone()
            assert recent_owner_name,"This car don't have a recent owner"
            
            # do exception handling, should be char(12)
            current_owner_fname = input("Please input the firstname of the "\
                                        "current owner -> ").replace(" ","")  
            assert 0 < len(current_owner_fname) <= 12,\
                   "This is not a valid firstname since "\
                   "the length should not be more than 12 or less than 1"
            # do exception handling, should be char(12)
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", current_owner_fname),\
                   "There exists characters outside A-Z a-z"
            current_owner_lname = input("Please input the lastname of "\
                                        "the current owner -> ").replace(" ","")  
            assert 0 < len(current_owner_lname) <= 12,\
                   "This is not a valid lastname since "\
                   "the length should not be more than 12 or less than 1"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", current_owner_lname),\
                   "There exists characters outside A-Z a-z"
            # make sure the current owner's name is in the record
            check_cur_owner_name = '''select count(*) from persons where up(fname) = up(?) and up(lname) = up(?);'''
            cursor.execute(check_cur_owner_name, (current_owner_fname, current_owner_lname))

            assert cursor.fetchone()[0] == 1,"This current owner's name is now in the record"            
            assert (current_owner_fname.upper(), 
                    current_owner_lname.upper()) == (recent_owner_name[0].upper(), 
                                                     recent_owner_name[1].upper()),\
                   "This name is not the current owner's name"
            # check whether the name above is the same as the the 
            # name of the most recent owner of the car in the system
            # do exception handling, should be char(12)
            new_owner_fname = input("Please input the firstname "\
                                    "of the new owner -> ").replace(" ","")  
            assert 0 < len(new_owner_fname) <= 12,\
                   "This is not a valid lastname for "\
                   "new owner since the length should "\
                   "not be more than 12 or less than 1"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", new_owner_fname),\
                   "There exists characters outside A-Z a-z"
            # do exception handling, should be char(12)  
            new_owner_lname = input("Please input the lastname of "\
                                    "the new owner -> ").replace(" ","")  
            assert 0 < len(new_owner_lname) <= 12,\
                   "This is not a valid lastname for new "\
                   "owner since the length should not be "\
                   "more than 12 or less than 1"
            # regular expression, we only allow A-Z a-zhere
            assert re.match("^[A-Za-z]*$", new_owner_lname),\
                   "There exists characters outside A-Z a-z"
            # make sure the new owner's name is in the record
            check_new_owner_name = '''select count(*) from persons where up(fname) = up(?) and up(lname) = up(?);'''
            cursor.execute(check_new_owner_name,(new_owner_fname, new_owner_lname))
            assert cursor.fetchone()[0] == 1,"This new owner's name is not in the record"
            # plate char(7)
            assert (current_owner_fname, current_owner_lname) != (new_owner_fname, new_owner_lname),\
                   "One can't buy his own car"
            plate_number = input("Please input the "\
                                 "car's plate_number:").replace(" ","") 
            assert 0 < len(plate_number) <= 7,\
                   "The length of the plate should be 1 to 7"
            # regular expression, we only allow A-Z a-z 0-9 here
            assert re.match("^[A-Za-z0-9]*$", plate_number),\
                   "There exists characters outside 0-9 A-Z a-z"
            # do exception handling             
        except AssertionError as e:
            print("Error reason:",e)
        else:
            print("Input Successfully")
            break
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
              "or input N or n to get back to the menu".center(max_len+6),
              "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result)
    # the above variables so far we assume they are valid
    update_registration = '''update registrations set 
    expiry = date('now','localtime') 
    where up(vin) = up(?) and up(fname) = up(?) and up(lname) = up(?) 
    and regdate = (select max(regdate) from registrations where up(vin) = up(?));'''
    cursor.execute(update_registration,
    (vin, current_owner_fname ,current_owner_lname, vin))
    connection.commit()
    # registrations(regno, regdate, expiry, plate, vin, fname, lname)
    # assign a new regno for the new registration
    cursor.execute("select max(regno) from registrations")
    current_max_regno = cursor.fetchone()[0]
    assigned_new_regno = current_max_regno + 1
    insert_current_time = '''insert into registrations values 
    (?, date('now','localtime'), 
    date('now','+12 months','localtime'), ?, ?, ?, ?);'''
    cursor.execute(insert_current_time, 
                   (assigned_new_regno, 
                    plate_number, vin, 
                    new_owner_fname, 
                    new_owner_lname))
    connection.commit()
    print("-"*40)
    print("Here's your sale result:",
                  "Car's VIN: %s"%vin, 
                  "Current owner's name: %s %s"%(current_owner_fname,
                                                 current_owner_lname),
                  "New owner's name: %s %s"%(new_owner_fname, 
                                             new_owner_lname),
                  "New plate for the car: %s"%plate_number,
                  sep="\n")    
    print("-"*40)
    input("Press any thing to get back to the menu")
    return

def process_payment():
    '''
    Process a payment.
    The user should be able to record a payment 
    by entering a valid ticket number and an amount. 
    The payment date is automatically set to 
    the day of the payment (today's date). 
    A ticket can be paid in multiple payments but the sum of those
    payments cannot exceed the fine amount of the ticket.
    
    tickets(tno, regno, fine, violation, vdate)
    payments(tno, pdate, amount) 
    
    tno int,
    regno int,
    fine int,
    pdate date,
    amount int,
    '''
    global connection, cursor
    print("-" * 40)
    print("Process a payment")
    print("-" * 40)
    tno, amount = 0, 0;
    while True:
        try:
            # 1 the tno is larger than 0 
            # 2 the tno exists in the tickets table
            # 3 tno and amount are integers
            tno = int(input("Please input a ticket number -> ").replace(" ",""))
            assert tno >= 0,"A ticket number can't be negative" 
            cursor.execute("select tno from tickets where tno = ?;", (tno, ))
            assert len(cursor.fetchall()) != 0, \
                   "This tno does not exist"
            check_same_day = '''select ifnull(count(*), 0) 
            from payments where tno = ? 
            and pdate = date('now','localtime');'''
            cursor.execute(check_same_day,(tno,))
            assert cursor.fetchone()[0] == 0,\
                   "Each ticket can only have one payment in a day"
            payment_sum_content = '''select ifnull(sum(amount), 0) 
            from payments where tno = ?;'''
            cursor.execute(payment_sum_content, (tno, ))
            payment_sum = cursor.fetchone()[0]
            cursor.execute("select fine from tickets where tno = ?;", (tno, ))
            fine_num = cursor.fetchone()[0]
            # you can't pay more if you already payed all the fine on this ticket
            assert payment_sum < fine_num,\
                   "The fine has been clear, you can't pay more"
            amount = int(input("Please input an amount "\
                               "you want to pay -> ").replace(" ",""))
            assert amount > 0,"Not a valid amount"
            assert amount + payment_sum <= fine_num,\
                   "The amount you want to pay is %d"\
                   " and it's larger than the balance %d"\
                   %(amount, fine_num - payment_sum)
        except ValueError:
            print("You have input a non integer, "\
                  "both tno and amount should be integer")
        except AssertionError as e:
            print("Error reason:",e)
        else:
            print("Input Successfully")
            break
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
                  "or input N or n to get back to the menu".center(max_len+6),
                  "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result)     
            
    # below we assume the numbers are correct
    
    
    insert_content = '''insert into payments 
    values (?, date('now','localtime'), ?);'''
    cursor.execute(insert_content, (tno, amount))
    connection.commit()
    
    #payments(tno, pdate, amount) 
    result_content = '''select tno, pdate, amount from payments where tno = ? 
    and pdate = date('now', 'localtime');'''
    cursor.execute(result_content, (tno, ))
    payment_result = cursor.fetchone()
    sum_after_payment = '''select ifnull(sum(amount), 0) 
            from payments where tno = ?;'''
    cursor.execute(sum_after_payment, (tno, ))
    sum_after_pay = cursor.fetchone()[0]
    cursor.execute("select fine from tickets where tno = ?;", (tno, ))
    fine_num = cursor.fetchone()[0]    
    after_balance = fine_num - sum_after_pay
    print("-"*40)
    print("Here's your payment result")
    print("ticket no -> %d"%tno)
    print("payment amount -> %d"%amount)
    print("payment date -> %s"%payment_result[1])
    print("balance -> %s"%after_balance)
    print("-"*40)
    input("Press any thing to get back to the menu")
    return

def get_driver_abstract():
    fname,lname = "0","0"
    global connection, cursor
    print("-" * 40)
    print("Get a driver abstract")
    print("-" * 40)
    while True:
        try:
            '''
            Exception Handling logic:
            fname: 
            1 no more than length 12 
            2 a-z A-Z
            lname:
            1 no more than length 12 
            2 a-z A-Z
            together:
            1 fname,lname in the registrations
            '''
            fname = input("Please input the firstname "\
                          "of the driver -> ").replace(" ","")
            assert 0 < len(fname) <= 12,\
                   "The length of the firstname should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", fname),\
                   "There exists characters outside A-Z a-z"
             
            lname = input("Please input the lastname "\
                          "of the driver -> ").replace(" ","")
            assert 0 < len(lname) <= 12,\
                   "The length of the lastname should between 1 and 12"
            # regular expression, we only allow A-Z a-z here
            assert re.match("^[A-Za-z]*$", lname),\
                   "There exists characters outside A-Z a-z"
            check_name_exist = '''select fname, lname 
            from registrations 
            where up(fname) = up(?) 
            and up(lname) = up(?);'''
            cursor.execute(check_name_exist, (fname, lname))
            assert cursor.fetchone() != None,\
                   "This name is not a recorded driver's name"
        except AssertionError as e:
            print("Error reason:",e)
        else:
            print("Input Successfully")
            print("-"*40)
            break
        max_len = len("Your input hasn't been finished successfully")
        print("*"*(max_len+6))
        print("Error Notice".center(max_len+6))
        print("Your input hasn't been finished successfully".center(max_len+6))
        print("Please input Y or y to input again".center(max_len+6),
              "or input N or n to get back to the menu".center(max_len+6),
              "the others are invalid input".center(max_len+6),sep="\n")
        print("*"*(max_len+6))
        while True:
            result = input("Your input -> ")
            upper_case = result.upper()
            if upper_case == "Y":
                print("You choose to input again")
                break
            elif upper_case == "N":
                print("You choose to stop and back to the menu")
                print("Process terminate")
                print("-" * 40)
                return         
            else:
                print("%s is not a valid input, try something new"%result)
    # here the fname and lname are valid
      
    # get the ticket amount in total
    ticket_amount_content = '''select ifnull(count(tno), 0) 
    from tickets, registrations 
    where tickets.regno = registrations.regno
    and up(registrations.fname) = up(?) and up(registrations.lname) = up(?);'''
    cursor.execute(ticket_amount_content, (fname, lname))
    ticket_amount = cursor.fetchone()[0]
    
    # get the ticket amount in 2 years
    two_year_ticket_amount_content = '''select ifnull(count(tno), 0) 
    from tickets, registrations 
    where tickets.regno = registrations.regno
    and up(registrations.fname) = up(?) and up(registrations.lname) = up(?)
    and vdate >= date('now','-2 year','localtime') 
    and vdate <= date('now','localtime');'''
    cursor.execute(two_year_ticket_amount_content, (fname, lname))
    two_year_ticket_amount = cursor.fetchone()[0]    
    
    # get the total demeritNotices amount and the total demeritpoints amount
    demerit_amount_content = '''select ifnull(count(*), 0), 
    ifnull(sum(ifnull(points, 0)),0) 
    from demeritNotices 
    where up(fname) = up(?) and up(lname) = up(?);'''
    cursor.execute(demerit_amount_content,(fname, lname))
    tuples = cursor.fetchone()
    demerit_amount = tuples[0]
    demerit_point_sum = tuples[1]
    
    # get the 2 years demeritNotices amount and the 2 years demeritpoints amount
    two_year_point_sum_content = '''select ifnull(count(*), 0), ifnull(sum(ifnull(points, 0)), 0) 
    from demeritNotices 
    where up(fname) = up(?) and up(lname) = up(?) 
    and ddate >= date('now','-2 year','localtime') 
    and ddate <= date('now','localtime');'''
    cursor.execute(two_year_point_sum_content, (fname, lname))
    two_year_result = cursor.fetchone()
    two_year_demerit_amount = two_year_result[0]
    two_year_point_sum = two_year_result[1]
    '''
    The user should be given the option to see the tickets 
    ordered from the latest to the oldest.
    For each ticket, you will report the ticket number, 
    the violation date, 
    the violation description, 
    the fine, 
    the registration number 
    and the make 
    and model of the car for which the ticket is issued. 
    If there are more than 5 tickets, at most 5 tickets will be 
    shown at a time, and the user can select to see more.
    '''    
    '''
    vehicles(vin,make,model,year,color)
    registrations(regno, regdate, expiry, plate, vin, fname, lname)
    tickets(tno,regno,fine,violation,vdate)
    demeritNotices(ddate, fname, lname, points, desc)
    '''        
    print("Here we will show your tickets informations",
          "There are three view options here",
          "(1) normal order",
          "(2) from the latest to the oldest",
          "(3) from the oldest to the latest",
          sep="\n")
    choice = ""
    content_base = '''select tno, vdate, violation, fine, registrations.regno, 
    make, model from vehicles, tickets, registrations 
    where up(registrations.vin) = up(vehicles.vin) 
    and tickets.regno = registrations.regno 
    and up(registrations.fname) = up(?) 
    and up(registrations.lname) = up(?)'''
    while True:
        choice = input("Please input 1-3 to choose an order "\
                       "you want to view your tickets "\
                       "information or input q or Q "\
                       "back to the menu -> ").replace(" ","")
        if choice == "1":
            content_base += ";"
            break
        elif choice == "2":
            content_base += "order by vdate desc;"
            break            
        elif choice == "3":
            content_base += "order by vdate asc;"
            break 
        elif choice.upper() == "Q":
            print("Process Terminate");
            print("-" * 40)
            return
        else:
            print("This choice is not valid, it should between 1-3, q or Q")
            print("Please try again")
    print("-" * 40)
    cursor.execute(content_base, (fname, lname))
    result_list = cursor.fetchall()
    title_list = ["ticket no", "violation date", 
                  "violation description", "fine", 
                  "regno", "make", "model"]
    max_length_list = []
    view_limit = len(result_list);
    if view_limit > 5:
        while True:
            print("The default is checking top 5 tickets based on your view order",
                  "But you can choose to view all the tickets",
                      "Please input y or Y if you want to view all the tickets",
                      "Or input n or N to view the top 5 tickets",
                      "Or input q or Q to quit the view and back to the menu",
                      "Other inputs will be considered as invalid",
                      sep="\n")                
            choice = input("Please input your choice -> ")
            if choice.upper() == "Y":
                print("You choose to view all the tickets")
                break
            elif choice.upper() == "N":
                view_limit = 5
                print("You choose to view top 5 of "\
                "the tickets based on your view order")
                break
            elif choice.upper() == "Q":
                print("Process Terminate")
                return
            else:
                print("%s is not a valid input"%choice)     
    print("-" * 40)
    print("View result:")
    print("Driver name: %s %s"%(fname, lname))
    print("In two years:")
    print("Number of tickets -> %d"%two_year_ticket_amount, 
          "Number of demerit notices -> %d"%two_year_demerit_amount,
          "Total number of demerit points -> %d"%two_year_point_sum,sep="\n")
    print("In total:")
    print("Number of tickets -> %d"%ticket_amount, 
          "Number of demerit notices -> %d"%demerit_amount,
          "Total number of demerit points -> %d"%demerit_point_sum, sep="\n")    
    if len(result_list) != 0:
        print("|",end="")
        # to make the view result more clear
        for j in range(7):
            max_length_list.append(max(max([len(str(result_list[i][j])) \
                                            for i in range(len(result_list))]), 
                                       len(title_list[j])))
            print(title_list[j].center(max_length_list[j] + 4),end="|")
        print("",end="\n")
        for i in range(view_limit):
            print("|",end="")
            for j in range(7):
                print(str(result_list[i][j]).center(max_length_list[j] + 4), 
                      end="|")                              
            print("",end="\n")  
    else:
        print("No ticket record for driver %s %s"%(fname, lname))
    print("View over")
    input("Press any thing to get back to the menu")
    return
def LoginAndFunctions():
    global connection, cursor
    program_continue = True
    while program_continue:# main loop
        userid = ""
        password = ""
        user = None
        print("-"*40)
        print("Welcome to our program")
        print("-"*40)
        while True:
            try:
                # enter userid
                userid = input("Enter a user id -> ")
                assert 0 < len(userid) <= 8,"The id length should between 1 and 8"
                assert re.match("^[A-Za-z0-9-]*$", userid),"The id should only contains alphabets, numbers and underscore"
                # user password
                password = getpass.getpass("Enter a password -> ")
                assert 0 < len(password) <= 8,"The password length should between 1 and 8"
                assert re.match("^[A-Za-z0-9-]*$", password),"The password should only contains alphabets, numbers and underscore"
                # here password and user name are legal
                check_correct = '''select utype from users where uid = ? and pwd = ?;'''
                cursor.execute(check_correct, (userid, password))
                user_result = cursor.fetchone()
                assert user_result != None,"Sorry the password is not correct or the user is not in our system"
            except AssertionError as e:
                print("Error:",e)
            else:
                user = user_result[0]
                print("Login Successful User %s"%userid)
                break
            while True:
                stop = input("Input q or Q to terminate the program and input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Program terminate, thanks for using")
                    return
                elif stop_up == "Y":
                    print("You choose to login again")
                    break


        if user == 'a':
            user = 'registry'
        elif user == 'o':
            user = 'traffic'
        while True: 
            if user == "registry":
                print("-"*40)
                print("Possible actions are shown below",
                    "1: Register a birth",
                    "2: Register a marriage",
                    "3: Renew a vehicle registration",
                    "4: Process a bill of sale",
                    "5: Process a payment",
                    "6: Get a driver abstract",
                    "7: log out",
                    "8: Program terminate",
                    sep="\n")            
                print("-"*40)
                try:
                    chosen = int(input("Which would you like to do -> "))
                    assert chosen in range(1,9),"Your choice should be an integer between 1 and 8"
                        
                except ValueError:
                    print("Your choice should be an integer")
                except AssertionError as e:
                    print(e)
                else: 
                    print("You choose: %d"%chosen)
                    if chosen == 1:
                        reg_birth()
                    elif chosen == 2:
                        cursor.execute("select city from users where uid = ?",(userid,))
                        user_city = cursor.fetchone()[0]#question here: what if the user city is null
                        reg_marriage(user_city)
                    elif chosen == 3:
                        renew_vehicle_registration()
                    elif chosen == 4:
                        process_bill_sale()
                    elif chosen == 5:
                        process_payment()
                    elif chosen == 6:
                        get_driver_abstract()   
                    elif chosen == 7:
                        print("You choose to log out")
                        break
                    elif chosen == 8:
                        print("You choose to terminate the program")
                        program_continue = False
                        break       
            elif user == "traffic":
                print("-"*40)
                print("Possible actions are shown below",
                          "1: Issue a ticket",
                          "2: Find a car owner",
                          "3: Log out",
                          "4: Program terminate",
                          sep="\n")     
                print("-"*40)
                try:
                    chosen = int(input("Which would you like to do -> "))
                    assert chosen in range(1, 5),"Your choice should be an integer between 1 and 4"
                except ValueError:
                    print("Your choice should be an integer")
                except AssertionError as e:
                    print(e)
                else: 
                    print("You choose: %d"%chosen)
                    if chosen == 1:
                        ticketIssue()
                    elif chosen == 2:
                        find_carOwner()    
                    elif chosen == 3:
                        print("You choose to log out")
                        break                    
                    elif chosen == 4:
                        print("You choose to terminate the program")
                        program_continue = False
                        break

def ticketIssue():
    global connection, cursor

    print("-"*40)
    print("Issue a ticket")
    print("-"*40)
    print("You can provide a registration number to see the reg information")
    regno = None
    while True:
        try:
            regno = int(input("Please enter a registration number: "))
            cursor.execute('SELECT ifnull(count(*),0) FROM registrations WHERE regno=?;', (regno,))
            assert cursor.fetchone()[0] != 0,"Sorry, this registration is not in the record"
        except ValueError:
            print("The input should be an integer")
        except AssertionError as e:
            print(e)
        else:
            print("Succesfull input")

            break
        while True:
            stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
            stop_up = stop.upper()
            if stop_up not in["Q","Y"]:
                print("Invalid input, try again")
            elif stop_up == "Q":
                print("Back to the menu")
                return
            elif stop_up == "Y":
                print("You choose to input again")
                break        
    # here the regno is already valid and we already have this registration in our record
    
    cursor.execute('SELECT fname,lname,make,model,year,color FROM registrations r, vehicles t WHERE up(r.vin) = up(t.vin) and r.regno = ?;',(regno,))
    info = cursor.fetchone()   
    len_max = max([len(str(i)) for i in info])
    title_list = ["fname", "lname", "make", "model", "year", "color"]
    
    print("Here is %d 's information"%regno)
    for i in title_list:
        print(str(i).center(len_max+2),end="")
    print("\n",end="")
    for j in info:
        print(str(j).center(len_max+2),end="")
    print("\n",end="")
    
    cursor.execute('SELECT ifnull(MAX(tno), 0) FROM tickets')
    tno = cursor.fetchone()[0] + 1 # current maximum + 1
    viodate = None
    viotext = None
    fine = None
    print("Here you can process and ticket the registration")
    while True:

            print("Here please input the viodate for the ticket")
            viodate = input_birth(can_be_none = True)
            if not viodate:
                viodate = str(date.today())
            print("The input date is %s"%viodate)
            break

    while True:
        try:
            viotext = input("Here please input the viotext for the ticket -> ")
            assert re.match("^[A-Za-z0-9_ ]*$", viotext),"Only A-Z a-z 0-9 underscore space are allowed"
            assert len(viotext) > 0,"You input nothing for the viotext"
        except AssertionError as e:
            print(e)
        else:
            print("Succesfull input")
            break
        while True:
            stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
            stop_up = stop.upper()
            if stop_up not in["Q","Y"]:
                print("Invalid input, try again")
            elif stop_up == "Q":
                print("Back to the menu")
                return
            elif stop_up == "Y":
                print("You choose to input again")
                break          


    while True:
        try:
            fine = int(input("Enter a fine amount: "))
            assert fine > 0,"The fine amount should be lerger than 0"
        except AssertionError as e:
            print(e)
        except ValueError:
            print("fine should be an integer")
        else:
            break
        while True:
            stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
            stop_up = stop.upper()
            if stop_up not in["Q","Y"]:
                print("Invalid input, try again")
            elif stop_up == "Q":
                print("Back to the menu")
                return
            elif stop_up == "Y":
                print("You choose to input again")
                break         

    values = (int(tno), int(regno), int(fine), viotext, viodate)

    cursor.execute('INSERT into tickets Values (?,?,?,?,?);', values)
    connection.commit()
    
    cursor.execute('SELECT * from tickets Where tno = ?;', (tno, ))
    new_ticket = cursor.fetchone()
    print("Here's the new ticket information:")
    max_len = max([len(str(i)) for i in new_ticket])
    titles = ["tno", "regno", "fine", "violation", "vdate"]
    for i in titles:
        print(str(i).center(len_max+2),end="")
    print("\n",end="")
    for j in new_ticket:
        print(str(j).center(len_max+2),end="")
    print("\n",end="")
    print("-"*40)
    input("Press any thing to get back to the menu")

def find_carOwner():
    print("-"*40)
    print("find car owner")
    print("-"*40)
    
    keepgoing = True
    values = []
    values.append("No")
    make = None
    model = None
    color = None
    year = None
    plate = None
    index = 1
    while True:
        not_search_condition = 0
        while True:
            try:
                make = input("Enter make -> ")
                if make == "":
                    print("You don't want to search based on make")
                    not_search_condition += 1
                    break            
                assert re.match("^[A-Za-z]*$", make), "Incorrect format"
                assert 0 < len(make) <= 10,"The make length should between 1 and 10"
            except AssertionError as e:
                print(e)
            else:
                break
            while True:
                stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Back to the menu")
                    return
                elif stop_up == "Y":
                    print("You choose to input again")
                    break           
    
        while True:
            try:
                model = input("Enter model -> ")
                if model == "":
                    print("You don't want to search based on model")
                    not_search_condition += 1
                    break            
                assert re.match("^[A-Za-z0-9]*$", model), "Incorrect format"
                assert 0 < len(model) <= 10,"The model length should between 1 and 10"
            except AssertionError as e:
                print(e)
            else:
                break
            while True:
                stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Back to the menu")
                    return
                elif stop_up == "Y":
                    print("You choose to input again")
                    break    
    
        while True:
            try:
                year = input("Enter year -> ")
                if year == "":
                    print("You don't want to search based on year")
                    not_search_condition += 1
                    break      
                year = int(year)
            except ValueError:
                print("The year should be an integer")
            else:
                break
            while True:
                stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Back to the menu")
                    return
                elif stop_up == "Y":
                    print("You choose to input again")
                    break
    
        while True:
            try:
                color = input("Enter color -> ")
                if color == "":
                    print("You don't want to search based on color")
                    not_search_condition += 1
                    break
                assert re.match("^[A-Za-z]*$", color), "Incorrect format"
                assert 0 < len(color) <= 10,"The color length should between 1 and 10"
            except AssertionError as e:
                print(e)
            else:
                break
            while True:
                stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Back to the menu")
                    return
                elif stop_up == "Y":
                    print("You choose to input again")
                    break    
    
        while True:
            try:
                plate = input("Enter plate -> ")
                if plate == "":
                    print("You don't want to search based on plate")
                    not_search_condition += 1
                    break            
                assert re.match("^[A-Za-z0-9]*$", plate), "Incorrect format"
                assert 0 < len(plate) <= 7,"The plate length should between 1 and 7"
            except AssertionError as e:
                print(e)
            else:
                break
            while True:
                stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                stop_up = stop.upper()
                if stop_up not in["Q","Y"]:
                    print("Invalid input, try again")
                elif stop_up == "Q":
                    print("Back to the menu")
                    return
                elif stop_up == "Y":
                    print("You choose to input again")
                    break   
        if not_search_condition == 5:
            print("You must input search conditions num more than 1 and no more than 5")
        else:
            print("Input search condition successful")
            break

    statement = 'SELECT make,model,year,color,plate,registrations.vin FROM vehicles left outer join registrations using (vin) where 1 = 1'
    if make:
        statement += " AND up(make) = up(?)"
        values.append(make)
    if model:
        statement += " AND up(model) = up(?)"
        values.append(model)
    if year:
        statement += " AND year = ?"
        values.append(year)
    if color:
        statement += " AND up(color) = up(?)"
        values.append(color)
    if plate:
        
        statement += " AND up(plate) = up(?)"
        values.append(plate)    

    cursor.execute(statement,values[1:])
    result = cursor.fetchall() 
    # [(make1,model1,year1,color1,plate1,vin1),(make2,model2,year2,color2,plate2,vin2)]
    output = [i[:5] for i in result]
    # [(make1,model1,year1,color1,plate1),(make2,model2,year2,color2,plate2)]
    if not output:
        print("No matches found for the information inputted")
        input("Press any thing to get back to the menu")
        return
        
    else:
        '''make,model,year,color,plate'''
        titles = ["No", "make", "model","year","color","plate"]
        amount = len(output)
        if amount >= 4:
            for i in titles:
                print(str(i).center(12),end="")
            print("\n",end="")
            for i in output:
                print(str(index).center(12),end="")
                for j in i:
                    print(str(j).center(12),end="")
                index += 1
                print("\n",end="")  
            chosen = None
            while True:
                try:
                    chosen = int(input("Please choose a result Number to look in detail -> "))
                    assert 1 <= chosen <= index,"The no out of range, should be no more tham %d"%index
                except AssertionError as e:
                    print(e)
                except ValueError:
                    print("Your choice should be integer")
                else:
                    break
                while True:
                    stop = input("Input q or Q to back to the menu or input Y or y to continue input -> ")
                    stop_up = stop.upper()
                    if stop_up not in["Q","Y"]:
                        print("Invalid input, try again")
                    elif stop_up == "Q":
                        print("Back to the menu")
                        return
                    elif stop_up == "Y":
                        print("You choose to input again")
                        break                     
                
            print("Now display the detail information for this record")

            
            record_vin = result[chosen - 1][5]
            one_record_result = None
            max_length = 12
            if record_vin:
                command = '''SELECT v.make, v.model, v.year, v.color, r.regdate,
                r.expiry, fname, lname 
                FROM registrations r, vehicles v 
                WHERE up(v.vin) = up(r.vin) and up(r.vin) = up(?)
                AND r.regdate = (select max(t.regdate) FROM registrations t, vehicles k 
                WHERE up(t.vin) = up(k.vin) and up(k.vin) = up(?)) and r.expiry > r.regdate;
                '''
                
                cursor.execute(command, (record_vin, record_vin))
                one_record_result = cursor.fetchone() # [make, model, year, color, regdate, expiry, fname, lname]
                max_length = max([len(str(i)) for i in one_record_result])
               
            title_list = ["make", "model", "year", "color", "regdate", "expiry", "fname", "lname"]
            
            print("Here's in detail")
            for i in title_list:
                print(i.center(max_length+2), end="")
            print("\n",end="")
            if not record_vin:
                for k in result[chosen - 1]:
                    print(str(k).center(max_length+2),end="")
                print("This vehicle doesn't have registrations")
            else:
                for j in one_record_result:
                    print(str(j).center(max_length+2), end="")

            print("\n",end="")
            
        else:
            print("Since the amount of record is less than 4, display the information in detail")
            value_list = []
            none_list = []
            command = '''SELECT v.make, v.model, v.year, v.color, r.regdate,
                    r.expiry, fname, lname 
                    FROM registrations r, vehicles v 
                    WHERE up(v.vin) = up(r.vin) and up(r.vin) = up(?)
                    AND r.regdate = (select max(t.regdate) FROM registrations t, vehicles k 
                    WHERE up(t.vin) = up(k.vin) and up(k.vin) = up(?)) and r.expiry > r.regdate;
                    '''    
            max_length = 12
            for vin_index in range(len(result)):
                record_vin = result[vin_index][5]
                if record_vin:# is not none
                    cursor.execute(command, (record_vin, record_vin))
                    one_record_result = cursor.fetchone() # [make, model, year, color, regdate, expiry, fname, lname]
                    value_list.append(one_record_result)
                    max_length = max([len(str(i)) for i in one_record_result])
                else:
                    none_list.append(result[vin_index][:5])
                    
                    
                
            title_list = ["make", "model", "year", "color", "regdate", "expiry", "fname", "lname"]
            
            for i in title_list:
                print(i.center(max_length+2), end="")
            print("\n",end="")
            for i in value_list:
                for j in i:
                    print(str(j).center(max_length+2), end="")
                print("\n",end="")
            for j in none_list:
                for k in j:
                    print(str(k).center(max_length+2),end="")
                print("This vehicle doesn't have registrations")
                
    input("Press any thing to get back to the menu")
 
    
def main():
    global connection, cursor
    if len(sys.argv) > 1:
        path = sys.argv[1]    
        connect(path)      
        connection.create_function("up", 1, change_upper) 
        LoginAndFunctions()
    
main()