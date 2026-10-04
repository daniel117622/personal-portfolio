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
    )
]

# 3. Serialize the dataclasses to dictionaries for MongoDB
serialized_text_flow = [asdict(block) for block in text_flow]

# 4. Connect to the MongoDB container
client = MongoClient("mongodb://localhost:27017/")
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