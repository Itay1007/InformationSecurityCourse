import q1
import q2
from q2_atm import ATM, ServerResponse
import time
import random


def test1(test_cipher):
    # Part 0:
    test_cipher.key = bytes([255, 25, 0, 1 ,26, 78, 0, 148])
    text = "RfGWCtRYhfnuFdNDpuVXFttBQaBlJbzm!@#$%^&*(){}[]0123456789"
    enc = test_cipher.encrypt(text)
    if enc != b'\xad\x7fGVY:R\xcd\x97\x7fnt\\*N\xd0\x8flVY\\:t\xd6\xaexBmP,z\xf9\xdeY#%?\x10&\xbe\xd70{|A\x130\xa5\xcd*44,y8\xad':
        failuer(1, "part 0 - Incorrect: {} instead of {}".format(enc, b'\xad\x7fGVY:R\xcd\x97\x7fnt\\*N\xd0\x8flVY\\:t\xd6\xaexBmP,z\xf9\xdeY#%?\x10&\xbe\xd70{|A\x130\xa5\xcd*44,y8\xad'
))
        #exit(0)

    # Part 1:
    test_cipher.key = generate_key(4)
    enc = test_cipher.encrypt("hello world!")
    dec = test_cipher.decrypt(enc)
    #if "hello world!" != dec:
    #    failure(1, "Part 1 - Incorrect: {0} instead of {1}".format(dec, "hello world!"))
    #    #exit(0)
        
    # Part 2:
    text = "89aPLFX2R4\nSMqWoct387\ngrSdiBnd5e\n1XxP2ftxvb\nR123P12P0m\nQ0nWbDNk3y\nXZZkW07AbS\n9054qNbNFW\n4yGxK3g7BD\n0ckLDlvhkC"
    test_cipher.key = generate_key(18)
    enc = test_cipher.encrypt(text)
    dec = test_cipher.decrypt(enc)
    if text != dec:
        failure(1, "Part 2 - Incorrect: {0} instead of {1}".format(dec, text))
        #exit(0)
        
    # Part 3:
    test_cipher.key = generate_key(7)
    text = "!@#$%^&*()_-+={}[]|/?<>,.;:'"
    enc = test_cipher.encrypt(text)
    dec = test_cipher.decrypt(enc)
    if text != dec:
        failure(1, "Part 3 - Incorrect: {0} instead of {1}".format(dec, text))
        #exit(0)
    success(1)


def test2(breaker):
    # Part 1:
    real_text = "Hey"
    fake_text = "hg23"
    real_score = breaker.plaintext_score(real_text)
    fake_score = breaker.plaintext_score(fake_text)
    if real_score <= fake_score:
        failure(2, "Part 1 - Incorrect:\nfake text score: {0}\nreal text score: {1}".format(fake_score, real_score))
        #exit(0)
        
    # Part 2:
    real_text = "Roses are red, Violets are blue"
    fake_text = "R@ses are r$d, Vi0lets are blue"
    real_score = breaker.plaintext_score(real_text)
    fake_score = breaker.plaintext_score(fake_text)
    if real_score <= fake_score:
        failure(2, "Part 2 - Incorrect:\nfake text score: {0}\nreal text score: {1}".format(fake_score, real_score))
        #exit(0)
        
    # Part 3:
    real_text = "Pink Floyd were an English rock band formed in London in 1964. Gaining an early following as one of the first British psychedelic groups, they were distinguished for their extended compositions, sonic experimentation, philosophical lyrics and elaborate live shows. They became a leading band of the progressive rock genre, cited by some as the greatest progressive rock band of all time."
    fake_text = "Lorem ipsum dolor aitamet, conzectetur adipiscing juit, SEQ do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad 12441 veniam, quis nostrud exercitation uzamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident SUNTIZ."
    real_score = breaker.plaintext_score(real_text)
    fake_score = breaker.plaintext_score(fake_text)
    if real_score <= fake_score:
        failure(2, "Part 3 - Incorrect:\nfake text score: {0}\nreal text score: {1}".format(fake_score, real_score))
        #exit(0)
    success(2)


