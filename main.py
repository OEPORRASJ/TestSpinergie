# This is a Python script whose aim is to generate a json file from a json input file and
# a file with a list of changes, the generated file has to have the same structure of the json
# input file and the changes indicated in the other input file
# Input file 1 : configurationFile.json
# Input file 2 : inputChanges.txt
# Output file : modifiedFile.json (modifiable)
# Output : Report in console (success or failure of the change)

# Necessary module to    work with JSON files
import json
# Necessary module to work with List
from typing import List
# Necessary module to change the type of value to set
from ast import literal_eval


# 80 % StackOverflow
class DynamicAccessNestedDict:
    """Dynamically get/set nested dictionary keys of 'data' dict"""

    # One parameter, data of type dict
    def __init__(self, data: dict):
        self.data = data

    # Return the value according to a list with the keys "path" to the value
    def getVal(self, keys: List):
        data = self.data
        for key in keys:
            data = data[key]
        return data

    # Set a value according to a list with the keys "path" to the last key
    def setVal(self, keys: List, val) -> None:
        data = self.data

        lastkey = keys[-1]
        index = 0
        if isinstance(lastkey, list):
            lastkey = keys[-1][0]
            index = keys[-1][-1]

        for key in keys[:-1]:  # when assigning drill down to *second* last key
            if isinstance(key, list):
                data = data[key[0]][key[-1]]
                continue
            data = data[key]

        if isinstance(data[lastkey], list):
            data[lastkey][index] = val
        else:
            data[lastkey] = val

    # Return the modified dictionary
    def returnDict(self):
        return self.data


def modifications(data, inputChanges):
    """This function returns the same dict received as argument(data) with
    the changes applied according to the input file with the changes(inputChanges)"""
    global key, dictOut, index, dictEval
    for instruction in inputChanges:
        symbol = "\N{money-mouth face}"
        message = "The change was applied with succes!"
        try:
            # Obtaining the keys and value from the instruction
            keysValue = instruction.replace(' ', '').strip()
            keysValue = keysValue.split(sep=':', maxsplit=1)

            keys = keysValue[0].replace('"', '').split('.')
            value = literal_eval(keysValue[-1])

            # Check if the key has an index, accessing to a list
            for i in range(len(keys)):
                if '[' in keys[i]:
                    initSqrbr = keys[i].find('[')
                    endSqrbr = keys[i].find(']')
                    keys[i] = [keys[i][:initSqrbr], int(keys[i][initSqrbr + 1:endSqrbr])]

            # Prove that the key and index(if it is the case) exist
            # Error handling
            dictEval = data
            for key in keys:
                index = -1

                if isinstance(key, list):
                    index = key[-1]
                    key = key[0]
                    dictEval = dictEval[key][index]
                    if not isinstance(dictEval, dict):
                        break
                    if index > len(dictEval) - 1:
                        raise IndexError
                    continue

                if key not in dictEval:
                    raise KeyError

                dictEval = dictEval[key]

            # If all in the instruction is correct, apply the change
            dictOut = DynamicAccessNestedDict(data)
            dictOut.setVal(keys, value)

            # Return an object of type dict
            dictOut = dictOut.returnDict()

        # Key was not founded
        except KeyError:
            message = f"The key '{key}' does not exist in the JSON file."
            symbol = " \U00002716"

        # Index out of range in the list
        except IndexError:
            message = f"List index '{index}' is out of range."
            symbol = " \U00002716"

        # Any other error
        except:
            message = "Data in the instruction is corrupted!"
            symbol = " \U00002716"

        finally:
            report = symbol + " |" + instruction.replace('\n', '') + "| " + message
            print(report)

    return dictOut


# Opening the json file
try:
    configurationFile = open('configurationFile.json')
    inputChanges = open('inputChanges.txt')

    # Return json object as a dictionary
    data = json.load(configurationFile)

    # Calling the function to make the modifications
    dictOut = modifications(data, inputChanges)

    # Convert Python dict to JSON
    jsonOUT = json.dumps(dictOut, indent=2)

    # Writing the JSON object to a JSON file
    with open('modifiedFile.json', 'w') as outfile:
        outfile.write(jsonOUT)

except FileNotFoundError:
    print("It was not possible to open some file!")

except json.decoder.JSONDecodeError:
    print("There is an error in the format of the JSON File, file not opened!")

except:
    print("Something happens, program not executed !")

finally:
    print("Program ends!")
