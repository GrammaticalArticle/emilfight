import random
from time import sleep, time
import os
from colorama import Fore, Back, Style, init
from math import ceil, floor
import base64
import sys

attackonly = True

sys.stdin.reconfigure(encoding="utf-8")

# Animations #
HUGOanimation = [
    """



          🮣─────🮣         
          ┌─────┐ |       
          └─────┘🮠




  """,
    """



         🮣────────🮣         
         ┌────────┐ |       
         └────────┘🮠




  """,
    """



       🮣───────────🮣         
       ┌───────────┐ |  
       │      　   │ │
       └───────────┘🮠



  """,
    """
             │
                          🮣
             │        🮣   
                  🮣
             │🮣  
      - - - -X- - - -
          🮣  │
       🮣
    🮣        │
 🮣

  """,
]

TAGEanimation = [
    """

    :----------------------------:
    =*--------------------------#-
    ++ M Inko | Œ port | Ħ docs *-
    ++ <portal.kunskapsskola..> *-
    ++ Välkommen till <Logbook> *-
    ++ Kunskapsskolan           *-
    ++ Västerås                 *-
    ++                          *-
    ++ Veckans matsedel         *-
    +*--------------------------#-
    :----------------------------:
    == -----------------------: +-
    ++ :----------------------: #-
    =+ -----------------------: *-
    ++ -======----------======: *-
    ++ :::::::-++++++++:::::::: *-
    =+        =+     :%:        *-
    ++        =+------#:        *-
    =*--------==++++++=---------#-
    :-----------::::::----------::

  """,
    """

    :----------------------------:
    =*--------------------------#-
    ++ M Inko | Œ port | Ħ docs *-
    ++ <portal.kunskapsskola..> *-
    ++ Välkommen till <Logbook> *-
    ++ Kunskapsskolan           *-
    ++ Västerås                 *-
    ++                          *-
    ++ Veckans matsedel         *-
    +*--------------------------#-
    :----------------------------:
    == -----------------------: +-
    ++ :----------------------: #-
    =+ -----------------------: *-
    ++ -======----------======: *-
    ++ :::::::-++++++++:::::::: *-
    =+        =+     :%:        *-
    ++        =+------#:        *-
    =*--------==++++++=---------#-
    :-----------::::::----------::

  """,
    """

    :----------------------------:
    =*--------------------------#-
    ++ M Inko | Œ port | Ħ docs *-
    ++ <portal.kunskapsskola..> *-
    ++ Välkommen till <Logbook> *-
    ++ Kunskapsskolan           *-
    ++ Västerås                 *-
    ++                          *-
    ++ Veckans matsedel         *-
    +*--------------------------#-
    :----------------------------:
    == -----------------------: +-
    ++ :----------------------: #-
    =+ -----------------------: *-
    ++ -======----------======: *-
    ++ :::::::-++++++++:::::::: *-
    =+        =+     :%:        *-
    ++        =+------#:        *-
    =*--------==++++++=---------#-
    :-----------::::::----------::

  """,
    """




             +         + 

              \\    /
                 \\  /
                  VV     

    +*--------------------------#-
    :=          __--__          =:
    ==        := #    =:        +-
    ++       : ### # #  :       #-
    =+       : # # ###  :       *-
    ++       : ###   #  :       *-
    ++        :=__  _#=:        *-
    =+            ¨¨            *-
    ++                          *-
    =*--------==++++++==--------#-
    :-----------::::::----------::

  """,
    """










    +*--------------------------#-
    :=          __--__          =:
    ==        := #    =:        +-
    ++       : ### # #  :       #-
    =+       : # # ###  :       *-
    ++       : ###   #  :       *-
    ++        :=__  _#=:        *-
    =+            ¨¨            *-
    ++                          *-
    =*--------==++++++==--------#-
    :-----------::::::----------::

  """,
]

OSCARanimation = [
    """





  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▓▓▓▓▓▓▒▒▓▓▓▓░░░░░░░░░░░░░░░░▒▒▓▓▓▓▓▓▒▒
  ▓▓▓▓▓▓████▓▓░░░░░░▒▒▓▓▒▒▓▓▓▓░░▒▒▓▓▓▓▓▓▓▓
  ▓▓██████████▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▒▒▒▒░░░░▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▒▒░░░░░░░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓
  ▓▓▒▒▒▒▒▒░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░
  ▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░







  """,
    """




  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒
  ░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒
  ▓▓▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒░░░░░░▒▒░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓░░░░░░▒▒░░▒▒▓▓▒▒▒▒▒▒▒▒▓▓▒▒░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▒▒░░▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▓▓██▓▓████▒▒░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▒▒▒▒░░░░▒▒▒▒▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓▒▒▓▓▓▓▓▓▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░▒▒▒▒
  ▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓▓▓▓▓▒▒░░░░░░░░░░░░░░░░░░░░░░
  ▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░







  """,
    """



  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
  ▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒
  ░░▒▒▒▒▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒
  ▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▒▒▒▒▒▒░░░░░░░░▒▒▒▒░░░░░░░░▒▒░░░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒
  ▓▓▓▓▓▓▓▓▓▓██████████▓▓░░░░░░▒▒▒▒░░▒▒▓▓░░▒▒▒▒▒▒▓▓▒▒▒▒░░░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░▓▓▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓████████████████▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▒▒▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▓▓▓▓██████████░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░▒▒▒▒▓▓▓▓▓▓
  ▓▓▓▓▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░░░░░░░░░░░░░░░░░░░
  ▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░




  """,
    """



                ▒█
           ░  ░░  
            ██▒   
           █▓  ░  
         █▓       
       ██         
      █           
    █             
  █               
█                 




  """,
]
# Animations complete #

