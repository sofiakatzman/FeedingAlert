import machine
import time

# set up LEDs
red_led = machine.Pin(16, machine.Pin.OUT)
blue_led = machine.Pin(17, machine.Pin.OUT)

# set up Button
button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

# declare feeding schedule
feed_times = [(9, 00), (19, 00)]  # 9:00 AM and 7:00 PM

# alert state
alert_on = False
alert_triggered = False  # tracks if alert has yet been triggered to prevent bugs during same-alert-minute feeds

def is_feeding_time():
    current_time = time.localtime() 
    for hour, minute in feed_times:
        if current_time[3] == hour and current_time[4] == minute:
            return True
    return False

while True:
    # check if it's feeding time and if the alert has not yet been triggered
    if is_feeding_time() and not alert_triggered:
        alert_on = True  
        alert_triggered = True  

    # control the LEDs based on the alert state
    if alert_on:
        red_led.on()
        blue_led.off()
        print("It is feeding time!")
    else:
        red_led.off()
        blue_led.on()
        print("It is not yet feeding time.")

    # check if the button is pressed
    if not button.value():
        alert_on = False  
        print("Button pressed! Fed!")

    # reset slert triggered once it is no longer feeding time 
    if not is_feeding_time():
        alert_triggered = False 

    time.sleep(1)
