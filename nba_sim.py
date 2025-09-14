# Needed for all selection in generate_shot().
import random


    
# Helper functions for generate_shot().
def return_random_player():
    return random.choice(['pg', 'sg', 'sf', 'pf', 'c'])

def return_rebound_player():
    return random.choice(['pg', 
                          'sg',  
                          'sf', 'sf',  
                          'pf', 'pf', 
                          'c', 'c', 'c'])

def return_assist_player():
    return random.choice(['pg', 'pg', 'pg', 
                          'sg', 'sg', 
                          'sf', 'sf',  
                          'pf', 'pf', 
                          'c'])
    
def look_up_player(input, cavs, warriors):
    for position, p in cavs.players.items():
        if p.name == input:
            return "C", position
    for position, p in warriors.players.items():
        if p.name == input:
            return "W", position
    return 'fail', 'fail'
        


class Player:
    
    # All stas are initialized.
    # All attributes are public because this is not an extremely complex project
    # and it is not unsafe to do so.
    def __init__(self, name, fg, three_pt_fg, three_pt_shot_rate, p=0, 
                 r=0, a=0, s=0, b=0, to=0, shots_taken=0, shots_made=0, threes_taken=0, threes_made=0, 
                 free_throws_taken=0, free_throws_made=0
                 ):
        
        self.name = name
        self.fg = fg
        self.three_pt_fg = three_pt_fg
        self.three_pt_shot_rate = three_pt_shot_rate
        self.p = p
        self.r = r
        self.a = a
        self.s = s
        self.b = b
        self.to = to
        self.shots_taken = shots_taken
        self.shots_made = shots_made
        self.threes_taken = threes_taken
        self.threes_made = threes_made
        self.free_throws_taken = free_throws_taken
        self.free_throws_made = free_throws_made
      
    # The properties below have to be defined so that if a player's stats are checked
    # before the first quarter, there won't be a divide by 0 error.
    
    @property  # This allows the property to be called with .fg_pct instead of 
               # .fg_pct(), which allows for string formatting with :.2f.
    def fg_pct(self):
        return ((self.shots_made / self.shots_taken) * 100 if self.shots_taken > 0 else 0)
    
    @property  # This allows the property to be called with .three_pt_pct instead of
               # .three_pt_pct(), which allows for string formatting with :.2f.
    def three_pt_pct(self):
        return ((self.threes_made / self.threes_taken) * 100 if self.threes_taken > 0 else 0)
        
    # Defined so that a player can be printed when stats are requested.
    def __str__(self):
        main_stats= (f'{self.name}:\n  {self.p} Points\n'
                     f'  {self.r} Rebounds\n  {self.a} Assists\n'
                     f'  {self.s} Steals\n  {self.b} Blocks\n'
                     f'  {self.to} Turnovers\n'
        )
        
        shooting_stats = (f'  {self.shots_made}/{self.shots_taken} from field ({self.fg_pct:.0f}%)'
                         f'\n  {self.threes_made}/{self.threes_taken} from 3 ({self.three_pt_pct:.0f}%)'
                         f'\n  {self.free_throws_made}/{self.free_throws_taken} on free throws'
        )
        return main_stats + shooting_stats
    
        
        
