from Question import Question, found_matche, found_good_one
from file_function import print_debug
from selenium.webdriver.common.by import By
from random import randint

def test_Feature(Feature, driver): #test la presence d'une feature
    try:
        driver.find_element_by_class_name(Feature)
        return True
    except:
        return False

def found_verbe(data, phrase):
    i = 0
    for i in range(0, len(data)):
        if data[i] in phrase and data[i] != '':
            print_debug("[found_verbe] verbe found:"+data[i], "green")
            return data[i]
    print_debug("[found_verbe] None", "red")
    return None

def BOT(driver, module, accr):
    print_debug("[BOT] ####### WORKING #######","white")

    if not(module.test_blanc):
        if test_Feature("sentenceAudioReader", driver):
            driver.find_element_by_id("btn_speaker").click()
            driver.find_element_by_id("btn_non").click()

        if test_Feature("popupContent", driver):
            try:
                driver.find_element_by_id("btn_fermer").click()
            except:
                print_debug("[BOT] FAILED TO EXECUTE FEATURE IN","red")
                return "feature_in"

    if module.verbe_pron_I:
        pron_rep = test_Feature("instructions", driver)
    else:
        pron_rep = False

    try:
        Phrase = driver.find_element_by_class_name("sentence").text
        print_debug("[BOT] PHRASE: "+str(Phrase),"white")
    except:
        return "no_sentence"
            
    if not(pron_rep):

        question = found_matche(Phrase, module.data)

        if randint(1,100) > accr:
            if question.matche != "":
                if not(module.test_blanc):
                    driver.find_element_by_id("btn_pas_de_faute").click()
                else:
                    driver.find_element_by_class_name("noMistakeButton").click()
            else:
                print(question.phrase.split()[0].replace(",","").replace("'",""))
                driver.find_elements_by_xpath("//span[.='"+ question.phrase.split()[0].replace(",","").replace("'","").replace("-","") +"']")[0].click()
            return ["auto_fail"]
        
        if question.matche != "":
            try:
                driver.find_elements_by_xpath("//span[.='"+ question.err_in_phrase +"']")[ found_good_one(question.phrase, question.matche, question.err_in_phrase) ].click()
                print_debug("[BOT] EXECUTION CLICK DONE","green")
            except:
                try:
                    driver.find_elements_by_xpath("//span[.='"+ question.err_in_phrase.replace("…","").replace(",","").replace(".","").replace(";","") +"']")[ found_good_one(question.phrase, question.matche, question.err_in_phrase.replace("…","")) ].click()
                except:
                    print_debug("[BOT] FAILED TO EXECUTE CAN'T TOUCH: "+str(question.err_in_phrase),"red")
                    return "can't_touche &"+str(question.err_in_phrase)
        else:
            try:
                driver.find_element_by_class_name("noMistakeButton").click()
                print_debug("[BOT] EXECUTION NO MISTAKE DONE","green")
            except:
                return []
        
        return question.err_list
    else:
        if test_Feature("popupContent", driver):
            try:
                driver.find_element_by_id("btn_fermer").click()
            except:
                print_debug("[BOT] FAILED TO EXECUTE FEATURE IN","red")
                return "feature_in"
        consigne = driver.find_element_by_class_name("instructions").text
        phrase_clear = driver.find_element_by_class_name("sentence").text.replace("‑","-").replace(",","").replace(".","")
        phrase = phrase_clear.replace("‑","-").replace("-","- ").replace(",","").replace(".","").replace("'","' ").split()
        if "essentiellement" in consigne:
            verbe = found_verbe(module.ess, phrase)
        elif "autonome" in consigne:
            verbe = found_verbe(module.atnm, phrase)
        elif "passif" in consigne:
            verbe = found_verbe(module.pas, phrase)
        elif "accidentellement" in consigne:
            verbe = found_verbe(module.acc, phrase)
        else:
            question = found_matche(phrase_clear, module.match)
            verbe = question.corr_in_matche.replace("@","")

        if verbe != None and verbe != "":
            if "réfléchi" in consigne and "accidentellement" not in consigne:
                driver.find_elements_by_xpath("//span[.='"+ verbe.replace("-","").replace("'","") +"']")[found_good_one(question.phrase, question.matche, question.err_in_phrase)].click()
                print_debug("CLICK DONE", "green")

                if driver.find_elements_by_xpath("//span[@title='Mauvaise réponse']") != []:
                    print_debug("FAILED, learning...\n", "magenta")
                    add_data = driver.find_element_by_class_name("answerWord").text.replace("‑","-").replace("-","- ").replace(",","").replace(".","").replace("'","' ").split()
                    add_data = add_data[len(add_data)-1].replace(" ","")
                    match1 = question.matche_No_Change
                    match2 = match1[:match1.index(add_data, match1.index(">"))] + "<@" + add_data + ">" + match1[match1.index(add_data, match1.index(">"))+len(add_data):]
                    match2 = match2[ :match2.index("<") ] + add_data + match2[ match2.index(">")+1:]
                    module.match[module.match.index(match1)] = match2
            else:
                driver.find_elements_by_xpath("//span[.='"+ verbe +"']")[0].click()
                print_debug("CLICK DONE", "green")

        else:
            print_debug("FAILED, learning...", "magenta")
            print(phrase)
            driver.find_elements_by_xpath("//span[.='"+ phrase[0].replace("-","").replace("'","") +"']")[0].click()
            add_data = driver.find_element_by_class_name("answerWord").text.replace("‑","-").replace("-","- ").replace(",","").replace(".","").replace("'","' ").split()
            add_data = add_data[len(add_data)-1].replace(" ","")
            if "essentiellement" in consigne:
                module.ess += [add_data]
            elif "autonome" in consigne:
                module.atnm += [add_data]
            elif "passif" in consigne:
                module.pas += [add_data]
            elif "accidentellement" in consigne:
                module.acc += [add_data]
            else:
                module.match += [phrase_clear[:phrase_clear.index(add_data)] + "<@" + add_data + ">" + phrase_clear[phrase_clear.index(add_data)+len(add_data):]]
            
        return ["verbe_pron_I"]

