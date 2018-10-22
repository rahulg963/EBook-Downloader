#!/usr/bin/python2

import requests
from bs4 import BeautifulSoup
import optparse
import sys
import os

class SearchBook :

	ROOT_URL = 'http://gen.lib.rus.ec/'
	available_books = []
	download_links = []

	def __init__(self, name) :

		self.sb(name)

	def sb(self, name) :

		if len(name) < 3 :
			print 'Book Name must contain minimum three characters'
			os._exit(0)

		name = name.replace(' ','+')
		url = self.ROOT_URL + 'search.php?req=' + str(name) + '&lg_topic=libgen&open=0&view=simple&res=25&phrase=0&column=def'
		r = requests.get(url)
		soup = BeautifulSoup(r.text, "lxml")
		book_lists = soup.find_all("table")[2]
		# there are total 4 tables inside the page, and the third table is storing the list of book

		headings = []
		for h in book_lists.tr.find_all("td") :
			headings.append(h.text.encode('utf-8'))
		#print headings

		no_of_available_books = len(book_lists.find_all("tr"))
		print "\n" + str(no_of_available_books - 1) + " Books found."

		for i in range(1,no_of_available_books) :
			self.available_books.append(book_lists.find_all("tr")[i])
		# available_books contains list of available books with <tr>
		#print self.available_books[0]

		for i in self.available_books :
			count = 0
			cur_inf = {}
			cur_inf['book_id'] = i.find_all('td')[0].text.encode('utf-8')
			for j in i.find_all('a') :
				count += 1
				if count in range(3,8) :
					cur_inf[str(count-2)] = j['href']
			self.download_links.append(cur_inf)
			#print cur_inf
		
		#print self.download_links

		available_books_details = []
		for b in self.available_books :
			book = []
			for s in b.find_all("td") :
				book.append(s.text.encode('utf-8'))
			available_books_details.append(book)
		#print available_books_details

		# Display of each book
		for item in available_books_details :
			print ""
			for r in range(9) :
				print headings[r] + " => " + item[r]

def main() :

	parser = optparse.OptionParser()
	parser.add_option('-s', help="Search for ebook by name", dest="bname")
	parser.add_option('-d', help="Download book by id", dest="bdwl")

	(options, args) = parser.parse_args()

	if len(sys.argv) == 1 :
		print str(parser.print_help())[:-4]
		os._exit(0)

	if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
		print str(parser.print_help())
		os._exit(0)

	if sys.argv[1] == '-s' : 
		bookName = options.bname
		sb_obj = SearchBook(bookName)

if __name__ == '__main__':

	main()