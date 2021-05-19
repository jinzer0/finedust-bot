import time

epoch = time.time()
real = time.localtime(epoch)
print(real.tm_hour)