init(autoreset=True)

attackmulti = 1.0
shieldmulti = 1.0
healthmulti = 1.0
alive = True
lang_code = "en"

encoded_censorwords = [
    "ZGljaw==",
    "bmlnZ2Vy",
    "ZXBzdGVpbg==",
    "bmlnZ2E=",
    "ZnVjaw==",
    "cGVkbw==",
    "cnVzc2lh",
    "cnlzc2xhbmQ=",
    "cHV0aW4=",
    "cHVo",
    "ZGlo",
    "bnVo",
    "cG9ybg==",
    "bW9sZXN0",
    "cmFwZQ==",
    "b25seWZhbnM=",
    "cmFwaXN0",
    "c2V4",
    "c2xhdmU=",
    "bjFnZ2E=",
    "bjFnZ2Vy",
    "bjFnZ2U=",
    "c2xhdg==",
]
censorwords = [base64.b64decode(w).decode() for w in encoded_censorwords]

# Dictionary for Language Strings
LANGUAGES = {
    "en": {
        "menu_invalid": "Please choose one of the listed numbers.",
        "name_prompt": "Enter the character name: ",
        "name_censored": "Your name has been CENSORED.",
        "name_new": "Please write a new name.",
        "name_too_long": "Your name is way too long.",
        "name_char_limit": "Please type less than 25 characters.",
        "name_confirm": "Are you sure you would like to be {name}?",
        "player_registered": "PLAYER 1: {name}",
        "yes_keys": ["y"],
        "challenge": "You have been challenged to a fight by {boss}!",
        "stats_hp": "{name}'s HP: {hp} HP",
        "attack_mult": "Attack multiplier: {val}%",
        "shield_mult": "Shield multiplier: {val}%",
        "health_mult": "Health multiplier: {val}%",
        "choose_option": "Choose an option",
        "action_attack": "ATTACK",
        "action_shield": "SHIELD",
        "err_enter": "You accidentally pressed enter... Try again!",
        "err_number": "Hmm... Try typing a number!",
        "player_attack": "You attack {boss} and deal {damage} damage!",
        "player_shield": "You use your shield, and shield {shield} hitpoints!",
        "boss_preparing": "{boss}'s preparing...",
        "shield_reflect": "Your shield was so strong it reflected {damage} damage back to {boss}!",
        "shield_partial": "Your shield blocks a part of the attack!",
        "shield_partial_hp": "{boss} deals {final_damage} damage instead of {damage}!",
        "victory_box": "VICTORY AGAINST {boss}",
        "game_over": "YOU SUCK...",
        "next_prompt": "What would you like to do next?",
        "fight_option": "Fight {boss}",
        "upgrade_attack": "Upgrade Attack",
        "upgrade_shield": "Upgrade Shield",
        "upgrade_health": "Upgrade Health",
        "upgrade_done": "{stat} upgraded! Multiplier is now {val}%",
        "attack_only_omar": "Did you really think I would not notice you picking Attack each time.",
        "speedrun_done": "Congratulations on completing the speedrun!",
        "speedrun_time": "Your time:",
        "speedrun_send": "Send your screenshot to ujh1906@edu.kunskapsskolan.se to add your time to the leaderboard!",
        "speedrun_fake": "(If you fake your screenshot, you are going to be permanently banned from speedrunning.)",
        "speedrun_code": "Code:"
    },
    "sv": {
        "menu_invalid": "Välj ett av sifrorna ovan.",
        "name_prompt": "Skriv in namnet på din karaktär: ",
        "name_censored": "Namnet har blivit CENSURERAT.",
        "name_new": "Skriv ett nytt namn, tack.",
        "name_too_long": "Ditt namn är för långt. Skriver du en insändare??",
        "name_char_limit": "Skriv mindre än 25 symboler, tack.",
        "name_confirm": "Är du säker att du vill vara {name}?",
        "player_registered": "SPELARE 1: {name}",
        "yes_keys": ["j", "y"],
        "challenge": "Du har blivit utmanad till en match av {boss}!",
        "stats_hp": "{name}s HP: {hp} HP",
        "attack_mult": "Attackmultiplikator: {val}%",
        "shield_mult": "Sköldmultiplikator: {val}%",
        "health_mult": "Hälsomultiplikator: {val}%",
        "choose_option": "Välj ett val",
        "action_attack": "ATTACKERA",
        "action_shield": "SKÖLD",
        "err_enter": "Du råkade trycka på enter... Försök igen!",
        "err_number": "Hmm... Testa att skriva en siffra!",
        "player_attack": "Du attackerar {boss} och gör {damage} skada!",
        "player_shield": "Du använder din sköld, och skyddar dig själv från {shield} skada!",
        "boss_preparing": "{boss} förbereder sig...",
        "shield_reflect": "Din sköld var så stark att den reflekterade {damage} skada tillbaka till {boss}!",
        "shield_partial": "Din sköld blockerar en del av attacken!",
        "shield_partial_hp": "{boss} gör {final_damage} skada istället för {damage}!",
        "victory_box": "SEGER MOT {boss}",
        "game_over": "DU FÖRLORADE...",
        "next_prompt": "Vad vill du göra nu?",
        "fight_option": "Slåss mot {boss}",
        "upgrade_attack": "Uppgradera Attack",
        "upgrade_shield": "Uppgradera Sköld",
        "upgrade_health": "Uppgradera Hälsa",
        "upgrade_done": "{stat} uppgraderad! Multiplikatorn är nu {val}%",
        "attack_only_omar": "Trodde du verkligen att jag inte skulle märka att du bara valde Attack.",
        "speedrun_done": "Grattis att du klarade speedrunnen!",
        "speedrun_time": "Din tid:",
        "speedrun_send": "Skicka din screenshot till ujh1906@edu.kunskapsskolan.se för att få din tid på leaderboarden!",
        "speedrun_fake": "(Om du förfalskar din screenshot, du kommer att bli permanent bannad från att speedrunna.)",
        "speedrun_code": "Kod:"
    },
    "ja": {
        "menu_invalid": "有効な番号を入力してください！",
        "name_prompt": "プレイヤー名を入力してください: ",
        "name_censored": "その名前は使用できません（検閲されました）。",
        "name_new": "別の名前を入力してください。",
        "name_too_long": "名前が長すぎます！",
        "name_char_limit": "25文字以内で入力してください。",
        "name_confirm": "{name} で確定しますか？",
        "player_registered": "プレイヤー1: {name}",
        "yes_keys": ["は", "y"],
        "challenge": "{boss} が勝負を仕掛けてきた！",
        "stats_hp": "{name}のHP: {hp}HP",
        "attack_mult": "攻撃倍率: {val}%",
        "shield_mult": "シールド倍率: {val}%",
        "health_mult": "体力倍率: {val}%",
        "choose_option": "コマンドを選択してください",
        "action_attack": "攻撃",
        "action_shield": "シールド",
        "err_enter": "おっと！ 攻撃が空振りした！（コマンドを選んでね）",
        "err_number": "謎の行動をとってしまった！ 番号を入力しよう。",
        "player_attack": "{boss}に攻撃！ {damage}のダメージを与えた！",
        "player_shield": "シールドを展開！ {shield}のダメージを防ぎ切る！",
        "boss_preparing": "{boss}が強力な一撃を構えている……！",
        "shield_reflect": "完璧なガード！ 衝撃を跳ね返し、{boss}に {damage}ダメージを与えた！",
        "shield_partial": "シールドで衝撃を和らげた！",
        "shield_partial_hp": "ボスは{damage}ではなく{final_damage}のダメージを与えます！",
        "victory_box": "{boss} を撃破！",
        "game_over": "力尽きてしまった ...",
        "next_prompt": "次は何をする？",
        "fight_option": "{boss} と戦う",
        "upgrade_attack": "攻撃力を強化",
        "upgrade_shield": "シールドを強化",
        "upgrade_health": "最大HPを強化",
        "upgrade_done": "{stat}完了！ 倍率が {val}% にアップ！",
        "attack_only_omar": "毎回『攻撃』を選んでいることに、私が気づかないとでも思ったの？",
        "speedrun_done": "スピードランのクリア、おめでとうございます！",
        "speedrun_time": "あなたのタイム：",
        "speedrun_send": "リーダーボードにあなたのタイムを掲載するには、スクリーンショットをujh1906@edu.kunskapsskolan.seまで送信してください！",
        "speedrun_fake": "（スクリーンショットを偽造した場合、スピードランへの参加資格を永久に剥奪されます。）",
        "speedrun_code": "コード："
    },
    "uk": {
        "menu_invalid": "Вибери одну з цифр.",
        "name_prompt": "Вибери ім'я: ",
        "name_censored": "Твоє ім'я ЗАЦЕНЗУРИЛОСЬ.",
        "name_new": "Будь ласка, напиши нове ім'я (без матів).",
        "name_too_long": "Твоє ім'я занадто довге.",
        "name_char_limit": "Максимум 25 символів. Ти що казку пишеш?",
        "name_confirm": "Ти точно хочеш бути {name}?",
        "player_registered": "ГРАВЕЦЬ 1: {name}",
        "yes_keys": ["т", "y"],
        "challenge": "{boss} викликав тебе на битву!",
        "stats_hp": "{name} HP: {hp} HP",
        "attack_mult": "Бонусна атака: {val}%",
        "shield_mult": "Бонусний щит: {val}%",
        "health_mult": "Бонусне здоров'я: {val}%",
        "choose_option": "Вибери одне:",
        "action_attack": "АТАКА",
        "action_shield": "ЩИТ",
        "err_enter": "Ти тикнув на Enter... Спробуй ще раз!",
        "err_number": "Нууу... Цифру напиши!",
        "player_attack": "Ти атакуюш {boss} і даєш {damage} урона!",
        "player_shield": "Ти використовуєш щит, і захищаєш себе від {shield} урона!",
        "boss_preparing": "{boss} підготовлюється...",
        "shield_reflect": "Щит був таким сильним, що він дав назад {damage} урона назад до {boss}!",
        "shield_partial": "Твій щит захистив тебе від частини атаки!",
        "shield_partial_hp": "{boss} наносить {final_damage} замість {damage} урону!",
        "victory_box": "ТИ ВИГРАВ ПРОТИ {boss}",
        "game_over": "ХРІНОВО ГРАЄШ...",
        "next_prompt": "Що хочеш робити зараз?",
        "fight_option": "Битись проти {boss}",
        "upgrade_attack": "Прокачати Атаку",
        "upgrade_shield": "Прокачати Щит",
        "upgrade_health": "Прокачати Здоров'я",
        "upgrade_done": "{stat} прокачано! Тепер бонус {val}%",
        "attack_only_omar": "Ти реально думав що я не помічу що ти щоразу вибирав атаку?",
        "speedrun_done": "Молодець, ти пройшов спідран!",
        "speedrun_time": "Твій час:",
        "speedrun_send": "Надішли твій скріншот до ujh1906@edu.kunskapsskolan.se щоб отримати місце на лідерборді!",
        "speedrun_fake": "(Якщо ти модифікуєш твій скріншот, ти будеш забанений від спідранів назавжди.)",
        "speedrun_code": "Код:"
    },
}

