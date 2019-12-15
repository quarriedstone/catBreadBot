from unittest.mock import Mock
from behave import given, when, then
from bot.CatBreadBot import CatBreadBot


@given('a bot and new update')
def step_impl(context):
    context.bot = Mock()
    context.update = Mock()
    context.dispatcher = Mock()
    context.test_bot = CatBreadBot(dispatcher=context.dispatcher)


@when('user sends /start')
def step_impl(context):
    context.init_step = context.test_bot.start(context.update, context)


@then('change state to QUESTION1')
def step_impl(context):
    assert context.init_step == context.test_bot.QUESTION1


@given('a bot in step QUESTION1')
def step_impl(context):
    context.bot = Mock()
    context.update = Mock()
    context.dispatcher = Mock()
    context.update.message.from_user = type('TelegramUser', (object,), {'first_name': 'test_user'})
    context.test_bot = CatBreadBot(dispatcher=context.dispatcher)


@when('user sends "{message}" for first question')
def step_impl(context, message):
    context.update.message.text = message
    context.next_step = context.test_bot.question_cube(update=context.update, context=context)


@given('a bot in step QUESTION2')
def step_impl(context):
    context.bot = Mock()
    context.update = Mock()
    context.dispatcher = Mock()
    context.update.message.from_user = type('TelegramUser', (object,), {'first_name': 'test_user'})
    context.test_bot = CatBreadBot(dispatcher=context.dispatcher)


@when('user sends "{message}" for second question')
def step_impl(context, message):
    context.update.message.text = message
    context.next_step = context.test_bot.question_ears(update=context.update, context=context)


@then('it should change state to "{state}"')
def step_impl(context, state):
    assert context.next_step == int(state)
