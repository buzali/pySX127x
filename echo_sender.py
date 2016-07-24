#!/usr/bin/env python2.7

""" A simple echo class. """

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import sys, locale, readline

BOARD.setup()

class LoraEchoSender(LoRa):
    def __init__(self, verbose=False):
        super(LoraEchoSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])
        self.set_symb_timeout(1000)

    def on_rx_done(self):
        BOARD.led_on()
        #print("\nRxDone")
        #print(self.get_irq_flags())
        payload = self.read_payload(nocheck=True)
        print(bytearray(payload).decode("utf-8"))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        # send echo
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

        msg = raw_input("Your message:")
        self.send_msg(msg)
        # self.set_mode(MODE.STDBY)
        # self.clear_irq_flags()
        # self.write_payload(payload)
        # self.set_payload_length(len(payload))
        # BOARD.led_on()
        #
        # self.set_mode(MODE.TX)
        # # self.set_mode()


    def on_tx_done(self):
        #print("\nTxDone")
        #print(self.get_irq_flags())
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXSINGLE)

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])

        msg = raw_input("Your message:")
        self.send_msg(msg)

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def send_msg(self, str):
        payload = list(bytearray(str, encoding="utf-8"))
        lora.write_payload(payload)
        lora.set_payload_length(len(payload))
        lora.set_mode(MODE.TX)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.STDBY)
        lora.clear_irq_flags()
        msg = raw_input("Your message:")
        self.send_msg(msg)
        while True:
            sleep(1)
        #     rssi_value = self.get_rssi_value()
        #     status = self.get_modem_status()
        #     sys.stdout.flush()
        #     sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))

lora = LoraEchoSender(verbose=False)
lora.set_freq(434)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
#lora.set_rx_crc(True)
#lora.set_coding_rate(CODING_RATE.CR4_6)
#lora.set_pa_config(max_power=0, output_power=0)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
#lora.set_low_data_rate_optim(True)
#lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
#lora.set_agc_auto_on(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)


try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()

