#Code starts here

import pprint
from operator import itemgetter
from random import shuffle

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
	time = int(time)
	return (time//100)*60 + (time%100)

def MilitaryTime(time):
	return (time//60)*100 + time%60

'''def CalculateArrivalTime(origin,destination,departureTime):
	return MilitaryTime(fly_time(origin,destination)+MinutesSinceMidnight(departureTime))'''

'''def CalculateDepartureTime(origin,arrivalTime):
	return MilitaryTime(MinutesSinceMidnight(arrivalTime) + CalculateGroundTime(origin))'''

def CalculateGroundTime(origin):
	if origin == 'AUS':return 25
	elif origin == 'DAL':return 30
	elif origin == 'HOU':return 35  

class Airport_Status:
	def __init__(self,airportName,noOfGates,gateStatus):
		self.airportName = airportName
		self.noOfGates = noOfGates
		self.gateStatus = gateStatus

class Flight_Status:
	def __init__(self,tailNumber,currentAirport,time,updated):
		self.tailNumber = tailNumber
		self.currentAirport = currentAirport
		self.time = time
		self.updated = True

def check_Availability(origin,destination,time,Airports):
	time = int(time)
	i = 1
	value = False
	time_available = MilitaryTime(fly_time(origin,destination) + MinutesSinceMidnight(time))
	#print(time_available)
	for port in Airports:
		if port.airportName == destination:
			for status in port.gateStatus:
				if int(status[0]) <= time_available and int(status[1]) >= time_available:
					#return (True,i)
					value = True
					break
				else:
					i +=1
					value= False
	return value,i,str(time_available).rjust(4,'0')

def update_Airport_Status(airport, i, fly_time):
	
	value = MilitaryTime(MinutesSinceMidnight(int(fly_time)) + \
									CalculateGroundTime(airport.airportName)+5)
	if value < 2200:
		airport.gateStatus[i-1][0] = str(value).rjust(4,'0')
	else:
		pass


def update_flight_status(fl,airportName,fly_time):
	fl.currentAirport = airportName
	fl.time = str(MilitaryTime(MinutesSinceMidnight(int(fly_time)) + \
									CalculateGroundTime(airportName))).rjust(4,'0')
	fl.updated = True
	#print(fl.time)

def update_leftout_flight(fl):
	value = MilitaryTime(MinutesSinceMidnight(int(fl.time)) + \
									2*CalculateGroundTime(fl.currentAirport))
	fl.time = str(value).rjust(4,'0')
	fl.updated = True
	'''if value <= 2200:
		fl.time = str(value).rjust(4,'0')
		fl.updated = True
		else:pass'''

def check_allflight_status(Flights):
	for x in Flights:
		#print(x.time)
		if int(x.time) >= 2200:
			#print('Flight that returned False: ',x.tailNumber,x.time)
			return False
			break
		else:return True

def lineup_flights(Flights,Airports):
	count=dict.fromkeys(['AUS','DAL','HOU'],0)
	flt_last_schedule =  list()
	#for fl in Flights:
	#	print(fl.tailNumber,fl.updated,fl.time,fl.currentAirport)
	for ap in Airports:
		#print("Airport: ",ap.airportName)
		for fl in Flights:
			#print("Flight: ",fl.currentAirport)
			#print(count.get(fl.currentAirport,0))
			if ap.airportName == fl.currentAirport:
				count[ap.airportName] = count.get(fl.currentAirport,0) + 1
				#print(count.get(fl.currentAirport,0))
	#pprint.pprint(count)
	if count['AUS']>1:
		#print('AUS has {0} flight'.format(count['AUS']))
		for x in range(count['AUS']-1):
			fs_last = list()
			#print(x)
			if count['HOU']<3:
				for fl in Flights:
					if fl.currentAirport == 'AUS' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('AUS'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('AUS','HOU'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'HOU',departureTime,arrivalTime))
						#print(fs_last)
						count['HOU']+=1
						count['AUS']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)
			else:
				for fl in Flights:
					if fl.currentAirport == 'AUS' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('AUS'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('AUS','DAL'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'DAL',departureTime,arrivalTime))
						#print(fs_last)
						count['DAL']+=1
						count['AUS']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)

	if count['DAL']>2:
		#print('DAL has {0} flight'.format(count['DAL']))
		for x in range(count['DAL']-2):
			fs_last = list()
			#print(x)
			if count['HOU']<3:
				for fl in Flights:
					if fl.currentAirport == 'DAL' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('DAL'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('DAL','HOU'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'HOU',departureTime,arrivalTime))
						#print(fs_last)
						count['HOU']+=1
						count['DAL']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)
			else:
				for fl in Flights:
					if fl.currentAirport == 'DAL' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('DAL'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('DAL','AUS'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'AUS',departureTime,arrivalTime))
						#print(fs_last)
						count['AUS']+=1
						count['DAL']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)
									

	if count['HOU']>3:
		#print('HOU has {0} flight'.format(count['HOU']))
		for x in range(count['HOU']-3):
			fs_last = list()
			#print(x)
			if count['DAL']<2:
				for fl in Flights:
					if fl.currentAirport == 'HOU' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('HOU'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('HOU','DAL'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'DAL',departureTime,arrivalTime))
						#print(fs_last)
						count['DAL']+=1
						count['HOU']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)
			else:
				for fl in Flights:
					if fl.currentAirport == 'HOU' and fl.updated is True:
						departureTime = str(MilitaryTime(MinutesSinceMidnight(fl.time) + \
											CalculateGroundTime('HOU'))).rjust(4,'0')
						arrivalTime = str(MilitaryTime(MinutesSinceMidnight(departureTime) + \
																		fly_time('HOU','AUS'))).rjust(4,'0')
						fs_last.extend((fl.tailNumber,fl.currentAirport,'AUS',departureTime,arrivalTime))
						#print(fs_last)
						count['AUS']+=1
						count['HOU']-=1
						fl.updated = False
						break
				if len(fs_last)!=0:flt_last_schedule.append(fs_last)
	#print('New Dictionary:')
	#pprint.pprint(count)
	#print(flt_last_schedule)
	#for fl in Flights:
	#	print(fl.tailNumber,fl.updated,fl.time,fl.currentAirport)
	#for ap in Airports:
	#	print(ap.gateStatus,ap.airportName)
	return flt_last_schedule


