# modbus_client.py
# Cliente Modbus TCP
# segun la medida y el medidor especificado como parametros se envua al server mbusd
# Autor: Carlos y Gepeto


from pymodbus.client import ModbusTcpClient
from meter_data import MeterData
import sys
#import time

# --- Configuración Modbus del Gateway mbusd ---
SERVER_HOST = '127.0.0.1'  # IP del servidor mbusd, esto se debe mejorar,
SERVER_PORT = 502          # Puerto por defecto de Modbus TCP

def fetch_modbus_data(client, meter_data_manager, meter_id_name, measure_name):
    """
    Solicita una medida específica de un medidor dado al servidor Modbus y la decodifica.
    """
    try:
        # 1. Obtener el Unit ID del medidor
        unit_id = meter_data_manager.get_meter_id(meter_id_name) # Método renombrado
        
        # 2. Obtener la información de la medida (dirección, cantidad, tipo)
        address_1_based, count, data_type = meter_data_manager.get_measure(measure_name) # Método renombrado
        
        # Las funciones de pymodbus esperan direcciones 0-based
        start_address_0_based = address_1_based - 1 

        print(f"Solicitando {measure_name} del {meter_id_name} (Unit ID: {unit_id}, Addr: {address_1_based} (0-based: {start_address_0_based}), Count: {count}, Tipo: {data_type})...")

        # Realizar la lectura de registros de holding (función Modbus 0x03)
        response = client.read_holding_registers(start_address_0_based, count, unit=unit_id)

        if response.isError():
            print(f"Error al leer registros para {measure_name} del {meter_id_name}: {response}")
            return None
        else:
            registers = response.registers
            print(f"Registros brutos recibidos para {measure_name}: {registers}")
            
            # Decodificar los datos usando el método estático de la clase de datos del medidor
            value = MeterData.decode_registers(registers, data_type)
            return value

    except ValueError as e:
        print(f"Error en la configuración (medidor o medida): {e}")
        return None
    except NotImplementedError as e:
        print(f"Error de decodificación: {e}")
        return None
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
        return None

def main(meter_id_name, measure_name):
    """
    Función principal para ejecutar el cliente Modbus.
    """
    # Instanciar la clase que maneja los datos del medidor
    meter_data_manager = MeterData()
    
    # Conectar al servidor Modbus TCP (mbusd)
    client = ModbusTcpClient(SERVER_HOST, port=SERVER_PORT)
    print(f"Intentando conectar a Modbus TCP server en {SERVER_HOST}:{SERVER_PORT}...")

    if not client.connect():
        print("Error: No se pudo conectar al servidor Modbus. Asegúrese de que mbusd esté corriendo y accesible.")
        return

    print("Conectado al servidor Modbus.")

    try:
        # Verificar si el medidor y la medida existen antes de intentar leer
        try:
            meter_data_manager.get_meter_id(meter_id_name) # Solo para verificar si existe
            meter_data_manager.get_measure(measure_name)    # Solo para verificar si existe
        except ValueError as e:
            print(f"Error de validación: {e}")
            client.close()
            return
            
        value = fetch_modbus_data(client, meter_data_manager, meter_id_name, measure_name)

        if value is not None:
            print(f"\n--- Resultado para {measure_name} en {meter_id_name} ---")
            print(f"Valor decodificado: {value:.3f}") # Formatear floats para mejor legibilidad
        else:
            print(f"No se pudo obtener el valor para {measure_name} de {meter_id_name}.")

    except KeyboardInterrupt:
        print("\nCliente Modbus detenido por el usuario.")
    finally:
        print("Cerrando conexión Modbus...")
        client.close()

if __name__ == "__main__":
    # La ejecución será: python modbus_client.py <nombre_medidor> <nombre_medida>
    if len(sys.argv) != 3:
        print("Uso: python modbus_client.py <nombre_medidor> <nombre_medida>")
        print("Ejemplo: python modbus_client.py METER1 FASE_A_Tension_Instantanea")
        print("Medidores disponibles:", list(MeterData().METERS.keys()))
        print("Medidas disponibles:", list(MeterData()).MEASURES.keys())
        sys.exit(1)
    
    meter_id_arg = sys.argv[1] # Ej. "METER1"
    measure_name_arg = sys.argv[2] # Ej. "FASE_A_Tension_Instantanea"
    
    main(meter_id_arg, measure_name_arg)


# la idea es escalar esto para que se implemente desde el servidor central por ejemplo con una ventana con un dashboard o algo asi.
# en el nuevo caso de que es una pasarela mbusd corriendo en cada armario, este cliente debe cambiar dinamicamente la ip del server mbusd
# tal vez se pueda hacer asignandole un nombre a cada gateway y que el cliente busque ese nombre en toda la red
# esto haria que si la ip del server mbusd cambia, el cliente sigue encontrando el dispositivo que le interese
