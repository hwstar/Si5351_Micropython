#
# Si5351 Micropython test/example program
#

from machine import I2C,Pin
import si5351

# Define pins to use with I2C interface
scl_pin = Pin(13)
sda_pin = Pin(12)

# Instantiate I2C object 

i2c = I2C(0, freq=100000, scl = scl_pin, sda = sda_pin)

# Instantiate clock generator object

clkgen = si5351.SI5351(i2c)

# Initialize the clock generator

print("Init")
clkgen.init(si5351.CRYSTAL_LOAD_0PF, 25000000, -4000)

# Set the output frequencies

print("Set clk0 freq")
clkgen.set_freq(si5351.CLK0, 5000000000)

print("Set clk1 freq")
clkgen.set_freq(si5351.CLK1, 3000000000)

print("Set clk2 freq")
clkgen.set_freq(si5351.CLK2, 2500000000)

# Enable the outputs

print("Output enable")

clkgen.output_enable(si5351.CLK0, True)
clkgen.output_enable(si5351.CLK1, True)
clkgen.output_enable(si5351.CLK2, True)

# Set the output drive levels

print("Output drive")
clkgen.drive_strength(si5351.CLK0, si5351.DRIVE_2MA)
clkgen.drive_strength(si5351.CLK1, si5351.DRIVE_2MA)
clkgen.drive_strength(si5351.CLK2, si5351.DRIVE_2MA)