def test3(cipher, breaker):
    # Part 1:
    plaintext = "Ancient Egypt - ancient civilization of eastern North Africa, concentrated along the lower reaches of the Nile River in what is now the modern country of Egypt. Egyptian civilization coalesced around 3150 BCE (according to conventional Egyptian chronology)[1] with the political unification of Upper and Lower Egypt under the first pharaoh.[2]"
    cipher.key = generate_key(2)
    enc = cipher.encrypt(plaintext)
    start = time.time()
    result = breaker.brute_force(enc, 2)
    stop = time.time()
    if (stop-start) >= 60.0:
        failure(3, "Part 1 - Took too long: {0} seconds".format(stop-start))
        #exit(0)
    elif result != plaintext:
        failure(3, "Part 1 - Incorrect")
        #exit(0)
    
    # Part 2:
    plaintext = "The Enigma machine is a cipher device developed and used in the early- to mid-20th century to protect commercial, diplomatic, and military communication. It was employed extensively by Nazi Germany during World War II, in all branches of the German military. The Enigma machine was considered so secure that it was used to encipher the most top-secret messages.[1]\nThe Enigma has an electromechanical rotor mechanism that scrambles the 26 letters of the alphabet."
    cipher.key = generate_key(2)
    enc = cipher.encrypt(plaintext)
    start = time.time()
    result = breaker.brute_force(enc, 2)
    stop = time.time()
    if (stop-start) >= 60.0:
        failure(3, "Part 2 - Took too long: {0} seconds".format(stop-start))
        #exit(0)
    elif result != plaintext:
        failure(3, "Part 2 - Incorrect")
        #exit(0)
    success(3)
    
    
