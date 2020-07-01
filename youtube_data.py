# Author:  Javier Diaz
# Date: 06/17/20
# Pledge: I pledge my honor that I have abided by the Stevens Honor System.
# Name: youtube_data.py
# Description: youtube_data.py searches YouTube for videos matching a search term. Once it retrieves the data it needs from the YouTube API, the program proceeds to print out the results of the search to the console. As well as creating a .csv file titled 'YouTube Results.csv', if already not created, which will contain the output of the youtube_search(s_term, s_max). Lastly, the program will print to the console the top 5 highest view counts, highest like percentage (like count / view count), and highest dislike percentage (dislike count / view count) all formatted in a proper way.
# Purpose: The purpose of the program is to allow the user to have s_max number of results written to the .csv file based on the search_term that they provide. As well as to show the top 5 most viewed, liked, and disliked content presented on the console.
# To run from terminal window:   python3 youtube_data.py 

from apiclient.discovery import build      # use build function to create a service object

import unidecode   #  need for processing text fields in the search results

import csv
import format

OUTPUT_MAX = 5
# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyBnfOACyzeDP827J7nMFGAjR14Xy6QtKeM"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version
csv_result_list = []    #list that holds the results printed to the csv
view_count_list = []    #list holding all of the view counts
like_percentage_list = []   #list holding the percentages of likes
dislike_percentage_list = []    #list holding the percentages of dislikes

#  function youtube_search retrieves the YouTube records

def youtube_search(s_term, s_max):
    #s_term - The key that will be searched for using the YouTube API
    #s_max - The maximum number of results that you will traverse
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(q=s_term, part="id,snippet", maxResults=s_max).execute()
    
    # search for videos matching search term;

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
            
            #Append the every view count to the list view_count_list
            view_count_list.append(int(viewCount))
            
            #Append the like percentages as a decimal to the list like_percentage_list
            like_percentage_list.append((float(likeCount)/float(viewCount)))
            
            #Append the dislike percentages as a decimal to the list dislike_percentage_list
            dislike_percentage_list.append((float(dislikeCount)/float(viewCount)))
            
            #Create a list with all of the contents in order to format output correctly
            result = [title, videoId, viewCount, likeCount, dislikeCount, commentCount]
            
            #Append the result list to csv_result_list which will be used for printing
            csv_result_list.append(result)
    
def format_percentages(list, like_or_dislike):
    #list - either like or dislike list
    #like_or_dislike - a boolean value that will allow the function to print the correct output
    #This function is used to print out the percentages or like or dislike. It will match the percentage with the objects that it corresponds to in order to ensure that the highest ranking order is intact.
    
    #Loop through list
    for cells in range(0, len(list)):
        if cells == OUTPUT_MAX:
            break
        target = list[cells]
        #Loop through csv_result_list which holds all of the content
        for x in range(0, len(csv_result_list)):
            #Check whether you are looking at a like percent list or dislike percent list
            if (like_or_dislike):
                compare_like = (float(csv_result_list[x][3])/float(csv_result_list[x][2]))
                #check if list[cell] is equal to the float division of the like count and view count
                if target == compare_like:
                    #print the result
                    print("{}. {}, {}, {:.2%}".format(cells + 1, csv_result_list[x][0], csv_result_list[x][1], list[cells]))
            else:
                #check if list[cell] is equal to the float division of the like count and view count
                compare_dislike = (float(csv_result_list[x][4])/float(csv_result_list[x][2]))
                if target == compare_dislike:
                    #print the result
                    print("{}. {}, {}, {:.2%}".format(cells + 1, csv_result_list[x][0], csv_result_list[x][1], list[cells]))

    
def print_highest_views(list):
    #list - a list holding the view counts [s_max] objects recieved
    print("Title", "Video ID", "View Count")\
    
    #traverse list
    for cells in range(0, len(list)):
        if cells == OUTPUT_MAX:
            break
        target = list[cells]
        #traverse the csv_result_list to check all objects
        for x in range(0, len(csv_result_list)):
            compare_view_count = int(csv_result_list[x][2])
            #check if the view count in list is equal to the view count in csv_result_list
            if target == compare_view_count:
                #print relusts
                print("{}. {}, {}, {}".format(cells + 1, csv_result_list[x][0], csv_result_list[x][1],  list[cells]))

def print_highest_like_percent(list):
    # list - like_percentage_list
    #Print header and the top five highest like percentages
    print("\n")
    print("Highest Like Percentage:")
    print("------------------------")
    print("Title", "Video ID", "Like Percentage")
    like_percentage_list.sort(reverse=True)
    format_percentages(like_percentage_list, True)

def print_lowest_like_percent(list):
    # list - dislike_percentage_list
    #Print header and the top five highest dislike percentages
    print("\n")
    print("Highest Dislike Percentage:")
    print("---------------------------")
    print("Title", "Video ID", "Dislike Percentage")
    dislike_percentage_list.sort(reverse=True)
    format_percentages(dislike_percentage_list, False)
    

def output_to_csv():
    #Create a .csv file that will print out the results from running youtube_search(). If already created, update the .csv file named 'Youtube Results.csv' and write the output to it
    
    #Open/Create .csv file
    with open("YouTube Results.csv", "w+") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        #Write the header
        writer.writerow(["Title", "Video ID", "Video Count", "Like Count", "Dislike Count", "Comment Count"])
        #Write the results of youtube_search()
        writer.writerows(csv_result_list)
        
def output_to_console(search_term, search_max):
    #Print the first header to the console
    print("\nAnalysis")
    print("--------\n")
    print("Search Term: {}".format(search_term))
    print("Search Max: {}\n".format(search_max))
    print("Highest Views:")
    print("--------------")

# main routine

#Get the input for what the user want to search for
search_term = str(raw_input("\nEnter a search term: "))

#Get the input for the number of results the user wants
search_max = input("Enter a maximum number of results: ")

#Search YouTube and get the results of passing search_term and search_max
#For this I added the '+1' to search_max because if I passed 1 then I would recieve no output
youtube_search(search_term, search_max + 1)

#Create and fill the .csv file
output_to_csv()

#Print the header to the console
output_to_console(search_term, search_max)

#Sort the view counts in descending order
view_count_list.sort(reverse=True)

#Print the view count to the console
print_highest_views(view_count_list)

#Print the highest percentage
print_highest_like_percent(like_percentage_list)

#Print the lowest percentage in descending order
print_lowest_like_percent(dislike_percentage_list)

print("\n")

