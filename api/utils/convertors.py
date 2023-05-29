def convertTime(sec):# Function to convert the duration of the video to more readable format
	time = ''
	dur = {# Dictionary to convert duration to more readable format
		'Years': 365 * 24 * 3600,
		'Days': 24 * 3600,
		'Hours': 3600,
		'Minutes': 60
    }
	for d in dur.keys():# Iterating through the 'dur' dictionary keys
		if int(sec) // dur[d]:# Dividing the duration by the value of the 'dur' dictionary
			time += f"{sec//dur[d]} {d} "# If the duration completely divides then adding that more readable format to the 'time' variable
			sec %= dur[d]# Removing the amount of seconds converted into more readable format to not make it repeat and ruin the format
	if sec:# Checking if converting the format converted it competely to more readable format or if some seconds are left
		time += f"{sec} Seconds"# If seconds are left them adding them to the 'time' variable
	return time# Returning the duration of the video after convertion

def convertViews(view):# Function to convert the number of views to more readable format
	views = {'Crore': 10000000, 'Lakh': 100000, 'Thousand': 1000}# Dictionary to convert the number of views to more readable format
	for v in views.keys():# Iteration through the 'views' dictionary keys
		if isinstance(view, int):# Checking if the the 'view' variable is an interger or not
			if view // views[v]:# If the 'view' variable is an integer than dividing the number of views by the value of the 'views' dictionary
				view = f"{round(view/views[v], 1)} {v}"# If the number of views completely divides then converting the number of views to more readable format 
	return view# Returning the number of views of the video after convertion