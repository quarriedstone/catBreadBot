Feature: changing of states
    Testing if the states of bot are changing according to function calls

    Scenario: start the conversation with bot
        Given a bot and new update
        When user sends /start
        Then change state to QUESTION1
    Scenario Outline: answer first question
        Given a bot in step QUESTION1
        When user sends "<message>" for first question
        Then it should change state to "<state>"

        Examples: Positive
        | message | state |
        | да      | 1     |
        | конечно | 1     |
        | пожалуй | 1     |
        | ага     | 1     |

        Examples: Negative
        | message      | state |
        | нет          | -1    |
        | нет, конечно | -1    |
        | ноуп         | -1    |
        | найн         | -1    |

        Examples: Not matched
       | message      | state |
       | тест         | 0     |
    Scenario Outline: answer second question
       Given a bot in step QUESTION2
       When user sends "<message>" for second question
       Then it should change state to "<state>"

       Examples: Positive
       | message      | state |
       | да           | -1    |
       | конечно      | -1    |
       | пожалуй      | -1    |
       | ага          | -1    |
       | нет          | -1    |
       | нет, конечно | -1    |
       | ноуп         | -1    |
       | найн         | -1    |

       Examples: Not matched
       | message      | state |
       | тест         | 1     |
