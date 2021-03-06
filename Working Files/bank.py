from datetime import date, timedelta
from decimal import *
import pdb

"""
Module construct
---------------------
class InvalidOperationError
    custom build exception class that contains a message
class UserQuitException
    custom build exception class that contains a message
class Accountant
    Transaction _transactions[]
    Trip _tdy

    method __init__()
    method get_transaction_value(variable_name, transaction_index)
    method get_trip_value(variable_name)
    static method convert_to_date(d)
    method trip_parameters_set()
    method load_data()
    method save_data()
    method set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
    method calculate_trip_duration()
    method calculate_per_diem_total()
    method add_transaction(name, transaction_date, amount, remarks)
    method find_transaction(find_me)
    method calculate_total_spent()
    method calculate_earned_per_diem()
    method modify_transaction(transaction_number, name, transaction_date, amount, remarks)
    method num_transactions()
class Transaction
    String name
    Date transaction_date
    Decimal amount
    String remarks

    method __init__(name, transaction_date, amount, remarks)
class Trip
    Date _begin_date
    Date _end_date
    Decimal _daily_per_diem
    Devimal _travel_per_diem

    method set_per_diem(daily_per_diem, travel_per_diem)
    method set_dates(begin_date, end_date)
    method retrieve_values()
    method dates_set()
    method per_diem_values_set()
    method calculate_duration()
    method calculate_per_diem_total()
    method calculate_earned_per_diem()
"""

class InvalidOperationError(Exception):  # exception class
    def __init__(self, message):
        self.message = message

class UserQuitException(Exception): # exception class
    def __init__(self, message):
        self.message = message

