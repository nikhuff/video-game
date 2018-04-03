mport pygame as pg
import os
from settings import *
import random

class Dialogue:
    def __init__(self):
        self.sentences1 = ["Sometimes, all you need to do is completely make a fool of yourself and laugh it off to realise that life isn’t so bad after all.",
                 "Last Friday I thought I saw a spotted striped blue worm shake hands with a legless lizard.",
                 "I'd rather be a bird than a fish.",
                 "I want more detailed information. guess I'll go to the library",
                 "Where do random thoughts come from?",
                 "Steven turned in the research paper on Friday; otherwise, he would have not passed the class.",
                 "Let me help you with your baggage.",
                 "Some random person always comes asking for bread on fridays.",
                 "Sally told us a very exciting adventure story.",
                 "Don't step on the broken glass.",
                 "Yeah, I think the city, It is a good environment for learning English, no?",
                 "I often see the time 11:11 or 12:34 on clocks.",
                 "Ever wonder what makes your skin stay on?",
                 "my fortune cookie said: Abstraction is often one floor above you.",
                 "I think I will buy the red car, or I will lease the blue one.",
                 "We need to rent a room for our party tomorrow.",
                 "The body may perhaps compensate for the loss of true metaphysics.",
                 "My Mum tries to be cool by saying that she likes all the same things that I do.",
                 "Tom got a small piece of pie at the store, so he didn't share with me.",
                 "I am counting my calories, yet I really want dessert.",
                 "I really want to go to work, but I am too sick to drive.",
                 "I would have gotten the promotion, but my attendance wasn’t good enough.",
                 "I hear that Maggie is very pretty.",
                 "If Purple People Eaters are real… where do they find purple people to eat?",
                 "A song can make or ruin a person’s day if they let it get to them.",
                 "I currently 4 rocks in my pocket… and I don’t know why.",
                 "A glittering gem is not enough. sometimes you need 2 glittering gems",
                 "Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else try it either.",
                 "Everyone was busy, so I went to that new movie alone.",
                 "If the Easter Bunny and the Tooth Fairy had babies would they take your teeth and leave chocolate for you?",
                 "Lets all be unique together until we realise we are all the same.",
                 "What was the person thinking when they discovered cow’s milk was fine for human consumption… and why did they drink it in the first place!?",
                 "Italy is my favorite country; in fact, I plan to spend three weeks there next year.",
                 "The quick brown fox jumps over the lazy dog... or so they say",
                 "You know, malls are great places to shop! I can find everything I need under one roof.",
                 "That bus driver doesn't shave every month...",
                 "It takes a while to get to know Isabel, but two things you'll never forget are that she's bold and exciting.",
                 "Unfortunately Charles blunt nature is always there to ruin everything.",
                 "I need eggs. Not just any eggs though, I need eggs of an ostrich. They're the perfect size for what I have planned, it's going to be amazing.",
                 "I am so blue I'm greener than purple.",
                 "I stepped on a Corn Flake, I guess now I'm a Cereal Killer",
                 "I was asked to name all the presidents... I thought they already had names?",
                 "On a scale from one to ten what is your favourite colour of the alphabet.",
                 "Look, a distraction!",
                 "When life gives you lemons, chuck them at people you hate",
                 "Oh no, you're one of THEM!!!!",
                 "Thank you for noticing me, your noticing has been noticed",
                 "Buy some soap! It's clean!",
                 "Wanna help me steal a giraffe?",
                 "Nom nom nom nom nom!",
                 "Did you ever notice that pineapples never wear bathrobes?",
                 "check out my new pickup line: Hey, are you from France because your English sucks.",
                 "I am not a hoarder, I am a lover of things.",
                 "Do you think water is wet?",
                 "I have a cool pickup line: Hey, what's your favorite color? Because you smell nice",
                 "Why is there a 'd' in fridge but not in refrigerator?",
                 "Who closes the bus door once the bus driver gets off?",
                 "Why is the word abbreviation so long?",
                 "If I try to fail, but succeed, which one did I do?",
                 "What color are mirrors?",
                 "isn't it a bit unnerving that doctors call what they do practice?",
                 "I'm not a magician I just constantly lose rabbits and handkerchiefs.",
                 "People find it comforting when you say 'I'll pray for you' until they find out you worship Xarath the spider king.",
                 "Did you know, Moses had the first tablet that could connect to the cloud."
                 "The air is tasty here!"
                 "I heard Andrew is a real goofball"
                 "My boss Micah, he only wears sweats and sandals."
                 "My Buddy Nick is a great programmer, he says the key is to change stuff and just see what happens.",
                 "I am very busy right now",
                 "Weren't you ever taught not to talk to strangers?",
                 "....",
                 "What do you want?",
                 "I think I'll go to the park today",
                 "I like your outfit, cool hoodie!",
                 "What's with your hair? are you some kind of anime character?",
                 "I should probably get back to work.",
                 "The city is a busy place, but I enjoy living here.",
                 "The building here all look so similar, it's easy to get lost!",
                 "Sometimes while walking around I count all the bricks I step on",
                 "It feels like theres always construction going on in the city!",
                 "I moved here from the country, it's way different!",
                 "The cost of living here is so expensive!",
                 "Driving is faster but walking is much healthier!",
                 "Howdy!",
                 "How's it going?",
                 "Hello Stranger!",
                 "First impressions are very important."
                 ]
        self.sentences2 = []
    #pull sentence from list one to put in list two. If sentence one list is empty copy in sentence
    # list 2 to list 1 and delete the contents of list 2



    def random_sentence(self):
        if self.sentences1:
            rand = random.randint(0, len(sentences1)-1)
            sentence = self.sentences1[rand]
            self.sentences2.append(sentence)
            self.sentences1.remove(sentence)
            return sentence
        else:
            self.sentences1 = self.sentences2[:]
            sentences2.clear()
            rand = random.randint(0, len(sentences1) - 1)
            sentence = sentences1[rand]
            sentences2.append(sentence)
            sentences1.remove(sentence)
            return sentence
