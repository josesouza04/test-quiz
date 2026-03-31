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


def test_add_choice_with_empty_text_raises():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)


def test_add_choice_with_too_long_text_raises():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)


def test_choice_ids_increment_from_one():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3


def test_remove_choice_by_id_removes_only_target():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(1)
    ids = [c.id for c in question.choices]
    assert ids == [2]


def test_remove_choice_with_invalid_id_raises():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert question.choices == []


def test_set_correct_choices_and_correct_selected_choices():
    question = Question(title='q1', max_selections=3)
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.set_correct_choices([1, 3])
    result = question.correct_selected_choices([1, 2, 3])
    assert result == [1, 3]


def test_correct_selected_choices_raises_when_exceeding_max():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a')
    question.add_choice('b')
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2])


def test_points_out_of_bounds_raise():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)