import re
import sys

def check_bounds(testval,  valrange):
    '''
    Test function to test whether the value falls within an acceptable range
    Args:
        testval (int): the value to be tested
        valrange (tuple): range of values that tested value can take, in the form of min, max (<= min x <= max) 
    Returns:
        boolean: indicates whether the testval is within the range specified
    Examples:
        >>> check_bounds( 15, (10,20))
    '''
    range_min, range_max = valrange
    if( range_min <= testval <=range_max):
        return (True)
    else:
        return(False)

		
def get_max_month_day( month, year):
    '''
    Given a month and year combo return the max date possible for validation
    '''
    if month ==2:
        if (year%4 ==0):
            return(29)
        else:
            return(28)
    elif (month in [4, 6, 9, 11]) :
        return(30)
    else: 
        return(31)
 
def process_dates (date_string, pattern = '(\d{2})/(\d{2})/(\d{4})', US = False):
    '''
    Args:
        date_string (string): string representation of date e.g. '10/11/2020'
        pattern (string): regex pattern to match, defaults to  '(\d{2})/(\d{2})/(\d{4})'
        US (boolean): flag indicating whether to process dates as a boolean
    Returns:
        list : list of integer [year, month, day ]
    Examples:
        >>> process_dates('10/11/2020',  '(\d{2})/(\d{2})/(\d{4})')
    ''' 
    cmp_list = [(1,31),(1,12),(1901,2999)] #list that dates are compared to
    if (US):
        cmp_list[0],cmp_list[1] = cmp_list[1],cmp_list[0]
    date_matched = re.search(pattern ,date_string)
    if( date_matched is None):
        raise Exception('could not parse date: '+date_string)
    else:
        date_components = []
        if (US):
            date_matched[1],date_matched[2] = date_matched[2], date_matched[1]
        for i in range(1,4):
            if (i ==1):
                maxday = get_max_month_day(int(date_matched[i+1]) , int(date_matched[i+2]) )
                test_res = check_bounds( int(date_matched[i]), (1, maxday))
            else:
                test_res = check_bounds( int(date_matched[i]), cmp_list[i-1])
            if (test_res is False):
                message = 'date component out of range: ' + date_matched[i] + ' in '+ date_string
                raise Exception(message)
            else:
                date_components.append(int(date_matched[i]))
    date_components = [int(dt) for dt in date_components]
    return(date_components)

def date_difference(date1, date2, enddate=False):
    '''
    Gets the difference between two dates
    Args:
        date1 (list): list of dates broken up into integer dmy components [d,m,y]
        date2 (list): list of dates broken up into integer dmy components [d,m,y]
        enddate (Boolean): whether or not the enddate is included in the calculation 1 day is added
    Returns:
        Integer difference in days
    '''
 
    startyear = int(date1[2])
    startmonth = int(date1[1])
    startday = int(date1[0])
    endyear = int(date2[2])
    endmonth = int(date2[1])
    endday = int(date2[0])
    
    #calculate the number of days that have elapsed between start and end year
    days_elapsed = 0
    for y in range (startyear, endyear+1):
        for m in range(1, 13):
            days_elapsed += get_max_month_day(m,y)

    #start date minus start of year
    time_since_start = 0
    for m in range(1,(startmonth)):
        time_since_start += get_max_month_day(m,startyear)

    #time_since_start = time_since_start + (-get_max_month_day(startmonth,startyear) + startday)
    time_since_start += startday

    #get extra days at the end of the year
    end_date_extra = 0
    for m in range(endmonth,(13)):
        end_date_extra += get_max_month_day(m,endyear)
    end_date_extra = end_date_extra + ( -endday )
    #remove the extra bits of the date
    days_elapsed= days_elapsed-(end_date_extra+time_since_start)
    if (enddate):
        return(days_elapsed)
    else:
        return(days_elapsed-1 )


def date_sub_handler(date1, date2):
    '''
    handler for dates
    '''
    date1 = process_dates(date1)
    date2 = process_dates(date2)
    date_diff = date_difference(date2, date1)
    if (date_diff == -1):
        date_diff = 0
    message = str(date_diff) +' days'
    return(message)

	
if __name__ == "__main__":
	#print('processing ', sys.argv[1],sys.argv[2])
	message = date_sub_handler(sys.argv[2],sys.argv[1])
	print(message)

