import phylib;
import os;
import sqlite3;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS=phylib.PHYLIB_MAX_OBJECTS;
FRAME_RATE = 0.01;


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n"""



# add more here



################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n"""%(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, 
                                                                            BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])


class RollingBall (phylib.phylib_object):


    def __init__( self, number, pos, vel, acc ):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0);

        self.__class__ = RollingBall

    #add svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n"""%(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, 
                                                                        BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

class Hole (phylib.phylib_object):


    def __init__(self, pos):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE,  
                                       0,
                                       pos,None,None, 
                                       0.0, 0.0);

        self.__class__ = Hole

    #add svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n"""%(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)


class HCushion (phylib.phylib_object):


    def __init__(self, y):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION,  
                                       0,
                                       None,None,None, 
                                       0.0, y)

        self.__class__ = HCushion

    #add svg method here
    def svg(self):
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n"""%(-25 if self.obj.hcushion.y == 0 else 2700)


class VCushion (phylib.phylib_object):


    def __init__(self, x):

        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_VCUSHION,  
                                       0,
                                       None,None,None, 
                                       x, 0.0);

        self.__class__ = VCushion;

        #add svg method here
    def svg(self):
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n"""%(-25 if self.obj.vcushion.x == 0 else 1350)




################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        tString = HEADER

        for obj in self:
            if obj is not None:
                tString += obj.svg()

        tString += FOOTER
        return tString


    def roll( self, t ):
                new = Table();
                for ball in self:
                    if isinstance( ball, RollingBall ):
                        # create4 a new ball with the same number as the old ball
                        new_ball = RollingBall( ball.obj.rolling_ball.number,
                                                Coordinate(0,0),
                                                Coordinate(0,0),
                                                Coordinate(0,0) );
                        # compute where it rolls to
                        phylib.phylib_roll( new_ball, ball, t );

                        # add ball to table
                        new += new_ball;

                    if isinstance( ball, StillBall ):
                        # create a new ball with the same number and pos as the old ball
                        new_ball = StillBall( ball.obj.still_ball.number,
                                                Coordinate( ball.obj.still_ball.pos.x,
                                                            ball.obj.still_ball.pos.y ) );
                        # add ball to table
                        new += new_ball;

                    # return table
                    return new;



class Database( phylib.phylib_table ):

    def __init__( self, reset=False ):

        file_db = 'phylib.db'

        if reset and os.path.exists("phylib.db"):
            os.remove("phylib.db")


        self.connection = sqlite3.connect(file_db)
        self.createDB()
        self.cur = self.connection.cursor()


    def createDB(self):

        #connection = sqlite3.connect('file_db')
        cur = self.connection.cursor()

        cur.execute("""
            SELECT name FROM sqlite_master WHERE type='table';
        """)
        existing_tables = [table[0] for table in cur.fetchall()]

        if "Ball" not in existing_tables:
            cur.execute("""
                CREATE TABLE Ball (
                    BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    BALLNO INTEGER,
                    XPOS FLOAT,
                    YPOS FLOAT,
                    XVEL FLOAT,
                    YVEL FLOAT,
                    FOREIGN KEY (BALLID) REFERENCES BallTable(BALLID)
                );
            """)

        if "TTable" not in existing_tables:
            cur.execute("""
                CREATE TABLE TTable (
                    TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    TIME FLOAT
                    );
            """)

        if "BallTable" not in existing_tables:
            cur.execute("""
                CREATE TABLE BallTable (
                    BALLID INTEGER,
                    TABLEID INTEGER,
                    PRIMARY KEY (BALLID, TABLEID),
                    FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                    FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
                );
            """)

        if "Shot" not in existing_tables:  
            cur.execute("""
                CREATE TABLE Shot (
                    SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    PLAYERID INTEGER,
                    gameID INTEGER,
                    FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                    FOREIGN KEY (gameID) REFERENCES Game(gameID)
                );
            """)

        if "TableShot" not in existing_tables:
            cur.execute("""
                CREATE TABLE TableShot (
                    TABLEID INTEGER,
                    SHOTID INTEGER,
                    PRIMARY KEY (TABLEID, SHOTID),
                    FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                    FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
                );
            """)


        if "Game" not in existing_tables:
            cur.execute("""
                CREATE TABLE Game (
                    gameID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    gameName VARCHAR(64)
                );
            """)


        if "Player" not in existing_tables:
            cur.execute("""
                CREATE TABLE Player (
                    PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    gameID INTEGER,
                    PLAYERNAME VARCHAR(64),
                    FOREIGN KEY (gameID) REFERENCES Game(gameID)
                );
            """)

            cur.close()
            self.connection.commit()
            



