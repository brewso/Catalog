from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="E Brousseau", email="ebrousseau@gmail.com",
             picture='https://www.ienglishstatus.com/wp-content/uploads/'
                     '2018/04/Anonymous-Whatsapp-profile-picture.jpg')
session.add(User1)
session.commit()

# category for sports
category1 = Category(user_id=1, name="Sports")

session.add(category1)
session.commit()

CategoryItem9 = CategoryItem(user_id=1, name="Soccer",
                             description="""Association football, more
                             commonly known as football or soccer, is a
                             team sport played between two teams of eleven
                             players with a spherical ball.""",
                             category=category1)

session.add(CategoryItem9)
session.commit()


CategoryItem1 = CategoryItem(user_id=1, name="Football",
                             description="""American football, referred to
                             as football in the United States and Canada
                             and also known as gridiron, is a team sport
                             played by two teams of eleven players on a
                             rectangular field with goalposts at each end.""",
                             category=category1)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Rugby",
                             description="""Rugby union, commonly known in
                             most of the world as rugby, is a contact team
                             sport which originated in England in the first
                             half of the 19th century. One of the two codes
                             of rugby football, it is based on running with
                             the ball in hand.""",
                             category=category1)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="Basketball",
                             description="""Basketball is a team sport in
                             which ten players, five on a side, opposing
                             one another on a rectangular court, have in
                             play the primary objective to shoot a basketball
                             through the defender's hoop""",
                             category=category1)

session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(user_id=1, name="Baseball",
                             description="""Baseball is a bat-and-ball game
                             played between two opposing teams who take turns
                             batting and fielding.""",
                             category=category1)

session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(user_id=1, name="Volleyball",
                             description="""Volleyball is a team sport in
                             which two teams of six players are separated by
                             a net. Each team tries to score points by
                             grounding a ball on the other team's court under
                             organized rules.""",
                             category=category1)

session.add(CategoryItem5)
session.commit()

CategoryItem6 = CategoryItem(user_id=1, name="Tennis",
                             description="""Tennis is a racket sport that can
                             be played individually against a single opponent
                             (singles) or between two teams of two players each
                             (doubles). Each player uses a tennis racket that
                             is strung with cord to strike a hollow rubber ball
                             covered with felt over or around a net and into
                             the opponent's court.""",
                             category=category1)

session.add(CategoryItem6)
session.commit()

CategoryItem7 = CategoryItem(user_id=1, name="Cricket",
                             description="""Cricket is a sport which is played
                             between two teams of eleven players each who score
                             runs (points) by running between two sets of three
                             small, wooden posts called wickets. Each of the
                             wickets is at one end of a rectangle of flattened
                             grass called the pitch.""",
                             category=category1)

session.add(CategoryItem7)
session.commit()

CategoryItem8 = CategoryItem(user_id=1, name="Golf",
                             description="""Golf is a club-and-ball sport in
                             which players use various clubs to hit balls into
                             a series of holes on a course in as few strokes
                             as possible.""",
                             category=category1)

session.add(CategoryItem8)
session.commit()


# category for Super Stir Fry
category2 = Category(user_id=1, name="Video Games")

session.add(category2)
session.commit()


CategoryItem1 = CategoryItem(user_id=1, name="GTA V",
                             description="""Grand Theft Auto V is an
                             action-adventure video game developed by Rockstar
                             North and published by Rockstar Games.""",
                             category=category2)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1, name="Minecraft",
                             description="""Minecraft is a sandbox video game
                             created by Swedish game developer Markus Persson
                             and later developed by Mojang.""",
                             category=category2)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="Skyrim",
                             description="""The Elder Scrolls V: Skyrim is an
                             action role-playing video game developed by
                             Bethesda Game Studios and published by Bethesda
                             Softworks.""",
                             category=category2)

session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(
    user_id=1,
    name="The Legend of Zelda: Breath of the wild",
    description="""The Legend of Zelda: Breath of the
                    Wild is an action-adventure game developed and
                    published by Nintendo. An entry in the longrunning
                    The Legend of Zelda series, it was released for the
                    Nintendo Switch and Wii U consoles on
                    March 3, 2017.""",
    category=category2)

session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(
    user_id=1,
    name="Fortnite",
    description="""Fortnite is a 2017 online game
                             developed by Epic Games, released as different
                             software packages having different game modes that
                             otherwise share the same general gameplay
                             and game engine.""",
    category=category2)

session.add(CategoryItem5)
session.commit()

CategoryItem6 = CategoryItem(
    user_id=1, name="World of Warcraft",
    description="""World of Warcraft is a massively
                             multiplayer online role-playing game released in
                             2004 by Blizzard Entertainment. It is the fourth
                             released game set in the Warcraft fantasy
                             universe.""",
    category=category2)

session.add(CategoryItem6)
session.commit()


# category for Thyme for that
category1 = Category(user_id=1, name="Books")

session.add(category1)
session.commit()


