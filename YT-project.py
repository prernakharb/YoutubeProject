#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install google-api-python-client')



# In[2]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[3]:


#Api key connection

def Api_connect():
    Api_Id = 'AIzaSyCX1rl5nN2fMjINUiOzjB6iP2aGNENZbkA'
    
    api_service_name = 'youtube'
    api_version = 'v3'
    
    youtube = build(api_service_name, api_version, developerKey = Api_Id)
    
    return youtube
youtube = Api_connect()


# In[4]:


channel_ids = ['UCsKc38DDpGkNTHwsYjA0rbA',   #cravingsandcalories vlogs
               'UCnwL537dF3kV8hGVHvvof3Q',   #Golgappa Girl
               'UCGtu9J8Hp5lOOdNR4_nZa2Q',   #Foodie We
               'UCIZlw-2iKC-nXMGRJewEPOg',   #ShivArjun
               'UCh9ttnbZCsGfAqbH2Mi_IRQ',   #Sinful Foodie
               'UCVC9JRU1JpfupKHVV0sThOg',   #Veggie Paaj
               'UCm3uwvJw2KHp4aWRjj_IWTQ',   #so saute
               'UC2UWtuZR3kH-5C26HVMMB6A',   #Aayush Sapra
               'UCY36X43AGYzsny8vN693PKA',   #Radhi Arora
               'UCl90rgsYqIKsVHDJLHqKp_Q',   #Thakur Sisters
              ]



# In[5]:


## Function to get channel statistics


# In[6]:


def get_channel_info(youtube, channel_ids):
    all_data = []
    try:
        request = youtube.channels().list(
                  part = 'snippet, contentDetails, statistics',
                  id = channel_ids,
                  maxResults = 50
        )
        response = request.execute()

        for i in response['items']:    
                data = dict(Channel_name = i['snippet']['title'],
                         Channel_Id = i['id'],
                         Subscribers = i['statistics']['subscriberCount'],
                         Views = i['statistics']['viewCount'],
                         Total_videos = i['statistics']['videoCount'],
                         Channel_desciption =i['snippet']['description'],
                         Playlist_id = i['contentDetails']['relatedPlaylists']['uploads'])

                all_data.append(data)
    except:
            pass
    return all_data


# In[7]:


all_data


# In[8]:


get_channel_info(youtube, channel_ids)


# In[9]:


channel_statistics = get_channel_info(youtube, channel_ids)


# In[10]:


channel_data = pd.DataFrame(channel_statistics)


# In[11]:


channel_data


# In[12]:


channel_data.dtypes


# In[13]:


channel_data['Subscribers']= pd.to_numeric(channel_data['Subscribers'])
channel_data['Views']= pd.to_numeric(channel_data['Views'])
channel_data['Total_videos']= pd.to_numeric(channel_data['Total_videos'])
channel_data.dtypes


# In[14]:


sns.set(rc={'figure.figsize':(20,7)})
ax = sns.barplot(x = 'Channel_name', y = 'Subscribers', data = channel_data)


# In[15]:


sns.set(rc={'figure.figsize':(20,7)})
ax = sns.barplot(x = 'Channel_name', y = 'Views', data = channel_data)


# In[16]:


sns.set(rc={'figure.figsize':(20,7)})
ax = sns.barplot(x = 'Channel_name', y = 'Total_videos', data = channel_data)


# In[17]:


channel_data


# In[18]:


response1 = youtube.channels().list(id =','.join(channel_ids), 
                                  part = 'contentDetails').execute()
Playlist_id = response1['items'][0]['contentDetails']['relatedPlaylists']['uploads']

for i in range(len(response1['items'])):
     y = list[Playlist_id == response1['items'][i]['contentDetails']['relatedPlaylists']['uploads']]

response = youtube.playlistItems().list(
                                 part = 'snippet',
                                 playlistId = Playlist_id,
                                 maxResults = 50).execute()


# In[19]:


response


# In[97]:


def get_video_ids(youtube, Playlist_id):
    
    request = youtube.playlistItems().list(
              part = 'contentDetails',
              playlistId =Playlist_id,
              maxResults = 50)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response['nextPageToken']
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                       part = 'contentDetails',
                       playlistId = Playlist_id,
                       maxResults = 50,
                       pageToken = next_page_token)
            response = request.execute()
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
            
    return video_ids