class Accountant:
    # Class contains transaction and perdiem data and performs operations on them

    def __init__(self):
        self._transactions = []
        self._tdy = Trip() # create Trip object with dummy values (values will be set later)

    def get_transaction_value(self, variable_name, transaction_index):
        """
        This function is a one stop shop for necessary variable data
        Input
            variable_name - name of the variable caller wants a value for
                possibilities include: "begin date", "end date" "daily per diem" "travel per diem"
            transaction_index = 0 - which transaction the caller wants values for
        Return
            value of variable requested
        Throws
            value error if name is incorrect
        """
        # step 1: create a check to ensure transaction_index is not out of bounds of existing transactions
        in_list_bounds = transaction_index < len(self._transactions)

        # step 2: if not in bounds, raise an exception
        if not in_list_bounds:
            raise ValueError("Debug Error: Accountant.get_transaction_value requested transaction does not exist")

        # step 3: check which variable to caller is asking for and return that value
        if variable_name == "name":
            return self._transactions[transaction_index].name
        elif variable_name == "date":
            return self._transactions[transaction_index].transaction_date
        elif variable_name == "amount":
            return self._transactions[transaction_index].amount
        elif variable_name == "remarks":
            return self._transactions[transaction_index].remarks
        else: # step 4: if none of the previous checks are correct, the caller isn't asking for a valid variable
            raise ValueError("Debug error: Accountant.get_transaction_value variable does not exist")

    def get_trip_value(self, variable_name):
        """
        This function is a one stop shop for necessary variable data
        Input
            variable_name - name of the variable caller wants a value for
            possibilities include: "begin date", "end date" "daily per diem" "travel per diem"
            trip_index = 0 - which trip the caller wants values for
        Return
            value of variable requested
        Throws
            value error if name is incorrect
        """

        # step 1: pull dictionary variable containing trip's values from Trip method
        pulled_values = self._tdy.retrieve_values()

        # step 2: determine what caller is asking for and return that value
        try:
            if variable_name == "begin date":
                return pulled_values['begin_date']
            elif variable_name == "end date":
                return pulled_values['end_date']
            elif variable_name == "daily per diem":
                return pulled_values['daily_per_diem']
            elif variable_name == "travel per diem":
                return pulled_values['travel_per_diem']
            else: # step 3: handle error scenarios
                raise InvalidOperationError("Debug error: Accountant.get_trip_values: trip variable does not exist")
        except InvalidOperationError as e:
            raise e

    @staticmethod  # This means we can call the method without initializing an object
    def convert_to_date(d):
        """
        This function accepts a date and attempts to convert it to date object
        Input
            d - the date string to convert to a date object.  Must be military time
        Returns
            date object
        Throws
            value error if date can't be converted
        """

        # step 1: ensure method parameter is an integer
        try:
            begging_value = int(d)
        except ValueError as e:
            raise e

        # step 2: convert the method parameter to a string
        working_value = str(begging_value)

        # step 3: cut up string into year, month and day segments
        try:
            result = date(int(working_value[:4]), int(working_value[4:6]), int(working_value[6:]))
        except ValueError as e:  # step 4: raise value error if number can't be parsed into a date
            raise e

        # step 5: return resulting date object
        return result

    def trip_parameters_set(self):
        """
    Determines whether a trip's date and per diem values have been set
    Input
        none
    Returns
        answer - boolean value indicating whether the trip has values
    Throws
        none
        """
        # step 1: combine dates_set() and per_diem_values_set() with "and".  If either is false, method returns false.
        return self._tdy.dates_set() and self._tdy.per_diem_values_set()

    def load_data(self):
        """
        This function loads data from the file ledger.txt
        Input
            none
        Returns
            none
        Throws
            Invalid operation error if ledger.txt is not found
        """

        # step 1: open the file in read only mode
        try:
            file = open("ledger.txt", "r")
        except IOError:  # todo: incorporate better "file missing" logic
            raise InvalidOperationError("Ledger.txt not found")

        # step 2: read each line of the file into an array
        file_data = []  # this is the array we will read all data into

        for line in file:
            file_data.append(line)

        # step 3: close the file
        file.close()

        # todo: check file inputs for bad data and raise ValueError exception if necessary
        # todo: parse all file data before loading any of it into accountant object
        try:
            temp = file_data[0]
            begin_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))

            temp = file_data[1]
            end_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))


            travel_per_diem = Decimal(file_data[2])
            daily_per_diem = Decimal(file_data[3])

            # step 5: set per diem and dates values in default TDY
            self._tdy.set_per_diem(daily_per_diem, travel_per_diem)
            self._tdy.set_dates(begin_date, end_date)

            # step 6: iterate through each transaction pulled from the file
            i = 4  # index number,starts after previous reads for trip data is done
            while i + 4 <= len(file_data):  # continue until file_data is out of records
                # store next transaction's name and increment index
                name = file_data[i]
                name = name[:-1]  # this cuts off the newline character
                i += 1

                # store transaction date and increment index
                temp = file_data[i]
                transaction_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))
                i += 1

                # store transaction amount and increment index
                amount = Decimal(file_data[i])
                i += 1

                # store transaction remarks and increment index
                remarks = file_data[i]
                remarks = remarks[:-1]  # this cuts off the newline character
                i += 1

                # step 7: add pulled transaction data to new transaction
                self.add_transaction(name, transaction_date, amount, remarks)
        except IndexError as e:
            raise e

    def save_data(self):
        """
        This function saves data to the file ledger.txt
        Input
            none
        Returns
            none
        Throws
            Invalid Operation error if tdy is not initialized
        """

        # step 1: open file ledger.txt in write mode
        file = open("ledger.txt", "w")

        # step 2: write beginning and end date along with per diem values
        try:
            pulled_values = self._tdy.retrieve_values()
            file.write(pulled_values['begin_date'].strftime("%Y%m%d") + "\n")
            file.write(pulled_values['end_date'].strftime("%Y%m%d") + "\n")
            file.write(str(pulled_values['travel_per_diem']) + "\n")
            file.write(str(pulled_values['daily_per_diem']) + "\n")
        except InvalidOperationError as e:  # Trip.retrieve values can throw exception if object is not initialized
            raise e

        # step 3: loop through each transaction and write their values
        i = 0
        while True:
            if i >= len(self._transactions):
                break

            file.write(self._transactions[i].name + "\n")
            file.write(str(self._transactions[i].transaction_date.strftime("%Y%m%d")) + "\n")
            file.write(str(self._transactions[i].amount) + "\n")
            file.write(str(self._transactions[i].remarks) + "\n")

            i += 1

        # step 4: close the file
        file.close()

    def set_per_diem_data(self, begin_date, end_date, travel_per_diem, daily_per_diem):
        """
        Function sets per diem data for a trip
        Input
            date and per diem values to pass to Trip object
        Returns
            none
        Throws
            Value errors if bad data is passed to the program
        """
        # step 1: sanitize date values
        if not isinstance(begin_date, date) or not isinstance(end_date, date):
            raise InvalidOperationError("Debug error: dates provided to Bank.setperdiemdata are not correct type")
        if end_date <= begin_date:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: end date is <= to begin date")

        # step 2: sanitize per diem values
        if not isinstance(travel_per_diem, Decimal) or not isinstance(daily_per_diem, Decimal):
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data provided are not Decimal")
        if travel_per_diem < 0 or daily_per_diem < 0:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data not valid")

        # step 3: set tdy values by calling Trip object methods
        try:
            self._tdy.set_per_diem(daily_per_diem, travel_per_diem)
            self._tdy.set_dates(begin_date, end_date)
        except ValueError as e:
            raise e

    def calculate_trip_duration(self):
        """
        Function returns the duration of the TDY
        Input
            none
        Returns
            duration of trip
        Throws
            Invalid Operation Error if trip is not initialized
        """

        # step 1: call upon Trip object to calculate own duration
        try:
            result = self._tdy.calculate_duration()
        except InvalidOperationError as e:  # this exception occurs if Trip object's dates have not been set
            raise e

        # step 2: return the result
        return result

    def calculate_per_diem_total(self):
        """
        Method returns the amount of per diem for the a Trip object
        Input
            trip_index=0 - indicates which Trip object to perform calculations on
        Returns
            total per diem for trip
        Throws
            Invalid Operation Error dates or per diem totals have not been set
        """

        # step 1: call on Trip object to calculate its own per diem total
        try:
            total = self._tdy.calculate_per_diem_total()
        except InvalidOperationError as e: # exception occurs if Trip object date or per diem values not set
            raise e

        # step 2: return the total per diem
        return total

    def add_transaction(self, name, transaction_date, amount, remarks):
        """
        Adds a single transaction to Transaction array
        Input
            name - the name of the transaction
            transaction_date - the date of the transaction
            amount - the amount of the transaction
            remarks - remarks for the transaction
        Returns
            index of new transaction's location
        Throws
            Invalid Operation Error if parameters are not valid
            Value Error if attempted duplicate transaction
        """
        # step 1: create new Transaction object and append to Transaction array
        try:
            new_transaction = Transaction(name, transaction_date, amount, remarks)

            # detect duplicate transaction
            self.find_transaction(new_transaction)

            self._transactions.append(new_transaction)

            # step 2: sort the transactions by date
            self._transactions = sorted(self._transactions, key=lambda Transaction: Transaction.transaction_date)

            return self.find_transaction(new_transaction)

        except InvalidOperationError as e: # most likely a duplicate transaction
            raise e

    def find_transaction(self, find_me):
        """
        Finds a transaction and returns it's location in the list
        params: find_me -- the transaction object to find
        returns: location as an integer
        Throws: ValueError if param is not transaction or transaction is not found
        """
        # todo: test function

        # initialize variables
        result = -1 # stores find_me's location
        temp_index = 0 # keeps track of our location in the list

        # check find_me is valid Transaction object
        if not isinstance(find_me, Transaction):
            raise ValueError("Accountant.find_transaction param not valid")

        # iterate over list of transactions to find find_me
        for transaction in self._transactions:
            amount_same = transaction.amount == find_me.amount
            date_same = transaction.transaction_date == find_me.transaction_date
            amount_same = transaction.amount == find_me.amount
            remarks_same = transaction.remarks == find_me.remarks

            if amount_same and date_same and amount_same and remarks_same:
                if not result == -1: # case that we have already found the transaction
                    raise InvalidOperationError("Error: duplicate transactions exist")
                result = temp_index
                temp_index += 1
            else:
                temp_index += 1

        return result

    def calculate_total_spent(self):
        """
        Sums the amount parameter in all transactions and returns the result
        Input
            none
        Returns
            sum of all Transactions amount
        Throws
            none
        """

        # step 1: initialize placeholder for result
        total = 0

        # step 2: iterate through each transaction and add each amount to the total
        for t in self._transactions:
            total = total + t.amount

        # step 3: return the total
        return total

    def calculate_earned_per_diem(self):
        """
        Calls Trip object to calculate how much per diem we have earned based on the current date
        Input
            none
        Returns
            earned per diem
        Throws
            none
        """

        # step 1: have the Trip object do the calculation and return the result
        return self._tdy.calculate_earned_per_diem()

    def modify_transaction(self, transaction_number, name, transaction_date, amount, remarks):
        """
        Changes a transaction
        Input
            transaction_numer - index of transaction we want to modify
            name - new transaction name
            transaction_date - new transaction date
            amount - new transaction amount
            remarks - new transaction remarks
        Returns
            none
        Throws
            InvalidOperationError if transaction object index is out of range of current transaction array
        """
        # todo: function testing

        # step 1: check that transaction index number is not out of array range
        if len(self._transactions) < transaction_number:
            raise InvalidOperationError("transaction number out of range")

        # step 1.1: check for duplicate transaction
        new_transaction = Transaction(name, transaction_date, amount, remarks) # this will throw an exception if duplicate

        try:
            self.find_transaction(new_transaction) # find where the current transaction is
        except InvalidOperationError as e:
            raise e

        # Step 2: remove old transaction
        self._transactions.remove(self._transactions[transaction_number - 1])

        # Step 3: use bank's own add_transaction function to add transaction
        self.add_transaction(new_transaction.name, new_transaction.transaction_date, new_transaction.amount, new_transaction.remarks)

        # Step 4: sort with the new transactions
        self._transactions = sorted(self._transactions, key=lambda Transaction: Transaction.transaction_date)

        return self.find_transaction(new_transaction)

    def num_transactions(self):
        return len(self._transactions)

