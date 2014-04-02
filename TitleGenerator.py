#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import math,string,itertools,fractions,heapq,collections,re,array,bisect,random,urllib

#THIS CLASS WILL TAKE IN A PASSAGE AND CREATE A FAKE SUMMARY.
class TitleGenerator:

	def __init__(self, text = "DEFAULTS ARE BORING"):
		self.set_text(text)

	def set_text(self, text):
		"""Set text of object and prepare a dictionary of words used in text with the words that follow them."""
		
		if text == '':
			text = self.text
		
		#PARSE TEXT AND REMOVE BLANKS
		self.text = text.upper()
		self.text = "".join(i for i in self.text if 65<=ord(i)<=90 or ord(i)==46 or ord(i)==32)
		self.parsed_text = self.text.replace('.', ' .').split(' ')
		self.parsed_text = filter(lambda a: a != '', self.parsed_text)

		#CREATE DICTIONARY OF WORDS USED IN TEXT AS KEYS WITH FIRST WORD THAT FOLLOWS AS VALUES.
		self.text_dict = collections.defaultdict(list)
		for x in range(len(self.parsed_text)-1):
			self.text_dict[self.parsed_text[x]].append(self.parsed_text[x+1])

	def generate_title(self):
		"""Sample from distributions in dictionary to create a randomly generated title for text."""
		
		summary = ''
		current_word = ''
		
		while (current_word == ''):
			current_word = random.sample(self.parsed_text, 1)[0]

		while ('.' not in current_word):
			summary += current_word + ' '
			try:
				check_word = random.sample(self.text_dict[current_word], 1)[0]
			except:
				print 'FAILED WORD ENCOUNTERED: ' + current_word
				if summary == '':
					summary = self.generate_title()
					current_word='.'
				else:
					return summary.strip()
	
			if check_word != '':
				current_word = check_word
		
		#ENSURE A TITLE IS RETURNED
		if summary == '':
			summary = self.generate_title()
		
		return summary.strip()
	
	def get_thought_catalog_story(self, address, use_text=False):
		"""Get story from sent url on thoughtcatalog.com. No exception handling as of yet."""
		
		try:
			filehandle = urllib.urlopen(address)
		except Exception:
			print 'Unable to open sent URL.'
			return None, None
			
		begin_read = False
		web_element = False
		original_title = ''
		story_text = ''
		
		for lines in filehandle.readlines():
	
			#ORIGINAL TITLE
			if lines.find("</h1>")>=0:
				original_title = lines.replace('</h1>', '').replace(' ', '')
			
			#START OF TEXT
			if lines.find('<div class=\"entry grid_8 prefix_2\">')>=0:
				begin_read = True
			
			#END OF TEXT
			if lines.find('<!-- .entry grid_8 -->')>=0:
				break
			
			#READ TEXT AND REMOVE WEB ELEMENTS
			if (begin_read):

				for c in lines.strip().upper():
					if c == '<':
						web_element = True
					elif c == '>':
						web_element = False
					elif (web_element == False):
						story_text += c

		filehandle.close()
		return_story = "".join(i for i in story_text if 65<=ord(i)<=90 or ord(i)==46 or ord(i)==32)
		
		if (use_text):
			self.set_text(return_story)
		
		return original_title, return_story

#TEST 1
print '\n\nTEST 1'
sample_text = "As we detailed in Basecamp was under network attack, criminals assaulted our network with a DDoS attack on March 24. This is the technical postmortem that we promised. The main attack lasted a total of an hour and 40 minutes starting at 8:32 central time and ending around 10:12. During that window, Basecamp and the other services were completely unavailable for 45 minutes, and intermittently up and down or slow for the rest. In addition to the attack itself, Basecamp got put in network quarantine by other providers, so it wasn’t until 11:08 that access was restored for everyone, everywhere. The attack was a combination of SYN flood, DNS reflection, ICMP flooding, and NTP amplification. The combined flow was in excess of 20Gbps. Our mitigation strategy included filtering through a single provider and working with them to remove bogus traffic. To reiterate, no data was compromised in this attack. This was solely an attack on our customers’ ability to access Basecamp and the other services. There are two main areas we will improve upon following this event. Regarding our shield against future network attacks: We’ve formed a DDoS Survivors group to collaborate with other sites who’ve been subject to the same or similar attacks. That’s been enormously helpful already. We’re exploring all sorts of vendor shields to be able to mitigate future attacks even faster. While it’s tough to completely prevent any interruption in the face of a massive attack, there are options to minimize the disturbance. Law enforcement has been contacted, we’ve added our statement to their case file, and we’ll continue to assist them in catching the criminals behind this attack. Regarding the communication: There was a 20-minute delay between our first learning of the attack and reporting it to our customers via Twitter and status. That’s unacceptable. We’ll make changes to ensure that it doesn’t take more than a maximum of 5 minutes to report something like this again. Although we were successful at posting information to our status site (which is hosted off site), the site received more traffic than ever in the past, and it too had availability problems. We’ve already upgraded the servers that power the site and we’ll be conducting additional load and availability testing in the coming days. We will continue to be on high alert in case there is another attack. We have discussed plans with our providers, and we’re initiating new conversations with some of the top security vendors. Monday was a rough day and we’re incredibly sorry we weren’t more effective at minimizing this interruption. We continue to sincerely appreciate your patience and support. Thank you."
tg = TitleGenerator(sample_text)

print '\"' + tg.generate_title() + '\"'
tg.set_text('')
print '\"' + tg.generate_title() + '\"'

#TEST 2
print '\n\nTEST 2'
t, s = tg.get_thought_catalog_story("http://thoughtcatalog.com/taryn-lachter/2014/03/12-things-i-learned-from-starting-over/", True)
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'

#TEST 3
print '\n\nTEST 3'
t, s = tg.get_thought_catalog_story("http://thoughtcatalog.com/ari-eastman/2014/03/my-depression-is-cheating-on-me-with-my-trauma/", True)
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'

#TEST 4
print '\n\nTEST 4'
t, s = tg.get_thought_catalog_story("http://thoughtcatalog.com/whitney-van-laningham/2014/03/10-classes-i-wish-they-taught-in-college/", True)
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'
print '\"' + tg.generate_title() + '\"'

print '\n\nTEST 5'
t, s = tg.get_thought_catalog_story("http://thoughtcat23vr24rv2rc2crc2c2alog.com/whitney-van-laninht-in-college/", True)
