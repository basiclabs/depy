import sqlite3

class VisualNovel(object):
    def __init__(self, gamedata=None):
        try:
            conn = sqlite3.connect(gamedata)
            self.c = conn.cursor()

            self.c.execute("select * from games")
            row = self.c.fetchone()
        except:
            print 'could not open database', gamedata
        else:
            if row:
                self.name = row[1]
                self.current_scene = row[2]

    def get_scene(self, scene_ref):
        return Scene(scene_ref, self.c)
        
    def get_dialogue(self, dialogue_ref):
        return Dialogue(dialogue_ref, self.c)

class Scene(object):
    def __init__(self, scene_ref=None, c=None):
        self.c = c
        args = (scene_ref,)
        self.c.execute("select * from Scenes where id=?", args)
        row = self.c.fetchone()

        self.setup_text = row[1]
        self.location = Location(row[2], self.c)
        self.initial_dialogue = row[3]

        self.c.execute("select * from Actors_Scenes where sceneId=?", args)
        rows = self.c.fetchall()

        self.actors = []
        for row in rows:
            self.actors.append(Actor(row[2], self.c))

class Location(object):
    def __init__(self, location_ref=None, c=None):
        self.c = c
        args = (location_ref,)
        self.c.execute("select * from Locations where id=?", args)
        row = self.c.fetchone()

        self.name = row[1]
        self.img_path = row[2]

class Dialogue(object):
    def __init__(self, dialogue_ref=None, c=None):
        self.c = c
        args = (dialgue_ref,)
        self.c.execute("select * from Dialgoue where id=?", args)
        row = self.c.fetchone()

        self.actor = row[1]
        self.text = row[2]

        self.c.execute("select * from Options where dialogueId=?", args)
        rows = self.c.fetchall()

        self.options = []
        for row in rows:
           self.options.append(Option(row[3], row[2], row[4], row[5])) 

class Option(object):
    def __init__(self, text=None, display_text=None, outcome_type=None, outcome_ref=None):
        self.text = text
        self.display_text = display_text
        self.outcome_type = outcome_type
        self.outcome_ref = outcome_ref

class Actor(object):
    def __init__(self, actor_ref=None, c=None):
        self.c = c
        args = (actor_ref,)
        self.c.execute("select * from actors where id=?", args)
        row = self.c.fetchone()

        self.name = row[1]

class Outcome:
    DIALOGUE = 0
    SCENE = 1
    FIGHT = 2
    GAMEEND = 3
