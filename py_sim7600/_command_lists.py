"""
This file contains all name constraints used in this library.

For detailed explanation, please check the individual comments and DocString.
"""

memory_list = ["DC", "MC", "RC", "SM", "ME", "FD", "ON", "LD", "EN"]
"""
This is the memory name allowed to use in the command ATD.
"""

pin_status = ["READY", "SIM PIN", "SIM PUK", "PH-SIM PIN", "SIM PIN2", "SIM PUK2", "PH-NET PIN"]
"""
This is the PIN status return from command AT+CPIN.
"""

restricted_sim_command = {
    176: "READ BINARY",
    178: "READ RECORD",
    192: "GET RESPONSE",
    214: "UPDATE BINARY",
    220: "UPDATE RECORD",
    242: "STATUS",
    203: "RETRIEVE DATA",
    219: "SET DATA"
}
"""
This is the accepted restricted SIM access command
"""

restricted_sim_file_id = {
    0x2FE2: "ICCID",
    0x2F05: "Extended Language Preferences",
    0x2F00: "EF DIR",
    0x2F06: "Access Rule Reference, Efs under USIM ADF",
    0x6F05: "Language Indication",
    0x6F07: "IMSI",
    0x6F08: "Ciphering and Integrity keys",
    0x6F09: "C and I keys for pkt switched domain",
    0x6F60: "User controlled PLMN selector w/Acc Tech",
    0x6F30: "User controlled PLMN selector",
    0x6F31: "HPLMN search period",
    0x6F37: "ACM maximum value",
    0x6F38: "USIM Service table",
    0x6F39: "Accumulated Call meter",
    0x6F3E: "Group Identifier Level",
    0x6F3F: "Group Identifier Level 2",
    0x6F46: "Service Provider Name",
    0x6F41: "Price Per Unit and Currency table",
    0x6F45: "Cell Bcast Msg identifier selection",
    0x6F78: "Access control class",
    0x6F7B: "Forbidden PLMNs",
    0x6F7E: "Location information",
    0x6FAD: "Administrative data",
    0x6F48: "Cell Bcast msg id for data download",
    0x6FB7: "Emergency call codes",
    0x6F50: "Cell bcast msg id range selection",
    0x6F73: "Packet switched location information",
    0x6F3B: "Fixed dialing numbers",
    0x6F3C: "Short messages",
    0x6F40: "MSISDN",
    0x6F42: "SMS parameters",
    0x6F43: "SMS Status",
    0x6F49: "Service dialing numbers",
    0x6F4B: "Extension 2",
    0x6F4C: "Extension 3",
    0x6F47: "SMS reports",
    0x6F80: "Incoming call information",
    0x6F81: "Outgoing call information",
    0x6F82: "Incoming call timer",
    0x6F83: "Outgoing call timer",
    0x6F4E: "Extension 5",
    0x6F4F: "Capability Config Parameters 2",
    0x6FB5: "Enh Multi Level Precedence and Pri",
    0x6FB6: "Automatic answer for Emlpp service",
    0x6FC2: "Group identity",
    0x6FC3: "Key for hidden phonebook entries",
    0x6F4D: "Barred dialing numbers",
    0x6F55: "Extension 4",
    0x6F58: "Comparison Method information",
    0x6F56: "Enabled services table",
    0x6F57: "Access Point Name Control List",
    0x6F2C: "De-personalization Control Keys",
    0x6F32: "Co-operative network list",
    0x6F5B: "Hyperframe number",
    0x6F5C: "Maximum value of Hyperframe number",
    0x6F61: "OPLMN selector with access tech",
    0x6F5D: "OPLMN selector",
    0x6F62: "HPLMN selector with access technology",
    0x6F06: "Access Rule reference",
    0x6F65: "RPLMN last used access tech",
    0x6FC4: "Network Parameters",
    0x6F11: "CPHS: Voice Mail Waiting Indicator",
    0x6F12: "CPHS: Service String Table",
    0x6F13: "CPHS: Call Forwarding Flag",
    0x6F14: "CPHS: Operator Name String",
    0x6F15: "CPHS: Customer Service Profile",
    0x6F16: "CPHS: CPHS Information",
    0x6F17: "CPHS: Mailbox Number",
    0x6FC5: "PLMN Network Name",
    0x6FC6: "Operator PLMN List",
    0x6F9F: "Dynamic Flags Status",
    0x6F92: "Dynamic2 Flag Setting",
    0x6F98: "Customer Service Profile Line2",
    0x6F9B: "EF PARAMS — Welcome Message",
    0x4F30: "Phone book reference file",
    0x4F22: "Phone book synchronization center",
    0x4F23: "Change counter",
    0x4F24: "Previous Unique Identifier",
    0x4F20: "GSM ciphering key Kc",
    0x4F52: "GPRS ciphering key",
    0x4F63: "CPBCCH information",
    0x4F64: "Investigation scan",
    0x4F40: "MexE Service table",
    0x4F41: "Operator Root Public Key",
    0x4F42: "Administrator Root Public Key",
    0x4F43: "Third party Root public key",
    0x6FC7: "Mail Box Dialing Number",
    0x6FC8: "Extension 6",
    0x6FC9: "Mailbox Identifier",
    0x6FCA: "Message Waiting Indication Status",
    0x6FCD: "Service Provider Display Information",
    0x6FD2: "UIM_USIM_SPT_TABLE",
    0x6FD9: "Equivalent HPLMN",
    0x6FCB: "Call Forwarding Indicator Status",
    0x6FD6: "GBA Bootstrapping parameters",
    0x6FDA: "GBA NAF List",
    0x6FD7: "MBMS Service Key",
    0x6FD8: "MBMS User Key",
    0x6FCE: "MMS Notification",
    0x6FD0: "MMS Issuer connectivity parameters",
    0x6FD1: "MMS User Preferences",
    0x6FD2: "MMS User connectivity parameters",
    0x6FCF: "Extension 8",
    0x5031: "Object Directory File",
    0x5032: "Token Information File",
    0x5033: "Unused space Information File, Efs under Telecom DF",
    0x6F3A: "Abbreviated Dialing Numbers",
    0x6F3B: "Fixed dialing numbers",
    0x6F3C: "Short messages",
    0x6F3D: "Capability Configuration Parameters",
    0x6F4F: "Extended CCP",
    0x6F40: "MSISDN",
    0x6F42: "SMS parameters",
    0x6F43: "SMS Status",
    0x6F44: "Last number dialed",
    0x6F49: "Service Dialling numbers",
    0x6F4A: "Extension 1",
    0x6F4B: "Extension 2",
    0x6F4C: "Extension 3",
    0x6F4D: "Barred Dialing Numbers",
    0x6F4E: "Extension 4",
    0x6F47: "SMS reports",
    0x6F58: "Comparison Method Information",
    0x6F54: "Setup Menu elements",
    0x6F06: "Access Rule reference",
    0x4F20: "Image",
    0x4F30: "Phone book reference file",
    0x4F22: "Phone book synchronization center",
    0x4F23: "Change counter",
    0x4F24: "Previous Unique Identifier"
}
"""
This is the file ID for restricted SIM access command
"""

urc_ports = {
    0: "all ports",
    1: "use UART port to output URCs",
    2: "use MODEM port to output URCs",
    3: "use ATCOM port to output URCs",
    4: "use cmux virtual port1 to output URCs",
    5: "use cmux virtual port2 to output URCs",
    6: "use cmux virtual port3 to output URCs",
    7: "use cmux virtual port4 to output URCs"
}
"""
This is the ports to use by URC interface
"""
