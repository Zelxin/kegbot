#define FLOW_SENSOR_PIN 2
//pulse counter
volatile uint16_t pulses= 0;
//track state of pulse pin
volatile uint8_t lastFlowpinState;
volatile uint32_t lastFlowRateTimer = 0;
volatile float flowrate;

//Interrupt is called once a millisecond, looks for any pulses from sensor
SIGNAL(TIMER0_COMPA_vect)
{
  uint8_t x = digitalRead(FLOW_SENSOR_PIN);
  if (x == lastFlowpinState)
  {
    lastFlowRateTimer++;
    return;
  }
  if(x==HIGH)
  {
    //Low to high transition
    pulses++;
  }
  lastflowpinState = x;
  flowrate = 1000.0;
  flowrate /= lastFlowRateTimer;/hertz
  lastFlowRateTimer = 0
}

void useInterrupt(bool v)
{
  
}