# In[98]:


video_ids = get_video_ids(youtube, Playlist_id)


# In[99]:


video_ids


# In[30]:


len(video_ids)


# In[100]:


#function to get video details
def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                  part = 'snippet, statistics',
                  id = ','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            video_stats = dict(Channel_Id = video['snippet']['channelId'],
                               Channel_Name = video['snippet']['channelTitle'],
                               Video_id = video['id'],
                               Title = video['snippet']['title'],
                               Tags = video.get('tags'),
                               Thumbnail = video['snippet']['thumbnails'],
                               Description = video.get('description'),
                               Published_date = video['snippet']['publishedAt'],
                               Duration = video.get('duration'),
                               Views = video['statistics']['viewCount'],
                               Dislikes = video.get('dislikeCount'),
                               #Likes = video['statistics']['likeCount'],
                               Favoritecount = video['statistics']['favoriteCount'],
                               Comments = video.get('commentCount'),
                               Definition = video.get('definition'),
                               Caption_Status = video.get('caption')
                              )
            all_video_stats.append(video_stats)
    return all_video_stats


# In[101]:


video_details = get_video_details(youtube, video_ids)


# In[102]:


video_data = pd.DataFrame(video_details) 


# In[34]:


video_data


# In[35]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
#video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Favoritecount'] = pd.to_numeric(video_data['Favoritecount'])
video_data


# In[134]:


def get_comment_info(youtube, video_ids):
    Comment_data=[]
    try:
        for Video_id in video_ids:
                request = youtube.commentThreads().list(
                    part = 'snippet',
                    videoId = Video_id,
                    maxResults = 50
                )
                response = request.execute()
                for item in response['items']:
                    xdata = dict(Comment_Id = item['snippet']['topLevelComment']['id'],
                                             Video_id = item['snippet']['topLevelComment']['snippet']['videoId'],
                                             Comment_Text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                                             Comment_Author = item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                             Comment_Published = item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    Comment_data.append(xdata)

    except:
        pass
    return Comment_data


# In[135]:


Comment_data


# In[136]:


len(Comment_data)


# In[48]:


response


# In[137]:


Comment_details = get_comment_info(youtube, video_ids)


# In[138]:


Comment_details


# In[140]:


Comment_table = pd.DataFrame(Comment_details)


# In[141]:


Comment_table


# In[181]:


def get_playlist_details(youtube, channel_ids):
    next_page_token = None
    Complete_data=[]
    try:
        while True:
            request = youtube.playlists().list(
                     part = 'snippet,contentDetails',
                     channelId = channel_ids,
                     maxResults = 50,
                     pageToken = next_page_token
            )
            response = request.execute()

            for item in response['items']:
                Pdata = dict(Playlist_Id = item['id'],
                             Title = item['snippet']['title'],
                             Channel_Id = item['snippet']['channelId'],
                             Channel_Name = item['snippet']['channelTitle'],
                             PublishedAt = item['snippet']['publishedAt'],
                             Video_Count = item['contentDetails']['itemCount'])
                Complete_data.append(Pdata)

            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return Complete_data


# In[184]:


Complete_data


# In[165]:


len(Complete_data)


# In[166]:


response


# In[185]:


playlist_details = get_playlist_details(youtube, channel_ids)


# In[186]:


playlist_details


# In[187]:


def get_playlist_details(youtube, channel_ids):

        next_page_token = None
        All_data = []
        try: 
            for Channel_Id in channel_ids:
                while True:
                        request = youtube.playlists().list(
                                        part = 'snippet, contentDetails',
                                        channelId =  ','.join(channel_ids),
                                        maxResults = 50,
                                        pageToken = next_page_token
                        )
                        response = request.execute()
                        for item in response['items']:
                                atad = dict(Playlist_Id = item['id'],
                                            Title = item['snippet']['title'],
                                            Channel_Id = item['snippet']['channelId'],
                                            Channel_Name = item['snippet']['channelTitle'],
                                            PublishedAt = item['snippet']['publishedAt'],
                                            Video_Count = item['contentDetails']['itemCount'])
                                All_data.append(atad)

                        next_page_token = response.get('nextPageToken')
                        if next_page_token is None:
                                    break

        except:
             pass
        return All_data


# In[189]:


top10_videos = video_data.sort_values(by='Views', ascending = False).head(10)


# In[190]:


top10_videos


# In[191]:


sns.set(rc={'figure.figsize':(18,7)})
ax1 = sns.barplot(x ='Views', y = 'Title', data = top10_videos)


# In[192]:


video_data


# In[193]:


video_data['Month']= pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[194]:


video_data


# In[195]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date


# In[196]:


videos_per_month = video_data.groupby('Month', as_index=False).size()


# In[197]:


videos_per_month


# In[198]:


sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# In[199]:


videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'],categories=sort_order, ordered = True)


# In[200]:


videos_per_month = videos_per_month.sort_index()


# In[201]:


ax2 = sns.barplot(x='Month', y = 'size', data = videos_per_month)


# In[202]:


channel_data.to_csv('Video_Details(so saute).csv')


# In[203]:


video_data.to_csv('so saute.csv')


# In[204]:


video_data.to_json('so saute.json')


# In[205]:


pip install pymongo


# In[206]:


from googleapiclient.discovery import build
import pymongo


# In[207]:


client = pymongo.MongoClient('mongodb+srv://prernakharb14:Hr20Q6487@cluster0.kdfw5ek.mongodb.net/')


# In[208]:


client


# In[209]:


#upload to mongodb
db = client['youtube-project']


# In[218]:


def channel_details(channel_id):
    channelDetails = get_channel_info(youtube, channel_id)
    playlistDetails = get_playlist_details(youtube, channel_id)
    videoIds = get_video_ids(youtube,Playlist_id )
    videoDetails = get_video_details(youtube, videoIds)
    commentDetails = get_comment_info(youtube, videoIds)
    
    
    collection = db['channel_details']
    collection.insert_one({'channel_information':channelDetails,'playlist_information':playlistDetails,'videoId_information':videoIds,'videos_information':videoDetails,'comments_information':commentDetails})
    
    return 'upload completed successfully'


# In[219]:


insert =channel_details('UCGtu9J8Hp5lOOdNR4_nZa2Q')


# In[220]:


insert


# In[221]:


pip install psycopg2


# In[234]:


from googleapiclient.discovery import build
import pymongo
import psycopg2
import pandas as pd


# In[235]:


#table creation for channels, playlists, videos, commments

mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Hr20Q6487',
                        database = 'YT_project',
                        port = '5432')
