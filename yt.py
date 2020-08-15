import sys   
import json  
import os

#Custom Imports
from CLIArgsParser import CLIArgsParser
from YoutubeLauncher import YoutubeLauncher


def loadChannelDataFromFile():
	filename = os.path.join(os.path.dirname(__file__) , "channels.json")
	try:
		with open(filename, 'r') as channels_data_file:
			return json.load(channels_data_file)
	except IOError as error:
		print("{}".format(error.message))
		return None#Stop Execution 

def main(args):

	#Load channel data
	channels_data_json = loadChannelDataFromFile()["channels"]
	if channels_data_json == None:
		return

    
	# Parse Arguments with our custom CLI parameters parser
    # It's not the best implementation of a CLI parser out there
    # But it will do our job just fine.
	cliParser = CLIArgsParser()

	# In case of successful parsing, we will get an array containing
    # [action, data-required-to-perform-this-action] structure
    # This [action,data] can be to launch a single channel or a group of channels or to just simply list channels.
    # For more information, please keep reading, CLIArgsParser is described in much more detail below.
	command_data = cliParser.parseCLIArguments(args)
	
	#If a Critical Error Occured
	if (command_data[0] == "-e" ):
		#Print the error and stop execution
		print(command_data[1])
		return

	# Perform action, using YoutubeLauncher
	# YoutubeLauncher Requires following parameters
    # 	1) Channels data
    #   2) command_data, which contains the [action,data] structure essentially letting it (YoutubeLauncher) know what to do
	youtube_launcher = YoutubeLauncher(channels_data_json , command_data)
	
	#Execute
	youtube_launcher.launch()
	

	

if ( __name__ == "__main__"):
	args = sys.argv

    # Make sure at least 2 parameters (filename + channel name) are provided
	args_good = True
	if (len(args) < 2):
		help_txt = " Please provide proper arguments, E.g\n\n  1) yt <channel name> \n    Example => yt linus tech tips\n\n  2) yt -g <group name>\n    Example yt -g technology\n\n  3) yt -l # To list channel names with meta data."
		print(help_txt)
		args_good = False
    
	 # Tidy up the parameters for the rest of the code
	if(args_good):
		#Transform text to lowercase
		args = list(map(lambda x: x.lower(), args)) 
		#Skip filename
		args = args[1 : len(args)] 
		main(args)
