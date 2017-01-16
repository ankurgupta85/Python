from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulSoup, SoupStrainer
import pylab as pl
import numpy as np
import urllib
import os
import urllib2

import time
start_time = time.localtime()
print "Start time: "+ time.strftime("%b %d %Y %H:%M:%S", start_time)
movieList = "movieList.txt"
wholePage = "topMovies.html"
website="http://www.imdb.com"
topCharts ="/chart/top"
delimiter=";"
wholeTopChartUrl = website+topCharts
mainDirectory="mainDir"
moviesDirectory = "moviesDir"
moviesSummary = "moviesSummary"

yearRatingDict={}

if not os.path.exists(mainDirectory):
    os.makedirs(mainDirectory)
    
if not os.path.exists(moviesDirectory):
    os.makedirs(moviesDirectory)

if not os.path.exists(moviesSummary):
    os.makedirs(moviesSummary)
    
        

f = open(mainDirectory+os.sep+movieList,"wt")
f1 = open(mainDirectory+os.sep+wholePage,"wt")
urllib.URLopener.version = 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'
soup = BeautifulSoup(urllib2.urlopen(wholeTopChartUrl))
#posterColumn = soup.findAll('td', attrs={'class': 'posterColumn'})
#print soup
f1.write(str(soup))
#print table
#tableBody = soup.findAll("tbody",attrs={"class":"lister-list"})
#print tableBody
f1.close()
f1 = open(mainDirectory+os.sep+wholePage,"r")
soup = BeautifulSoup(f1)
#readMoviesData = f1.read()
titleColumn = soup.findAll('td', attrs={'class': 'titleColumn'})
ratingColumn = soup.findAll('td', attrs={'class':'ratingColumn imdbRating'})
ratings=[]
#print ratingColumn

for imdbrating in ratingColumn:
    allRatings = imdbrating.findAll("strong")
    for rating in allRatings:
        ratings.append(rating.getText())
    
    
#print ratings

#watchListColumn = soup.findAll('td', attrs={'class': 'watchlistColumn'})
#print ratingColumn
#print(titleColumn)
count=0
for title in titleColumn:
    
    allA = title.findAll("a")
    for a,rating in zip(allA,ratings) :
        count = count+1
        #print a.getText()
        if(count!=1):
            f.write("\n")
        link = a['href']
        completeLink = website+link
        #print rating
        moviewithRating = a.getText().encode("utf-8")+delimiter+rating.encode("utf-8")+delimiter+completeLink.encode('utf-8')
        f.write(moviewithRating)
        

f.close()
f1.close()

print "Please find main files inside "+mainDirectory
print "Starting to fetch meaningful data for analysis"

f= open(mainDirectory+os.sep+movieList)
moviesList = f.readlines()
f.close()
#print len(moviesList)

for movieInfo in moviesList:
    try:
        
        movie = movieInfo.split(delimiter)
    
        movieInformation = ""
        movieName = movie[0]
        movieInformation = movieInformation+ "Name: "+movieName+"\n"
        movieRating = movie[1]
        movieInformation = movieInformation+ "Rating: "+movieRating+"\n"
        movieLink = movie[2]
        movieInformation = movieInformation+ "Link: "+movieLink+"\n"
    #print movieName+"   "+movieRating+"  "+movieLink
        movieFile = movieName+".html"
        f1 = open(moviesDirectory+os.sep+movieFile,"wt")
        soup = BeautifulSoup(urllib2.urlopen(movieLink))
        f1.write(str(soup))
        f1.close()
        f1= open(moviesDirectory+os.sep+movieName+".html")
        soup = BeautifulSoup(f1)

#print(soup.findAll('a'))
    
    #print(soup.find('span',{'class':'itemprop'}).getText()) #Movie name
        movieYear = soup.find('span',{'class':'nobr'}).find('a').getText()
    #print(soup.find('span',{'class':'nobr'}).find('a').getText()) #Movie year
        movieInformation = movieInformation+ "Year: "+movieYear+"\n"
        
        if yearRatingDict.has_key(movieYear):
            existingRating = yearRatingDict.get(movieYear)
        else:
            existingRating = []
            
        existingRating.append(movieRating)
        yearRatingDict[movieYear] = existingRating  
        print yearRatingDict     
    #print(soup.find('div',{'class':'titlePageSprite star-box-giga-star'}).getText())  # Rating

        ratings = soup.find('div',{'class':'star-box-details'})
        ratingValue = ratings.find('span',{'itemprop':'ratingValue'}).getText()
        bestRating = ratings.find('span',{'itemprop':'bestRating'}).getText()
        ratingCount = ratings.find('span',{'itemprop':'ratingCount'}).getText()
        imdbReviewCounts = ratings.findAll('span',{'itemprop':'reviewCount'})
        ratingValue = ratingValue+"/"+bestRating
        movieInformation = movieInformation+ "Rating value: "+ratingValue+"\n"
        movieInformation = movieInformation+ "Rating Count: "+ratingCount+"\n"
    #print (ratingValue+"/"+bestRating)
    #print ratingCount
        userRating = imdbReviewCounts[0].getText()
        criticRating = imdbReviewCounts[1].getText()
        movieInformation = movieInformation+ "User Review counts: "+userRating+"\n"
        movieInformation = movieInformation+ "Critic Review Count: "+criticRating+"\n"
    #for imdbRating in imdbReviewCounts:
     #   print imdbRating.getText()

        summary=soup.find('p',{'itemprop':'description'}).getText()
        movieInformation = movieInformation+ "Summary: "+summary+"\n"
        storyline=soup.find('div',{'itemprop':'description'}).getText()
        movieInformation = movieInformation+ "Storyline: "+storyline+"\n"
    #print soup.find('p',{'itemprop':'description'}).getText()
    #print soup.find('div',{'itemprop':'description'}).getText()
        f2 = open(moviesSummary+os.sep+movieName+".txt","wt")
        #print movieInformation
    #movieInformation=movieInformation.decode('utf-8').encode('utf-8')
    #print movieInformation
    
        f2.write(str(movieInformation))
        
        
    except UnicodeEncodeError:
        print "Unicode encode Error for movie: "+movieName
        f2.close()
        continue
    except UnicodeDecodeError:
        print "Unicode decode Error for movie: "+movieName
        f2.close()
        continue
    finally:
        f1.close()
    




print "Please find movies files inside "+moviesDirectory
print "Please find movies summary inside "+moviesSummary

endTime = time.localtime()
print "End time: "+ time.strftime("%b %d %Y %H:%M:%S", endTime)
print yearRatingDict    
#print("--- %s seconds ---" % str(endTime - start_time) )
yearCountDict={}
sortedYearCountDict={}
for key in yearRatingDict:
    yearCountDict[key]=len(yearRatingDict[key])

count = 0    
print yearCountDict
for key in sorted(yearCountDict):
    if key >= '1990':
        sortedYearCountDict[key] = yearCountDict[key]
        count = count + yearCountDict[key]
        
print sortedYearCountDict
print count

d = sortedYearCountDict

 
X = np.arange(len(d))
pl.bar(X, d.values(), align='center', width=0.5)
pl.xticks(X, d.keys())
ymax = max(d.values()) + 1
pl.ylim(0, ymax)
pl.show()
    
#print("Table:\n")
#print(Table)  







