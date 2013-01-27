#!/usr/bin/env python

""" Description and Comments {{{
* @version $Id:
* usage examples:
  $ ./craigslist_search.py -r 'sfbay,sandiego' -k ducati > ~/Desktop/ducs.html
  $ ./craigslist_search.py -r all -k s1000rr > ~/Desktop/bimmers.html
}}} """

""" XXX TODO dpugache: {{{
  - SQLite to store 'viewed' md5s
  - prettyfy report: by regon, new, sortable Jquery table, etc
}}} """

import sys
import re
from urllib2 import urlopen
from cli.app import CommandLineApp


class CLSearch(CommandLineApp):

  # ------------
  # __init__() :
  # ------------
  def __init__(self):
    """ inits class vard """
    super(CLSearch, self).__init__()
    self.ca_regions = [
      'bakersfield',
      'chico',
      'fresno',
      'goldcountry',
      'hanford',
      'humboldt',
      'imperial',
      'inlandempire',
      'mendocino',
      'merced',
      'modesto',
      'monterey',
      'orangecounty',
      'palmsprings',
      'redding',
      'sacramento',
      'santabarbara',
      'santamaria',
      'siskiyou',
      'susanville',
      'ventura',
      'visalia',
      'yubasutter',
      'sfbay',
      'losangeles',
      'sandiego',
    ]
    self.all_matches = []  # list of lists [[url, sbj], region] ... ]

  # --------
  # main() :
  # --------
  def main(self):
    """ grabs all pages for all regions """
    regions = self.ca_regions if self.params.regions.strip() == 'all' else [r.strip() for r in self.params.regions.split(",")]
    for region in regions:
      start = 0
      while True:
        url = "http://%s.craigslist.org/search/mca?query=%s&srchType=A&s=%d" % (region, self.params.keyword, start)
        num_of_results = self.getPage(region, url)
        start += 100
        if not num_of_results:
          break

    self.printReport()

  # -----------
  # getPage() :
  # -----------
  def getPage(self, region, url):
    """ gets the list of (url, subject, region) tuples for a given URL """
    try:
      contents = urlopen(url).read()
    except Exception, e:
      print "Can't open url %s: %s" % (url, str(e))
      sys.exit(1)
    # example <a href="http://stockton.craigslist.org/ctd/3537756420.html">&gt;&gt; 2010 Ducati Streetfighter</a>
    curr_matches = [(pair[0], pair[1], region) for pair in re.findall(r'<a href="(http://' + region + '.craigslist.org/\S*\d+.html)">(.*)</a>', contents) if re.search(self.params.keyword.strip(), pair[1], re.IGNORECASE)]
    self.all_matches += curr_matches
    if self.params.verbose:
      print "Processing region %s, offset %s" % (region, url.split('=')[-1])
    return len(curr_matches)

  # ---------------
  # printReport() :
  # ---------------
  def printReport(self):
    """ prints ugly HTML list """
    print "<ul>"
    for m in self.all_matches:
      print '<li><a href="%s">%s</a> ( %s ) </li>' % (m[0], m[1], m[2])
    print "</ul>"


if __name__ == '__main__':
  clsearch = CLSearch()
  clsearch.add_param("-r", "--regions", help="CSV list of regions", action="store")
  clsearch.add_param("-k", "--keyword", help="Keyword", action="store")
  clsearch.add_param("-v", "--verbose", help="Verbode mode", action="store_true")
  clsearch.run()
