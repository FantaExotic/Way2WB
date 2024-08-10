
################################################################################
## 
## helpfunction:
## get_keyFromDictValue
##
## Description:
## this helpfunction returns the key to the corresponding dict value
## 
################################################################################
def get_keyFromDictValue(value: str, dict: dict) -> str:
    key_list = list(dict.keys())
    val_list = list(dict.values())
    pos = val_list.index(value)
    return key_list[pos]