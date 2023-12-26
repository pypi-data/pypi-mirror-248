import amtFMC as fmc
import warnings
warnings.filterwarnings("ignore",category=UserWarning)


# Zedboard's IP
ip = "169.254.92.202"
# Input “int” to use internal clock and “ext” to use external reference clock.
refClk = "ext"
# clkFreq: Reference clock frequency in MHz, range: 10 to 100 MHz.
clkFreq = 10
# Note that 10 MHz reference clock is required to be a sinusoidal wave.
fmc.amtFmcRfRef(ip,refClk,clkFreq)