# Dictionary for Boss Data
BOSSES = {
    "Hugo": {
        "names": {"en": "Hugo", "sv": "Hugo", "ja": "ヒューゴ", "uk": "Хюго"},
        "hp": 100,
        "attack_low": 15,
        "attack_high": 40,
        "quotes": {
            "en": "is enraged...",
            "sv": "är arg...",
            "ja": "は激怒している……",
            "uk": "злий..."
        },
        "attack_lines": {
            "en": "forces you to eat licorice and deals {damage} damage!",
            "sv": "tvingmatar dig lakrits och gör {damage} skada!",
            "ja": "に無理やりサルミアッキを食べさせられ、{damage}ダメージを受けた！",
            "uk": "заставляє тебе їсти лакрицю і наносить {damage} урона!"
        },
        "animation": HUGOanimation,
    },
    "Oscar": {
        "names": {
            "en": "Oscar [HARD]",
            "sv": "Oscar [SVÅR]",
            "ja": "オスカー [ハード]",
            "uk": "Оскар [ВАЖКИЙ]"
        },
        "hp": 140,
        "attack_low": 10,
        "attack_high": 55,
        "quotes": {
            "en": "is ready to fight.",
            "sv": "är redo att slåss.",
            "ja": "は戦う準備ができている。",
            "uk": "готовий битися."
        },
        "attack_lines": {
            "en": "throws a Mini-Oscar at you and deals {damage} damage!",
            "sv": "kastar en Mini-Oscar på dig och gör {damage} skada!",
            "ja": "がミニ・オスカーを投げつけてきた！ {damage}ダメージを受けた！",
            "uk": "кидає в тебе Міні-Оскара і наносить {damage} урона!"
        },
        "animation": OSCARanimation,
    },
    "Tage Mage": {
        "names": {"en": "Tage Mage", "sv": "Tage Mage", "ja": "ターゲマーゲ", "uk": "Таге Маге"},
        "hp": 120,
        "attack_low": 15,
        "attack_high": 35,
        "quotes": {
            "en": "is hungry...",
            "sv": "är hungrig...",
            "ja": "はお腹を空かせている……",
            "uk": "голодний..."
        },
        "attack_lines": {
            "en": "closes your computer and deals {damage} damage!",
            "sv": "stänger din dator och gör {damage} skada!",
            "ja": "にノートパソコンを閉じられ、{damage}ダメージを受けた！",
            "uk": "закриває твій комп'ютер і наносить {damage} урона!"
        },
        "animation": TAGEanimation,
    },
    "Omar": {
        "names": {"en": "Omar", "sv": "Omar", "ja": "ウーマー", "uk": "Умар"},
        "hp": 160,
        "attack_low": 35,
        "attack_high": 90,
        "quotes": {
            "en": "is ready to fight.",
            "sv": "är redo att slåss.",
            "ja": "は戦う準備ができている。",
            "uk": "готовий битися."
        },
        "attack_lines": {
            "en": "lands a punch and deals {damage} damage!",
            "sv": "får in ett slag och gör {damage} skada!",
            "ja": "のパンチが炸裂！ {damage}ダメージを受けた！",
            "uk": "ударяє тебе і наносить {damage} урона!"
        },
        "post_victory": {
            "en": "Congratulations on beating Omar!\nThat is one difficult fight you survived!",
            "sv": "Grattis till att du besegrade Omar!\nDet var en riktigt svår fight du överlevde!",
            "ja": "ウーマー撃破おめでとう！\nかなりの死闘を生き残ったな！",
            "uk": "Молодець! Ти виграв проти Умара! \nТо була важка битва!"
        },
        "animation": None,
    },
    "Prime Omar": {
        "names": {"en": "Prime Omar", "sv": "Prime Omar", "ja": "かわいいウーマー", "uk": "Прайм Умар"},
        "hp": 160,
        "attack_low": 55,
        "attack_high": 110,
        "quotes": {
            "en": "is cracking his knuckles.",
            "sv": "knäcker sina knogar.",
            "ja": "は指の関節を鳴らしている。",
            "uk": "хрустить пальцями."
        },
        "attack_lines": {
            "en": "lands a punch and deals {damage} damage!",
            "sv": "får in ett slag och gör {damage} skada!",
            "ja": "のパンチが炸裂！ {damage}ダメージを受けた！",
            "uk": "ударяє тебе і наносить {damage} урона!"
        },
        "post_victory": {
            "en": "Congratulations on beating PRIME Omar!\nThat is one difficult fight you survived!",
            "sv": "Grattis till att du besegrade PRIME Omar!\nDet var en riktigt svår fight du överlevde!",
            "ja": "プライムウーマー撃破おめでとう！\nかなりの死闘を生き残ったな！",
            "uk": "Молодець! Ти виграв проти Прайм Умара! \nТо була важка битва!"
        },
        "animation": None,
    },
    "Mini Tage Mage": {
        "names": {"en": "Mini Tage Mage", "sv": "Mini Tage Mage", "ja": "ミニターゲマーゲ", "uk": "Міні Таге Маге"},
        "hp": 10000,
        "attack_low": 1,
        "attack_high": 10,
        "quotes": {
            "en": "is barely awake.",
            "sv": "är knappt vaken.",
            "ja": "は、かろうじて目が覚めている。",
            "uk": "ледве прокинувся."
        },
        "attack_lines": {
            "en": "somehow deals {damage} damage!",
            "sv": "på något sätt gör {damage} skada!",
            "ja": "{boss}は、なんと{damage}のダメージを受けた！",
            "uk": "якось наносить {damage} урона!"
        },
        "post_victory": {
            "en": "That was quite easy, wasn't it?",
            "sv": "Det var ganska lätt, eller hur?",
            "ja": "とても簡単でしたね。",
            "uk": "Це було доволі легко, хіба не так?"
        },
        "animation": None,
    },
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def tprint(text, delay=0.05 if lang_code=="ja" else 0.02, fore="", back="", style="", newline=True):
    for char in str(text):
        print(fore + back + style + char, end="", flush=True)
        sleep(delay)
    if newline:
        print()


def get_text(key, **kwargs):
    lang_dict = LANGUAGES.get(lang_code, LANGUAGES["en"])
    template = lang_dict.get(key, LANGUAGES["en"].get(key, ""))
    if isinstance(template, str):
        return template.format(**kwargs)
    return template


def get_menu_choice(valid_options):
    valid_options = set(valid_options)
    while True:
        pick = input("> ")
        if pick and pick[0] in valid_options:
            return pick[0]
        tprint(get_text("menu_invalid"), fore=Fore.YELLOW)


def namepick():
    clear()
    tprint(get_text("name_prompt"), style=Style.BRIGHT, newline=False)
    name = input()
    if any(censorword in name.lower() for censorword in censorwords):
        tprint(get_text("name_censored"), fore=Fore.RED, style=Style.BRIGHT)
        tprint(get_text("name_new"), fore=Fore.RED, style=Style.BRIGHT)
        return namepick()

    if len(name) > 25:
        tprint(get_text("name_too_long"), fore=Fore.RED, style=Style.BRIGHT)
        tprint(get_text("name_char_limit"), fore=Fore.RED, style=Style.BRIGHT)
        return namepick()

    tprint(get_text("name_confirm", name=name), delay=0.01)
    pick = input("Ja/Nej: " if lang_code == "sv" else "はい・いいえ: " if lang_code == "ja" else "Так/Ні: " if lang_code == "uk" else "Yes/No: ")
    if pick and pick[0].lower() in LANGUAGES[lang_code]["yes_keys"]:
        tprint(get_text("player_registered", name=name.upper()))
        return name
    elif not pick:
        tprint(get_text("player_registered", name=name.upper()))
        return name
    else:
        return namepick()

def formatHP(hp):
    return str(floor(hp)).rjust(3)


def showstats(p_name, p_hp, b_name, b_hp):
    tprint("\n" + "=" * 20)
    tprint(get_text("stats_hp", name=p_name, hp=formatHP(p_hp)), fore=Fore.GREEN)
    tprint(get_text("stats_hp", name=b_name, hp=formatHP(b_hp)), fore=Fore.RED)
    tprint("=" * 20 + "\n")


def fightloop(boss_key, playername):
    global alive, attackmulti, shieldmulti, healthmulti
    boss = BOSSES[boss_key]

    boss_name = boss["names"].get(lang_code, boss["names"]["en"])
    bossHP = boss["hp"]
    playerHP = 100 * healthmulti

    # Challenge message
    tprint(get_text("challenge", boss=boss_name), fore=Fore.RED, style=Style.BRIGHT)
    tprint(
        f"\n{get_text('attack_mult', val=int(floor(attackmulti * 100)))}\n"
        f"{get_text('shield_mult', val=int(floor(shieldmulti * 100)))}\n"
        f"{get_text('health_mult', val=int(floor(healthmulti * 100)))}"
    )
    sleep(.5)

    quote = boss["quotes"].get(lang_code, boss["quotes"]["en"])
    tprint(f"{boss_name} {quote}", fore=Fore.RED, style=Style.BRIGHT)
    sleep(1)

    while playerHP > 0 and bossHP > 0:
        showstats(playername, playerHP, boss_name, bossHP)

        tprint(get_text("choose_option"), style=Style.BRIGHT)
        tprint("1. ", newline=False)
        tprint(get_text("action_attack"), fore=Fore.RED)
        tprint("2. ", newline=False)
        tprint(get_text("action_shield"), fore=Fore.BLUE)

        choice = input("> ")
        player_defense = 0
        clear()

        if not choice:
            tprint(get_text("err_enter"), fore=Fore.YELLOW)
            sleep(.5)
            continue
        elif choice[0] in ["1", "１"]:
            damage = random.randint(ceil(20 * attackmulti), ceil(35 * attackmulti))
            bossHP -= damage
            tprint(
                get_text("player_attack", boss=boss_name, damage=damage), fore=Fore.RED
            )
        elif choice[0] in ["2", "２"]:
            player_defense = random.randint(
                ceil(10 * shieldmulti), ceil(50 * shieldmulti)
            )
            tprint(get_text("player_shield", shield=player_defense), fore=Fore.BLUE)
        else:
            tprint(get_text("err_number"), fore=Fore.YELLOW)
            sleep(.5)
            continue

        if bossHP <= 0:
            break

        # Boss Turn
        sleep(.5)
        tprint(get_text("boss_preparing", boss=boss_name), fore=Fore.RED)
        sleep(0.25)
        boss_damage = random.randint(boss["attack_low"], boss["attack_high"])
        if boss == "Mini Tage Mage" and boss_damage == 10:
            boss_damage = 200

        if player_defense > boss_damage:
            reflect_damage = int(player_defense - boss_damage)
            bossHP = int(bossHP - reflect_damage)
            tprint(
                get_text("shield_reflect", damage=reflect_damage, boss=boss_name),
                fore=Fore.CYAN,
            )
        else:
            if boss["animation"]:
                for frame in boss["animation"]:
                    clear()
                    print(frame)
                    sleep(0.2)
            
            final_damage = boss_damage - player_defense
            playerHP -= final_damage
            if player_defense > 0:
                tprint(get_text("shield_partial"))
                tprint(get_text("shield_partial_hp", boss=boss_name, final_damage=final_damage, damage=boss_damage))

            
            attack_msg = boss["attack_lines"].get(lang_code, boss["attack_lines"]["en"])
            tprint(
                f"{boss_name} " + attack_msg.format(damage=final_damage), fore=Fore.RED
            )

        sleep(.5)

    clear()
    if playerHP > 0:
        tprint("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓", fore=Fore.YELLOW,   style=Style.BRIGHT)
        tprint(
            f"┃ {get_text('victory_box', boss=boss_name.upper()).center(26)} ┃",
            fore=Fore.YELLOW,
            style=Style.BRIGHT,
        )
        tprint("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛", fore=Fore.YELLOW, style=Style.BRIGHT)

        if "post_victory" in boss and boss["post_victory"]:
            sleep(.5)
            msg = boss["post_victory"].get(lang_code, boss["post_victory"]["en"])
            tprint(f"\n{msg}\n", fore=Fore.GREEN, style=Style.BRIGHT)
            sleep(1)
    else:
        alive = False
        tprint("╔══════════════════════╗")
        tprint(
            "║ " + get_text("game_over").center(20) + " ║",
            fore=Fore.RED,
            style=Style.BRIGHT,
        )
        tprint("╚══════════════════════╝")


# Intro
clear()
sleep(.5)
tprint("┏━━━━━━━━━━━━━━┓")
tprint("┃     EMIL     ┃")
tprint("┃  ", newline=False)
tprint("BOSS FIGHT", fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint("  ┃")
tprint("┃  ", newline=False)
tprint("SIMULATOR!", fore=Fore.YELLOW, style=Style.BRIGHT, newline=False)
tprint("  ┃")
tprint("┗━━━━━━━━━━━━━━┛")
tprint("Version 5.1! Changed new boss")

tprint("\n┏━━━━━━━━━━━━━━━━┓\n┃ ENTER TO START ┃\n┗━━━━━━━━━━━━━━━━┛", delay=0.01)
input()

clear()

tprint("Send an email to ", newline=False)
tprint("ujh1906@edu.kunskapsskolan.se", fore=Fore.GREEN, style=Style.BRIGHT, newline=False)
tprint(" to log your time! (with a screenshot)")
tprint("The time will start as soon as you finish choosing a name.")

print()
tprint("Speedrun scoreboard:")
tprint("* if a time is \"old\", it means it was in the old version")
tprint("Current version (v5.1) times")
tprint("[· 1] [NO] None        - X:XX.X", fore=Fore.YELLOW, style=Style.BRIGHT)
tprint("[· 2] [NO] None        - X:XX.X", fore=Fore.RED, style=Style.BRIGHT)
tprint("[· 3] [NO] None        - X:XX.X", fore=Fore.YELLOW, style=Style.BRIGHT)
print()
print()
tprint("Old version times")
tprint("[· 1] [SV] Axelosaurus - 2:27.0 [v5   PRIME]", fore=Fore.YELLOW, style=Style.BRIGHT)
tprint("[· 2] [EN] SAWE        - 2:33.0 [v5 NOPRIME]", fore=Fore.RED, style=Style.BRIGHT)
tprint("[· 3] [SV] fakdanmark  - 3:22.3 [v4]", fore=Fore.GREEN, style=Style.BRIGHT)
tprint("[· 4] [EN] Korvkungen  - 4:55.0 [v4]", fore=Fore.RED, style=Style.BRIGHT)
tprint("In the next version, times from ", style=Style.BRIGHT, newline=False)
tprint("v4", fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint(" will be removed.", style=Style.BRIGHT)
print
tprint("Enter to continue...", newline=False)
input()

# Language Selection
clear()
tprint("Choose a language:", fore=Fore.YELLOW)
tprint("1. English", fore=Fore.RED, style=Style.BRIGHT)
tprint("2. Svenska (Swedish)", fore=Fore.BLUE, style=Style.BRIGHT)
tprint("3. 日本語 (Japanese)", fore=Fore.GREEN, style=Style.BRIGHT)
tprint("4. Українська (Ukrainian)", fore=Fore.YELLOW, style=Style.BRIGHT)

lang_choice = get_menu_choice("1234")
lang_code = ["en", "sv", "ja", "uk"][int(lang_choice) - 1]

playername = namepick()

tprint("Ready?     ", delay=0.01, fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint("◉ ", delay=0.01, fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint("◯ ", delay=0.01, fore=Fore.YELLOW, style=Style.BRIGHT, newline=False)
tprint("◯     ", delay=0.01, fore=Fore.GREEN, style=Style.BRIGHT, newline=False)
sleep(1)
tprint("\rSteady... ", delay=0.01, fore=Fore.YELLOW, style=Style.BRIGHT, newline=False)
tprint("◉ ", delay=0.01, fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint("◉ ", delay=0.01, fore=Fore.YELLOW, style=Style.BRIGHT, newline=False)
tprint("◯     ", delay=0.01, fore=Fore.GREEN, style=Style.BRIGHT, newline=False)
sleep(1)
tprint("\rGo!       ", delay=0.01, fore=Fore.GREEN, style=Style.BRIGHT, newline=False)
tprint("◉ ", delay=0.01, fore=Fore.RED, style=Style.BRIGHT, newline=False)
tprint("◉ ", delay=0.01, fore=Fore.YELLOW, style=Style.BRIGHT, newline=False)
tprint("◉     ", delay=0.01, fore=Fore.GREEN, style=Style.BRIGHT)

# Tutorial Fight
timestart = time()

fightloop("Hugo", playername)


# Game Loop for Main Progression
available_bosses = ["Tage Mage", "Oscar", "Omar"]


# --- STEP 2: First Choice (Oscar or Tage Mage) ---
if alive:
    clear()
    tprint(get_text("next_prompt"))

    # Get localized boss names
    oscar_name = BOSSES["Oscar"]["names"].get(lang_code, BOSSES["Oscar"]["names"]["en"])
    tage_name = BOSSES["Tage Mage"]["names"].get(
        lang_code, BOSSES["Tage Mage"]["names"]["en"]
    )

    tprint(f"1. {get_text('fight_option', boss=oscar_name)}", fore=Fore.RED)
    tprint(f"2. {get_text('fight_option', boss=tage_name)}", fore=Fore.CYAN)
    tprint(f"3. {get_text('upgrade_attack')}", fore=Fore.RED)
    tprint(f"4. {get_text('upgrade_shield')}", fore=Fore.BLUE)
    tprint(f"5. {get_text('upgrade_health')}", fore=Fore.LIGHTGREEN_EX)

    first_choice = get_menu_choice("12345")

    # Handle upgrades before fight 1
    if first_choice in ["3", "4", "5"]:
        if first_choice == "3":
            attackmulti *= 1.5
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_attack"),
                    val=int(floor(attackmulti * 100)),
                )
            )
        elif first_choice == "4":
            shieldmulti *= 1.5
            attackonly = False
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_shield"),
                    val=int(floor(shieldmulti * 100)),
                )
            )
        elif first_choice == "5":
            healthmulti *= 1.5
            attackonly = False
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_health"),
                    val=int(floor(healthmulti * 100)),
                )
            )

        clear()
        tprint(get_text("next_prompt"))
        tprint(f"1. {get_text('fight_option', boss=oscar_name)}", fore=Fore.RED)
        tprint(f"2. {get_text('fight_option', boss=tage_name)}", fore=Fore.CYAN)
        first_choice = get_menu_choice("12")

    # Determine Fight 1 & Fight 2 order
    if first_choice == "1":
        first_boss = "Oscar"
        second_boss = "Tage Mage"
    else:
        first_boss = "Tage Mage"
        second_boss = "Oscar"

    # Run Fight 1
    
    
    fightloop(first_boss, playername)
    
    

