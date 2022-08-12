# list of zipcodes
from zipcodes import zipcodes as data

# to make web request in real-time
import requests

# to plot graph
import matplotlib.pyplot as plt

# for MultipleLocator on x-axis
from matplotlib.ticker import (MultipleLocator)

zipcode = input('Please enter a City of Chicago zip code: ')

if zipcode not in data:
	print("Data for this zip code is not available.")
	quit()

else:
	url = "https://data.cityofchicago.org/resource/553k-3xzc.json?$order=date&zip_code="

	# concatenate both strings for zipcode-specific data
	new_url = url + zipcode

	# make web request and store data
	get_data = requests.get(new_url)

	# convert data into python object (lists/dictionaries)
	covid_data = get_data.json()

	#print(covid_data)

	# empty lists
	dates = []
	daily_doses = []
	total_doses = []

	for i in range(len(covid_data)):
		# access 'date' key in each dictionary in the list
		#print(covid_data[i]['date'])

		# split date and time values
		rmv_time = covid_data[i]['date'].split("T")

		# add only date value to empty 'dates' list for better readability on x-axis
		dates.append(rmv_time[0])

		# access 'total_doses_daily' key in each dictionary in the list, convert to float value, add to empty 'daily_doses' dictionary
		daily_doses.append(float(covid_data[i]['total_doses_daily']))

		# access 'total_doses_cumulative' key in each dictionary in the list, convert to float value, add to empty 'total_doses' dictionary
		total_doses.append(float(covid_data[i]['total_doses_cumulative']))

	#print(dates)
	#print(doses)

	# assign figure and axes to two variables to later access x-axis & y-axis seperately
	fig, ax = plt.subplots()

	# ax is by default the left; didn't add new subplot
	left_axis = ax
	right_axis = left_axis.twinx()

	# graph data (x,y)
	blueline, = left_axis.plot(dates, daily_doses)
	redline, = right_axis.plot(dates, total_doses,
	                           'r-')  # or color="red" instead of 'r'

	# set x-axis values (dates) apart by 14
	ax.xaxis.set_major_locator(MultipleLocator(21))

	# title of graph, zip code updates based on user input
	plt.title('Covid-19 Vaccinations for {}'.format(zipcode))

	# format & rotate xticks for better readability
	fig.autofmt_xdate(rotation=70)

	# legend
	plt.legend([blueline, redline], ["daily doses", "total doses"],
	           shadow=True)

	# block=True is to show graph until it's dismissed, instead of automatically ending after execution
	plt.show(block=True)
