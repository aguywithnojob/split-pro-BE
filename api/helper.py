import datetime

# function convert epoch to datetime format "6 Nov, 12:14 AM"
def convert_epoch_to_datetime(epoch):
    dt = datetime.datetime.fromtimestamp(epoch)
    formatted_dt = dt.strftime("%d %b, %I:%M %p")
    return formatted_dt