######HELPER FUNCTIONS##################################

    #getGame
    def getGame(self, gameID):
        cursor = self.connection.cursor()

        cursor.execute('''
                       SELECT GAME.GAMEID, GAME.GAMENAME,PLAYER1.PLAYERNAME AS PLAYER1NAME,PLAYER2.PLAYERNAME AS PLAYER2NAME
                       FROM GAME
                       JOIN PLAYER PLAYER1 ON GAME.GAMEID = PLAYER1.GAMEID
                       JOIN PLAYER PLAYER 2 ON GAME.GAMEID = PLAYER2.GAMEID
                       WHERE GAME.GAMEID == (%d);
        '''%(gameID))

        return cursor.fetchall()

    #setGame
    def setGame( self, gameName, player1Name, player2Name ):
        self.cur = self.connection.cursor()
        self.cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        gameID = self.cur.lastrowid
        self.cur.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player1Name, gameID))
        self.cur.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (player2Name, gameID))

        self.connection.commit()
        self.cur.close()
        return gameID

    #playerid
    def getPlayerID( self, playerCalled, gameID):
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = (?) AND GAMEID = (?)", (playerCalled, gameID))
        playerID = self.cursor.fetchone()
        if playerID is not None:
            self.connection.commit()
            self.cur.close()
            return playerID[0]

        else:
            return None



    def new_shot(self, gameName, playerName):
        self.cur.execute("""
            SELECT gameID FROM Game WHERE gameName = ?;
        """, (gameName,))
        gameID = self.cur.fetchone()[0]

        self.cur.execute("""
            SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND gameID = ?;
        """, (playerName, gameID))
        playerID = self.cur.fetchone()[0]

        self.cur.execute("""
            INSERT INTO Shot (PLAYERID, gameID) VALUES (?, ?);
        """, (playerID, gameID))
        return self.cur.lastrowid


    def record_table_shot(self, shotID, tableID):
        self.cur.execute("""
            INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?);
        """, (tableID, shotID))

    def close(self):
        self.connection.commit()
        self.connection.close()


###########################################################

    def readTable( self, tableID ):
        self.cur = self.connection.cursor()
        table = Table()

        self.cur.execute('''SELECT  * FROM BallTable WHERE TABLEID = ?''', (tableID + 1,))
        final_result = self.cur.fetchone()

        if final_result is None:
            return None

        #Get Time for table using fetchone
        self.cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,))
        calcTime = self.cur.fetchone()
        table.time = int(calcTime[0])
             
        
        self.cur.execute("SELECT * FROM Ball INNER JOIN BallTable ON (Ball.BALLID = BallTable.BALLID) WHERE BallTable.TABLEID = ?", (tableID + 1,))
        pool_balls = self.cur.fetchall()

        #For loop to assign data to a ball object
        for ball_info in pool_balls:
            ballID = ball_info[0]
            ballNum = ball_info[1]
            ballPos = Coordinate(float(ball_info[2]), float(ball_info[3]))
        
            if ball_info[4] == 0.0 and ball_info[5] == 0.0:
                ball = StillBall(ballNum, ballPos)
            else:
                ballVel = Coordinate(float(ball_info[4]), float(ball_info[5]))
                speed = phylib.phylib_length(ballVel)
                
                # Check if speed is zero to avoid division by zero
                if speed != 0:
                    acc = Coordinate((-ballVel.x / speed) * DRAG, (-ballVel.y / speed) * DRAG)
                else:
                    acc = Coordinate(0, 0)  # Set acceleration to zero if speed is zero
                ball = RollingBall(ballNum, ballPos, ballVel, acc)
            table += ball

        self.connection.commit()
        self.cur.close()

        return table


