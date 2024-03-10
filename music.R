library(audio)

library(tuneR)

library(beepr)
setWavPlayer('"C:/Program Files/Windows Media Player/wmplayer.exe"')

t1 = seq(0, 3, 1/8000) #times in seconds if sample for 3 seconds at 8000Hz
u1 = (2^14-1)*sin(2*pi*400*t1) #400 Hz sine wave that lasts t length seconds (here, 3 seconds)
w1 = Wave(u1, samp.rate = 8000, bit=16) #make the wave variable
play(w1)
writeWave(w1, "400HZ.wav", extensible = TRUE)


t2 = seq(0, 3, 1/8000) #times in seconds if sample for 3 seconds at 8000Hz
u2 = (2^14-1)*sin(2*pi*200*t2) #200 Hz sine wave that lasts t length seconds (here, 3 seconds)
w2 = Wave(u2, samp.rate = 8000, bit=16) #make the wave variable
play(w2)
writeWave(w2, "200HZ.wav", extensible = TRUE)


t3 = seq(0, 3, 1/8000) #times in seconds if sample for 3 seconds at 8000Hz
u3 = (2^14-1)*sin(2*pi*800*t3) #800 Hz sine wave that lasts t length seconds (here, 3 seconds)
w3 = Wave(u3, samp.rate = 8000, bit=16) #make the wave variable
play(w3)
writeWave(w3, "800HZ.wav", extensible = TRUE)



sr <- 8000
bits <- 16
secs <- 1
amp <- 1
t <- seq(0, 1, 1/sr)

C0 <- 16.35
G3 <- 196
A5 <- 880
E5 = 659.25
E=82.407
A=110
G=195.998
D=146.832



C0 <- floor(2^(bits-2)*(amp*sin(2*pi*C0*t)))
G3 <- floor(2^(bits-2)*(amp*sin(2*pi*G3*t)))
A5 <- floor(2^(bits-2)*(amp*sin(2*pi*A5*t)))

u <- Wave(c(C0,G3,A5), samp.rate=sr, bit=bits)

play(u)


E <- floor(2^(bits-2)*(amp*sin(2*pi*E*t)))
G <- floor(2^(bits-2)*(amp*sin(2*pi*G*t)))
D <- floor(2^(bits-2)*(amp*sin(2*pi*D*t)))
A <- floor(2^(bits-2)*(amp*sin(2*pi*A*t)))

u <- Wave(c(E,G,D,A), samp.rate=sr, bit=bits)

play(u)