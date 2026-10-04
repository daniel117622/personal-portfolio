from dataclasses import dataclass, asdict
from pymongo import MongoClient

# 1. Define your dataclasses
@dataclass
class ImageBlock:
    img: str
    description: str

@dataclass
class TextBlock:
    text_content: str

# 2. Define the new text_flow array
text_flow = [
    TextBlock(
        text_content="""
            <h3>Introduction</h3>
            <p>With the rise of AI, its very common to interact with chatbots that help you complete a task, this can be things like, placing orders for a product, making an appointment or booking a flight. Aside from the LLM that is powering this apps, do you know what are the two fundamentals datastructures that can hold this systems together? If you are interested in learning how this systems work, and how to build one yourself, keep reading the article.</p>

            <p>You might think, "Isn't it easier to hack together a bunch of nested if-else statements?". That would work, but depending on the edge-cases or business rules you are handling, every new feature gets exponentially harder to code. This is a mathematical fact, because this "hack" is you modeling the chatbot as a finite state machine ( FSM ), which is the wrong data structure for this task.</p>

            <h3>Definitions</h3>
            <ul>
                <li><strong>Business rules:</strong> In software design, business rules describe what the client needs the chatbot to do, by specifying which choices to display first, which actions the user can take, and ensuring that navigation through the chatbot is intuitive and easy to follow.</li>
                <li><strong>Knowledge:</strong> In this context, knowledge refers to the chatbot’s access to shared data or global state, such as current user session details, booking information, or configuration settings. Rather than relying on hidden globals, we explicitly pass the necessary variables into each menu or handler object.</li>
                <li><strong>Finite State Machine (FSM):</strong> Its a graph that has information about which states are valid, a description on which transitions are possible and how they are triggered. It cannot hold any knowledge beyond its current state.</li>
                <li><strong>Pushdown Automata (PDA):</strong> It contains an FSM but it also contains a stack, which is a data structure that serves as memory, you can push and pop items off. In this case is used to have knowledge about the previous options.</li>
                <li><strong>Composite pattern:</strong> A design pattern that uses object‐oriented programming to build tree‐like components. Each individual component implements the same interface, which defines how a node can open submenus, perform actions, or return to the previous menu.</li>
            </ul>
        """
    ), 
    TextBlock(
        text_content="""
            <h3>Why am I writing about this?</h3>
            <p>Data structures, chatbots, and the Composite pattern might seem unrelated at first, but I discovered their connection while building a GUI for database operations. The interface needed to validate inputs, execute read queries, safely write to the database, and even roll back those writes if necessary. At first, I vibe-coded everything together but my code was a mess, it was hard to follow and very hard to implement the features I had to write so I decided to throw it away and start over.</p>

            <p>I had to step back and think carefully about which abstraction would truly model the problem. I knew it involved a state machine or a design pattern, though I wasn’t sure which one. After several conversations with an AI assistant and plenty of experimentation, I finally landed on the right solution: a Composite-pattern hierarchy combined with a Pushdown Automaton will model the problem perfectly. Some random data structures I learned in college suddenly made sense and helped me solve the task. Finding this so interesting, I decided to write about my findings in the hope that they might help other developers facing similar challenges.</p>
        """
    ),
    TextBlock(
        text_content="""
            <h3>The solution.</h3>
            <p>The code I will show belongs to some tests I was doing using a simpler set of business rules, it was a toy problem which helped me nail down the best way to place this knowledge together. The following snippet of code shows the relationship between each component. There are some debug.</p>
            
            <p>Its important to notice that some variables are passed into the constructors of the classes, this describes that that class has "knowledge" about the PDA and the DB which are shared variables. The DB is just a file in disk, but could be replaced by a connection or something else.</p>
        """
    ),
    ImageBlock(
        img="/static/images/articles/composite1.png",
        description="The program runs in a loop until the user decides to exit"
    ),
    TextBlock(
        text_content="""
            <p>First, I’ll show you how to implement the Composite pattern we discussed. In this design, every component must implement the same interface. My <code>IMenuBehaviour</code> interface enforces that each menu class:</p>
            <ol>
                <li>Defines a <code>submenus</code> dictionary for child menus.</li>
                <li>Defines an <code>actions</code> dictionary for executing a process (e.g., adding a product or printing the current list of products). In general, it is a dictionary that maps a choice to a function.</li>
                <li>Accepts a reference to the shared Pushdown Automaton (PDA) so the composite can handle navigation and state. This is done easily by calling the following method.</li>
            </ol>

            <p>Finally, it tells you to use the PDA to either jump into a submenu or to go back to the previous menu. For the purposes of writing this article, I wrote a function that lays out the menu—it simply shows you the name of the class and whether or not it contains other instances of <code>MenuBehaviour</code>.</p>

            <p>Below is a snippet of code that shows how the Composite pattern looks in practice. Notice how easy it is to read what a menu item will do, as well as how straightforward it is to add nested menus:</p>
        """
    ),
    ImageBlock(
        img="/static/images/articles/composite2.png",
        description="The IMenuBehaviour tells you what properties the class should have and how you should use the PDA to perform the navigation."
    ),
    TextBlock(
        text_content="""
            <p>The composite pattern is not enough for an options menu to work. To help you understand whats the role of the PDA I will show how it looks while navigating the menu. As the definition tells you, a PDA is just a FSM with the added bonus of a memory section, which is just a list containing data, this data can be accessed at any moment.</p>
            
            <p>Here the FSM is the information about the current action being performed, and some metadata like submenus and stack_depth, but in practice it could hold anything, and the stack here is represented as the list, which is used by each instance to navigate back and forth. Without this stack, navigating back and forth will be harder as you will need some sort of global variable to carry this knowledge, by using the PDA class the navigation becomes easy.</p>
        """
    ),
    ImageBlock(
        img="/static/images/articles/composite3.png",
        description="The PDA holds the logic to run the program. It displays the available options, reads user input and handles navigation swiftly."
    ),
    TextBlock(
        text_content="""
            <p>This example shows only the bare-bones of my stack-based structure. In a real-world app, you would want to use the same setup but hold richer state. For example, shopping cart contents, payment status, session data, etc. While the stack’s 'memory' helps you manage the user flow through your application. You just need to handle some edge cases, like the user quitting or popping an empty stack, which will indicate the user exiting the app.</p>

            <p>On the other hand, the composition pattern gives you an instant map of every path a user might take. You could even get fancy and build your menus up from a JSON file, in which you could create or modify the layout without writing more code. The flow of the user could be defined in this file and the programmer is just left with the task of implementing the actions that the user should perform in that section.</p>

            <p>I won’t dive into the technical details as that gets into the topic of metaprogramming, but the power of Composite really shines here. Below is a screenshot of this program’s structure; since it’s just a toy example, most submenu methods are left unimplemented. The composite pattern allows you to visualize the entire program workflow at runtime. You could get fancy and also show the actions that the user could perform at each level.</p>
        """
    ),
    ImageBlock(
        img="/static/images/articles/composite4.png",
        description="The composite pattern allows you to implement methods to visualize the program workflow at runtime. You could get fancy and also show actions that the user could perform at each level."
    ),
    TextBlock(
        text_content="""
            <p>All of this is overkill for this example. You are better off just doing your system with if-else statements. But when you want to scale a system like chatbots that have to handle large amounts of cases in an scalable manner, this is one of the best ways to tackle the problem. As I've been gaining experience working as a SWE, it's really satisfying when some of the stuff I thought as useless comes to the rescue when you need a reliable way to solve a problem.</p>

            <p>While researching this topic, I became sure that real world systems use something very akin to this to build chatbots. Or if they don't it's probably a mess and hard to work on pushing new features. If someone who actually works with this type of systems it would be great to know what type of architecture they use.</p>
        """
    ),
    TextBlock(
        text_content="""
            <h3>Conclusion</h3>
            <p>When working with complex problems in software engineering, it’s always good to step back and think about what you’re doing. If something feels hard to achieve, chances are you’re not using the right set of tools. This article—and the research behind it—stems from an annoying problem I ran into, which forced me to ask: which data structure really models the behavior I needed?</p>

            <p>I knew a pushdown automaton would be central to the solution, but something was still missing. So I resorted to asking AI for help pairing the PDA with some design pattern, and the suggestion of using the Composite Pattern made all the pieces fit together perfectly.</p>

            <p>That really made me happy and motivated me to write about it. Is this the sort of challenge that leads Big Tech to rely so much on LeetCode interviews? Maybe they’re looking for people who can spot and apply the right tool for any job.</p>

            <h3>References</h3>
            <ul>
                <li><a href="https://medium.com/dotcrossdot/hierarchical-finite-state-machine-c9e3f4ce0d9e" target="_blank">Article that describes the complexities of modeling games with FSM</a>. It describes the phenomenon of "state explosion" when adding more rules or behaviours.</li>
                <li><a href="https://refactoring.guru/design-patterns/composite" target="_blank">Composite design pattern</a>. It explains its use cases and also its drawbacks.</li>
                <li><a href="https://dev.to/karishmashukla/a-practical-guide-to-metaprogramming-in-python-691" target="_blank">An explanation of Metaprogramming</a>. It is an advanced python topic that allows you to use the type() constructor to create classes at runtime.</li>
                <li><a href="https://github.com/daniel117622/pda-article.git" target="_blank">The code I used for the screenshots</a>. You can take a look at it on Github, most of the methods are not implemented, as that wasn't the point of it[cite: 2].</li>
            </ul>
        """
    )
]

# 3. Serialize the dataclasses to dictionaries for MongoDB
serialized_text_flow = [asdict(block) for block in text_flow]

# 4. Connect to the MongoDB container
from dotenv import load_dotenv
import os
load_dotenv()
conn_str = os.environ["MONGO_CONN_STR"]
client = MongoClient(conn_str)
print(conn_str)
db = client["blog_db"]

collection = db["articles"] 

# 5. Execute the update targeting the document with id: 1
result = collection.update_one(
    {"id": 1}, 
    {"$set": {"text_flow": serialized_text_flow}}
)

# 6. Verify the operation
print(f"Documents matched: {result.matched_count}")
print(f"Documents modified: {result.modified_count}")