class Transaction:
    # Class contains data for individual _transactions
    # Data: date, name, amount, remarks
    def __init__(self, name, transaction_date, amount, remarks):
        # first step: sanitize input
        # todo: change InvalidOperationErrors to ValueErrors
        if isinstance(amount, int): # if amount is an integer, we can convert it to a Decimal
            amount = Decimal(amount)

        if not isinstance(name, str) or not isinstance(amount, Decimal) or not isinstance(remarks, str):
            raise InvalidOperationError("Debug error: Transaction init; values passed not valid type")
        if not isinstance(transaction_date, date):
            raise InvalidOperationError("Debug error: Transaction init; values passed not valid type")

        if not amount > 0:
            raise InvalidOperationError("Debug error: Transaction init; amount not greater than 0")

        # set object values
        self.name = name
        self.transaction_date = transaction_date
        self.amount = amount
        self.remarks = remarks

class Trip:
    # Class contains beginning and end dates of a trip, per diem info and calculations
    def __init__(self, begin_date = date(1950, 1, 1) , end_date = date(1950, 1, 1), daily_per_diem = -1, travel_per_diem = -1):
        self._begin_date = begin_date
        self._end_date = end_date
        self._daily_per_diem = daily_per_diem
        self._travel_per_diem = travel_per_diem

    def set_per_diem(self, daily_per_diem, travel_per_diem):
        """
        Function used to set optional per diem values
        parameters: Decimal daily_per_diem and travel_per_diem
        throws Value error if parameters are not Decimal
        returns: none
        """
        # step 1: make sure per diem values provided to function are integers or Decimal
        if (not isinstance(daily_per_diem, Decimal) and not isinstance(daily_per_diem, int)) or (not isinstance(travel_per_diem, Decimal) and not isinstance(travel_per_diem, int)):
            raise ValueError('Debug error: Trip.set_per_diem; values passed not Decimal or int')

        # step 2: make sure the per diem values provided to function make sense (not negative)
        if daily_per_diem < 0 or travel_per_diem < 0:
            raise ValueError('Debug error: Trip.set_per_diem; values passed must be positive')

        # step 3: store per diem values as Decimals
        self._daily_per_diem = Decimal(daily_per_diem)
        self._travel_per_diem = Decimal(travel_per_diem)

    def set_dates(self, begin_date, end_date):
        """
        Function used to set begin and end dates
        parameters: Date objects for the beggining and end dates of trip
        throwns: ValueError if parameters are not date objects
        returns: none
        """
        # step 1: ensure that parameters provided are Date objects
        if not isinstance(begin_date, date) or not isinstance(end_date, date):
            raise ValueError('Debug error: Trip.set_dates; error: parameters provided not date objects')

        # step 2: ensure that begin_date and end_dates make sense
        if end_date <= begin_date:
            raise ValueError('Debug error: Trip.set_dates; error: trip end date should be after begin date')

        # step 3: set begin and end dates to provided values
        self._begin_date = begin_date
        self._end_date = end_date

    def retrieve_values(self):
        """
        Function used to retrieve all values from the Trip.
        parameters: none
        returns: dictionary containing all values.  These values can be modified without affecting object's variables
        throws: none
        """
        # step 1: make sure Trip object has been initialized (provided legit values for)
        if not self.dates_set():
            raise InvalidOperationError('Debug error: Trip.retrieve_values; error:attempted to retrieve vales before '
                                        'object is initialized')

        # step 2: create a dictionary with date objects belonging to Trip object
        values = {'begin_date': self._begin_date, 'end_date': self._end_date}

        # step 2: if per diem values are set, include those as well
        if self.per_diem_values_set():
             values['daily_per_diem'] = self._daily_per_diem
             values['travel_per_diem'] = self._travel_per_diem

        # step 3: return dictionary to caller
        return values

    def dates_set(self):
        """
        Function used to determine whether Trip object has been provided proper dates
        parameters: none
        returns: boolean indicating if object is initialized
        throws: none
        """
        # step 1: check all mandatory variables against the default values to make sure some value has been provided to it
        # the only mandatory variables are the begin_date and the end_date, as of right now
        if self._begin_date == date(1950, 1, 1) or self._end_date == date(1950, 1, 1):
            return False

        # step 2: if you make it past that first check, values are good and we return true
        return True

    def per_diem_values_set(self):
        """
        Function check per diem values to see if they have been set
        parameters: none
        returns: boolean indicating if per diem values have been set
        throws: none
        """
        # step 1: check per diem values against defaults
        if self._daily_per_diem == -1 or self._travel_per_diem == -1:
            return False

        # step 2: if we got past the first check, we must be good
        return True

    def calculate_duration(self):
        """
        Method returns the duration of this TDY
        Input
            none
        Returns
            duration of trip
        Throws
            Invalid Operation Error if object is not initialized
        """
        # step 1: check if trip object is initialized
        if not self.dates_set():
            raise InvalidOperationError("Debug error: Trip.calculate_duration() trip dates not set")

        # Create timedelta object that is the difference between two dates
        result = self._end_date - self._begin_date

        # Result will be short one day, so we create a timedelta object of one day
        modification = timedelta(days=1)

        # Finally, we add modification to result
        result = result + modification

        return result

    def calculate_per_diem_total(self):
        """
        Method returns the amount of per diem for a trip object
        Input
            none
        Returns
            total per diem for trip
        Throws
            Invalid Operation Error dates or per diem totals have not been set
        """
        # step 1: ensure dates and per diem values have been set
        if not self.dates_set() or not self.per_diem_values_set():
            raise InvalidOperationError("Debug Error: Trip.calculate_per_diem_total() dates/perdiem not set")

        # step 2: double the travel per diem total
        total = self._travel_per_diem * 2

        # step 3: calculate the duration of the trip
        duration = self.calculate_duration().days

        # step 4: multiply the duration by the daily per diem
        total += (duration - 2) * self._daily_per_diem

        # step 5: return the total per diem
        return total

    def calculate_earned_per_diem(self):
        """
        Calculates how much per diem we have earned based on the current date
        Params:
            none
        Returns:
            earned per diem as double
        Throws: InvalidOperationError if trip not initialized correctly
        """

        # check if tdy is in a valid state
        if not self.dates_set() or not self.per_diem_values_set():
            raise InvalidOperationError("Debug Error: Trip.calculate_earned_per_diem -- trip object not in valid state")

        # initialize variabels
        total = 0

        # if tdy hasn't started yet, return 0
        if date.today() < self._begin_date:
            return 0

        # if the entire tdy has passed, return the total
        if date.today() >= self._end_date:
            return self.calculate_per_diem_total()

        # based on our previous checks, today must be on, or after, the first travel day
        total += self._travel_per_diem

        # calculate how many days have transpired (not including the first travel day)
        time_spent = date.today() - self._begin_date
        # note: because of the way dates are subtracted, it will be short 1 day. In this function, that
        # missing day is treated as the first travel day, making the calculations work.
        days = time_spent.days

        # multiple days by daily_per_diem and add to total
        total += (self._daily_per_diem * days)

        return total
