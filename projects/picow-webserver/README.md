# Pico W Webserver

This project implements a really basic socket-based HTTP webserver.

The motivation behind this project was to implement a way to accept HTTP requests, process the data in it (if any), and return an HTTP response; I wanted it to be accesible via Python `requests`, `curl`, or a browser.

It's not necessary to wire the Pico W to anything. Simply plug in a power source via USB and it'll start working. To monitor the server, run:
```bash
cat $DEVICE_PORT
```
after plugging the Pico W into the computer. `$DEVICE_PORT` will be whatever `/dev` device represents the Pico W. An easy way to find it is to run `rshell`.