def MANUAL(driver, module):
    if not(module.test_blanc):
        if test_Feature("sentenceAudioReader", driver):
            driver.find_element_by_id("btn_speaker").click()
            driver.find_element_by_id("btn_non").click()

        if test_Feature("popupContent", driver):
            try:
                driver.find_element_by_id("btn_fermer").click()
            except:
                print_debug("[BOT] FAILED TO EXECUTE FEATURE IN","red")
                return "feature_in"
    
    try:
        Phrase = driver.find_element_by_class_name("sentence").text
        print_debug("[BOT] PHRASE: "+str(Phrase),"white")
    except:
        return "no_sentence"
    
    if module.verbe_pron_I:
        pron_rep = test_Feature("instructions", driver)
    else:
        pron_rep = False

    if not(pron_rep):
        question = found_matche(Phrase, module.data)

        if question.matche != "":
            return question.err_in_phrase
        else:
            return "no_error"
    else:
        consigne = driver.find_element_by_class_name("instructions").text

        phrase_clear = driver.find_element_by_class_name("sentence").text.replace("‑","-").replace(",","").replace(".","")
        phrase = phrase_clear.replace("‑","-").replace("-","- ").replace(",","").replace(".","").replace("'","' ").split()
        if "essentiellement" in consigne:
            verbe = found_verbe(module.ess, phrase)
        elif "autonome" in consigne:
            verbe = found_verbe(module.atnm, phrase)
        elif "passif" in consigne:
            verbe = found_verbe(module.pas, phrase)
        elif "accidentellement" in consigne:
            verbe = found_verbe(module.acc, phrase)
        else:
            question = found_matche(phrase_clear, module.match)
            verbe = question.corr_in_matche.replace("@","")
        
        return verbe

