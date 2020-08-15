# Responsible For Parsing Command-Line parameters 
# And Generating [action, data] structure
class CLIArgsParser:


    #Returns an Array containing two items
    # 1) Command, this could be -c for single channel launch, -g for group launch or -l to only list channels, finally -e if there were any errors during parsing
    # 2) Data, this is the data required for the said command
    # 3) For Example, [-g , "technology"], will indicate to channels group with keyword `technology`
    def parseCLIArguments(self,args):
        
        CHANNEL_FLAG = "-c"
        GROUP_FLAG   = "-g"
        LIST_FLAG    = "-l"
        ERROR_FLAG   = "-e"

        #Handle single channel launch, Consider Everything is Query, join and return
        if(self.noFlagsProvided(args)): 
            return [CHANNEL_FLAG , ' '.join(args)]

        # Code does not handle both cases (-c and -g) at the same time, RAISE_ERROR
        elif (self.bothFlagsProvided(args)): 
            return [ERROR_FLAG, "ERROR: -g and -l flags can't be provided simultaneously\nPlease only provide one flag at a time."]

        #Handle group case, extract group query string 
        elif ("-g" in args): 
            group_query_index = args.index("-g") + 1

            # Check if group query exists after -g flag
            if(group_query_index < len(args)): 
                return [GROUP_FLAG , args[group_query_index]]
            else: #Raise Error
                return [ERROR_FLAG , "ERROR : -g flag provided without specifying group"]

        # Handle channel listing case        
        elif ("-l" in args):
            return [LIST_FLAG,None]
                
                
        else:
            return [ERROR_FLAG , "ERROR: Unknown error occured while parsing arguments."]
    

    
    #Helper Methods
    def noFlagsProvided(self,args):
	    return "-l" not in args and "-g" not in args

    def bothFlagsProvided(self, args):
        return "-l" in args and "-g" in args
