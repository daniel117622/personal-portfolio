from dataclasses import dataclass
from typing import List

from dtos import ValidCategories


@dataclass
class ImageBlock:
    img: str
    description: str


@dataclass
class TextBlock:
    text_content: str


@dataclass
class ArticleReadable:
    id: int
    title: str
    category : ValidCategories
    text_flow: List[ImageBlock | TextBlock]


def get_article_by_id(_id = 1) -> ArticleReadable:
    return ArticleReadable(
        id=1,
        title="Breaking the CPU Bottleneck with Cloud Functions",
        category=ValidCategories.ARTICLES(),
        text_flow=[
            TextBlock(
                text_content="""
                    <p style="line-height: 1.6; margin-bottom: 24px;">The cloud is a broad concept that encompasses servers and distributed computing 
                    accessible over the internet. In this discussion, I will explain how my understanding 
                    of computer science fundamentals helped me choose the right tools to solve a real 
                    problem I encountered while developing a chess gaming website. But first, let's 
                    define some key concepts related to this topic.</p>

                    <h3 style="margin-bottom: 16px;">Definitions:</h3>

                    <ul style="padding-left: 20px;">
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>REST API:</strong> A program that handles client requests, connects to 
                        a database, serves data, and manages authentication. It shouldn't do heavy CPU 
                        workloads as it could affect other client connections.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Horizontal Scaling:</strong> When more compute is needed more servers 
                        are added to the infrastructure, for this problem GCP functions provide on demand 
                        scaling very cheaply.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Vertical Scaling:</strong> The resources of the server are increased, 
                        a better CPU is added or more RAM or storage. Its the simpler solution, and it 
                        could be helpful if the server is unable to handle that many concurrent solutions. 
                        It’s not effective if individual requests are bottlenecking CPU usage, as the issue 
                        is with the processing power for each request, not overall server capacity.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Layering:</strong> This is a common a design pattern for API design. 
                        The logic for each endpoint is generally separated in this layers.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Authentication Layer:</strong> Verifies user identity and controls access.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Data Access Layer:</strong> Retrieves and stores data in the database.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Service Layer:</strong> Processes retrieved data, applying small 
                        computations before returning a response.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>CPU-Bound Task:</strong> A short computation-heavy process in the 
                        Service layer that manipulates or analyzes retrieved data before responding.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Cloud function:</strong> A serverless REST endpoint that behaves like 
                        a pure function, meaning that for a given input X, it always returns the same 
                        output Y. Cloud functions are highly data-dependent and stateless, meaning they 
                        do not retain state between invocations.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Minimax:</strong> An algorithm for building a tree from all possible 
                        positions in a game and then selecting the best one. This places high strain on 
                        the CPU.</li>
                    </ul>

                    <h3>What was the issue on my platform?</h3> 
                    <p>I am currently developing a chess platform where a player can challenge some premade 
                    AI bots. There was an endpoint that received the board state and the strategy that the 
                    player wanted to play against. This was working fine on a medium-sized EC2 instance, 
                    well, until I introduced a feature for streaming bot-vs-bot games.</p>

                    <p>With each connection to the streaming endpoint the minimax algorithm had to be 
                    executed back and forth causing a massive spike on CPU usage. I decided to make a 
                    stress test with just 3 simultaneous games and CPU quickly shot past 100%, crashing 
                    the container. Out of curiosity I upgraded to a larger $250 a month instance (Vertical 
                    scaling) and run the same tests, and not surprisingly with 5 players streaming games 
                    the server crashed.</p> 

                    <p>These findings led me to reconsider the role of an API. Through some reading, 
                    I found that performing CPU-intensive tasks is not typically part of its function. 
                    Yes, an API could handle a couple of hundred connections until it hits a limit, at 
                    which point I would need to upgrade. However, it shouldn't crash with just 3 or 5 
                    game streams.</p>

                    <h3>Solution</h3>
                    <p>Given that the task of an API is not to burn through CPU usage, my current approach 
                    was totally wrong. The only solution was to remove minimax from the server, as the 
                    definition of an API does not include to burn CPU usage on a single request.</p>
                    """
                                ),
                                ImageBlock(
                                    img="/static/images/articles/cpu1.png",
                                    description="The original endpoint ran Minimax for each connected "
                                    "client on the same server, causing CPU spikes. To fix this, I moved "
                                    "Minimax to a separate service.",
                                ),
                                TextBlock(
                                    text_content="""
                    <p>After that I realized that thanks to the well-layered design of the API, it was 
                    easy to remove the Minimax algorithm from the service layer and replace it with a 
                    request to a service that could handle the task. The service layer for this endpoint 
                    was simply a function that took data from the data access layer and returned a single 
                    result.</p> 

                    <p>A function? Wait, aren't there Cloud Functions? Sure enough, there are. After 
                    reading some documentation, I was pleased to find that Cloud Functions are pure, as 
                    defined in functional programming—providing a service where you send payload X and 
                    always get the same result back.</p>

                    <p>The only part that took a bit of time was implementing serialization methods for 
                    the arguments of the Minimax class. Notice that it accepts four parameters. I wrote a 
                    <code>.to_json()</code> and <code>.from_json()</code> method for the cloud function 
                    to deconstruct and reconstruct the inputs. Here's a code snippet illustrating the 
                    changes:</p>
                    """
                                ),
                                ImageBlock(
                                    img="/static/images/articles/cpu2.png",
                                    description="The server code does not contain any CPU-bound tasks. "
                                    "The minimax 'inference' was replaced by sending a network request "
                                    "and waiting for it.",
                                ),
                                TextBlock(
                                    text_content="""
                    <p style="line-height: 1.6; margin-bottom: 24px;">After moving the existing Minimax class to a separate folder and implementing the 
                    necessary code to deserialize the payload and reconstruct the inputs, the next logical 
                    step was to evaluate the new approach—using Cloud Functions.</p>

                    <h3 style="margin-bottom: 16px;">Cloud functions review</h3>

                    <p style="line-height: 1.6; margin-bottom: 24px;">With this new architecture in place, I turned my attention to assessing whether 
                    Cloud Functions would be a viable and cost-effective solution. After researching the 
                    service’s pricing model, I realized it was a perfect fit for my needs. Cloud Functions 
                    are priced based on CPU time and the number of invocations, which seemed ideal for my 
                    use case. To ensure the solution was economically viable, I ran a few calculations:</p>

                    <p style="line-height: 1.6; margin-bottom: 24px;">A full game stream requires up to 150 invocations, and with 100 players streaming 
                    10 games daily, the total monthly cost would be about $45. This allowed me to downgrade 
                    the server to an EC-small, where its only role was to store game data, handle 
                    matchmaking, and manage game streaming by calling the cloud function.</p>

                    <p style="line-height: 1.6; margin-bottom: 24px;">If this project takes off, I might need to move the function to another language 
                    like C or Rust, but for the moment being, Python is good enough.</p> 

                    <h3 style="margin-bottom: 16px;">Some conclusions</h3>

                    <p style="line-height: 1.6; margin-bottom: 24px;">What was needed to solve this problem? Was it necessary to take a certification of 
                    cloud technologies? Not at all, I think the three concepts that were needed where the 
                    following:</p>

                    <ul style="padding-left: 20px;">
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Follow the REST principles:</strong> From the beginning the API was 
                        following the philosophy of rest, even though at the beginning the code is more 
                        verbose, without this clean architecture separating the CPU-Bound task which was 
                        bringing the server down would be really hard. In this case the only challenge was 
                        to implement serialization methods on some existing classes.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>API Design:</strong> I want to emphasize how important it is to 
                        understand the responsibilities of an API. In this case, recognizing which tasks 
                        should and shouldn't be the API's responsibility was crucial. The API's job is to 
                        manage communication between components and ensure smooth data flow, but 
                        CPU-intensive tasks like the Minimax algorithm should be offloaded to other 
                        services designed to handle such workloads.</li>
                        
                        <li style="margin-bottom: 16px; line-height: 1.6;"><strong>Pure functions:</strong> Understanding the concept of pure functions 
                        was key to solving the problem. The bottleneck in this scenario stemmed from the 
                        Minimax function itself, and recognizing that I had to work on serializing this 
                        classes so they could be offloaded to a different service.</li>
                    </ul>

                    <p style="line-height: 1.6; margin-bottom: 24px;">With these insights in mind, it became easy to ask AI for guidance on the right 
                    tools to look up in Google Cloud. Additionally, this understanding enabled me to make 
                    quick cost estimations and motivated me to tackle the problem hands-on. After making 
                    this changes I tested the server running multiple games and the CPU usage didn't spike 
                    at all. For the moment the costs are fine for the size of the project.</p>
                    """
                                ),
                            ],
                        )


