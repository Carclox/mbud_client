# clase que contiene el mapa de registros Modbus para el medidor
# Microstar D2000 smart meter
# Autor: Carlos y Gepeto

import struct

class MeterData:
    """
    Clase para almacenar los registros modbus y decodificar datos
    de medidores Microstar D2000
    """


    # Diccionario para los registros, hay que buscarlos
    # de acuerdo a Gepeto estas direcciones pymodbus las maneja en formato decimal
    MEASURES = {
        "FASE_A_Tension_Instantanea": (0xA612, 2, "float32"),  #
        "FASE_B_Tension_Instantanea": (0xA614, 2, "float32"),  #
        "FASE_C_Tension_Instantanea": (0xA616, 2, "float32"),  #
        "FASE_A_Corriente_Instantanea": (0xA622, 2, "float32"),  #
        "FASE_B_Corriente_Instantanea": (0xA624, 2, "float32"),  #
        "FASE_C_Corriente_Instantanea": (0xA626, 2, "float32"),  #
        "Potencia_Activa_Instantanea": (0xA630, 2, "float32"),  #
        "FASE_A_Potencia_Activa_Instantanea": (0xA632, 2, "float32"),  #
        "FASE_B_Potencia_Activa_Instantanea": (0xA634, 2, "float32"),  #
        "FASE_C_Potencia_Activa_Instantanea": (0xA636, 2, "float32"),  #
        "Potencia_Reactiva_Instantanea": (0xA640, 2, "float32"),  #
        "FASE_A_Potencia_Reactiva_Instantanea": (0xA642, 2, "float32"),  #
        "FASE_B_Potencia_Reactiva_Instantanea": (0xA644, 2, "float32"),  #
        "FASE_C_Potencia_Reactiva_Instantanea": (0xA646, 2, "float32"),  #
        "Factor_de_Potencia_Instantanea": (0xA650, 2, "float32"),  #
        "FASE_A_Factor_de_Potencia_Instantanea": (0xA652, 2, "float32"),  #
        "FASE_B_Factor_de_Potencia_Instantanea": (0xA654, 2, "float32"),  #
        "FASE_C_Factor_de_Potencia_Instantanea": (0xA656, 2, "float32"),  #
        "Potencia_Aparente_Instantanea": (0xA660, 2, "float32"),  #
        "FASE_A_Potencia_Aparente_Instantanea": (0xA662, 2, "float32"),  #
        "FASE_B_Potencia_Aparente_Instantanea": (0xA664, 2, "float32"),  #
        "FASE_C_Potencia_Aparente_Instantanea": (0xA666, 2, "float32"),  #
        "Frecuencia_instantanea": (0xA670, 2, "float32"),  #
        "CH1_FASE_A_Tension_Instantanea": (0xA712, 2, "float32"),  #
        "CH1_FASE_B_Tension_Instantanea": (0xA714, 2, "float32"),  #
        "CH1_FASE_C_Tension_Instantanea": (0xA716, 2, "float32"),  #
        "CH1_FASE_A_Corriente_Instantanea": (0xA722, 2, "float32"),  #
        "CH1_FASE_B_Corriente_Instantanea": (0xA724, 2, "float32"),  #
        "CH1_FASE_C_Corriente_Instantanea": (0xA726, 2, "float32"),  #
        "CH1_Potencia_Activa_Instantanea": (0xA730, 2, "float32"),  #
        "CH1_FASE_A_Potencia_Activa_Instantanea": (0xA732, 2, "float32"),  #
        "CH1_FASE_B_Potencia_Activa_Instantanea": (0xA734, 2, "float32"),  #
        "CH1_FASE_C_Potencia_Activa_Instantanea": (0xA736, 2, "float32"),  #
        "CH1_Potencia_Reactiva_Instantanea": (0xA740, 2, "float32"),  #
        "CH1_FASE_A_Potencia_Reactiva_Instantanea": (0xA742, 2, "float32"),  #
        "CH1_FASE_B_Potencia_Reactiva_Instantanea": (0xA744, 2, "float32"),  #
        "CH1_FASE_C_Potencia_Reactiva_Instantanea": (0xA746, 2, "float32"),  #
        "CH1_Factor_de_Potencia_Instantanea": (0xA750, 2, "float32"),  #
        "CH1_FASE_A_Factor_de_Potencia_Instantanea": (0xA752, 2, "float32"),  #
        "CH1_FASE_B_Factor_de_Potencia_Instantanea": (0xA754, 2, "float32"),  #
        "CH1_FASE_C_Factor_de_Potencia_Instantanea": (0xA756, 2, "float32"),  #
        "CH1_Potencia_Aparente_Instantanea": (0xA760, 2, "float32"),  #
        "CH1_FASE_A_Potencia_Aparente_Instantanea": (0xA762, 2, "float32"),  #
        "CH1_FASE_B_Potencia_Aparente_Instantanea": (0xA764, 2, "float32"),  #
        "CH1_FASE_C_Potencia_Aparente_Instantanea": (0xA766, 2, "float32"),  #
        "CH1_Frecuencia_instantanea": (0xA770, 2, "float32"),  #
        "CH2_FASE_A_Tension_Instantanea": (0xA812, 2, "float32"),  #
        "CH2_FASE_B_Tension_Instantanea": (0xA814, 2, "float32"),  #
        "CH2_FASE_C_Tension_Instantanea": (0xA816, 2, "float32"),  #
        "CH2_FASE_A_Corriente_Instantanea": (0xA822, 2, "float32"),  #
        "CH2_FASE_B_Corriente_Instantanea": (0xA824, 2, "float32"),  #
        "CH2_FASE_C_Corriente_Instantanea": (0xA826, 2, "float32"),  #
        "CH2_Potencia_Activa_Instantanea": (0xA830, 2, "float32"),  #
        "CH2_FASE_A_Potencia_Activa_Instantanea": (0xA832, 2, "float32"),  #
        "CH2_FASE_B_Potencia_Activa_Instantanea": (0xA834, 2, "float32"),  #
        "CH2_FASE_C_Potencia_Activa_Instantanea": (0xA836, 2, "float32"),  #
        "CH2_Potencia_Reactiva_Instantanea": (0xA840, 2, "float32"),  #
        "CH2_FASE_A_Potencia_Reactiva_Instantanea": (0xA842, 2, "float32"),  #
        "CH2_FASE_B_Potencia_Reactiva_Instantanea": (0xA844, 2, "float32"),  #
        "CH2_FASE_C_Potencia_Reactiva_Instantanea": (0xA846, 2, "float32"),  #
        "CH2_Factor_de_Potencia_Instantanea": (0xA850, 2, "float32"),  #
        "CH2_FASE_A_Factor_de_Potencia_Instantanea": (0xA852, 2, "float32"),  #
        "CH2_FASE_B_Factor_de_Potencia_Instantanea": (0xA854, 2, "float32"),  #
        "CH2_FASE_C_Factor_de_Potencia_Instantanea": (0xA856, 2, "float32"),  #
        "CH2_Potencia_Aparente_Instantanea": (0xA860, 2, "float32"),  #
        "CH2_FASE_A_Potencia_Aparente_Instantanea": (0xA862, 2, "float32"),  #
        "CH2_FASE_B_Potencia_Aparente_Instantanea": (0xA864, 2, "float32"),  #
        "CH2_FASE_C_Potencia_Aparente_Instantanea": (0xA866, 2, "float32"),  #
        "CH2_Frecuencia_instantanea": (0xA870, 2, "float32")   #
    }

    # Diccionario para guaradar las direcciones ID de los medidores
    METERS = {
        "METER1": 0x1,
        "METER2": 0x2,
        "METER3": 0x3,
    }


    def get_measure(self, measure_name):
        if measure_name in self.MEASURES:
            # retormar la direccion como esta
            return self.MEASURES[measure_name]
        else:
            raise ValueError(f"Medida no encontrrada:{measure_name}")
        


    def get_meter_id(self, meter_id):
        if meter_id in self.METERS:
            return self.METERS[meter_id]
        else:
            raise ValueError(f"medidor no encontrado: {meter_id}. medidores disponibles: {list(self.METERS.keys())}")


    @staticmethod
    def decode_registers(registers, data_type):
        """
        Decodifica los registros Modbus en bruto basandose en el tipo de dato, esta vaina la hizo gepeto
        """
        if data_type == "float32":
            if len(registers) !=2:
                raise ValueError("Se esperan 2 registros para decodificar un float32 32-bit IEEE 754")
            # interpreta los 4 bytes como un float en orden Big-Endian (>)
            byte_data = struct.unpack('>f', byte_data[0])
            return struct.unpack('>f', byte_data[0])
        elif data_type == "uint16":
            if len(registers) != 1:
                raise ValueError("se espera un registro para decodificar un uint16 (16-bit unsigned integer).")
            return registers[0]# pymodbus ya devuelve el valor entero correcto

        else:
            raise NotImplementedError(f"Tipo de dato no soportado para decodificacion: {data_type}")     


### Se puede remombrar como class MicrostarD2000Data:
### y agregar mas clases para mas marcas de medidores con diferente mapa de registros.