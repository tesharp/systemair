from enum import Enum
from typing import Optional


class IntegerType(Enum):
    """

    Enum class representing integer types for Modbus communication.

    Attributes
    ----------
        UINT (str): Unsigned integer type.
        INT (str): Signed integer type.

    """

    UINT = "UINT"
    INT = "INT"


class RegisterType(Enum):
    """

    Enum class representing the types of Modbus registers.

    Attributes
    ----------
        Input (str): Represents an input register.
        Holding (str): Represents a holding register.

    """

    Input = "Input"
    Holding = "Holding"


class ModbusParameter:
    def __init__(
        self,
        register: int,
        sig: IntegerType,
        regType: RegisterType,
        short: str,
        description: str,
        min: Optional[int] = None,
        max: Optional[int] = None,
        boolean: Optional[bool] = None,
        scaleFactor: Optional[int] = None,
    ):
        self.register = register
        self.sig = sig
        self.regType = regType
        self.short = short
        self.description = description
        self.min = min
        self.max = max
        self.boolean = boolean
        self.scaleFactor = scaleFactor


parameters_list = [
    # Demand control
    ModbusParameter(
        register=1001,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_DEMC_RH_HIGHEST",
        description="Highest value of all RH sensors",
        min=0,
        max=100,
    ),
    # User modes
    ModbusParameter(
        register=1101,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_HOLIDAY_TIME",
        description="Time delay setting for user mode Holiday (days)",
        min=1,
        max=365,
    ),
    ModbusParameter(
        register=1102,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_AWAY_TIME",
        description="Time delay setting for user mode Away (hours)",
        min=1,
        max=72,
    ),
    ModbusParameter(
        register=1103,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_FIREPLACE_TIME",
        description="Time delay setting for user mode Fire Place (minutes)",
        min=1,
        max=60,
    ),
    ModbusParameter(
        register=1104,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_REFRESH_TIME",
        description="Time delay setting for user mode Refresh (minutes)",
        min=1,
        max=240,
    ),
    ModbusParameter(
        register=1105,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_CROWDED_TIME",
        description="Time delay setting for user mode Crowded (hours)",
        min=1,
        max=8,
    ),
    ModbusParameter(
        register=1111,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_USERMODE_REMAINING_TIME_L",
        description="Remaining time for the state Holiday/Away/Fire Place/Refresh/Crowded, lower 16 bits",
    ),
    ModbusParameter(
        register=1112,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_USERMODE_REMAINING_TIME_H",
        description="Remaining time for the state Holiday/Away/Fire Place/Refresh/Crowded, higher 16 bits",
    ),
    ModbusParameter(
        register=1135,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_CROWDED_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Crowded.\n3: Normal\n4: High\n5: Maximum",
        min=3,
        max=5,
    ),
    ModbusParameter(
        register=1136,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_CROWDED_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Crowded.\n3: Normal\n4: High\n5: Maximum",
        min=3,
        max=5,
    ),
    ModbusParameter(
        register=1137,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_REFRESH_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Refresh.\n3: Normal\n4: High\n5: Maximum",
        min=3,
        max=5,
    ),
    ModbusParameter(
        register=1138,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_REFRESH_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Refresh.\n3: Normal\n4: High\n5: Maximum",
        min=3,
        max=5,
    ),
    ModbusParameter(
        register=1139,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_FIREPLACE_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Fireplace.\n3: Normal\n4: High\n5: Maximum",
        min=3,
        max=5,
    ),
    ModbusParameter(
        register=1140,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_FIREPLACE_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Fireplace.\n1: Minimum\n2: Low\n3: Normal",
        min=1,
        max=3,
    ),
    ModbusParameter(
        register=1141,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_AWAY_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Away.\n0: Off(1)\n1: Minimum\n2: Low\n3: Normal.\n(1): value Off only allowed if contents of register REG_FAN_MANUAL_STOP_ALLOWED is 1.",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=1142,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_AWAY_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Away.\n0: Off(1)\n1: Minimum\n2: Low\n3: Normal.\n(1): value Off only allowed if contents of register REG_FAN_MANUAL_STOP_ALLOWED is 1.",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=1143,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_HOLIDAY_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Holiday.\n0: Off(1)\n1: Minimum\n2: Low\n3: Normal.\n(1): value Off only allowed if contents of register REG_FAN_MANUAL_STOP_ALLOWED is 1.",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=1144,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_HOLIDAY_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Holiday.\n0: Off(1)\n1: Minimum\n2: Low\n3: Normal.\n(1): value Off only allowed if contents of register REG_FAN_MANUAL_STOP_ALLOWED is 1.",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=1145,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_COOKERHOOD_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Cooker Hood.\n2: Low\n3: Normal\n4: High",
        min=1,
        max=5,
    ),
    ModbusParameter(
        register=1146,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_COOKERHOOD_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Cooker Hood.\n2: Low\n3: Normal\n4: High",
        min=1,
        max=5,
    ),
    ModbusParameter(
        register=1147,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_VACUUMCLEANER_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Vacuum Cleaner.\n2: Low\n3: Normal\n4: High",
        min=1,
        max=5,
    ),
    ModbusParameter(
        register=1148,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_VACUUMCLEANER_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for mode Vacuum Cleaner.\n2: Low\n3: Normal\n4: High",
        min=1,
        max=5,
    ),
    ModbusParameter(
        register=1161,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_USERMODE_MODE",
        description="Active User mode.\n0: Auto\n1: Manual\n2: Crowded\n3: Refresh\n4: Fireplace\n5: Away\n6: Holiday\n7: Cooker Hood\n8: Vacuum Cleaner\n9: CDI1\n10: CDI2\n11: CDI3\n12: PressureGuard",
        min=0,
        max=12,
    ),
    ModbusParameter(
        register=1162,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_HMI_CHANGE_REQUEST",
        description="New desired user mode as requested by HMI\n0: None\n1: Auto\n2: Manual\n3: Crowded\n4: Refresh\n5: Fireplace\n6: Away\n7: Holiday",
        min=0,
        max=7,
    ),
    ModbusParameter(
        register=1177,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_PRESSURE_GUARD_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for configurable pressure guard function.\n0: Off\n1: Minimum\n2: Low\n3: Normal\n4: High\n5: Maximum",
        min=0,
        max=5,
    ),
    ModbusParameter(
        register=1178,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_PRESSURE_GUARD_AIRFLOW_LEVEL_EAF",
        description="Fan speed level for configurable pressure guard function.\n0: Off\n1: Minimum\n2: Low\n3: Normal\n4: High\n5: Maximum",
        min=0,
        max=5,
    ),
    ModbusParameter(
        register=12306,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_SENSOR_DI_COOKERHOOD",
        description="Cooker hood",
        boolean=True,
    ),
    ModbusParameter(
        register=12307,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_SENSOR_DI_VACUUMCLEANER",
        description="Vacuum cleaner",
        boolean=True,
    ),
    ModbusParameter(
        register=3114,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FUNCTION_ACTIVE_PRESSURE_GUARD",
        description="Pressure guard",
        boolean=True,
    ),
    ModbusParameter(
        register=3115,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FUNCTION_ACTIVE_CDI_1",
        description="Configurable DI1",
        boolean=True,
    ),
    ModbusParameter(
        register=3116,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FUNCTION_ACTIVE_CDI_2",
        description="Configurable DI2",
        boolean=True,
    ),
    ModbusParameter(
        register=3117,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FUNCTION_ACTIVE_CDI_3",
        description="Configurable DI3",
        boolean=True,
    ),
    # Airflow control
    ModbusParameter(
        register=12401,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_SENSOR_RPM_SAF",
        description="Supply Air Fan RPM indication from TACHO",
        min=0,
        max=5000,
    ),
    ModbusParameter(
        register=12402,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_SENSOR_RPM_EAF",
        description="Extract Air Fan RPM indication from TACHO",
        min=0,
        max=5000,
    ),
    ModbusParameter(
        register=1131,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF",
        description="Fan speed level for mode Manual. Applies to both the SAF and the EAF fan.\n0: Off(1)\n2: Low\n3: Normal\n4: High\n(1): value Off only allowed if contents of register REG_FAN_MANUAL_STOP_ALLOWED is 1.",
        min=0,
        max=4,
    ),
    ModbusParameter(
        register=14001,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_SAF",
        description="SAF fan speed",
        min=0,
        max=100,
    ),
    ModbusParameter(
        register=14002,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_EAF",
        description="EAF fan speed",
        min=0,
        max=100,
    ),
    # Temperature control
    ModbusParameter(
        register=2001,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_TC_SP",
        description="Temperature setpoint for the supply air temperature",
        scaleFactor=10,
        min=120,
        max=300,
    ),
    # Cooler
    ModbusParameter(
        register=14201,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_Y3_ANALOG",
        description="Cooler AO state",
        min=0,
        max=100,
    ),
    ModbusParameter(
        register=14202,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_Y3_DIGITAL",
        description="Cooler DO state:\n0: Output not active\n1: Output active",
        boolean=True,
    ),
    # Heater
    ModbusParameter(
        register=3113,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_FUNCTION_ACTIVE_HEATER_COOL_DOWN",
        description="Active Heater Cool Down",
        boolean=True,
    ),
    ModbusParameter(
        register=14381,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_TRIAC",
        description="TRIAC control signal",
        boolean=True,
    ),
    ModbusParameter(
        register=14101,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_Y1_ANALOG",
        description="Heater AO state",
        min=0,
        max=100,
    ),
    ModbusParameter(
        register=14102,
        sig=IntegerType.INT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_Y1_DIGITAL",
        description="Heater DO state:\n0: Output not active\n1: Output active",
        boolean=True,
    ),
    # ECO mode
    ModbusParameter(
        register=2505,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_ECO_MODE_ON_OFF",
        description="Enabling of eco mode",
        boolean=True,
    ),
    # Filter replacement
    ModbusParameter(
        register=7005,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FILTER_REMAINING_TIME_L",
        description="Remaining filter time in seconds, lower 16 bits",
    ),
    ModbusParameter(
        register=7006,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_FILTER_REMAINING_TIME_H",
        description="Remaining filter time in seconds, higher 16 bits",
    ),
    # Analog Input values (Temperatures, CO2, RH)
    ModbusParameter(
        register=12102,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_OAT",
        description="Outdoor Air Temperature sensor (standard)",
        scaleFactor=10,
        min=-400,
        max=800,
    ),
    ModbusParameter(
        register=12103,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_SAT",
        description="Supply Air Temperature sensor (standard)",
        scaleFactor=10,
        min=-400,
        max=800,
    ),
    ModbusParameter(
        register=12105,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_EAT",
        description="Extract Air Temperature sensor (accessory)",
        scaleFactor=10,
        min=-400,
        max=800,
    ),
    ModbusParameter(
        register=12108,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_OHT",
        description="Overheat Temperature sensor (Electrical Heater)",
        scaleFactor=10,
        min=-400,
        max=800,
    ),
    ModbusParameter(
        register=12109,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_RHS",
        description="Relative Humidity Sensor (Accessory)",
        min=0,
        max=100,
    ),
    ModbusParameter(
        register=12544,
        sig=IntegerType.INT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_PDM_EAT_VALUE",
        description="PDM EAT sensor value (standard)",
        scaleFactor=10,
        min=-400,
        max=800,
    ),
    ModbusParameter(
        register=12136,
        sig=IntegerType.UINT,
        regType=RegisterType.Holding,
        short="REG_SENSOR_RHS_PDM",
        description="PDM RHS sensor value (standard)",
        min=0,
        max=100,
    ),
    # Output values
    ModbusParameter(
        register=14104,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_OUTPUT_Y2_DIGITAL",
        description="Heat Exchanger DO state.0: Output not active1: Output active",
        boolean=True,
    ),
    # Alarms
    ModbusParameter(
        register=15016,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_FROST_PROT_ALARM",
        description="Frost protection",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15023,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_DEFROSTING_ALARM",
        description="Defrosting",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15030,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_SAF_RPM_ALARM",
        description="Supply air fan RPM",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15037,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_EAF_RPM_ALARM",
        description="Extract air fan RPM",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15072,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_SAT_ALARM",
        description="Supply air temperature",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15086,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_EAT_ALARM",
        description="Extract air temperature",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15121,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_RGS_ALARM",
        description="Rotation guard (RGS)",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15142,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_FILTER_ALARM",
        description="Filter",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15170,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_CO2_ALARM",
        description="CO2",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15177,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_LOW_SAT_ALARM",
        description="Low supply air temperature",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15530,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_OVERHEAT_TEMPERATURE_ALARM",
        description="Overheat temperature",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15537,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_FIRE_ALARM_ALARM",
        description="Fire alarm",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15544,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_FILTER_WARNING_ALARM",
        description="Filter warning",
        min=0,
        max=3,
    ),
    ModbusParameter(
        register=15901,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_TYPE_A",
        description="Indicates if an alarm Type A is active",
        boolean=True,
    ),
    ModbusParameter(
        register=15902,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_TYPE_B",
        description="Indicates if an alarm Type B is active",
        boolean=True,
    ),
    ModbusParameter(
        register=15903,
        sig=IntegerType.UINT,
        regType=RegisterType.Input,
        short="REG_ALARM_TYPE_C",
        description="Indicates if an alarm Type C is active",
        boolean=True,
    ),
]

