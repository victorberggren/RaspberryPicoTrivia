from machine import Pin, Timer
import time

questionBank = [
    {"prompt": "What was the first state?",
     "optionA": "Delaware",
     "optionB": "New Jersey",
     "optionC": "Pennsylvania",
     "answer": "A"},
    {"prompt": "Which country produces the most coffee in the world?",
     "optionA": "Colombia",
     "optionB": "Brazil",
     "optionC": "Indonesia",
     "answer": "B"},
    {"prompt": "Zurich is a city in which country?",
     "optionA": "Germany",
     "optionB": "Switzerland",
     "optionC": "Austria",
     "answer": "B"},
    {"prompt": "How many hearts does an octopus have?",
     "optionA": "Two",
     "optionB": "One",
     "optionC": "Three",
     "answer": "C"},
    {"prompt": "What country is AC/DC from?",
     "optionA": "Australia",
     "optionB": "England",
     "optionC": "United States",
     "answer": "A"},
    {"prompt": "How many national parks are in the United States?",
     "optionA": "54",
     "optionB": "58",
     "optionC": "63",
     "answer": "B"},
    {"prompt": "What is the world's longest river?",
     "optionA": "Nile",
     "optionB": "Yangtze",
     "optionC": "Amazon",
     "answer": "C"},
    {"prompt": "How long is an eon in geology?",
     "optionA": "A billion years",
     "optionB": "A million years",
     "optionC": "A hundred thousand years",
     "answer": "A"},
    {"prompt": "Who is depicted on the $50 bill?",
     "optionA": "Alexander Hamilton",
     "optionB": "Thomas Jefferson",
     "optionC": "Ulysses S. Grant",
     "answer": "C"},
    {"prompt": "When is Canada Day?",
     "optionA": "April 15th",
     "optionB": "July 1st",
     "optionC": "June 14th",
     "answer": "B"},
    ]

timer = Timer()
buttonALed = Pin(18, Pin.OUT)
buttonBLed = Pin(21, Pin.OUT)
buttonCLed = Pin(16, Pin.OUT)
buttonAInputPin = Pin(28, Pin.IN, Pin.PULL_DOWN)
buttonBInputPin = Pin(22, Pin.IN, Pin.PULL_DOWN)
buttonCInputPin = Pin(17, Pin.IN, Pin.PULL_DOWN)
redLedPin = Pin(14, Pin.OUT)
greenLedPin = Pin(10, Pin.OUT)

selectedAnswer = ""
correctAnswer = ""

def cycleLeds(timer):
    leds = [buttonCLed, buttonBLed, buttonALed]
    for led in leds:
        led.toggle()
        time.sleep_ms(100)
        led.toggle()

def triggerAnswerLights(leds):
    for i in range(6):
        leds.toggle()
        time.sleep_ms(150)

def clickedA(pin):
    global selectedAnswer
    timer.deinit()
    turnOffButtonLeds()
    buttonALed.on()
    turnOffIRQ()
    selectedAnswer = "A"
    handleSelectAnswer()

def clickedB(pin):
    global selectedAnswer
    timer.deinit()
    turnOffButtonLeds()
    buttonBLed.on()
    turnOffIRQ()
    selectedAnswer = "B"
    handleSelectAnswer()

def clickedC(pin):
    global selectedAnswer
    timer.deinit()
    turnOffButtonLeds()
    buttonCLed.on()
    turnOffIRQ()
    selectedAnswer = "C"
    handleSelectAnswer()

def handleSelectAnswer():
    if correctAnswer == selectedAnswer:
        triggerAnswerLights(greenLedPin)
    else:
        triggerAnswerLights(redLedPin)

def turnOffButtonLeds():
    buttonALed.off()
    buttonBLed.off()
    buttonCLed.off()

def turnOnButtonLeds():
    buttonALed.on()
    buttonBLed.on()
    buttonCLed.on()

def turnOnIRQ():
    buttonAInputPin.irq(trigger=Pin.IRQ_RISING, handler=clickedA)
    buttonBInputPin.irq(trigger=Pin.IRQ_RISING, handler=clickedB)
    buttonCInputPin.irq(trigger=Pin.IRQ_RISING, handler=clickedC)

def turnOffIRQ():
    buttonAInputPin.irq(trigger=Pin.IRQ_RISING, handler=lambda p: None)
    buttonBInputPin.irq(trigger=Pin.IRQ_RISING, handler=lambda p: None)
    buttonCInputPin.irq(trigger=Pin.IRQ_RISING, handler=lambda p: None)

def main():
    global selectedAnswer
    global correctAnswer
    streak = 0
    longestStreak = 0
    numRight = 0
    numWrong = 0

    #primary gameplay loop, iterate over all trivia questions
    for count, question in enumerate(questionBank):
        print("Streak:", streak, " Right:", numRight, " Wrong:", numWrong, "\n")
        print("Q" + str(count+1) + " - " + question["prompt"])
        print("A)", question["optionA"])
        print("B)", question["optionB"])
        print("C)", question["optionC"])
        print()
        correctAnswer = question["answer"]

        #start blinking LEDs next to buttons, and initialize button interrupt handlers
        timer.init(freq=2, mode=Timer.PERIODIC, callback=cycleLeds)
        turnOnIRQ()
        
        #poll every 50ms to see if player has answered the current question
        while selectedAnswer == "":
            time.sleep_ms(50)
        
        if correctAnswer == selectedAnswer:
            numRight += 1
            streak += 1
            if streak > longestStreak:
                longestStreak = streak
            print("That's right!")
        else:
            numWrong += 1
            streak = 0
            print("Sorry! The right answer was '" + question["option"+correctAnswer] + "'!")
        
        #reset state for next loop iteration
        selectedAnswer = ""
        turnOffButtonLeds()

    print("\nThanks for playing!")
    print("Longest streak:", longestStreak, " Right:", numRight, " Wrong:", numWrong)

if __name__ == "__main__":
    main()
