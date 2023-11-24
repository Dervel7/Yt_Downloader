from pytube import YouTube
import os
import psycopg2

connection = psycopg2.connect(host="localhost" , dbname = "YT_DL", user = "postgres" , password = "excalibur" , port = 5432)

cur = connection.cursor()


# read list of links from text file
with open('links.txt') as f:
    links = f.readlines()

# remove whitespace and newlines from links
links = [x.strip() for x in links]


destination = './Bonamin'

# create destination directory if it does not exist
if not os.path.exists(destination):
    os.makedirs(destination)

# iterate through links and download each video
for link in links:

    
    try:
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        print("this is the link " + link)
        print("this is the title " + yt.title)
        print("this is the destination folder " + destination)

        try:
            print("tha mpw k tha kanw to query")
            cur.execute("insert into dls.downloads (link , title , \"user\" , destination ) values (%s , %s , %s , %s)" , ( str(link) , str(yt.title) , 'Dimitrios' , str(destination)))
            connection.commit()
        except Exception as error:
            print("An exception occurred  " , error )

        # download the file
        out_file = video.download(output_path=destination)

        # save the file with video title
        base, ext = os.path.splitext(out_file)
        print("edw to lew egw " + yt.title)
        new_file = os.path.join(destination, yt.title + '.mp3')
        os.rename(out_file, new_file)



        # result of success
        print(yt.title + " has been successfully downloaded to " + destination)
    except Exception as e:
        print("Error downloading " + link + ": " + str(e))