# --- STEP 3: Second Boss (The one you didn't pick in Fight 1) ---
if alive:
    clear()
    tprint(get_text("next_prompt"))

    other_boss_name = BOSSES[second_boss]["names"].get(
        lang_code, BOSSES[second_boss]["names"]["en"]
    )

    tprint(f"1. {get_text('fight_option', boss=other_boss_name)}", fore=Fore.RED)
    tprint(f"2. {get_text('upgrade_attack')}", fore=Fore.RED)
    tprint(f"3. {get_text('upgrade_shield')}", fore=Fore.BLUE)
    tprint(f"4. {get_text('upgrade_health')}", fore=Fore.LIGHTGREEN_EX)

    second_choice = get_menu_choice("1234")

    # Handle upgrades before fight 2
    if second_choice in ["2", "3", "4"]:
        if second_choice == "2":
            attackmulti *= 1.5
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_attack"),
                    val=int(floor(attackmulti * 100)),
                )
            )
        elif second_choice == "3":
            attackonly = False
            shieldmulti *= 1.5
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_shield"),
                    val=int(floor(shieldmulti * 100)),
                )
            )
        elif second_choice == "4":
            attackonly = False
            healthmulti *= 1.5
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_health"),
                    val=int(floor(healthmulti * 100)),
                )
            )

        sleep(2)
        clear()
        tprint(get_text("next_prompt"))
        tprint(f"1. {get_text('fight_option', boss=other_boss_name)}", fore=Fore.RED)
        second_choice = get_menu_choice("1")

    # Run Fight 2
    fightloop(second_boss, playername)

