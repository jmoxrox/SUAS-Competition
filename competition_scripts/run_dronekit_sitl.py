import dronekit_sitl
from time import sleep

if __name__ == '__main__':
    sitl = dronekit_sitl.start_default()
    print("Connection String:", sitl.connection_string())

    try:
        while True:
            sleep(1)
    except:
        sitl.stop()