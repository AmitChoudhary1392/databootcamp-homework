{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Library Imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#libraries:\n",
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import numpy as np\n",
    "import requests\n",
    "import xml.etree.ElementTree as ET\n",
    "import xmltodict\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "#Dependencies:\n",
    "from config import api_key, google_api_key"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "GoogleBooks/ GoodReads data cleaning, visualisation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#define global variables:\n",
    "books=[]\n",
    "isbns=[]\n",
    "results=[]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First 10 results from google API for fiction books"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#define categories for books:\n",
    "#categories=['fiction','nonfiction']      #'Fantasy','Thriller',\"adventure\",\"Horror\",\"Pyschology\",\"History\",\"romance\"\n",
    "\n",
    "category='fiction'\n",
    "\n",
    "#parameters\n",
    "params={'startIndex':0,\n",
    "    'key':google_api_key,\n",
    "        'maxResults':2}\n",
    "\n",
    "url= f'https://www.googleapis.com/books/v1/volumes?q=subject:{category}'\n",
    "\n",
    "#get request\n",
    "response= requests.get(url, params).json()\n",
    "\n",
    "result=response['items']\n",
    "\n",
    "results.append(result)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "category='nonfiction'\n",
    "#parameters\n",
    "params={'startIndex':0,\n",
    "    'key':google_api_key,\n",
    "        'maxResults':2}\n",
    "\n",
    "url= f'https://www.googleapis.com/books/v1/volumes?q=subject:{category}'\n",
    "\n",
    "#get request\n",
    "response= requests.get(url, params).json()\n",
    "#result=response['items'] if 'items' in response.keys() else \" \"\n",
    "\n",
    "#results.append(result)\n",
    "result=response['items']\n",
    "\n",
    "results.append(result)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "results[1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "len(results)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "9780451495426\n",
      "{'books': [{'id': 33595756, 'isbn': '045149542X', 'isbn13': '9780451495426', 'ratings_count': 87, 'reviews_count': 1098, 'text_reviews_count': 12, 'work_ratings_count': 763, 'work_reviews_count': 3132, 'work_text_reviews_count': 98, 'average_rating': '4.10'}]}\n",
      "9781501145667\n",
      "{'books': [{'id': 32895285, 'isbn': '1501145665', 'isbn13': '9781501145667', 'ratings_count': 189, 'reviews_count': 1724, 'text_reviews_count': 25, 'work_ratings_count': 232, 'work_reviews_count': 1934, 'work_text_reviews_count': 31, 'average_rating': '4.16'}]}\n",
      "9781456736866\n",
      "{'books': [{'id': 17642054, 'isbn': '1456736868', 'isbn13': '9781456736866', 'ratings_count': 0, 'reviews_count': 0, 'text_reviews_count': 0, 'work_ratings_count': 0, 'work_reviews_count': 0, 'work_text_reviews_count': 0, 'average_rating': '0.00'}]}\n",
      "9781451658903\n",
      "{'books': [{'id': 12106746, 'isbn': '1451658907', 'isbn13': '9781451658903', 'ratings_count': 4382, 'reviews_count': 20038, 'text_reviews_count': 520, 'work_ratings_count': 62882, 'work_reviews_count': 130460, 'work_text_reviews_count': 5028, 'average_rating': '4.15'}]}\n"
     ]
    }
   ],
   "source": [
    "books=[]\n",
    "#explore response from google API\n",
    "for i in range(len(results)):    \n",
    "   \n",
    "    book={}\n",
    "    for item in results[i]:\n",
    "        try:\n",
    "            book={\n",
    "                'image_url':item['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else \" \",\n",
    "                'id_book': item['id'],\n",
    "                'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else \" \",\n",
    "                'category/genre':item['volumeInfo']['categories'] if 'categories' in item['volumeInfo'].keys() else \" \",\n",
    "                'authors':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else \" \",\n",
    "                'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else \" \",\n",
    "                'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else \" \",\n",
    "                'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else \" \",\n",
    "                'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else \" \",\n",
    "                'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else \" \"     \n",
    "            }\n",
    "\n",
    "        except:\n",
    "            book = {'id_book': 'not found'}\n",
    "\n",
    "        #isbns.append(book['isbn'])\n",
    "       \n",
    "        #Good books review counts for isbn_string\n",
    "        url_gr='https://www.goodreads.com/book/review_counts.json'\n",
    "\n",
    "        parameters_gr={\"key\":api_key,\n",
    "            \"format\":'json',\n",
    "            \"isbns\":book['isbn']\n",
    "        }\n",
    "        \n",
    "        #if ISBN not found in goodreads\n",
    "        if requests.get(url_gr, params=parameters_gr).text!='No books match those ISBNs.':\n",
    "            \n",
    "            results_gr=requests.get(url_gr, params=parameters_gr).json()\n",
    "\n",
    "            id=results_gr['books'][0]['id']\n",
    "            # use goodreads book ID to get ratings distribution\n",
    "            \n",
    "            #Set URL\n",
    "            url_gr2='https://www.goodreads.com/book/show/'\n",
    "            \n",
    "            #set parameters\n",
    "            parameters_gr2={\n",
    "                \"key\":api_key,\n",
    "                \"format\":'xml',\n",
    "                \"id\":id\n",
    "            }\n",
    "            #get requests\n",
    "            results_gr2=requests.get(url_gr2, params=parameters_gr2)\n",
    "\n",
    "            #parse XML to string, define root\n",
    "            root_gr= ET.fromstring(results_gr2.text)\n",
    "            \n",
    "            rating_dist=root_gr.findall('.//rating_dist')[0].text\n",
    "\n",
    "            rating={\"5-stars\":rating_dist.split(\"|\")[0].split(':')[1],\n",
    "                \"4-stars\":rating_dist.split(\"|\")[1].split(':')[1],\n",
    "                \"3-stars\":rating_dist.split(\"|\")[2].split(':')[1],\n",
    "                \"2-stars\":rating_dist.split(\"|\")[3].split(':')[1],\n",
    "                \"1-star\":rating_dist.split(\"|\")[4].split(':')[1]\n",
    "                   }\n",
    "\n",
    "            reviews={\"ratings_count\":results_gr['books'][0]['work_ratings_count'],\n",
    "                    \"reviews_count\":results_gr['books'][0]['work_reviews_count'],\n",
    "                    'text_reviews_count':results_gr['books'][0]['work_text_reviews_count'],\n",
    "                    'average_rating':results_gr['books'][0]['average_rating'],\n",
    "                    'rating_dist':rating\n",
    "                     }\n",
    "            # append reviews to book\n",
    "            book['reviews']=reviews\n",
    "\n",
    "            #append books\n",
    "            books.append(book)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "books"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>authors</th>\n",
       "      <th>category/genre</th>\n",
       "      <th>description</th>\n",
       "      <th>id_book</th>\n",
       "      <th>image_url</th>\n",
       "      <th>isbn</th>\n",
       "      <th>language</th>\n",
       "      <th>published_date</th>\n",
       "      <th>publisher</th>\n",
       "      <th>reviews</th>\n",
       "      <th>title</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>[Mary C. Neal]</td>\n",
       "      <td>[Religion]</td>\n",
       "      <td>\"Dr. Mary Neal's unforgettable account of a 19...</td>\n",
       "      <td>StkxDwAAQBAJ</td>\n",
       "      <td>http://books.google.com/books/content?id=StkxD...</td>\n",
       "      <td>9780451495426</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Convergent Books</td>\n",
       "      <td>{'ratings_count': 763, 'reviews_count': 3132, ...</td>\n",
       "      <td>7 Lessons from Heaven</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>[Tererai Trent]</td>\n",
       "      <td>[Body, Mind &amp; Spirit]</td>\n",
       "      <td>Through one incredible woman’s journey from a ...</td>\n",
       "      <td>eFU3DwAAQBAJ</td>\n",
       "      <td>http://books.google.com/books/content?id=eFU3D...</td>\n",
       "      <td>9781501145667</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Simon and Schuster</td>\n",
       "      <td>{'ratings_count': 232, 'reviews_count': 1934, ...</td>\n",
       "      <td>The Awakened Woman</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>[Thomas G. Johnson Sr.]</td>\n",
       "      <td>[Fiction]</td>\n",
       "      <td>The Trials of Worly the Ward is a historic fic...</td>\n",
       "      <td>rJqgupUXGUYC</td>\n",
       "      <td>http://books.google.com/books/content?id=rJqgu...</td>\n",
       "      <td>9781456736866</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>AuthorHouse</td>\n",
       "      <td>{'ratings_count': 0, 'reviews_count': 0, 'text...</td>\n",
       "      <td>The Trials of Worly the Ward</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>[Stephen King]</td>\n",
       "      <td>[Fiction]</td>\n",
       "      <td>Returns to the rich landscape of Mid-World in ...</td>\n",
       "      <td>Nvkwjw2LToEC</td>\n",
       "      <td>http://books.google.com/books/content?id=Nvkwj...</td>\n",
       "      <td>9781451658903</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Simon and Schuster</td>\n",
       "      <td>{'ratings_count': 62882, 'reviews_count': 1304...</td>\n",
       "      <td>The Wind Through the Keyhole</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   authors         category/genre  \\\n",
       "0           [Mary C. Neal]             [Religion]   \n",
       "1          [Tererai Trent]  [Body, Mind & Spirit]   \n",
       "2  [Thomas G. Johnson Sr.]              [Fiction]   \n",
       "3           [Stephen King]              [Fiction]   \n",
       "\n",
       "                                         description       id_book  \\\n",
       "0  \"Dr. Mary Neal's unforgettable account of a 19...  StkxDwAAQBAJ   \n",
       "1  Through one incredible woman’s journey from a ...  eFU3DwAAQBAJ   \n",
       "2  The Trials of Worly the Ward is a historic fic...  rJqgupUXGUYC   \n",
       "3  Returns to the rich landscape of Mid-World in ...  Nvkwjw2LToEC   \n",
       "\n",
       "                                           image_url           isbn language  \\\n",
       "0  http://books.google.com/books/content?id=StkxD...  9780451495426       en   \n",
       "1  http://books.google.com/books/content?id=eFU3D...  9781501145667       en   \n",
       "2  http://books.google.com/books/content?id=rJqgu...  9781456736866       en   \n",
       "3  http://books.google.com/books/content?id=Nvkwj...  9781451658903       en   \n",
       "\n",
       "  published_date           publisher  \\\n",
       "0                   Convergent Books   \n",
       "1                 Simon and Schuster   \n",
       "2                        AuthorHouse   \n",
       "3                 Simon and Schuster   \n",
       "\n",
       "                                             reviews  \\\n",
       "0  {'ratings_count': 763, 'reviews_count': 3132, ...   \n",
       "1  {'ratings_count': 232, 'reviews_count': 1934, ...   \n",
       "2  {'ratings_count': 0, 'reviews_count': 0, 'text...   \n",
       "3  {'ratings_count': 62882, 'reviews_count': 1304...   \n",
       "\n",
       "                          title  \n",
       "0         7 Lessons from Heaven  \n",
       "1            The Awakened Woman  \n",
       "2  The Trials of Worly the Ward  \n",
       "3  The Wind Through the Keyhole  "
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#convert to books dataframe\n",
    "books_df=pd.DataFrame(books)\n",
    "books_df.head"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>authors</th>\n",
       "      <th>category/genre</th>\n",
       "      <th>description</th>\n",
       "      <th>id_book</th>\n",
       "      <th>image_url</th>\n",
       "      <th>isbn</th>\n",
       "      <th>language</th>\n",
       "      <th>published_date</th>\n",
       "      <th>publisher</th>\n",
       "      <th>reviews</th>\n",
       "      <th>title</th>\n",
       "      <th>ratings_count</th>\n",
       "      <th>reviews_count</th>\n",
       "      <th>text_reviews_count</th>\n",
       "      <th>average_rating</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>[Mary C. Neal]</td>\n",
       "      <td>[Religion]</td>\n",
       "      <td>\"Dr. Mary Neal's unforgettable account of a 19...</td>\n",
       "      <td>StkxDwAAQBAJ</td>\n",
       "      <td>http://books.google.com/books/content?id=StkxD...</td>\n",
       "      <td>9780451495426</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Convergent Books</td>\n",
       "      <td>{'ratings_count': 763, 'reviews_count': 3132, ...</td>\n",
       "      <td>7 Lessons from Heaven</td>\n",
       "      <td>763</td>\n",
       "      <td>3132</td>\n",
       "      <td>98</td>\n",
       "      <td>4.10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>[Tererai Trent]</td>\n",
       "      <td>[Body, Mind &amp; Spirit]</td>\n",
       "      <td>Through one incredible woman’s journey from a ...</td>\n",
       "      <td>eFU3DwAAQBAJ</td>\n",
       "      <td>http://books.google.com/books/content?id=eFU3D...</td>\n",
       "      <td>9781501145667</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Simon and Schuster</td>\n",
       "      <td>{'ratings_count': 232, 'reviews_count': 1934, ...</td>\n",
       "      <td>The Awakened Woman</td>\n",
       "      <td>232</td>\n",
       "      <td>1934</td>\n",
       "      <td>31</td>\n",
       "      <td>4.16</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>[Thomas G. Johnson Sr.]</td>\n",
       "      <td>[Fiction]</td>\n",
       "      <td>The Trials of Worly the Ward is a historic fic...</td>\n",
       "      <td>rJqgupUXGUYC</td>\n",
       "      <td>http://books.google.com/books/content?id=rJqgu...</td>\n",
       "      <td>9781456736866</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>AuthorHouse</td>\n",
       "      <td>{'ratings_count': 0, 'reviews_count': 0, 'text...</td>\n",
       "      <td>The Trials of Worly the Ward</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>[Stephen King]</td>\n",
       "      <td>[Fiction]</td>\n",
       "      <td>Returns to the rich landscape of Mid-World in ...</td>\n",
       "      <td>Nvkwjw2LToEC</td>\n",
       "      <td>http://books.google.com/books/content?id=Nvkwj...</td>\n",
       "      <td>9781451658903</td>\n",
       "      <td>en</td>\n",
       "      <td></td>\n",
       "      <td>Simon and Schuster</td>\n",
       "      <td>{'ratings_count': 62882, 'reviews_count': 1304...</td>\n",
       "      <td>The Wind Through the Keyhole</td>\n",
       "      <td>62882</td>\n",
       "      <td>130460</td>\n",
       "      <td>5028</td>\n",
       "      <td>4.15</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                   authors         category/genre  \\\n",
       "0           [Mary C. Neal]             [Religion]   \n",
       "1          [Tererai Trent]  [Body, Mind & Spirit]   \n",
       "2  [Thomas G. Johnson Sr.]              [Fiction]   \n",
       "3           [Stephen King]              [Fiction]   \n",
       "\n",
       "                                         description       id_book  \\\n",
       "0  \"Dr. Mary Neal's unforgettable account of a 19...  StkxDwAAQBAJ   \n",
       "1  Through one incredible woman’s journey from a ...  eFU3DwAAQBAJ   \n",
       "2  The Trials of Worly the Ward is a historic fic...  rJqgupUXGUYC   \n",
       "3  Returns to the rich landscape of Mid-World in ...  Nvkwjw2LToEC   \n",
       "\n",
       "                                           image_url           isbn language  \\\n",
       "0  http://books.google.com/books/content?id=StkxD...  9780451495426       en   \n",
       "1  http://books.google.com/books/content?id=eFU3D...  9781501145667       en   \n",
       "2  http://books.google.com/books/content?id=rJqgu...  9781456736866       en   \n",
       "3  http://books.google.com/books/content?id=Nvkwj...  9781451658903       en   \n",
       "\n",
       "  published_date           publisher  \\\n",
       "0                   Convergent Books   \n",
       "1                 Simon and Schuster   \n",
       "2                        AuthorHouse   \n",
       "3                 Simon and Schuster   \n",
       "\n",
       "                                             reviews  \\\n",
       "0  {'ratings_count': 763, 'reviews_count': 3132, ...   \n",
       "1  {'ratings_count': 232, 'reviews_count': 1934, ...   \n",
       "2  {'ratings_count': 0, 'reviews_count': 0, 'text...   \n",
       "3  {'ratings_count': 62882, 'reviews_count': 1304...   \n",
       "\n",
       "                          title  ratings_count  reviews_count  \\\n",
       "0         7 Lessons from Heaven            763           3132   \n",
       "1            The Awakened Woman            232           1934   \n",
       "2  The Trials of Worly the Ward              0              0   \n",
       "3  The Wind Through the Keyhole          62882         130460   \n",
       "\n",
       "   text_reviews_count average_rating  \n",
       "0                  98           4.10  \n",
       "1                  31           4.16  \n",
       "2                   0           0.00  \n",
       "3                5028           4.15  "
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#expand reviews columns to separate fields\n",
    "books_df['ratings_count']=books_df['reviews'].apply(lambda x:x['ratings_count'])\n",
    "books_df['reviews_count']=books_df['reviews'].apply(lambda x:x['reviews_count'])\n",
    "books_df['text_reviews_count']=books_df['reviews'].apply(lambda x:x['text_reviews_count'])\n",
    "books_df['average_rating']=books_df['reviews'].apply(lambda x:x['average_rating'])\n",
    "\n",
    "#final dataframe\n",
    "books_df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "isbns_string=\",\".join(isbns)\n",
    "isbns_string"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