# --- STEP 4: Boss Fight 3 (Omar) ---
if alive:
    clear()
    
    
    tprint(get_text("next_prompt"))

    omar_name = BOSSES["Omar"]["names"].get(lang_code, BOSSES["Omar"]["names"]["en"])

    tprint(f"1. {get_text('fight_option', boss=omar_name)}", fore=Fore.RED)
    tprint(f"2. {get_text('upgrade_attack')}", fore=Fore.RED)
    tprint(f"3. {get_text('upgrade_shield')}", fore=Fore.BLUE)
    tprint(f"4. {get_text('upgrade_health')}", fore=Fore.LIGHTGREEN_EX)

    omar_choice = get_menu_choice("1234")

    # Handle upgrades before Omar
    if omar_choice in ["2", "3", "4"]:
        if omar_choice == "2":
            attackmulti *= 1.5
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_attack"),
                    val=int(floor(attackmulti * 100)),
                )
            )
        elif omar_choice == "3":
            shieldmulti *= 1.5
            attackonly = False
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_shield"),
                    val=int(floor(shieldmulti * 100)),
                )
            )
        elif omar_choice == "4":
            healthmulti *= 1.5
            attackonly = False
            
            
            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_health"),
                    val=int(floor(healthmulti * 100)),
                )
            )

        sleep(1)

    # Fight against Omar
    if attackonly == True:
        print(get_text("attack_only_omar"))
        sleep(1)
        fightloop("Prime Omar", playername)        
    else:
        fightloop("Omar", playername)


