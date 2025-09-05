import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_multiple_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b', True)

    assert len(question.choices) == 2

    assert question.choices[0].text == 'a'
    assert not question.choices[0].is_correct

    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct

def test_remove_choice():
    question = Question(title='q1')
    
    question.add_choice('a')

    choice = question.choices[0]
    choice_id = choice.id
    
    question.remove_choice_by_id(choice_id)
    assert len(question.choices) == 0

def test_remove_non_existent_choice():
    question = Question(title='q1')
    
    question.add_choice('a')
    
    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b', True)

    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1', max_selections=2)

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')

    question.set_correct_choices([question.choices[1].id, question.choices[3].id])

    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct
    assert not question.choices[2].is_correct
    assert question.choices[3].is_correct

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    
    question.add_choice('a')
    question.add_choice('b', True)
    question.add_choice('c')
    question.add_choice('d', True)

    selected_ids = [question.choices[1].id, question.choices[3].id]
    correct_selected_ids = question.correct_selected_choices(selected_ids)

    assert len(correct_selected_ids) == 2
    assert question.choices[1].id in correct_selected_ids
    assert question.choices[3].id in correct_selected_ids

def test_correct_selected_choices_exceeding_max_selections():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b', True)

    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([question.choices[0].id, question.choices[1].id])

def test_add_choice_with_invalid_text():
    question = Question(title='q1')

    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')

def test_set_non_existent_choice_as_correct():
    question = Question(title='q1')
    
    question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id -1'):
        question.set_correct_choices([-1])

def test_create_question_with_empty_title():
    with pytest.raises(Exception, match='Title cannot be empty'):
        question = Question(title='')

@pytest.fixture
def question_with_multiple_choices():
    question = Question(title='q1', max_selections=2)

    question.add_choice('a')
    question.add_choice('b', True)
    question.add_choice('c')
    question.add_choice('d', True)

    return question

def test_correct_one_selected_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    selected_ids = [question.choices[1].id, question.choices[2].id]
    correct_selected_ids = question.correct_selected_choices(selected_ids)

    assert len(correct_selected_ids) == 1
    assert question.choices[1].id in correct_selected_ids

def test_all_wrong_selected_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    selected_ids = [question.choices[0].id, question.choices[2].id]
    correct_selected_ids = question.correct_selected_choices(selected_ids)

    assert len(correct_selected_ids) == 0