CategoryItem1 = CategoryItem(user_id=1,
                             name="HOW TO BE FAMOUS BY CAITLIN MORAN",
                             description="""Johanna Morrigan (aka Dolly Wilde)
                             has it all: she is nineteen, lives in her own flat
                             in London, and writes for the coolest music
                             magazine in Britain. Her star is rising, just not
                             quickly enough for her liking.""",
                             category=category1)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(user_id=1,
                             name="A TERRIBLE COUNTRY BY KEITH GESSEN",
                             description="""What is everyday life like under
                             Putin's rule? Russian-born Gessen, founding editor
                             of n+1 magazine, draws on his first-hand
                             experiences to paint a vivid picture of Moscow
                             circa 2008. His big-hearted second novel
                             chronicles the adventures and mishaps of young
                             Russian-American academic Andrei, who leaves his
                             life in New York on the eve of the financial
                             crisis to care for his Russian grandmother, who
                             still lives in the apartment Stalin gave her. In
                             Moscow, he falls for a young activist, gets
                             entwined with a group of leftists, and is forced
                             to confront what it is to be shaped by two
                             radically different societies.""",
                             category=category1)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(user_id=1, name="SEXOGRAPHIES BY GABRIELA WIENER",
                             description="""In the first essay by Peruvian
                             journalist Gabriela Wiener, she recalls being
                             invited to spend two nights at an unspecified
                             location in Lima with polygamist guru of sex,
                             Ricardo Badani, and his six wives. Her aim? To
                             explore what she calls his 'recycled but
                             revolutionary formula for happiness.' Besides
                             being a controversial and somewhat reviled figure
                             in Lima, he and his wives run a successful
                             lingerie store, where the clothing tags read:
                             'Badani, instruments of seduction.' Wiener is
                             instructed to bring white marshmallows for
                             toasting, and upon arrival has her 'honesty aura'
                             read by one of Badani's wives. Thus begins this
                             collection of essays that open on the outskirts of
                             Lima, jumps to a swinger's party in Barcelona, and
                             next a squirt expert's apartment. This book can
                             feel psychologically hazardous to read; it pushes
                             you to answer the questions Wiener asks herself:
                             Would I? Could I? Will I?""",
                             category=category1)
session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(
    user_id=1,
    name="BROTHER BY DAVID CHARIANDY",
    description="""The Canadian brothers in Chariandys
    coming-of-age novel grow up poor in a Toronto
    neighborhood in the '90s. Born to a Trinidadian
    mother and absent 'Indian' father, they navigate
    the world as a protective duo whose camaraderie and
    love buffers them, somewhat, from the hostility of
    police officers and racism they face on a daily
    basis. But when Michael loses his older brother
    Francis, his all-consuming grief is compounded by
    the injustice of his brother's premature death.""",
    category=category1)

session.add(CategoryItem4)
session.commit()

CategoryItem5 = CategoryItem(
    user_id=1,
    name="YOU'RE ON AN AIRPLANE: A SELF-MYTHOLOGIZING MEMOIR BY PARKER POSEY",
    description="""Arguably one of the most beloved actresses of her
    generation-Posey opens up about her iconic film roles and her extraordinary
    life in this candid memoir that includes intimate reflections of her
    Southern childhood, mediations on the absurdity of fame, her favorite
    recipes, and original collages. Once again, she proves to be as original,
    refreshing, and funny as her most recognizable characters.""",
    category=category1)

session.add(CategoryItem5)
session.commit()

CategoryItem2 = CategoryItem(
    user_id=1,
    name="""BAD BLOOD: SECRETS AND LIES IN A SILICON VALLEY STARTUP BY JOHN
    CARREYROU""",
    description="""In 2015, Stanford dropout and founder of the biotech company
    Theranos Elizabeth Holmes was so ready to be the new Steve Jobs that she
    even wore the black turtleneck. Her intense unblinking stare and unbridled
    intensity convinced even the most seasoned investors, such as Larry Ellison
    and Tim Draper, that Theranos's blood testing machine-'the iPod of
    healthcare'-would revolutionize the medical industry. After one particular
    round of fund-raising, Theranos was valued at more than $9 billion. During
    this period, two-time Pulitzer Prize-winning Wall Street Journal reporter
    Carreyrou got a tip that the technology didn't work. He found that Holmes
    had been misleading investors and putting patients' lives at risk-and she
    didn't care. She willfully deceived Silicon Valley in what's become one of
    the biggest corporate frauds since Enron. Carreyrou's book is a compelling
    account of how his dogged reporting brought her down.""",
    category=category1)

session.add(CategoryItem2)
session.commit()


# category for food
category1 = Category(user_id=1, name="Food")

session.add(category1)
session.commit()