def test4(cipher, breaker):
    # Part 1:
    plaintext = "Friedrich Wilhelm Nietzsche was a German philosopher, cultural critic and philologist whose work has exerted a profound influence on modern intellectual history. He began his career as a classical philologist before turning to philosophy. He became the youngest person ever to hold the Chair of Classical Philology at the University of Basel in 1869 at the age of 24. Nietzsche resigned in 1879 due to health problems that plagued him most of his life; he completed much of his core writing in the following decade. In 1889, at age 45, he suffered a collapse and afterward a complete loss of his mental faculties. He lived his remaining years in the care of his mother until her death in 1897 and then with his sister Elisabeth Forster-Nietzsche. Nietzsche died in 1900.\n\nNietzsche's writing spans philosophical polemics, poetry, cultural criticism, and fiction while displaying a fondness for aphorism and irony. Prominent elements of his philosophy include his radical critique of truth in favor of perspectivism; a genealogical critique of religion and Christian morality and a related theory of master-slave morality; the aesthetic affirmation of life in response to both the \"death of God\" and the profound crisis of nihilism; the notion of Apollonian and Dionysian forces; and a characterization of the human subject as the expression of competing wills, collectively understood as the will to power. He also developed influential concepts such as the Ubermensch and his doctrine of eternal return. In his later work, he became increasingly preoccupied with the creative powers of the individual to overcome cultural and moral mores in pursuit of new values and aesthetic health. His body of work touched a wide range of topics, including art, philology, history, music, religion, tragedy, culture, and science, and drew inspiration from Greek tragedy as well as figures such as Zoroaster, Arthur Schopenhauer, Ralph Waldo Emerson, Richard Wagner and Johann Wolfgang von Goethe.\n\nAfter his death, his sister Elisabeth became the curator and editor of Nietzsche's manuscripts. She edited his unpublished writings to fit her German ultranationalist ideology while often contradicting or obfuscating Nietzsche's stated opinions, which were explicitly opposed to antisemitism and nationalism. Through her published editions, Nietzsche's work became associated with fascism and Nazism; 20th-century scholars such as Walter Kaufmann, R.J. Hollingdale, and Georges Bataille defended Nietzsche against this interpretation, and corrected editions of his writings were soon made available. Nietzsche's thought enjoyed renewed popularity in the 1960s and his ideas have since had a profound impact on 20th and early-21st century thinkers across philosophy-especially in schools of continental philosophy such as existentialism, postmodernism and post-structuralism-as well as art, literature, poetry, politics, and popular culture."
    cipher.key = generate_key(16)
    enc = cipher.encrypt(plaintext)
    start = time.time()
    result = breaker.smarter_break(enc, 16)
    stop = time.time()
    if (stop-start) >= 60.0:
        failure(4, "Part 1 - Took too long: {0} seconds".format(stop-start))
        #exit(0)
    if result != plaintext:
        failure(4, "Part 1 - Incorrect")
        #exit(0)
    
    # Part 2:
    plaintext = "Mark Elliot Zuckerberg (born May 14, 1984) is an American media magnate, internet entrepreneur, and philanthropist. He is known for co-founding the social media website Facebook and its parent company Meta Platforms (formerly, Facebook, Inc.), of which he is the chairman, chief executive officer, and controlling shareholder.[1][2]Zuckerberg attended Harvard University, where he launched Facebook from his dormitory room in February 2004 with his roommates Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, and Chris Hughes. Originally launched to select college campuses, the site expanded rapidly and eventually beyond colleges, reaching one billion users by 2012. Zuckerberg took the company public in May 2012 with majority shares. In 2007, at age 23, he became the world's youngest self-made billionaire. As of March 2022, Zuckerberg's net worth was $74.5 billion according to the Forbes' Real Time Billionaires.\n\nSince 2008, Time magazine has named Zuckerberg among the 100 most influential people in the world as a part of its Person of the Year award, which he was recognized with in 2010.[3][4][5] In December 2016, Zuckerberg was ranked 10th on Forbes list of The World's Most Powerful People.[6]\n\nZuckerberg began using computers and writing software in middle school. His father taught him Atari BASIC Programming in the 1990s, and later hired software developer David Newman to tutor him privately. Zuckerberg took a graduate course in the subject at Mercy College near his home while still in high school. In one program, since his father's dental practice was operated from their home, he built a software program he called \"ZuckNet\" that allowed all the computers between the house and dental office to communicate with each other. It is considered a \"primitive\" version of AOL's Instant Messenger, which came out the following year.[17][18]\n\nA New Yorker profile said of Zuckerberg: \"some kids played computer games. Mark created them.\" Zuckerberg himself recalls this period: \"I had a bunch of friends who were artists. They'd come over, draw stuff, and I\'d build a game out of it.\" The New Yorker piece noted that Zuckerberg was not, however, a typical \"geek-klutz\", as he later became captain of his prep school fencing team and earned a classics diploma. Napster co-founder Sean Parker, a close friend, notes that Zuckerberg was \"really into Greek odysseys and all that stuff\", recalling how he once quoted lines from the Roman epic poem Aeneid, by Virgil, during a Facebook product conference.[11]\n\nDuring Zuckerberg's high-school years, he worked under the company name Intelligent Media Group to build a music player called the Synapse Media Player. The device used machine learning to learn the user's listening habits, which was posted to Slashdot[19] and received a rating of 3 out of 5 from PC Magazine.[20]\n\nThe New Yorker noted that by the time Zuckerberg began classes at Harvard in 2002, he had already achieved a \"reputation as a programming prodigy\". He studied psychology and computer science and belonged to Alpha Epsilon Pi and Kirkland House.[4][11][21] In his sophomore year, he wrote a program that he called CourseMatch, which allowed users to make class selection decisions based on the choices of other students and also to help them form study groups. A short time later, he created a different program he initially called Facemash that let students select the best-looking person from a choice of photos. According to Arie Hasit, Zuckerberg's roommate at the time, \"he built the site for fun\". Hasit explains:\n\nWe had books called Face Books, which included the names and pictures of everyone who lived in the student dorms. At first, he built a site and placed two pictures or pictures of two males and two females. Visitors to the site had to choose who was \"hotter\" and according to the votes there would be a ranking.[22]\n\nThe site went up over a weekend, but by Monday morning, the college shut it down, because its popularity had overwhelmed one of Harvard's network switches and prevented students from accessing the Internet. In addition, many students complained that their photos were being used without permission. Zuckerberg apologized publicly, and the student paper ran articles stating that his site was \"completely improper\".[22]\n\nThe following semester, in January 2004, Zuckerberg began writing code for a new website.[23] On February 4, 2004, Zuckerberg launched \"Thefacebook\", originally located at thefacebook.com.[24]\n\nSix days after the site launched, three Harvard seniors, Cameron Winklevoss, Tyler Winklevoss, and Divya Narendra, accused Zuckerberg of intentionally misleading them into believing he would help them build a social network called HarvardConnection.com, while he was instead using their ideas to build a competing product.[25] The three complained to The Harvard Crimson, and the newspaper began an investigation in response. While Zuckerberg tried to convince the editors not to run the story,[26] Zuckerberg broke into two of the editors' email accounts. He did it based on the editors' private login data logs from TheFacebook.[27][28]\n\nFollowing the official launch of the Facebook social media platform, the three filed a lawsuit against Zuckerberg that resulted in a settlement.[29] The agreed settlement was for 1.2 million Facebook shares.[30]\n\nZuckerberg dropped out of Harvard in his sophomore year in order to complete his project.[31] In January 2014, he recalled:\n\nI remember really vividly, you know, having pizza with my friends a day or two after-I opened up the first version of Facebook at the time I thought, \"You know, someone needs to build a service like this for the world.\" But I just never thought that we'd be the ones to help do it. And I think a lot of what it comes down to is we just cared more.[32]\n\nOn May 25, 2017, at Harvard's 366th commencement Day, Zuckerberg, after giving a commencement speech,[33] received an honorary degree from Harvard.[34][35]"
    cipher.key = generate_key(62)
    enc = cipher.encrypt(plaintext)
    start = time.time()
    result = breaker.smarter_break(enc, 62)
    stop = time.time()
    if (stop-start) >= 60.0:
        failure(4, "Part 2 - Took too long: {0} seconds".format(stop-start))
        #exit(0)
    if result != plaintext:
        failure(4, "Part 2 - Incorrect")
        #exit(0)
    success(4)


