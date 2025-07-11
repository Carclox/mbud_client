# mbud_client
Cliente modbus para gateway mbusd


# gateway mbusd
https://github.com/3cky/mbusd.git


clonar repositorio
```bash
git clone https://github.com/3cky/mbusd.git
```


Para este gateway es necesario modificar el archivo config para especificarle el dispositivo usb to rs485

cambiar ```/dev/ttys0``` por el que el sistema asigne

```txt
# Serial port device name
device = /dev/ttyS0
```