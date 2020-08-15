from fuzzywuzzy import fuzz # For String Matching operations
import webbrowser
from colored import bg , attr # FOr printing pretty console output

class YoutubeLauncher:

    def __init__(self , channels_data_json, action_data, match_percentage = 65 ):

        # Store Channel data and [action, data] structure
        self.channels_data_json = channels_data_json
        self.action_data = action_data
        self.match_percentage = match_percentage
        
        #Expected action/command flags
        self.CHANNEL_FLAG = "-c"
        self.GROUP_FLAG   = "-g"
        self.LIST_FLAG    = "-l"
    
    
    # Core Method, will call other supporting methods implicitly
    def launch(self):
        command  = self.action_data[0]
        data = self.action_data[1] 

        #IF Parser has specified a single channel launch action/command    
        if (command == self.CHANNEL_FLAG):

            matching_channel = self.__findBestMatchingChannel(data)
            if matching_channel != None:
                self.__initiateYoutubeLaunch(1, matching_channel)
            else:
                print("No Matching channel found.")

        #if parser has specified a group launch action/command
        elif (command == self.GROUP_FLAG):
            matching_channels = self.__findChannelsWithBestMatchingGroup(data)
            if (len(matching_channels) > 0):
                i = 1
                for matching_channel in matching_channels:
                    self.__initiateYoutubeLaunch(i, matching_channel)
                    i += 1
            else:
                print("No Matcing groups found.")

        #if parser has specified list action/command
        elif(command  == self.LIST_FLAG):
            self.__listAvailableChannelData()

   



    def __findChannelsWithBestMatchingGroup(self, group_names):
        matching_channels = []
        for channel in self.channels_data_json:
            group_matching_score = fuzz.partial_token_set_ratio(group_names, channel["groups"])
            if(group_matching_score >= self.match_percentage):
                matching_channels.append(channel)

        return matching_channels

    def __findBestMatchingChannel(self, channel_name):

        best_match_channel = None
        channel_with_max_score = 0

        for channel_index in range(0 , len(self.channels_data_json)):

            current_channel = self.channels_data_json[channel_index]
            local_score = fuzz.partial_token_set_ratio(channel_name, current_channel["name"])

            if(local_score > channel_with_max_score and local_score > self.match_percentage):
                best_match_channel = current_channel
                channel_with_max_score = local_score
        
        return best_match_channel


    def __listAvailableChannelData(self):
        i = 1
        for channel in self.channels_data_json:
            data_to_print = "{}) {} {} {}\n      URL = {}\n      Groups = {}".format(i, bg(25) ,channel["name"], attr(0), channel["url"], channel["groups"])
            print(data_to_print)
            i += 1


    def __initiateYoutubeLaunch(self,counter, channel):
        print("{}) {} Launching {} {}\n".format(counter, bg(25), channel["name"], attr(0)))
        webbrowser.open_new_tab(channel["url"])
      


        