CategoryItem1 = CategoryItem(
    user_id=1,
    name="Lamb Curry",
    description="""Slow cook that thang in a pool of tomatoes, onions and all
    those tasty Indian spices. Mmmm.""",
    category=category1)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(
    user_id=1,
    name="Chicken Marsala",
    description="Chicken cooked in Marsala wine sauce with mushrooms",
    category=category1)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(
    user_id=1,
    name="Potstickers",
    description="Delicious chicken and veggies encapsulated in fried dough.",
    category=category1)

session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(
    user_id=1,
    name="Nigiri Sampler",
    description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
    category=category1)

session.add(CategoryItem4)
session.commit()

CategoryItem2 = CategoryItem(
    user_id=1,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category1)

session.add(CategoryItem2)
session.commit()


# category for film
category1 = Category(user_id=1, name="Film")

session.add(category1)
session.commit()

CategoryItem9 = CategoryItem(
    user_id=1,
    name="The Wizard of Oz (1939)",
    description="""The Wizard of Oz stars legendary Judy Garland as Dorothy, an
    innocent farm girl whisked out of her mundane earthbound existence into a
    land of pure imagination. Dorothy's journey in Oz will take her through
    emerald forests, yellow brick roads, and creepy castles, all with the help
    of some unusual but earnest song-happy friends.""",
    category=category1)

session.add(CategoryItem9)
session.commit()


CategoryItem1 = CategoryItem(
    user_id=1,
    name="Citizen Kane (1941)",
    description="""This is the labyrinthine study of the life of a
    newspaper tycoon.""",
    category=category1)

session.add(CategoryItem1)
session.commit()

CategoryItem2 = CategoryItem(
    user_id=1,
    name="Get Out (2017)",
    description="""Now that Chris and his girlfriend, Rose, have reached the
    meet-the-parents milestone of dating, she invites him for a weekend getaway
    upstate with Missy and Dean. At first, Chris reads the family's overly
    accommodating behavior as nervous attempts to deal with their daughter's
    interracial relationship, but as the weekend progresses, a series of
    increasingly disturbing discoveries lead him to a truth that he could have
    never imagined.""",
    category=category1)

session.add(CategoryItem2)
session.commit()

CategoryItem3 = CategoryItem(
    user_id=1,
    name="The Third Man (1949)",
    description="""American writer, Holly Martins, arrives in post-war Vienna
    to visit his old friend Harry Lime. On arrival, he learns that his friend
    has been killed in a street accident, but also that Lime was a black
    marketer wanted by the police.""",
    category=category1)

session.add(CategoryItem3)
session.commit()

CategoryItem4 = CategoryItem(
    user_id=1,
    name="Mad Max: Fury Road (2015)",
    description="""Filmmaker George Miller gears up for another
    post-apocalyptic action adventure with Fury Road, the fourth outing in the
    Mad Max film series. Charlize Theron stars alongside Tom Hardy (Bronson),
    with Zoe Kravitz, Adelaide Clemens, and Rosie Huntington Whiteley heading
    up the supporting cast.""",
    category=category1)

session.add(CategoryItem4)
session.commit()

CategoryItem2 = CategoryItem(
    user_id=1,
    name="The Cabinet of Dr. Caligari (Das Cabinet des Dr. Caligari) (1920)",
    description="""In one of the most influential films of the silent era,
    Werner Krauss plays the title character, a sinister hypnotist who travels
    the carnival circuit displaying a somnambulist named Cesare (Conrad Veidt).
    In one tiny German town, a series of murders coincides with Caligari's
    visit. When the best friend of hero Francis (Friedrich Feher) is killed,
    the deed seems to be the outgrowth of a romantic rivalry over the hand of
    the lovely Jane (Lil Dagover). Francis suspects Caligari, but he is ignored
    by the police. Investigating on his own, Francis seemingly discovers that
    Caligari has been ordering the somnambulist to commit the murders, but the
    story eventually takes a more surprising direction. Caligari's
    Expressionist style ultimately led to the dark shadows and sharp angles of
    the film noir urban crime dramas of the 1940s, many of which were directed
    by such German emigres as Billy Wilder and Robert Siodmak.""",
    category=category1)

session.add(CategoryItem2)
session.commit()

CategoryItem10 = CategoryItem(
    user_id=1,
    name="Inside Out (2015)",
    description="""Growing up can be a bumpy road, and it's no exception for
    Riley, who is uprooted from her Midwest life when her father starts a new
    job in San Francisco. Like all of us, Riley is guided by her emotions - Joy
    (Amy Poehler), Fear (Bill Hader), Anger (Lewis Black), Disgust
    (Mindy Kaling) and Sadness (Phyllis Smith). The emotions live in
    Headquarters, the control center inside Riley's mind, where they help
    advise her through everyday life. As Riley and her emotions struggle to
    adjust to a new life in San Francisco, turmoil ensues in Headquarters.
    Although Joy, Riley's main and most important emotion, tries to keep things
    positive, the emotions conflict on how best to navigate a new city, house
    and school.""",
    category=category1)

session.add(CategoryItem10)
session.commit()


print("added category items!")