class Team:
    
    # Shot splits are explained later on line 299, but they are the basis of how players are picked to take the shot for their team.
    def __init__(self, name, players, shot_splits, score = 0):
        self.name = name
        self.players = players
        self.shot_splits = shot_splits
        self.score = score
        
    def __str__(self):
        return_str = (f'\n{self.name}:\n'  
                      f"PG = {self.players['pg'].name}\n"
                      f"SG = {self.players['sg'].name}\n"
                      f"SF = {self.players['sf'].name}\n"
                      f"PF = {self.players['pf'].name}\n"
                      f"C = {self.players['c'].name}\n"
        )
        return return_str
    
    
    
    def generate_shot(self, other, output = False): # By default does not generate output
        
        # This is the core of the project and the function that took by FAR the most time.
        # I had to research the rules, iron out countless glitches, and design a system
        # from scratch that fairly and accurrately simulates a singular basketball possession.
        
        # The code is far from perfect. Blocks and steals occur often in unrealistic situations,
        # centers get a few too many rebounds, and a few more small inaccuracies. I intend to fix
        # these issues one day, but overall I am happy with how the code functions. If you are not a 
        # basketball enthusiest, you will likely not notice any issues with the function.
        
        output_str = ""
        
        # The code loops until a shot is made or the ball is recovered by the other team
        while True:  
            repeat = False 
            is_blocked = False
            
            # If the ball is stolen, possession ends.
            steal_number = random.randint(0,24)
            if steal_number < 2:
                steal_player = return_random_player()
                stolen_player = return_random_player()
                output_str += '\t' + other.players[steal_player].name + " steals the ball from " + self.players[stolen_player].name + '\n'
                other.players[steal_player].s += 1
                self.players[stolen_player].to += 1
                if output:
                    print(output_str)
                return
            
            # Deciding player and type of shot. How this works is explained on line 299.
            player_num = random.random()
            if player_num > self.shot_splits[1]:
                selected_player = 'pg'
            elif player_num > self.shot_splits[2]:
                selected_player = 'sg'
            elif player_num > self.shot_splits[3]:
                selected_player = 'sf'
            elif player_num > self.shot_splits[4]:
                selected_player = 'pf'
            else:
                selected_player = 'c'
            output_str += '\t' + self.players[selected_player].name + " shoots a "
            
            # Determine if the shot is a 3 or 2 pointer.
            shot_num = random.random()
            is_three = False
            if shot_num < self.players[selected_player].three_pt_shot_rate:
                is_three = True
                output_str += "3 "
                self.players[selected_player].threes_taken += 1
            else:
                output_str += "2 "
            self.players[selected_player].shots_taken += 1
            
            # Deciding if shot is made / missed / blocked.     
            score_num = random.random()
            made_shot = False
            
            # If shot is made:
            if (score_num * 100) < self.players[selected_player].fg:
                made_shot = True
    
                if is_three:
                    self.score += 3
                    self.players[selected_player].p += 3
                    self.players[selected_player].threes_made += 1
                else:
                    self.score += 2
                    self.players[selected_player].p += 2
                self.players[selected_player].shots_made += 1
                
                output_str += "\n\tand makes it! "
                
            # If shot is missed: 
            else:
                made_shot = False
                block_num = random.randint(0,15)
                if block_num == 0:
                    is_blocked = True
                    block_player = return_random_player()
                    other.players[block_player].b += 1
                    output_str += "\n\tbut it's blocked by " + other.players[block_player].name
                else:
                    output_str += "\n\tbut misses it. "

            # If the shot is made, determine if a player assisted, and which player:
            assist_num = 0
            if made_shot:
                assist_player = return_assist_player()
                while assist_player == selected_player:
                    assist_player = return_assist_player()
                assist_num = random.randint(0,1)
                if assist_num == 1:
                    self.players[assist_player].a += 1
                    output_str += "\n\t" + self.players[assist_player].name + " assisted on the bucket"
                    
            # If the shot is missed, determine if a player gets free throws, if the ball goes out of bounds, 
            # or who gets the rebound
            else: # Fouled
                foul_chance = 0
                if is_three:
                    foul_chance = 2
                else:
                    foul_chance = 14
                foul_num = random.random() * 100

                if foul_chance > foul_num and not is_blocked:
                    output_str += '\n\tBut he was fouled'
                    ftm = random.choice([0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2])
                    if is_three:
                        ftm += 1
                        self.players[selected_player].free_throws_taken += 1
                    self.players[selected_player].p += ftm
                    self.players[selected_player].free_throws_taken += 2
                    self.players[selected_player].free_throws_made += ftm
                    self.score += ftm
                    output_str += '\n\tand made ' + str(ftm) + ' free throws!'  
                      
                else: #Rebounded / Out of Bounds
                    OB_num = random.randint(0,7)
                    if OB_num == 0:
                        output_str += "\n\tThe ball goes out of bounds- "  
                        repeat_num = random.random()
                        if repeat_num < 0.6:
                            output_str += 'offense retains possession!'
                            repeat = True
                        else:
                            output_str += 'defense gains possession!'
                    else:         
                        rebound_player = return_rebound_player()
                        team_rebound_num = random.randint(0,2)
                        
                        if team_rebound_num == 0:
                            if not is_blocked:
                                self.players[rebound_player].r += 1
                            output_str += "\n\t" + self.players[rebound_player].name + " "
                            output_str += ("recovers the ball!" if is_blocked else "gets the rebound!")
                            repeat = True

                        else:
                            if not is_blocked:
                                other.players[rebound_player].r += 1
                            output_str += "\n\t" + other.players[rebound_player].name + " "
                            output_str += ("recovers the ball!" if is_blocked else "gets the rebound!")
            
            # If the play is not repeated and text is to be outputted, do so.            
            if output and not repeat:   
                print(output_str + '\n')
                return
            
            # If the play is to be repeated, do so.
            elif repeat:
                output_str += '\n'
                
            # If no output or repition is needed, end the play.
            else:
                return
        
    
    
                        
