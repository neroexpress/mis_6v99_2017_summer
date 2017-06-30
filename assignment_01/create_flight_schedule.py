#Code starts here

csv_header = 'tail_number,origin,destination,departure_time,arrival_time' 
file_name = 'flight_schedule.csv'

def print_flight_schedule(fn, csv_hdr, flt_sched):
    with open(fn,'wt') as f:
        print(csv_hdr, file=f)
        for s in flt_sched:
            print(','.join(s), file=f)

flight_times = [['AUS','DAL',50],
                ['DAL','HOU',65],
                ['AUS','HOU',45]]

def fly_time(origin,dest):
    fly_time =0
    for lst in flight_times:
        if (lst[0] == origin and lst[1]==dest) or (lst[1] == origin and lst[0]==dest):
            fly_time = lst[2]
            break;
    return fly_time

def MinutesSinceMidnight(time):
    return (time//100)*60 + (time%100)

def MilitaryTime(time):
    return (time//60)*100 + time%60

def CalculateArrivalTime(origin,destination,departureTime):
    return MilitaryTime(fly_time(origin,destination)+MinutesSinceMidnight(departureTime))

def CalculateGroundTime(origin):
    if origin == 'AUS':return 25
    elif origin == 'DAL':return 30
    elif origin == 'HOU':return 35

def CalculateDepartureTime(origin,arrivalTime):
    return MilitaryTime(MinutesSinceMidnight(arrivalTime) + CalculateGroundTime(origin))   

class Airport_Status:
    def __init__(self,airportName,noOfGates,gateStatus):
        self.airportName = airportName
        self.noOfGates = noOfGates
        self.gateStatus = gateStatus


class Flight_Status:
    def __init__(self,tailNumber,currentAirport,time):
        self.tailNumber = tailNumber
        self.currentAirport = currentAirport
        self.time = time

def check_Availability(origin,destination,time,Airports):
    time = int(time)
    i = 1
    value = False
    time_available = MilitaryTime(fly_time(origin,destination) + MinutesSinceMidnight(time))
    #print(time_available)
    for port in Airports:
        if port.airportName == destination:
            for status in port.gateStatus:
                if int(status[0]) <= time_available:
                    #return (True,i)
                    value = True
                    break
                else:
                    i +=1
                    value= False
    return value,i,str(time_available).rjust(4,'0')

def update_Airport_Status(airport, i, fly_time):
    
    airport.gateStatus[i-1][0] = MilitaryTime(MinutesSinceMidnight(int(fly_time)) + \
                                    CalculateGroundTime(airport.airportName))
    #print(str(airport.gateStatus[i-1][0]).rjust(4,'0'))
    airport.gateStatus[i-1][0] = str(airport.gateStatus[i-1][0]).rjust(4,'0')

def update_flight_status(fl,airportName,fly_time):
    fl.currentAirport = airportName
    fl.time = MilitaryTime(MinutesSinceMidnight(int(fly_time)) + \
                                    CalculateGroundTime(airportName))
    #print(fl.time)

flt_schedule = list()

AUS = Airport_Status('AUS',1,[['0600','2200']])
DAL = Airport_Status('DAL',2,[['0600','2200'],['0600','2200']])
HOU = Airport_Status('HOU',3,[['0600','2200'],['0600','2200'],['0600','2200']])

Airports = [AUS,DAL,HOU]

t1 = Flight_Status('T1','AUS','0600')
t2 = Flight_Status('T2','DAL','0600')
t3 = Flight_Status('T3','DAL','0600')
t4 = Flight_Status('T4','HOU','0600')
t5 = Flight_Status('T5','HOU','0600')
t6 = Flight_Status('T6','HOU','0600')

Flights = [t1,t2,t3,t4,t5,t6]


def create_schedule(Flights,Airports):
    for fl in Flights:
        fs = list()
        for airport in Airports:
            #print(airport.airportName)
            if fl.currentAirport != airport.airportName:
                (value , i, fly_time) = check_Availability(fl.currentAirport,airport.airportName,fl.time,Airports)
                #print(airport.gateStatus,airport.airportName)
                #print(value , i, fly_time)
                if value is True:
                    fs.extend((fl.tailNumber,fl.currentAirport,airport.airportName,fl.time,fly_time))
                    #print(airport.gateStatus,airport.airportName)
                    update_Airport_Status(airport,i,fly_time)
                    #print(airport.gateStatus,airport.airportName)
                    update_flight_status(fl,airport.airportName,fly_time)
                    #print(fl.tailNumber,fl.currentAirport,fl.time)
                    break
        #print(fs)
        if len(fs)!=0:flt_schedule.append(fs)
    print(flt_schedule)
    print_flight_schedule(file_name, csv_header, flt_schedule)

create_schedule(Flights,Airports)

                                     