def test5(atm):
    # Part 1:
    pin = 0000
    enc_pin = atm.encrypt_PIN(pin)
    result = q2.extract_PIN(enc_pin)
    if pin != result:
        failure(5, "Part 1 - Incorrect: {} instead of 0000".format(result))
        #exit(0)
    
    # Part 2:
    pin = 1234
    enc_pin = atm.encrypt_PIN(pin)
    result = q2.extract_PIN(enc_pin)
    if pin != result:
        failure(5, "Part 2 - Incorrect: {} instead of 1234".format(result))
        #exit(0)
        
    # Part 3:
    pin = 6472
    enc_pin = atm.encrypt_PIN(pin)
    result = q2.extract_PIN(enc_pin)
    if pin != result:
        failure(5, "Part 3 - Incorrect: {} instead of 6472".format(result))
        #exit(0)
        
    # Part 4:
    pin = 9999
    enc_pin = atm.encrypt_PIN(pin)
    result = q2.extract_PIN(enc_pin)
    if result != pin:
        failure(5, "Part 4 - Incorrect: {} instead of 9999".format(result))
        #exit(0)
    success(5)
    

def test6(atm):
    # Part 1:
    credit_card = 12345678
    enc_credit = atm.encrypt_credit_card(credit_card)
    result = q2.extract_credit_card(enc_credit)
    if credit_card != result:
        failure(6, "Part 1 - Incorrect: {} instead of 12345678".format(result))
        #exit(0)
    
    # Part 2:
    credit_card = 123456789
    enc_credit = atm.encrypt_credit_card(credit_card)
    result = q2.extract_credit_card(enc_credit)
    if credit_card != result:
        failure(6, "Part 2 - Incorrect: {} instead of 123456789".format(result))
        #exit(0)
        
    # Part 3:
    credit_card = 783467201
    enc_credit = atm.encrypt_credit_card(credit_card)
    result = q2.extract_credit_card(enc_credit)
    if credit_card != result:
        failure(6, "Part 3 - Incorrect: {} instead of 783467201".format(result))
        #exit(0)
    success(6)
    
    
def test7(atm):
    fake_signature = q2.forge_signature()
    if atm.verify_server_approval(fake_signature) != True:
        fauilure(7, "Incorrect")
        #exit(0)
    success(7)
  

def failure(test_num, reason):
    print("TEST {}: FAILURE!\nREASON: {}".format(test_num, reason))
    
    
def success(test_num):
    print("TEST {}: SUCCESS!".format(test_num))


def generate_key(length):
    key = []
    for i in range(length):
        key.append(random.randint(0,255))
    key = bytes(key)
    return key
    
    
if __name__ == '__main__':
    print("### Q1 TEST RESULTS ###")
    test_cipher = q1.RepeatedKeyCipher()
    test_breaker = q1.BreakerAssistant()
    test1(test_cipher)
    test2(test_breaker)
    test3(test_cipher, test_breaker)
    test4(test_cipher, test_breaker)
    print("\n### Q2 TEST RESULTS ###")
    test_atm = ATM()
    test5(test_atm)
    test6(test_atm)
    test7(test_atm)
    print("\n### DONE ###")