# Here, player and team stats are initialized.                       
def initialize_teams():
    # Order of stats: name, fg, three_pt_fg, three_pt_rate, p, r, a, s, b, to, shots_taken, shots_made, threes_taken, threes_made.
    # Most of these stats do not require input, as they are automatically set to 0.
    
    # Players are assigned to either thier first or last name depending on which is more recognizable.
    # I am aware this is a bad system for a group project, but as a basketball nerd, it's the easiest system for me.
    
    
    # The first 2 numbers are FG% and 3pt%, and the third number is what percent of a player's shots are three pointers.
    # This helps simulate accurate shooting.
    
    # Cavs
    kyrie = Player("Kyrie Irving", 45, 38, 0.295)
    jr = Player("JR Smith", 42, 40, 0.6)
    lebron = Player("Lebron James", 56, 33, 0.120) # Players don't need their P/R/A, etc assigned because
    love = Player("Kevin Love", 42, 36, 0.449)     # the initializier initializes them to 0.
    thompson = Player("Tristan Thompson", 59, 0, 0)
    
    # Warriors
    steph = Player("Steph Curry", 50, 45, 0.554)
    klay = Player("Klay Thompson", 47, 43, 0.468)
    barnes = Player("Harrison Barnes", 47, 38, 0.330)
    draymond = Player("Draymond Green", 49, 39, 0.317)
    bogut = Player("Andrew Bogut", 63, 12, 0)
    
    # I chose to use a dictionary instead of a list largely because I wanted more practice with dictionaries.
    # A list with accessing with (team).(players_list)[x] would have worked well, but lists are extremely simple
    # and won't help me improve as a programmer.
    c_dict = {'pg': kyrie, 'sg': jr, 'sf': lebron, 'pf': love, 'c': thompson}
    w_dict = {'pg': steph, 'sg': klay, 'sf': barnes, 'pf': draymond, 'c': bogut}
    
    # These numbers are the player shooting rates. I calculated them through doing research and finding the frequency of how often the first
    # player in the players' dictinary shot the ball for their team, then subtracting that frequency from 1. Then, I found
    # the second player's frequency, and subtracted it from the first number. I repeated this until the number reached 0.
    
    # I'll give an example for the Warriors shooting splits. First, a number between 0 and 1 is generated.
    # Anything between 1 and 0.67 means the first player in the dctionary shoots the ball.
    # Anything between 0.67 and 0.387 means the second player shoots. And so on...
    w_shot_splits = [1, 0.67, 0.387, 0.23, 0.065]
    c_shot_splits = [1, 0.771, 0.58, 0.252, 0.080]
    
    c = Team('Cleveland Cavaliers', c_dict, c_shot_splits)
    w = Team('Golden State Warriors', w_dict, w_shot_splits)
    
    return c, w   


# This function simulates one quarter.
def sim_quarter(q, c, w):
    print(f"\tQUARTER {q}\n")
    
    print("You have 3 options! You can:")
    while True:
        print("1. Automatically simulate the quarter, or")
        print("2. Simulate the quarter slowly, or")
        print("3. Show a player's stats\n")
        print("Please select a number:\n")

        selection = input().strip()

        if selection == "3":
            print("\nPlease enter a player's name:\n")
            player_selection = input().strip()

            team_key, pos = look_up_player(player_selection, c, w)
            while team_key == "fail":
                print("\nPlayer not found. Please enter their first and last name\n")
                player_selection = input().strip()
                team_key, pos = look_up_player(player_selection, c, w)

            print('')
            if team_key == "C":
                print(c.players[pos])
            else:
                print(w.players[pos])
            print('')

        elif selection == "1":
            for _ in range(20):
                c.generate_shot(w)
                w.generate_shot(c)
            break

        elif selection == "2":
            for _ in range(20):
                c.generate_shot(w, True)
                w.generate_shot(c, True)
            break

        else:
            print("\nPlease enter a valid number.\n")

    print(f'\nQuarter {q} is complete! The score is:\n'
          f'Cavs: {c.score}, Warriors: {w.score}\n')


                
                
# Winner is chosen from the teams' scores   
def determine_winner(t1, t2):
    if t1.score > t2.score:
        print(f'{t1.name} won the game!')
    elif t1.score < t2.score:
        return print(f'{t2.name} won the game!')
    else:
        print("Score is tied! Overtime feature not implemented yet")
        

# This screen is displayed initially when the code is run.        
def start_screen():
    print("Welcome to the 2016 NBA Finals Simulator!\n"
          "\tThis project simulates the iconic game 7 between the Cavs and the Warriors\n"
          "\tThe project is meant to simulate the logic of basketball and how the sport works,\n"
          "\twhich is why no unique user interface is created.\n"
          "\tIf you automatically simulate a quarter, the score updates automatically.\n"
          "\tIf you simulate the quarter slowly, a playlog will generate to show you everything\n"
          "\tthat happened in the quarter. This option is here to show the logic of the basketball game\n"
          "\tworks as intended\n"
          "\tThe third option is to see a player's stats. You will need to know the players name to look them up,\n"
          "\tand the name must be typed correctly, otherwise you will be prompted to enter their name again.\n"
          "\tI hope you enjoy!\n")
    

    
            
        
        
    
         
    
    
    
# main is very simple and consists only of prints, function calls, and iteration of quarter.
def main():
    print('\n\n\n')
    cavs, warriors = initialize_teams()
    
    
    start_screen()
    
    # Yes, this could be a for loop. In my opinion, this is more readable and 
    # easier to understand what is going on.
    quarter = 1
    sim_quarter(quarter, cavs, warriors)
    quarter = 2
    sim_quarter(quarter, cavs, warriors)
    quarter = 3
    sim_quarter(quarter, cavs, warriors)
    quarter = 4
    sim_quarter(quarter, cavs, warriors)
    
    determine_winner(cavs, warriors)
    print('\n\n\n\n\n')
    
    
    
# I hope you enjoy my program! This is the first somewhat time consuming project I have ever created,
# and I enjoyed learning and improving as a coder as I created it. Thank you for reading!
main()
