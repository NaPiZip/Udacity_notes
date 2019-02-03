<img src="https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.l8H7yN_ZVoz_SCzv3qD4ngHaFd%26pid%3D15.1&f=1" alt="Udacity Logo" height="42px" width="42px" align="left">

# Designing RESTful APIs
<div>
    <a href="https://github.com/NaPiZip/Docker_GUI_Apps_on_Windows">
        <img src="https://img.shields.io/badge/Document%20Version-1.0.0-brightgreen.svg"/>
    </a>
    <a href="https://www.microsoft.com">
        <img src="https://img.shields.io/badge/Windows%2010%20x64-10.0.17134%20Build%2017134-blue.svg"/>
    </a>
</div>

## Objectives
These are my notes of the Udacity course `Designing RESTful APIs`. I am only covering details which I think are important for me. This document is not supposed to be a summary of all the content covered by the course, it's just a centralized place to store information in order to support my learning process. A lot of information is online nowadays and I think it's not needed to memorize all details, it's more important to have a solid overview and to know where to look for the details.

##  What's and Why's of APIs

**What are APIs**<br>
APIs are application programming interfaces, APIs can be described as building blocks of software components or applications. A comprehensive metaphor is a wall socket, the socket represents a interface to a service better know as electricity. The user is comfortable able to use the service if he is in compliance with the policy of the service provider, meaning if the consumer decides to agree on a contract with a energy provider, then the provider invokes the rights for the user to access the service, though out a defined interface the wall socket. The wall socket has specific properties, such as a physical shape for a plug as well as a defined voltage and a maximum current. Those properties are defined by the service provider, e.g. the API provider. A more formal definition is the following one:<br>

*In computer programming, an application programming interface (API) is a set of subroutine definitions, communication protocols, and tools for building software. In general terms, it is a set of clearly defined methods of communication among various components. A good API makes it easier to develop a computer program by providing all the building blocks, which are then put together by the programmer. An API may be for a web-based system, operating system, database system, computer hardware, or software library [Wikipedia](https://en.wikipedia.org/wiki/Application_programming_interface).*   

**Web APIs**<br>
A web API is a specific type of API which is used for either a web server or web browser, they are typically HTTP based.  The API itself defines a set of endpoints, request messages and response structures. It is a standard approach also to identify the supported response media types. XML and JSON are two favorite examples of response media types that can be easily interpreted by API consumers.

**The OSI layers**<br>
The Open System Interconnection (OSI) is a reference model for how various applications communicate over any network. The purpose behind this model was to provide developers, programmers, engineers, vendors and all the associated people a standard that can serve as a guide for them using which they would be able to create communication equipment and software inter operable. The following image shows the seven layers of the OSI model and its use protocols, a detailed description can be found [here](https://www.bmc.com/blogs/osi-model-7-layers/).

<p align="center">
<img src="https://raw.githubusercontent.com/NaPiZip/Udacity_notes/master/Designing_RESTful_APIs/Images/osi-model-7.jpg" alt="Object diagram example"/></p>

**The Web Service Layer**<br>
In a web service, the Web technology such as HTTP—originally designed for human-to-machine communication—is utilized for machine-to-machine communication, more specifically for transferring machine-readable file formats such as XML and JSON. In practice, a web service commonly provides an object-oriented web-based interface to a database server, utilized for example by another web server, or by a mobile app, that provides a user interface to the end user. Many organizations that provide data in formatted HTML pages will also provide that data on their server as XML or JSON, often through a web service to allow syndication, for example Wikipedia's Export. Another application offered to the end user may be a mashup, where a web server consumes several web services at different machines, and compiles the content into one user interface [Wikipedia](https://en.wikipedia.org/wiki/Web_service).

When talking about API (application programming interface) architectures, it’s common to want to compare SOAP vs. REST, two of the most common API paradigms.

**REST**<br>
REST determines how the API looks like. It stands for “Representational State Transfer”. It is a set of rules that developers follow when they create their API. One of these rules states that you should be able to get a piece of data (called a resource) when you link to a specific URL.

Each URL is called a request while the data sent back to you is called a response.

- REST is all about simplicity, thanks to HTTP protocols.
- REST APIs facilitate client-server communications and architectures. If it’s RESTful, it’s built on this client-server principle, with round trips between the two passing payloads of information.
- REST APIs use a single uniform interface. This simplifies how applications interact with the API by requiring they all interface in the same way, through the same portal. This has advantages and disadvantages; check with your developer to see if this will affect implementation changes down the road.
- REST is optimized for the web. Using JSON as its data format makes it compatible with browsers.
- REST is known for excellent performance and scalability. But, like any technology, it can get bogged down or bog down your app. That’s why languages like GraphQL have come along to address problems even REST can’t solve [UpWork](https://www.upwork.com/hiring/development/soap-vs-rest-comparing-two-apis/).

**SOAP**<br>
SOAP (Simple Object Access Protocol) is its own protocol, and is a bit more complex by defining more standards than REST—things like security and how messages are sent. These built-in standards do carry a bit more overhead, but can be a deciding factor for organizations that require more comprehensive features in the way of security, transactions, and ACID (Atomicity, Consistency, Isolation, Durability) compliance.

- SOAP has tighter security. WS-Security, in addition to SSL support, is a built-in standard that gives SOAP some more enterprise-level security features, if you have a requirement for them.
- Successful/retry logic for reliable messaging functionality. Rest doesn’t have a standard messaging system and can only address communication failures by retrying. SOAP has successful/retry logic built in and provides end-to-end reliability even through SOAP intermediaries.
- SOAP has built-in ACID compliance. ACID compliance reduces anomalies and protects the integrity of a database by prescribing exactly how transactions can interact with the database. ACID is more conservative than other data consistency models, which is why it’s typically favored when handling financial or otherwise sensitive transactions [UpWork](https://www.upwork.com/hiring/development/soap-vs-rest-comparing-two-apis/).