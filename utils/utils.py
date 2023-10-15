def msToTime(duration: int) -> str:
	seconds = duration / 1000
	minutes = seconds / 60
	hours = minutes / 60
	days = hours / 24

	if days >= 1:
		return f"{int(days)}d {int(hours % 24)}h {int(minutes % 60)}m"
	elif hours >= 1:
		return f"{int(hours)}h {int(minutes % 60)}m"
	elif minutes >= 1:
		return f"{int(minutes)}m"
	else:
		return f"1m"