def update_last_flightStatus(flt_schedule,Flights):
	for fl in Flights:
		fl.updated = False
		#print(fl.tailNumber,fl.updated,fl.time,fl.currentAirport)
		for fs in flt_schedule:
			if fs[0]==fl.tailNumber and fl.updated is False:
				fl.updated= True
				fl.currentAirport = fs[2]
				fl.time = fs[4]
				break
			else:continue
	#for fl in Flights:
 	#	print(fl.tailNumber,fl.updated,fl.time,fl.currentAirport)

AUS = Airport_Status('AUS',1,[['0601','2000']])
DAL = Airport_Status('DAL',2,[['0601','2000'],['0601','2000']])
HOU = Airport_Status('HOU',3,[['0601','2000'],['0601','2000'],['0601','2000']])

Airports = [AUS,DAL,HOU]

t1 = Flight_Status('T1','AUS','0600',True)
t2 = Flight_Status('T2','DAL','0600',True)
t3 = Flight_Status('T3','DAL','0600',True)
t4 = Flight_Status('T4','HOU','0600',True)
t5 = Flight_Status('T5','HOU','0600',True)
t6 = Flight_Status('T6','HOU','0600',True)

Flights = [t1,t2,t3,t4,t5,t6]

flt_schedule = list()

def create_flight_schedule(Flights,Airports):
	while check_allflight_status(Flights):
		shuffle(Airports)
		for fl in Flights:
			fs = list()
			fl.updated = False
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
						#print(fl.tailNumber,fl.currentAirport,fl.time,fl.updated)
						#print(fs)
						break
			if len(fs)!=0 and int(fl.time)<=2200:flt_schedule.append(fs)
			if fl.updated is False:update_leftout_flight(fl)
		#print(check_allflight_status(Flights))
	update_last_flightStatus(flt_schedule[::-1],Flights)
	flt_last_schedule = lineup_flights(Flights,Airports)
	for x in flt_last_schedule:
		flt_schedule.append(x)
	flt_schedule.sort(key=itemgetter(0,3))
	#print('')
	#update_last_flightStatus(flt_schedule[::-1],Flights)
	#pprint.pprint(flt_schedule)
	print_flight_schedule(file_name, csv_header, flt_schedule)

create_flight_schedule(Flights,Airports)

									 

