flowchart TD
    Start([New Exercise]) --> Read[Read Exercise 2-3 Times]
    Read --> Understand{Can I explain\nit simply?}

    Understand -->|No| Clarify[Ask Questions\nRe-read]
    Clarify --> Understand

    Understand -->|Yes| Inputs[Identify Inputs,\nOutputs, Constraints]
    Inputs --> Edge[List Edge Cases]
    Edge --> Break[Break into\nSub-problems]
    Break --> Manual[Solve by Hand\nWithout Code]
    Manual --> Pseudo[Write Pseudocode]
    Pseudo --> Choose[Choose Data Structures\n& Algorithms]

    Choose --> Implement1[Implement First\nSub-problem]
    Implement1 --> Test1{Does it work?}

    Test1 -->|No| Debug1[Debug This Piece]
    Debug1 --> Test1

    Test1 -->|Yes| More{More\nsub-problems?}
    More -->|Yes| ImplementNext[Implement Next Piece]
    ImplementNext --> TestNext{Works?}

    TestNext -->|No| DebugNext[Debug]
    DebugNext --> TestNext

    TestNext -->|Yes| More
    More -->|No| TestAll[Test All Cases:\nSimple, Complex, Edge]

    TestAll --> AllPass{All tests pass?}
    AllPass -->|No| DebugFinal[Debug Issues]
    DebugFinal --> TestAll

    AllPass -->|Yes| Compare[Compare with\nSample Solution]
    Compare --> Analyze[Analyze Differences]
    Analyze --> Refactor{Need to\nrefactor?}

    Refactor -->|Yes| Optimize[Optimize Code]
    Optimize --> Document[Document Learnings]

    Refactor -->|No| Document
    Document --> End([Exercise Complete])

    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style Understand fill:#fff4e1
    style Test1 fill:#fff4e1
    style TestNext fill:#fff4e1
    style AllPass fill:#fff4e1
    style Refactor fill:#fff4e1