# --- STEP 5: Boss Fight 4 (Zombie Tage) ---
if alive:
    clear()

    tprint(get_text("next_prompt"))

    zomtage_name = BOSSES["Mini Tage Mage"]["names"].get(lang_code, BOSSES["Mini Tage Mage"]["names"]["en"])

    tprint(f"1. {get_text('fight_option', boss="???")}", fore=Fore.RED)
    tprint(f"2. {get_text('upgrade_attack')}", fore=Fore.RED)
    tprint(f"3. {get_text('upgrade_shield')}", fore=Fore.BLUE)
    tprint(f"4. {get_text('upgrade_health')}", fore=Fore.LIGHTGREEN_EX)

    omar_choice = get_menu_choice("1234")

    # Handle upgrades before ZomTage
    if omar_choice in ["2", "3", "4"]:
        if omar_choice == "2":
            attackmulti *= 1.5

            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_attack"),
                    val=int(floor(attackmulti * 100)),
                )
            )
        elif omar_choice == "3":
            shieldmulti *= 1.5
            attackonly = False

            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_shield"),
                    val=int(floor(shieldmulti * 100)),
                )
            )
        elif omar_choice == "4":
            healthmulti *= 1.5
            attackonly = False

            tprint(
                get_text(
                    "upgrade_done",
                    stat=get_text("upgrade_health"),
                    val=int(floor(healthmulti * 100)),
                )
            )

        sleep(1)

    # Fight against Zomtage
    get_text("zombie_tage_intro")
    sleep(1)
    fightloop("Mini Tage Mage", playername)

if alive:
    timefinish = time()
    timespeedrun = timefinish - timestart
    speedminutes = int(timespeedrun // 60)
    speedseconds = float(str(timespeedrun)[:4]) % 60
    tprint(get_text("speedrun_done"), fore=Fore.YELLOW, style=Style.BRIGHT)
    tprint(get_text("speedrun_time"))
    tprint(f"{speedminutes}:{speedseconds}")
    tprint(get_text("speedrun_send"))
    tprint(get_text("speedrun_fake"))
    verificationstring = f"START.VERIF.999.666.333.000.MIN.{speedminutes}.SEC.{speedseconds}.ATKONLY.{attackonly}.START.{round(timestart,2)}.END.{round(timefinish,2)}.NAME.{playername}.DONE"
    verifstring_bytes = verificationstring.encode("ascii")
    base64_bytes = base64.b64encode(verifstring_bytes)
    base64_string = base64_bytes.decode("ascii")
    print(get_text("speedrun_code"), base64_string)