parameter_map = {param.short: param for param in parameters_list}

operation_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_TC_SP",
        "REG_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_MODE",
        "REG_ECO_MODE_ON_OFF",
        "REG_SENSOR_RPM_SAF",
        "REG_SENSOR_RPM_EAF",
        "REG_OUTPUT_SAF",
        "REG_OUTPUT_EAF",
    ]
}

sensor_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_SENSOR_RHS_PDM",
        "REG_SENSOR_OAT",
        "REG_SENSOR_SAT",
        "REG_SENSOR_PDM_EAT_VALUE",
        "REG_SENSOR_OHT",
    ]
}

config_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_FILTER_REMAINING_TIME_L",
        "REG_FILTER_REMAINING_TIME_H",
        "REG_USERMODE_CROWDED_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_REFRESH_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_FIREPLACE_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_AWAY_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_HOLIDAY_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_COOKERHOOD_AIRFLOW_LEVEL_SAF",
        "REG_USERMODE_VACUUMCLEANER_AIRFLOW_LEVEL_SAF",
        "REG_PRESSURE_GUARD_AIRFLOW_LEVEL_SAF",
    ]
}

alarm_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_ALARM_FROST_PROT_ALARM",
        "REG_ALARM_DEFROSTING_ALARM",
        "REG_ALARM_SAF_RPM_ALARM",
        "REG_ALARM_EAF_RPM_ALARM",
        "REG_ALARM_SAT_ALARM",
        "REG_ALARM_EAT_ALARM",
        "REG_ALARM_RGS_ALARM",
        "REG_ALARM_FILTER_ALARM",
        "REG_ALARM_CO2_ALARM",
        "REG_ALARM_LOW_SAT_ALARM",
        "REG_ALARM_OVERHEAT_TEMPERATURE_ALARM",
        "REG_ALARM_FIRE_ALARM_ALARM",
        "REG_ALARM_FILTER_WARNING_ALARM",
        "REG_ALARM_TYPE_A",
        "REG_ALARM_TYPE_B",
        "REG_ALARM_TYPE_C",
    ]
}

function_parameters = {
    short: parameter_map[short]
    for short in [
        "REG_FUNCTION_ACTIVE_PRESSURE_GUARD",
        "REG_SENSOR_DI_COOKERHOOD",
        "REG_SENSOR_DI_VACUUMCLEANER",
        "REG_FUNCTION_ACTIVE_HEATER_COOL_DOWN",
        "REG_FUNCTION_ACTIVE_CDI_1",
        "REG_FUNCTION_ACTIVE_CDI_2",
        "REG_FUNCTION_ACTIVE_CDI_3",
    ]
}
