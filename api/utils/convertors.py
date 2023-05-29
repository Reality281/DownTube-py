def convertTime(sec):
	time = ''
	dur = {
		'Years': 365 * 24 * 3600,
		'Days': 24 * 3600,
		'Hours': 3600,
		'Minutes': 60
    }
	for d in dur.keys():
		if int(sec) // dur[d]:
			time += f"{sec//dur[d]} {d} "
			sec %= dur[d]
	if sec:
		time += f"{sec} Seconds"
	return time

def convertViews(view):
	views = {'Crore': 10000000, 'Lakh': 100000, 'Thousand': 1000}
	for v in views.keys():
		if isinstance(view, int):
			if view // views[v]:
				view = f"{round(view/views[v], 1)} {v}"
	return view