#######################################################################

    def writeTable(self, table):

        cur = self.connection.cursor()
        bID = []
        pink = 10
        
        # Iterate over balls in the table and insert them into Ball and BallTable tables
        while pink < MAX_OBJECTS:
            ball = table[pink]
            
            if ball is None:
                break

            elif isinstance(ball, RollingBall):
                cur.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?);
                """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))

                #print ("Test0")
            elif isinstance(ball, StillBall):
                cur.execute("""
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, 0.0, 0.0);
                """, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))

                #print("Test 1")

            
            # Get the last inserted ball ID
            cur.execute("""
                SELECT last_insert_rowid();
            """)
            row = cur.fetchone()
            #print("test 1")
            if row:
                bID.append(row[0])  # Fetch the last inserted ball ID
            cur.fetchall()

            pink += 1

       
        # Insert table time into TTable
        cur.execute("""
            INSERT INTO TTable (TIME) VALUES (?);
        """, 
        (table.time,))
        
        # Get the last inserted table ID
        tableID = cur.lastrowid #Another way for tableid 

    
        # Insert into BallTable
        for ball_id in bID:
            cur.execute("""
                INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?);
            """, (ball_id, tableID))
        
        # Commit changes to the database
        self.connection.commit()

        cur.close()
        return tableID - 1


##############################################################
class Game:

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        if gameID is not None and (gameName is None or player1Name is None or player2Name is None):
            db = Database(False)
            gameID += 1
            db.getGame(gameID)
            db.close()

        elif gameID is None and all(isinstance(arg, str) for arg in [gameName, player1Name, player2Name]):
            db = Database(True)
            gameID = db.setGame(gameName, player1Name, player2Name)
            db.close()

        else:
            raise TypeError("Invalid")




    def shoot(self, gameName, playerName, table, xvel, yvel):
        db = Database(False)
        shot_id = db.new_shot(gameName, playerName)

        cue_ball_index = self.find_cue_ball(table)
        #table[cue_ball_index] = self.prepare_cue_ball(table[cue_ball_index], xvel, yvel)
        xpos = table[cue_ball_index].obj.still_ball.pos.x
        ypos = table[cue_ball_index].obj.still_ball.pos.y

        table[cue_ball_index].type = phylib.PHYLIB_ROLLING_BALL
        table[cue_ball_index].__class__ = RollingBall

        table[cue_ball_index].obj.rolling_ball.number = 0
        table[cue_ball_index].obj.rolling_ball.pos.x = xpos
        table[cue_ball_index].obj.rolling_ball.pos.y = ypos

        vel = Coordinate(xvel, yvel)
        speed = phylib.phylib_length(vel)

        table[cue_ball_index].obj.rolling_ball.vel.x = xvel
        table[cue_ball_index].obj.rolling_ball.vel.y = yvel

        print(speed)

        if speed != 0:
            table[cue_ball_index].obj.rolling_ball.acc.x = -xvel / speed * DRAG
            table[cue_ball_index].obj.rolling_ball.acc.y = -yvel / speed * DRAG
        else:
            table[cue_ball_index].obj.rolling_ball.acc.x = 0
            table[cue_ball_index].obj.rolling_ball.acc.y = 0

        while table:
            try:
                b_time = table.time
                o_table = table
                table = table.segment()
                time_diff = int((table.time - b_time) / FRAME_RATE)
                for i in range(time_diff):
                    roll_time = i * FRAME_RATE
                    new_table = o_table.roll(roll_time)
                    new_table.time = b_time + roll_time
                    table_id = db.writeTable(new_table)
                    db.record_table_shot(shot_id, table_id)
            except:
                break
        
        db.close()


        

    #CUE BALL

    def find_cue_ball(self, table):
        for i in range(10, MAX_OBJECTS):
            if isinstance(table[i], StillBall) and table[i].obj.still_ball.number == 0:
                return i

    def prepare_cue_ball(self, cue_ball, xvel, yvel):
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.__class__ = RollingBall

        cue_ball.obj.rolling_ball.number = 0
        speed = phylib.phylib_length(cue_ball.obj.rolling_ball.vel)

        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        if speed != 0:
            cue_ball.obj.rolling_ball.acc.x = -xvel / speed * DRAG
            cue_ball.obj.rolling_ball.acc.y = -yvel / speed * DRAG
        else:
            cue_ball.obj.rolling_ball.acc.x = 0
            cue_ball.obj.rolling_ball.acc.y = 0

        return cue_ball


    '''''
    def record_shot(self, db, shot_id, new_table):
        #for table_id, new_table in enumerate(new_table):
        table_id = db.writeTable(new_table)
        db.record_table_shot(shot_id, table_id)
    '''

    def cueBall(self, table):
        for i in range(10, MAX_OBJECTS):
            if isinstance(table[i], StillBall) and table[i].obj.still_ball.number == 0:
                return table[i]