cursor = mydb.cursor()

try:
    create_query = ''''create table if not exists channels(Channel_Name varchar(100),
                  Channel_id varchar(80) primary key,
                  Subscribers bigint,
                  Views bigint,
                  Total_videos int,
                  Channel_description text,
                  Playlist_id varchar(80))'''
    cursor.execute(create_query)
    mydb.commit()
except:
    print('Channels table already created')


# In[257]:


Channel_information = ['Channel_Name', 'Subscribers', 'Views', 'Total_videos', 'Channel_description', 'Playlist_id']


# In[280]:


ch_list = []
db = client['youtube-project']
collection = db['channel_details']
for ch_data in collection.find({},{part == 'snippet, contentDetails, statistics',
                                   id == 'UCGtu9J8Hp5lOOdNR4_nZa2Q'}):
    print(ch_data)
     #print(ch_data)
#     #ch_list.append(ch_data['channel_information'])

for i in ch_data['items']:
    fdata = dict(Channel_Id = i['snippet']['channelId'],
                 Channel_Name = i['snippet']['channelTitle'],
                 Subscribers = i['statistics']['subscriberCount'],
                 Views = i['statistics']['viewCount'],
                 Total_videos = i['statistics']['videoCount'],
                 Channel_desciption =i['snippet']['description'],
                 Playlist_id = i['contentDetails']['relatedPlaylists']['uploads']
             )
    ch_list.append(fdata)
    
return ch_list    


# In[271]:


ch_list


# In[272]:


df = pd.DataFrame(ch_list)


# In[273]:


df


# In[ ]:




