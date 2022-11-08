from math import dist
import RPi.GPIO as GPIO         
import time                     # importing the time library to use the sleep function to give a delay in between the progeam 

GPIO.setmode(GPIO.BOARD)         # to use the pins of raspberry pi according to the numbering

GPIO_TRIG = 7           # initialising the pin number 7 on RPi as trigger which is used to trigger the ultrasonic wave
GPIO_ECHO = 8           # initialising the pin number 8 as echo as it will be used to recieve the wave
led = 33

GPIO.setup(33, GPIO.OUT)        # to set the pin number 12 on RPi as an output pin
pwm_led = GPIO.pwm_led(33, 200)         # initializing Pulse With Modulation on pin number 12 with a frequency of 200Hz

GPIO.setup(GPIO_TRIG, GPIO.OUT)     # to set the trig pin as output
GPIO.setup(GPIO_ECHO, GPIO.IN)      # to set the echo pin as input

GPIO.output(GPIO_TRIG, GPIO.LOW)
time.sleep(5.0)


try:
    GPIO.output(GPIO_TRIG, GPIO.HIGH)       #to send a ultrasonic wave
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, GPIO.LOW)        # to recieve the reflected wave
    
    temp = 0                               # using this temp variable, starting the PWM with 0 percent duty cycle
    pwm_led.start(temp)                      # Start the PWM on the pin number 12, i.e., pwm_led

    while GPIO.input(GPIO_ECHO) == 0:       #recording the time until the trigger sends a ultrasonic wave
        send_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:       #recording the time when the reflected wave from the object is received
        recieve_time = time.time()

    pulse_duration = recieve_time - send_time       #time difference between the sending and receiving of wave
    distance = round(pulse_duration * 17150, 2)     #calculating the distance of the object in centi meters

    print("Distance: " + distance)
    
    if distance <= 25 and distance >= 0:        #algorithm to convert the distance to PWM duty cycle
        duty_cycle = round(((25 - distance) * 4))
        pwm_led.ChangeDutyCycle(duty_cycle)
        time.sleep(0.4)

    GPIO.cleanup()      #to set all the pins back to default state, i.e., enable
except KeyboardInterrupt:
    pwm_led.stop()                         # to stop the pwm
    GPIO.cleanup()                