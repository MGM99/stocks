import os
import time
import re
import nsepy
from slackclient import SlackClient

token = 'xoxb-356641465604-GeJO0WuMP9rLVLkxmTa321H4'

slack_client = SlackClient(token)
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def slack_message(message, channel):
    # Sends the direct response back to the channel
    slack_client.api_call('chat.postMessage', channel=channel, 
                text=message, username="botuser",
                icon_emoji=':robot_face:')

def slack_direct_message(uname, channel, symbol):
    # Sends the direct response back to the channel
    response = get_quote_message(symbol)
    slack_client.api_call(
        "chat.postEphemeral",
        channel=channel,
        text=response, user=uname
    )

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            #print(event["text"],event["user"])
            return event["text"], event["user"], event["channel"]
    return None, None, None

def get_quote_message(symbol):
    try:
        s = nsepy.live.get_quote(symbol)
        #response =  "*{5}*\n_Current quote:_     {0} ({1}%)\n_Day Low:_\t\t     {3}\n_Day High:_\t\t    {2}\n_Open_\t\t\t       {4}".format(s["lastPrice"], s["pChange"],s["dayHigh"],s["dayLow"],s["open"],s["companyName"])
        #response =  "```{5}\nCurrent quote:\t\t{0} ({1}%)\nDay Low:\t\t\t  {3}\nDay High:\t\t\t {2}\nOpen\t\t\t\t  {4}```".format(s["lastPrice"], s["pChange"],s["dayHigh"],s["dayLow"],s["open"],s["companyName"])
        response =  "```{:25}\n{:25}  {:7} ({:5}%)\n{:25}     {:7}\n{:25}    {:7}\n{:25}      {:7}```".format(s["companyName"],"Current quote:",s["lastPrice"],s["pChange"],"Day Low:",s["dayLow"],"Day High:",s["dayHigh"],"Open:",s["open"])
    except IndexError:
        response = "Cannot get quote right now. Please try later!"
    return response

if __name__ == "__main__":
    #slack_message("Alert!", "stock-alerts");
    if slack_client.rtm_connect(with_team_state=False):
        print("Stock Bot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            symbol, uname, channel = parse_bot_commands(slack_client.rtm_read())
            if uname:
                slack_direct_message(uname, channel, symbol)
               # handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

    #print('Sending Message');
    #slack_message("From Python Script", "stocks");

